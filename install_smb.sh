#!/bin/sh

set -e

echo "🚀 Iniciando instalación de smbsync..."

INSTALL_DIR="$(pwd)"
WRAPPER_PATH="/usr/local/bin/smbsync"
VENV_PATH="$INSTALL_DIR/.venv"

# Crear entorno virtual si no existe
if [ ! -d "$VENV_PATH" ]; then
    echo "🐍 Creando entorno virtual..."
    python3 -m venv "$VENV_PATH"
else
    echo "📦 Entorno virtual ya existe"
fi

# Activar entorno e instalar dependencias
echo "📦 Instalando dependencias..."
. "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install -r "$INSTALL_DIR/requirements.txt"
deactivate

# Crear wrapper con rutas absolutas
echo "🔧 Creando wrapper ejecutable..."

cat > smbsync <<EOF
#!/bin/sh
. "$VENV_PATH/bin/activate"
python "$INSTALL_DIR/main.py" "\$@"
EOF

chmod +x smbsync

# Mover a /usr/local/bin
echo "🚚 Instalando comando smbsync en /usr/local/bin (se necesita sudo)"
sudo mv smbsync "$WRAPPER_PATH"

echo "✅ Instalación completada. Ejecuta el programa con: smbsync"
