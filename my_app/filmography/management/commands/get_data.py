from django.apps import apps
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        api_requests = apps.get_model("filmography.ActorUserRequest").objects.filter(status='p')
        if api_requests.exists():
            obj = api_requests.last()
            obj.set_response()