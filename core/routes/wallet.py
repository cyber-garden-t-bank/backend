from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.lib.generic import list_view, create_view, get_view
from core.lib.schemas.wallet import WalletView, WalletCreateView
from db.database import get_db
from db.models.finance import Wallet

router = APIRouter(
    prefix="/wallet",
    tags=["wallets"],
    responses={404: {"description": "Not found"}},
)



@router.get("/list")
async def get_wallets(db: AsyncSession = Depends(get_db)) -> list[WalletView]:
    return await list_view(Wallet, WalletView, db)

@router.post("/create")
async def create_wallet(wallet: WalletCreateView, db: AsyncSession = Depends(get_db)) -> WalletView:
    return await create_view(Wallet, wallet, WalletView, db)


@router.get("/detail/{wallet_number}")
async def get_wallet(wallet_number: str, db: AsyncSession = Depends(get_db)) -> WalletView:
    expr = (Wallet.wallet_number == wallet_number)
    return await get_view(Wallet, WalletView, db, by_expr= expr)