from django.db import connection

EMPLOYEE_FIELDS_NO_PASSWORD = (
    "id_employee, empl_surname, empl_name, empl_patronymic, empl_role, "
    "salary, date_of_birth, date_of_start, phone_number, city, street, zip_code"
)

EMPLOYEE_FIELDS_WITH_PASSWORD = EMPLOYEE_FIELDS_NO_PASSWORD + ", password_hash"


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

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT {EMPLOYEE_FIELDS_NO_PASSWORD} FROM Employee ORDER BY empl_surname;"
            )
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id_public(id_employee: str):
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT {EMPLOYEE_FIELDS_NO_PASSWORD} FROM Employee WHERE id_employee = %s;",
                [id_employee]
            )
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    @staticmethod
    def get_by_surname(surname: str):
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT {EMPLOYEE_FIELDS_NO_PASSWORD} FROM Employee "
                "WHERE empl_surname ILIKE %s ORDER BY empl_surname;",
                [f"%{surname}%"]
            )
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def _generate_next_id():
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(id_employee) FROM Employee;")
            row = cursor.fetchone()
            if row[0] is None:
                return "EMP0000001"
            max_id = row[0]
            num = int(max_id[3:]) + 1
            return f"EMP{num:07d}"

    @staticmethod
    def create(data: dict):
        id_employee = EmployeeRepository._generate_next_id()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Employee (id_employee, empl_surname, empl_name, empl_patronymic, "
                "empl_role, salary, date_of_birth, date_of_start, phone_number, city, street, "
                "zip_code, password_hash) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                "RETURNING id_employee;",
                [
                    id_employee,
                    data['empl_surname'],
                    data['empl_name'],
                    data.get('empl_patronymic'),
                    data['empl_role'],
                    data['salary'],
                    data['date_of_birth'],
                    data['date_of_start'],
                    data['phone_number'],
                    data['city'],
                    data['street'],
                    data['zip_code'],
                    data['password_hash'],
                ]
            )
            return cursor.fetchone()[0]

    @staticmethod
    def update(id_employee: str, data: dict):
        fields = []
        values = []
        for key in ['empl_surname', 'empl_name', 'empl_patronymic', 'empl_role',
                     'salary', 'date_of_birth', 'date_of_start', 'phone_number',
                     'city', 'street', 'zip_code', 'password_hash']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])
        if not fields:
            return
        values.append(id_employee)
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE Employee SET {', '.join(fields)} WHERE id_employee = %s;",
                values
            )

    @staticmethod
    def delete(id_employee: str):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Employee WHERE id_employee = %s;",
                [id_employee]
            )
