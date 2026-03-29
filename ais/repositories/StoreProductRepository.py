from django.db import connection


class StoreProductRepository:
    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT sp.UPC, sp.UPC_prom, sp.id_product, sp.selling_price,
                       sp.products_number, sp.promotional_product, p.product_name
                FROM Store_Product sp
                INNER JOIN Product p ON sp.id_product = p.id_product
                ORDER BY p.product_name;
            """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_by_upc(upc: str):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT sp.UPC, sp.UPC_prom, sp.id_product, sp.selling_price,
                       sp.products_number, sp.promotional_product, p.product_name
                FROM Store_Product sp
                INNER JOIN Product p ON sp.id_product = p.id_product
                WHERE sp.UPC = %s;
            """, [upc])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    @staticmethod
    def get_by_product_name(name: str):
        with connection.cursor() as cursor:
            search_pattern = f"%{name}%"
            cursor.execute("""
                SELECT sp.UPC, sp.UPC_prom, sp.id_product, sp.selling_price,
                       sp.products_number, sp.promotional_product, p.product_name
                FROM Store_Product sp
                INNER JOIN Product p ON sp.id_product = p.id_product
                WHERE p.product_name ILIKE %s
                ORDER BY p.product_name;
            """, [search_pattern])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def create(data: dict):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Store_Product (UPC, UPC_prom, id_product, selling_price,
                                           products_number, promotional_product)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING UPC;
            """, [
                data['UPC'],
                data.get('UPC_prom'),
                data['id_product'],
                data['selling_price'],
                data['products_number'],
                data['promotional_product'],
            ])
            return cursor.fetchone()[0]

    @staticmethod
    def update(upc: str, data: dict):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Store_Product
                SET UPC_prom = %s, id_product = %s, selling_price = %s,
                    products_number = %s, promotional_product = %s
                WHERE UPC = %s;
            """, [
                data.get('UPC_prom'),
                data['id_product'],
                data['selling_price'],
                data['products_number'],
                data['promotional_product'],
                upc,
            ])

    @staticmethod
    def delete(upc: str):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Store_Product WHERE UPC = %s;", [upc])

    @staticmethod
    def update_stock(upc: str, quantity_delta: int):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Store_Product
                SET products_number = products_number + %s
                WHERE UPC = %s;
            """, [quantity_delta, upc])
