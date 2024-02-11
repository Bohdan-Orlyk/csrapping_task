import asyncio
import logging

from services.request_service import send_request
from services.parser_service import ParserService

from database.database import get_db_session


class Parser:
    def __init__(self):
        self.main_url = "https://auto.ria.com/car/used/"
        self.parser_service = ParserService()

    async def parse_autoria(self):
        html_response = await send_request(url=self.main_url)

        try:
            pages_count = await self.parser_service.get_pages_count(html_response)
            async with get_db_session() as session:
                await self.parser_service.parse_offer_data(session=session,
                                                           page_count=pages_count,
                                                           main_url=self.main_url)

        except Exception as e:
            logging.error("Unexpected error occurred", exc_info=e)


if __name__ == "__main__":
    parser = Parser()
    asyncio.run(parser.parse_autoria())

