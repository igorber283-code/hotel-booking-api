from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    rooms_count: Mapped[int] = mapped_column(nullable=False)
