from django.db import IntegrityError
from ..repositories.StoreProductRepository import StoreProductRepository


class StoreProductService:
    def __init__(self):
        self.repository = StoreProductRepository()

    def get_list_of_store_products(self):
        return self.repository.get_all()

    def get_store_product_by_upc(self, upc: str):
        store_product = self.repository.get_by_upc(upc)
        if not store_product:
            raise ValueError(f"Товар з UPC {upc} не знайдено.")
        return store_product

    def search_by_product_name(self, name: str):
        return self.repository.get_by_product_name(name)

    def add_store_product(self, data: dict):
        self.repository.create(data)
        return self.repository.get_by_upc(data['UPC'])

    def update_store_product(self, upc: str, data: dict):
        self.get_store_product_by_upc(upc)
        self.repository.update(upc, data)
        return self.repository.get_by_upc(upc)

    def delete_store_product(self, upc: str):
        self.get_store_product_by_upc(upc)
        try:
            self.repository.delete(upc)
        except IntegrityError:
            raise ValueError(
                "Цей товар неможливо видалити, оскільки він використовується в чеках. "
                "Спочатку видаліть пов'язані записи продажів."
            )
