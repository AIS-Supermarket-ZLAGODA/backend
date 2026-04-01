from django.db import IntegrityError
from ..repositories.CustomerCardRepository import CustomerCardRepository
import re


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
        self.__check_data(data)

        card_number = self.repository.generate_card_number()
        data['card_number'] = card_number
        self.repository.create(data)
        return self.repository.get_by_number(card_number)

    def update_customer(self, card_number: str, data: dict):
        self.__check_data(data)

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

    @staticmethod
    def __check_data(data: dict):
        percent = data.get("percent")
        if percent is None or percent < 0 or percent > 100:
            raise ValueError("Знижка не має бути менше 0% або більше 100%!")

        phone_number: str = data.get("phone_number", "")

        phone_regex = r"^\+380\d{9}$"

        if not re.fullmatch(phone_regex, phone_number):
            raise ValueError("Неправильний номер телефона! Формат має бути +380XXXXXXXXX (13 символів).")