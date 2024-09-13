from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from src.auth import schemas, auth, utils, models
from src.config import settings

auth_router = APIRouter()

@auth_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(auth.get_db)):
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = utils.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/register", response_model=schemas.User)
async def register_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(auth.get_db)):
    user = await auth.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    user_data = user_in.dict()
    user_data.pop("password")
    user_in_db = models.User(**user_data, password_hash=utils.get_password_hash(user_in.password))
    db.add(user_in_db)
    await db.commit()
    await db.refresh(user_in_db)
    return user_in_db

@auth_router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Successfully logged out"}
