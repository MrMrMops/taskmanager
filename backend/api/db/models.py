import uuid
from datetime import datetime
from sqlalchemy import BigInteger, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from api.db.database import Base


class Task(Base):
    """
    Модель для хранения информации о задачах.
    """
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True,autoincrement=True, index=True, doc="Уникальный идентификатор задачи."
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False, doc="Краткое название задачи (максимум 255 символов)."
    )
    text: Mapped[str] = mapped_column(
        Text, nullable=True, doc="Описание задачи. Может быть пустым."
    )
    image_url: Mapped[str] = mapped_column(
        String(2083), nullable=True, doc="URL изображения задачи (максимум 2083 символа)."
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=True, default=0, doc="Приоритет задачи. Чем выше число, тем важнее задача."
    )
    due_date: Mapped[datetime] = mapped_column(
        nullable=True, index=True, doc="Дата завершения задачи. Может быть пустой."
    )
    created_date: Mapped[datetime] = mapped_column(
        default=datetime.now(), nullable=False, doc="Дата создания задачи. Устанавливается автоматически."
    )
    updated_date: Mapped[datetime] = mapped_column(
        default=datetime.now(), onupdate=datetime.now(), nullable=False,
        doc="Дата последнего обновления задачи. Обновляется автоматически."
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта для отладки.
        """
        return f"<Task(id={self.id}, title={self.title}, priority={self.priority})>"


class User(Base):
    """
    Модель для хранения данных пользователей.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, index=True, doc="Уникальный идентификатор пользователя."
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, doc="Имя пользователя. Максимум 100 символов."
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=True, unique=True, doc="Email пользователя. Должен быть уникальным."
    )
    created_date: Mapped[datetime] = mapped_column(
        default=datetime.now(), nullable=False, doc="Дата создания аккаунта. Устанавливается автоматически."
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        """
        Строковое представление объекта для отладки.
        """
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"