from django.core.management.base import BaseCommand
from table.models import User
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = []
        for i in range(999900):
            users.append(User(first_name=fake.first_name(), last_name = fake.last_name(), birthday = fake.date()))
            if len(users) == 1000:
                print(i)
                User.objects.bulk_create(users)
                users = []
        if len(users) > 0:
            User.objects.bulk_create(users)

