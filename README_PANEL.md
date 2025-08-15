# Panel Central - Hub de APIs

## Descripción

Panel centralizado que integra múltiples APIs bajo un sistema de autenticación unificado. El proyecto incluye:

- **Panel Central**: Hub principal con autenticación OAuth2/JWT
- **API Sergio**: Gestión de partidos de fútbol (Gallos Querétaro)
- **API Andrea**: Gestión de eventos culturales
- **API Inventario**: Sistema CRUD para gestión de productos
- **Integración Externa**: API de clima (OpenWeatherMap)

## Arquitectura

```
Panel Central (Puerto 8000)
├── Backend (FastAPI + SQLAlchemy)
├── Frontend (HTML + Bootstrap + JavaScript)
├── Autenticación (OAuth2 + JWT)
└── Proxy a APIs existentes

APIs Integradas:
├── API Sergio (Puerto 8001)
├── API Andrea (Puerto 8002)
└── APIs Externas (OpenWeatherMap)
```

## Características

### Seguridad
- ✅ Autenticación OAuth2 con tokens JWT
- ✅ Registro y login de usuarios
- ✅ Protección de rutas con middleware
- ✅ Validación de tokens en cada petición

### APIs Integradas
- ✅ **API Sergio**: Partidos de fútbol con geolocalización
- ✅ **API Andrea**: Eventos culturales con información detallada
- ✅ **API Inventario**: CRUD completo para productos
- ✅ **API Externa**: Integración con OpenWeatherMap

### Frontend
- ✅ Dashboard responsivo con Bootstrap 5
- ✅ Interfaz intuitiva para gestión de datos
- ✅ Tablas dinámicas para visualización
- ✅ Formularios para operaciones CRUD
- ✅ Notificaciones y alertas

### Comunicación
- ✅ Proxy transparente a APIs existentes
- ✅ Manejo de promesas con async/await
- ✅ Comunicación entre APIs fluida
- ✅ CORS configurado correctamente

## Instalación

### Prerrequisitos
- Python 3.8+
- pip
- PowerShell (Windows)

### Instalación Automática

1. **Clonar/Descargar el proyecto**
2. **Ejecutar el script de instalación:**
   ```powershell
   .\install_dependencies.ps1
   ```

### Instalación Manual

Si prefieres instalar manualmente:

```bash
# Panel Central
cd panel_central/backend
pip install -r requirements.txt

# API Sergio
cd ../../apis/sergio  
pip install -r requirements.txt

# API Andrea
cd ../andrea
pip install -r requirements.txt
```

## Ejecución

### Inicio Automático (Recomendado)

```powershell
.\start_all_apis.ps1
```

Este script iniciará automáticamente:
- Panel Central en puerto 8000
- API Sergio en puerto 8001  
- API Andrea en puerto 8002

### Inicio Manual

Si prefieres iniciar cada servicio por separado:

```bash
# Terminal 1 - Panel Central
cd panel_central/backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2 - API Sergio  
cd apis/sergio
python -m uvicorn main:app --reload --port 8001

# Terminal 3 - API Andrea
cd apis/andrea
python -m uvicorn main:app --reload --port 8002
```

## Uso

### Acceso al Sistema

1. **Abrir navegador**: http://localhost:8000
2. **Registro**: Crear una cuenta nueva
3. **Login**: Iniciar sesión con credenciales
4. **Dashboard**: Acceder al panel de control

### Funcionalidades Disponibles

#### 1. Resumen del Sistema
- Estado de todas las APIs
- Estadísticas generales
- Información del usuario

#### 2. Gestión de Inventario (API Nueva)
- ➕ Agregar productos
- 👁️ Visualizar inventario
- ✏️ Editar productos
- 🗑️ Eliminar productos

#### 3. Partidos de Fútbol (API Sergio)
- 📋 Listar todos los partidos
- 🌍 Geolocalización de estadios
- 📊 Resultados y estadísticas

#### 4. Eventos Culturales (API Andrea)
- 🎭 Gestión de eventos
- 📍 Información de ubicaciones
- 💰 Control de precios y aforos

#### 5. Información Meteorológica
- ☀️ Consulta de clima por ciudad
- 🌡️ Temperatura, humedad, presión
- 🔄 Actualización en tiempo real

## Estructura del Proyecto

