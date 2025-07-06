@echo off
echo ==========================================
echo   ORGANIZANDO SISTEMA DE EMERGENCIAS
echo ==========================================
echo.

echo 📁 Organizando estructura de archivos...

REM Renombrar main_app.py a main.py
if exist main_app.py (
    ren main_app.py main.py
    echo ✅ Renombrado: main_app.py → main.py
)

REM Crear archivos __init__.py en las carpetas de módulos
echo. > database\__init__.py
echo. > gui\__init__.py  
echo. > utils\__init__.py
echo ✅ Creados archivos __init__.py

REM Mover archivo de base de datos
if exist database_manager.py (
    move database_manager.py database\db_manager.py >nul
    echo ✅ Movido: database_manager.py → database\db_manager.py
)

REM Mover archivos de GUI
echo.
echo 📋 Moviendo archivos de interfaz...
if exist login_window.py move login_window.py gui\ >nul
if exist main_window.py move main_window.py gui\ >nul
if exist nueva_llamada_window.py move nueva_llamada_window.py gui\ >nul
if exist consulta_llamadas_window.py move consulta_llamadas_window.py gui\ >nul
if exist gestion_moviles_window.py move gestion_moviles_window.py gui\ >nul
if exist gestion_usuarios_window.py move gestion_usuarios_window.py gui\ >nul
if exist configuracion_window.py move configuracion_window.py gui\ >nul
if exist estadisticas_window.py move estadisticas_window.py gui\ >nul
if exist triaje_medico_window.py move triaje_medico_window.py gui\ >nul
if exist triaje_bomberos_window.py move triaje_bomberos_window.py gui\ >nul
if exist triaje_defensa_civil_window.py move triaje_defensa_civil_window.py gui\ >nul
if exist triaje_seguridad_window.py move triaje_seguridad_window.py gui\ >nul
echo ✅ Archivos de GUI organizados

REM Mover archivos de utilidades
echo.
echo 🛠️ Moviendo archivos de utilidades...
if exist config_utils.py move config_utils.py utils\config.py >nul
if exist logger_utils.py move logger_utils.py utils\logger.py >nul
if exist whatsapp_manager.py move whatsapp_manager.py utils\ >nul
echo ✅ Archivos de utilidades organizados

REM Limpiar archivos duplicados innecesarios
echo.
echo 🧹 Limpiando archivos duplicados...
if exist installer_1.py del installer_1.py >nul
if exist installer_py.py del installer_py.py >nul
if exist init_files.py del init_files.py >nul
echo ✅ Archivos duplicados eliminados

REM Verificar estructura final
echo.
echo 🔍 Verificando estructura final...
if exist main.py echo ✅ main.py - OK
if exist database\db_manager.py echo ✅ database\db_manager.py - OK
if exist gui\login_window.py echo ✅ gui\login_window.py - OK
if exist utils\whatsapp_manager.py echo ✅ utils\whatsapp_manager.py - OK

echo.
echo 🎉 ¡Organización completada!
echo ==========================================
echo.
echo ▶️ Ejecuta ahora: 2_instalar_sistema.bat
echo.
pause