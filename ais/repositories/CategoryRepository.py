from django.db import connection

class CategoryRepository:
    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("SELECT category_number, category_name FROM Category ORDER BY category_name;")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


    @staticmethod
    def create(category_name: str):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Category (category_name) VALUES (%s) RETURNING category_number;",
                [category_name]
            )
            return cursor.fetchone()[0]


    @staticmethod
    def delete(category_number: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Category WHERE category_number = %s;",
                [category_number]
            )


    @staticmethod
    def update(category_number: int, category_name: str):
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Category SET category_name = %s WHERE category_number = %s;",
                [category_name, category_number]
            )


    @staticmethod
    def get_by_number(category_number: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT category_number, category_name FROM Category WHERE category_number = %s;",
                [category_number]
            )
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None