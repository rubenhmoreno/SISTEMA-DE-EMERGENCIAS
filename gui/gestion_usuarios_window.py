"""
Ventana de Gestión de Usuarios - Sistema de Emergencias
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import hashlib
from datetime import datetime

class GestionUsuariosWindow(ctk.CTkToplevel):
    def __init__(self, app, parent):
        super().__init__(parent)
        
        self.app = app
        self.parent = parent
        self.selected_user_id = None
        
        self.setup_window()
        self.create_widgets()
        self.load_data()
        
    def setup_window(self):
        """Configura la ventana"""
        self.title("Gestión de Usuarios")
        self.geometry("900x600")
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(self.parent)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crea la interfaz"""
        
        # Panel izquierdo - Lista de usuarios
        self.create_left_panel()
        
        # Panel derecho - Detalles y formulario
        self.create_right_panel()
        
    def create_left_panel(self):
        """Crea el panel izquierdo con la lista de usuarios"""
        
        left_frame = ctk.CTkFrame(self, width=350)
        left_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_propagate(False)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            left_frame,
            text="👤 USUARIOS DEL SISTEMA",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Treeview para usuarios
        self.create_users_treeview(left_frame)
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(left_frame)
        buttons_frame.grid(row=2, column=0, padx=20, pady=(15, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Nuevo usuario
        new_btn = ctk.CTkButton(
            buttons_frame,
            text="➕ Nuevo",
            command=self.nuevo_usuario,
            fg_color=("green", "darkgreen")
        )
        new_btn.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        # Editar usuario
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Editar",
            command=self.editar_usuario,
            fg_color=("blue", "darkblue")
        )
        edit_btn.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        # Eliminar usuario
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Eliminar",
            command=self.eliminar_usuario,
            fg_color=("red", "darkred")
        )
        delete_btn.grid(row=0, column=2, padx=5, pady=10, sticky="ew")
        
    def create_users_treeview(self, parent):
        """Crea el treeview para mostrar usuarios"""
        
        # Frame para el treeview
        tree_frame = tk.Frame(parent)
        tree_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Treeview
        columns = ('Usuario', 'Nombre', 'Rol', 'Estado')
        self.users_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.users_tree.heading('Usuario', text='Usuario')
        self.users_tree.heading('Nombre', text='Nombre Completo')
        self.users_tree.heading('Rol', text='Rol')
        self.users_tree.heading('Estado', text='Estado')
        
        self.users_tree.column('Usuario', width=100)
        self.users_tree.column('Nombre', width=150)
        self.users_tree.column('Rol', width=80)
        self.users_tree.column('Estado', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.users_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Binding para selección
        self.users_tree.bind('<<TreeviewSelect>>', self.on_user_select)
        
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
            text="👤 DATOS DEL USUARIO",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Formulario
        self.create_form(main_scroll)
        
        # Sección de permisos y actividad
        self.create_activity_section(main_scroll)
        
        # Botones de acción
        self.create_form_buttons(main_scroll)
        
    def create_form(self, parent):
        """Crea el formulario de datos del usuario"""
        
        # Nombre de usuario
        ctk.CTkLabel(parent, text="Usuario:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        self.username_entry = ctk.CTkEntry(parent, placeholder_text="usuario123")
        self.username_entry.grid(row=1, column=1, pady=10, sticky="ew")
        
        # Contraseña
        ctk.CTkLabel(parent, text="Contraseña:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(0, 10), pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(parent, show="*", placeholder_text="Nueva contraseña")
        self.password_entry.grid(row=2, column=1, pady=10, sticky="ew")
        
        # Confirmar contraseña
        ctk.CTkLabel(parent, text="Confirmar:", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=(0, 10), pady=10, sticky="w")
        self.confirm_password_entry = ctk.CTkEntry(parent, show="*", placeholder_text="Confirmar contraseña")
        self.confirm_password_entry.grid(row=3, column=1, pady=10, sticky="ew")
        
        # Separador
        separator1 = ctk.CTkFrame(parent, height=2)
        separator1.grid(row=4, column=0, columnspan=2, padx=0, pady=15, sticky="ew")
        
        # Nombre completo
        ctk.CTkLabel(parent, text="Nombre completo:", font=ctk.CTkFont(weight="bold")).grid(
            row=5, column=0, padx=(0, 10), pady=10, sticky="w")
        self.nombre_entry = ctk.CTkEntry(parent, placeholder_text="Juan Pérez")
        self.nombre_entry.grid(row=5, column=1, pady=10, sticky="ew")
        
        # Teléfono
        ctk.CTkLabel(parent, text="Teléfono:", font=ctk.CTkFont(weight="bold")).grid(
            row=6, column=0, padx=(0, 10), pady=10, sticky="w")
        self.telefono_entry = ctk.CTkEntry(parent, placeholder_text="3516789012")
        self.telefono_entry.grid(row=6, column=1, pady=10, sticky="ew")
        
        # Email
        ctk.CTkLabel(parent, text="Email:", font=ctk.CTkFont(weight="bold")).grid(
            row=7, column=0, padx=(0, 10), pady=10, sticky="w")
        self.email_entry = ctk.CTkEntry(parent, placeholder_text="usuario@ejemplo.com")
        self.email_entry.grid(row=7, column=1, pady=10, sticky="ew")
        
        # Rol
        ctk.CTkLabel(parent, text="Rol:", font=ctk.CTkFont(weight="bold")).grid(
            row=8, column=0, padx=(0, 10), pady=10, sticky="w")
        self.rol_combo = ctk.CTkComboBox(
            parent,
            values=["operador", "supervisor", "administrador"],
            state="readonly"
        )
        self.rol_combo.grid(row=8, column=1, pady=10, sticky="ew")
        
        # Estado
        ctk.CTkLabel(parent, text="Estado:", font=ctk.CTkFont(weight="bold")).grid(
            row=9, column=0, padx=(0, 10), pady=10, sticky="w")
        self.activo_switch = ctk.CTkSwitch(parent, text="Usuario activo")
        self.activo_switch.grid(row=9, column=1, pady=10, sticky="w")
        
    def create_activity_section(self, parent):
        """Crea la sección de actividad del usuario"""
        
        # Separador
        separator2 = ctk.CTkFrame(parent, height=2)
        separator2.grid(row=10, column=0, columnspan=2, padx=0, pady=15, sticky="ew")
        
        # Título actividad
        activity_title = ctk.CTkLabel(
            parent,
            text="📊 INFORMACIÓN DE ACTIVIDAD",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        activity_title.grid(row=11, column=0, columnspan=2, pady=(10, 15))
        
        # Frame de información
        info_frame = ctk.CTkFrame(parent)
        info_frame.grid(row=12, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        info_frame.grid_columnconfigure(1, weight=1)
        
        # Fecha de creación
        ctk.CTkLabel(info_frame, text="Fecha de creación:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=(15, 10), pady=10, sticky="w")
        self.fecha_creacion_label = ctk.CTkLabel(info_frame, text="No disponible")
        self.fecha_creacion_label.grid(row=0, column=1, padx=(0, 15), pady=10, sticky="w")
        
        # Último acceso
        ctk.CTkLabel(info_frame, text="Último acceso:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=(15, 10), pady=10, sticky="w")
        self.ultimo_acceso_label = ctk.CTkLabel(info_frame, text="Nunca")
        self.ultimo_acceso_label.grid(row=1, column=1, padx=(0, 15), pady=10, sticky="w")
        
        # Llamadas registradas
        ctk.CTkLabel(info_frame, text="Llamadas registradas:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=(15, 10), pady=10, sticky="w")
        self.llamadas_label = ctk.CTkLabel(info_frame, text="0")
        self.llamadas_label.grid(row=2, column=1, padx=(0, 15), pady=10, sticky="w")
        
        # Botón resetear contraseña
        reset_btn = ctk.CTkButton(
            parent,
            text="🔑 Resetear Contraseña",
            command=self.resetear_contraseña,
            fg_color=("orange", "darkorange"),
            width=200
        )
        reset_btn.grid(row=13, column=0, columnspan=2, pady=15)
        
    def create_form_buttons(self, parent):
        """Crea los botones del formulario"""
        
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.grid(row=14, column=0, columnspan=2, pady=20, sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Guardar
        self.save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            command=self.guardar_usuario,
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
        self.refresh_users_list()
        
    def refresh_users_list(self):
        """Actualiza la lista de usuarios"""
        try:
            # Limpiar treeview
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Obtener usuarios
            usuarios = self.app.db_manager.fetch_all("""
                SELECT id, username, nombre_completo, rol, activo
                FROM usuarios
                ORDER BY username
            """)
            
            # Llenar treeview
            for usuario in usuarios:
                estado_icon = "✅" if usuario[4] else "❌"
                estado_text = "Activo" if usuario[4] else "Inactivo"
                
                self.users_tree.insert('', 'end', values=(
                    usuario[1],  # username
                    usuario[2],  # nombre_completo
                    usuario[3].title(),  # rol
                    f"{estado_icon} {estado_text}"  # estado
                ), tags=(usuario[0],))  # ID como tag
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando usuarios: {e}")
    
    def on_user_select(self, event):
        """Maneja la selección de un usuario"""
        selection = self.users_tree.selection()
        if selection:
            # Obtener ID del usuario
            item = self.users_tree.item(selection[0])
            self.selected_user_id = item['tags'][0]
            
            # Cargar datos del usuario
            self.load_user_data(self.selected_user_id)
    
    def load_user_data(self, user_id):
        """Carga los datos de un usuario específico"""
        try:
            # Obtener datos del usuario
            usuario = self.app.db_manager.fetch_one("""
                SELECT username, nombre_completo, telefono, email, rol, activo,
                       fecha_creacion, ultimo_acceso
                FROM usuarios WHERE id = ?
            """, (user_id,))
            
            if usuario:
                # Llenar formulario
                self.username_entry.delete(0, 'end')
                self.username_entry.insert(0, usuario[0] or "")
                
                # Limpiar campos de contraseña al editar
                self.password_entry.delete(0, 'end')
                self.confirm_password_entry.delete(0, 'end')
                
                self.nombre_entry.delete(0, 'end')
                self.nombre_entry.insert(0, usuario[1] or "")
                
                self.telefono_entry.delete(0, 'end')
                self.telefono_entry.insert(0, usuario[2] or "")
                
                self.email_entry.delete(0, 'end')
                self.email_entry.insert(0, usuario[3] or "")
                
                self.rol_combo.set(usuario[4] or "operador")
                
                if usuario[5]:
                    self.activo_switch.select()
                else:
                    self.activo_switch.deselect()
                
                # Información de actividad
                if usuario[6]:
                    fecha_creacion = datetime.strptime(usuario[6], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
                    self.fecha_creacion_label.configure(text=fecha_creacion)
                else:
                    self.fecha_creacion_label.configure(text="No disponible")
                
                if usuario[7]:
                    ultimo_acceso = datetime.strptime(usuario[7], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
                    self.ultimo_acceso_label.configure(text=ultimo_acceso)
                else:
                    self.ultimo_acceso_label.configure(text="Nunca")
                
                # Contar llamadas registradas
                llamadas_count = self.app.db_manager.fetch_one("""
                    SELECT COUNT(*) FROM llamadas WHERE usuario_id = ?
                """, (user_id,))
                self.llamadas_label.configure(text=str(llamadas_count[0] if llamadas_count else 0))
                
                # Cambiar título
                self.form_title.configure(text=f"👤 USUARIO: {usuario[0]}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando datos del usuario: {e}")
    
    def nuevo_usuario(self):
        """Prepara el formulario para un nuevo usuario"""
        self.selected_user_id = None
        self.limpiar_formulario()
        self.form_title.configure(text="👤 NUEVO USUARIO")
        self.username_entry.focus()
        
    def editar_usuario(self):
        """Edita el usuario seleccionado"""
        if not self.selected_user_id:
            messagebox.showwarning("Advertencia", "Debe seleccionar un usuario para editar")
            return
        # Los datos ya están cargados por la selección
        self.username_entry.focus()
        
    def eliminar_usuario(self):
        """Elimina el usuario seleccionado"""
        if not self.selected_user_id:
            messagebox.showwarning("Advertencia", "Debe seleccionar un usuario para eliminar")
            return
        
        # No permitir eliminar al usuario actual
        if self.selected_user_id == self.app.current_user['id']:
            messagebox.showerror("Error", "No puede eliminar su propio usuario")
            return
        
        # Obtener username para confirmación
        usuario = self.app.db_manager.fetch_one("""
            SELECT username FROM usuarios WHERE id = ?
        """, (self.selected_user_id,))
        
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado")
            return
        
        # Confirmación
        if messagebox.askyesno("Confirmar Eliminación", 
                             f"¿Está seguro que desea eliminar el usuario '{usuario[0]}'?\n"
                             "Esta acción marcará el usuario como inactivo."):
            try:
                # Marcar como inactivo (no eliminar físicamente)
                self.app.db_manager.execute_query("""
                    UPDATE usuarios SET activo = 0 WHERE id = ?
                """, (self.selected_user_id,))
                
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                
                # Actualizar lista y limpiar formulario
                self.refresh_users_list()
                self.limpiar_formulario()
                self.selected_user_id = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Error eliminando usuario: {e}")
    
    def guardar_usuario(self):
        """Guarda los datos del usuario"""
        try:
            # Validaciones
            if not self.username_entry.get().strip():
                messagebox.showerror("Error", "El nombre de usuario es obligatorio")
                return
            
            if not self.nombre_entry.get().strip():
                messagebox.showerror("Error", "El nombre completo es obligatorio")
                return
            
            if not self.rol_combo.get():
                messagebox.showerror("Error", "Debe seleccionar un rol")
                return
            
            # Validar contraseñas para nuevo usuario o si se está cambiando
            if not self.selected_user_id or self.password_entry.get():
                if not self.password_entry.get():
                    messagebox.showerror("Error", "La contraseña es obligatoria")
                    return
                
                if len(self.password_entry.get()) < 6:
                    messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
                    return
                
                if self.password_entry.get() != self.confirm_password_entry.get():
                    messagebox.showerror("Error", "Las contraseñas no coinciden")
                    return
            
            # Datos del usuario
            username = self.username_entry.get().strip()
            password = self.password_entry.get()
            nombre_completo = self.nombre_entry.get().strip()
            telefono = self.telefono_entry.get().strip() or None
            email = self.email_entry.get().strip() or None
            rol = self.rol_combo.get()
            activo = 1 if self.activo_switch.get() else 0
            
            if self.selected_user_id:
                # Verificar que no exista otro usuario con el mismo username
                existe = self.app.db_manager.fetch_one("""
                    SELECT id FROM usuarios WHERE username = ? AND id != ?
                """, (username, self.selected_user_id))
                
                if existe:
                    messagebox.showerror("Error", "Ya existe otro usuario con ese nombre")
                    return
                
                # Actualizar usuario existente
                if password:
                    # Cambiar contraseña también
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    self.app.db_manager.execute_query("""
                        UPDATE usuarios SET 
                        username = ?, password = ?, nombre_completo = ?, telefono = ?,
                        email = ?, rol = ?, activo = ?
                        WHERE id = ?
                    """, (username, password_hash, nombre_completo, telefono, email, rol, activo, self.selected_user_id))
                else:
                    # No cambiar contraseña
                    self.app.db_manager.execute_query("""
                        UPDATE usuarios SET 
                        username = ?, nombre_completo = ?, telefono = ?,
                        email = ?, rol = ?, activo = ?
                        WHERE id = ?
                    """, (username, nombre_completo, telefono, email, rol, activo, self.selected_user_id))
                
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            else:
                # Verificar que no exista el username
                existe = self.app.db_manager.fetch_one("""
                    SELECT id FROM usuarios WHERE username = ?
                """, (username,))
                
                if existe:
                    messagebox.showerror("Error", "Ya existe un usuario con ese nombre")
                    return
                
                # Crear nuevo usuario
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                self.app.db_manager.execute_query("""
                    INSERT INTO usuarios (username, password, nombre_completo, telefono,
                                        email, rol, activo, fecha_creacion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, password_hash, nombre_completo, telefono, email, rol, activo, datetime.now()))
                
                self.selected_user_id = self.app.db_manager.get_last_insert_id()
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
            
            # Actualizar lista
            self.refresh_users_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando usuario: {e}")
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')
        self.nombre_entry.delete(0, 'end')
        self.telefono_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.rol_combo.set("")
        self.activo_switch.select()  # Por defecto activo
        
        # Limpiar información de actividad
        self.fecha_creacion_label.configure(text="No disponible")
        self.ultimo_acceso_label.configure(text="Nunca")
        self.llamadas_label.configure(text="0")
        
        self.form_title.configure(text="👤 DATOS DEL USUARIO")
    
    def resetear_contraseña(self):
        """Resetea la contraseña del usuario seleccionado"""
        if not self.selected_user_id:
            messagebox.showwarning("Advertencia", "Debe seleccionar un usuario primero")
            return
        
        # No permitir resetear la contraseña del usuario actual
        if self.selected_user_id == self.app.current_user['id']:
            messagebox.showwarning("Advertencia", "No puede resetear su propia contraseña desde aquí")
            return
        
        # Obtener username para confirmación
        usuario = self.app.db_manager.fetch_one("""
            SELECT username FROM usuarios WHERE id = ?
        """, (self.selected_user_id,))
        
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado")
            return
        
        # Generar nueva contraseña temporal
        nueva_password = f"temp{datetime.now().strftime('%Y%m%d')}"
        
        if messagebox.askyesno("Resetear Contraseña", 
                             f"¿Resetear la contraseña del usuario '{usuario[0]}'?\n\n"
                             f"Nueva contraseña temporal: {nueva_password}\n\n"
                             "El usuario deberá cambiarla en su próximo acceso."):
            try:
                # Actualizar contraseña
                password_hash = hashlib.sha256(nueva_password.encode()).hexdigest()
                self.app.db_manager.execute_query("""
                    UPDATE usuarios SET password = ? WHERE id = ?
                """, (password_hash, self.selected_user_id))
                
                messagebox.showinfo("Contraseña Reseteada", 
                                  f"Contraseña reseteada exitosamente.\n\n"
                                  f"Nueva contraseña: {nueva_password}\n\n"
                                  "Informe al usuario su nueva contraseña.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error reseteando contraseña: {e}")
