from fastapi import APIRouter, HTTPException, status
from app.db.mongodb import users_collection
from app.schemas.user import UserCreate, UserResponse
from app.db.auth import hash_password, verify_password, create_access_token
from app.db.utils import fix_id

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    # CORRECCIÓN: Usar user.email en lugar de user.username
    existing_user = await users_collection.find_one({"email": user.email})
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El correo electrónico ya está registrado"
        )
    
    user_dict = user.model_dump()
    # Usar el hash de la contraseña
    user_dict["password"] = hash_password(user.password)
    
    new_user = await users_collection.insert_one(user_dict)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    
    return fix_id(created_user)

@router.post("/login")
async def login(user_credentials: UserCreate):
    # CORRECCIÓN: Buscar por email usando user_credentials.email
    user = await users_collection.find_one({"email": user_credentials.email})
    
    if not user or not verify_password(user_credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales inválidas"
        )
    
    # Generar el token usando el email como identidad (sub)
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}