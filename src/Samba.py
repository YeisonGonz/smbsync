import os
import smbclient
import smbprotocol
import shutil
from smbprotocol.exceptions import LogonFailure


class SambaConnection:
    def __init__(self, username, password, host):
        self.username = username
        self.password = password
        self.host = host

    def test_connection(self):
        try:
            smbclient.ClientConfig(username=self.username, password=self.password)
            smbclient.listdir(self.host)
            print("✅ Conexión exitosa a Samba.")
            return True
        except LogonFailure as auth_error:
            raise ValueError(
                f"❌ Error de autenticación: Credenciales incorrectas para el host {self.host}"
            ) from auth_error
        except Exception as e:
            raise ConnectionError(f"❌ Error al conectar con el host {self.host}: {e}") from e

    def upload_folder(self, local_folder: str, remote_folder: str):
        """Sube todos los archivos y carpetas de una carpeta local al recurso compartido Samba.

        Args:
            local_folder (str): Ruta de la carpeta local.
            remote_folder (str): Ruta remota en el recurso compartido Samba.
        """
        try:
            smbclient.ClientConfig(username=self.username, password=self.password)

            if not os.path.exists(local_folder):
                raise FileNotFoundError(f"La carpeta local '{local_folder}' no existe.")

            # Verifica si la carpeta remota existe, si no, la crea
            try:
                smbclient.listdir(remote_folder)
                print(f"📁 Carpeta remota encontrada: {remote_folder}")
            except smbprotocol.exceptions.SMBOSError as e:
                if "No such file or directory" in str(e):
                    smbclient.mkdir(remote_folder)
                    print(f"📁 Carpeta remota creada: {remote_folder}")
                else:
                    raise ConnectionError(f"❌ Error al verificar la carpeta remota: {e}") from e

            # Itera sobre los archivos y carpetas en la carpeta local
            for item in os.listdir(local_folder):
                local_item_path = os.path.join(local_folder, item)
                remote_item_path = f"{remote_folder}/{item}"

                if os.path.isfile(local_item_path):  # Si es un archivo, lo sube
                    with open(local_item_path, "rb") as file:
                        with smbclient.open_file(remote_item_path, mode="wb") as remote_file:
                            shutil.copyfileobj(file, remote_file)
                            print(f"⬆️ Archivo subido: {local_item_path} -> {remote_item_path}")
                elif os.path.isdir(local_item_path):  # Si es una carpeta, llama recursivamente a upload_folder
                    print(f"📂 Encontrada subcarpeta: {local_item_path}. Creando en remoto...")
                    self.upload_folder(local_item_path, remote_item_path)

            print("✅ Todos los archivos y carpetas han sido subidos correctamente.")
        except Exception as e:
            raise ConnectionError(f"❌ Error al subir archivos: {e}") from e

    def upload_file(self, local_file: str, remote_folder: str):
        """Sube un archivo específico al recurso compartido Samba.

        Args:
            local_file (str): Ruta del archivo local.
            remote_folder (str): Ruta remota en el recurso compartido Samba.
        """
        try:
            smbclient.ClientConfig(username=self.username, password=self.password)

            if not os.path.isfile(local_file):
                raise FileNotFoundError(f"El archivo local '{local_file}' no existe o no es un archivo válido.")

            # Verifica si la carpeta remota existe, si no, la crea
            try:
                smbclient.listdir(remote_folder)
                print(f"📁 Carpeta remota encontrada: {remote_folder}")
            except smbprotocol.exceptions.SMBOSError as e:
                if "No such file or directory" in str(e):
                    smbclient.mkdir(remote_folder)
                    print(f"📁 Carpeta remota creada: {remote_folder}")
                else:
                    raise ConnectionError(f"❌ Error al verificar la carpeta remota: {e}") from e

            # Subir el archivo al recurso compartido remoto
            remote_file_path = f"{remote_folder}/{os.path.basename(local_file)}"
            with open(local_file, "rb") as file:
                with smbclient.open_file(remote_file_path, mode="wb") as remote_file:
                    shutil.copyfileobj(file, remote_file)
                    print(f"⬆️ Archivo subido: {local_file} -> {remote_file_path}")

            print("✅ Archivo subido correctamente.")
        except Exception as e:
            raise ConnectionError(f"❌ Error al subir el archivo: {e}") from e