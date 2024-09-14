import logging
from fastapi import Request, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_403_FORBIDDEN
from src.database import async_session
from src.auth import models, schemas, utils
from src.config import settings

import bcrypt




# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_db():
    async with async_session() as session:
        yield session


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id_user == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        logger.error(f"Пользователь с электронной почтой {email} не найден.")
        return False
    if not verify_password(password, user.password_hash):
        logger.error(f"Не удалось проверить пароль для пользователя {email}.")
        return False
    return user


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        logger.error("No token found in cookies.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    # Убираем Bearer из токена
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    logger.info(f"Received token after stripping Bearer: {token}")

    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )

    try:
        # Проверка на наличие трех сегментов
        if token.count('.') != 2:
            logger.error("Token does not have exactly 3 segments.")
            raise credentials_exception

        # Попытка декодировать токен
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            logger.error("No email found in JWT payload.")
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError as e:
        logger.error(f"JWTError: {e}")
        raise credentials_exception

    user = await get_user_by_email(db, email=token_data.email)
    if user is None:
        logger.error(f"User with email {token_data.email} not found after token verification.")
        raise credentials_exception

    logger.info(f"User {user.email} authenticated successfully.")
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))