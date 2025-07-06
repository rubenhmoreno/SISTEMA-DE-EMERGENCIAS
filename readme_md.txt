# 🚨 Sistema de Emergencias Villa Allende

## Descripción

Sistema integral de gestión de emergencias médicas, defensa civil, seguridad ciudadana y bomberos para la Municipalidad de Villa Allende, Córdoba, Argentina.

### Características Principales

- ✅ **Gestión de Alertas y Triaje** - Sistema completo de triaje para cada tipo de emergencia
- ✅ **Base de Datos Unificada** - SQLite con capacidad de importar/exportar Excel
- ✅ **Gestión de Llamadas** - Seguimiento completo desde recepción hasta cierre
- ✅ **Integración WhatsApp** - Envío automático de alertas via API
- ✅ **Gestión de Usuarios** - Control de acceso por roles
- ✅ **Gestión de Móviles** - Control de estado y asignación de personal
- ✅ **Interfaz Moderna** - GUI intuitiva y responsive con CustomTkinter
- ✅ **Mapas Integrados** - Ubicación automática en Google Maps
- ✅ **Reportes y Estadísticas** - Análisis completo del sistema
- ✅ **Sistema de Logs** - Registro detallado de todas las actividades

## 🏗️ Arquitectura del Sistema

```
Sistema de Emergencias/
├── main.py                          # Archivo principal
├── installer.py                     # Instalador automático
├── requirements.txt                 # Dependencias
├── README.md                        # Esta documentación
├── 
├── database/
│   ├── __init__.py
│   └── db_manager.py               # Gestor de base de datos SQLite
├── 
├── gui/
│   ├── __init__.py
│   ├── login_window.py             # Ventana de login
│   ├── main_window.py              # Ventana principal/dashboard
│   ├── nueva_llamada_window.py     # Registro de nuevas llamadas
│   ├── consulta_llamadas_window.py # Consulta y búsqueda
│   ├── gestion_moviles_window.py   # Gestión de móviles
│   ├── gestion_usuarios_window.py  # Gestión de usuarios
│   ├── configuracion_window.py     # Configuración del sistema
│   ├── estadisticas_window.py      # Estadísticas y reportes
│   ├── triaje_medico_window.py     # Triaje médico DEMVA/CEC
│   ├── triaje_bomberos_window.py   # Triaje bomberos
│   ├── triaje_defensa_civil_window.py # Triaje defensa civil
│   └── triaje_seguridad_window.py  # Triaje seguridad ciudadana
├── 
├── utils/
│   ├── __init__.py
│   ├── config.py                   # Gestión de configuración
│   ├── logger.py                   # Sistema de logging
│   └── whatsapp_manager.py         # Integración WhatsApp API
├── 
├── data/
│   ├── emergencias.db              # Base de datos principal
│   └── config.json                 # Archivo de configuración
├── 
├── logs/                           # Archivos de log del sistema
├── exports/                        # Archivos exportados
├── backups/                        # Respaldos automáticos
└── docs/                          # Documentación adicional
```

## 🚀 Instalación Rápida

### Requisitos Previos

- **Python 3.8+** (recomendado Python 3.10+)
- **Conexión a Internet** (para instalación de dependencias)
- **Windows 10/11** o **Linux Ubuntu 20.04+** o **macOS 10.15+**

### Instalación Automática

1. **Descargar** el proyecto completo
2. **Ejecutar** el instalador:

```bash
# Windows
python installer.py

# Linux/macOS
python3 installer.py
```

3. **Seguir** las instrucciones del instalador
4. **Iniciar** el sistema con el script generado

### Instalación Manual

Si prefiere instalar manualmente:

```bash
# 1. Crear entorno virtual (recomendado)
python -m venv venv

# 2. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar sistema
python main.py
```

## 🎯 Inicio Rápido

### Primera Ejecución

1. **Ejecutar** `python main.py` o usar el script de inicio
2. **Login** con credenciales por defecto:
   - Usuario: `admin`
   - Contraseña: `admin123` (o la que configuró en instalación)
3. **Configurar** números de WhatsApp en Configuración → WhatsApp
4. **Crear** usuarios adicionales en Gestión de Usuarios
5. **Configurar** móviles en Gestión de Móviles

### Flujo Básico de Uso

