import uuid
from datetime import datetime, date, timedelta

from sqlalchemy import DECIMAL, String, ForeignKey, Date, func
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.lib.mixins import TimeMixin
from db.lib.types import pk_id

def expiration_date(diff):
    return datetime.now() + diff


class Wallet(Base, TimeMixin):
    __tablename__ = "wallet"
    wallet_uuid: Mapped[pk_id]
    wallet_number: Mapped[str] = mapped_column(String(255), unique=True)
    user_uuid:Mapped[uuid.UUID]
    balance: Mapped[float] = mapped_column(DECIMAL, default=0.0)
    wallet_type: Mapped[str] = mapped_column(String(255))

class Card(Base, TimeMixin):
    __tablename__ = "card"
    card_uuid: Mapped[pk_id]
    card_number: Mapped[str] = mapped_column(String(255), unique=True)
    wallet_number = mapped_column(ForeignKey("wallet.wallet_number"))
    balance: Mapped[float] = mapped_column(DECIMAL, default=0.0)
    card_type: Mapped[str] = mapped_column(String(255))
    expiration_date: Mapped[date] = mapped_column(Date, default=lambda: date.today() + timedelta(days=3*365),server_default=func.current_date() + func.interval('3 years'))

