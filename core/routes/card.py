from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.lib.generic import list_view, get_view, create_view
from core.lib.schemas.card import CardView, CardCreateView
from db.database import get_db
from db.models.finance import Card

router = APIRouter(
    prefix="/card",
    tags=["cards"],
    responses={404: {"description": "Not found"}},
)


@router.get("/detail/{card_number}")
async def get_card(card_number: str, db: AsyncSession = Depends(get_db)) -> CardView:
    expr = (Card.card_number == card_number)
    return await get_view(Card, CardView, db, model_id=card_number, by_expr=expr)

@router.get("/list")
async def get_cards(db: AsyncSession = Depends(get_db)) -> list[CardView]:
    return await list_view(Card, CardView, db)

@router.post("/create")
async def create_card(card: CardCreateView, db: AsyncSession = Depends(get_db)) -> CardCreateView:
    return await create_view(Card, card, CardCreateView, db)