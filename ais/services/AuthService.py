from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from ..repositories.EmployeeRepository import EmployeeRepository


class AuthService:
    def __init__(self):
        self.repository = EmployeeRepository()
        self.ph = PasswordHasher()

    def authenticate(self, login: str, password: str) -> dict:
        employee = self.repository.get_by_id(login)
        if not employee:
            employee = self.repository.get_by_phone(login)
        if not employee:
            raise ValueError("Невірний логін або пароль")

        try:
            self.ph.verify(employee['password_hash'], password)
        except VerifyMismatchError:
            raise ValueError("Невірний логін або пароль")

        role_map = {"Касир": "Cashier", "Менеджер": "Manager"}
        role = role_map.get(employee["empl_role"], employee["empl_role"])

        return {
            "id_employee": employee["id_employee"],
            "empl_name": employee["empl_name"],
            "empl_surname": employee["empl_surname"],
            "empl_role": role,
        }
