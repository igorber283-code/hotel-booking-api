import re
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=64,  # Хорошая практика — ограничить сверху от DoS-атак длинными строками
        description="Пароль должен быть от 8 до 64 символов",
    )

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        if not re.search(r"\d", value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[a-zA-Z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну английскую букву")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    # Для логина жесткие проверки убираем, оставляем только минимальную защиту
    password: str = Field(min_length=1, description="Пароль не может быть пустым")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
