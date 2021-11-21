from django.apps import AppConfig

# a ten model niżej co robił?
class FilmographyConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    name = 'filmography'

    def ready(self):
        import filmography.signals
