import re
from datetime import date
from argon2 import PasswordHasher
from django.db import IntegrityError
from ..repositories.EmployeeRepository import EmployeeRepository


class EmployeeService:
    def __init__(self):
        self.repository = EmployeeRepository()
        self.ph = PasswordHasher()

    def get_list_of_employees(self, surname=None):
        if surname:
            return self.repository.get_by_surname(surname)
        return self.repository.get_all()

    def get_employee_by_id(self, id_employee: str):
        employee = self.repository.get_by_id_public(id_employee)
        if not employee:
            raise ValueError(f"Працівника з ID {id_employee} не знайдено.")
        return employee

    def _validate_phone(self, phone_number: str, exclude_id: str = None):
        pattern = r"^\+380\d{9}$"
        if not re.match(pattern, phone_number):
            raise ValueError("Номер телефону повинен бути у форматі +380XXXXXXXXX.")

        existing = self.repository.get_by_phone(phone_number)
        if existing:
            if exclude_id and existing['id_employee'] == exclude_id:
                pass
            else:
                raise ValueError(f"Працівник з номером телефону {phone_number} вже існує.")

    def _validate_date_of_birth(self, date_of_birth):
        today = date.today()
        age = today.year - date_of_birth.year - (
            (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )
        if age < 18:
            raise ValueError("Працівник повинен бути не молодше 18 років.")

    def _validate_required_fields(self, data: dict):
        required = ['empl_surname', 'empl_name', 'empl_role', 'salary',
                     'date_of_birth', 'date_of_start', 'phone_number',
                     'city', 'street', 'zip_code']
        for field in required:
            value = data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"Поле '{field}' є обов'язковим і не може бути порожнім.")

    def add_employee(self, data: dict):
        self._validate_required_fields(data)
        self._validate_phone(data['phone_number'])
        self._validate_date_of_birth(data['date_of_birth'])

        if not data.get('password'):
            raise ValueError("Пароль є обов'язковим при створенні працівника.")

        create_data = {k: v for k, v in data.items() if k != 'password'}
        create_data['password_hash'] = self.ph.hash(data['password'])

        return self.repository.create(create_data)

    def update_employee(self, id_employee: str, data: dict):
        existing = self.repository.get_by_id_public(id_employee)
        if not existing:
            raise ValueError(f"Працівника з ID {id_employee} не знайдено.")

        if 'phone_number' in data:
            self._validate_phone(data['phone_number'], exclude_id=id_employee)

        if 'date_of_birth' in data:
            self._validate_date_of_birth(data['date_of_birth'])

        update_data = {k: v for k, v in data.items() if k != 'password'}

        if data.get('password'):
            update_data['password_hash'] = self.ph.hash(data['password'])

        self.repository.update(id_employee, update_data)

        return self.repository.get_by_id_public(id_employee)

    def delete_employee(self, id_employee: str):
        existing = self.repository.get_by_id_public(id_employee)
        if not existing:
            raise ValueError(f"Працівника з ID {id_employee} не знайдено.")
        try:
            self.repository.delete(id_employee)
        except IntegrityError:
            raise ValueError(
                "Цього працівника неможливо видалити, оскільки він має пов'язані чеки. "
                "Спочатку видаліть або змініть працівника для всіх пов'язаних чеків."
            )
