import logging


class DbService:
    @staticmethod
    async def create_table_if_not_exists(session):
        try:
            stmt = (
                'CREATE TABLE IF NOT EXISTS used_cars_offers ( '
                'id SERIAL PRIMARY KEY, '
                'url VARCHAR(255),'
                'title VARCHAR(255),'
                'price_usd INT,'
                'odometer INT, '
                'username VARCHAR(255),'
                'phone_number INT,'
                'image_url VARCHAR(255),'
                'images_count INT,'
                'car_number VARCHAR(255),'
                'car_vin VARCHAR(255), '
                'datetime_found TIMESTAMP'
                ');'
            )

            await session.execute(stmt)
        except Exception as e:
            logging.error("Error while creating table in DB", exc_info=e)

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
