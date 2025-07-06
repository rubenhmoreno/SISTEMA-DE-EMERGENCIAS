"""
Gestor de WhatsApp - Sistema de Emergencias
Maneja el envío de alertas via WhatsApp usando la API de Nubelix
"""

import requests
import urllib.parse
from datetime import datetime
import sqlite3

class WhatsAppManager:
    def __init__(self):
        # Configuración de la API Nubelix
        self.base_url = "https://bot.nubelix.com/wabot/50aa4db2d5d872b6878edfe7755f194d"
        self.token = "e0072338d75f46d992f0430ffea2d154"
        self.session_url = f"{self.base_url}/api/session/status"
        
        # Conexión a la base de datos
        self.db_path = "data/emergencias.db"
    
    def check_session_status(self):
        """Verifica el estado de la sesión de WhatsApp"""
        try:
            response = requests.get(self.session_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Verificar si la respuesta indica que está conectado
                return data.get('connected', False) or data.get('status') == 'connected'
            return False
        except Exception as e:
            print(f"Error verificando estado WhatsApp: {e}")
            return False
    
    def send_message(self, phone_number, message):
        """Envía un mensaje de WhatsApp"""
        try:
            # Limpiar número de teléfono (remover espacios, guiones, etc.)
            clean_phone = self._clean_phone_number(phone_number)
            
            # Codificar mensaje para URL
            encoded_message = urllib.parse.quote(message)
            
            # Construir URL
            send_url = f"{self.base_url}/api/send/chat"
            params = {
                'uid': clean_phone,
                'text': encoded_message,
                'token': self.token
            }
            
            # Enviar mensaje
            response = requests.get(send_url, params=params, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                success = result.get('success', False) or response.status_code == 200
                return {
                    'success': success,
                    'response': result,
                    'message_id': result.get('id'),
                    'status': result.get('status', 'sent')
                }
            else:
                return {
                    'success': False,
                    'error': f"Error HTTP {response.status_code}",
                    'response': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _clean_phone_number(self, phone):
        """Limpia y formatea el número de teléfono"""
        # Remover espacios, guiones y paréntesis
        clean = ''.join(filter(str.isdigit, phone))
        
        # Si empieza con 54 (código de Argentina), mantenerlo
        if clean.startswith('54'):
            return clean
        
        # Si empieza con 0, removerlo
        if clean.startswith('0'):
            clean = clean[1:]
        
        # Si no tiene código de país, agregar 54 (Argentina)
        if not clean.startswith('54'):
            # Para números de Córdoba, agregar 54351
            if len(clean) == 7:  # Número local de Córdoba
                clean = '54351' + clean
            elif len(clean) == 10 and clean.startswith('351'):  # Con código de área
                clean = '54' + clean
            elif len(clean) == 10:  # Celular sin 54
                clean = '54' + clean
            else:
                clean = '54' + clean
        
        return clean
    
    def enviar_alerta_emergencia(self, llamada_id):
        """Envía alerta de emergencia según el tipo"""
        try:
            # Obtener datos de la llamada
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT l.numero_llamada, l.direccion_completa, l.descripcion_inicial,
                       l.receptor_destino, te.codigo, te.nombre, 
                       v.nombre, v.apellido, v.telefono
                FROM llamadas l
                JOIN tipos_emergencia te ON l.tipo_emergencia_id = te.id
                LEFT JOIN vecinos v ON l.vecino_id = v.id
                WHERE l.id = ?
            """, (llamada_id,))
            
            llamada = cursor.fetchone()
            
            if not llamada:
                return {'success': False, 'error': 'Llamada no encontrada'}
            
            numero_llamada, direccion, descripcion, receptor_destino, tipo_codigo, tipo_nombre, nombre, apellido, telefono = llamada
            
            # Construir mensaje
            mensaje = self._construir_mensaje_alerta(
                numero_llamada, direccion, descripcion, tipo_nombre, 
                nombre, apellido, telefono
            )
            
            # Obtener números de destino
            numeros_destino = self._obtener_numeros_destino(tipo_codigo, receptor_destino)
            
            # Enviar a cada número
            resultados = []
            for numero in numeros_destino:
                resultado = self.send_message(numero, mensaje)
                resultados.append({
                    'numero': numero,
                    'resultado': resultado
                })
                
                # Registrar en logs
                self._registrar_envio_whatsapp(llamada_id, numero, resultado)
            
            # Marcar como enviado en la llamada
            cursor.execute("""
                UPDATE llamadas SET whatsapp_enviado = 1 WHERE id = ?
            """, (llamada_id,))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'resultados': resultados,
                'total_enviados': len([r for r in resultados if r['resultado']['success']])
            }
            
        except Exception as e:
            print(f"Error enviando alerta de emergencia: {e}")
            return {'success': False, 'error': str(e)}
    
    def _construir_mensaje_alerta(self, numero_llamada, direccion, descripcion, tipo, nombre, apellido, telefono):
        """Construye el mensaje de alerta"""
        mensaje = f"🚨 *ALERTA DE EMERGENCIA* 🚨\n\n"
        mensaje += f"📋 *Llamada:* {numero_llamada}\n"
        mensaje += f"🚨 *Tipo:* {tipo}\n"
        mensaje += f"📍 *Dirección:* {direccion}\n"
        
        if nombre and apellido:
            mensaje += f"👤 *Solicitante:* {nombre} {apellido}\n"
        
        if telefono:
            mensaje += f"📞 *Teléfono:* {telefono}\n"
        
        if descripcion:
            mensaje += f"📝 *Descripción:* {descripcion}\n"
        
        mensaje += f"\n⏰ *Hora:* {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        mensaje += f"🏥 *Sistema de Emergencias Villa Allende*"
        
        return mensaje
    
    def _obtener_numeros_destino(self, tipo_codigo, receptor_destino=None):
        """Obtiene los números de destino según el tipo de emergencia"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            numeros = []
            
            if tipo_codigo == 'MEDICA':
                # Para emergencias médicas, usar el receptor específico
                if receptor_destino == 'CEC':
                    cursor.execute("""
                        SELECT numero FROM config_whatsapp 
                        WHERE tipo = 'MEDICA_CEC' AND activo = 1
                    """)
                else:  # DEMVA por defecto
                    cursor.execute("""
                        SELECT numero FROM config_whatsapp 
                        WHERE tipo = 'MEDICA_DEMVA' AND activo = 1
                    """)
            else:
                # Para otros tipos, usar configuración directa
                cursor.execute("""
                    SELECT numero FROM config_whatsapp 
                    WHERE tipo = ? AND activo = 1
                """, (tipo_codigo,))
            
            resultados = cursor.fetchall()
            numeros = [r[0] for r in resultados]
            
            conn.close()
            return numeros
            
        except Exception as e:
            print(f"Error obteniendo números destino: {e}")
            return []
    
    def _registrar_envio_whatsapp(self, llamada_id, numero, resultado):
        """Registra el envío de WhatsApp en logs"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            estado = 'enviado' if resultado['success'] else 'error'
            detalles = f"Número: {numero}, Estado: {estado}"
            
            if not resultado['success']:
                detalles += f", Error: {resultado.get('error', 'Unknown')}"
            
            cursor.execute("""
                INSERT INTO logs_sistema (usuario_id, accion, detalles, timestamp)
                VALUES (?, ?, ?, ?)
            """, (None, 'WHATSAPP_SEND', detalles, datetime.now()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error registrando envío WhatsApp: {e}")
    
    def test_connection(self):
        """Prueba la conexión de WhatsApp"""
        try:
            # Verificar estado de sesión
            is_connected = self.check_session_status()
            
            if is_connected:
                return {
                    'success': True,
                    'message': 'WhatsApp conectado correctamente',
                    'status': 'online'
                }
            else:
                return {
                    'success': False,
                    'message': 'WhatsApp no está conectado',
                    'status': 'offline'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error probando conexión: {str(e)}',
                'status': 'error'
            }
    
    def enviar_mensaje_prueba(self, numero_destino):
        """Envía un mensaje de prueba"""
        mensaje = f"🧪 *Mensaje de Prueba*\n\n"
        mensaje += f"Este es un mensaje de prueba del Sistema de Emergencias Villa Allende.\n\n"
        mensaje += f"⏰ Enviado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        mensaje += f"✅ Si recibe este mensaje, la configuración es correcta."
        
        return self.send_message(numero_destino, mensaje)
    
    def get_phone_status(self, phone_number):
        """Obtiene el estado de un número de teléfono en WhatsApp"""
        try:
            # Esta funcionalidad dependería de la API específica
            # Por ahora retornamos un estado básico
            clean_phone = self._clean_phone_number(phone_number)
            
            # Podrías implementar una verificación más específica aquí
            return {
                'phone': clean_phone,
                'exists': True,  # Asumir que existe
                'last_seen': None
            }
            
        except Exception as e:
            return {
                'phone': phone_number,
                'exists': False,
                'error': str(e)
            }
