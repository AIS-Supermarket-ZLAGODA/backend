import re
from django.db import IntegrityError
from ..repositories.CategoryRepository import CategoryRepository


def _validate_category_name(name: str) -> str:
    if not name or not name.strip():
        raise ValueError("Назва категорії не може бути порожньою!")

    pattern = r"^[А-Яа-яІіЇїЄєҐґA-Za-z0-9\s\-']+$"

    if not re.match(pattern, name):
        raise ValueError(
            "Назва категорії може містити лише українські та англійські літери, цифри, пробіли, дефіси та апострофи!"
        )

    return name.strip()


class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()

    def get_list_of_categories(self):
        return self.repository.get_all()

    def get_category_by_number(self, category_number: int):
        category = self.repository.get_by_number(category_number)
        if not category:
            raise ValueError(f"Категорію з номером {category_number} не знайдено.")
        return category

    def add_category(self, category_name: str):
        valid_name = _validate_category_name(category_name)
        return self.repository.create(valid_name)

    def update_category(self, category_number: int, category_name: str):
        self.get_category_by_number(category_number)

        valid_name = _validate_category_name(category_name)

        self.repository.update(category_number, valid_name)
        return {"category_number": category_number, "category_name": valid_name}

    def delete_category(self, category_number: int):
        self.get_category_by_number(category_number)
        try:
            self.repository.delete(category_number)
        except IntegrityError:
            raise ValueError(
                "Цю категорію неможливо видалити, оскільки до неї належать товари. "
                "Спочатку видаліть або змініть категорію для всіх пов'язаних товарів."
            )