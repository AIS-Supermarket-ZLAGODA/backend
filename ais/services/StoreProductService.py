import re

from django.db import IntegrityError
from ..repositories.StoreProductRepository import StoreProductRepository


class StoreProductService:
    def __init__(self):
        self.repository = StoreProductRepository()

    @staticmethod
    def _validate_store_product_data(data: dict):
        selling_price = data['selling_price']
        if selling_price is not None and float(selling_price) <= 0:
            raise ValueError("Ціна продажу не може бути від'ємною, або дорівнювати 0.")

        products_number = data['products_number']
        if products_number is not None and int(products_number) < 0:
            raise ValueError("Кількість товарів не може бути від'ємною.")

        upc_pattern = re.compile(r'^\d{1,12}$')

        upc = data.get('upc')
        if upc is not None and not upc_pattern.match(str(upc)):
            raise ValueError("UPC має містити лише цифри (максимум 12).")

        upc_prom = data.get('upc_prom')
        if upc_prom and not upc_pattern.match(str(upc_prom)):
            raise ValueError("UPC акційного товару має містити лише цифри (максимум 12).")

    def get_list_of_store_products(self, product_name=None, is_promotional=None, sort_by_quantity=False):
        return self.repository.get_all(
            product_name=product_name,
            is_promotional=is_promotional,
            sort_by_quantity=sort_by_quantity
        )

    def get_store_product_by_upc(self, upc: str):
        store_product = self.repository.get_by_upc(upc)
        if not store_product:
            raise ValueError(f"Товар з UPC {upc} не знайдено.")
        return store_product

    def search_by_product_name(self, name: str):
        return self.repository.get_by_product_name(name)

    def add_store_product(self, data: dict):
        self._validate_store_product_data(data)
        self.repository.create(data)
        return self.repository.get_by_upc(data['upc'])

    def update_store_product(self, upc: str, data: dict):
        self._validate_store_product_data(data)
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
