from django.db import connection


class SaleRepository:
    @staticmethod
    def create(upc: str, check_number: str, product_number: int, selling_price):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Sale (UPC, check_number, product_number, selling_price)
                VALUES (%s, %s, %s, %s);
            """, [upc, check_number, product_number, selling_price])

    @staticmethod
    def get_by_check(check_number: str):
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
