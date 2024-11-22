import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["core"],
    responses={404: {"description": "Not found"}},
)