```
API Panel/
├── panel_central/
│   └── backend/
│       ├── main.py              # Aplicación principal
│       ├── models.py            # Modelos de BD
│       ├── schemas.py           # Esquemas Pydantic
│       ├── crud.py              # Operaciones CRUD
│       ├── database.py          # Configuración BD
│       ├── requirements.txt     # Dependencias
│       └── static/             # Frontend
│           ├── index.html      # Página principal
│           ├── login.html      # Página de login
│           ├── dashboard.html  # Dashboard
│           └── dashboard.js    # Lógica frontend
├── apis/
│   ├── sergio/                 # API Partidos
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── crud.py
│   │   └── ...
│   └── andrea/                 # API Eventos
│       ├── main.py
│       ├── models.py
│       ├── crud.py
│       └── ...
├── login/                      # Sistema login PHP (opcional)
├── install_dependencies.ps1    # Script instalación
├── start_all_apis.ps1          # Script inicio
└── README.md
```

## APIs y Endpoints

### Panel Central (Puerto 8000)

#### Autenticación
- `POST /register` - Registro de usuarios
- `POST /token` - Login (obtener token)
- `GET /users/me` - Información del usuario actual

#### Inventario
- `GET /inventario/productos` - Listar productos
- `POST /inventario/productos` - Crear producto
- `GET /inventario/productos/{id}` - Obtener producto
- `PUT /inventario/productos/{id}` - Actualizar producto
- `DELETE /inventario/productos/{id}` - Eliminar producto

#### Proxy APIs
- `GET /api/sergio/*` - Proxy a API Sergio
- `POST /api/sergio/*` - Proxy a API Sergio
- `DELETE /api/sergio/*` - Proxy a API Sergio
- `GET /api/andrea/*` - Proxy a API Andrea
- `POST /api/andrea/*` - Proxy a API Andrea
- `DELETE /api/andrea/*` - Proxy a API Andrea

#### Externa
- `GET /weather/{city}` - Información del clima

### API Sergio (Puerto 8001)
- `GET /partidos/` - Listar partidos
- `POST /partidos/` - Crear partido
- `GET /partidos/{id}` - Obtener partido
- `GET /partidos/{id}/estadio` - Coordenadas del estadio
- `DELETE /partidos/{id}` - Eliminar partido

### API Andrea (Puerto 8002)
- `GET /eventos/` - Listar eventos
- `POST /eventos/` - Crear evento
- `GET /eventos/{id}` - Obtener evento
- `GET /eventos/{id}/coordenadas` - Coordenadas del evento
- `DELETE /eventos/{id}` - Eliminar evento

## Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos ligera
- **Pydantic**: Validación de datos
- **PassLib**: Hashing de contraseñas
- **Jose**: Manejo de tokens JWT
- **Httpx**: Cliente HTTP asíncrono

### Frontend
- **HTML5**: Estructura de páginas
- **Bootstrap 5**: Framework CSS responsivo
- **JavaScript ES6+**: Lógica del frontend
- **Font Awesome**: Iconografía

### Integración
- **CORS**: Comunicación entre orígenes
- **OAuth2**: Estándar de autenticación
- **JWT**: Tokens de acceso seguros

## Seguridad

### Medidas Implementadas
1. **Autenticación obligatoria** para todas las operaciones
2. **Tokens JWT** con expiración automática
3. **Hashing seguro** de contraseñas con bcrypt
4. **CORS configurado** correctamente
5. **Validación de datos** en backend y frontend

### Configuración de Producción
Para usar en producción, actualizar:
- `SECRET_KEY` en `main.py`
- URLs de CORS para dominios específicos
- Configuración de base de datos (PostgreSQL/MySQL)
- Variables de entorno para APIs externas

## Troubleshooting

### Problemas Comunes

1. **Puerto ocupado**: Cambiar puertos en los scripts
2. **CORS Error**: Verificar configuración de CORS
3. **Token expirado**: Hacer logout y login nuevamente
4. **API no responde**: Verificar que todas las APIs estén ejecutándose

### Logs y Debug
- FastAPI automáticamente muestra logs en consola
- Documentación interactiva disponible en `/docs`
- Usar herramientas de desarrollo del navegador

## Contribución

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para nueva característica
3. Implementar cambios
4. Ejecutar tests
5. Crear Pull Request

## Licencia

Proyecto desarrollado para fines educativos. Libre uso y modificación.

---

**Desarrollado con ❤️ por el equipo de desarrollo**
