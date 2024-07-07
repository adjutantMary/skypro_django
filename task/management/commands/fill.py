from django.core.management import BaseCommand
import json
from task.catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open("catalog.json", encoding="utf-8") as file:
            data = json.load(file)
        return [item for item in data if item["model"] == "catalog.category"]

    @staticmethod
    def json_read_products():
        with open("catalog.json", encoding="utf-8") as file:
            data = json.load(file)
        return [item for item in data if item["model"] == "catalog.product"]

    def handle(self, *args, **options):

        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(
                Category(
                    id=category["pk"], category_name=category["fields"]["category_name"],
                    category_description=category["fields"]["category_description"]
                )
            )
        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(
                Product(
                    id=product["pk"],
                    product_name=product["fields"]["product_name"],
                    product_description=product["fields"]["product_description"],
                    category=Category.objects.get(pk=product["fields"]["category_name"]),
                    product_cost=product["fields"]["product_cost"],
                )
            )

        Product.objects.bulk_create(product_for_create)

