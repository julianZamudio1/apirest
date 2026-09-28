# API REST de Tareas · FastAPI + MongoDB

API REST asíncrona para gestionar tareas, con registro e inicio de sesión de usuarios mediante **JWT**, contraseñas cifradas con **bcrypt** y documentación interactiva generada automáticamente con **Swagger / OpenAPI**.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Motor-47A248?logo=mongodb&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)

## Características

- CRUD completo de tareas (crear, listar, consultar por ID, actualizar y eliminar)
- Registro de usuarios con validación de correo (`EmailStr`) y contraseña cifrada con bcrypt
- Login que devuelve un token **JWT Bearer** con expiración configurable
- Endpoint de creación de tareas protegido con `OAuth2PasswordBearer`
- Acceso asíncrono a MongoDB con **Motor**
- Validación de datos y modelos de respuesta con **Pydantic v2**
- Verificación de la conexión a la base de datos al iniciar la app (`lifespan`)
- Manejo de errores HTTP: `400` (ID inválido), `401` (credenciales), `404` (no encontrado)

## Stack

| Capa | Tecnología |
|---|---|
| Framework | FastAPI, Uvicorn |
| Base de datos | MongoDB (driver asíncrono Motor) |
| Validación | Pydantic v2 |
| Seguridad | python-jose (JWT), passlib + bcrypt |
| Configuración | python-dotenv |

## Estructura

```
app/
├── main.py            # Punto de entrada, lifespan y registro de routers
├── db/
│   ├── mongodb.py     # Cliente Motor y colecciones (users, tasks)
│   ├── auth.py        # Hash de contraseñas, creación y validación de JWT
│   └── utils.py       # Conversión de ObjectId a string
├── routes/
│   ├── users.py       # /auth/register, /auth/login
│   └── tasks.py       # /tasks CRUD
└── schemas/
    ├── user.py        # Modelos Pydantic de usuario
    └── task.py        # Modelos Pydantic de tarea
```

## Endpoints

| Método | Ruta | Descripción | Auth |
|---|---|---|---|
| `GET` | `/` | Estado de la API | — |
| `POST` | `/auth/register` | Registrar usuario | — |
| `POST` | `/auth/login` | Iniciar sesión y obtener JWT | — |
| `POST` | `/tasks/` | Crear tarea | Bearer |
| `GET` | `/tasks/` | Listar tareas | — |
| `GET` | `/tasks/{task_id}` | Obtener tarea por ID | — |
| `PUT` | `/tasks/{task_id}` | Actualizar tarea | — |
| `DELETE` | `/tasks/{task_id}` | Eliminar tarea | — |

## Instalación y ejecución

**Requisitos:** Python 3.11+ y una instancia de MongoDB (local o MongoDB Atlas).

```bash
git clone https://github.com/julianZamudio1/apirest.git
cd apirest
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz:

```env
MONGO_URL=mongodb://localhost:27017
SECRET_KEY=cambia_esta_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Inicia el servidor:

```bash
uvicorn app.main:app --reload
```

La documentación interactiva queda disponible en:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Ejemplo de uso

```bash
# 1. Registrar usuario
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@correo.com", "password": "123456"}'

# 2. Iniciar sesión
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@correo.com", "password": "123456"}'
# → {"access_token": "<TOKEN>", "token_type": "bearer"}

# 3. Crear una tarea con el token
curl -X POST http://127.0.0.1:8000/tasks/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Entregar reporte", "description": "Unidad 3", "completed": false}'
```

## Autor

**Eduardo Julián Zamudio Govea** · Ingeniería en Sistemas Computacionales, ITLP
[github.com/julianZamudio1](https://github.com/julianZamudio1)
