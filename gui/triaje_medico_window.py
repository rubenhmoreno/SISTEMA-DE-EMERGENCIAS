"""
Ventana de Triaje Médico - Sistema de Emergencias
Basado en protocolos DEMVA
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class TriajeMedicoWindow(ctk.CTkToplevel):
    def __init__(self, app, parent, llamada_id):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        self.llamada_id = llamada_id
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Triaje de Emergencia Médica")
        self.geometry("800x900")
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz de triaje médico"""
        
        # Frame scrollable principal
        main_scroll = ctk.CTkScrollableFrame(self)
        main_scroll.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            main_scroll,
            text="🚑 TRIAJE DE EMERGENCIA MÉDICA",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="red"
        )
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Sección 1: Estado de consciencia
        self.create_consciousness_section(main_scroll, 1)
        
        # Sección 2: Signos vitales
        self.create_vitals_section(main_scroll, 2)
        
        # Sección 3: Síntomas principales
        self.create_symptoms_section(main_scroll, 3)
        
        # Sección 4: Datos del paciente
        self.create_patient_data_section(main_scroll, 4)
        
        # Sección 5: Antecedentes
        self.create_history_section(main_scroll, 5)
        
        # Sección 6: Evaluación y destino
        self.create_evaluation_section(main_scroll, 6)
        
        # Botones de acción
        self.create_action_buttons(main_scroll, 7)
        
    def create_consciousness_section(self, parent, row):
        """Sección de estado de consciencia"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🧠 ESTADO DE CONSCIENCIA",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Pregunta principal
        question_frame = ctk.CTkFrame(section_frame)
        question_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            question_frame,
            text="¿El paciente está consciente y puede hablar?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=15)
        
        # Radio buttons
        self.consciente_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            question_frame,
            text="✅ Sí, está consciente y puede hablar",
            variable=self.consciente_var,
            value="si"
        ).grid(row=1, column=0, padx=40, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            question_frame,
            text="⚠️ Está consciente pero confundido",
            variable=self.consciente_var,
            value="confundido"
        ).grid(row=2, column=0, padx=40, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            question_frame,
            text="❌ No está consciente o no responde",
            variable=self.consciente_var,
            value="no"
        ).grid(row=3, column=0, padx=40, pady=(5, 15), sticky="w")
        
    def create_vitals_section(self, parent, row):
        """Sección de signos vitales"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="💓 SIGNOS VITALES",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        # Respiración
        resp_frame = ctk.CTkFrame(section_frame)
        resp_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            resp_frame,
            text="¿Respira normalmente?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.respira_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            resp_frame, text="✅ Normal", variable=self.respira_var, value="si"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            resp_frame, text="⚠️ Dificultad", variable=self.respira_var, value="dificultad"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            resp_frame, text="❌ No respira", variable=self.respira_var, value="no"
        ).grid(row=3, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Pulso
        pulso_frame = ctk.CTkFrame(section_frame)
        pulso_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            pulso_frame,
            text="¿Tiene pulso perceptible?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.pulso_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            pulso_frame, text="✅ Normal", variable=self.pulso_var, value="si"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            pulso_frame, text="⚠️ Débil/rápido", variable=self.pulso_var, value="alterado"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            pulso_frame, text="❌ No se percibe", variable=self.pulso_var, value="no"
        ).grid(row=3, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Sangrado
        sangrado_frame = ctk.CTkFrame(section_frame)
        sangrado_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            sangrado_frame,
            text="¿Hay sangrado abundante visible?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.sangrado_var = ctk.StringVar(value="")
        
        buttons_frame = ctk.CTkFrame(sangrado_frame)
        buttons_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        ctk.CTkRadioButton(
            buttons_frame, text="❌ No hay sangrado", variable=self.sangrado_var, value="no"
        ).grid(row=0, column=0, padx=15, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            buttons_frame, text="⚠️ Sangrado leve", variable=self.sangrado_var, value="leve"
        ).grid(row=0, column=1, padx=15, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            buttons_frame, text="🩸 Sangrado abundante", variable=self.sangrado_var, value="abundante"
        ).grid(row=0, column=2, padx=15, pady=5, sticky="w")
        
    def create_symptoms_section(self, parent, row):
        """Sección de síntomas principales"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🩺 SÍNTOMAS PRINCIPALES",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Dolor de pecho
        dolor_frame = ctk.CTkFrame(section_frame)
        dolor_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            dolor_frame,
            text="¿Presenta dolor en el pecho?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.dolor_pecho_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            dolor_frame, text="❌ No", variable=self.dolor_pecho_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            dolor_frame, text="⚠️ Dolor leve", variable=self.dolor_pecho_var, value="leve"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            dolor_frame, text="🫀 Dolor intenso", variable=self.dolor_pecho_var, value="intenso"
        ).grid(row=3, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Síntomas adicionales
        sintomas_frame = ctk.CTkFrame(section_frame)
        sintomas_frame.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            sintomas_frame,
            text="Descripción detallada de síntomas:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.sintomas_text = ctk.CTkTextbox(sintomas_frame, height=80)
        self.sintomas_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        sintomas_frame.grid_columnconfigure(0, weight=1)
        
    def create_patient_data_section(self, parent, row):
        """Sección de datos del paciente"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((1, 3), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="👤 DATOS DEL PACIENTE",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 15))
        
        # Edad aproximada
        ctk.CTkLabel(section_frame, text="Edad aproximada:").grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.edad_entry = ctk.CTkEntry(section_frame, placeholder_text="Años", width=100)
        self.edad_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Sexo
        ctk.CTkLabel(section_frame, text="Sexo:").grid(row=1, column=2, padx=(20, 10), pady=10, sticky="w")
        self.sexo_combo = ctk.CTkComboBox(
            section_frame, 
            values=["Masculino", "Femenino", "No especificado"],
            state="readonly",
            width=150
        )
        self.sexo_combo.grid(row=1, column=3, padx=(0, 20), pady=10, sticky="w")
        
    def create_history_section(self, parent, row):
        """Sección de antecedentes"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="📋 ANTECEDENTES MÉDICOS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Antecedentes relevantes
        ctk.CTkLabel(
            section_frame,
            text="Antecedentes médicos relevantes:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.antecedentes_text = ctk.CTkTextbox(section_frame, height=60)
        self.antecedentes_text.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        # Medicamentos actuales
        ctk.CTkLabel(
            section_frame,
            text="Medicamentos que toma actualmente:",
            font=ctk.CTkFont(size=14)
        ).grid(row=3, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.medicamentos_text = ctk.CTkTextbox(section_frame, height=60)
        self.medicamentos_text.grid(row=4, column=0, padx=20, pady=(0, 15), sticky="ew")
        
    def create_evaluation_section(self, parent, row):
        """Sección de evaluación y destino"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="⚕️ EVALUACIÓN Y DESTINO",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Nivel de prioridad (calculado automáticamente)
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
        
        # Destino
        destino_frame = ctk.CTkFrame(section_frame)
        destino_frame.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            destino_frame,
            text="Destino del paciente:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.destino_var = ctk.StringVar(value="DEMVA")
        
        ctk.CTkRadioButton(
            destino_frame,
            text="🏥 DEMVA (Departamento de Emergencias Médicas Villa Allende)",
            variable=self.destino_var,
            value="DEMVA"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            destino_frame,
            text="🚑 CEC (Centro de Emergencias Coordinado)",
            variable=self.destino_var,
            value="CEC"
        ).grid(row=2, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Botón calcular prioridad
        calc_btn = ctk.CTkButton(
            section_frame,
            text="🧮 Calcular Prioridad",
            command=self.calcular_prioridad,
            fg_color=("blue", "darkblue")
        )
        calc_btn.grid(row=3, column=0, padx=20, pady=(0, 15))
        
        # Observaciones
        ctk.CTkLabel(
            section_frame,
            text="Observaciones adicionales:",
            font=ctk.CTkFont(size=14)
        ).grid(row=4, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.observaciones_text = ctk.CTkTextbox(section_frame, height=80)
        self.observaciones_text.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="ew")
        
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
        
        # Guardar sin despachar
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar Triaje",
            command=self.guardar_triaje,
            fg_color=("orange", "darkorange")
        )
        save_btn.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        
        # Despachar móvil
        dispatch_btn = ctk.CTkButton(
            buttons_frame,
            text="🚑 Despachar Móvil",
            command=self.despachar_movil,
            fg_color=("red", "darkred")
        )
        dispatch_btn.grid(row=0, column=2, padx=20, pady=20, sticky="ew")
        
    def calcular_prioridad(self):
        """Calcula la prioridad basada en las respuestas del triaje"""
        try:
            prioridad = 5  # Prioridad baja por defecto
            
            # Factores críticos (prioridad 1 - crítica)
            if (self.consciente_var.get() == "no" or 
                self.respira_var.get() == "no" or 
                self.pulso_var.get() == "no" or
                self.sangrado_var.get() == "abundante"):
                prioridad = 1
                texto = "🔴 CRÍTICA - Despacho inmediato"
                color = "red"
                
            # Factores de alta prioridad (prioridad 2)
            elif (self.consciente_var.get() == "confundido" or
                  self.respira_var.get() == "dificultad" or
                  self.pulso_var.get() == "alterado" or
                  self.dolor_pecho_var.get() == "intenso"):
                prioridad = 2
                texto = "🟠 ALTA - Despacho urgente"
                color = "orange"
                
            # Prioridad media (prioridad 3)
            elif (self.dolor_pecho_var.get() == "leve" or
                  self.sangrado_var.get() == "leve"):
                prioridad = 3
                texto = "🟡 MEDIA - Despacho en breve"
                color = "yellow"
                
            # Prioridad baja (prioridad 4-5)
            else:
                prioridad = 4
                texto = "🟢 BAJA - Evaluación telefónica"
                color = "green"
            
            # Actualizar label
            self.prioridad_label.configure(text=texto, text_color=color)
            self.nivel_prioridad = prioridad
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculando prioridad: {e}")
    
    def validar_triaje(self):
        """Valida que se hayan completado los campos obligatorios"""
        if not self.consciente_var.get():
            messagebox.showerror("Error", "Debe indicar el estado de consciencia")
            return False
            
        if not self.respira_var.get():
            messagebox.showerror("Error", "Debe indicar si respira normalmente")
            return False
            
        if not self.pulso_var.get():
            messagebox.showerror("Error", "Debe indicar si tiene pulso")
            return False
            
        if not self.sangrado_var.get():
            messagebox.showerror("Error", "Debe indicar si hay sangrado")
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
            
            # Insertar triaje médico
            self.app.db_manager.execute_query("""
                INSERT INTO triaje_medico (
                    llamada_id, paciente_consciente, respira_normal, pulso_presente,
                    sangrado_abundante, dolor_pecho, edad_aproximada, sexo,
                    sintomas_principales, antecedentes_relevantes, medicamentos_actuales,
                    nivel_prioridad, recomendacion_despacho, observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.llamada_id,
                1 if self.consciente_var.get() == "si" else 0,
                1 if self.respira_var.get() == "si" else 0,
                1 if self.pulso_var.get() == "si" else 0,
                1 if self.sangrado_var.get() == "abundante" else 0,
                1 if self.dolor_pecho_var.get() in ["leve", "intenso"] else 0,
                int(self.edad_entry.get()) if self.edad_entry.get().isdigit() else None,
                self.sexo_combo.get() if self.sexo_combo.get() != "No especificado" else None,
                self.sintomas_text.get("1.0", "end-1c"),
                self.antecedentes_text.get("1.0", "end-1c"),
                self.medicamentos_text.get("1.0", "end-1c"),
                self.nivel_prioridad,
                1 if self.nivel_prioridad <= 2 else 0,
                self.observaciones_text.get("1.0", "end-1c")
            ))
            
            # Actualizar receptor destino en la llamada
            self.app.db_manager.execute_query("""
                UPDATE llamadas SET receptor_destino = ? WHERE id = ?
            """, (self.destino_var.get(), self.llamada_id))
            
            messagebox.showinfo("Éxito", "Triaje médico guardado correctamente")
            
            # Callback al parent
            despachar = self.nivel_prioridad <= 2
            self.parent.triaje_completado(self.llamada_id, despachar)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando triaje: {e}")
    
    def despachar_movil(self):
        """Guarda el triaje y procede a despachar móvil"""
        try:
            if not self.validar_triaje():
                return
            
            # Primero guardar el triaje
            self.guardar_triaje_silencioso()
            
            # Cambiar estado de la llamada
            self.app.db_manager.execute_query("""
                UPDATE llamadas SET estado = 'despachada', fecha_despacho = ?
                WHERE id = ?
            """, (datetime.now(), self.llamada_id))
            
            messagebox.showinfo("Móvil Despachado", 
                               f"Móvil despachado para emergencia médica.\n"
                               f"Destino: {self.destino_var.get()}\n"
                               f"Prioridad: {self.nivel_prioridad}")
            
            # Callback al parent
            self.parent.triaje_completado(self.llamada_id, True)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error despachando móvil: {e}")
    
    def guardar_triaje_silencioso(self):
        """Guarda el triaje sin mostrar mensajes"""
        self.app.db_manager.execute_query("""
            INSERT INTO triaje_medico (
                llamada_id, paciente_consciente, respira_normal, pulso_presente,
                sangrado_abundante, dolor_pecho, edad_aproximada, sexo,
                sintomas_principales, antecedentes_relevantes, medicamentos_actuales,
                nivel_prioridad, recomendacion_despacho, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.llamada_id,
            1 if self.consciente_var.get() == "si" else 0,
            1 if self.respira_var.get() == "si" else 0,
            1 if self.pulso_var.get() == "si" else 0,
            1 if self.sangrado_var.get() == "abundante" else 0,
            1 if self.dolor_pecho_var.get() in ["leve", "intenso"] else 0,
            int(self.edad_entry.get()) if self.edad_entry.get().isdigit() else None,
            self.sexo_combo.get() if self.sexo_combo.get() != "No especificado" else None,
            self.sintomas_text.get("1.0", "end-1c"),
            self.antecedentes_text.get("1.0", "end-1c"),
            self.medicamentos_text.get("1.0", "end-1c"),
            self.nivel_prioridad,
            1 if self.nivel_prioridad <= 2 else 0,
            self.observaciones_text.get("1.0", "end-1c")
        ))
        
        # Actualizar receptor destino
        self.app.db_manager.execute_query("""
            UPDATE llamadas SET receptor_destino = ? WHERE id = ?
        """, (self.destino_var.get(), self.llamada_id))
    
    def cancelar(self):
        """Cancela el triaje"""
        if messagebox.askyesno("Cancelar", "¿Está seguro que desea cancelar el triaje?"):
            self.destroy()
