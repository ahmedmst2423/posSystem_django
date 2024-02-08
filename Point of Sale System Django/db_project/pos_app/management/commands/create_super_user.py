from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model



Operator = get_user_model()



class Command(BaseCommand):
    help = 'Create a superuser with Operator user type'

    def handle(self, *args, **options):
        superuser = Operator.objects.create_user(
            operator_id= 123,
            username='admin',
            password='hello',
            is_staff=True,
            is_superuser=True,
            email='admin@example.com',
            user_type='superuser',
            first_name = 'Admin',
            last_name = 'Null',
            salary = 10000,



        )

        # Optionally, set other fields if needed
        # superuser.first_name = 'Admin'

        superuser.save()
        self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))

        