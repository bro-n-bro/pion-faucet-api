from typing import Optional

from pydantic import BaseModel


class TelegramAccountRequest(BaseModel):
    telegram_id: int
    address: str
