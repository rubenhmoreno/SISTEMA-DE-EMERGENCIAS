"""
Ventana Principal - Sistema de Emergencias
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from datetime import datetime
import threading

# Importar ventanas específicas
from gui.nueva_llamada_window import NuevaLlamadaWindow
from gui.consulta_llamadas_window import ConsultaLlamadasWindow
from gui.gestion_moviles_window import GestionMovilesWindow
from gui.gestion_usuarios_window import GestionUsuariosWindow
from gui.configuracion_window import ConfiguracionWindow
from gui.estadisticas_window import EstadisticasWindow

class MainWindow(ctk.CTk):
    def __init__(self, app):
        super().__init__()
        
        self.app = app
        self.setup_window()
        self.create_widgets()
        self.update_status_bar()
        
        # Timer para actualizar estado
        self.status_timer()
        
    def setup_window(self):
        """Configura la ventana principal"""
        self.title(f"Sistema de Emergencias - Villa Allende | Usuario: {self.app.current_user['nombre_completo']}")
        
        # Pantalla completa por defecto
        self.state('zoomed')  # Windows
        # self.attributes('-zoomed', True)  # Linux
        
        # Configurar protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configurar grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz principal"""
        
        # Barra lateral
        self.create_sidebar()
        
        # Área principal
        self.create_main_area()
        
        # Barra de estado
        self.create_status_bar()
        
    def create_sidebar(self):
        """Crea la barra lateral con navegación"""
        
        # Frame de navegación
        nav_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        nav_frame.grid(row=0, column=0, sticky="nsew")
        nav_frame.grid_rowconfigure(10, weight=1)  # Espaciador
        
        # Título
        title_label = ctk.CTkLabel(
            nav_frame,
            text="EMERGENCIAS",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Botones de navegación
        self.nav_buttons = {}
        
        # Nueva Llamada (más prominente)
        self.nav_buttons['nueva_llamada'] = ctk.CTkButton(
            nav_frame,
            text="🚨 NUEVA LLAMADA",
            command=self.nueva_llamada,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("red", "darkred"),
            hover_color=("darkred", "red")
        )
        self.nav_buttons['nueva_llamada'].grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Separador
        separator = ctk.CTkFrame(nav_frame, height=2)
        separator.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Consultas y gestión
        buttons_config = [
            ("📋 Consultar Llamadas", self.consultar_llamadas),
            ("🚗 Gestión de Móviles", self.gestion_moviles),
            ("👥 Gestión de Usuarios", self.gestion_usuarios),
            ("📊 Estadísticas", self.estadisticas),
            ("⚙️ Configuración", self.configuracion),
        ]
        
        for i, (text, command) in enumerate(buttons_config, start=3):
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
            
        # Información del usuario
        user_frame = ctk.CTkFrame(nav_frame)
        user_frame.grid(row=11, column=0, padx=20, pady=20, sticky="ew")
        
        user_label = ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.app.current_user['nombre_completo']}",
            font=ctk.CTkFont(size=12)
        )
        user_label.grid(row=0, column=0, padx=15, pady=(15, 5))
        
        role_label = ctk.CTkLabel(
            user_frame,
            text=f"Rol: {self.app.current_user['rol'].title()}",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        role_label.grid(row=1, column=0, padx=15, pady=(0, 15))
        
        # Botón cerrar sesión
        logout_btn = ctk.CTkButton(
            nav_frame,
            text="🚪 Cerrar Sesión",
            command=self.logout,
            height=35,
            fg_color=("gray", "gray"),
            hover_color=("darkgray", "lightgray")
        )
        logout_btn.grid(row=12, column=0, padx=20, pady=(0, 20), sticky="ew")
        
    def create_main_area(self):
        """Crea el área principal de contenido"""
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Título del dashboard
        dashboard_title = ctk.CTkLabel(
            self.main_frame,
            text="Dashboard - Sistema de Emergencias",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        dashboard_title.grid(row=0, column=0, padx=30, pady=(30, 20))
        
        # Contenedor de estadísticas rápidas
        self.create_dashboard_stats()
        
        # Lista de llamadas activas
        self.create_active_calls_list()
        
    def create_dashboard_stats(self):
        """Crea las estadísticas del dashboard"""
        
        stats_frame = ctk.CTkFrame(self.main_frame)
        stats_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Obtener estadísticas
        stats = self.get_dashboard_stats()
        
        # Llamadas activas
        self.create_stat_widget(
            stats_frame, 
            "Llamadas Activas", 
            str(stats['llamadas_activas']), 
            "🚨", 
            ("red", "darkred"),
            0
        )
        
        # Móviles disponibles
        self.create_stat_widget(
            stats_frame,
            "Móviles Disponibles",
            str(stats['moviles_disponibles']),
            "🚗",
            ("green", "darkgreen"),
            1
        )
        
        # Llamadas hoy
        self.create_stat_widget(
            stats_frame,
            "Llamadas Hoy",
            str(stats['llamadas_hoy']),
            "📞",
            ("blue", "darkblue"),
            2
        )
        
        # Personal en turno
        self.create_stat_widget(
            stats_frame,
            "Personal en Turno",
            str(stats['personal_turno']),
            "👥",
            ("orange", "darkorange"),
            3
        )
        
    def create_stat_widget(self, parent, title, value, icon, color, column):
        """Crea un widget de estadística"""
        
        stat_frame = ctk.CTkFrame(parent, fg_color=color)
        stat_frame.grid(row=0, column=column, padx=10, pady=20, sticky="ew")
        
        icon_label = ctk.CTkLabel(
            stat_frame,
            text=icon,
            font=ctk.CTkFont(size=30)
        )
        icon_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        value_label = ctk.CTkLabel(
            stat_frame,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        value_label.grid(row=1, column=0, padx=20, pady=5)
        
        title_label = ctk.CTkLabel(
            stat_frame,
            text=title,
            font=ctk.CTkFont(size=12)
        )
        title_label.grid(row=2, column=0, padx=20, pady=(5, 20))
        
    def create_active_calls_list(self):
        """Crea la lista de llamadas activas"""
        
        # Frame para la lista
        list_frame = ctk.CTkFrame(self.main_frame)
        list_frame.grid(row=2, column=0, padx=30, pady=(0, 30), sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        # Título
        list_title = ctk.CTkLabel(
            list_frame,
            text="Llamadas Activas",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        list_title.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Treeview para las llamadas
        self.create_calls_treeview(list_frame)
        
    def create_calls_treeview(self, parent):
        """Crea el treeview para mostrar llamadas"""
        
        # Frame para el treeview
        tree_frame = tk.Frame(parent)
        tree_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Treeview
        columns = ('Número', 'Tipo', 'Dirección', 'Estado', 'Hora')
        self.calls_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        # Configurar columnas
        for col in columns:
            self.calls_tree.heading(col, text=col)
            
        self.calls_tree.column('Número', width=100)
        self.calls_tree.column('Tipo', width=150)
        self.calls_tree.column('Dirección', width=300)
        self.calls_tree.column('Estado', width=100)
        self.calls_tree.column('Hora', width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.calls_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.calls_tree.xview)
        
        self.calls_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid
        self.calls_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Cargar datos
        self.refresh_calls_list()
        
    def create_status_bar(self):
        """Crea la barra de estado"""
        
        self.status_frame = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_frame.grid_columnconfigure(1, weight=1)
        
        # Estado del sistema
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Sistema listo",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.grid(row=0, column=0, padx=10, pady=5)
        
        # Hora actual
        self.time_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=10)
        )
        self.time_label.grid(row=0, column=2, padx=10, pady=5)
        
        # Estado WhatsApp
        self.whatsapp_status = ctk.CTkLabel(
            self.status_frame,
            text="WhatsApp: Verificando...",
            font=ctk.CTkFont(size=10)
        )
        self.whatsapp_status.grid(row=0, column=3, padx=10, pady=5)
        
    def get_dashboard_stats(self):
        """Obtiene estadísticas para el dashboard"""
        try:
            stats = {}
            
            # Llamadas activas
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(*) FROM llamadas 
                WHERE estado IN ('activa', 'despachada', 'en_curso')
            """)
            stats['llamadas_activas'] = result[0] if result else 0
            
            # Móviles disponibles
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(*) FROM moviles 
                WHERE estado = 'disponible' AND activo = 1
            """)
            stats['moviles_disponibles'] = result[0] if result else 0
            
            # Llamadas hoy
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(*) FROM llamadas 
                WHERE DATE(fecha_hora) = DATE('now')
            """)
            stats['llamadas_hoy'] = result[0] if result else 0
            
            # Personal en turno (simplificado)
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(DISTINCT personal_id) FROM asignaciones_personal 
                WHERE activo = 1
            """)
            stats['personal_turno'] = result[0] if result else 0
            
            return stats
            
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {
                'llamadas_activas': 0,
                'moviles_disponibles': 0,
                'llamadas_hoy': 0,
                'personal_turno': 0
            }
    
    def refresh_calls_list(self):
        """Actualiza la lista de llamadas activas"""
        try:
            # Limpiar treeview
            for item in self.calls_tree.get_children():
                self.calls_tree.delete(item)
            
            # Obtener llamadas activas
            calls = self.app.db_manager.fetch_all("""
                SELECT l.numero_llamada, te.nombre, l.direccion_completa, 
                       l.estado, l.fecha_hora
                FROM llamadas l
                JOIN tipos_emergencia te ON l.tipo_emergencia_id = te.id
                WHERE l.estado IN ('activa', 'despachada', 'en_curso')
                ORDER BY l.fecha_hora DESC
            """)
            
            # Agregar llamadas al treeview
            for call in calls:
                fecha_hora = datetime.strptime(call[4], '%Y-%m-%d %H:%M:%S')
                hora_str = fecha_hora.strftime('%H:%M:%S')
                
                self.calls_tree.insert('', 'end', values=(
                    call[0],  # número
                    call[1],  # tipo
                    call[2][:50] + "..." if len(call[2]) > 50 else call[2],  # dirección
                    call[3].title(),  # estado
                    hora_str  # hora
                ))
                
        except Exception as e:
            print(f"Error actualizando lista de llamadas: {e}")
    
    def update_status_bar(self):
        """Actualiza la barra de estado"""
        try:
            # Actualizar hora
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.time_label.configure(text=current_time)
            
            # Verificar estado WhatsApp en un hilo separado
            threading.Thread(target=self.check_whatsapp_status, daemon=True).start()
            
        except Exception as e:
            print(f"Error actualizando barra de estado: {e}")
    
    def check_whatsapp_status(self):
        """Verifica el estado de WhatsApp"""
        try:
            from utils.whatsapp_manager import WhatsAppManager
            wa_manager = WhatsAppManager()
            is_online = wa_manager.check_session_status()
            
            status_text = "WhatsApp: ✅ Online" if is_online else "WhatsApp: ❌ Offline"
            
            # Actualizar en el hilo principal
            self.after(0, lambda: self.whatsapp_status.configure(text=status_text))
            
        except Exception as e:
            self.after(0, lambda: self.whatsapp_status.configure(text="WhatsApp: ⚠️ Error"))
    
    def status_timer(self):
        """Timer para actualizar estado periódicamente"""
        self.update_status_bar()
        self.refresh_calls_list()
        # Repetir cada 30 segundos
        self.after(30000, self.status_timer)
    
    # Métodos de navegación
    def nueva_llamada(self):
        """Abre ventana de nueva llamada"""
        try:
            NuevaLlamadaWindow(self.app, self)
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo nueva llamada: {e}")
    
    def consultar_llamadas(self):
        """Abre ventana de consulta de llamadas"""
        try:
            ConsultaLlamadasWindow(self.app, self)
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo consulta: {e}")
    
    def gestion_moviles(self):
        """Abre ventana de gestión de móviles"""
        try:
            GestionMovilesWindow(self.app, self)
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo gestión de móviles: {e}")
    
    def gestion_usuarios(self):
        """Abre ventana de gestión de usuarios"""
        if self.app.current_user['rol'] in ['administrador', 'supervisor']:
            try:
                GestionUsuariosWindow(self.app, self)
            except Exception as e:
                messagebox.showerror("Error", f"Error abriendo gestión de usuarios: {e}")
        else:
            messagebox.showwarning("Acceso Denegado", "No tiene permisos para acceder a esta función")
    
    def estadisticas(self):
        """Abre ventana de estadísticas"""
        try:
            EstadisticasWindow(self.app, self)
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo estadísticas: {e}")
    
    def configuracion(self):
        """Abre ventana de configuración"""
        if self.app.current_user['rol'] in ['administrador', 'supervisor']:
            try:
                ConfiguracionWindow(self.app, self)
            except Exception as e:
                messagebox.showerror("Error", f"Error abriendo configuración: {e}")
        else:
            messagebox.showwarning("Acceso Denegado", "No tiene permisos para acceder a esta función")
    
    def logout(self):
        """Cierra sesión"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.destroy()
    
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir del sistema?"):
            self.destroy()
