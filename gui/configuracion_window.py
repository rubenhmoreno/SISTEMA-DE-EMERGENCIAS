"""
Ventana de Configuración - Sistema de Emergencias
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
import tkinter as tk
from datetime import datetime
import threading

from utils.whatsapp_manager import WhatsAppManager

class ConfiguracionWindow(ctk.CTkToplevel):
    def __init__(self, app, parent):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        
        self.setup_window()
        self.create_widgets()
        self.load_current_config()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Configuración del Sistema")
        self.geometry("900x700")
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz"""
        
        # Panel izquierdo - Navegación
        self.create_navigation_panel()
        
        # Panel derecho - Contenido
        self.create_content_panel()
        
    def create_navigation_panel(self):
        """Crea el panel de navegación izquierdo"""
        
        nav_frame = ctk.CTkFrame(self, width=200)
        nav_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        nav_frame.grid_propagate(False)
        nav_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            nav_frame,
            text="⚙️ CONFIGURACIÓN",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Botones de navegación
        self.nav_buttons = {}
        
        nav_items = [
            ("🏢 Sistema", "sistema"),
            ("💬 WhatsApp", "whatsapp"),
            ("🗺️ Mapas", "mapas"),
            ("🔒 Seguridad", "seguridad"),
            ("🎨 Interfaz", "interfaz"),
            ("📊 Reportes", "reportes"),
            ("📝 Logs", "logs"),
            ("💾 Backup", "backup")
        ]
        
        for i, (text, key) in enumerate(nav_items):
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=lambda k=key: self.show_section(k),
                height=40,
                anchor="w"
            )
            btn.grid(row=i+1, column=0, padx=15, pady=5, sticky="ew")
            self.nav_buttons[key] = btn
        
        # Botones de acción
        action_frame = ctk.CTkFrame(nav_frame)
        action_frame.grid(row=len(nav_items)+2, column=0, padx=15, pady=(30, 20), sticky="ew")
        
        save_btn = ctk.CTkButton(
            action_frame,
            text="💾 Guardar Todo",
            command=self.save_all_config,
            fg_color=("green", "darkgreen")
        )
        save_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        cancel_btn = ctk.CTkButton(
            action_frame,
            text="❌ Cancelar",
            command=self.destroy,
            fg_color=("gray", "darkgray")
        )
        cancel_btn.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        action_frame.grid_columnconfigure(0, weight=1)
        
    def create_content_panel(self):
        """Crea el panel de contenido principal"""
        
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Crear frames para cada sección
        self.section_frames = {}
        self.create_all_sections()
        
        # Mostrar primera sección por defecto
        self.show_section("sistema")
        
    def create_all_sections(self):
        """Crea todas las secciones de configuración"""
        
        # Crear scroll frame principal
        self.main_scroll = ctk.CTkScrollableFrame(self.content_frame)
        self.main_scroll.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_scroll.grid_columnconfigure(0, weight=1)
        
        # Crear cada sección
        self.create_sistema_section()
        self.create_whatsapp_section()
        self.create_mapas_section()
        self.create_seguridad_section()
        self.create_interfaz_section()
        self.create_reportes_section()
        self.create_logs_section()
        self.create_backup_section()
        
    def create_sistema_section(self):
        """Crea la sección de configuración del sistema"""
        
        frame = ctk.CTkFrame(self.main_scroll)
        frame.grid_columnconfigure(1, weight=1)
        self.section_frames["sistema"] = frame
        
        # Título
        title = ctk.CTkLabel(frame, text="🏢 CONFIGURACIÓN DEL SISTEMA", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 25))
        
        # Nombre del sistema
        ctk.CTkLabel(frame, text="Nombre del Sistema:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.sistema_nombre_entry = ctk.CTkEntry(frame, width=300)
        self.sistema_nombre_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Organización
        ctk.CTkLabel(frame, text="Organización:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.sistema_organizacion_entry = ctk.CTkEntry(frame, width=300)
        self.sistema_organizacion_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Dirección
        ctk.CTkLabel(frame, text="Dirección:", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w")
        self.sistema_direccion_entry = ctk.CTkEntry(frame, width=300)
        self.sistema_direccion_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Teléfono central
        ctk.CTkLabel(frame, text="Teléfono Central:", font=ctk.CTkFont(weight="bold")).grid(
            row=4, column=0, padx=(20, 10), pady=10, sticky="w")
        self.sistema_telefono_entry = ctk.CTkEntry(frame, width=300)
        self.sistema_telefono_entry.grid(row=4, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Prefijo número de llamada
        ctk.CTkLabel(frame, text="Prefijo Llamadas:", font=ctk.CTkFont(weight="bold")).grid(
            row=5, column=0, padx=(20, 10), pady=10, sticky="w")
        self.sistema_prefijo_entry = ctk.CTkEntry(frame, width=100)
        self.sistema_prefijo_entry.grid(row=5, column=1, padx=(0, 20), pady=10, sticky="w")
        
    def create_whatsapp_section(self):
        """Crea la sección de configuración de WhatsApp"""
        
        frame = ctk.CTkFrame(self.main_scroll)
        frame.grid_columnconfigure(1, weight=1)
        self.section_frames["whatsapp"] = frame
        
        # Título
        title = ctk.CTkLabel(frame, text="💬 CONFIGURACIÓN DE WHATSAPP", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 25))
        
        # URL de la API
        ctk.CTkLabel(frame, text="URL de la API:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.whatsapp_url_entry = ctk.CTkEntry(frame, width=400)
        self.whatsapp_url_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Token
        ctk.CTkLabel(frame, text="Token:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.whatsapp_token_entry = ctk.CTkEntry(frame, width=400, show="*")
        self.whatsapp_token_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Timeout
        ctk.CTkLabel(frame, text="Timeout (segundos):", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w")
        self.whatsapp_timeout_entry = ctk.CTkEntry(frame, width=100)
        self.whatsapp_timeout_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Números de destino
        ctk.CTkLabel(frame, text="Números de Destino:", font=ctk.CTkFont(weight="bold")).grid(
            row=4, column=0, padx=(20, 10), pady=(20, 10), sticky="nw")
        
        # Frame para números
        numeros_frame = ctk.CTkFrame(frame)
        numeros_frame.grid(row=4, column=1, padx=(0, 20), pady=(20, 10), sticky="ew")
        numeros_frame.grid_columnconfigure(1, weight=1)
        
        # Emergencias médicas DEMVA
        ctk.CTkLabel(numeros_frame, text="DEMVA:").grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")
        self.whatsapp_demva_entry = ctk.CTkEntry(numeros_frame)
        self.whatsapp_demva_entry.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="ew")
        
        # Emergencias médicas CEC
        ctk.CTkLabel(numeros_frame, text="CEC:").grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        self.whatsapp_cec_entry = ctk.CTkEntry(numeros_frame)
        self.whatsapp_cec_entry.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="ew")
        
        # Bomberos
        ctk.CTkLabel(numeros_frame, text="Bomberos:").grid(row=2, column=0, padx=(10, 5), pady=5, sticky="w")
        self.whatsapp_bomberos_entry = ctk.CTkEntry(numeros_frame)
        self.whatsapp_bomberos_entry.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")
        
        # Defensa Civil
        ctk.CTkLabel(numeros_frame, text="Defensa Civil:").grid(row=3, column=0, padx=(10, 5), pady=5, sticky="w")
        self.whatsapp_defensa_entry = ctk.CTkEntry(numeros_frame)
        self.whatsapp_defensa_entry.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="ew")
        
        # Seguridad
        ctk.CTkLabel(numeros_frame, text="Seguridad:").grid(row=4, column=0, padx=(10, 5), pady=(5, 15), sticky="w")
        self.whatsapp_seguridad_entry = ctk.CTkEntry(numeros_frame)
        self.whatsapp_seguridad_entry.grid(row=4, column=1, padx=(0, 10), pady=(5, 15), sticky="ew")
        
        # Botones de prueba
        test_frame = ctk.CTkFrame(frame)
        test_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        test_frame.grid_columnconfigure((0, 1), weight=1)
        
        test_connection_btn = ctk.CTkButton(
            test_frame,
            text="🔍 Probar Conexión",
            command=self.test_whatsapp_connection,
            fg_color=("blue", "darkblue")
        )
        test_connection_btn.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        
        send_test_btn = ctk.CTkButton(
            test_frame,
            text="📱 Enviar Mensaje de Prueba",
            command=self.send_test_message,
            fg_color=("green", "darkgreen")
        )
        send_test_btn.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        
    def create_mapas_section(self):
        """Crea la sección de configuración de mapas"""
        
        frame = ctk.CTkFrame(self.main_scroll)
        frame.grid_columnconfigure(1, weight=1)
        self.section_frames["mapas"] = frame
        
        # Título
        title = ctk.CTkLabel(frame, text="🗺️ CONFIGURACIÓN DE MAPAS", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 25))
        
        # Proveedor
        ctk.CTkLabel(frame, text="Proveedor:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.mapas_proveedor_combo = ctk.CTkComboBox(frame, values=["google", "openstreetmap"])
        self.mapas_proveedor_combo.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Zoom por defecto
        ctk.CTkLabel(frame, text="Zoom por Defecto:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.mapas_zoom_entry = ctk.CTkEntry(frame, width=100)
        self.mapas_zoom_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Centro - Latitud
        ctk.CTkLabel(frame, text="Centro - Latitud:", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w")
        self.mapas_lat_entry = ctk.CTkEntry(frame, width=150)
        self.mapas_lat_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Centro - Longitud
        ctk.CTkLabel(frame, text="Centro - Longitud:", font=ctk.CTkFont(weight="bold")).grid(
            row=4, column=0, padx=(20, 10), pady=10, sticky="w")
        self.mapas_lng_entry = ctk.CTkEntry(frame, width=150)
        self.mapas_lng_entry.grid(row=4, column=1, padx=(0, 20), pady=10, sticky="w")
        
    def create_seguridad_section(self):
        """Crea la sección de configuración de seguridad"""
        
        frame = ctk.CTkFrame(self.main_scroll)
        frame.grid_columnconfigure(1, weight=1)
        self.section_frames["seguridad"] = frame
        
        # Título
        title = ctk.CTkLabel(frame, text="🔒 CONFIGURACIÓN DE SEGURIDAD", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 25))
        
        # Timeout de sesión
        ctk.CTkLabel(frame, text="Timeout Sesión (minutos):", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.seguridad_timeout_entry = ctk.CTkEntry(frame, width=100)
        self.seguridad_timeout_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Máximo intentos de login
        ctk.CTkLabel(frame, text="Máx. Intentos Login:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.seguridad_intentos_entry = ctk.CTkEntry(frame, width=100)
        self.seguridad_intentos_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Tiempo de bloqueo
        ctk.CTkLabel(frame, text="Tiempo Bloqueo (minutos):", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w")
        self.seguridad_bloqueo_entry = ctk.CTkEntry(frame, width=100)
        self.seguridad_bloqueo_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Log de acciones
        self.seguridad_log_switch = ctk.CTkSwitch(frame, text="Registrar todas las acciones en log")
        self.seguridad_log_switch.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        
    def create_interfaz_section(self):
        """Crea la sección de configuración de interfaz"""
        
        frame = ctk.CTkFrame(self.main_scroll)
        frame.grid_columnconfigure(1, weight=1)
        self.section_frames["interfaz"] = frame
        
        # Título
        title = ctk.CTkLabel(frame, text="🎨 CONFIGURACIÓN DE INTERFAZ", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 25))
        
        # Tema
        ctk.CTkLabel(frame, text="Tema:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.interfaz_tema_combo = ctk.CTkComboBox(frame, values=["system", "dark", "light"])
        self.interfaz_tema_combo.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Color del tema
        ctk.CTkLabel(frame, text="Color del Tema:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.interfaz_color_combo = ctk.CTkComboBox(frame, values=["blue", "green", "dark-blue"])
        self.interfaz_color_combo.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Formato de fecha
        ctk.CTkLabel(frame, text="Formato de Fecha:", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w")
        self.interfaz_fecha_combo = ctk.CTkComboBox(frame, values=["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        self.interfaz_fecha_combo.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Formato de hora
        ctk.CTkLabel(frame, text="Formato de Hora:", font=ctk.CTkFont(weight="bold")).grid(
            row=4, column=0, padx=(20, 10), pady=10, sticky="w")
        self.interfaz_hora_combo = ctk.CTkComboBox(frame, values=["HH:MM:SS", "HH:MM", "hh:MM:SS AM/PM"])
        self.interfaz_hora_combo.grid(row=4, column=1, padx=(0, 20), pady=10, sticky="w")
        
    def create_reportes_section(self):
        """Crea la sección de configuración de reportes"""
        
        frame = ctk.CTkFrame(self.main_scroll)
        frame.grid_columnconfigure(1, weight=1)
        self.section_frames["reportes"] = frame
        
        # Título
        title = ctk.CTkLabel(frame, text="📊 CONFIGURACIÓN DE REPORTES", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 25))
        
        # Directorio de exportación
        ctk.CTkLabel(frame, text="Directorio de Exportación:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        
        dir_frame = ctk.CTkFrame(frame)
        dir_frame.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        dir_frame.grid_columnconfigure(0, weight=1)
        
        self.reportes_directorio_entry = ctk.CTkEntry(dir_frame)
        self.reportes_directorio_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        
        browse_btn = ctk.CTkButton(dir_frame, text="📁", width=40, command=self.browse_export_directory)
        browse_btn.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Formato por defecto
        ctk.CTkLabel(frame, text="Formato por Defecto:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.reportes_formato_combo = ctk.CTkComboBox(frame, values=["xlsx", "csv", "pdf"])
        self.reportes_formato_combo.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Incluir logo
        self.reportes_logo_switch = ctk.CTkSwitch(frame, text="Incluir logo en reportes")
        self.reportes_logo_switch.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # Mostrar pie de página
        self.reportes_pie_switch = ctk.CTkSwitch(frame, text="Mostrar pie de página")
        self.reportes_pie_switch.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
    def create_logs_section(self):
        """Crea la sección de configuración de logs"""
        
        frame = ctk.CTkFrame(self.main_scroll)
        frame.grid_columnconfigure(1, weight=1)
        self.section_frames["logs"] = frame
        
        # Título
        title = ctk.CTkLabel(frame, text="📝 CONFIGURACIÓN DE LOGS", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 25))
        
        # Nivel de log
        ctk.CTkLabel(frame, text="Nivel de Log:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.logs_nivel_combo = ctk.CTkComboBox(frame, values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.logs_nivel_combo.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Días de retención
        ctk.CTkLabel(frame, text="Días de Retención:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.logs_retencion_entry = ctk.CTkEntry(frame, width=100)
        self.logs_retencion_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Tamaño máximo por archivo
        ctk.CTkLabel(frame, text="Tamaño Máx. Archivo (MB):", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w")
        self.logs_tamaño_entry = ctk.CTkEntry(frame, width=100)
        self.logs_tamaño_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="w")
        
    def create_backup_section(self):
        """Crea la sección de configuración de backup"""
        
        frame = ctk.CTkFrame(self.main_scroll)
        frame.grid_columnconfigure(1, weight=1)
        self.section_frames["backup"] = frame
        
        # Título
        title = ctk.CTkLabel(frame, text="💾 CONFIGURACIÓN DE BACKUP", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 25))
        
        # Backup automático
        self.backup_automatico_switch = ctk.CTkSwitch(frame, text="Backup Automático")
        self.backup_automatico_switch.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # Intervalo de backup
        ctk.CTkLabel(frame, text="Intervalo (horas):", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.backup_intervalo_entry = ctk.CTkEntry(frame, width=100)
        self.backup_intervalo_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Directorio de backup
        ctk.CTkLabel(frame, text="Directorio de Backup:", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w")
        
        backup_dir_frame = ctk.CTkFrame(frame)
        backup_dir_frame.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")
        backup_dir_frame.grid_columnconfigure(0, weight=1)
        
        self.backup_directorio_entry = ctk.CTkEntry(backup_dir_frame)
        self.backup_directorio_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        
        backup_browse_btn = ctk.CTkButton(backup_dir_frame, text="📁", width=40, command=self.browse_backup_directory)
        backup_browse_btn.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Botones de acción
        action_frame = ctk.CTkFrame(frame)
        action_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        action_frame.grid_columnconfigure((0, 1), weight=1)
        
        backup_now_btn = ctk.CTkButton(
            action_frame,
            text="💾 Backup Ahora",
            command=self.create_backup_now,
            fg_color=("green", "darkgreen")
        )
        backup_now_btn.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        
        restore_btn = ctk.CTkButton(
            action_frame,
            text="📂 Restaurar Backup",
            command=self.restore_backup,
            fg_color=("orange", "darkorange")
        )
        restore_btn.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        
    def show_section(self, section_key):
        """Muestra una sección específica"""
        # Ocultar todas las secciones
        for key, frame in self.section_frames.items():
            frame.grid_remove()
        
        # Mostrar la sección seleccionada
        if section_key in self.section_frames:
            self.section_frames[section_key].grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        
        # Actualizar estado de botones
        for key, btn in self.nav_buttons.items():
            if key == section_key:
                btn.configure(fg_color=("gray", "darkgray"))
            else:
                btn.configure(fg_color=("blue", "darkblue"))
    
    def load_current_config(self):
        """Carga la configuración actual en los campos"""
        config = self.app.config.get_all_config()
        
        try:
            # Sistema
            self.sistema_nombre_entry.insert(0, config.get('sistema', {}).get('nombre', ''))
            self.sistema_organizacion_entry.insert(0, config.get('sistema', {}).get('organizacion', ''))
            self.sistema_direccion_entry.insert(0, config.get('sistema', {}).get('direccion', ''))
            self.sistema_telefono_entry.insert(0, config.get('sistema', {}).get('telefono_central', ''))
            self.sistema_prefijo_entry.insert(0, config.get('emergencias', {}).get('numero_llamada_prefijo', ''))
            
            # WhatsApp
            whatsapp_config = config.get('whatsapp', {})
            self.whatsapp_url_entry.insert(0, whatsapp_config.get('api_url', ''))
            self.whatsapp_token_entry.insert(0, whatsapp_config.get('token', ''))
            self.whatsapp_timeout_entry.insert(0, str(whatsapp_config.get('timeout_segundos', 15)))
            
            # Cargar números de WhatsApp desde la base de datos
            self.load_whatsapp_numbers()
            
            # Mapas
            mapas_config = config.get('mapas', {})
            self.mapas_proveedor_combo.set(mapas_config.get('proveedor', 'google'))
            self.mapas_zoom_entry.insert(0, str(mapas_config.get('zoom_defecto', 15)))
            self.mapas_lat_entry.insert(0, str(mapas_config.get('centro_lat', -31.3298)))
            self.mapas_lng_entry.insert(0, str(mapas_config.get('centro_lng', -64.2959)))
            
            # Seguridad
            seguridad_config = config.get('seguridad', {})
            self.seguridad_timeout_entry.insert(0, str(seguridad_config.get('timeout_sesion_minutos', 480)))
            self.seguridad_intentos_entry.insert(0, str(seguridad_config.get('intentos_login_max', 5)))
            self.seguridad_bloqueo_entry.insert(0, str(seguridad_config.get('bloqueo_tiempo_minutos', 30)))
            if seguridad_config.get('log_acciones', True):
                self.seguridad_log_switch.select()
            
            # Interfaz
            interfaz_config = config.get('interfaz', {})
            self.interfaz_tema_combo.set(interfaz_config.get('tema', 'system'))
            self.interfaz_color_combo.set(interfaz_config.get('color_tema', 'blue'))
            self.interfaz_fecha_combo.set(interfaz_config.get('formato_fecha', 'DD/MM/YYYY'))
            self.interfaz_hora_combo.set(interfaz_config.get('formato_hora', 'HH:MM:SS'))
            
            # Reportes
            reportes_config = config.get('reportes', {})
            self.reportes_directorio_entry.insert(0, reportes_config.get('directorio', 'exports/'))
            self.reportes_formato_combo.set(reportes_config.get('formato_defecto', 'xlsx'))
            if reportes_config.get('incluir_logo', True):
                self.reportes_logo_switch.select()
            if reportes_config.get('mostrar_pie_pagina', True):
                self.reportes_pie_switch.select()
            
            # Logs
            logs_config = config.get('logs', {})
            self.logs_nivel_combo.set(logs_config.get('nivel', 'INFO'))
            self.logs_retencion_entry.insert(0, str(logs_config.get('rotacion_dias', 30)))
            self.logs_tamaño_entry.insert(0, str(logs_config.get('archivo_max_mb', 10)))
            
            # Backup
            backup_config = config.get('base_datos', {})
            if backup_config.get('backup_automatico', True):
                self.backup_automatico_switch.select()
            self.backup_intervalo_entry.insert(0, str(backup_config.get('backup_intervalo_horas', 24)))
            self.backup_directorio_entry.insert(0, backup_config.get('backup_directorio', 'backups/'))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando configuración: {e}")
    
    def load_whatsapp_numbers(self):
        """Carga los números de WhatsApp desde la base de datos"""
        try:
            numeros = self.app.db_manager.fetch_all("""
                SELECT tipo, numero FROM config_whatsapp WHERE activo = 1
            """)
            
            for tipo, numero in numeros:
                if tipo == "MEDICA_DEMVA":
                    self.whatsapp_demva_entry.insert(0, numero)
                elif tipo == "MEDICA_CEC":
                    self.whatsapp_cec_entry.insert(0, numero)
                elif tipo == "BOMBEROS":
                    self.whatsapp_bomberos_entry.insert(0, numero)
                elif tipo == "DEFENSA_CIVIL":
                    self.whatsapp_defensa_entry.insert(0, numero)
                elif tipo == "SEGURIDAD":
                    self.whatsapp_seguridad_entry.insert(0, numero)
                    
        except Exception as e:
            print(f"Error cargando números WhatsApp: {e}")
    
    def save_all_config(self):
        """Guarda toda la configuración"""
        try:
            # Guardar configuración del sistema
            self.app.config.set('sistema.nombre', self.sistema_nombre_entry.get())
            self.app.config.set('sistema.organizacion', self.sistema_organizacion_entry.get())
            self.app.config.set('sistema.direccion', self.sistema_direccion_entry.get())
            self.app.config.set('sistema.telefono_central', self.sistema_telefono_entry.get())
            self.app.config.set('emergencias.numero_llamada_prefijo', self.sistema_prefijo_entry.get())
            
            # Guardar configuración de WhatsApp
            self.app.config.set('whatsapp.api_url', self.whatsapp_url_entry.get())
            self.app.config.set('whatsapp.token', self.whatsapp_token_entry.get())
            self.app.config.set('whatsapp.timeout_segundos', int(self.whatsapp_timeout_entry.get() or 15))
            
            # Guardar números de WhatsApp en la base de datos
            self.save_whatsapp_numbers()
            
            # Guardar configuración de mapas
            self.app.config.set('mapas.proveedor', self.mapas_proveedor_combo.get())
            self.app.config.set('mapas.zoom_defecto', int(self.mapas_zoom_entry.get() or 15))
            self.app.config.set('mapas.centro_lat', float(self.mapas_lat_entry.get() or -31.3298))
            self.app.config.set('mapas.centro_lng', float(self.mapas_lng_entry.get() or -64.2959))
            
            # Guardar configuración de seguridad
            self.app.config.set('seguridad.timeout_sesion_minutos', int(self.seguridad_timeout_entry.get() or 480))
            self.app.config.set('seguridad.intentos_login_max', int(self.seguridad_intentos_entry.get() or 5))
            self.app.config.set('seguridad.bloqueo_tiempo_minutos', int(self.seguridad_bloqueo_entry.get() or 30))
            self.app.config.set('seguridad.log_acciones', bool(self.seguridad_log_switch.get()))
            
            # Guardar configuración de interfaz
            self.app.config.set('interfaz.tema', self.interfaz_tema_combo.get())
            self.app.config.set('interfaz.color_tema', self.interfaz_color_combo.get())
            self.app.config.set('interfaz.formato_fecha', self.interfaz_fecha_combo.get())
            self.app.config.set('interfaz.formato_hora', self.interfaz_hora_combo.get())
            
            # Guardar configuración de reportes
            self.app.config.set('reportes.directorio', self.reportes_directorio_entry.get())
            self.app.config.set('reportes.formato_defecto', self.reportes_formato_combo.get())
            self.app.config.set('reportes.incluir_logo', bool(self.reportes_logo_switch.get()))
            self.app.config.set('reportes.mostrar_pie_pagina', bool(self.reportes_pie_switch.get()))
            
            # Guardar configuración de logs
            self.app.config.set('logs.nivel', self.logs_nivel_combo.get())
            self.app.config.set('logs.rotacion_dias', int(self.logs_retencion_entry.get() or 30))
            self.app.config.set('logs.archivo_max_mb', int(self.logs_tamaño_entry.get() or 10))
            
            # Guardar configuración de backup
            self.app.config.set('base_datos.backup_automatico', bool(self.backup_automatico_switch.get()))
            self.app.config.set('base_datos.backup_intervalo_horas', int(self.backup_intervalo_entry.get() or 24))
            self.app.config.set('base_datos.backup_directorio', self.backup_directorio_entry.get())
            
            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
            
            # Actualizar ventana principal si es necesario
            if hasattr(self.parent, 'refresh_calls_list'):
                self.parent.refresh_calls_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando configuración: {e}")
    
    def save_whatsapp_numbers(self):
        """Guarda los números de WhatsApp en la base de datos"""
        try:
            # Actualizar números existentes
            numbers_config = [
                ("MEDICA_DEMVA", self.whatsapp_demva_entry.get()),
                ("MEDICA_CEC", self.whatsapp_cec_entry.get()),
                ("BOMBEROS", self.whatsapp_bomberos_entry.get()),
                ("DEFENSA_CIVIL", self.whatsapp_defensa_entry.get()),
                ("SEGURIDAD", self.whatsapp_seguridad_entry.get())
            ]
            
            for tipo, numero in numbers_config:
                if numero.strip():
                    # Verificar si existe
                    existe = self.app.db_manager.fetch_one("""
                        SELECT id FROM config_whatsapp WHERE tipo = ?
                    """, (tipo,))
                    
                    if existe:
                        # Actualizar
                        self.app.db_manager.execute_query("""
                            UPDATE config_whatsapp SET numero = ?, fecha_actualizacion = ?
                            WHERE tipo = ?
                        """, (numero.strip(), datetime.now(), tipo))
                    else:
                        # Insertar
                        self.app.db_manager.execute_query("""
                            INSERT INTO config_whatsapp (tipo, numero, activo, fecha_actualizacion)
                            VALUES (?, ?, 1, ?)
                        """, (tipo, numero.strip(), datetime.now()))
                        
        except Exception as e:
            print(f"Error guardando números WhatsApp: {e}")
            raise
    
    def test_whatsapp_connection(self):
        """Prueba la conexión de WhatsApp"""
        def test_connection():
            try:
                wa_manager = WhatsAppManager()
                result = wa_manager.test_connection()
                
                # Actualizar UI en el hilo principal
                self.after(0, lambda: self.show_whatsapp_test_result(result))
                
            except Exception as e:
                error_result = {
                    'success': False,
                    'message': f'Error: {str(e)}',
                    'status': 'error'
                }
                self.after(0, lambda: self.show_whatsapp_test_result(error_result))
        
        # Ejecutar en hilo separado
        threading.Thread(target=test_connection, daemon=True).start()
        
        # Mostrar mensaje de espera
        messagebox.showinfo("Probando", "Probando conexión de WhatsApp...")
    
    def show_whatsapp_test_result(self, result):
        """Muestra el resultado de la prueba de WhatsApp"""
        if result['success']:
            messagebox.showinfo("Conexión Exitosa", result['message'])
        else:
            messagebox.showerror("Error de Conexión", result['message'])
    
    def send_test_message(self):
        """Envía un mensaje de prueba por WhatsApp"""
        # Pedir número de destino
        TestMessageDialog(self.app, self)
    
    def browse_export_directory(self):
        """Busca directorio de exportación"""
        directory = filedialog.askdirectory(title="Seleccionar directorio de exportación")
        if directory:
            self.reportes_directorio_entry.delete(0, 'end')
            self.reportes_directorio_entry.insert(0, directory + "/")
    
    def browse_backup_directory(self):
        """Busca directorio de backup"""
        directory = filedialog.askdirectory(title="Seleccionar directorio de backup")
        if directory:
            self.backup_directorio_entry.delete(0, 'end')
            self.backup_directorio_entry.insert(0, directory + "/")
    
    def create_backup_now(self):
        """Crea un backup inmediato"""
        try:
            backup_file = self.app.db_manager.backup_database()
            if backup_file:
                messagebox.showinfo("Backup Creado", f"Backup creado exitosamente:\n{backup_file}")
            else:
                messagebox.showerror("Error", "Error creando backup")
        except Exception as e:
            messagebox.showerror("Error", f"Error creando backup: {e}")
    
    def restore_backup(self):
        """Restaura desde un backup"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de backup",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        
        if file_path:
            if messagebox.askyesno("Confirmar Restauración", 
                                 "¿Está seguro que desea restaurar este backup?\n"
                                 "Se perderán todos los datos actuales."):
                try:
                    # Aquí implementarías la lógica de restauración
                    messagebox.showinfo("Restauración", "Función de restauración no implementada aún")
                except Exception as e:
                    messagebox.showerror("Error", f"Error restaurando backup: {e}")


class TestMessageDialog(ctk.CTkToplevel):
    """Diálogo para enviar mensaje de prueba"""
    
    def __init__(self, app, parent):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Enviar Mensaje de Prueba")
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Centrar ventana
        self.center_window()
        
    def center_window(self):
        """Centra la ventana"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (200 // 2)
        self.geometry(f"400x200+{x}+{y}")
        
    def create_widgets(self):
        """Crea la interfaz"""
        
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="📱 Mensaje de Prueba",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 25))
        
        # Número de teléfono
        ctk.CTkLabel(self, text="Número de teléfono:").grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.phone_entry = ctk.CTkEntry(self, placeholder_text="3516789012")
        self.phone_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Botones
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        send_btn = ctk.CTkButton(
            buttons_frame,
            text="📤 Enviar",
            command=self.send_message,
            fg_color=("green", "darkgreen")
        )
        send_btn.grid(row=0, column=0, padx=(15, 5), pady=15, sticky="ew")
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=self.destroy,
            fg_color=("gray", "darkgray")
        )
        cancel_btn.grid(row=0, column=1, padx=(5, 15), pady=15, sticky="ew")
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        
        # Focus inicial
        self.phone_entry.focus()
        
    def send_message(self):
        """Envía el mensaje de prueba"""
        phone = self.phone_entry.get().strip()
        
        if not phone:
            messagebox.showerror("Error", "Debe ingresar un número de teléfono")
            return
        
        def send_test():
            try:
                wa_manager = WhatsAppManager()
                result = wa_manager.enviar_mensaje_prueba(phone)
                
                # Actualizar UI en el hilo principal
                self.after(0, lambda: self.show_send_result(result))
                
            except Exception as e:
                error_result = {
                    'success': False,
                    'error': str(e)
                }
                self.after(0, lambda: self.show_send_result(error_result))
        
        # Ejecutar en hilo separado
        threading.Thread(target=send_test, daemon=True).start()
        
        # Deshabilitar botón mientras se envía
        send_btn = self.nametowidget(f"{self.winfo_children()[-1].winfo_children()[0]}")
        send_btn.configure(state="disabled", text="Enviando...")
    
    def show_send_result(self, result):
        """Muestra el resultado del envío"""
        if result['success']:
            messagebox.showinfo("Mensaje Enviado", "Mensaje de prueba enviado correctamente")
            self.destroy()
        else:
            messagebox.showerror("Error", f"Error enviando mensaje: {result.get('error', 'Unknown')}")
            
            # Rehabilitar botón
            send_btn = self.nametowidget(f"{self.winfo_children()[-1].winfo_children()[0]}")
            send_btn.configure(state="normal", text="📤 Enviar")
