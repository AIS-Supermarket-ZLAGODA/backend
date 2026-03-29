from django.db import connection


class CheckRepository:
    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.check_number, c.id_employee, c.card_number, c.print_date,
                       c.sum_total, c.vat, e.empl_surname, e.empl_name
                FROM "Check" c
                INNER JOIN Employee e ON c.id_employee = e.id_employee
                ORDER BY c.print_date DESC;
            """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_by_number(check_number: str):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.check_number, c.id_employee, c.card_number, c.print_date,
                       c.sum_total, c.vat, e.empl_surname, e.empl_name
                FROM "Check" c
                INNER JOIN Employee e ON c.id_employee = e.id_employee
                WHERE c.check_number = %s;
            """, [check_number])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    @staticmethod
    def get_by_employee(id_employee: str):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.check_number, c.id_employee, c.card_number, c.print_date,
                       c.sum_total, c.vat, e.empl_surname, e.empl_name
                FROM "Check" c
                INNER JOIN Employee e ON c.id_employee = e.id_employee
                WHERE c.id_employee = %s
                ORDER BY c.print_date DESC;
            """, [id_employee])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def create(data: dict):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO "Check" (check_number, id_employee, card_number, print_date, sum_total, vat)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING check_number;
            """, [
                data['check_number'],
                data['id_employee'],
                data.get('card_number'),
                data['print_date'],
                data['sum_total'],
                data['vat'],
            ])
            return cursor.fetchone()[0]

    @staticmethod
    def delete(check_number: str):
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM "Check" WHERE check_number = %s;', [check_number])

    @staticmethod
    def get_sales_by_check(check_number: str):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.UPC, s.check_number, s.product_number, s.selling_price,
                       p.product_name
                FROM Sale s
                INNER JOIN Store_Product sp ON s.UPC = sp.UPC
                INNER JOIN Product p ON sp.id_product = p.id_product
                WHERE s.check_number = %s;
            """, [check_number])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def generate_check_number():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT check_number FROM "Check"
                WHERE check_number LIKE 'CHK%%'
                ORDER BY check_number DESC LIMIT 1;
            """)
            row = cursor.fetchone()
            if row:
                last_num = int(row[0][3:])
                return f"CHK{last_num + 1:07d}"
            return "CHK0000001"