1. **Nueva Llamada** → Completar datos del solicitante
2. **Seleccionar Tipo** de emergencia
3. **Realizar Triaje** según protocolo correspondiente
4. **Despachar Móvil** si es necesario
5. **Seguimiento** hasta cierre de la llamada

## 📋 Tipos de Emergencia y Triaje

### 🚑 Emergencias Médicas

**Protocolos DEMVA:**
- Estado de consciencia del paciente
- Signos vitales (respiración, pulso)
- Presencia de sangrado
- Dolor torácico
- Antecedentes médicos
- **Destino:** DEMVA o CEC según criterio

### 🚒 Bomberos

**Evaluación de Incendios:**
- Tipo de incendio (domicilio/vía pública/vehículo)
- Personas atrapadas
- Extensión aproximada
- Materiales involucrados
- Presencia de explosivos/químicos
- Condiciones climáticas

### 🏗️ Defensa Civil

**Emergencias Climáticas/Desastres:**
- Tipo de evento
- Personas afectadas/evacuadas
- Daños estructurales
- Servicios públicos afectados
- Necesidad de evacuación
- Coordinación con otros organismos

### 👮 Seguridad Ciudadana

**Incidentes de Seguridad:**
- Tipo de incidente
- Presencia de heridos
- Agresor presente/armado
- Vehículos involucrados
- Testigos presentes
- Necesidad de ambulancia/bomberos

### 📞 Llamadas Generales

- Consultas y trámites no urgentes
- Solo observaciones, sin triaje

## 🔧 Configuración del Sistema

### Configuración de WhatsApp

La integración con WhatsApp utiliza la API de Nubelix:

```
URL API: https://bot.nubelix.com/wabot/50aa4db2d5d872b6878edfe7755f194d
Token: e0072338d75f46d992f0430ffea2d154
```

**Configurar números de destino:**
- DEMVA: Emergencias médicas Villa Allende
- CEC: Centro de Emergencias Coordinado
- Bomberos: Cuerpo de Bomberos
- Defensa Civil: Defensa Civil Municipal
- Seguridad: Seguridad Ciudadana

### Gestión de Usuarios

**Roles disponibles:**
- **Administrador:** Acceso completo al sistema
- **Supervisor:** Gestión de llamadas y reportes
- **Operador:** Registro de llamadas y triaje

### Gestión de Móviles

**Tipos de móviles:**
- **Ambulancia:** Para emergencias médicas
- **Patrulla:** Para seguridad ciudadana
- **Rescate:** Para defensa civil y bomberos

**Estados:**
- Disponible
- Ocupado
- Fuera de servicio
- En mantenimiento

## 📊 Base de Datos

### Estructura Principal

**Tablas principales:**
- `llamadas` - Registro de todas las llamadas
- `vecinos` - Datos de solicitantes
- `usuarios` - Usuarios del sistema
- `moviles` - Vehículos de emergencia
- `tipos_emergencia` - Tipos de emergencia
- `barrios` - Barrios de Villa Allende

**Tablas de triaje:**
- `triaje_medico` - Datos específicos médicos
- `triaje_bomberos` - Datos específicos bomberos
- `triaje_defensa_civil` - Datos específicos defensa civil
- `triaje_seguridad` - Datos específicos seguridad

**Tablas de configuración:**
- `config_whatsapp` - Números de WhatsApp
- `asignaciones_personal` - Personal asignado a móviles
- `novedades` - Seguimiento de llamadas
- `logs_sistema` - Registro de actividades

### Backup y Restauración

- **Backup automático** cada 24 horas
- **Backup manual** desde Configuración → Backup
- **Exportación** a Excel desde múltiples ventanas
- **Restauración** desde archivo de backup

## 🔐 Seguridad

### Autenticación
- Contraseñas hasheadas con SHA-256
- Control de intentos de login
- Timeout de sesión configurable
- Roles y permisos diferenciados

### Logging
- Registro de todas las acciones de usuarios
- Logs de sistema rotativos
- Logs de emergencias específicos
- Logs de errores detallados

### Datos Sensibles
- Cifrado de configuración WhatsApp
- Backup seguro de base de datos
- Limpieza automática de logs antiguos

## 📈 Reportes y Estadísticas

### Dashboard Principal
- Llamadas activas en tiempo real
- Móviles disponibles
- Estadísticas del día
- Gráficos de tendencias

