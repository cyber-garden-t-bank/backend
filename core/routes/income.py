import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.lib.generic import create_view, get_view, list_view
from db.database import get_db
from core.lib.schemas.income import IncomeBillView, IncomeTransactionView
from db.models.transactions import IncomeTransaction

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/deprecated/income",
    tags=["deprecated"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def add_income(income_transaction: IncomeTransactionView, db: AsyncSession = Depends(get_db))->IncomeBillView:
    return await create_view( IncomeTransaction, income_transaction, IncomeBillView, db)

@router.get("/detail/{transaction_uuid}")
async def get_income(transaction_uuid: str, db: AsyncSession = Depends(get_db)) -> IncomeBillView:
    expr = (IncomeTransaction.transaction_uuid == transaction_uuid)
    return await get_view(IncomeTransaction, IncomeBillView, db, by_expr=expr)

@router.get("/list")
async def get_incomes(db: AsyncSession = Depends(get_db)) -> list[IncomeBillView]:
    return await list_view(IncomeTransaction, IncomeBillView, db)


