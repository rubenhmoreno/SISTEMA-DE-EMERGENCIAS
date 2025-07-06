"""
Sistema de Logging - Sistema de Emergencias
Maneja todos los logs del sistema
"""

import logging
import os
from datetime import datetime, timedelta
import glob

class Logger:
    def __init__(self, log_dir="logs", max_file_size_mb=10, retention_days=30):
        self.log_dir = log_dir
        self.max_file_size = max_file_size_mb * 1024 * 1024  # Convertir a bytes
        self.retention_days = retention_days
        
        # Crear directorio de logs si no existe
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Configurar logger
        self.setup_logger()
        
        # Limpiar logs antiguos
        self.cleanup_old_logs()
    
    def setup_logger(self):
        """Configura el sistema de logging"""
        
        # Crear logger principal
        self.logger = logging.getLogger('EmergencySystem')
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicar handlers si ya existen
        if self.logger.handlers:
            return
        
        # Formato de log
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para archivo de aplicación
        app_log_file = os.path.join(self.log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
        app_handler = logging.FileHandler(app_log_file, encoding='utf-8')
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(formatter)
        self.logger.addHandler(app_handler)
        
        # Handler para errores críticos
        error_log_file = os.path.join(self.log_dir, f"errors_{datetime.now().strftime('%Y%m%d')}.log")
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
        
        # Handler para consola (solo para desarrollo)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Handler para sistema de emergencias específico
        emergency_log_file = os.path.join(self.log_dir, f"emergency_{datetime.now().strftime('%Y%m%d')}.log")
        emergency_handler = logging.FileHandler(emergency_log_file, encoding='utf-8')
        emergency_handler.setLevel(logging.INFO)
        emergency_handler.setFormatter(formatter)
        
        # Crear logger específico para emergencias
        self.emergency_logger = logging.getLogger('EmergencySystem.Emergency')
        self.emergency_logger.addHandler(emergency_handler)
        self.emergency_logger.setLevel(logging.INFO)
    
    def log(self, message, level="INFO", category="GENERAL"):
        """
        Registra un mensaje en el log
        
        Args:
            message (str): Mensaje a registrar
            level (str): Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            category (str): Categoría del mensaje
        """
        
        # Agregar categoría al mensaje
        formatted_message = f"[{category}] {message}"
        
        # Registrar según el nivel
        if level.upper() == "DEBUG":
            self.logger.debug(formatted_message)
        elif level.upper() == "INFO":
            self.logger.info(formatted_message)
        elif level.upper() == "WARNING":
            self.logger.warning(formatted_message)
        elif level.upper() == "ERROR":
            self.logger.error(formatted_message)
        elif level.upper() == "CRITICAL":
            self.logger.critical(formatted_message)
        else:
            self.logger.info(formatted_message)
    
    def log_emergency(self, action, details, user_id=None, call_id=None):
        """
        Registra eventos específicos de emergencias
        
        Args:
            action (str): Acción realizada
            details (str): Detalles de la acción
            user_id (int): ID del usuario que realizó la acción
            call_id (int): ID de la llamada relacionada
        """
        
        emergency_info = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details,
            'user_id': user_id,
            'call_id': call_id
        }
        
        log_message = f"EMERGENCY_ACTION: {action}"
        if call_id:
            log_message += f" | CALL_ID: {call_id}"
        if user_id:
            log_message += f" | USER_ID: {user_id}"
        log_message += f" | DETAILS: {details}"
        
        self.emergency_logger.info(log_message)
    
    def log_user_action(self, user_id, username, action, details=""):
        """
        Registra acciones de usuarios
        
        Args:
            user_id (int): ID del usuario
            username (str): Nombre del usuario
            action (str): Acción realizada
            details (str): Detalles adicionales
        """
        
        message = f"USER_ACTION: {username} ({user_id}) - {action}"
        if details:
            message += f" - {details}"
        
        self.log(message, "INFO", "USER")
    
    def log_system_event(self, event, details=""):
        """
        Registra eventos del sistema
        
        Args:
            event (str): Tipo de evento
            details (str): Detalles del evento
        """
        
        message = f"SYSTEM_EVENT: {event}"
        if details:
            message += f" - {details}"
        
        self.log(message, "INFO", "SYSTEM")
    
    def log_whatsapp_event(self, action, phone_number, success, details=""):
        """
        Registra eventos de WhatsApp
        
        Args:
            action (str): Acción realizada (send, status_check, etc.)
            phone_number (str): Número de teléfono
            success (bool): Si la acción fue exitosa
            details (str): Detalles adicionales
        """
        
        status = "SUCCESS" if success else "FAILED"
        message = f"WHATSAPP_{action.upper()}: {phone_number} - {status}"
        if details:
            message += f" - {details}"
        
        level = "INFO" if success else "WARNING"
        self.log(message, level, "WHATSAPP")
    
    def log_database_event(self, operation, table, success, details=""):
        """
        Registra eventos de base de datos
        
        Args:
            operation (str): Operación realizada (INSERT, UPDATE, DELETE, etc.)
            table (str): Tabla afectada
            success (bool): Si la operación fue exitosa
            details (str): Detalles adicionales
        """
        
        status = "SUCCESS" if success else "FAILED"
        message = f"DATABASE_{operation.upper()}: {table} - {status}"
        if details:
            message += f" - {details}"
        
        level = "INFO" if success else "ERROR"
        self.log(message, level, "DATABASE")
    
    def log_security_event(self, event_type, username, ip_address="", details=""):
        """
        Registra eventos de seguridad
        
        Args:
            event_type (str): Tipo de evento (LOGIN_SUCCESS, LOGIN_FAILED, etc.)
            username (str): Usuario involucrado
            ip_address (str): Dirección IP
            details (str): Detalles adicionales
        """
        
        message = f"SECURITY_{event_type.upper()}: {username}"
        if ip_address:
            message += f" from {ip_address}"
        if details:
            message += f" - {details}"
        
        # Eventos de fallo son warnings
        level = "WARNING" if "FAILED" in event_type.upper() else "INFO"
        self.log(message, level, "SECURITY")
    
    def log_error(self, error, context="", user_id=None):
        """
        Registra errores del sistema
        
        Args:
            error (Exception or str): Error ocurrido
            context (str): Contexto donde ocurrió el error
            user_id (int): ID del usuario cuando ocurrió el error
        """
        
        if isinstance(error, Exception):
            error_message = f"{error.__class__.__name__}: {str(error)}"
        else:
            error_message = str(error)
        
        message = f"ERROR: {error_message}"
        if context:
            message += f" | CONTEXT: {context}"
        if user_id:
            message += f" | USER_ID: {user_id}"
        
        self.log(message, "ERROR", "ERROR")
    
    def get_log_stats(self, days=7):
        """
        Obtiene estadísticas de logs de los últimos días
        
        Args:
            days (int): Número de días para analizar
            
        Returns:
            dict: Estadísticas de logs
        """
        
        stats = {
            'total_entries': 0,
            'by_level': {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
            'by_category': {},
            'emergency_actions': 0,
            'user_actions': 0,
            'system_events': 0
        }
        
        try:
            # Obtener archivos de log de los últimos días
            start_date = datetime.now() - timedelta(days=days)
            
            for i in range(days + 1):
                current_date = start_date + timedelta(days=i)
                log_file = os.path.join(self.log_dir, f"app_{current_date.strftime('%Y%m%d')}.log")
                
                if os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            stats['total_entries'] += 1
                            
                            # Analizar nivel
                            for level in stats['by_level'].keys():
                                if f" - {level} - " in line:
                                    stats['by_level'][level] += 1
                                    break
                            
                            # Analizar categorías
                            if '[' in line and ']' in line:
                                start = line.find('[') + 1
                                end = line.find(']')
                                if start < end:
                                    category = line[start:end]
                                    stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
                            
                            # Contar tipos específicos
                            if 'EMERGENCY_ACTION:' in line:
                                stats['emergency_actions'] += 1
                            elif 'USER_ACTION:' in line:
                                stats['user_actions'] += 1
                            elif 'SYSTEM_EVENT:' in line:
                                stats['system_events'] += 1
            
        except Exception as e:
            self.log_error(e, "get_log_stats")
        
        return stats
    
    def cleanup_old_logs(self):
        """Elimina logs antiguos según la política de retención"""
        
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            
            # Buscar todos los archivos de log
            log_patterns = [
                os.path.join(self.log_dir, "app_*.log"),
                os.path.join(self.log_dir, "errors_*.log"),
                os.path.join(self.log_dir, "emergency_*.log")
            ]
            
            for pattern in log_patterns:
                for log_file in glob.glob(pattern):
                    try:
                        # Extraer fecha del nombre del archivo
                        filename = os.path.basename(log_file)
                        date_str = filename.split('_')[1].split('.')[0]
                        file_date = datetime.strptime(date_str, '%Y%m%d')
                        
                        if file_date < cutoff_date:
                            os.remove(log_file)
                            self.log(f"Archivo de log eliminado: {log_file}", "INFO", "CLEANUP")
                    except (ValueError, IndexError):
                        # Si no se puede parsear la fecha, ignorar el archivo
                        continue
                        
        except Exception as e:
            self.log_error(e, "cleanup_old_logs")
    
    def rotate_logs_if_needed(self):
        """Rota logs si exceden el tamaño máximo"""
        
        try:
            today = datetime.now().strftime('%Y%m%d')
            log_files = [
                f"app_{today}.log",
                f"errors_{today}.log", 
                f"emergency_{today}.log"
            ]
            
            for log_file in log_files:
                log_path = os.path.join(self.log_dir, log_file)
                
                if os.path.exists(log_path) and os.path.getsize(log_path) > self.max_file_size:
                    # Crear archivo rotado
                    timestamp = datetime.now().strftime('%H%M%S')
                    rotated_name = log_file.replace('.log', f'_{timestamp}.log')
                    rotated_path = os.path.join(self.log_dir, rotated_name)
                    
                    os.rename(log_path, rotated_path)
                    
                    self.log(f"Log rotado: {log_file} -> {rotated_name}", "INFO", "ROTATION")
                    
        except Exception as e:
            self.log_error(e, "rotate_logs_if_needed")
    
    def export_logs(self, start_date, end_date, export_file):
        """
        Exporta logs de un rango de fechas a un archivo
        
        Args:
            start_date (datetime): Fecha de inicio
            end_date (datetime): Fecha de fin
            export_file (str): Archivo de destino
            
        Returns:
            bool: True si la exportación fue exitosa
        """
        
        try:
            with open(export_file, 'w', encoding='utf-8') as output:
                output.write(f"# Logs del Sistema de Emergencias\n")
                output.write(f"# Período: {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}\n")
                output.write(f"# Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                current_date = start_date
                while current_date <= end_date:
                    log_file = os.path.join(self.log_dir, f"app_{current_date.strftime('%Y%m%d')}.log")
                    
                    if os.path.exists(log_file):
                        output.write(f"\n--- {current_date.strftime('%Y-%m-%d')} ---\n")
                        
                        with open(log_file, 'r', encoding='utf-8') as log_input:
                            output.write(log_input.read())
                    
                    current_date += timedelta(days=1)
            
            self.log(f"Logs exportados a: {export_file}", "INFO", "EXPORT")
            return True
            
        except Exception as e:
            self.log_error(e, "export_logs")
            return False
