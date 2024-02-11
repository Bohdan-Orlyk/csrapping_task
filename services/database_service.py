import logging


class DbService:
    @staticmethod
    async def insert_data_to_db(session, offer_data: dict) -> None:
        try:
            stmt = (
                    f'INSERT INTO used_cars_offers ({", ".join(offer_data.keys())}) '
                    f'VALUES ({", ".join(f"${i}" for i in range(1, len(offer_data) + 1))})'
                    )

            await session.execute(stmt, *offer_data.values())
        except Exception as e:
            logging.error("Error while insert data to DB", exc_info=e)
