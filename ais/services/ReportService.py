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


class LapkoReportService:
    def __init__(self):
        self.repository = LapkoReportRepository()