"""
Management command для инициализации начальных данных
"""

from django.core.management.base import BaseCommand
from apps.benchmark.models import Bank, Product, Criterion, Source


class Command(BaseCommand):
    help = 'Initialize sample data for benchmarking'

    def handle(self, *args, **options):
        self.stdout.write('Initializing data...')

        # Create banks
        banks_data = [
            ('sber', 'Сбербанк'),
            ('vtb', 'ВТБ'),
            ('alfa', 'Альфа-Банк'),
            ('uralsib', 'УралСиб'),
            ('gazprombank', 'Газпромбанк'),
        ]

        for bank_id, bank_name in banks_data:
            bank, created = Bank.objects.get_or_create(
                id=bank_id,
                defaults={
                    'name': bank_name,
                    'website': f'https://{bank_id}.ru',
                }
            )
            if created:
                self.stdout.write(f'✓ Created bank: {bank_name}')

        # Create products
        products_data = [
            ('deposits', 'Вклады'),
            ('credits', 'Кредиты'),
            ('cards', 'Карты'),
            ('tariffs', 'Тарифы'),
        ]

        for product_id, product_name in products_data:
            product, created = Product.objects.get_or_create(
                id=product_id,
                defaults={'name': product_name}
            )
            if created:
                self.stdout.write(f'✓ Created product: {product_name}')

        # Create criteria
        criteria_data = [
            ('cost', 'Стоимость обслуживания'),
            ('sms', 'СМС-уведомления'),
            ('withdrawal', 'Снятие наличных в других банках'),
            ('transfers', 'Переводы по реквизитам'),
            ('interest', 'Процент на остаток'),
            ('limit', 'Кредитный лимит'),
            ('rate', 'Процентные ставки'),
            ('payment', 'Первоначальный взнос'),
            ('loyalty', 'Программа лояльности'),
            ('cashback', 'Кэшбэк'),
            ('grace', 'Льготный период'),
        ]

        for criterion_id, criterion_name in criteria_data:
            criterion, created = Criterion.objects.get_or_create(
                id=criterion_id,
                defaults={'name': criterion_name}
            )
            if created:
                self.stdout.write(f'✓ Created criterion: {criterion_name}')

        # Create sources
        sources_data = [
            ('Banki.ru', 'https://banki.ru', 'Портал о банках и финансах'),
            ('Sravni.ru', 'https://sravni.ru', 'Сравнение банковских продуктов'),
            ('Frankrg.com', 'https://frankrg.com', 'Рейтинги банков'),
            ('RBK.ru', 'https://www.rbc.ru/quotes', 'РБК котировки и рынки'),
        ]

        for source_name, source_url, description in sources_data:
            source, created = Source.objects.get_or_create(
                name=source_name,
                defaults={
                    'url': source_url,
                    'description': description,
                }
            )
            if created:
                self.stdout.write(f'✓ Created source: {source_name}')

        self.stdout.write(self.style.SUCCESS('✓ Data initialization completed!'))
