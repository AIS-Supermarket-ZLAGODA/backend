from django.db import connection


class BezukhReportRepository:
    @staticmethod
    def get_sales_analysis_report(date_from=None, date_to=None):
        with connection.cursor() as cursor:
            query = """
                    SELECT c.category_name,
                           p.product_name,
                           SUM(s.product_number)                   AS total_quantity_sold,
                           SUM(s.product_number * s.selling_price) AS product_revenue,
                           SUM(SUM(s.product_number * s.selling_price))
                           OVER (PARTITION BY c.category_name)     AS total_category_revenue
                    FROM category c
                             JOIN product p ON c.category_number = p.category_number
                             JOIN store_product sp ON p.id_product = sp.id_product
                             JOIN sale s ON sp.UPC = s.UPC
                             JOIN "Check" ch ON s.check_number = ch.check_number
                    WHERE 1 = 1 """

            params = []

            if date_from:
                query += "AND ch.print_date >= %s "
                params.append(date_from)

            if date_to:
                query += "AND ch.print_date <= %s "
                params.append(date_to)

            query += """
                     GROUP BY c.category_name, p.product_name
                     ORDER BY c.category_name, product_revenue DESC;
                     """

            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_categories_with_only_promotional_products():
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT *
                           FROM category c
                           WHERE NOT EXISTS(SELECT 1
                                            FROM product p
                                            WHERE c.category_number = p.category_number
                                              AND NOT EXISTS(SELECT 1
                                                             FROM store_product sp
                                                             WHERE sp.id_product = p.id_product
                                                               AND sp.promotional_product))
                             AND EXISTS (SELECT 1
                                         FROM product p2
                                         WHERE p2.category_number = c.category_number)
                           ORDER BY category_name;
                           """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


class ZmeulReportRepository:
    @staticmethod
    def get_producer_performance(category_name, date_from=None, date_to=None):
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.producer, 
                    SUM(s.product_number) AS total_items_sold, 
                    SUM(s.product_number * s.selling_price) AS total_revenue
                FROM Category c
                INNER JOIN Product p ON c.category_number = p.category_number
                INNER JOIN Store_Product sp ON p.id_product = sp.id_product
                INNER JOIN Sale s ON sp.UPC = s.UPC
                INNER JOIN "Check" ch ON s.check_number = ch.check_number
                WHERE c.category_name = %s 
            """
            
            params = [category_name]
            
            if date_from:
                query += " AND ch.print_date >= %s"
                params.append(date_from)
            if date_to:
                query += " AND ch.print_date <= %s"
                params.append(date_to)
                
            query += """
                GROUP BY p.producer
                ORDER BY total_revenue DESC;
            """
            
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_universal_categories():
        with connection.cursor() as cursor:
            query = """
                SELECT c.category_number, c.category_name
                FROM Category c
                WHERE NOT EXISTS (
                    SELECT e.id_employee
                    FROM Employee e
                    WHERE e.empl_role = 'Касир'
                      AND NOT EXISTS (
                          SELECT 1
                          FROM "Check" ch
                          INNER JOIN Sale s ON ch.check_number = s.check_number
                          INNER JOIN Store_Product sp ON s.UPC = sp.UPC
                          INNER JOIN Product p ON sp.id_product = p.id_product
                          WHERE ch.id_employee = e.id_employee 
                            AND p.category_number = c.category_number
                      )
                );
            """
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

class LapkoReportRepository:
    ...
