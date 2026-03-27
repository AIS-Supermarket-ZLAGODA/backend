from django.db import connection


class CustomerCardRepository:
    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT card_number, cust_surname, cust_name, cust_patronymic,
                       phone_number, city, street, zip_code, percent
                FROM Customer_Card
                ORDER BY cust_surname;
            """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_by_number(card_number: str):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT card_number, cust_surname, cust_name, cust_patronymic,
                       phone_number, city, street, zip_code, percent
                FROM Customer_Card
                WHERE card_number = %s;
            """, [card_number])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    @staticmethod
    def get_by_surname(surname: str):
        with connection.cursor() as cursor:
            search_pattern = f"%{surname}%"
            cursor.execute("""
                SELECT card_number, cust_surname, cust_name, cust_patronymic,
                       phone_number, city, street, zip_code, percent
                FROM Customer_Card
                WHERE cust_surname ILIKE %s
                ORDER BY cust_surname;
            """, [search_pattern])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def create(data: dict):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Customer_Card (card_number, cust_surname, cust_name, cust_patronymic,
                                           phone_number, city, street, zip_code, percent)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING card_number;
            """, [
                data['card_number'],
                data['cust_surname'],
                data['cust_name'],
                data.get('cust_patronymic'),
                data['phone_number'],
                data.get('city'),
                data.get('street'),
                data.get('zip_code'),
                data['percent'],
            ])
            return cursor.fetchone()[0]

    @staticmethod
    def update(card_number: str, data: dict):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Customer_Card
                SET cust_surname = %s, cust_name = %s, cust_patronymic = %s,
                    phone_number = %s, city = %s, street = %s, zip_code = %s, percent = %s
                WHERE card_number = %s;
            """, [
                data['cust_surname'],
                data['cust_name'],
                data.get('cust_patronymic'),
                data['phone_number'],
                data.get('city'),
                data.get('street'),
                data.get('zip_code'),
                data['percent'],
                card_number,
            ])

    @staticmethod
    def delete(card_number: str):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Customer_Card WHERE card_number = %s;", [card_number])

    @staticmethod
    def generate_card_number():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT card_number FROM Customer_Card
                WHERE card_number LIKE 'CARD%%'
                ORDER BY card_number DESC LIMIT 1;
            """)
            row = cursor.fetchone()
            if row:
                last_num = int(row[0][4:])
                return f"CARD{last_num + 1:09d}"
            return "CARD000000001"
