from decimal import Decimal
from django.db import transaction, IntegrityError
from django.utils import timezone
from ..repositories.CheckRepository import CheckRepository
from ..repositories.SaleRepository import SaleRepository
from ..repositories.StoreProductRepository import StoreProductRepository
from ..repositories.CustomerCardRepository import CustomerCardRepository


class CheckService:
    def __init__(self):
        self.check_repository = CheckRepository()
        self.sale_repository = SaleRepository()
        self.store_product_repository = StoreProductRepository()
        self.customer_card_repository = CustomerCardRepository()

    def get_list_of_checks(self, id_employee=None):
        if id_employee:
            return self.check_repository.get_by_employee(id_employee)
        return self.check_repository.get_all()

    def get_check_by_number(self, check_number: str):
        check = self.check_repository.get_by_number(check_number)
        if not check:
            raise ValueError(f"Чек з номером {check_number} не знайдено.")
        items = self.check_repository.get_sales_by_check(check_number)
        check['items'] = items
        return check

    def create_check(self, id_employee: str, card_number: str, items: list):
        if not items:
            raise ValueError("Чек повинен містити хоча б один товар.")

        with transaction.atomic():
            sum_total = Decimal('0')

            sale_entries = []
            for item in items:
                upc = item['UPC']
                product_number = item['product_number']

                store_product = self.store_product_repository.get_by_upc(upc)
                if not store_product:
                    raise ValueError(f"Товар з UPC {upc} не знайдено в магазині.")

                if store_product['products_number'] < product_number:
                    raise ValueError(
                        f"Недостатньо товару з UPC {upc} на складі. "
                        f"Доступно: {store_product['products_number']}, запитано: {product_number}."
                    )

                selling_price = store_product['selling_price']
                item_total = Decimal(str(selling_price)) * product_number
                sum_total += item_total

                sale_entries.append({
                    'UPC': upc,
                    'product_number': product_number,
                    'selling_price': selling_price,
                })

            # Apply customer card discount
            if card_number:
                customer = self.customer_card_repository.get_by_number(card_number)
                if customer:
                    discount = Decimal(str(customer['percent'])) / Decimal('100')
                    sum_total = sum_total * (Decimal('1') - discount)

            vat = sum_total * Decimal('0.2')

            check_number = self.check_repository.generate_check_number()

            check_data = {
                'check_number': check_number,
                'id_employee': id_employee,
                'card_number': card_number if card_number else None,
                'print_date': timezone.now(),
                'sum_total': sum_total,
                'vat': vat,
            }
            self.check_repository.create(check_data)

            for entry in sale_entries:
                self.sale_repository.create(
                    upc=entry['UPC'],
                    check_number=check_number,
                    product_number=entry['product_number'],
                    selling_price=entry['selling_price'],
                )
                self.store_product_repository.update_stock(entry['UPC'], -entry['product_number'])

            return self.get_check_by_number(check_number)

    def delete_check(self, check_number: str):
        check = self.check_repository.get_by_number(check_number)
        if not check:
            raise ValueError(f"Чек з номером {check_number} не знайдено.")
        try:
            self.check_repository.delete(check_number)
        except IntegrityError:
            raise ValueError(
                "Цей чек неможливо видалити."
            )
