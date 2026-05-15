from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.users import UserDAO
from app.core.security import get_password_hash, verify_password, security
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException


class UserService:
    @classmethod
    async def register_user(cls, session: AsyncSession, email: str, password: str):

        user = await UserDAO.find_one_or_none(session, email=email)
        if user:
            raise UserAlreadyExistsException()

        hashed_password = get_password_hash(password)

        await UserDAO.add(
            session,
            email=email,
            hashed_password=hashed_password,
        )

        await session.commit()

    @classmethod
    async def login_user(cls, session: AsyncSession, email: str, password: str) -> str:

        user = await UserDAO.find_one_or_none(session, email=email)

        if not user or not verify_password(password, str(user.hashed_password)):
            raise IncorrectEmailOrPasswordException()

        return security.create_access_token(uid=str(user.id))
