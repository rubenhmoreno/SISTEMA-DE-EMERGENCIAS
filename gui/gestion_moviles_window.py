"""
Ventana de Gestión de Móviles - Sistema de Emergencias
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from datetime import datetime

class GestionMovilesWindow(ctk.CTkToplevel):
    def __init__(self, app, parent):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        self.selected_movil_id = None
        
        self.setup_window()
        self.create_widgets()
        self.load_data()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Gestión de Móviles")
        self.geometry("1000x700")
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz"""
        
        # Panel izquierdo - Lista de móviles
        self.create_left_panel()
        
        # Panel derecho - Detalles y formulario
        self.create_right_panel()
        
    def create_left_panel(self):
        """Crea el panel izquierdo con la lista de móviles"""
        
        left_frame = ctk.CTkFrame(self, width=400)
        left_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_propagate(False)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            left_frame,
            text="🚗 MÓVILES REGISTRADOS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Treeview para móviles
        self.create_moviles_treeview(left_frame)
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(left_frame)
        buttons_frame.grid(row=2, column=0, padx=20, pady=(15, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Nuevo móvil
        new_btn = ctk.CTkButton(
            buttons_frame,
            text="➕ Nuevo",
            command=self.nuevo_movil,
            fg_color=("green", "darkgreen")
        )
        new_btn.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        # Editar móvil
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Editar",
            command=self.editar_movil,
            fg_color=("blue", "darkblue")
        )
        edit_btn.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        # Eliminar móvil
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Eliminar",
            command=self.eliminar_movil,
            fg_color=("red", "darkred")
        )
        delete_btn.grid(row=0, column=2, padx=5, pady=10, sticky="ew")
        
    def create_moviles_treeview(self, parent):
        """Crea el treeview para mostrar móviles"""
        
        # Frame para el treeview
        tree_frame = tk.Frame(parent)
        tree_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Treeview
        columns = ('Número', 'Tipo', 'Estado', 'Patente')
        self.moviles_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.moviles_tree.heading('Número', text='Número')
        self.moviles_tree.heading('Tipo', text='Tipo')
        self.moviles_tree.heading('Estado', text='Estado')
        self.moviles_tree.heading('Patente', text='Patente')
        
        self.moviles_tree.column('Número', width=80)
        self.moviles_tree.column('Tipo', width=100)
        self.moviles_tree.column('Estado', width=100)
        self.moviles_tree.column('Patente', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.moviles_tree.yview)
        self.moviles_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.moviles_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Binding para selección
        self.moviles_tree.bind('<<TreeviewSelect>>', self.on_movil_select)
        
    def create_right_panel(self):
        """Crea el panel derecho con detalles y formulario"""
        
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame
        main_scroll = ctk.CTkScrollableFrame(right_frame)
        main_scroll.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_scroll.grid_columnconfigure(1, weight=1)
        
        # Título
        self.form_title = ctk.CTkLabel(
            main_scroll,
            text="📝 DATOS DEL MÓVIL",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Formulario
        self.create_form(main_scroll)
        
        # Personal asignado
        self.create_personal_section(main_scroll)
        
        # Botones de acción
        self.create_form_buttons(main_scroll)
        
    def create_form(self, parent):
        """Crea el formulario de datos del móvil"""
        
        # Número del móvil
        ctk.CTkLabel(parent, text="Número:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        self.numero_entry = ctk.CTkEntry(parent, placeholder_text="M001")
        self.numero_entry.grid(row=1, column=1, pady=10, sticky="ew")
        
        # Tipo de móvil
        ctk.CTkLabel(parent, text="Tipo:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(0, 10), pady=10, sticky="w")
        self.tipo_combo = ctk.CTkComboBox(
            parent,
            values=["ambulancia", "patrulla", "rescate"],
            state="readonly"
        )
        self.tipo_combo.grid(row=2, column=1, pady=10, sticky="ew")
        
        # Patente
        ctk.CTkLabel(parent, text="Patente:", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=(0, 10), pady=10, sticky="w")
        self.patente_entry = ctk.CTkEntry(parent, placeholder_text="ABC123")
        self.patente_entry.grid(row=3, column=1, pady=10, sticky="ew")
        
        # Modelo
        ctk.CTkLabel(parent, text="Modelo:", font=ctk.CTkFont(weight="bold")).grid(
            row=4, column=0, padx=(0, 10), pady=10, sticky="w")
        self.modelo_entry = ctk.CTkEntry(parent, placeholder_text="Ford Transit")
        self.modelo_entry.grid(row=4, column=1, pady=10, sticky="ew")
        
        # Año
        ctk.CTkLabel(parent, text="Año:", font=ctk.CTkFont(weight="bold")).grid(
            row=5, column=0, padx=(0, 10), pady=10, sticky="w")
        self.año_entry = ctk.CTkEntry(parent, placeholder_text="2020")
        self.año_entry.grid(row=5, column=1, pady=10, sticky="ew")
        
        # Estado
        ctk.CTkLabel(parent, text="Estado:", font=ctk.CTkFont(weight="bold")).grid(
            row=6, column=0, padx=(0, 10), pady=10, sticky="w")
        self.estado_combo = ctk.CTkComboBox(
            parent,
            values=["disponible", "ocupado", "fuera_servicio", "mantenimiento"],
            state="readonly"
        )
        self.estado_combo.grid(row=6, column=1, pady=10, sticky="ew")
        
        # Ubicación actual
        ctk.CTkLabel(parent, text="Ubicación:", font=ctk.CTkFont(weight="bold")).grid(
            row=7, column=0, padx=(0, 10), pady=10, sticky="w")
        self.ubicacion_entry = ctk.CTkEntry(parent, placeholder_text="Base Central")
        self.ubicacion_entry.grid(row=7, column=1, pady=10, sticky="ew")
        
        # Observaciones
        ctk.CTkLabel(parent, text="Observaciones:", font=ctk.CTkFont(weight="bold")).grid(
            row=8, column=0, padx=(0, 10), pady=(10, 5), sticky="nw")
        self.observaciones_text = ctk.CTkTextbox(parent, height=80)
        self.observaciones_text.grid(row=8, column=1, pady=(10, 20), sticky="ew")
        
    def create_personal_section(self, parent):
        """Crea la sección de personal asignado"""
        
        # Separador
        separator = ctk.CTkFrame(parent, height=2)
        separator.grid(row=9, column=0, columnspan=2, padx=0, pady=10, sticky="ew")
        
        # Título personal
        personal_title = ctk.CTkLabel(
            parent,
            text="👥 PERSONAL ASIGNADO",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        personal_title.grid(row=10, column=0, columnspan=2, pady=(10, 15))
        
        # Frame para lista de personal
        personal_frame = ctk.CTkFrame(parent)
        personal_frame.grid(row=11, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        personal_frame.grid_columnconfigure(0, weight=1)
        
        # Lista de personal asignado
        self.personal_listbox = tk.Listbox(personal_frame, height=6)
        self.personal_listbox.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        
        # Botones de personal
        personal_buttons = ctk.CTkFrame(parent)
        personal_buttons.grid(row=12, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        personal_buttons.grid_columnconfigure((0, 1), weight=1)
        
        add_personal_btn = ctk.CTkButton(
            personal_buttons,
            text="➕ Asignar Personal",
            command=self.asignar_personal,
            fg_color=("green", "darkgreen")
        )
        add_personal_btn.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="ew")
        
        remove_personal_btn = ctk.CTkButton(
            personal_buttons,
            text="➖ Quitar Personal",
            command=self.quitar_personal,
            fg_color=("red", "darkred")
        )
        remove_personal_btn.grid(row=0, column=1, padx=(5, 0), pady=10, sticky="ew")
        
    def create_form_buttons(self, parent):
        """Crea los botones del formulario"""
        
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.grid(row=13, column=0, columnspan=2, pady=20, sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Guardar
        self.save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            command=self.guardar_movil,
            fg_color=("green", "darkgreen")
        )
        self.save_btn.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        
        # Limpiar
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Limpiar",
            command=self.limpiar_formulario,
            fg_color=("orange", "darkorange")
        )
        clear_btn.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        
        # Cerrar
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cerrar",
            command=self.destroy,
            fg_color=("gray", "darkgray")
        )
        close_btn.grid(row=0, column=2, padx=10, pady=15, sticky="ew")
        
    def load_data(self):
        """Carga los datos iniciales"""
        self.refresh_moviles_list()
        
    def refresh_moviles_list(self):
        """Actualiza la lista de móviles"""
        try:
            # Limpiar treeview
            for item in self.moviles_tree.get_children():
                self.moviles_tree.delete(item)
            
            # Obtener móviles
            moviles = self.app.db_manager.fetch_all("""
                SELECT id, numero, tipo, estado, patente, activo
                FROM moviles
                ORDER BY numero
            """)
            
            # Llenar treeview
            for movil in moviles:
                if movil[5]:  # activo
                    # Determinar color según estado
                    estado = movil[3]
                    if estado == 'disponible':
                        estado_icon = "✅"
                    elif estado == 'ocupado':
                        estado_icon = "🚨"
                    elif estado == 'fuera_servicio':
                        estado_icon = "❌"
                    else:  # mantenimiento
                        estado_icon = "🔧"
                    
                    self.moviles_tree.insert('', 'end', values=(
                        movil[1],  # número
                        movil[2].title(),  # tipo
                        f"{estado_icon} {movil[3].replace('_', ' ').title()}",  # estado
                        movil[4] or "Sin patente"  # patente
                    ), tags=(movil[0],))  # ID como tag
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando móviles: {e}")
    
    def on_movil_select(self, event):
        """Maneja la selección de un móvil"""
        selection = self.moviles_tree.selection()
        if selection:
            # Obtener ID del móvil
            item = self.moviles_tree.item(selection[0])
            self.selected_movil_id = item['tags'][0]
            
            # Cargar datos del móvil
            self.load_movil_data(self.selected_movil_id)
    
    def load_movil_data(self, movil_id):
        """Carga los datos de un móvil específico"""
        try:
            # Obtener datos del móvil
            movil = self.app.db_manager.fetch_one("""
                SELECT numero, tipo, patente, modelo, año, estado, 
                       ubicacion_actual, observaciones
                FROM moviles WHERE id = ?
            """, (movil_id,))
            
            if movil:
                # Llenar formulario
                self.numero_entry.delete(0, 'end')
                self.numero_entry.insert(0, movil[0] or "")
                
                self.tipo_combo.set(movil[1] or "ambulancia")
                
                self.patente_entry.delete(0, 'end')
                self.patente_entry.insert(0, movil[2] or "")
                
                self.modelo_entry.delete(0, 'end')
                self.modelo_entry.insert(0, movil[3] or "")
                
                self.año_entry.delete(0, 'end')
                self.año_entry.insert(0, str(movil[4]) if movil[4] else "")
                
                self.estado_combo.set(movil[5] or "disponible")
                
                self.ubicacion_entry.delete(0, 'end')
                self.ubicacion_entry.insert(0, movil[6] or "")
                
                self.observaciones_text.delete("1.0", "end")
                self.observaciones_text.insert("1.0", movil[7] or "")
                
                # Cargar personal asignado
                self.load_personal_asignado(movil_id)
                
                # Cambiar título
                self.form_title.configure(text=f"📝 MÓVIL {movil[0]}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando datos del móvil: {e}")
    
    def load_personal_asignado(self, movil_id):
        """Carga el personal asignado al móvil"""
        try:
            # Limpiar listbox
            self.personal_listbox.delete(0, 'end')
            
            # Obtener personal asignado
            personal = self.app.db_manager.fetch_all("""
                SELECT p.nombre, p.apellido, p.cargo, ap.fecha_asignacion
                FROM asignaciones_personal ap
                JOIN personal p ON ap.personal_id = p.id
                WHERE ap.movil_id = ? AND ap.activo = 1
                ORDER BY ap.fecha_asignacion
            """, (movil_id,))
            
            # Llenar listbox
            for persona in personal:
                fecha_asig = datetime.strptime(persona[3], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
                item_text = f"{persona[0]} {persona[1]} - {persona[2]} (desde {fecha_asig})"
                self.personal_listbox.insert('end', item_text)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando personal: {e}")
    
    def nuevo_movil(self):
        """Prepara el formulario para un nuevo móvil"""
        self.selected_movil_id = None
        self.limpiar_formulario()
        self.form_title.configure(text="📝 NUEVO MÓVIL")
        self.numero_entry.focus()
        
    def editar_movil(self):
        """Edita el móvil seleccionado"""
        if not self.selected_movil_id:
            messagebox.showwarning("Advertencia", "Debe seleccionar un móvil para editar")
            return
        # Los datos ya están cargados por la selección
        self.numero_entry.focus()
        
    def eliminar_movil(self):
        """Elimina el móvil seleccionado"""
        if not self.selected_movil_id:
            messagebox.showwarning("Advertencia", "Debe seleccionar un móvil para eliminar")
            return
        
        # Obtener número del móvil para confirmación
        movil = self.app.db_manager.fetch_one("""
            SELECT numero FROM moviles WHERE id = ?
        """, (self.selected_movil_id,))
        
        if not movil:
            messagebox.showerror("Error", "Móvil no encontrado")
            return
        
        # Confirmación
        if messagebox.askyesno("Confirmar Eliminación", 
                             f"¿Está seguro que desea eliminar el móvil {movil[0]}?\n"
                             "Esta acción marcará el móvil como inactivo."):
            try:
                # Marcar como inactivo (no eliminar físicamente)
                self.app.db_manager.execute_query("""
                    UPDATE moviles SET activo = 0 WHERE id = ?
                """, (self.selected_movil_id,))
                
                # Desasignar personal activo
                self.app.db_manager.execute_query("""
                    UPDATE asignaciones_personal 
                    SET activo = 0, fecha_desasignacion = ?
                    WHERE movil_id = ? AND activo = 1
                """, (datetime.now(), self.selected_movil_id))
                
                messagebox.showinfo("Éxito", "Móvil eliminado correctamente")
                
                # Actualizar lista y limpiar formulario
                self.refresh_moviles_list()
                self.limpiar_formulario()
                self.selected_movil_id = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Error eliminando móvil: {e}")
    
    def guardar_movil(self):
        """Guarda los datos del móvil"""
        try:
            # Validaciones
            if not self.numero_entry.get().strip():
                messagebox.showerror("Error", "El número del móvil es obligatorio")
                return
            
            if not self.tipo_combo.get():
                messagebox.showerror("Error", "Debe seleccionar el tipo de móvil")
                return
            
            # Datos del móvil
            datos = (
                self.numero_entry.get().strip(),
                self.tipo_combo.get(),
                self.patente_entry.get().strip() or None,
                self.modelo_entry.get().strip() or None,
                int(self.año_entry.get()) if self.año_entry.get().strip().isdigit() else None,
                self.estado_combo.get() or "disponible",
                self.ubicacion_entry.get().strip() or None,
                self.observaciones_text.get("1.0", "end-1c").strip() or None
            )
            
            if self.selected_movil_id:
                # Actualizar móvil existente
                self.app.db_manager.execute_query("""
                    UPDATE moviles SET 
                    numero = ?, tipo = ?, patente = ?, modelo = ?, año = ?,
                    estado = ?, ubicacion_actual = ?, observaciones = ?
                    WHERE id = ?
                """, datos + (self.selected_movil_id,))
                
                messagebox.showinfo("Éxito", "Móvil actualizado correctamente")
            else:
                # Verificar que no exista el número
                existe = self.app.db_manager.fetch_one("""
                    SELECT id FROM moviles WHERE numero = ? AND activo = 1
                """, (datos[0],))
                
                if existe:
                    messagebox.showerror("Error", "Ya existe un móvil con ese número")
                    return
                
                # Crear nuevo móvil
                self.app.db_manager.execute_query("""
                    INSERT INTO moviles (numero, tipo, patente, modelo, año,
                                       estado, ubicacion_actual, observaciones, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                """, datos)
                
                self.selected_movil_id = self.app.db_manager.get_last_insert_id()
                messagebox.showinfo("Éxito", "Móvil creado correctamente")
            
            # Actualizar lista
            self.refresh_moviles_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando móvil: {e}")
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.numero_entry.delete(0, 'end')
        self.tipo_combo.set("")
        self.patente_entry.delete(0, 'end')
        self.modelo_entry.delete(0, 'end')
        self.año_entry.delete(0, 'end')
        self.estado_combo.set("")
        self.ubicacion_entry.delete(0, 'end')
        self.observaciones_text.delete("1.0", "end")
        self.personal_listbox.delete(0, 'end')
        self.form_title.configure(text="📝 DATOS DEL MÓVIL")
    
    def asignar_personal(self):
        """Abre ventana para asignar personal al móvil"""
        if not self.selected_movil_id:
            messagebox.showwarning("Advertencia", "Debe seleccionar un móvil primero")
            return
        
        AsignarPersonalWindow(self.app, self, self.selected_movil_id)
    
    def quitar_personal(self):
        """Quita personal del móvil"""
        if not self.selected_movil_id:
            messagebox.showwarning("Advertencia", "Debe seleccionar un móvil primero")
            return
        
        selection = self.personal_listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Debe seleccionar una persona para quitar")
            return
        
        # Obtener el personal seleccionado
        persona_text = self.personal_listbox.get(selection[0])
        nombre_completo = persona_text.split(" - ")[0]
        
        if messagebox.askyesno("Confirmar", f"¿Quitar a {nombre_completo} del móvil?"):
            try:
                # Buscar la asignación activa
                partes_nombre = nombre_completo.split()
                nombre = partes_nombre[0]
                apellido = " ".join(partes_nombre[1:])
                
                personal = self.app.db_manager.fetch_one("""
                    SELECT id FROM personal WHERE nombre = ? AND apellido = ?
                """, (nombre, apellido))
                
                if personal:
                    # Desasignar
                    self.app.db_manager.execute_query("""
                        UPDATE asignaciones_personal 
                        SET activo = 0, fecha_desasignacion = ?
                        WHERE movil_id = ? AND personal_id = ? AND activo = 1
                    """, (datetime.now(), self.selected_movil_id, personal[0]))
                    
                    messagebox.showinfo("Éxito", "Personal removido del móvil")
                    self.load_personal_asignado(self.selected_movil_id)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error quitando personal: {e}")


class AsignarPersonalWindow(ctk.CTkToplevel):
    """Ventana para asignar personal a un móvil"""
    
    def __init__(self, app, parent, movil_id):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        self.movil_id = movil_id
        
        self.setup_window()
        self.create_widgets()
        self.load_data()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Asignar Personal al Móvil")
        self.geometry("500x400")
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz"""
        
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="👥 ASIGNAR PERSONAL",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Lista de personal disponible
        personal_frame = ctk.CTkFrame(self)
        personal_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew")
        personal_frame.grid_columnconfigure(0, weight=1)
        personal_frame.grid_rowconfigure(0, weight=1)
        
        self.personal_listbox = tk.Listbox(personal_frame, selectmode='multiple')
        self.personal_listbox.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        # Scrollbar
        scrollbar = tk.Scrollbar(personal_frame, orient="vertical", command=self.personal_listbox.yview)
        self.personal_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 15), pady=15)
        
        # Botones
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        asignar_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ Asignar",
            command=self.asignar_personal,
            fg_color=("green", "darkgreen")
        )
        asignar_btn.grid(row=0, column=0, padx=(15, 5), pady=15, sticky="ew")
        
        cancelar_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=self.destroy,
            fg_color=("gray", "darkgray")
        )
        cancelar_btn.grid(row=0, column=1, padx=(5, 15), pady=15, sticky="ew")
        
    def load_data(self):
        """Carga el personal disponible"""
        try:
            # Obtener personal que no está asignado al móvil
            personal = self.app.db_manager.fetch_all("""
                SELECT p.id, p.nombre, p.apellido, p.cargo
                FROM personal p
                WHERE p.activo = 1 
                AND p.id NOT IN (
                    SELECT ap.personal_id 
                    FROM asignaciones_personal ap 
                    WHERE ap.movil_id = ? AND ap.activo = 1
                )
                ORDER BY p.apellido, p.nombre
            """, (self.movil_id,))
            
            # Llenar listbox
            for persona in personal:
                item_text = f"{persona[1]} {persona[2]} - {persona[3]}"
                self.personal_listbox.insert('end', item_text)
                # Guardar ID como atributo del widget para referencia
                
            # Guardar IDs para referencia
            self.personal_ids = [persona[0] for persona in personal]
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando personal: {e}")
    
    def asignar_personal(self):
        """Asigna el personal seleccionado al móvil"""
        selection = self.personal_listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos una persona")
            return
        
        try:
            # Asignar cada persona seleccionada
            for index in selection:
                personal_id = self.personal_ids[index]
                
                self.app.db_manager.execute_query("""
                    INSERT INTO asignaciones_personal (movil_id, personal_id, fecha_asignacion, activo)
                    VALUES (?, ?, ?, 1)
                """, (self.movil_id, personal_id, datetime.now()))
            
            messagebox.showinfo("Éxito", f"Se asignaron {len(selection)} personas al móvil")
            
            # Actualizar la ventana parent
            self.parent.load_personal_asignado(self.movil_id)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error asignando personal: {e}")
