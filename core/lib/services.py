
import logging



from sqlalchemy.ext.asyncio import AsyncSession



logger = logging.getLogger(__name__)



async def first_func(db: AsyncSession):
    logger.debug("lol")
    return None
    #
