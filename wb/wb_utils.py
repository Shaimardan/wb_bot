from aiogram.fsm.state import State, StatesGroup
import requests


class ProductQuery(StatesGroup):
    waiting_for_product_id = State()


class WildberriesProductInfo:
    def __init__(self, product_id):
        self.product_id = product_id
        self.base_url = "https://card.wb.ru/cards/v1/detail"
        self.params = {
            "appType": 1,
            "curr": "rub",
            "dest": "-1257786",
            "spp": 30,
            "nm": self.product_id
        }

    @staticmethod
    def is_valid_product_id(product_id):
        return product_id.isdigit() and 5 <= len(product_id) <= 10

    def fetch_product_info(self):
        if not self.is_valid_product_id(self.product_id):
            print("Неверный формат артикула товара.")
            return None

        try:
            response = requests.get(self.base_url, params=self.params)
            response.raise_for_status()
            data = response.json()
            return self.parse_product_info(data)
        except requests.RequestException as e:
            print(f"Error fetching product info: {e}")
            return None

    @staticmethod
    def parse_product_info(data):
        try:
            product_data = data.get('data', {}).get('products', [])[0]  # Берем первый продукт из списка
            product_info = {
                "name": product_data.get("name"),
                "articul": product_data.get("id"),
                "price": product_data.get('salePriceU'),
                "sale": product_data.get('priceU'),
                "rating": product_data.get('supplierRating')
            }
            return product_info
        except (IndexError, KeyError, TypeError):
            print("Error parsing product data.")
            return None


