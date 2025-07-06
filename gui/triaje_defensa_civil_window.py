"""
Ventana de Triaje Defensa Civil - Sistema de Emergencias
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class TriajeDefensaCivilWindow(ctk.CTkToplevel):
    def __init__(self, app, parent, llamada_id):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        self.llamada_id = llamada_id
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Triaje de Emergencia - Defensa Civil")
        self.geometry("800x800")
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz de triaje de defensa civil"""
        
        # Frame scrollable principal
        main_scroll = ctk.CTkScrollableFrame(self)
        main_scroll.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            main_scroll,
            text="🏗️ TRIAJE DE EMERGENCIA - DEFENSA CIVIL",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="blue"
        )
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Sección 1: Tipo de evento
        self.create_event_type_section(main_scroll, 1)
        
        # Sección 2: Personas afectadas
        self.create_people_affected_section(main_scroll, 2)
        
        # Sección 3: Daños y servicios
        self.create_damages_section(main_scroll, 3)
        
        # Sección 4: Evacuación
        self.create_evacuation_section(main_scroll, 4)
        
        # Sección 5: Recursos y coordinación
        self.create_resources_coordination_section(main_scroll, 5)
        
        # Sección 6: Evaluación
        self.create_evaluation_section(main_scroll, 6)
        
        # Botones de acción
        self.create_action_buttons(main_scroll, 7)
        
    def create_event_type_section(self, parent, row):
        """Sección de tipo de evento"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="⚡ TIPO DE EVENTO",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Tipo de evento
        type_frame = ctk.CTkFrame(section_frame)
        type_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            type_frame,
            text="Seleccione el tipo de evento:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.tipo_evento_combo = ctk.CTkComboBox(
            type_frame,
            values=[
                "Inundación", "Temporal de viento", "Granizo", "Caída de árboles",
                "Deslizamiento de tierra", "Colapso estructural", "Corte de servicios",
                "Emergencia climática", "Accidente vial grave", "Derrame de sustancias",
                "Otro (especificar en observaciones)"
            ],
            state="readonly"
        )
        self.tipo_evento_combo.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        type_frame.grid_columnconfigure(0, weight=1)
        
    def create_people_affected_section(self, parent, row):
        """Sección de personas afectadas"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="👥 PERSONAS AFECTADAS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        # Personas afectadas
        afectadas_frame = ctk.CTkFrame(section_frame)
        afectadas_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            afectadas_frame,
            text="Cantidad de personas afectadas:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.personas_afectadas_entry = ctk.CTkEntry(
            afectadas_frame, 
            placeholder_text="Número aproximado"
        )
        self.personas_afectadas_entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        afectadas_frame.grid_columnconfigure(0, weight=1)
        
        # Personas evacuadas
        evacuadas_frame = ctk.CTkFrame(section_frame)
        evacuadas_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            evacuadas_frame,
            text="Personas ya evacuadas:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.personas_evacuadas_entry = ctk.CTkEntry(
            evacuadas_frame, 
            placeholder_text="Número"
        )
        self.personas_evacuadas_entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        evacuadas_frame.grid_columnconfigure(0, weight=1)
        
    def create_damages_section(self, parent, row):
        """Sección de daños y servicios"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🏠 DAÑOS Y SERVICIOS AFECTADOS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Daños estructurales
        damages_frame = ctk.CTkFrame(section_frame)
        damages_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            damages_frame,
            text="¿Hay daños estructurales?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.danos_estructurales_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            damages_frame, text="❌ No", variable=self.danos_estructurales_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            damages_frame, text="⚠️ Daños menores", variable=self.danos_estructurales_var, value="menores"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            damages_frame, text="🏠 Daños importantes", variable=self.danos_estructurales_var, value="importantes"
        ).grid(row=3, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            damages_frame, text="🏚️ Colapso/riesgo grave", variable=self.danos_estructurales_var, value="grave"
        ).grid(row=4, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Servicios afectados
        services_frame = ctk.CTkFrame(section_frame)
        services_frame.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            services_frame,
            text="Servicios públicos afectados:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.servicios_text = ctk.CTkTextbox(services_frame, height=60)
        self.servicios_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        services_frame.grid_columnconfigure(0, weight=1)
        
    def create_evacuation_section(self, parent, row):
        """Sección de evacuación"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🚨 EVACUACIÓN",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        # Necesidad de evacuación
        evacuation_frame = ctk.CTkFrame(section_frame)
        evacuation_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            evacuation_frame,
            text="¿Se necesita evacuación?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.necesidad_evacuacion_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            evacuation_frame, text="❌ No", variable=self.necesidad_evacuacion_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            evacuation_frame, text="⚠️ Preventiva", variable=self.necesidad_evacuacion_var, value="preventiva"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            evacuation_frame, text="🚨 Inmediata", variable=self.necesidad_evacuacion_var, value="inmediata"
        ).grid(row=3, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Acceso vehicular
        access_frame = ctk.CTkFrame(section_frame)
        access_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            access_frame,
            text="¿Hay acceso vehicular?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.acceso_vehicular_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            access_frame, text="✅ Normal", variable=self.acceso_vehicular_var, value="normal"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            access_frame, text="⚠️ Dificultoso", variable=self.acceso_vehicular_var, value="dificultoso"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            access_frame, text="❌ Bloqueado", variable=self.acceso_vehicular_var, value="bloqueado"
        ).grid(row=3, column=0, padx=25, pady=(5, 15), sticky="w")
        
    def create_resources_coordination_section(self, parent, row):
        """Sección de recursos y coordinación"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🤝 RECURSOS Y COORDINACIÓN",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Recursos necesarios
        resources_frame = ctk.CTkFrame(section_frame)
        resources_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            resources_frame,
            text="Recursos necesarios:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.recursos_text = ctk.CTkTextbox(resources_frame, height=60)
        self.recursos_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        resources_frame.grid_columnconfigure(0, weight=1)
        
        # Coordinación con otros organismos
        coordination_frame = ctk.CTkFrame(section_frame)
        coordination_frame.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            coordination_frame,
            text="Coordinación con otros organismos:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.coordinacion_text = ctk.CTkTextbox(coordination_frame, height=60)
        self.coordinacion_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        coordination_frame.grid_columnconfigure(0, weight=1)
        
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
            fg_color=("blue", "darkblue")
        )
        save_btn.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        
        # Activar protocolo
        protocol_btn = ctk.CTkButton(
            buttons_frame,
            text="🚨 Activar Protocolo",
            command=self.activar_protocolo,
            fg_color=("red", "darkred")
        )
        protocol_btn.grid(row=0, column=2, padx=20, pady=20, sticky="ew")
        
    def calcular_prioridad(self):
        """Calcula la prioridad basada en las respuestas del triaje"""
        try:
            prioridad = 4  # Prioridad baja por defecto
            
            # Factores críticos (prioridad 1)
            if (self.danos_estructurales_var.get() == "grave" or 
                self.necesidad_evacuacion_var.get() == "inmediata"):
                prioridad = 1
                texto = "🔴 CRÍTICA - Activación inmediata"
                color = "red"
                
            # Factores de alta prioridad (prioridad 2)
            elif (self.danos_estructurales_var.get() == "importantes" or
                  self.necesidad_evacuacion_var.get() == "preventiva" or
                  self.acceso_vehicular_var.get() == "bloqueado"):
                prioridad = 2
                texto = "🟠 ALTA - Activación urgente"
                color = "orange"
                
            # Prioridad media (prioridad 3)
            elif (self.danos_estructurales_var.get() == "menores" or
                  self.acceso_vehicular_var.get() == "dificultoso" or
                  (self.personas_afectadas_entry.get().isdigit() and 
                   int(self.personas_afectadas_entry.get()) > 10)):
                prioridad = 3
                texto = "🟡 MEDIA - Evaluación necesaria"
                color = "yellow"
                
            # Prioridad baja (prioridad 4)
            else:
                prioridad = 4
                texto = "🟢 BAJA - Seguimiento preventivo"
                color = "green"
            
            # Actualizar label
            self.prioridad_label.configure(text=texto, text_color=color)
            self.nivel_prioridad = prioridad
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculando prioridad: {e}")
    
    def validar_triaje(self):
        """Valida que se hayan completado los campos obligatorios"""
        if not self.tipo_evento_combo.get():
            messagebox.showerror("Error", "Debe seleccionar el tipo de evento")
            return False
            
        if not self.danos_estructurales_var.get():
            messagebox.showerror("Error", "Debe indicar si hay daños estructurales")
            return False
            
        if not self.necesidad_evacuacion_var.get():
            messagebox.showerror("Error", "Debe indicar si se necesita evacuación")
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
            
            # Insertar triaje defensa civil
            self.app.db_manager.execute_query("""
                INSERT INTO triaje_defensa_civil (
                    llamada_id, tipo_evento, personas_afectadas, personas_evacuadas,
                    daños_estructurales, servicios_afectados, necesidad_evacuacion,
                    recursos_necesarios, acceso_vehicular, coordinacion_otros_organismos,
                    nivel_prioridad, observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.llamada_id,
                self.tipo_evento_combo.get(),
                int(self.personas_afectadas_entry.get()) if self.personas_afectadas_entry.get().isdigit() else 0,
                int(self.personas_evacuadas_entry.get()) if self.personas_evacuadas_entry.get().isdigit() else 0,
                1 if self.danos_estructurales_var.get() in ["importantes", "grave"] else 0,
                self.servicios_text.get("1.0", "end-1c"),
                1 if self.necesidad_evacuacion_var.get() in ["preventiva", "inmediata"] else 0,
                self.recursos_text.get("1.0", "end-1c"),
                1 if self.acceso_vehicular_var.get() == "normal" else 0,
                self.coordinacion_text.get("1.0", "end-1c"),
                self.nivel_prioridad,
                self.observaciones_text.get("1.0", "end-1c")
            ))
            
            messagebox.showinfo("Éxito", "Triaje de defensa civil guardado correctamente")
            
            # Callback al parent
            activar = self.nivel_prioridad <= 2
            self.parent.triaje_completado(self.llamada_id, activar)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando triaje: {e}")
    
    def activar_protocolo(self):
        """Guarda el triaje y activa protocolo de emergencia"""
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
            
            messagebox.showinfo("Protocolo Activado", 
                               "Protocolo de Defensa Civil activado.\n"
                               "Se ha notificado a las autoridades correspondientes.")
            
            # Callback al parent
            self.parent.triaje_completado(self.llamada_id, True)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error activando protocolo: {e}")
    
    def guardar_triaje_silencioso(self):
        """Guarda el triaje sin mostrar mensajes"""
        self.app.db_manager.execute_query("""
            INSERT INTO triaje_defensa_civil (
                llamada_id, tipo_evento, personas_afectadas, personas_evacuadas,
                daños_estructurales, servicios_afectados, necesidad_evacuacion,
                recursos_necesarios, acceso_vehicular, coordinacion_otros_organismos,
                nivel_prioridad, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.llamada_id,
            self.tipo_evento_combo.get(),
            int(self.personas_afectadas_entry.get()) if self.personas_afectadas_entry.get().isdigit() else 0,
            int(self.personas_evacuadas_entry.get()) if self.personas_evacuadas_entry.get().isdigit() else 0,
            1 if self.danos_estructurales_var.get() in ["importantes", "grave"] else 0,
            self.servicios_text.get("1.0", "end-1c"),
            1 if self.necesidad_evacuacion_var.get() in ["preventiva", "inmediata"] else 0,
            self.recursos_text.get("1.0", "end-1c"),
            1 if self.acceso_vehicular_var.get() == "normal" else 0,
            self.coordinacion_text.get("1.0", "end-1c"),
            self.nivel_prioridad,
            self.observaciones_text.get("1.0", "end-1c")
        ))
    
    def cancelar(self):
        """Cancela el triaje"""
        if messagebox.askyesno("Cancelar", "¿Está seguro que desea cancelar el triaje?"):
            self.destroy()
