import smbclient
import shutil
from src.utils import *
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='smbsync',
        description='🔄 smbsync: Sincroniza carpetas locales con servidores SMB fácilmente.',
        epilog='Ejemplo de uso: smbsync sync --target \\\\192.168.1.100\\MiCarpeta'
    )

    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')

    # Comando "sync"
    sync_parser = subparsers.add_parser('sync', help='Sincroniza con una carpeta SMB remota')
    # sync_parser.add_argument('--target', required=True, help='Ruta remota SMB (ej: \\\\192.168.1.100\\Carpeta)')
    # sync_parser.add_argument('--local', default='.', help='Ruta local a sincronizar')

    upload_file_parser = subparsers.add_parser('upload-file',
                                               help='Sube un archivo específico al recurso compartido SMB')
    upload_file_parser.add_argument('--file', required=True, help='Ruta del archivo local a subir')
    upload_file_parser.add_argument('--remote-folder', required=True, help='Ruta remota en el recurso compartido SMB')

    # Comando "install"
    subparsers.add_parser('install', help='Realiza instalación inicial del programa')

    # Comando "test"
    subparsers.add_parser('test', help='Comando para ejecuciones de prueba')

    subparsers.add_parser('prune', help='Elimina todos los usuarios almacenados')

    # Comando "test"
    subparsers.add_parser('reinstall', help='Reinicia el registro de usuarios y servidores samba')

    # Comando "uninstall"
    subparsers.add_parser('uninstall', help='Elimina la base de datos y configuración')

    add_user_parser = subparsers.add_parser('add-user', help='Agrega un nuevo usuario Samba')
    add_user_parser.add_argument('--name', required=True, help='Nombre de usuario')
    add_user_parser.add_argument('--password', required=True, help='Contraseña del usuario')
    add_user_parser.add_argument('--host', required=True, help='Ruta del host SMB (ej: \\\\192.168.1.50\\Carpeta)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'sync':
        print(f"📡 Sincronizando ")
        from src.database.ORM import ORM
        from src.Samba import SambaConnection
        orm = ORM()
        user_info = orm.get_first_user()

        if not user_info:
            print("No hay usuarios de Samba registrados")
            return

        user_info = user_info[0]
        conn = SambaConnection(user_info["name"], user_info["password"], user_info["host_connection"])
        conn.upload_folder(get_currentshell_path(), f'\\{user_info["host_connection"]}\\smbSyncFolder')

    if args.command == 'reinstall':
        from src.scripts.uninstall import uninstall
        uninstall()
        from src.scripts.install import make_installation
        make_installation()

    elif args.command == 'upload-file':
        """ 
            Subir un archivo específico al recurso compartido SMB.

            Ejemplo: smbsync upload-file --file /ruta/local/archivo.txt --remote-folder \\servidor\recurso
            smbsync upload-file --file /home/yeisongonz/Work/PersonalProjects/smbSync/install_smb.sh --remote-folder //192.168.1.32/DellSmb/Documentos
        """
        from src.database.ORM import ORM
        from src.Samba import SambaConnection
        orm = ORM()
        user_info = orm.get_first_user()

        if not user_info:
            print("No hay usuarios de Samba registrados")
            return

        user_info = user_info[0]
        conn = SambaConnection(user_info["name"], user_info["password"], user_info["host_connection"])

        try:
            conn.upload_file(local_file=args.file, remote_folder=args.remote_folder)
        except Exception as e:
            print(f"❌ Error al subir el archivo: {e}")

    elif args.command == 'prune':
        """
            Delete all Samba users
        """
        from src.database.ORM import ORM
        orm = ORM()
        orm.prune_users()


    elif args.command == 'add-user':
        """ 
            Insertar un nuevo usuario del servidor de samba
             
            Ejemplo: smbsync add-user --name usuario --password 'password' --host 
        """

        from src.database.ORM import ORM
        orm = ORM()
        user_id = orm.add_user(
            name=args.name,
            password=args.password,
            host_connection=args.host
        )
        print(f"✅ Usuario agregado correctamente con ID {user_id}")



    elif args.command == 'test':
        from src.database.ORM import ORM
        from src.Samba import SambaConnection
        orm = ORM()
        user_info = orm.get_first_user()

        if not user_info:
            print("No hay usuarios de Samba registrados")
            return

        user_info = user_info[0]
        conn = SambaConnection(user_info["name"], user_info["password"], user_info["host_connection"])
        conn.test_connection()



    elif args.command == 'install':
        print("⚙️ Ejecutando instalación...")
        from src.scripts.install import make_installation
        make_installation()
    elif args.command == 'uninstall':
        print("❌ Desinstalando...")
        # uninstall()

if __name__ == '__main__':
    main()
