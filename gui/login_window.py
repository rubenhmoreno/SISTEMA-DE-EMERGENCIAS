"""
Ventana de Login - Sistema de Emergencias
"""

import customtkinter as ctk
from tkinter import messagebox
import os

class LoginWindow(ctk.CTk):
    def __init__(self, app):
        super().__init__()
        
        self.app = app
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configura la ventana principal"""
        self.title("Sistema de Emergencias - Villa Allende")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="Sistema de Emergencias",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(30, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Villa Allende - Córdoba",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Frame de login
        login_frame = ctk.CTkFrame(main_frame)
        login_frame.grid(row=2, column=0, padx=40, pady=20, sticky="ew")
        login_frame.grid_columnconfigure(0, weight=1)
        
        # Campo usuario
        username_label = ctk.CTkLabel(login_frame, text="Usuario:")
        username_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.username_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Ingrese su usuario",
            width=300
        )
        self.username_entry.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        # Campo contraseña
        password_label = ctk.CTkLabel(login_frame, text="Contraseña:")
        password_label.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.password_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Ingrese su contraseña",
            show="*",
            width=300
        )
        self.password_entry.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Botón de login
        login_button = ctk.CTkButton(
            login_frame,
            text="Iniciar Sesión",
            command=self.handle_login,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        login_button.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Frame de información
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.grid(row=3, column=0, padx=40, pady=(10, 20), sticky="ew")
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Usuario por defecto: admin\nContraseña: admin123",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        info_label.grid(row=0, column=0, padx=20, pady=15)
        
        # Versión
        version_label = ctk.CTkLabel(
            main_frame,
            text="Versión 1.0 - 2025",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        version_label.grid(row=4, column=0, pady=(10, 20))
        
        # Eventos
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Focus inicial
        self.username_entry.focus()
        
    def handle_login(self):
        """Maneja el proceso de login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validaciones básicas
        if not username:
            messagebox.showerror("Error", "Debe ingresar un usuario")
            self.username_entry.focus()
            return
            
        if not password:
            messagebox.showerror("Error", "Debe ingresar una contraseña")
            self.password_entry.focus()
            return
        
        # Intentar login
        try:
            if self.app.login(username, password):
                messagebox.showinfo("Éxito", f"Bienvenido {self.app.current_user['nombre_completo']}")
                self.destroy()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                self.password_entry.delete(0, 'end')
                self.password_entry.focus()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el sistema de login:\n{str(e)}")
            
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        self.destroy()
        
    def show(self):
        """Muestra la ventana"""
        self.deiconify()
        self.lift()
        self.username_entry.focus()
