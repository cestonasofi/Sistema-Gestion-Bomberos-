import os

from django.core.management.base import BaseCommand, CommandError
from inventario.models import UsuarioBombero


class Command(BaseCommand):
    help = (
        "Crea o actualiza las cuentas de jefe, bombero y admin. "
        "Las contraseñas se leen del archivo .env (JEFE_PASSWORD, BOMBERO_PASSWORD, ADMIN_PASSWORD)."
    )

    def handle(self, *args, **options):
        jefe_pass = os.getenv('JEFE_PASSWORD', '')
        bombero_pass = os.getenv('BOMBERO_PASSWORD', '')
        admin_pass = os.getenv('ADMIN_PASSWORD', '')

        faltantes = []
        if not jefe_pass:
            faltantes.append('JEFE_PASSWORD')
        if not bombero_pass:
            faltantes.append('BOMBERO_PASSWORD')
        if not admin_pass:
            faltantes.append('ADMIN_PASSWORD')
        if faltantes:
            raise CommandError(
                'Faltan definir en el archivo .env: ' + ', '.join(faltantes)
            )

        self.stdout.write("--- CREANDO CUENTAS DE ACCESO ---")

        # 1. Usuario Jefe (acceso total)
        u_jefe, _ = UsuarioBombero.objects.get_or_create(
            username='jefe',
            defaults={
                'email': 'jefe@cuartel.gob',
                'documento': '22222222',
                'rol': 'jefe',
                'is_approved': True,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        u_jefe.set_password(jefe_pass)
        u_jefe.rol = 'jefe'
        u_jefe.is_approved = True
        u_jefe.is_staff = True
        u_jefe.is_superuser = True
        u_jefe.save()
        self.stdout.write(self.style.SUCCESS('[OK] Cuenta Jefe creada/actualizada.'))

        # 2. Usuario Bombero Rescatista
        u_bombero, _ = UsuarioBombero.objects.get_or_create(
            username='bombero',
            defaults={
                'email': 'bombero@cuartel.gob',
                'documento': '33333333',
                'rol': 'rescatista',
                'is_approved': True,
            },
        )
        u_bombero.set_password(bombero_pass)
        u_bombero.rol = 'rescatista'
        u_bombero.is_approved = True
        u_bombero.save()
        self.stdout.write(self.style.SUCCESS('[OK] Cuenta Bombero creada/actualizada.'))

        # 3. Usuario Admin (superusuario)
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
        u_admin.set_password(admin_pass)
        u_admin.is_approved = True
        u_admin.save()
        self.stdout.write(self.style.SUCCESS('[OK] Cuenta Admin creada/actualizada.'))
