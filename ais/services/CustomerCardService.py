from django.db import IntegrityError
from ..repositories.CustomerCardRepository import CustomerCardRepository


class CustomerCardService:
    def __init__(self):
        self.repository = CustomerCardRepository()

    def get_list_of_customers(self):
        return self.repository.get_all()

    def get_customer_by_number(self, card_number: str):
        customer = self.repository.get_by_number(card_number)
        if not customer:
            raise ValueError(f"Картку клієнта з номером {card_number} не знайдено.")
        return customer

    def search_by_surname(self, surname: str):
        return self.repository.get_by_surname(surname)

    def add_customer(self, data: dict):
        card_number = self.repository.generate_card_number()
        data['card_number'] = card_number
        self.repository.create(data)
        return self.repository.get_by_number(card_number)

    def update_customer(self, card_number: str, data: dict):
        self.get_customer_by_number(card_number)
        self.repository.update(card_number, data)
        return self.repository.get_by_number(card_number)

    def delete_customer(self, card_number: str):
        self.get_customer_by_number(card_number)
        try:
            self.repository.delete(card_number)
        except IntegrityError:
            raise ValueError(
                "Цю картку клієнта неможливо видалити, оскільки вона використовується в чеках. "
                "Спочатку видаліть пов'язані чеки."
            )
