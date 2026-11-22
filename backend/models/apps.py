from django.apps import AppConfig


class ModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'models'
    label = 'core'
    verbose_name = 'Domain models'

    def ready(self):
        import models.clients  # noqa: F401
        import models.tokens  # noqa: F401
        import models.user  # noqa: F401


    def ready(self):
        import models.clients  # noqa: F401
        import models.tokens  # noqa: F401
        import models.user  # noqa: F401

