import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

#leer la URL desde el .env
MONGO_URL = os.getenv("MONGO_URL")
print(f"URL de MongoDB: {MONGO_URL}")
client = AsyncIOMotorClient(MONGO_URL)

#seleccionar la base de datos y la colección
db = client.tareas_db
users_collection = db.get_collection("users")
tasks_collection = db.get_collection("tasks")

async def test_conection():
    try:
        # Intentar obtener la lista de bases de datos para verificar la conexión
        await client.admin.command('ping')
        print("Conexión a MongoDB exitosa")
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")