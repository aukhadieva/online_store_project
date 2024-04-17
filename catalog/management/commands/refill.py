import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories() -> list[dict]:
        """
        Получает данные из фикстур с категориями.
        """
        with open('category.json') as j_file:
            load_categories = json.load(j_file)
            commands_list = []
            for item in load_categories:
                commands_list.append(item)
            return commands_list

    @staticmethod
    def json_read_products() -> list[dict]:
        """
        Получает данные из фикстур с продуктами.
        """
        with open('product.json') as j_file:
            load_products = json.load(j_file)
            commands_list = []
            for item in load_products:
                commands_list.append(item)
            return commands_list

    def handle(self, *args, **options) -> None:
        """
        Заполняет данные в базу данных, предварительно зачистив ее от старых данных.
        """
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories_for_create = []
        product_for_create = []

        for categories in Command.json_read_categories():
            categories_for_create.append(Category(id=categories["pk"],
                                         category_name=categories["fields"]["category_name"],
                                         cat_desc=categories["fields"]["cat_desc"]))

        Category.objects.bulk_create(categories_for_create)

        for products in Command.json_read_products():
            product_for_create.append(Product(id=products["pk"], category=Category.objects.get(pk=2),
                                              in_stock=products['fields']['in_stock'],
                                              price=products['fields']['price'],
                                              prod_desc=products['fields']['prod_desc'],
                                              product_name=products['fields']['product_name']))

        Product.objects.bulk_create(product_for_create)
