from django.db import connection

class TestTableRepository:
    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM test_table")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def create(full_name: str):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO test_table (full_name) VALUES (%s) RETURNING id",
                [full_name]
            )
            return cursor.fetchone()[0]