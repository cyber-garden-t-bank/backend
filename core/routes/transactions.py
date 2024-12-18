from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.jwt.jwt import decode_access_token, oauth2_scheme, SUB
from core.lib.generic import list_view, create_view, get_view
from core.lib.schemas.transactions import TransactionView, TransactionCreateView
from db.database import get_db
from db.models.transactions import Transaction, IncomeTransaction

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)



@router.get("/list")
async def get_transactions( token: Annotated[str, Depends(oauth2_scheme)],db: AsyncSession = Depends(get_db)) -> list[TransactionView]:
    token_data = await decode_access_token(token=token, db=db)
    expr = (Transaction.transaction_user == token_data[SUB])
    return await list_view(Transaction, TransactionView, db)

@router.post("/create")
async def create_transaction(wallet: TransactionCreateView, db: AsyncSession = Depends(get_db)) -> TransactionView:
    return await create_view(Transaction, wallet, TransactionView, db)


@router.get("/detail/{transaction_uuid}")
async def get_transaction(transaction_uuid: str, db: AsyncSession = Depends(get_db)) -> TransactionView:
    expr = (Transaction.transaction_uuid == transaction_uuid)
    return await get_view(Transaction, TransactionView, db, by_expr= expr)





@router.get("/income/{transaction_uuid}")
async def get_income_transaction(transaction_uuid: str, db: AsyncSession = Depends(get_db)) -> TransactionView:
    expr = (IncomeTransaction.transaction_uuid == transaction_uuid)
    return await get_view(Transaction, TransactionView, db, by_expr= expr)


