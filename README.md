# 🚒 Sistema de Gestión - Cuartel de Bomberos

Producto Mínimo Viable (PMV) desarrollado en **Django** para la gestión operativa, inventario crítico y partes de guardia.

## 🎥 Video Tutorial

[Ver video explicativo en YouTube](https://youtu.be/D4GwhBEr-FY)

---

## 🚀 Inicio Rápido

1. **Clonar el repo**:
   ```bash
   git clone <url-del-repo>
   cd Central
   ```

2. **Levantar el sistema**:
   ```bash
   docker-compose up --build
   ```

3. **Acceder**: Abrí [http://localhost:8000](http://localhost:8000)

---

## 🔑 Cuentas de Prueba (Autogeneradas)

El sistema se autopuebla con datos reales y las siguientes cuentas:

| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|----------|
| Jefe de Unidad | `jefe` | `jefepassword123` | Acceso total + Panel de control |
| Bombero Rescatista | `bombero` | `bomberopassword123` | Carga de partes de guardia |

---

## 🏗 Arquitectura - Múltiples Apps con URLs

El framework de **URLs de Django** permite derivar en múltiples aplicaciones desde un punto de entrada único. En este proyecto, dos apps independientes comparten la misma base de datos y puerto:

| Ruta | App | Funcionalidad |
|------|-----|---------------|
| `/` | inventario | Home, stock, herramientas, unidades |
| `/panel/` | inventario | Panel de control del jefe y bombero |
| `/partes/` | inventario | Partes de guardia |
| `/exportar/` | inventario | Reportes CSV, Excel, PDF |
| `/login/` | usuarios | Inicio de sesión |
| `/registro/` | usuarios | Registro de nuevos bomberos |
| `/recuperar-clave/` | usuarios | Recuperación de contraseña |

La configuración central en `central_gestion/urls.py` incluye las apps:
```python
urlpatterns = [
    path('', include('inventario.urls')),
    path('', include('usuarios.urls')),
]
```

Este enfoque es el **mayor valor agregado** del framework: escalar a nuevas funcionalidades sumando apps sin configuración adicional.

---

## 🛠 Características Técnicas
*   **Dockerizado**: Despliegue en un solo paso.
*   **Roles (RBAC)**: Permisos diferenciados por rango.
*   **Recuperación de Clave**: Integración con SMTP de Gmail.
*   **Reportes**: Exportación a Excel, CSV y PDF.
*   **Arquitectura**: Python 3.12, Django 6.0, PostgreSQL 15.
