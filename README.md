
# 🚀 **smbsync** – Sincronización fácil con servidores Samba

**smbsync** es una herramienta de línea de comandos hecha en Python 🐍 que facilita la sincronización de carpetas locales y remotas, así como la gestión de usuarios en servidores Samba (SMB). Ideal para administradores o usuarios que buscan rapidez y eficiencia.

## 🛠️ Características principales

- 🔁 **Sincronización** de carpetas locales con servidores SMB.
- 📤 **Subida de archivos** específicos a carpetas remotas.
- 👥 **Gestión de usuarios Samba** (agregar, eliminar, listar).
- ⚙️ **Instalación y configuración** del entorno con un solo comando.
- 🔄 **Reinstalación** o 🧹 **desinstalación** completa del sistema.

---

## 📦 Requisitos previos

1. Python **3.8 o superior** instalado.
2. Instalacion del programa:

   ```bash
   source ./install_smb.sh
   ```

   1. Tras instalar el programa deberas hacer una instalacion de los requisitos:
   ```bash
   smbsync install 
   ```


3. Un servidor Samba configurado con permisos adecuados.

---

## 🧭 Comandos disponibles

### 🔄 `sync`
Sincroniza una carpeta local con una remota.

```bash
smbsync sync
```

✔ Usa el primer usuario registrado para autenticarse.  
✔ Copia todos los archivos y subcarpetas desde el directorio actual hacia una carpeta remota predefinida.

---

### 📤 `upload-file`
Sube un archivo específico a una carpeta remota.

```bash
smbsync upload-file --file <ruta_local> --remote-folder <ruta_remota>
```

- `--file`: Ruta del archivo local.
- `--remote-folder`: Carpeta destino en el servidor Samba.

📌 **Ejemplo:**

```bash
smbsync upload-file --file /home/usuario/documento.txt --remote-folder //192.168.1.2/Resource/Documentos
```

---

### ➕ `add-user`
Agrega un nuevo usuario para conectarse al servidor SMB.

```bash
smbsync add-user --name <nombre_usuario> --password <contraseña> --host <ruta_host>
```

📌 **Ejemplo:**

```bash
smbsync add-user --name admin --password admin123 --host //192.168.1.02/Resource
```

---

### 🧹 `prune`
Elimina todos los usuarios registrados.

```bash
smbsync prune
```

⚠️ Borra todos los registros de usuarios en el sistema.

---

### 🧪 `test`
Verifica la conexión y credenciales con el servidor Samba.

```bash
smbsync test
```

🔍 Comprueba si las credenciales del primer usuario son válidas y si el servidor responde.

---

### ⚙️ `install`
Instala y configura `smbsync` por primera vez.

```bash
smbsync install
```

🧰 Automatiza la configuración inicial del entorno.

---

### 🔁 `reinstall`
Reinstala completamente `smbsync` desde cero.

```bash
smbsync reinstall
```

🧨 Elimina datos existentes y reinicia la configuración.

---

### ❌ `uninstall`
Desinstala completamente `smbsync`.

```bash
smbsync uninstall
```

🗑️ Borra todos los archivos y configuraciones relacionadas con el programa.

---

## 🎯 Ejemplos prácticos

📷 Subir una imagen:
```bash
smbsync upload-file --file /home/usuario/foto.jpg --remote-folder //192.168.1.2/Resource/Fotos
```

👤 Agregar usuario:
```bash
smbsync add-user --name admin --password admin123 --host //192.168.1.2/Resource/RecursosCompartidos
```

📁 Sincronizar carpeta actual:
```bash
smbsync sync
```

🔍 Probar conexión:
```bash
smbsync test
```

🧽 Eliminar usuarios:
```bash
smbsync prune
```

---

## 📝 Notas adicionales

- 📐 Asegúrate de usar rutas correctas en formato `//servidor/recurso`.
- 🔐 Verifica que el usuario tenga permisos suficientes en las carpetas remotas.
- 📚 Consulta la documentación oficial de [`smbprotocol`](https://pypi.org/project/smbprotocol/) para más información.

---
