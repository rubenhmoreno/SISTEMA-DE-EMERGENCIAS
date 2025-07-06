"""
Gestor de Base de Datos - Sistema de Emergencias
Maneja todas las operaciones de SQLite
"""

import sqlite3
import os
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self, db_path="data/emergencias.db"):
        self.db_path = db_path
        self.connection = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Para acceso por nombre de columna
            # Habilitar claves foráneas
            self.connection.execute("PRAGMA foreign_keys = ON")
            return True
        except Exception as e:
            print(f"Error conectando a la base de datos: {e}")
            return False
    
    def create_tables(self):
        """Crea todas las tablas necesarias"""
        
        # Tabla de usuarios
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                rol TEXT NOT NULL CHECK (rol IN ('operador', 'supervisor', 'administrador')),
                nombre_completo TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                activo INTEGER DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                ultimo_acceso DATETIME
            )
        """)
        
        # Tabla de tipos de emergencia
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS tipos_emergencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                prioridad INTEGER DEFAULT 1,
                activo INTEGER DEFAULT 1
            )
        """)
        
        # Tabla de barrios
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS barrios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                codigo_postal TEXT,
                activo INTEGER DEFAULT 1
            )
        """)
        
        # Tabla de vecinos/solicitantes
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS vecinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT NOT NULL,
                telefono_alternativo TEXT,
                direccion TEXT NOT NULL,
                numero TEXT,
                piso TEXT,
                departamento TEXT,
                barrio_id INTEGER,
                coordenadas_lat REAL,
                coordenadas_lng REAL,
                observaciones TEXT,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (barrio_id) REFERENCES barrios (id)
            )
        """)
        
        # Tabla de móviles
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS moviles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                tipo TEXT NOT NULL CHECK (tipo IN ('ambulancia', 'patrulla', 'rescate')),
                patente TEXT,
                modelo TEXT,
                año INTEGER,
                estado TEXT DEFAULT 'disponible' CHECK (estado IN ('disponible', 'ocupado', 'fuera_servicio', 'mantenimiento')),
                ubicacion_actual TEXT,
                observaciones TEXT,
                activo INTEGER DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de personal
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS personal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cargo TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                activo INTEGER DEFAULT 1,
                fecha_ingreso DATE,
                observaciones TEXT
            )
        """)
        
        # Tabla de asignaciones de personal a móviles
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS asignaciones_personal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movil_id INTEGER NOT NULL,
                personal_id INTEGER NOT NULL,
                fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_desasignacion DATETIME,
                turno TEXT,
                activo INTEGER DEFAULT 1,
                FOREIGN KEY (movil_id) REFERENCES moviles (id),
                FOREIGN KEY (personal_id) REFERENCES personal (id)
            )
        """)
        
        # Tabla principal de llamadas/alertas
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS llamadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_llamada TEXT UNIQUE NOT NULL,
                vecino_id INTEGER,
                tipo_emergencia_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                direccion_completa TEXT NOT NULL,
                coordenadas_lat REAL,
                coordenadas_lng REAL,
                descripcion_inicial TEXT,
                prioridad INTEGER DEFAULT 1,
                estado TEXT DEFAULT 'activa' CHECK (estado IN ('activa', 'despachada', 'en_curso', 'finalizada', 'cancelada')),
                movil_despachado_id INTEGER,
                receptor_destino TEXT, -- Para médicas: DEMVA o CEC
                fecha_despacho DATETIME,
                fecha_cierre DATETIME,
                observaciones_cierre TEXT,
                whatsapp_enviado INTEGER DEFAULT 0,
                FOREIGN KEY (vecino_id) REFERENCES vecinos (id),
                FOREIGN KEY (tipo_emergencia_id) REFERENCES tipos_emergencia (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (movil_despachado_id) REFERENCES moviles (id)
            )
        """)
        
        # Tabla de triaje médico
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS triaje_medico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                llamada_id INTEGER NOT NULL,
                paciente_consciente INTEGER,
                respira_normal INTEGER,
                pulso_presente INTEGER,
                sangrado_abundante INTEGER,
                dolor_pecho INTEGER,
                edad_aproximada INTEGER,
                sexo TEXT,
                sintomas_principales TEXT,
                antecedentes_relevantes TEXT,
                medicamentos_actuales TEXT,
                nivel_prioridad INTEGER,
                recomendacion_despacho INTEGER DEFAULT 0,
                observaciones TEXT,
                FOREIGN KEY (llamada_id) REFERENCES llamadas (id)
            )
        """)
        
        # Tabla de triaje bomberos
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS triaje_bomberos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                llamada_id INTEGER NOT NULL,
                tipo_incendio TEXT CHECK (tipo_incendio IN ('domicilio', 'via_publica', 'vehiculo', 'otro')),
                hay_personas_atrapadas INTEGER DEFAULT 0,
                extension_aproximada TEXT,
                materiales_involucrados TEXT,
                hay_explosivos INTEGER DEFAULT 0,
                viento_direccion TEXT,
                accesos_disponibles TEXT,
                hidrantes_cercanos INTEGER DEFAULT 0,
                nivel_prioridad INTEGER,
                observaciones TEXT,
                FOREIGN KEY (llamada_id) REFERENCES llamadas (id)
            )
        """)
        
        # Tabla de triaje defensa civil
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS triaje_defensa_civil (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                llamada_id INTEGER NOT NULL,
                tipo_evento TEXT,
                personas_afectadas INTEGER DEFAULT 0,
                personas_evacuadas INTEGER DEFAULT 0,
                daños_estructurales INTEGER DEFAULT 0,
                servicios_afectados TEXT,
                necesidad_evacuacion INTEGER DEFAULT 0,
                recursos_necesarios TEXT,
                acceso_vehicular INTEGER DEFAULT 1,
                coordinacion_otros_organismos TEXT,
                nivel_prioridad INTEGER,
                observaciones TEXT,
                FOREIGN KEY (llamada_id) REFERENCES llamadas (id)
            )
        """)
        
        # Tabla de triaje seguridad ciudadana
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS triaje_seguridad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                llamada_id INTEGER NOT NULL,
                tipo_incidente TEXT,
                hay_heridos INTEGER DEFAULT 0,
                agresor_presente INTEGER DEFAULT 0,
                agresor_armado INTEGER DEFAULT 0,
                vehiculos_involucrados TEXT,
                testigos_presentes INTEGER DEFAULT 0,
                necesidad_ambulancia INTEGER DEFAULT 0,
                necesidad_bomberos INTEGER DEFAULT 0,
                peligro_inmediato INTEGER DEFAULT 0,
                nivel_prioridad INTEGER,
                observaciones TEXT,
                FOREIGN KEY (llamada_id) REFERENCES llamadas (id)
            )
        """)
        
        # Tabla de novedades/seguimiento
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS novedades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                llamada_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                tipo_novedad TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                archivo_adjunto TEXT,
                FOREIGN KEY (llamada_id) REFERENCES llamadas (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        """)
        
        # Tabla de configuración WhatsApp
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS config_whatsapp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                numero TEXT NOT NULL,
                activo INTEGER DEFAULT 1,
                fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de logs del sistema
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS logs_sistema (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                accion TEXT NOT NULL,
                detalles TEXT,
                ip_address TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        """)
        
        # Índices para mejorar performance
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_llamadas_fecha ON llamadas (fecha_hora)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_llamadas_estado ON llamadas (estado)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_vecinos_dni ON vecinos (dni)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_vecinos_telefono ON vecinos (telefono)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs_sistema (timestamp)")
    
    def execute_query(self, query, params=None):
        """Ejecuta una query de modificación (INSERT, UPDATE, DELETE)"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            print(f"Error ejecutando query: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            raise
    
    def fetch_all(self, query, params=None):
        """Ejecuta una query de consulta y retorna todos los resultados"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en fetch_all: {e}")
            return []
    
    def fetch_one(self, query, params=None):
        """Ejecuta una query de consulta y retorna un resultado"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except Exception as e:
            print(f"Error en fetch_one: {e}")
            return None
    
    def get_last_insert_id(self):
        """Retorna el ID del último registro insertado"""
        return cursor.lastrowid
    
    def is_first_run(self):
        """Verifica si es la primera ejecución del sistema"""
        result = self.fetch_one("SELECT COUNT(*) as count FROM usuarios")
        return result[0] == 0 if result else True
    
    def backup_database(self, backup_path=None):
        """Crea un backup de la base de datos"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backups/backup_{timestamp}.db"
        
        try:
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Crear conexión de backup
            backup_conn = sqlite3.connect(backup_path)
            self.connection.backup(backup_conn)
            backup_conn.close()
            
            return backup_path
        except Exception as e:
            print(f"Error creando backup: {e}")
            return None
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()
