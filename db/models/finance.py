import random
import uuid
from datetime import datetime, date, timedelta

from sqlalchemy import DECIMAL, String, ForeignKey, Date, func
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.lib.mixins import TimeMixin
from db.lib.types import pk_id


def generate_random_card_number():
    card_number = [random.randint(0, 9) for _ in range(15)]

    def luhn_checksum(card_number):
        for i in range(len(card_number) - 2, -1, -2):
            card_number[i] *= 2
            if card_number[i] > 9:
                card_number[i] -= 9
        return sum(card_number) % 10

    checksum_digit = (10 - luhn_checksum(card_number + [0])) % 10
    card_number.append(checksum_digit)

    return ''.join(map(str, card_number))


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
    card_number: Mapped[str] = mapped_column(String(255),default=generate_random_card_number, unique=True)
    wallet_number = mapped_column(ForeignKey("wallet.wallet_number"))
    balance: Mapped[float] = mapped_column(DECIMAL, default=0.0)
    card_type: Mapped[str] = mapped_column(String(255))
    expiration_date: Mapped[date] = mapped_column(Date, default=lambda: date.today() + timedelta(days=3*365), server_default=func.current_date() + func.interval('3 years'))

