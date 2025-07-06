"""
Ventana de Triaje Seguridad Ciudadana - Sistema de Emergencias
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class TriajeSeguridadWindow(ctk.CTkToplevel):
    def __init__(self, app, parent, llamada_id):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        self.llamada_id = llamada_id
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Triaje de Seguridad Ciudadana")
        self.geometry("800x900")
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz de triaje de seguridad"""
        
        # Frame scrollable principal
        main_scroll = ctk.CTkScrollableFrame(self)
        main_scroll.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            main_scroll,
            text="👮 TRIAJE DE SEGURIDAD CIUDADANA",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="green"
        )
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Sección 1: Tipo de incidente
        self.create_incident_type_section(main_scroll, 1)
        
        # Sección 2: Estado de la situación
        self.create_situation_status_section(main_scroll, 2)
        
        # Sección 3: Personas involucradas
        self.create_people_involved_section(main_scroll, 3)
        
        # Sección 4: Vehículos involucrados
        self.create_vehicles_section(main_scroll, 4)
        
        # Sección 5: Testigos y evidencia
        self.create_witnesses_section(main_scroll, 5)
        
        # Sección 6: Recursos adicionales
        self.create_additional_resources_section(main_scroll, 6)
        
        # Sección 7: Evaluación
        self.create_evaluation_section(main_scroll, 7)
        
        # Botones de acción
        self.create_action_buttons(main_scroll, 8)
        
    def create_incident_type_section(self, parent, row):
        """Sección de tipo de incidente"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🚨 TIPO DE INCIDENTE",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Tipo de incidente
        type_frame = ctk.CTkFrame(section_frame)
        type_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            type_frame,
            text="Seleccione el tipo de incidente:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.tipo_incidente_combo = ctk.CTkComboBox(
            type_frame,
            values=[
                "Robo/Hurto", "Accidente de tránsito", "Violencia doméstica",
                "Disturbios/Peleas", "Vandalismo", "Persona sospechosa",
                "Vehículo abandonado", "Ruidos molestos", "Denuncia vecinal",
                "Emergencia médica menor", "Otro (especificar)"
            ],
            state="readonly"
        )
        self.tipo_incidente_combo.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        type_frame.grid_columnconfigure(0, weight=1)
        
    def create_situation_status_section(self, parent, row):
        """Sección de estado de la situación"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="⚠️ ESTADO DE LA SITUACIÓN",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        # Heridos
        heridos_frame = ctk.CTkFrame(section_frame)
        heridos_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            heridos_frame,
            text="¿Hay personas heridas?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.heridos_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            heridos_frame, text="❌ No", variable=self.heridos_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            heridos_frame, text="⚠️ Heridas leves", variable=self.heridos_var, value="leves"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            heridos_frame, text="🩸 Heridas graves", variable=self.heridos_var, value="graves"
        ).grid(row=3, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Agresor presente
        agresor_frame = ctk.CTkFrame(section_frame)
        agresor_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            agresor_frame,
            text="¿El agresor está presente?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.agresor_presente_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            agresor_frame, text="❌ No/Se fue", variable=self.agresor_presente_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            agresor_frame, text="❓ No se sabe", variable=self.agresor_presente_var, value="desconocido"
        ).grid(row=2, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            agresor_frame, text="🚨 SÍ, está presente", variable=self.agresor_presente_var, value="si"
        ).grid(row=3, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Agresor armado
        armado_frame = ctk.CTkFrame(section_frame)
        armado_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            armado_frame,
            text="¿El agresor está armado?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.agresor_armado_var = ctk.StringVar(value="")
        
        buttons_frame = ctk.CTkFrame(armado_frame)
        buttons_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        ctk.CTkRadioButton(
            buttons_frame, text="❌ No", variable=self.agresor_armado_var, value="no"
        ).grid(row=0, column=0, padx=15, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            buttons_frame, text="❓ No se sabe", variable=self.agresor_armado_var, value="desconocido"
        ).grid(row=0, column=1, padx=15, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            buttons_frame, text="🔫 Arma de fuego", variable=self.agresor_armado_var, value="arma_fuego"
        ).grid(row=0, column=2, padx=15, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            buttons_frame, text="🔪 Arma blanca", variable=self.agresor_armado_var, value="arma_blanca"
        ).grid(row=0, column=3, padx=15, pady=5, sticky="w")
        
    def create_people_involved_section(self, parent, row):
        """Sección de personas involucradas"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="👥 PERSONAS INVOLUCRADAS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Descripción de personas
        people_frame = ctk.CTkFrame(section_frame)
        people_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            people_frame,
            text="Descripción de personas involucradas:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.personas_text = ctk.CTkTextbox(people_frame, height=80)
        self.personas_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        people_frame.grid_columnconfigure(0, weight=1)
        
    def create_vehicles_section(self, parent, row):
        """Sección de vehículos involucrados"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🚗 VEHÍCULOS INVOLUCRADOS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Vehículos
        vehicles_frame = ctk.CTkFrame(section_frame)
        vehicles_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            vehicles_frame,
            text="Información de vehículos (patentes, características, etc.):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.vehiculos_text = ctk.CTkTextbox(vehicles_frame, height=80)
        self.vehiculos_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        vehicles_frame.grid_columnconfigure(0, weight=1)
        
    def create_witnesses_section(self, parent, row):
        """Sección de testigos y evidencia"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="👁️ TESTIGOS Y EVIDENCIA",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        # Testigos presentes
        testigos_frame = ctk.CTkFrame(section_frame)
        testigos_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            testigos_frame,
            text="¿Hay testigos presentes?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.testigos_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            testigos_frame, text="❌ No", variable=self.testigos_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            testigos_frame, text="✅ SÍ", variable=self.testigos_var, value="si"
        ).grid(row=2, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Peligro inmediato
        peligro_frame = ctk.CTkFrame(section_frame)
        peligro_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            peligro_frame,
            text="¿Hay peligro inmediato?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.peligro_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            peligro_frame, text="❌ No", variable=self.peligro_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            peligro_frame, text="🚨 SÍ", variable=self.peligro_var, value="si"
        ).grid(row=2, column=0, padx=25, pady=(5, 15), sticky="w")
        
    def create_additional_resources_section(self, parent, row):
        """Sección de recursos adicionales"""
        
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=row, column=0, padx=0, pady=(0, 20), sticky="ew")
        section_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            section_frame,
            text="🚑 RECURSOS ADICIONALES NECESARIOS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        # Ambulancia
        ambulancia_frame = ctk.CTkFrame(section_frame)
        ambulancia_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            ambulancia_frame,
            text="¿Se necesita ambulancia?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.ambulancia_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            ambulancia_frame, text="❌ No", variable=self.ambulancia_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            ambulancia_frame, text="🚑 SÍ", variable=self.ambulancia_var, value="si"
        ).grid(row=2, column=0, padx=25, pady=(5, 15), sticky="w")
        
        # Bomberos
        bomberos_frame = ctk.CTkFrame(section_frame)
        bomberos_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            bomberos_frame,
            text="¿Se necesitan bomberos?",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(15, 10))
        
        self.bomberos_var = ctk.StringVar(value="")
        
        ctk.CTkRadioButton(
            bomberos_frame, text="❌ No", variable=self.bomberos_var, value="no"
        ).grid(row=1, column=0, padx=25, pady=5, sticky="w")
        
        ctk.CTkRadioButton(
            bomberos_frame, text="🚒 SÍ", variable=self.bomberos_var, value="si"
        ).grid(row=2, column=0, padx=25, pady=(5, 15), sticky="w")
        
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
            fg_color=("green", "darkgreen")
        )
        save_btn.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        
        # Despachar patrulla
        dispatch_btn = ctk.CTkButton(
            buttons_frame,
            text="🚔 Despachar Patrulla",
            command=self.despachar_patrulla,
            fg_color=("red", "darkred")
        )
        dispatch_btn.grid(row=0, column=2, padx=20, pady=20, sticky="ew")
        
    def calcular_prioridad(self):
        """Calcula la prioridad basada en las respuestas del triaje"""
        try:
            prioridad = 4  # Prioridad baja por defecto
            
            # Factores críticos (prioridad 1)
            if (self.heridos_var.get() == "graves" or 
                self.agresor_presente_var.get() == "si" and self.agresor_armado_var.get() in ["arma_fuego", "arma_blanca"] or
                self.peligro_var.get() == "si"):
                prioridad = 1
                texto = "🔴 CRÍTICA - Despacho inmediato"
                color = "red"
                
            # Factores de alta prioridad (prioridad 2)
            elif (self.heridos_var.get() == "leves" or
                  self.agresor_presente_var.get() == "si" or
                  self.tipo_incidente_combo.get() in ["Robo/Hurto", "Violencia doméstica", "Accidente de tránsito"]):
                prioridad = 2
                texto = "🟠 ALTA - Despacho urgente"
                color = "orange"
                
            # Prioridad media (prioridad 3)
            elif (self.tipo_incidente_combo.get() in ["Disturbios/Peleas", "Vandalismo", "Persona sospechosa"] or
                  self.testigos_var.get() == "si"):
                prioridad = 3
                texto = "🟡 MEDIA - Despacho cuando esté disponible"
                color = "yellow"
                
            # Prioridad baja (prioridad 4)
            else:
                prioridad = 4
                texto = "🟢 BAJA - Seguimiento telefónico"
                color = "green"
            
            # Actualizar label
            self.prioridad_label.configure(text=texto, text_color=color)
            self.nivel_prioridad = prioridad
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculando prioridad: {e}")
    
    def validar_triaje(self):
        """Valida que se hayan completado los campos obligatorios"""
        if not self.tipo_incidente_combo.get():
            messagebox.showerror("Error", "Debe seleccionar el tipo de incidente")
            return False
            
        if not self.heridos_var.get():
            messagebox.showerror("Error", "Debe indicar si hay heridos")
            return False
            
        if not self.agresor_presente_var.get():
            messagebox.showerror("Error", "Debe indicar si el agresor está presente")
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
            
            # Insertar triaje seguridad
            self.app.db_manager.execute_query("""
                INSERT INTO triaje_seguridad (
                    llamada_id, tipo_incidente, hay_heridos, agresor_presente,
                    agresor_armado, vehiculos_involucrados, testigos_presentes,
                    necesidad_ambulancia, necesidad_bomberos, peligro_inmediato,
                    nivel_prioridad, observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.llamada_id,
                self.tipo_incidente_combo.get(),
                1 if self.heridos_var.get() in ["leves", "graves"] else 0,
                1 if self.agresor_presente_var.get() == "si" else 0,
                1 if self.agresor_armado_var.get() in ["arma_fuego", "arma_blanca"] else 0,
                self.vehiculos_text.get("1.0", "end-1c"),
                1 if self.testigos_var.get() == "si" else 0,
                1 if self.ambulancia_var.get() == "si" else 0,
                1 if self.bomberos_var.get() == "si" else 0,
                1 if self.peligro_var.get() == "si" else 0,
                self.nivel_prioridad,
                self.observaciones_text.get("1.0", "end-1c")
            ))
            
            messagebox.showinfo("Éxito", "Triaje de seguridad ciudadana guardado correctamente")
            
            # Callback al parent
            despachar = self.nivel_prioridad <= 3
            self.parent.triaje_completado(self.llamada_id, despachar)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando triaje: {e}")
    
    def despachar_patrulla(self):
        """Guarda el triaje y despacha patrulla"""
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
            
            messagebox.showinfo("Patrulla Despachada", 
                               f"Patrulla despachada para {self.tipo_incidente_combo.get()}.\n"
                               f"Prioridad: {self.nivel_prioridad}")
            
            # Callback al parent
            self.parent.triaje_completado(self.llamada_id, True)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error despachando patrulla: {e}")
    
    def guardar_triaje_silencioso(self):
        """Guarda el triaje sin mostrar mensajes"""
        self.app.db_manager.execute_query("""
            INSERT INTO triaje_seguridad (
                llamada_id, tipo_incidente, hay_heridos, agresor_presente,
                agresor_armado, vehiculos_involucrados, testigos_presentes,
                necesidad_ambulancia, necesidad_bomberos, peligro_inmediato,
                nivel_prioridad, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.llamada_id,
            self.tipo_incidente_combo.get(),
            1 if self.heridos_var.get() in ["leves", "graves"] else 0,
            1 if self.agresor_presente_var.get() == "si" else 0,
            1 if self.agresor_armado_var.get() in ["arma_fuego", "arma_blanca"] else 0,
            self.vehiculos_text.get("1.0", "end-1c"),
            1 if self.testigos_var.get() == "si" else 0,
            1 if self.ambulancia_var.get() == "si" else 0,
            1 if self.bomberos_var.get() == "si" else 0,
            1 if self.peligro_var.get() == "si" else 0,
            self.nivel_prioridad,
            self.observaciones_text.get("1.0", "end-1c")
        ))
    
    def cancelar(self):
        """Cancela el triaje"""
        if messagebox.askyesno("Cancelar", "¿Está seguro que desea cancelar el triaje?"):
            self.destroy()
