import os
import sqlite3
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea una copia de seguridad de la base de datos en la carpeta backups/."

    def handle(self, *args, **options):
        db_path = settings.DATABASES['default']['NAME']
        if not db_path or db_path == ':memory:':
            self.stderr.write('La base de datos configurada no es un archivo SQLite. No se pudo respaldar.')
            return

        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        nombre = datetime.now().strftime('respaldo_%Y%m%d_%H%M%S.sqlite3')
        destino = os.path.join(backup_dir, nombre)

        try:
            conn = sqlite3.connect(db_path)
            ruta_sql = destino.replace("'", "''")
            conn.execute("VACUUM INTO '{}'".format(ruta_sql))
            conn.close()
        except Exception as e:
            self.stderr.write('[ERROR] No se pudo crear el respaldo: {}'.format(e))
            return

        self.stdout.write(self.style.SUCCESS('[OK] Respaldo creado: {}'.format(destino)))

        # Mantener solo los últimos 10 respaldos
        respaldos = sorted(f for f in os.listdir(backup_dir) if f.endswith('.sqlite3'))
        eliminados = 0
        while len(respaldos) > 10:
            os.remove(os.path.join(backup_dir, respaldos.pop(0)))
            eliminados += 1
        if eliminados:
            self.stdout.write('Respaldo(s) antiguo(s) eliminado(s) para dejar solo los últimos 10: {}'.format(eliminados))
