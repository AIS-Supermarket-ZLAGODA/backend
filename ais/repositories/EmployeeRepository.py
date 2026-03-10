from django.db import connection


class EmployeeRepository:
    @staticmethod
    def get_by_id(id_employee: str):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_employee, empl_surname, empl_name, empl_patronymic, empl_role, "
                "salary, date_of_birth, date_of_start, phone_number, city, street, zip_code, password_hash "
                "FROM Employee WHERE id_employee = %s;",
                [id_employee]
            )
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    @staticmethod
    def get_by_phone(phone_number: str):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_employee, empl_surname, empl_name, empl_patronymic, empl_role, "
                "salary, date_of_birth, date_of_start, phone_number, city, street, zip_code, password_hash "
                "FROM Employee WHERE phone_number = %s;",
                [phone_number]
            )
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None
