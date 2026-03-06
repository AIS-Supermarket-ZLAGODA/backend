import re
from ..repositories.CategoryRepository import CategoryRepository


def _validate_category_name(name: str) -> str:
    if not name or not name.strip():
        raise ValueError("Category name cannot be empty!")

    pattern = r"^[А-Яа-яІіЇїЄєҐґA-Za-z0-9\s\-']+$"

    if not re.match(pattern, name):
        raise ValueError(
            "Your category name can only contain letters, numbers, spaces, hyphens, and apostrophes!")

    return name.strip()


class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()

    def get_list_of_categories(self):
        return self.repository.get_all()

    def get_category_by_number(self, category_number: int):
        category = self.repository.get_by_number(category_number)
        if not category:
            raise ValueError(f"Category with number: {category_number} not found.")
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
        self.repository.delete(category_number)