### Reportes Disponibles
- **Diario:** Actividad del día
- **Semanal:** Resumen semanal
- **Mensual:** Estadísticas mensuales
- **Por tipo:** Análisis por tipo de emergencia
- **Personalizado:** Filtros específicos

### Exportación
- Excel (.xlsx)
- CSV para análisis
- PDF para reportes oficiales
- Impresión directa

## 🗺️ Integración con Mapas

### Google Maps
- Ubicación automática de direcciones
- Apertura directa en navegador
- Coordenadas GPS opcionales
- Visualización de ubicaciones de llamadas

## 📱 Integración WhatsApp

### Funcionalidades
- Envío automático de alertas
- Verificación de estado de conexión
- Mensajes de prueba
- Configuración por tipo de emergencia

### Formato de Mensajes
```
🚨 ALERTA DE EMERGENCIA 🚨

📋 Llamada: EM20241201123456
🚨 Tipo: Emergencia Médica
📍 Dirección: Calle Ejemplo 123, Villa Allende
👤 Solicitante: Juan Pérez
📞 Teléfono: 3516789012
📝 Descripción: Dolor de pecho intenso

⏰ Hora: 01/12/2024 12:34:56
🏥 Sistema de Emergencias Villa Allende
```

## 🛠️ Desarrollo y Mantenimiento

### Tecnologías Utilizadas
- **Python 3.8+**
- **CustomTkinter** - Interfaz gráfica moderna
- **SQLite** - Base de datos
- **Requests** - API WhatsApp
- **Pandas** - Exportación Excel
- **Matplotlib** - Gráficos estadísticos

### Estructura del Código
- **Modular:** Cada ventana es un módulo independiente
- **MVC:** Separación de lógica y presentación
- **Documentado:** Código ampliamente comentado
- **Mantenible:** Estructura clara y organizada

### Extensibilidad
- Nuevos tipos de emergencia
- Módulos de triaje adicionales
- Integraciones con otros sistemas
- Reportes personalizados

## 🐛 Solución de Problemas

### Problemas Comunes

**Error de importación de CustomTkinter:**
```bash
pip install customtkinter --upgrade
```

**Error de conexión WhatsApp:**
- Verificar conexión a internet
- Comprobar credenciales API
- Revisar formato de números

**Base de datos bloqueada:**
- Cerrar todas las instancias del programa
- Verificar permisos de archivos
- Ejecutar como administrador si es necesario

**Problemas de permisos:**
```bash
# Linux/macOS
chmod +x iniciar_sistema.sh
```

### Logs de Error
Revisar archivos en directorio `logs/`:
- `app_YYYYMMDD.log` - Log general
- `errors_YYYYMMDD.log` - Solo errores
- `emergency_YYYYMMDD.log` - Eventos de emergencia

## 📞 Soporte

### Contacto Técnico
- **Desarrollador:** Sistema de Emergencias Team
- **Email:** soporte@emergenciasvallende.gov.ar
- **Teléfono:** 3543-498000

### Documentación Adicional
- Manual de Usuario (PDF)
- Manual Técnico (PDF)
- Videos tutoriales
- FAQ en línea

## 🔄 Actualizaciones

### Versión Actual: 1.0.0

**Próximas funcionalidades:**
- [ ] Integración con sistemas externos
- [ ] App móvil para operadores
- [ ] API REST para terceros
- [ ] Dashboards en tiempo real
- [ ] Reportes automáticos por email
- [ ] Integración con GPS de móviles

### Historial de Versiones

**v1.0.0** (2024-12-01)
- ✅ Versión inicial completa
- ✅ Todos los módulos implementados
- ✅ Triaje para 4 tipos de emergencia
- ✅ Integración WhatsApp funcional
- ✅ Sistema de reportes básico

## 📜 Licencia

Este software ha sido desarrollado específicamente para la Municipalidad de Villa Allende, Córdoba, Argentina.

**Derechos de uso:**
- Uso exclusivo municipal
- Modificaciones permitidas
- Redistribución restringida
- Soporte técnico incluido

---

## 🎉 ¡Gracias por usar el Sistema de Emergencias Villa Allende!

Para más información, consulte la documentación completa o contacte al equipo de soporte técnico.

**¡Su dedicación salva vidas! 🚨👨‍⚕️👩‍🚒👮‍♂️**
