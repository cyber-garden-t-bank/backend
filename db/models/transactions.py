import enum

from sqlalchemy import DECIMAL, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.lib.mixins import TimeMixin
from db.lib.types import pk_id


class IncomeTransactionCategory(str, enum.Enum):
    salary = "salary"
    gift = "gift"
    grant = "grant"


class TransactionType(str, enum.Enum):
    internal = "internal"
    external = "external"


class Transaction(Base, TimeMixin):
    __tablename__ = "transaction"
    transaction_uuid: Mapped[pk_id]
    transaction_card_target: Mapped[str] = mapped_column(ForeignKey("card.card_number"))
    transaction_source_card: Mapped[str] = mapped_column(ForeignKey("card.card_number"))
    amount: Mapped[float] = mapped_column(DECIMAL, default=0.0)
    transaction_type: Mapped[TransactionType] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(255), default="undefined")

    __table_args__ = (
        CheckConstraint("amount > 0"),
    )

class IncomeTransaction(Base, TimeMixin):
    __tablename__ = "income_transaction"
    transaction_uuid: Mapped[pk_id]
    category: Mapped[IncomeTransactionCategory] = mapped_column(String(255))
    target_card: Mapped[str] = mapped_column(ForeignKey("card.card_number"))
    amount: Mapped[float] = mapped_column(DECIMAL, default=0.0)