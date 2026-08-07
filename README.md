# Sistema de Gestión de Cuartel de Bomberos

Sistema web desarrollado con **Django** para el control, monitoreo e inventario de herramientas, materiales y dotación operativa de un cuartel de bomberos, con módulos de partes de guardia, calendario de inspecciones y control de acceso por roles.

## Funcionalidades

1. **Inventario por unidades**
   - Unidad Estructural: ERA, tramos de línea, lanzas, herramientas de entrada forzada.
   - Unidad de Rescate: tijeras hidráulicas, expansores, tablas espinales, DEA, botiquines.
   - Unidad Forestal: mochilas de agua, pulaskis, batefuegos, motobombas.
   - Unidad Cisterna / Hidrante: mangotes, tramos de abastecimiento, llaves de paso.
   - Depósito Central: espumógenos, combustible de reserva, repuestos.

2. **Estados de disponibilidad fijos**
   - Disponible: equipo operativo listo para despacho.
   - En Stock: equipo almacenado sin asignación.
   - En Uso: equipo desplegado en servicio activo.
   - No Disponible: equipo en reparación, mantenimiento o fuera de servicio.

3. **Partes de Guardia**
   - Asignación de partes por unidad a cada bombero.
   - Completado de parte: actualiza automáticamente la disponibilidad de cada herramienta, crea notas automáticas y registra la actividad.

4. **Calendario de inspecciones**
   - Carga y gestión de eventos e inspecciones desde el Panel de Control.

5. **Registro de actividad y notas**
   - Historial de acciones (crear, editar, eliminar, completar partes).
   - Notas por herramienta (mantenimiento, novedades, reparaciones).
   - El Jefe puede vaciar el historial de actividad.

6. **Usuarios y control de acceso (RBAC)**
   - Jefe de Unidad / Comandante: acceso total (agregar, editar, eliminar herramientas, aprobar bomberos, asignar partes).
   - Bombero Rescatista: consulta de inventario, reporte de estado y completado de partes asignadas.
   - Registro público con selección de rol. Las cuentas quedan pendientes de aprobación por el Jefe; el primer jefe registrado se aprueba automáticamente.

7. **Panel de Control**
   - Métricas y totales en tiempo real calculados desde la base de datos.
   - Modo oscuro / modo claro.
   - Gestión de expedientes de personal.

8. **Responsive**
   - Diseño adaptado a celulares y tablets, con fondo de login personalizado.

9. **Exportación y reportes**
   - Exportar el inventario completo a **Excel** (.xlsx) o **CSV** desde el panel.
   - Reporte imprimible del inventario agrupado por unidad, con versión **PDF** descargable.

## Requisitos

- Python 3.10 o superior
- Django 6.0.4 (ver `requirements.txt`)

## Configuración inicial

Crear un archivo `.env` en la raíz del proyecto (no se sube a git). Ejemplo:

```env
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Contraseñas de las cuentas de acceso (python manage.py crear_cuentas)
JEFE_PASSWORD=cambiar_jefe
BOMBERO_PASSWORD=cambiar_bombero
ADMIN_PASSWORD=cambiar_admin

# Correo para el recupero de contraseña (opcional)
EMAIL_HOST_USER=tucorreo@gmail.com
EMAIL_HOST_PASSWORD=contraseña_de_aplicacion_google
```

Si se quiere acceder desde otros dispositivos de la red local, agregar la IP de la máquina a `ALLOWED_HOSTS` (por ejemplo `192.168.1.100`) y ejecutar el servidor con `0.0.0.0:8000`.

## Inicio rápido

1. **Clonar el repositorio e instalar dependencias**

   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd central_bomberos
   pip install -r requirements.txt
   ```

2. **Ejecutar migraciones**

   ```bash
   python manage.py migrate
   ```

3. **Cargar todos los datos del cuartel** (sitios, unidades móviles y el inventario completo de herramientas)

   ```bash
   python manage.py poblar_cuartel
   ```

4. **Crear cuentas de acceso** (jefe, bombero y admin)

   ```bash
   python manage.py crear_cuentas
   ```

   Usuarios: `jefe`, `bombero` y `admin`. Las contraseñas se definen en el archivo `.env`
   (variables `JEFE_PASSWORD`, `BOMBERO_PASSWORD`, `ADMIN_PASSWORD`) — nunca van en el código.

5. **Iniciar el servidor**

   ```bash
   python manage.py runserver
   ```

   Acceder en el navegador a `http://127.0.0.1:8000/`.

## Respaldo de la base de datos

Crea una copia de seguridad completa en la carpeta `backups/` (guarda los últimos 10):

```bash
python manage.py respaldar
```

Para restaurar: detener el servidor, reemplazar `db.sqlite3` por el respaldo deseado y volver a iniciar.

## Usuarios y permisos

| Rol        | Registro                    | Permisos                                                                 |
|------------|-----------------------------|--------------------------------------------------------------------------|
| Jefe       | Se crea con `manage.py crear_cuentas`, en `/admin`, o registrado en `/register` (el primero se aprueba automáticamente) | Acceso total: herramientas, aprobación de bomberos, partes, calendario, vaciar historial |
| Rescatista | Registro público en `/register` (queda pendiente de aprobación) | Consulta inventario, reporte de estado, completar partes asignadas |

## Rutas principales

| Ruta                    | Descripción                                  |
|-------------------------|----------------------------------------------|
| `/`                     | Panel de control / inventario                |
| `/configuracion/`       | Configuración y calendario de inspecciones   |
| `/agregar/`             | Agregar herramienta                          |
| `/editar/<id>/`         | Editar herramienta                           |
| `/partes/`              | Partes de guardia                            |
| `/partes/asignar/`      | Asignar parte de guardia                     |
| `/evento/agregar/`      | Agendar inspección en el calendario          |
| `/exportar/excel/`      | Descargar inventario en Excel                |
| `/exportar/csv/`        | Descargar inventario en CSV                  |
| `/reporte/`             | Reporte imprimible del inventario            |
| `/reporte/pdf/`         | Descargar reporte en PDF                     |
| `/admin/`               | Panel de administración de Django            |
| `/register/`            | Registro público de bomberos                 |

## Estructura del proyecto

```text
central_bomberos/
├── central_gestion/               # Configuración de Django (settings, urls, wsgi)
├── inventario/                    # Aplicación principal
│   ├── management/commands/       # Comandos: poblar_cuartel, crear_cuentas, respaldar
│   ├── migrations/                # Migraciones de base de datos
│   ├── models.py                  # UsuarioBombero, Herramienta, NotaHerramienta,
│   │                              # RegistroActividad, EventoCalendario, ParteGuardia, ParteDetalle
│   ├── forms.py                   # Formularios del sistema
│   ├── views.py                   # Lógica de negocio, métricas, exportación y reportes
│   ├── urls.py                    # Rutas de la aplicación
│   ├── templates/inventario/      # Plantillas HTML
│   └── static/                    # style.css, fondo_login.png
├── usuarios/                      # App de login y registro
├── manage.py                      # Utilidad de gestión de Django
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Imagen Docker
├── docker-compose.yml             # Orquestación Docker
└── README.md                      # Documentación
```

## Tecnologías utilizadas

- **Backend**: Python, Django
- **Base de datos**: SQLite (migrable a PostgreSQL)
- **Frontend**: HTML5, CSS, JavaScript (vanilla)
- **Configuración**: python-dotenv (variables de entorno en `.env`)
