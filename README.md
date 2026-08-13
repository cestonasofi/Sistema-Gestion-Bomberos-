# Sistema de Gestión de Cuartel de Bomberos

Sistema web profesional desarrollado con **Django** para el control, monitoreo e inventario de herramientas, materiales y dotación operativa de un cuartel de bomberos. Cuenta con módulos completos de partes de guardia, calendario de inspecciones, contenedorización con Docker, recuperación de contraseñas por correo electrónico y control de acceso basado en roles (RBAC).

---

## 🚀 Funcionalidades Principales

### 1. Autenticación, Seguridad y Roles (RBAC)
- **Registro público y roles diferenciados**: Los usuarios pueden registrarse seleccionando su rol (`Bombero Rescatista` o `Jefe de Unidad / Comandante`).
- **Aprobación de cuentas**: Las nuevas cuentas quedan pendientes de validación por seguridad; el primer jefe registrado se aprueba automáticamente y los siguientes requieren validación desde el **Panel de Control**.
- **Recuperación de contraseña**: Módulo integrado de recupero de clave vía correo electrónico utilizando servidor SMTP (Gmail).
- **Control por Roles**:
  - **Jefe de Unidad**: Acceso total (crear, editar, eliminar herramientas y unidades, aprobar personal, asignar partes de guardia, agendar eventos y vaciar auditoría).
  - **Bombero Rescatista**: Consulta de inventario, reporte de estado y completado de partes de guardia asignados.

### 2. Contenedorización con Docker
- **Docker & Docker Compose**: Configuración completa para desplegar el sistema en cualquier entorno con un solo comando, levantando el servidor web y aplicando migraciones automáticamente.

### 3. Inventario Operativo por Unidades y Depósito
- **Clasificación por Unidades Operativas**:
  - *Unidad Estructural*: Equipos ERA, tramos de línea, lanzas, herramientas de entrada forzada.
  - *Unidad de Rescate*: Tijeras hidráulicas, expansores, tablas espinales, DEA, botiquines.
  - *Unidad Forestal*: Mochilas de agua, pulaskis, batefuegos, motobombas.
  - *Unidad Cisterna / Hidrante*: Mangotes, tramos de abastecimiento, llaves de paso.
  - *Depósito Central*: Espumógenos, combustible de reserva, repuestos.
- **Estados de disponibilidad fijos**: Disponible, En Stock, En Uso, No Disponible (con control de notas de novedades/averías).

### 4. Partes de Guardia
- Asignación de revisiones por unidad a cada bombero y turno.
- Al completar el parte, el sistema actualiza automáticamente la disponibilidad del inventario, registra notas automáticas y genera un registro de actividad.

### 5. Calendario de Inspecciones y Panel de Control
- Calendario interactivo con carga y gestión de eventos e inspecciones.
- Métricas y totales en tiempo real con gráficos de estado y distribución.
- Modo oscuro / modo claro integrado.

### 6. Exportación y Reportes
- Exportación del inventario completo a **Excel** (.xlsx) o **CSV**.
- Reporte imprimible y generación de versión descargable en **PDF**.

---

## 🛠️ Requisitos Técnicos

- Python 3.10 o superior (Django 6.0.4)
- Docker y Docker Compose (opcional para despliegue contenerizado)

---

## 📦 Configuración y Ejecución Local

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/cestonasofi/Sistema-Gestion-Bomberos-.git
   cd Sistema-Gestion-Bomberos-/central_bomberos
   ```

2. **Crear el archivo `.env` en la carpeta `central_bomberos/`**
   ```env
   SECRET_KEY=tu_clave_secreta
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   JEFE_PASSWORD=jefepassword123
   BOMBERO_PASSWORD=bomberopassword123
   ADMIN_PASSWORD=admin123

   # Configuración de correo para recuperación de contraseña (SMTP)
   EMAIL_HOST_USER=tucorreo@gmail.com
   EMAIL_HOST_PASSWORD=contraseña_de_aplicacion
   ```

3. **Instalar dependencias y ejecutar migraciones**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   ```

4. **Poblar datos iniciales y crear cuentas**
   ```bash
   python manage.py poblar_cuartel
   python manage.py crear_cuentas
   ```

5. **Iniciar el servidor**
   ```bash
   python manage.py runserver
   ```
   Acceder en el navegador a `http://127.0.0.1:8000/`.

---

## 🐳 Ejecución con Docker

Para levantar el sistema utilizando Docker Compose:

```bash
docker-compose up --build
```
El contenedor aplicará las migraciones automáticamente y dejará la aplicación accesible en `http://localhost:8000/`.

---

## 📂 Estructura del Proyecto

```text
central_bomberos/
├── central_gestion/         # Configuración principal de Django (settings, urls, wsgi)
├── inventario/              # Módulo principal (inventario, unidades, partes, calendario)
│   ├── management/commands/ # Comandos de gestión (poblar_cuartel, crear_cuentas, respaldar)
│   ├── migrations/          # Migraciones de base de datos
│   ├── models.py            # Modelos de datos (Herramienta, ParteGuardia, etc.)
│   ├── views.py             # Lógica de negocio, métricas y reportes
│   ├── urls.py              # Rutas optimizadas con namespace
│   ├── templates/inventario/# Plantillas HTML unificadas (base.html, index.html, etc.)
│   └── static/              # Archivos estáticos consolidados (style.css, script.js)
├── usuarios/                # Módulo de autenticación, registro y recuperación de password
├── manage.py                # Utilidad CLI de Django
├── requirements.txt         # Dependencias del proyecto
├── Dockerfile               # Configuración de imagen Docker
└── docker-compose.yml       # Orquestación de servicios Docker
```
