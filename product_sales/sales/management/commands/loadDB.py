import json
from django.core.management.base import BaseCommand
from sales.models import Item
from django.db import transaction
class Command(BaseCommand):
    help = 'Load items from a JSON file into the Item model'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            Item.objects.all().delete()
        # read data
        with open('./input_data.json', 'r') as file:
            data = json.load(file)  
            for item_data in data:
                # Create or update the Item based on `id`
                item, created = Item.objects.update_or_create(
                    id=item_data['id'],  # Use 'id' for matching items
                    defaults={
                        'name': item_data['name'],
                        'category': item_data['category'],
                        'description': item_data['description'],
                        'count': item_data['count'],
                        'image': item_data['image'],
                        'price': item_data['price']
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created new item '{item.name}'"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated item '{item.name}'"))
