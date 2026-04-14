from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.mongodb import client
from app.routes import tasks
from app.routes import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await client.admin.command('ping')
        print("✅ Conexión a MongoDB exitosa")
        yield
    except Exception as e:
        print(f"❌ Error al conectar a MongoDB: {e}")
        yield
    finally:
        client.close()
        print("🔌 Conexión a MongoDB cerrada")

app = FastAPI(
    title="API REST con FastAPI y MongoDB",
    lifespan=lifespan
)

# Registra las rutas AQUÍ (después de definir app)
app.include_router(tasks.router)

@app.get("/", tags=["Inicio"])
async def root():
    return {"message": "¡Bienvenido a la API REST!", "database": "Conectada"}

app.include_router(users.router)