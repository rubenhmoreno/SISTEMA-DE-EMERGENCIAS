"""
Utilidad de Configuración - Sistema de Emergencias
Maneja la configuración general del sistema
"""

import json
import os
from datetime import datetime

class Config:
    def __init__(self, config_file="data/config.json"):
        self.config_file = config_file
        self.config_data = {}
        self.load_config()
    
    def load_config(self):
        """Carga la configuración desde el archivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
            else:
                # Crear configuración por defecto
                self.create_default_config()
                self.save_config()
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            self.create_default_config()
    
    def create_default_config(self):
        """Crea la configuración por defecto"""
        self.config_data = {
            "sistema": {
                "nombre": "Sistema de Emergencias Villa Allende",
                "version": "1.0.0",
                "fecha_instalacion": datetime.now().isoformat(),
                "organizacion": "Municipalidad de Villa Allende",
                "direccion": "Villa Allende, Córdoba, Argentina",
                "telefono_central": "3543-498000"
            },
            "base_datos": {
                "path": "data/emergencias.db",
                "backup_automatico": True,
                "backup_intervalo_horas": 24,
                "backup_directorio": "backups/"
            },
            "whatsapp": {
                "api_url": "https://bot.nubelix.com/wabot/50aa4db2d5d872b6878edfe7755f194d",
                "token": "e0072338d75f46d992f0430ffea2d154",
                "timeout_segundos": 15,
                "reintentos": 3
            },
            "mapas": {
                "proveedor": "google",
                "zoom_defecto": 15,
                "centro_lat": -31.3298,
                "centro_lng": -64.2959,
                "url_base": "https://www.google.com/maps/search/"
            },
            "interfaz": {
                "tema": "system",  # system, dark, light
                "color_tema": "blue",  # blue, green, dark-blue
                "idioma": "es",
                "formato_fecha": "DD/MM/YYYY",
                "formato_hora": "HH:MM:SS"
            },
            "seguridad": {
                "timeout_sesion_minutos": 480,  # 8 horas
                "intentos_login_max": 5,
                "bloqueo_tiempo_minutos": 30,
                "log_acciones": True
            },
            "emergencias": {
                "numero_llamada_prefijo": "EM",
                "prioridades": {
                    "1": {"nombre": "Crítica", "color": "red", "tiempo_respuesta": 5},
                    "2": {"nombre": "Alta", "color": "orange", "tiempo_respuesta": 15},
                    "3": {"nombre": "Media", "color": "yellow", "tiempo_respuesta": 30},
                    "4": {"nombre": "Baja", "color": "green", "tiempo_respuesta": 60},
                    "5": {"nombre": "Sin triaje", "color": "gray", "tiempo_respuesta": 120}
                }
            },
            "reportes": {
                "directorio": "exports/",
                "formato_defecto": "xlsx",
                "incluir_logo": True,
                "mostrar_pie_pagina": True
            },
            "logs": {
                "nivel": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
                "directorio": "logs/",
                "rotacion_dias": 30,
                "archivo_max_mb": 10
            }
        }
    
    def save_config(self):
        """Guarda la configuración al archivo"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def get(self, key_path, default=None):
        """
        Obtiene un valor de configuración usando notación de puntos
        Ejemplo: config.get('sistema.nombre')
        """
        try:
            keys = key_path.split('.')
            value = self.config_data
            
            for key in keys:
                value = value[key]
            
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """
        Establece un valor de configuración usando notación de puntos
        Ejemplo: config.set('sistema.nombre', 'Nuevo Nombre')
        """
        try:
            keys = key_path.split('.')
            target = self.config_data
            
            # Navegar hasta el penúltimo nivel
            for key in keys[:-1]:
                if key not in target:
                    target[key] = {}
                target = target[key]
            
            # Establecer el valor final
            target[keys[-1]] = value
            
            # Guardar automáticamente
            self.save_config()
            return True
        except Exception as e:
            print(f"Error estableciendo configuración: {e}")
            return False
    
    def update_section(self, section, data):
        """Actualiza una sección completa de la configuración"""
        try:
            self.config_data[section] = data
            self.save_config()
            return True
        except Exception as e:
            print(f"Error actualizando sección: {e}")
            return False
    
    def get_whatsapp_config(self):
        """Obtiene la configuración de WhatsApp"""
        return self.get('whatsapp', {})
    
    def get_database_config(self):
        """Obtiene la configuración de base de datos"""
        return self.get('base_datos', {})
    
    def get_maps_config(self):
        """Obtiene la configuración de mapas"""
        return self.get('mapas', {})
    
    def get_security_config(self):
        """Obtiene la configuración de seguridad"""
        return self.get('seguridad', {})
    
    def get_interface_config(self):
        """Obtiene la configuración de interfaz"""
        return self.get('interfaz', {})
    
    def get_emergency_config(self):
        """Obtiene la configuración de emergencias"""
        return self.get('emergencias', {})
    
    def validate_config(self):
        """Valida que la configuración tenga todos los campos necesarios"""
        required_sections = [
            'sistema', 'base_datos', 'whatsapp', 'mapas', 
            'interfaz', 'seguridad', 'emergencias', 'reportes', 'logs'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in self.config_data:
                missing_sections.append(section)
        
        return len(missing_sections) == 0, missing_sections
    
    def reset_to_defaults(self):
        """Resetea la configuración a los valores por defecto"""
        self.create_default_config()
        self.save_config()
    
    def export_config(self, file_path):
        """Exporta la configuración a un archivo"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exportando configuración: {e}")
            return False
    
    def import_config(self, file_path):
        """Importa configuración desde un archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # Validar que tenga estructura básica
            if isinstance(imported_data, dict):
                self.config_data = imported_data
                self.save_config()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error importando configuración: {e}")
            return False
    
    def get_all_config(self):
        """Retorna toda la configuración"""
        return self.config_data.copy()
    
    def backup_config(self):
        """Crea un backup de la configuración actual"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backups/config_backup_{timestamp}.json"
            
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            
            return backup_file
        except Exception as e:
            print(f"Error creando backup de configuración: {e}")
            return None
