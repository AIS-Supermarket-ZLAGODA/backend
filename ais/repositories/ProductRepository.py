from django.db import connection

class ProductRepository:
    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_product, category_number, product_name, producer, characteristics 
                FROM Product 
                ORDER BY product_name;
            """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


    @staticmethod
    def get_by_name(product_name: str):
        with connection.cursor() as cursor:
            search_pattern = f"%{product_name}%"
            cursor.execute("""
                           SELECT id_product, category_number, product_name, producer, characteristics
                           FROM Product
                           WHERE product_name ILIKE %s
                           ORDER BY product_name;
                           """, [search_pattern])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


    @staticmethod
    def get_by_category_name(category_name: str):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id_product, p.category_number, p.product_name, p.producer, p.characteristics 
                FROM Product p
                INNER JOIN Category c ON p.category_number = c.category_number
                WHERE c.category_name = %s
                ORDER BY p.product_name;
            """, [category_name])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


    @staticmethod
    def create(category_number: int, product_name: str, producer: str, characteristics: str):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Product (category_number, product_name, producer, characteristics) 
                VALUES (%s, %s, %s, %s) RETURNING id_product;
                """,
                [category_number, product_name, producer, characteristics]
            )
            return cursor.fetchone()[0]


    @staticmethod
    def delete(id_product: int):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Product WHERE id_product = %s;", [id_product])


    @staticmethod
    def update(id_product: int, category_number: int, product_name: str, producer: str, characteristics: str):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Product 
                SET category_number = %s, product_name = %s, producer = %s, characteristics = %s 
                WHERE id_product = %s;
                """,
                [category_number, product_name, producer, characteristics, id_product]
            )


    @staticmethod
    def get_by_id(id_product: int):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_product, category_number, product_name, producer, characteristics 
                FROM Product 
                WHERE id_product = %s;
                """,
                [id_product]
            )
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    @staticmethod
    def get_sold_stats(id_product: int, date_from=None, date_to=None):
        with connection.cursor() as cursor:
            query = """
                    SELECT SUM(s.product_number)
                    FROM Sale s
                    INNER JOIN Store_Product sp ON s.UPC = sp.UPC
                    INNER JOIN "Check" c ON s.check_number = c.check_number
                    WHERE sp.id_product = %s 
                    """
            params = [id_product]

            if date_from:
                query += " AND c.print_date >= %s"
                params.append(date_from)
            if date_to:
                query += " AND c.print_date <= %s"
                params.append(date_to)

            cursor.execute(query, params)
            result = cursor.fetchone()
            return int(result[0]) if result[0] is not None else 0