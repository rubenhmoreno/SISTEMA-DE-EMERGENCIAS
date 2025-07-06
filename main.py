#!/usr/bin/env python3
"""
Sistema de Gestión de Emergencias
Villa Allende - Córdoba, Argentina

Autor: Sistema de Emergencias
Versión: 1.0
Fecha: 2025
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import os
import sys
from datetime import datetime

# Importar módulos del sistema
from database.db_manager import DatabaseManager
from gui.login_window import LoginWindow
from gui.main_window import MainWindow
from utils.config import Config
from utils.logger import Logger

class EmergencySystem:
    def __init__(self):
        # Configurar tema de CustomTkinter
        ctk.set_appearance_mode("system")  # "dark", "light", "system"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        self.config = Config()
        self.logger = Logger()
        self.db_manager = None
        self.current_user = None
        
        # Inicializar sistema
        self.initialize_system()
        
    def initialize_system(self):
        """Inicializa el sistema y la base de datos"""
        try:
            # Crear directorios necesarios
            os.makedirs("data", exist_ok=True)
            os.makedirs("logs", exist_ok=True)
            os.makedirs("exports", exist_ok=True)
            os.makedirs("backups", exist_ok=True)
            
            # Inicializar base de datos
            self.db_manager = DatabaseManager()
            
            # Verificar si es la primera ejecución
            if self.db_manager.is_first_run():
                self.setup_initial_data()
                
            self.logger.log("Sistema inicializado correctamente")
            
        except Exception as e:
            self.logger.log(f"Error al inicializar sistema: {str(e)}", level="ERROR")
            messagebox.showerror("Error", f"Error al inicializar el sistema:\n{str(e)}")
            sys.exit(1)
    
    def setup_initial_data(self):
        """Configura datos iniciales del sistema"""
        try:
            # Crear usuario administrador por defecto
            admin_password = hashlib.sha256("admin123".encode()).hexdigest()
            
            self.db_manager.execute_query("""
                INSERT INTO usuarios (username, password, rol, nombre_completo, activo)
                VALUES (?, ?, ?, ?, ?)
            """, ("admin", admin_password, "administrador", "Administrador del Sistema", 1))
            
            # Insertar tipos de emergencia
            tipos_emergencia = [
                ("MEDICA", "Emergencia Médica", 1),
                ("BOMBEROS", "Bomberos", 2),
                ("DEFENSA_CIVIL", "Defensa Civil", 3),
                ("SEGURIDAD", "Seguridad Ciudadana", 4),
                ("GENERAL", "Llamada General", 5)
            ]
            
            for tipo in tipos_emergencia:
                self.db_manager.execute_query("""
                    INSERT INTO tipos_emergencia (codigo, nombre, prioridad)
                    VALUES (?, ?, ?)
                """, tipo)
            
            # Insertar barrios de Villa Allende
            barrios = [
                "Centro", "Villa Allende Golf", "Lomas de la Carolina", 
                "Los Boulevares", "Villa Belgrano", "Parque Norte",
                "Villa del Dique", "La Reserva", "Villa Nueva",
                "Los Aromos", "Santa Ana", "Villa Warcalde"
            ]
            
            for barrio in barrios:
                self.db_manager.execute_query("""
                    INSERT INTO barrios (nombre, activo) VALUES (?, ?)
                """, (barrio, 1))
            
            # Configuraciones WhatsApp por defecto
            config_whatsapp = [
                ("MEDICA_DEMVA", "573001234567", 1),
                ("MEDICA_CEC", "573001234568", 1),
                ("BOMBEROS", "573001234569", 1),
                ("DEFENSA_CIVIL", "573001234570", 1),
                ("SEGURIDAD", "573001234571", 1)
            ]
            
            for config in config_whatsapp:
                self.db_manager.execute_query("""
                    INSERT INTO config_whatsapp (tipo, numero, activo)
                    VALUES (?, ?, ?)
                """, config)
            
            self.logger.log("Datos iniciales configurados correctamente")
            
        except Exception as e:
            self.logger.log(f"Error al configurar datos iniciales: {str(e)}", level="ERROR")
            raise
    
    def login(self, username, password):
        """Maneja el proceso de login"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            user = self.db_manager.fetch_one("""
                SELECT id, username, rol, nombre_completo, activo
                FROM usuarios 
                WHERE username = ? AND password = ? AND activo = 1
            """, (username, password_hash))
            
            if user:
                self.current_user = {
                    'id': user[0],
                    'username': user[1],
                    'rol': user[2],
                    'nombre_completo': user[3]
                }
                
                # Registrar login
                self.db_manager.execute_query("""
                    INSERT INTO logs_sistema (usuario_id, accion, detalles, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (user[0], "LOGIN", f"Usuario {username} inició sesión", datetime.now()))
                
                self.logger.log(f"Login exitoso para usuario: {username}")
                return True
            else:
                self.logger.log(f"Intento de login fallido para usuario: {username}")
                return False
                
        except Exception as e:
            self.logger.log(f"Error en login: {str(e)}", level="ERROR")
            return False
    
    def logout(self):
        """Maneja el proceso de logout"""
        if self.current_user:
            try:
                # Registrar logout
                self.db_manager.execute_query("""
                    INSERT INTO logs_sistema (usuario_id, accion, detalles, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (self.current_user['id'], "LOGOUT", 
                     f"Usuario {self.current_user['username']} cerró sesión", datetime.now()))
                
                self.logger.log(f"Logout para usuario: {self.current_user['username']}")
                self.current_user = None
                
            except Exception as e:
                self.logger.log(f"Error en logout: {str(e)}", level="ERROR")
    
    def run(self):
        """Ejecuta la aplicación"""
        try:
            # Mostrar ventana de login
            login_window = LoginWindow(self)
            login_window.mainloop()
            
            # Si el login fue exitoso, mostrar ventana principal
            if self.current_user:
                main_window = MainWindow(self)
                main_window.mainloop()
                
        except Exception as e:
            self.logger.log(f"Error en ejecución principal: {str(e)}", level="ERROR")
            messagebox.showerror("Error", f"Error en la aplicación:\n{str(e)}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Limpia recursos antes de cerrar"""
        try:
            if self.current_user:
                self.logout()
            
            if self.db_manager:
                self.db_manager.close()
                
            self.logger.log("Sistema cerrado correctamente")
            
        except Exception as e:
            print(f"Error en cleanup: {str(e)}")

def main():
    """Función principal"""
    try:
        app = EmergencySystem()
        app.run()
    except Exception as e:
        print(f"Error fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
