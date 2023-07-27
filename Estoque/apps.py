from django.apps import AppConfig


class EstoqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Estoque'

    def ready(self):
        import os
        from .models import Usuario

        email = os.getenv('EMAIL_ADMIN')
        senha = os.getenv('SENHA_ADMIN')

        users = Usuario.objects.filter(email=email)

        if not users:
            Usuario.objects.create_user(username=email, email=email, password=senha,
                                        is_active=True, is_staff=True)