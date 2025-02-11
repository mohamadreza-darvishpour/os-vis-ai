from django.apps import AppConfig


class SellingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'selling'


    def ready(self):
        import selling.templatetags.custom_filters