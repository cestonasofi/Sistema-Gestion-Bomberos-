from django.core.management.base import BaseCommand
from inventario.models import UsuarioBombero


class Command(BaseCommand):
    help = "Crea o actualiza las cuentas de acceso."

    def handle(self, *args, **options):
        PASS = 'bombero123'

        self.stdout.write("--- CREANDO CUENTAS DE ACCESO ---")

        # 1. Sofia - Jefe (superusuario)
        try:
            viejo = UsuarioBombero.objects.get(username='jefe')
            viejo.delete()
            self.stdout.write(self.style.WARNING('[OK] Usuario "jefe" eliminado.'))
        except UsuarioBombero.DoesNotExist:
            pass

        u_sofia, _ = UsuarioBombero.objects.get_or_create(
            username='sofia',
            defaults={
                'email': 'sofia@cuartel.gob',
                'documento': '22222222',
                'rol': 'jefe',
                'is_approved': True,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        u_sofia.set_password(PASS)
        u_sofia.rol = 'jefe'
        u_sofia.is_approved = True
        u_sofia.is_staff = True
        u_sofia.is_superuser = True
        u_sofia.save()
        self.stdout.write(self.style.SUCCESS('[OK] sofia / bombero123'))

        # 2. Bombero
        u_bombero, _ = UsuarioBombero.objects.get_or_create(
            username='bombero',
            defaults={
                'email': 'bombero@cuartel.gob',
                'documento': '33333333',
                'rol': 'rescatista',
                'is_approved': True,
            },
        )
        u_bombero.set_password(PASS)
        u_bombero.rol = 'rescatista'
        u_bombero.is_approved = True
        u_bombero.save()
        self.stdout.write(self.style.SUCCESS('[OK] bombero / bombero123'))

        # 3. Admin
        u_admin, _ = UsuarioBombero.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@cuartel.gob',
                'documento': '00000000',
                'rol': 'jefe',
                'is_approved': True,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        u_admin.set_password(PASS)
        u_admin.is_approved = True
        u_admin.save()
        self.stdout.write(self.style.SUCCESS('[OK] admin / bombero123'))
