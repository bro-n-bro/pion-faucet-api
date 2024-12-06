from sqlalchemy import Column, Integer, String, Float

from app.common.base_class import Base


class TelegramAccount(Base):
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
