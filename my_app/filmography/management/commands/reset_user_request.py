from django.apps import apps
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        users_requests = apps.get_model("filmography.UserProfile").objects.all()
        users_requests.update(daily_api_counter=0)