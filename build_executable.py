#!/usr/bin/env python3
"""
Script para crear ejecutable del Sistema de Emergencias
Utiliza PyInstaller para generar un archivo .exe distribuible
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

class ExecutableBuilder:
    def __init__(self):
        self.project_name = "SistemaEmergenciasVillaAllende"
        self.version = "1.0.0"
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.dist_dir = os.path.join(self.base_dir, "dist")
        self.build_dir = os.path.join(self.base_dir, "build")
        
    def check_pyinstaller(self):
        """Verifica que PyInstaller esté instalado"""
        try:
            import PyInstaller
            print(f"✅ PyInstaller {PyInstaller.__version__} encontrado")
            return True
        except ImportError:
            print("❌ PyInstaller no está instalado")
            print("   Instalando PyInstaller...")
            
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
                print("✅ PyInstaller instalado correctamente")
                return True
            except subprocess.CalledProcessError:
                print("❌ Error instalando PyInstaller")
                return False
    
    def clean_previous_builds(self):
        """Limpia builds anteriores"""
        print("🧹 Limpiando builds anteriores...")
        
        dirs_to_clean = [self.dist_dir, self.build_dir]
        files_to_clean = [f"{self.project_name}.spec"]
        
        for directory in dirs_to_clean:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                print(f"   Eliminado: {directory}")
        
        for file in files_to_clean:
            file_path = os.path.join(self.base_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"   Eliminado: {file}")
    
    def create_icon(self):
        """Crea o verifica el icono para el ejecutable"""
        icon_path = os.path.join(self.base_dir, "icon.ico")
        
        if not os.path.exists(icon_path):
            print("⚠️  Icono no encontrado. Se usará icono por defecto.")
            return None
        else:
            print(f"✅ Icono encontrado: {icon_path}")
            return icon_path
    
    def create_version_file(self):
        """Crea archivo de versión para Windows"""
        version_file_content = f"""# UTF-8
