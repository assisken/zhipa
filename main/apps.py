from django.apps import AppConfig


class SmiapConfig(AppConfig):
    name = "main"

    def ready(self) -> None:
        import main.signals  # noqa
