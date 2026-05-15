from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users import UserRegister, UserLogin
from app.core.database import get_session
from app.services.users import UserService

router = APIRouter(prefix="/authx", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, session: AsyncSession = Depends(get_session)):
    await UserService.register_user(session, user.email, user.password)
    return {"message": "Вы успешно зарегистрированы"}


@router.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    token = await UserService.login_user(session, user.email, user.password)
    return {"access_token": token}
