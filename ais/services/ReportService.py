from ..repositories.ReportRepository import BezukhReportRepository, ZmeulReportRepository, LapkoReportRepository


class BezukhReportService:
    def __init__(self):
        self.repository = BezukhReportRepository()

    def get_sales_analysis_report(self, date_from=None, date_to=None):
        return self.repository.get_sales_analysis_report(date_from, date_to)

    def get_categories_with_only_promotional_products(self):
        return self.repository.get_categories_with_only_promotional_products()


class ZmeulReportService:
    def __init__(self):
        self.repository = ZmeulReportRepository()

    def get_producer_performance(self, category_name, date_from=None, date_to=None):
        if not category_name:
            raise ValueError("category_name is required")
            
        return self.repository.get_producer_performance(category_name, date_from, date_to)

    def get_universal_categories(self):
        return self.repository.get_universal_categories()

class LapkoReportService:
    def __init__(self):
        self.repository = LapkoReportRepository()

    def get_customers_category_spending(self, category_name, date_from=None, date_to=None):
        if not category_name:
            raise ValueError("category_name is required")
        return self.repository.get_customers_category_spending(category_name, date_from, date_to)

    def get_customers_bought_all_in_category(self, category_name):
        if not category_name:
            raise ValueError("category_name is required")
        return self.repository.get_customers_bought_all_in_category(category_name)