from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from src.auth import schemas, auth, utils, models
from src.config import settings
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_router = APIRouter()

@auth_router.post("/register", response_model=schemas.User, tags=["Авторизация"])
async def register_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(auth.get_db)):
    user = await auth.get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_data = user_in.dict()
    user_data.pop("password")
    user_in_db = models.User(**user_data, password_hash=utils.get_password_hash(user_in.password))
    db.add(user_in_db)
    await db.commit()
    await db.refresh(user_in_db)
    return user_in_db


@auth_router.post("/login", tags=["Авторизация"])
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: AsyncSession = Depends(auth.get_db)):
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.error(f"Invalid login attempt for user {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    logger.info(f"User {user.email} authenticated successfully.")
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = utils.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    logger.info(f"Token set in cookie for user {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}



@auth_router.get("/users/me/", response_model=schemas.User, tags=["Авторизация"])
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

@auth_router.post("/logout", tags=["Авторизация"])
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}

@auth_router.patch("/assign-role", tags=["Авторизация"])
async def assign_role(email: str, role: str, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(auth.get_db)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to assign roles")
    user = await auth.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    await db.commit()
    return {"message": f"Role {role} assigned to user {email}"}