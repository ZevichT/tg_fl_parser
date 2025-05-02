from sqlalchemy import select

from .database import new_session, OffersORM


class OfferRepository:
    @classmethod
    async def get_offers(cls) -> list:
        async with new_session as session:
            query = select(OffersORM)
            result = await session.execute(query)
            offers = result.scalars().all()
            offers_list = [dict(offer.__dict__) for offer in offers]
            for i in range(len(offers_list)):
                offers_list[i].pop('_sa_instance_state')
            return offers_list

    @classmethod
    async def add_offer(cls, offer: dict) -> None:
        async with new_session as session:
            offer = OffersORM(**offer)
            session.add(offer)
            await session.commit()
            await session.close()

