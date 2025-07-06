"""
Ventana Nueva Llamada - Sistema de Emergencias
Incluye triaje para todos los tipos de emergencia
"""

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import webbrowser
from datetime import datetime
import threading

from gui.triaje_medico_window import TriajeMedicoWindow
from gui.triaje_bomberos_window import TriajeBomberosWindow
from gui.triaje_defensa_civil_window import TriajeDefensaCivilWindow
from gui.triaje_seguridad_window import TriajeSeguridadWindow

class NuevaLlamadaWindow(ctk.CTkToplevel):
    def __init__(self, app, parent):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        self.vecino_id = None
        self.llamada_id = None
        
        self.setup_window()
        self.create_widgets()
        self.load_data()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Nueva Llamada de Emergencia")
        self.geometry("900x700")
        self.resizable(True, True)
        
        # Centrar ventana
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz"""
        
        # Scrollable frame principal
        main_scroll = ctk.CTkScrollableFrame(self)
        main_scroll.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            main_scroll,
            text="🚨 NUEVA LLAMADA DE EMERGENCIA",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="red"
        )
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Frame de datos del solicitante
        self.create_caller_section(main_scroll)
        
        # Frame de dirección
        self.create_address_section(main_scroll)
        
        # Frame de tipo de emergencia
        self.create_emergency_type_section(main_scroll)
        
        # Frame de botones
        self.create_buttons_section(main_scroll)
        
    def create_caller_section(self, parent):
        """Sección de datos del solicitante"""
        
        # Frame principal
        caller_frame = ctk.CTkFrame(parent)
        caller_frame.grid(row=1, column=0, padx=0, pady=(0, 20), sticky="ew")
        caller_frame.grid_columnconfigure((1, 3), weight=1)
        
        # Título de sección
        section_title = ctk.CTkLabel(
            caller_frame,
            text="👤 DATOS DEL SOLICITANTE",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_title.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 15))
        
        # DNI
        ctk.CTkLabel(caller_frame, text="DNI:").grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.dni_entry = ctk.CTkEntry(caller_frame, placeholder_text="12345678")
        self.dni_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.dni_entry.bind("<KeyRelease>", self.buscar_vecino_por_dni)
        
        # Teléfono
        ctk.CTkLabel(caller_frame, text="Teléfono:").grid(row=1, column=2, padx=(20, 10), pady=10, sticky="w")
        self.telefono_entry = ctk.CTkEntry(caller_frame, placeholder_text="3516789012")
        self.telefono_entry.grid(row=1, column=3, padx=(0, 20), pady=10, sticky="ew")
        self.telefono_entry.bind("<KeyRelease>", self.buscar_vecino_por_telefono)
        
        # Nombre
        ctk.CTkLabel(caller_frame, text="Nombre:").grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.nombre_entry = ctk.CTkEntry(caller_frame, placeholder_text="Juan")
        self.nombre_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Apellido
        ctk.CTkLabel(caller_frame, text="Apellido:").grid(row=2, column=2, padx=(20, 10), pady=10, sticky="w")
        self.apellido_entry = ctk.CTkEntry(caller_frame, placeholder_text="Pérez")
        self.apellido_entry.grid(row=2, column=3, padx=(0, 20), pady=10, sticky="ew")
        
        # Teléfono alternativo
        ctk.CTkLabel(caller_frame, text="Tel. Alternativo:").grid(row=3, column=0, padx=(20, 10), pady=10, sticky="w")
        self.telefono_alt_entry = ctk.CTkEntry(caller_frame, placeholder_text="Opcional")
        self.telefono_alt_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Botón guardar vecino
        self.save_caller_btn = ctk.CTkButton(
            caller_frame,
            text="💾 Guardar Datos",
            command=self.guardar_datos_vecino,
            width=150
        )
        self.save_caller_btn.grid(row=3, column=3, padx=(0, 20), pady=10)
        
    def create_address_section(self, parent):
        """Sección de dirección"""
        
        address_frame = ctk.CTkFrame(parent)
        address_frame.grid(row=2, column=0, padx=0, pady=(0, 20), sticky="ew")
        address_frame.grid_columnconfigure((1, 3), weight=1)
        
        # Título
        section_title = ctk.CTkLabel(
            address_frame,
            text="📍 DIRECCIÓN DE LA EMERGENCIA",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_title.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 15))
        
        # Dirección
        ctk.CTkLabel(address_frame, text="Dirección:").grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.direccion_entry = ctk.CTkEntry(address_frame, placeholder_text="Calle y altura")
        self.direccion_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Número
        ctk.CTkLabel(address_frame, text="Número:").grid(row=1, column=2, padx=(20, 10), pady=10, sticky="w")
        self.numero_entry = ctk.CTkEntry(address_frame, placeholder_text="1234", width=100)
        self.numero_entry.grid(row=1, column=3, padx=(0, 20), pady=10, sticky="w")
        
        # Piso y Departamento
        ctk.CTkLabel(address_frame, text="Piso:").grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        self.piso_entry = ctk.CTkEntry(address_frame, placeholder_text="Opcional", width=100)
        self.piso_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="w")
        
        ctk.CTkLabel(address_frame, text="Depto:").grid(row=2, column=2, padx=(20, 10), pady=10, sticky="w")
        self.depto_entry = ctk.CTkEntry(address_frame, placeholder_text="A", width=100)
        self.depto_entry.grid(row=2, column=3, padx=(0, 20), pady=10, sticky="w")
        
        # Barrio
        ctk.CTkLabel(address_frame, text="Barrio:").grid(row=3, column=0, padx=(20, 10), pady=10, sticky="w")
        self.barrio_combo = ctk.CTkComboBox(address_frame, values=[], state="readonly")
        self.barrio_combo.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Botón ubicar en mapa
        self.map_btn = ctk.CTkButton(
            address_frame,
            text="🗺️ Ubicar en Mapa",
            command=self.ubicar_en_mapa,
            width=150
        )
        self.map_btn.grid(row=3, column=3, padx=(0, 20), pady=10)
        
    def create_emergency_type_section(self, parent):
        """Sección de tipo de emergencia"""
        
        emergency_frame = ctk.CTkFrame(parent)
        emergency_frame.grid(row=3, column=0, padx=0, pady=(0, 20), sticky="ew")
        emergency_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        section_title = ctk.CTkLabel(
            emergency_frame,
            text="🚨 TIPO DE EMERGENCIA",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_title.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Descripción inicial
        ctk.CTkLabel(emergency_frame, text="Descripción inicial:").grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        self.descripcion_text = ctk.CTkTextbox(emergency_frame, height=80)
        self.descripcion_text.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        # Botones de tipo de emergencia
        buttons_frame = ctk.CTkFrame(emergency_frame)
        buttons_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        # Botones para cada tipo
        self.emergency_buttons = {}
        
        # Emergencia médica
        self.emergency_buttons['medica'] = ctk.CTkButton(
            buttons_frame,
            text="🚑\nEMERGENCIA\nMÉDICA",
            command=lambda: self.iniciar_triaje('MEDICA'),
            height=80,
            fg_color=("red", "darkred"),
            hover_color=("darkred", "red")
        )
        self.emergency_buttons['medica'].grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        # Bomberos
        self.emergency_buttons['bomberos'] = ctk.CTkButton(
            buttons_frame,
            text="🚒\nBOMBEROS",
            command=lambda: self.iniciar_triaje('BOMBEROS'),
            height=80,
            fg_color=("orange", "darkorange"),
            hover_color=("darkorange", "orange")
        )
        self.emergency_buttons['bomberos'].grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        # Defensa Civil
        self.emergency_buttons['defensa_civil'] = ctk.CTkButton(
            buttons_frame,
            text="🏗️\nDEFENSA\nCIVIL",
            command=lambda: self.iniciar_triaje('DEFENSA_CIVIL'),
            height=80,
            fg_color=("blue", "darkblue"),
            hover_color=("darkblue", "blue")
        )
        self.emergency_buttons['defensa_civil'].grid(row=0, column=2, padx=5, pady=10, sticky="ew")
        
        # Seguridad Ciudadana
        self.emergency_buttons['seguridad'] = ctk.CTkButton(
            buttons_frame,
            text="👮\nSEGURIDAD\nCIUDADANA",
            command=lambda: self.iniciar_triaje('SEGURIDAD'),
            height=80,
            fg_color=("green", "darkgreen"),
            hover_color=("darkgreen", "green")
        )
        self.emergency_buttons['seguridad'].grid(row=0, column=3, padx=5, pady=10, sticky="ew")
        
        # Llamada General
        self.emergency_buttons['general'] = ctk.CTkButton(
            buttons_frame,
            text="📞\nLLAMADA\nGENERAL",
            command=lambda: self.iniciar_triaje('GENERAL'),
            height=80,
            fg_color=("gray", "darkgray"),
            hover_color=("darkgray", "gray")
        )
        self.emergency_buttons['general'].grid(row=0, column=4, padx=5, pady=10, sticky="ew")
        
    def create_buttons_section(self, parent):
        """Sección de botones de acción"""
        
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.grid(row=4, column=0, padx=0, pady=(0, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=self.cancelar,
            fg_color=("gray", "darkgray"),
            hover_color=("darkgray", "gray")
        )
        cancel_btn.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Guardar sin triaje (para llamadas generales)
        self.save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            command=self.guardar_llamada_simple,
            state="disabled"
        )
        self.save_btn.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        
        # Limpiar formulario
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Limpiar",
            command=self.limpiar_formulario,
            fg_color=("orange", "darkorange"),
            hover_color=("darkorange", "orange")
        )
        clear_btn.grid(row=0, column=2, padx=20, pady=20, sticky="ew")
        
    def load_data(self):
        """Carga datos iniciales"""
        try:
            # Cargar barrios
            barrios = self.app.db_manager.fetch_all("""
                SELECT nombre FROM barrios WHERE activo = 1 ORDER BY nombre
            """)
            barrio_values = [barrio[0] for barrio in barrios]
            self.barrio_combo.configure(values=barrio_values)
            
            # Focus inicial
            self.telefono_entry.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando datos: {e}")
    
    def buscar_vecino_por_dni(self, event=None):
        """Busca vecino por DNI"""
        dni = self.dni_entry.get().strip()
        if len(dni) >= 7:  # DNI mínimo
            self._buscar_vecino('dni', dni)
    
    def buscar_vecino_por_telefono(self, event=None):
        """Busca vecino por teléfono"""
        telefono = self.telefono_entry.get().strip()
        if len(telefono) >= 8:  # Teléfono mínimo
            self._buscar_vecino('telefono', telefono)
    
    def _buscar_vecino(self, campo, valor):
        """Busca vecino en la base de datos"""
        try:
            if campo == 'dni':
                vecino = self.app.db_manager.fetch_one("""
                    SELECT v.*, b.nombre as barrio_nombre
                    FROM vecinos v
                    LEFT JOIN barrios b ON v.barrio_id = b.id
                    WHERE v.dni = ?
                """, (valor,))
            else:  # telefono
                vecino = self.app.db_manager.fetch_one("""
                    SELECT v.*, b.nombre as barrio_nombre
                    FROM vecinos v
                    LEFT JOIN barrios b ON v.barrio_id = b.id
                    WHERE v.telefono = ? OR v.telefono_alternativo = ?
                """, (valor, valor))
            
            if vecino:
                self.llenar_datos_vecino(vecino)
                self.vecino_id = vecino[0]  # ID del vecino
            
        except Exception as e:
            print(f"Error buscando vecino: {e}")
    
    def llenar_datos_vecino(self, vecino):
        """Llena los campos con datos del vecino encontrado"""
        self.dni_entry.delete(0, 'end')
        self.dni_entry.insert(0, vecino[1] or "")  # dni
        
        self.nombre_entry.delete(0, 'end')
        self.nombre_entry.insert(0, vecino[2] or "")  # nombre
        
        self.apellido_entry.delete(0, 'end')
        self.apellido_entry.insert(0, vecino[3] or "")  # apellido
        
        self.telefono_entry.delete(0, 'end')
        self.telefono_entry.insert(0, vecino[4] or "")  # telefono
        
        self.telefono_alt_entry.delete(0, 'end')
        self.telefono_alt_entry.insert(0, vecino[5] or "")  # telefono_alternativo
        
        self.direccion_entry.delete(0, 'end')
        self.direccion_entry.insert(0, vecino[6] or "")  # direccion
        
        self.numero_entry.delete(0, 'end')
        self.numero_entry.insert(0, vecino[7] or "")  # numero
        
        self.piso_entry.delete(0, 'end')
        self.piso_entry.insert(0, vecino[8] or "")  # piso
        
        self.depto_entry.delete(0, 'end')
        self.depto_entry.insert(0, vecino[9] or "")  # departamento
        
        # Barrio
        if vecino[14]:  # barrio_nombre
            self.barrio_combo.set(vecino[14])
    
    def guardar_datos_vecino(self):
        """Guarda o actualiza datos del vecino"""
        try:
            # Validaciones básicas
            if not self.telefono_entry.get().strip():
                messagebox.showerror("Error", "El teléfono es obligatorio")
                return
            
            if not self.nombre_entry.get().strip():
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            if not self.apellido_entry.get().strip():
                messagebox.showerror("Error", "El apellido es obligatorio")
                return
            
            # Obtener barrio_id
            barrio_id = None
            if self.barrio_combo.get():
                barrio = self.app.db_manager.fetch_one("""
                    SELECT id FROM barrios WHERE nombre = ?
                """, (self.barrio_combo.get(),))
                if barrio:
                    barrio_id = barrio[0]
            
            # Datos del vecino
            datos_vecino = (
                self.dni_entry.get().strip() or None,
                self.nombre_entry.get().strip(),
                self.apellido_entry.get().strip(),
                self.telefono_entry.get().strip(),
                self.telefono_alt_entry.get().strip() or None,
                self.direccion_entry.get().strip(),
                self.numero_entry.get().strip() or None,
                self.piso_entry.get().strip() or None,
                self.depto_entry.get().strip() or None,
                barrio_id
            )
            
            if self.vecino_id:
                # Actualizar vecino existente
                self.app.db_manager.execute_query("""
                    UPDATE vecinos SET 
                    dni = ?, nombre = ?, apellido = ?, telefono = ?, 
                    telefono_alternativo = ?, direccion = ?, numero = ?, 
                    piso = ?, departamento = ?, barrio_id = ?
                    WHERE id = ?
                """, datos_vecino + (self.vecino_id,))
            else:
                # Crear nuevo vecino
                self.app.db_manager.execute_query("""
                    INSERT INTO vecinos (dni, nombre, apellido, telefono, 
                    telefono_alternativo, direccion, numero, piso, 
                    departamento, barrio_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, datos_vecino)
                
                self.vecino_id = self.app.db_manager.get_last_insert_id()
            
            messagebox.showinfo("Éxito", "Datos del vecino guardados correctamente")
            self.save_btn.configure(state="normal")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando datos del vecino: {e}")
    
    def ubicar_en_mapa(self):
        """Abre Google Maps con la dirección"""
        try:
            direccion = self.direccion_entry.get().strip()
            numero = self.numero_entry.get().strip()
            barrio = self.barrio_combo.get()
            
            if not direccion:
                messagebox.showwarning("Advertencia", "Debe ingresar una dirección")
                return
            
            # Construir dirección completa
            direccion_completa = direccion
            if numero:
                direccion_completa += f" {numero}"
            if barrio:
                direccion_completa += f", {barrio}"
            direccion_completa += ", Villa Allende, Córdoba, Argentina"
            
            # URL de Google Maps
            url = f"https://www.google.com/maps/search/{direccion_completa.replace(' ', '+')}"
            webbrowser.open(url)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo mapa: {e}")
    
    def iniciar_triaje(self, tipo_emergencia):
        """Inicia el proceso de triaje según el tipo de emergencia"""
        try:
            # Validar datos mínimos
            if not self.telefono_entry.get().strip():
                messagebox.showerror("Error", "Debe ingresar al menos un teléfono")
                return
            
            if not self.direccion_entry.get().strip():
                messagebox.showerror("Error", "Debe ingresar la dirección de la emergencia")
                return
            
            # Guardar datos del vecino si no está guardado
            if not self.vecino_id:
                self.guardar_datos_vecino()
                if not self.vecino_id:
                    return
            
            # Crear llamada base
            llamada_id = self.crear_llamada_base(tipo_emergencia)
            if not llamada_id:
                return
            
            self.llamada_id = llamada_id
            
            # Abrir ventana de triaje correspondiente
            if tipo_emergencia == 'MEDICA':
                TriajeMedicoWindow(self.app, self, llamada_id)
            elif tipo_emergencia == 'BOMBEROS':
                TriajeBomberosWindow(self.app, self, llamada_id)
            elif tipo_emergencia == 'DEFENSA_CIVIL':
                TriajeDefensaCivilWindow(self.app, self, llamada_id)
            elif tipo_emergencia == 'SEGURIDAD':
                TriajeSeguridadWindow(self.app, self, llamada_id)
            elif tipo_emergencia == 'GENERAL':
                # Para llamadas generales, no hay triaje
                self.finalizar_llamada_general(llamada_id)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error iniciando triaje: {e}")
    
    def crear_llamada_base(self, tipo_emergencia):
        """Crea la llamada base en la base de datos"""
        try:
            # Generar número de llamada único
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            numero_llamada = f"EM{timestamp}"
            
            # Obtener tipo_emergencia_id
            tipo_em = self.app.db_manager.fetch_one("""
                SELECT id FROM tipos_emergencia WHERE codigo = ?
            """, (tipo_emergencia,))
            
            if not tipo_em:
                messagebox.showerror("Error", "Tipo de emergencia no encontrado")
                return None
            
            # Construir dirección completa
            direccion_completa = self.direccion_entry.get().strip()
            if self.numero_entry.get().strip():
                direccion_completa += f" {self.numero_entry.get().strip()}"
            if self.piso_entry.get().strip():
                direccion_completa += f", Piso {self.piso_entry.get().strip()}"
            if self.depto_entry.get().strip():
                direccion_completa += f", Depto {self.depto_entry.get().strip()}"
            if self.barrio_combo.get():
                direccion_completa += f", {self.barrio_combo.get()}"
            
            # Insertar llamada
            self.app.db_manager.execute_query("""
                INSERT INTO llamadas (
                    numero_llamada, vecino_id, tipo_emergencia_id, usuario_id,
                    direccion_completa, descripcion_inicial, estado
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                numero_llamada,
                self.vecino_id,
                tipo_em[0],
                self.app.current_user['id'],
                direccion_completa,
                self.descripcion_text.get("1.0", "end-1c"),
                'activa'
            ))
            
            return self.app.db_manager.get_last_insert_id()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creando llamada: {e}")
            return None
    
    def finalizar_llamada_general(self, llamada_id):
        """Finaliza una llamada general sin triaje"""
        try:
            # Actualizar estado
            self.app.db_manager.execute_query("""
                UPDATE llamadas SET estado = 'finalizada', fecha_cierre = ?
                WHERE id = ?
            """, (datetime.now(), llamada_id))
            
            messagebox.showinfo("Éxito", "Llamada general registrada correctamente")
            self.cerrar_ventana()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error finalizando llamada: {e}")
    
    def guardar_llamada_simple(self):
        """Guarda una llamada simple sin triaje"""
        try:
            if not self.vecino_id:
                messagebox.showerror("Error", "Debe guardar los datos del vecino primero")
                return
            
            llamada_id = self.crear_llamada_base('GENERAL')
            if llamada_id:
                self.finalizar_llamada_general(llamada_id)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando llamada: {e}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea limpiar todos los campos?"):
            # Limpiar campos de vecino
            self.dni_entry.delete(0, 'end')
            self.telefono_entry.delete(0, 'end')
            self.nombre_entry.delete(0, 'end')
            self.apellido_entry.delete(0, 'end')
            self.telefono_alt_entry.delete(0, 'end')
            
            # Limpiar campos de dirección
            self.direccion_entry.delete(0, 'end')
            self.numero_entry.delete(0, 'end')
            self.piso_entry.delete(0, 'end')
            self.depto_entry.delete(0, 'end')
            self.barrio_combo.set("")
            
            # Limpiar descripción
            self.descripcion_text.delete("1.0", "end")
            
            # Reset variables
            self.vecino_id = None
            self.llamada_id = None
            self.save_btn.configure(state="disabled")
            
            # Focus inicial
            self.telefono_entry.focus()
    
    def cancelar(self):
        """Cancela la creación de la llamada"""
        if messagebox.askyesno("Cancelar", "¿Está seguro que desea cancelar? Se perderán todos los datos."):
            self.cerrar_ventana()
    
    def cerrar_ventana(self):
        """Cierra la ventana y actualiza el parent"""
        self.parent.refresh_calls_list()  # Actualizar lista en ventana principal
        self.destroy()
    
    def triaje_completado(self, llamada_id, despachar_movil=False):
        """Callback cuando se completa un triaje"""
        try:
            if despachar_movil:
                # Aquí se podría abrir ventana de despacho de móvil
                messagebox.showinfo("Triaje Completado", "Triaje completado. Proceda a despachar móvil.")
            else:
                messagebox.showinfo("Triaje Completado", "Triaje completado. Llamada registrada.")
            
            # Enviar alerta por WhatsApp si corresponde
            threading.Thread(target=self.enviar_alerta_whatsapp, args=(llamada_id,), daemon=True).start()
            
            self.cerrar_ventana()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error completando triaje: {e}")
    
    def enviar_alerta_whatsapp(self, llamada_id):
        """Envía alerta por WhatsApp"""
        try:
            from utils.whatsapp_manager import WhatsAppManager
            wa_manager = WhatsAppManager()
            wa_manager.enviar_alerta_emergencia(llamada_id)
            
        except Exception as e:
            print(f"Error enviando WhatsApp: {e}")
