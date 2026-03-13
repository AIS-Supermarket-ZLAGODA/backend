import re
from django.db import IntegrityError
from ..repositories.ProductRepository import ProductRepository
from .CategoryService import CategoryService  # Імпортуємо сервіс!


def _validate_text_field(text: str, field_name: str) -> str:
    if not text or not text.strip():
        raise ValueError(f"Поле '{field_name}' не може бути порожнім!")

    pattern = r"^[А-Яа-яІіЇїЄєҐґA-Za-z0-9\s\-',.%]+$"
    if not re.match(pattern, text):
        raise ValueError(f"Поле '{field_name}' містить недопустимі символи.")

    return text.strip()


class ProductService:
    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_service = CategoryService()

    def get_list_of_products(self, category_name: str = None, product_name: str = None):
        if category_name:
            return self.product_repo.get_by_category_name(category_name)
        if product_name:
            return self.product_repo.get_by_name(product_name)
        return self.product_repo.get_all()

    def get_product_by_id(self, id_product: int):
        product = self.product_repo.get_by_id(id_product)
        if not product:
            raise ValueError(f"Товар з ID {id_product} не знайдено.")
        return product

    def add_product(self, category_number: int, product_name: str, producer: str, characteristics: str):
        self.category_service.get_category_by_number(category_number)

        valid_name = _validate_text_field(product_name, "Назва товару")
        valid_producer = _validate_text_field(producer, "Виробник")
        valid_chars = _validate_text_field(characteristics, "Характеристики")

        return self.product_repo.create(category_number, valid_name, valid_producer, valid_chars)

    def update_product(self, id_product: int, category_number: int, product_name: str, producer: str,
                       characteristics: str):
        self.get_product_by_id(id_product)

        self.category_service.get_category_by_number(category_number)

        valid_name = _validate_text_field(product_name, "Назва товару")
        valid_producer = _validate_text_field(producer, "Виробник")
        valid_chars = _validate_text_field(characteristics, "Характеристики")

        self.product_repo.update(id_product, category_number, valid_name, valid_producer, valid_chars)

        return {
            "id_product": id_product,
            "category_number": category_number,
            "product_name": valid_name,
            "producer": valid_producer,
            "characteristics": valid_chars
        }

    def delete_product(self, id_product: int):
        self.get_product_by_id(id_product)
        try:
            self.product_repo.delete(id_product)
        except IntegrityError:
            raise ValueError(
                "Цей товар неможливо видалити, оскільки він зараз наявний на складі магазину. "
                "Спершу видаліть його зі складу магазину."
            )