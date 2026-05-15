from authx import AuthX, AuthXConfig
from passlib.context import CryptContext

from app.core.config import settings


config = AuthXConfig()
config.JWT_ALGORITHM = settings.ALGORITHM
config.JWT_SECRET_KEY = settings.SECRET_KEY
config.JWT_TOKEN_LOCATION = ["headers"]

security = AuthX(config=config)


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
