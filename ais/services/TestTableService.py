from ..repositories.TestTableRepository import TestTableRepository


class TestTableService:
    def __init__(self):
        self.repository = TestTableRepository()

    def get_list_of_tests(self):
        return self.repository.get_all()

    def add_test_entry(self, full_name: str):
        if not full_name:
            raise ValueError("Name cannot be empty!")
        return self.repository.create(full_name)