#
# Para obtener más detalles sobre fixed file info, ver:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004L,
    fileType=0x1L,
    subtype=0x0L,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Municipalidad Villa Allende'),
        StringStruct(u'FileDescription', u'Sistema de Emergencias Villa Allende'),
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'{self.project_name}'),
        StringStruct(u'LegalCopyright', u'© 2024 Municipalidad Villa Allende'),
        StringStruct(u'OriginalFilename', u'{self.project_name}.exe'),
        StringStruct(u'ProductName', u'Sistema de Emergencias'),
        StringStruct(u'ProductVersion', u'{self.version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
        
        version_file_path = os.path.join(self.base_dir, "version_info.txt")
        with open(version_file_path, "w", encoding="utf-8") as f:
            f.write(version_file_content)
        
        return version_file_path
    
    def build_executable(self):
        """Construye el ejecutable"""
        print("🔨 Construyendo ejecutable...")
        
        # Crear archivo de versión
        version_file = self.create_version_file()
        
        # Verificar icono
        icon_file = self.create_icon()
        
        # Comando base de PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name", self.project_name,
            "--onefile",  # Un solo archivo ejecutable
            "--windowed",  # Sin ventana de consola
            "--clean",
            "--noconfirm"
        ]
        
        # Agregar icono si existe
        if icon_file:
            cmd.extend(["--icon", icon_file])
        
        # Agregar información de versión en Windows
        if sys.platform == "win32" and version_file:
            cmd.extend(["--version-file", version_file])
        
        # Incluir datos necesarios
        data_includes = [
            "--add-data", "database;database",
            "--add-data", "gui;gui", 
            "--add-data", "utils;utils",
            "--add-data", "requirements.txt;.",
        ]
        cmd.extend(data_includes)
        
        # Importaciones ocultas
        hidden_imports = [
            "--hidden-import", "customtkinter",
            "--hidden-import", "tkinter",
            "--hidden-import", "sqlite3",
            "--hidden-import", "requests",
            "--hidden-import", "pandas",
            "--hidden-import", "openpyxl",
            "--hidden-import", "PIL",
            "--hidden-import", "datetime",
            "--hidden-import", "json",
            "--hidden-import", "hashlib",
            "--hidden-import", "threading",
            "--hidden-import", "webbrowser"
        ]
        cmd.extend(hidden_imports)
        
        # Archivo principal
        cmd.append("main.py")
        
        print(f"   Ejecutando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Ejecutable creado exitosamente")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creando ejecutable: {e}")
            print(f"   Stdout: {e.stdout}")
            print(f"   Stderr: {e.stderr}")
            return False
    
    def create_installer_package(self):
        """Crea paquete de instalación"""
        print("📦 Creando paquete de instalación...")
        
        # Directorio del ejecutable
        exe_path = os.path.join(self.dist_dir, f"{self.project_name}.exe")
        
        if not os.path.exists(exe_path):
            print("❌ Ejecutable no encontrado")
            return False
        
        # Crear directorio del paquete
        package_name = f"{self.project_name}_v{self.version}_{datetime.now().strftime('%Y%m%d')}"
        package_dir = os.path.join(self.dist_dir, package_name)
        os.makedirs(package_dir, exist_ok=True)
        
        # Copiar ejecutable
        shutil.copy2(exe_path, package_dir)
        
        # Copiar archivos necesarios
        files_to_include = [
            "README.md",
            "requirements.txt",
            "installer.py"
        ]
        
        for file in files_to_include:
            src = os.path.join(self.base_dir, file)
            if os.path.exists(src):
                shutil.copy2(src, package_dir)
        
        # Crear directorios necesarios
        dirs_to_create = ["data", "logs", "exports", "backups"]
        for directory in dirs_to_create:
            os.makedirs(os.path.join(package_dir, directory), exist_ok=True)
        
        # Crear archivo de instalación
        install_instructions = f"""# {self.project_name} - Instalación

## Instalación Rápida

1. Ejecutar `{self.project_name}.exe`
2. El sistema creará automáticamente la estructura necesaria
3. Login inicial:
   - Usuario: admin
   - Contraseña: admin123

## Instalación Completa (Recomendada)

1. Instalar Python 3.8+ si no está instalado
2. Ejecutar `installer.py` para configuración completa
3. Ejecutar `{self.project_name}.exe`

## Requisitos del Sistema

- Windows 10/11 (64-bit)
- 4 GB RAM mínimo
- 500 MB espacio en disco
- Conexión a Internet (para WhatsApp)

## Soporte

Email: soporte@emergenciasvallende.gov.ar
Teléfono: 3543-498000

Versión: {self.version}
Fecha: {datetime.now().strftime('%d/%m/%Y')}
"""
        
        with open(os.path.join(package_dir, "INSTALACION.txt"), "w", encoding="utf-8") as f:
            f.write(install_instructions)
        
        # Crear archivo ZIP del paquete
        zip_path = f"{package_dir}.zip"
        shutil.make_archive(package_dir, 'zip', self.dist_dir, package_name)
        
        print(f"✅ Paquete creado: {zip_path}")
        return True
    
    def cleanup_build_files(self):
        """Limpia archivos temporales de build"""
        print("🧹 Limpiando archivos temporales...")
        
        files_to_clean = [
            "version_info.txt",
            f"{self.project_name}.spec"
        ]
        
        for file in files_to_clean:
            file_path = os.path.join(self.base_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"   Eliminado: {file}")
        
        # Mantener solo el archivo ZIP final
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
            print(f"   Eliminado: {self.build_dir}")
    
    def show_build_summary(self):
        """Muestra resumen del build"""
        print("\n" + "=" * 60)
        print("   🎉 BUILD COMPLETADO")
        print("=" * 60)
        
        exe_path = os.path.join(self.dist_dir, f"{self.project_name}.exe")
        
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"\n📁 Ejecutable: {exe_path}")
            print(f"📏 Tamaño: {file_size:.1f} MB")
        
        # Buscar archivo ZIP
        zip_files = [f for f in os.listdir(self.dist_dir) if f.endswith('.zip')]
        if zip_files:
            zip_path = os.path.join(self.dist_dir, zip_files[0])
            zip_size = os.path.getsize(zip_path) / (1024 * 1024)  # MB
            print(f"📦 Paquete: {zip_path}")
            print(f"📏 Tamaño: {zip_size:.1f} MB")
        
        print(f"\n✅ El ejecutable está listo para distribución!")
        print("=" * 60)
    
    def build(self):
        """Proceso completo de build"""
        print(f"🚀 Iniciando build de {self.project_name} v{self.version}")
        print("=" * 60)
        
        # Verificaciones
        if not self.check_pyinstaller():
            return False
        
        # Proceso de build
        steps = [
            ("Limpiar builds anteriores", self.clean_previous_builds),
            ("Construir ejecutable", self.build_executable),
            ("Crear paquete de instalación", self.create_installer_package),
            ("Limpiar archivos temporales", self.cleanup_build_files)
        ]
        
        for step_name, step_function in steps:
            print(f"\n{step_name}...")
            if not step_function():
                print(f"❌ FALLO en: {step_name}")
                return False
        
        self.show_build_summary()
        return True

def main():
    """Función principal"""
    try:
        builder = ExecutableBuilder()
        
        print("Este script creará un ejecutable distribuible del Sistema de Emergencias")
        print("¿Desea continuar? (s/n): ", end="")
        
        response = input().strip().lower()
        if response not in ['s', 'si', 'y', 'yes']:
            print("Build cancelado.")
            return
        
        success = builder.build()
        
        if success:
            print("\n🎉 ¡Build completado exitosamente!")
        else:
            print("\n❌ El build falló. Revise los errores mostrados.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Build interrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
