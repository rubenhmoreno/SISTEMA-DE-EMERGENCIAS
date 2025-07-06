"""
Ventana de Estadísticas - Sistema de Emergencias
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from datetime import datetime, timedelta
import threading

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class EstadisticasWindow(ctk.CTkToplevel):
    def __init__(self, app, parent):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        
        self.setup_window()
        self.create_widgets()
        self.load_statistics()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Estadísticas del Sistema")
        self.geometry("1000x700")
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz"""
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Crear pestañas
        self.create_general_tab()
        self.create_emergency_types_tab()
        self.create_response_times_tab()
        self.create_users_tab()
        self.create_reports_tab()
        
        # Botón cerrar
        close_btn = ctk.CTkButton(
            self,
            text="❌ Cerrar",
            command=self.destroy,
            fg_color=("gray", "darkgray")
        )
        close_btn.grid(row=1, column=0, pady=(10, 20))
        
    def create_general_tab(self):
        """Crea la pestaña de estadísticas generales"""
        
        general_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(general_frame, text="📊 General")
        
        # Configurar grid
        general_frame.grid_columnconfigure(0, weight=1)
        general_frame.grid_rowconfigure(1, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            general_frame,
            text="📊 ESTADÍSTICAS GENERALES",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 30))
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(general_frame)
        scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        scroll_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Crear tarjetas de estadísticas
        self.create_stat_cards(scroll_frame)
        
        # Gráfico de llamadas por día (si matplotlib está disponible)
        if MATPLOTLIB_AVAILABLE:
            self.create_calls_chart(scroll_frame)
        else:
            no_chart_label = ctk.CTkLabel(
                scroll_frame,
                text="📈 Gráficos no disponibles\n(Instalar matplotlib para ver gráficos)",
                font=ctk.CTkFont()
            )
            no_chart_label.grid(row=2, column=0, columnspan=4, pady=20)
        
    def create_stat_cards(self, parent):
        """Crea las tarjetas de estadísticas"""
        
        # Obtener estadísticas
        stats = self.get_general_statistics()
        
        # Tarjeta 1: Total de llamadas
        self.create_stat_card(
            parent, 0, 0,
            "📞 TOTAL LLAMADAS",
            str(stats['total_calls']),
            "Desde el inicio",
            ("blue", "darkblue")
        )
        
        # Tarjeta 2: Llamadas hoy
        self.create_stat_card(
            parent, 0, 1,
            "📅 LLAMADAS HOY",
            str(stats['calls_today']),
            "En las últimas 24h",
            ("green", "darkgreen")
        )
        
        # Tarjeta 3: Promedio diario
        self.create_stat_card(
            parent, 0, 2,
            "📈 PROMEDIO DIARIO",
            f"{stats['daily_average']:.1f}",
            "Último mes",
            ("orange", "darkorange")
        )
        
        # Tarjeta 4: Tiempo respuesta promedio
        self.create_stat_card(
            parent, 0, 3,
            "⏱️ TIEMPO RESPUESTA",
            f"{stats['avg_response_time']:.1f} min",
            "Promedio general",
            ("purple", "darkmagenta")
        )
        
        # Segunda fila de tarjetas
        
        # Tarjeta 5: Llamadas activas
        self.create_stat_card(
            parent, 1, 0,
            "🚨 LLAMADAS ACTIVAS",
            str(stats['active_calls']),
            "En este momento",
            ("red", "darkred")
        )
        
        # Tarjeta 6: Móviles disponibles
        self.create_stat_card(
            parent, 1, 1,
            "🚗 MÓVILES DISPONIBLES",
            str(stats['available_mobiles']),
            f"de {stats['total_mobiles']} totales",
            ("teal", "darkcyan")
        )
        
        # Tarjeta 7: Usuarios activos
        self.create_stat_card(
            parent, 1, 2,
            "👥 USUARIOS ACTIVOS",
            str(stats['active_users']),
            "En el sistema",
            ("indigo", "darkslateblue")
        )
        
        # Tarjeta 8: Eficiencia del sistema
        efficiency = stats['efficiency_percentage']
        efficiency_color = ("green", "darkgreen") if efficiency >= 80 else ("orange", "darkorange") if efficiency >= 60 else ("red", "darkred")
        
        self.create_stat_card(
            parent, 1, 3,
            "📊 EFICIENCIA",
            f"{efficiency:.1f}%",
            "Llamadas resueltas",
            efficiency_color
        )
        
    def create_stat_card(self, parent, row, col, title, value, subtitle, color):
        """Crea una tarjeta de estadística"""
        
        card_frame = ctk.CTkFrame(parent, fg_color=color)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white"
        )
        title_label.grid(row=0, column=0, padx=15, pady=(15, 5))
        
        value_label = ctk.CTkLabel(
            card_frame,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        value_label.grid(row=1, column=0, padx=15, pady=5)
        
        subtitle_label = ctk.CTkLabel(
            card_frame,
            text=subtitle,
            font=ctk.CTkFont(size=10),
            text_color="lightgray"
        )
        subtitle_label.grid(row=2, column=0, padx=15, pady=(5, 15))
        
    def create_calls_chart(self, parent):
        """Crea el gráfico de llamadas por día"""
        
        chart_frame = ctk.CTkFrame(parent)
        chart_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=20, sticky="ew")
        
        title_label = ctk.CTkLabel(
            chart_frame,
            text="📈 LLAMADAS POR DÍA (ÚLTIMOS 30 DÍAS)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(15, 10))
        
        try:
            # Obtener datos para el gráfico
            chart_data = self.get_calls_by_day_data()
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor('#2b2b2b')  # Fondo oscuro
            ax.set_facecolor('#2b2b2b')
            
            # Datos
            dates = [item[0] for item in chart_data]
            calls = [item[1] for item in chart_data]
            
            # Crear gráfico
            ax.plot(dates, calls, color='#1f77b4', linewidth=2, marker='o', markersize=4)
            ax.fill_between(dates, calls, alpha=0.3, color='#1f77b4')
            
            # Configurar ejes
            ax.set_xlabel('Fecha', color='white')
            ax.set_ylabel('Número de Llamadas', color='white')
            ax.tick_params(colors='white')
            
            # Formato de fechas en el eje X
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            plt.xticks(rotation=45)
            
            # Grid
            ax.grid(True, alpha=0.3, color='white')
            
            # Ajustar layout
            plt.tight_layout()
            
            # Integrar en tkinter
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
            
            chart_frame.grid_columnconfigure(0, weight=1)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                chart_frame,
                text=f"Error creando gráfico: {str(e)}",
                font=ctk.CTkFont()
            )
            error_label.grid(row=1, column=0, pady=20)
    
    def create_emergency_types_tab(self):
        """Crea la pestaña de tipos de emergencia"""
        
        types_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(types_frame, text="🚨 Tipos de Emergencia")
        
        types_frame.grid_columnconfigure(0, weight=1)
        types_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(types_frame)
        scroll_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            scroll_frame,
            text="🚨 ESTADÍSTICAS POR TIPO DE EMERGENCIA",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 30))
        
        # Crear tabla de tipos de emergencia
        self.create_emergency_types_table(scroll_frame)
        
        # Gráfico de pastel si está disponible
        if MATPLOTLIB_AVAILABLE:
            self.create_emergency_pie_chart(scroll_frame)
    
    def create_emergency_types_table(self, parent):
        """Crea la tabla de tipos de emergencia"""
        
        # Frame para la tabla
        table_frame = ctk.CTkFrame(parent)
        table_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Título de la tabla
        table_title = ctk.CTkLabel(
            table_frame,
            text="📊 Resumen por Tipo",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        table_title.grid(row=0, column=0, pady=(15, 10))
        
        # Crear treeview
        tree_frame = tk.Frame(table_frame)
        tree_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        tree_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('Tipo', 'Total', 'Hoy', 'Esta Semana', 'Este Mes', 'Promedio Diario')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        tree.grid(row=0, column=0, sticky="ew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Llenar datos
        emergency_stats = self.get_emergency_types_statistics()
        for stat in emergency_stats:
            tree.insert('', 'end', values=stat)
    
    def create_emergency_pie_chart(self, parent):
        """Crea gráfico de pastel de tipos de emergencia"""
        
        chart_frame = ctk.CTkFrame(parent)
        chart_frame.grid(row=2, column=0, pady=20, sticky="ew")
        
        title_label = ctk.CTkLabel(
            chart_frame,
            text="🥧 DISTRIBUCIÓN POR TIPO DE EMERGENCIA",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(15, 10))
        
        try:
            # Obtener datos
            pie_data = self.get_emergency_pie_data()
            
            if pie_data:
                # Crear figura
                fig, ax = plt.subplots(figsize=(8, 6))
                fig.patch.set_facecolor('#2b2b2b')
                
                labels = [item[0] for item in pie_data]
                sizes = [item[1] for item in pie_data]
                colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
                
                # Crear gráfico de pastel
                wedges, texts, autotexts = ax.pie(
                    sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                    colors=colors[:len(labels)], textprops={'color': 'white'}
                )
                
                ax.set_title('Distribución de Emergencias', color='white', fontsize=14)
                
                # Integrar en tkinter
                canvas = FigureCanvasTkAgg(fig, chart_frame)
                canvas.draw()
                canvas.get_tk_widget().grid(row=1, column=0, padx=15, pady=(0, 15))
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                chart_frame,
                text=f"Error creando gráfico: {str(e)}",
                font=ctk.CTkFont()
            )
            error_label.grid(row=1, column=0, pady=20)
    
    def create_response_times_tab(self):
        """Crea la pestaña de tiempos de respuesta"""
        
        response_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(response_frame, text="⏱️ Tiempos de Respuesta")
        
        response_frame.grid_columnconfigure(0, weight=1)
        response_frame.grid_rowconfigure(0, weight=1)
        
        # Contenido pendiente de implementar
        placeholder_label = ctk.CTkLabel(
            response_frame,
            text="⏱️ ANÁLISIS DE TIEMPOS DE RESPUESTA\n\n(Funcionalidad en desarrollo)",
            font=ctk.CTkFont(size=16)
        )
        placeholder_label.grid(row=0, column=0, pady=50)
    
    def create_users_tab(self):
        """Crea la pestaña de estadísticas de usuarios"""
        
        users_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(users_frame, text="👥 Usuarios")
        
        users_frame.grid_columnconfigure(0, weight=1)
        users_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(users_frame)
        scroll_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            scroll_frame,
            text="👥 ESTADÍSTICAS DE USUARIOS",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 30))
        
        # Crear tabla de usuarios
        self.create_users_table(scroll_frame)
    
    def create_users_table(self, parent):
        """Crea la tabla de estadísticas de usuarios"""
        
        table_frame = ctk.CTkFrame(parent)
        table_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        table_frame.grid_columnconfigure(0, weight=1)
        
        table_title = ctk.CTkLabel(
            table_frame,
            text="📊 Actividad por Usuario",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        table_title.grid(row=0, column=0, pady=(15, 10))
        
        # Crear treeview
        tree_frame = tk.Frame(table_frame)
        tree_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        tree_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('Usuario', 'Nombre', 'Llamadas Registradas', 'Último Acceso', 'Estado')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            
        tree.column('Usuario', width=100)
        tree.column('Nombre', width=150)
        tree.column('Llamadas Registradas', width=120)
        tree.column('Último Acceso', width=130)
        tree.column('Estado', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        tree.grid(row=0, column=0, sticky="ew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Llenar datos
        users_stats = self.get_users_statistics()
        for stat in users_stats:
            tree.insert('', 'end', values=stat)
    
    def create_reports_tab(self):
        """Crea la pestaña de reportes"""
        
        reports_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(reports_frame, text="📋 Reportes")
        
        reports_frame.grid_columnconfigure(0, weight=1)
        reports_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(reports_frame)
        scroll_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        scroll_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            scroll_frame,
            text="📋 GENERACIÓN DE REPORTES",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))
        
        # Reportes predefinidos
        self.create_predefined_reports(scroll_frame)
        
        # Reporte personalizado
        self.create_custom_report_section(scroll_frame)
    
    def create_predefined_reports(self, parent):
        """Crea sección de reportes predefinidos"""
        
        predefined_frame = ctk.CTkFrame(parent)
        predefined_frame.grid(row=1, column=0, padx=(0, 10), pady=(0, 20), sticky="ew")
        predefined_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            predefined_frame,
            text="📊 Reportes Predefinidos",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(15, 20))
        
        # Botones de reportes
        reports = [
            ("📅 Reporte Diario", "Llamadas del día actual", self.generate_daily_report),
            ("📊 Reporte Semanal", "Resumen de la semana", self.generate_weekly_report),
            ("📈 Reporte Mensual", "Estadísticas del mes", self.generate_monthly_report),
            ("🚨 Reporte de Emergencias", "Todas las emergencias por tipo", self.generate_emergency_report),
            ("👥 Reporte de Usuarios", "Actividad de usuarios", self.generate_users_report),
            ("🚗 Reporte de Móviles", "Estado y uso de móviles", self.generate_mobiles_report)
        ]
        
        for i, (title, desc, command) in enumerate(reports):
            report_frame = ctk.CTkFrame(predefined_frame)
            report_frame.grid(row=i+1, column=0, padx=15, pady=5, sticky="ew")
            report_frame.grid_columnconfigure(0, weight=1)
            
            btn = ctk.CTkButton(
                report_frame,
                text=title,
                command=command,
                height=40,
                anchor="w"
            )
            btn.grid(row=0, column=0, padx=(15, 5), pady=10, sticky="ew")
            
            desc_label = ctk.CTkLabel(
                report_frame,
                text=desc,
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            desc_label.grid(row=0, column=1, padx=(5, 15), pady=10, sticky="e")
    
    def create_custom_report_section(self, parent):
        """Crea sección de reporte personalizado"""
        
        custom_frame = ctk.CTkFrame(parent)
        custom_frame.grid(row=1, column=1, padx=(10, 0), pady=(0, 20), sticky="ew")
        custom_frame.grid_columnconfigure(1, weight=1)
        
        title_label = ctk.CTkLabel(
            custom_frame,
            text="🔧 Reporte Personalizado",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(15, 20))
        
        # Fecha desde
        ctk.CTkLabel(custom_frame, text="Desde:").grid(row=1, column=0, padx=(15, 5), pady=5, sticky="w")
        self.custom_from_date = ctk.CTkEntry(custom_frame, placeholder_text="DD/MM/YYYY")
        self.custom_from_date.grid(row=1, column=1, padx=(0, 15), pady=5, sticky="ew")
        
        # Fecha hasta
        ctk.CTkLabel(custom_frame, text="Hasta:").grid(row=2, column=0, padx=(15, 5), pady=5, sticky="w")
        self.custom_to_date = ctk.CTkEntry(custom_frame, placeholder_text="DD/MM/YYYY")
        self.custom_to_date.grid(row=2, column=1, padx=(0, 15), pady=5, sticky="ew")
        
        # Tipo de emergencia
        ctk.CTkLabel(custom_frame, text="Tipo:").grid(row=3, column=0, padx=(15, 5), pady=5, sticky="w")
        self.custom_type_combo = ctk.CTkComboBox(custom_frame, values=["Todos"])
        self.custom_type_combo.grid(row=3, column=1, padx=(0, 15), pady=5, sticky="ew")
        
        # Cargar tipos de emergencia
        self.load_emergency_types_for_custom_report()
        
        # Botón generar
        generate_btn = ctk.CTkButton(
            custom_frame,
            text="📋 Generar Reporte",
            command=self.generate_custom_report,
            fg_color=("green", "darkgreen")
        )
        generate_btn.grid(row=4, column=0, columnspan=2, padx=15, pady=20, sticky="ew")
    
    # Métodos para obtener estadísticas
    
    def get_general_statistics(self):
        """Obtiene estadísticas generales del sistema"""
        try:
            stats = {}
            
            # Total de llamadas
            result = self.app.db_manager.fetch_one("SELECT COUNT(*) FROM llamadas")
            stats['total_calls'] = result[0] if result else 0
            
            # Llamadas hoy
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(*) FROM llamadas 
                WHERE DATE(fecha_hora) = DATE('now')
            """)
            stats['calls_today'] = result[0] if result else 0
            
            # Promedio diario último mes
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(*) / 30.0 FROM llamadas 
                WHERE fecha_hora >= DATE('now', '-30 days')
            """)
            stats['daily_average'] = result[0] if result else 0
            
            # Tiempo respuesta promedio (simulado)
            stats['avg_response_time'] = 8.5  # En desarrollo
            
            # Llamadas activas
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(*) FROM llamadas 
                WHERE estado IN ('activa', 'despachada', 'en_curso')
            """)
            stats['active_calls'] = result[0] if result else 0
            
            # Móviles disponibles
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(*) FROM moviles 
                WHERE estado = 'disponible' AND activo = 1
            """)
            stats['available_mobiles'] = result[0] if result else 0
            
            # Total móviles
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(*) FROM moviles WHERE activo = 1
            """)
            stats['total_mobiles'] = result[0] if result else 0
            
            # Usuarios activos
            result = self.app.db_manager.fetch_one("""
                SELECT COUNT(*) FROM usuarios WHERE activo = 1
            """)
            stats['active_users'] = result[0] if result else 0
            
            # Eficiencia del sistema (llamadas resueltas vs totales)
            result = self.app.db_manager.fetch_one("""
                SELECT 
                    (COUNT(CASE WHEN estado = 'finalizada' THEN 1 END) * 100.0) / COUNT(*)
                FROM llamadas
            """)
            stats['efficiency_percentage'] = result[0] if result and result[0] else 0
            
            return stats
            
        except Exception as e:
            print(f"Error obteniendo estadísticas generales: {e}")
            return {
                'total_calls': 0, 'calls_today': 0, 'daily_average': 0,
                'avg_response_time': 0, 'active_calls': 0, 'available_mobiles': 0,
                'total_mobiles': 0, 'active_users': 0, 'efficiency_percentage': 0
            }
    
    def get_calls_by_day_data(self):
        """Obtiene datos de llamadas por día para el gráfico"""
        try:
            # Obtener datos de los últimos 30 días
            data = self.app.db_manager.fetch_all("""
                SELECT DATE(fecha_hora) as fecha, COUNT(*) as cantidad
                FROM llamadas
                WHERE fecha_hora >= DATE('now', '-30 days')
                GROUP BY DATE(fecha_hora)
                ORDER BY fecha
            """)
            
            # Convertir fechas string a datetime
            chart_data = []
            for fecha_str, cantidad in data:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
                chart_data.append((fecha, cantidad))
            
            return chart_data
            
        except Exception as e:
            print(f"Error obteniendo datos de gráfico: {e}")
            return []
    
    def get_emergency_types_statistics(self):
        """Obtiene estadísticas por tipo de emergencia"""
        try:
            data = self.app.db_manager.fetch_all("""
                SELECT 
                    te.nombre,
                    COUNT(*) as total,
                    COUNT(CASE WHEN DATE(l.fecha_hora) = DATE('now') THEN 1 END) as hoy,
                    COUNT(CASE WHEN l.fecha_hora >= DATE('now', '-7 days') THEN 1 END) as semana,
                    COUNT(CASE WHEN l.fecha_hora >= DATE('now', '-30 days') THEN 1 END) as mes,
                    ROUND(COUNT(CASE WHEN l.fecha_hora >= DATE('now', '-30 days') THEN 1 END) / 30.0, 1) as promedio
                FROM tipos_emergencia te
                LEFT JOIN llamadas l ON te.id = l.tipo_emergencia_id
                GROUP BY te.id, te.nombre
                ORDER BY total DESC
            """)
            
            return data
            
        except Exception as e:
            print(f"Error obteniendo estadísticas de tipos: {e}")
            return []
    
    def get_emergency_pie_data(self):
        """Obtiene datos para gráfico de pastel de emergencias"""
        try:
            data = self.app.db_manager.fetch_all("""
                SELECT te.nombre, COUNT(*) as cantidad
                FROM tipos_emergencia te
                LEFT JOIN llamadas l ON te.id = l.tipo_emergencia_id
                WHERE l.id IS NOT NULL
                GROUP BY te.id, te.nombre
                HAVING cantidad > 0
                ORDER BY cantidad DESC
            """)
            
            return data
            
        except Exception as e:
            print(f"Error obteniendo datos de pastel: {e}")
            return []
    
    def get_users_statistics(self):
        """Obtiene estadísticas de usuarios"""
        try:
            data = self.app.db_manager.fetch_all("""
                SELECT 
                    u.username,
                    u.nombre_completo,
                    COUNT(l.id) as llamadas_registradas,
                    COALESCE(u.ultimo_acceso, 'Nunca') as ultimo_acceso,
                    CASE WHEN u.activo = 1 THEN 'Activo' ELSE 'Inactivo' END as estado
                FROM usuarios u
                LEFT JOIN llamadas l ON u.id = l.usuario_id
                GROUP BY u.id, u.username, u.nombre_completo, u.ultimo_acceso, u.activo
                ORDER BY llamadas_registradas DESC
            """)
            
            # Formatear fechas de último acceso
            formatted_data = []
            for row in data:
                formatted_row = list(row)
                if formatted_row[3] != 'Nunca':
                    try:
                        fecha = datetime.strptime(formatted_row[3], '%Y-%m-%d %H:%M:%S')
                        formatted_row[3] = fecha.strftime('%d/%m/%Y %H:%M')
                    except:
                        pass
                formatted_data.append(tuple(formatted_row))
            
            return formatted_data
            
        except Exception as e:
            print(f"Error obteniendo estadísticas de usuarios: {e}")
            return []
    
    def load_emergency_types_for_custom_report(self):
        """Carga tipos de emergencia para reporte personalizado"""
        try:
            types = self.app.db_manager.fetch_all("""
                SELECT nombre FROM tipos_emergencia ORDER BY nombre
            """)
            
            values = ["Todos"] + [t[0] for t in types]
            self.custom_type_combo.configure(values=values)
            self.custom_type_combo.set("Todos")
            
        except Exception as e:
            print(f"Error cargando tipos de emergencia: {e}")
    
    def load_statistics(self):
        """Carga todas las estadísticas"""
        # Las estadísticas se cargan cuando se crean las pestañas
        pass
    
    # Métodos para generar reportes
    
    def generate_daily_report(self):
        """Genera reporte diario"""
        messagebox.showinfo("Reporte", "Generando reporte diario...")
        # Implementar generación de reporte
        
    def generate_weekly_report(self):
        """Genera reporte semanal"""
        messagebox.showinfo("Reporte", "Generando reporte semanal...")
        
    def generate_monthly_report(self):
        """Genera reporte mensual"""
        messagebox.showinfo("Reporte", "Generando reporte mensual...")
        
    def generate_emergency_report(self):
        """Genera reporte de emergencias"""
        messagebox.showinfo("Reporte", "Generando reporte de emergencias...")
        
    def generate_users_report(self):
        """Genera reporte de usuarios"""
        messagebox.showinfo("Reporte", "Generando reporte de usuarios...")
        
    def generate_mobiles_report(self):
        """Genera reporte de móviles"""
        messagebox.showinfo("Reporte", "Generando reporte de móviles...")
        
    def generate_custom_report(self):
        """Genera reporte personalizado"""
        from_date = self.custom_from_date.get()
        to_date = self.custom_to_date.get()
        emergency_type = self.custom_type_combo.get()
        
        if not from_date or not to_date:
            messagebox.showerror("Error", "Debe especificar las fechas")
            return
        
        messagebox.showinfo("Reporte", 
                          f"Generando reporte personalizado:\n"
                          f"Desde: {from_date}\n"
                          f"Hasta: {to_date}\n"
                          f"Tipo: {emergency_type}")
