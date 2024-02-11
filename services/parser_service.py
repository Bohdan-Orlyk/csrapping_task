import logging

from bs4 import BeautifulSoup
from datetime import datetime

from services.request_service import send_request
from services.database_service import DbService


class ParserService:
    def __init__(self):
        self.db_service = DbService()

    async def get_pages_count(self, page_html: str) -> int:
        soup = BeautifulSoup(page_html, "lxml")
        pagination_block = soup.find(id="pagination")
        page_count = (pagination_block
                      .find_all("a", class_="page-link")[-2]
                      .text
                      .strip()
                      .replace(' ', ''))

        return int(page_count)

    async def parse_offer_data(self, session, page_count: int, main_url: str) -> None:
        for page in range(1, page_count):
            page_response = await send_request(
                url=f"{main_url}?{page=}"
            )
            print(f"{main_url}?{page=}")

            page_soup = BeautifulSoup(page_response, "lxml")
            offers = page_soup.find_all("div", class_="content-bar")

            offer_links = []
            for offer in offers:
                offer_link = offer.find("a", class_="m-link-ticket").get("href")
                offer_links.append(offer_link)

                offer_data = await self.prepare_offer_data(offer_link)
                print(offer_data)
                await self.db_service.insert_data_to_db(session=session,
                                                        offer_data=offer_data)

    async def prepare_offer_data(self, offer_link: str) -> dict:
        try:
            offer_html = await send_request(url=offer_link)
            offer_soup = BeautifulSoup(offer_html, "lxml")

            car_number = offer_soup.find('span', class_='state-num ua')

            offer_data = {
                "url": offer_link,
                "title":
                    offer_soup.find("h1", class_="head").text,
                "price_usd":
                    int(offer_soup.select_one("div.price_value > strong").text
                        .replace(" ", "")
                        .replace("$", "")
                        .replace("€", "")
                        .replace("грн", "")
                        ),
                "odometer": int(f"{offer_soup.find('span', class_='size18').text}000"),
                "username":
                    offer_soup.find("div", class_="seller_info_name").text
                    if offer_soup.find("div", class_="seller_info_name")
                    else None,
                "phone_number": None,
                "image_url": offer_soup.find("img", class_="outline m-auto")["src"],
                "images_count":
                    len(offer_soup.find_all("div",
                                            class_=lambda value: value and value.startswith("photo-620x465"))
                        ),
                "car_number":
                    car_number.contents[0].strip()
                    if offer_soup.find('span', class_="state-num ua")
                    else None,
                "car_vin":
                    offer_soup.find('span', class_="label-vin").text
                    if offer_soup.find('span', class_="label-vin")
                    else None,
                "datetime_found": datetime.utcnow(),
            }

            return offer_data
        except AttributeError as e:
            logging.error("Invalid attributes", exc_info=e)

