from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import uvicorn
from fastapi import FastAPI, Depends
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

from app.common.base import Base
from app.common.models import TelegramAccount
from app.common.schemas import TelegramAccountRequest
from app.common.service import send_rewards
from app.common.session import engine, get_db, sessionmaker_for_periodic_task
from config import EXCLUDED_ACCOUNTS


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI()
    create_tables()
    return app

app = start_application()


@app.post("/claim_rewards/")
def read_users(request: TelegramAccountRequest, db: Session = Depends(get_db)):

    if request.telegram_id not in EXCLUDED_ACCOUNTS:
        existing_account = db.execute(
            select(TelegramAccount).where(TelegramAccount.telegram_id == request.telegram_id)
        ).scalar_one_or_none()

        if existing_account:
            raise HTTPException(status_code=400, detail="Such telegram account already exists")
    result = send_rewards(request.address)
    if result:
        if request.telegram_id not in EXCLUDED_ACCOUNTS:
            new_account = TelegramAccount(telegram_id=request.telegram_id)
            db.add(new_account)
            db.commit()


        return {"telegram_id": request.telegram_id, "result": result}
    else:
        raise HTTPException(status_code=400, detail="Fail to send rewards")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
