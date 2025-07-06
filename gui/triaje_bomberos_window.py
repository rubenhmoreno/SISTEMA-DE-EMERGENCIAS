"""
Ventana de Triaje Bomberos - Sistema de Emergencias
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class TriajeBomberosWindow(ctk.CTkToplevel):
    def __init__(self, app, parent, llamada_id):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        self.llamada_id = llamada_id
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Triaje de Emergencia - Bomberos")
        self.geometry("800x700")
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz de triaje de bomberos"""
        
        # Frame scrollable principal
        main_scroll = ctk.CTkScrollableFrame(self)
        main_scroll.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            main_scroll,
            text="🚒 TRIAJE DE EMERGENCIA - BOMBEROS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="orange"
        )
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Sección 1: Tipo de incendio
        self.create_fire_type_section(main_scroll, 1)
        
        # Sección 2: Personas en peligro
        self.create_people_section(main_scroll, 2)
        
        # Sección 3: Características del incendio
        self.create_fire_characteristics_section(main_scroll, 3)
        
        # Sección 4: Condiciones del lugar
        self.create_location_conditions_section(main_scroll, 4)
        
        # Sección 5: Recursos disponibles
        self.create_resources_section(main_scroll, 5)
        
        # Sección 6: Evaluación
        self.create_evaluation_section(main_scroll, 6)
        
        # Botones de acción
        self.create_action_buttons(main_scroll, 7)
        
    def create_fire_type_section(self, parent, row):
        """Sección de tipo de incendio"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🔥 TIPO DE INCENDIO",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Tipo de incendio
        type_frame = ctk.CTkFrame(section_frame)
        type_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            type_frame,
            text="¿Dónde se está produciendo el incendio?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(15, 10))
        
        self.tipo_incendio_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            type_frame,
            text="🏠 Domicilio/Vivienda",
            variable=self.tipo_incendio_var,
            value="domicilio"
        ).grid(row=1, column=0, padx=30, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            type_frame,
            text="🛣️ Vía pública",
            variable=self.tipo_incendio_var,
            value="via_publica"
        ).grid(row=2, column=0, padx=30, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            type_frame,
            text="🚗 Vehículo",
            variable=self.tipo_incendio_var,
            value="vehiculo"
        ).grid(row=3, column=0, padx=30, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            type_frame,
            text="🏭 Otro (especificar en observaciones)",
            variable=self.tipo_incendio_var,
            value="otro"
        ).grid(row=4, column=0, padx=30, pady=(5, 15), sticky="w")
        
    def create_people_section(self, parent, row):
        """Sección de personas en peligro"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="👥 PERSONAS EN PELIGRO",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        # Personas atrapadas
        atrapadas_frame = ctk.CTkFrame(section_frame)
        atrapadas_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            atrapadas_frame,
            text="¿Hay personas atrapadas?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.atrapadas_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            atrapadas_frame, text="❌ No", variable=self.atrapadas_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            atrapadas_frame, text="⚠️ No se sabe", variable=self.atrapadas_var, value="desconocido"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            atrapadas_frame, text="🚨 SÍ", variable=self.atrapadas_var, value="si"
        ).grid(row=3, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Información adicional
        info_frame = ctk.CTkFrame(section_frame)
        info_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            info_frame,
            text="Información sobre personas:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.personas_info_text = ctk.CTkTextbox(info_frame, height=80)
        self.personas_info_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        info_frame.grid_columnconfigure(0, weight=1)
        
    def create_fire_characteristics_section(self, parent, row):
        """Sección de características del incendio"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🔥 CARACTERÍSTICAS DEL INCENDIO",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        # Extensión aproximada
        extension_frame = ctk.CTkFrame(section_frame)
        extension_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            extension_frame,
            text="Extensión aproximada:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.extension_entry = ctk.CTkEntry(
            extension_frame, 
            placeholder_text="Ej: 2 habitaciones, motor del auto, etc."
        )
        self.extension_entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        extension_frame.grid_columnconfigure(0, weight=1)
        
        # Materiales involucrados
        materiales_frame = ctk.CTkFrame(section_frame)
        materiales_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            materiales_frame,
            text="Materiales involucrados:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.materiales_text = ctk.CTkTextbox(materiales_frame, height=60)
        self.materiales_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        materiales_frame.grid_columnconfigure(0, weight=1)
        
        # Explosivos o químicos
        explosivos_frame = ctk.CTkFrame(section_frame)
        explosivos_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            explosivos_frame,
            text="¿Hay presencia de explosivos, químicos o gases?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.explosivos_var = ctk.StringVar(value="no")
        
        buttons_frame = ctk.CTkFrame(explosivos_frame)
        buttons_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        ctk.CTkRadioButton(
            buttons_frame, text="❌ No", variable=self.explosivos_var, value="no"
        ).grid(row=0, column=0, padx=15, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            buttons_frame, text="⚠️ No se sabe", variable=self.explosivos_var, value="desconocido"
        ).grid(row=0, column=1, padx=15, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            buttons_frame, text="🧪 SÍ", variable=self.explosivos_var, value="si"
        ).grid(row=0, column=2, padx=15, pady=5, sticky="w")
        
    def create_location_conditions_section(self, parent, row):
        """Sección de condiciones del lugar"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🌬️ CONDICIONES DEL LUGAR",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        # Viento
        viento_frame = ctk.CTkFrame(section_frame)
        viento_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            viento_frame,
            text="Dirección del viento:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.viento_entry = ctk.CTkEntry(
            viento_frame, 
            placeholder_text="Ej: Norte, Sur, Sin viento"
        )
        self.viento_entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        viento_frame.grid_columnconfigure(0, weight=1)
        
        # Accesos
        accesos_frame = ctk.CTkFrame(section_frame)
        accesos_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            accesos_frame,
            text="Accesos disponibles:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.accesos_text = ctk.CTkTextbox(accesos_frame, height=60)
        self.accesos_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        accesos_frame.grid_columnconfigure(0, weight=1)
        
    def create_resources_section(self, parent, row):
        """Sección de recursos disponibles"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="💧 RECURSOS DISPONIBLES",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Hidrantes
        hidrantes_frame = ctk.CTkFrame(section_frame)
        hidrantes_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            hidrantes_frame,
            text="¿Hay hidrantes cercanos?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.hidrantes_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            hidrantes_frame, text="❌ No", variable=self.hidrantes_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            hidrantes_frame, text="⚠️ No se sabe", variable=self.hidrantes_var, value="desconocido"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            hidrantes_frame, text="✅ SÍ", variable=self.hidrantes_var, value="si"
        ).grid(row=3, column=0, padx=25, pady=(5, 15), sticky="w")
        
    def create_evaluation_section(self, parent, row):
        """Sección de evaluación"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="⚖️ EVALUACIÓN",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Nivel de prioridad
        priority_frame = ctk.CTkFrame(section_frame)
        priority_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            priority_frame,
            text="Nivel de Prioridad:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.prioridad_label = ctk.CTkLabel(
            priority_frame,
            text="Se calculará automáticamente",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.prioridad_label.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")
        
        # Botón calcular prioridad
        calc_btn = ctk.CTkButton(
            section_frame,
            text="🧮 Calcular Prioridad",
            command=self.calcular_prioridad,
            fg_color=("blue", "darkblue")
        )
        calc_btn.grid(row=2, column=0, padx=20, pady=(0, 15))
        
        # Observaciones
        ctk.CTkLabel(
            section_frame,
            text="Observaciones adicionales:",
            font=ctk.CTkFont(size=14)
        ).grid(row=3, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.observaciones_text = ctk.CTkTextbox(section_frame, height=80)
        self.observaciones_text.grid(row=4, column=0, padx=20, pady=(0, 15), sticky="ew")
        
    def create_action_buttons(self, parent, row):
        """Botones de acción"""
        
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=self.cancelar,
            fg_color=("gray", "darkgray")
        )
        cancel_btn.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Guardar triaje
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar Triaje",
            command=self.guardar_triaje,
            fg_color=("orange", "darkorange")
        )
        save_btn.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        
        # Enviar alerta
        alert_btn = ctk.CTkButton(
            buttons_frame,
            text="🚨 Enviar Alerta",
            command=self.enviar_alerta,
            fg_color=("red", "darkred")
        )
        alert_btn.grid(row=0, column=2, padx=20, pady=20, sticky="ew")
        
    def calcular_prioridad(self):
        """Calcula la prioridad basada en las respuestas del triaje"""
        try:
            prioridad = 3  # Prioridad media por defecto
            
            # Factores críticos (prioridad 1)
            if (self.atrapadas_var.get() == "si" or 
                self.explosivos_var.get() == "si"):
                prioridad = 1
                texto = "🔴 CRÍTICA - Alerta inmediata"
                color = "red"
                
            # Factores de alta prioridad (prioridad 2)
            elif (self.tipo_incendio_var.get() == "domicilio" and 
                  self.atrapadas_var.get() == "desconocido"):
                prioridad = 2
                texto = "🟠 ALTA - Alerta urgente"
                color = "orange"
                
            # Prioridad media (prioridad 3)
            elif self.tipo_incendio_var.get() in ["domicilio", "vehiculo"]:
                prioridad = 3
                texto = "🟡 MEDIA - Alerta normal"
                color = "yellow"
                
            # Prioridad baja (prioridad 4)
            else:
                prioridad = 4
                texto = "🟢 BAJA - Verificar situación"
                color = "green"
            
            # Actualizar label
            self.prioridad_label.configure(text=texto, text_color=color)
            self.nivel_prioridad = prioridad
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculando prioridad: {e}")
    
    def validar_triaje(self):
        """Valida que se hayan completado los campos obligatorios"""
        if not self.tipo_incendio_var.get():
            messagebox.showerror("Error", "Debe indicar el tipo de incendio")
            return False
            
        if not self.atrapadas_var.get():
            messagebox.showerror("Error", "Debe indicar si hay personas atrapadas")
            return False
            
        if not hasattr(self, 'nivel_prioridad'):
            messagebox.showerror("Error", "Debe calcular la prioridad primero")
            return False
            
        return True
    
    def guardar_triaje(self):
        """Guarda el triaje en la base de datos"""
        try:
            if not self.validar_triaje():
                return
            
            # Insertar triaje bomberos
            self.app.db_manager.execute_query("""
                INSERT INTO triaje_bomberos (
                    llamada_id, tipo_incendio, hay_personas_atrapadas, extension_aproximada,
                    materiales_involucrados, hay_explosivos, viento_direccion,
                    accesos_disponibles, hidrantes_cercanos, nivel_prioridad, observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.llamada_id,
                self.tipo_incendio_var.get(),
                1 if self.atrapadas_var.get() == "si" else 0,
                self.extension_entry.get(),
                self.materiales_text.get("1.0", "end-1c"),
                1 if self.explosivos_var.get() == "si" else 0,
                self.viento_entry.get(),
                self.accesos_text.get("1.0", "end-1c"),
                1 if self.hidrantes_var.get() == "si" else 0,
                self.nivel_prioridad,
                self.observaciones_text.get("1.0", "end-1c")
            ))
            
            messagebox.showinfo("Éxito", "Triaje de bomberos guardado correctamente")
            
            # Callback al parent
            self.parent.triaje_completado(self.llamada_id, False)  # Bomberos no despacha móviles propios
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando triaje: {e}")
    
    def enviar_alerta(self):
        """Guarda el triaje y envía alerta inmediata"""
        try:
            if not self.validar_triaje():
                return
            
            # Primero guardar el triaje
            self.guardar_triaje_silencioso()
            
            # Actualizar estado de la llamada
            self.app.db_manager.execute_query("""
                UPDATE llamadas SET estado = 'despachada', fecha_despacho = ?
                WHERE id = ?
            """, (datetime.now(), self.llamada_id))
            
            messagebox.showinfo("Alerta Enviada", 
                               "Alerta enviada a Bomberos.\n"
                               "El triaje ha sido guardado correctamente.")
            
            # Callback al parent
            self.parent.triaje_completado(self.llamada_id, True)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error enviando alerta: {e}")
    
    def guardar_triaje_silencioso(self):
        """Guarda el triaje sin mostrar mensajes"""
        self.app.db_manager.execute_query("""
            INSERT INTO triaje_bomberos (
                llamada_id, tipo_incendio, hay_personas_atrapadas, extension_aproximada,
                materiales_involucrados, hay_explosivos, viento_direccion,
                accesos_disponibles, hidrantes_cercanos, nivel_prioridad, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.llamada_id,
            self.tipo_incendio_var.get(),
            1 if self.atrapadas_var.get() == "si" else 0,
            self.extension_entry.get(),
            self.materiales_text.get("1.0", "end-1c"),
            1 if self.explosivos_var.get() == "si" else 0,
            self.viento_entry.get(),
            self.accesos_text.get("1.0", "end-1c"),
            1 if self.hidrantes_var.get() == "si" else 0,
            self.nivel_prioridad,
            self.observaciones_text.get("1.0", "end-1c")
        ))
    
    def cancelar(self):
        """Cancela el triaje"""
        if messagebox.askyesno("Cancelar", "¿Está seguro que desea cancelar el triaje?"):
            self.destroy()
