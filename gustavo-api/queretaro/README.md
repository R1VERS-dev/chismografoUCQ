# 🌄 API de Lugares Turísticos de Querétaro

> Una API web construida con **FastAPI** y **Supabase** para consultar y administrar lugares turísticos en Querétaro, México.

---

## 🚀 Tecnologías Usadas

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square\&logo=python\&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square\&logo=fastapi\&logoColor=white)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square\&logo=postgresql\&logoColor=white)]()
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square\&logo=supabase\&logoColor=white)]()
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FF0000?style=flat-square\&logo=sqlalchemy\&logoColor=white)]()
[![Pydantic](https://img.shields.io/badge/Pydantic-00BFFF?style=flat-square\&logo=pydantic\&logoColor=white)]()

---

## 📂 Estructura del Proyecto

```bash
queretaro/
├── .env               # Variables de entorno (cadena de conexión a Supabase)
├── database.py        # Configuración del engine de SQLAlchemy
├── models.py          # Modelos de datos SQLAlchemy (tablas)
├── schemas.py         # Esquemas Pydantic (validación de datos)
├── crud.py            # Funciones CRUD para la base de datos
└── main.py            # Aplicación FastAPI y definición de endpoints
```

---

## ⚙️ Instalación y Ejecución

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu-usuario/queretaro-api.git
   cd queretaro-api
   ```

2. **Crear y activar entorno virtual**

   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   ```

3. **Instalar dependencias**

   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
   ```

4. **Configurar variables de entorno**
   Crea un archivo `.env` con el siguiente contenido:

   ```env
   DATABASE_URL=postgresql://postgres:TU_PASSWORD@db.obmtljdwxfyayiolixis.supabase.co:5432/postgres
   ```

5. **Ejecutar servidor**

   ```bash
   uvicorn main:app --reload
   ```

* **URL base:** `http://127.0.0.1:8000`
* **Documentación automática:** `http://127.0.0.1:8000/docs`

---

## 📌 Endpoints

| Método | Ruta            | Descripción                   |
| ------ | --------------- | ----------------------------- |
| GET    | `/lugares/`     | Obtener todos los lugares     |
| POST   | `/lugares/`     | Crear un nuevo lugar          |
| GET    | `/lugares/{id}` | Obtener un lugar por ID       |
| PUT    | `/lugares/{id}` | Actualizar un lugar existente |
| DELETE | `/lugares/{id}` | Eliminar un lugar por ID      |

---

## 🛠️ Descripción de Archivos

| Archivo         | Función                                                      |
| --------------- | ------------------------------------------------------------ |
| **.env**        | Variables de entorno (credenciales y URLs seguras)           |
| **database.py** | Inicializa el engine de SQLAlchemy con Supabase              |
| **models.py**   | Define la estructura de la tabla `lugares`                   |
| **schemas.py**  | Esquemas Pydantic para validación de datos                   |
| **crud.py**     | Funciones de “Create, Read, Update, Delete”                  |
| **main.py**     | Crea la app de FastAPI, registra rutas y arranca el servidor |

---



## 🧪 Pruebas

Puedes usar:

* **Postman**
* **FastAPI Swagger** (`/docs`)

---

## 📬 Contacto

Desarrollado por **Gustavo Ríos**