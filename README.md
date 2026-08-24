# 🚒 Sistema de Gestión - Cuartel de Bomberos

Producto Mínimo Viable (PMV) desarrollado en **Django** para la gestión operativa, inventario crítico y partes de guardia.

## 🚀 Inicio Rápido (Un solo comando)

1. **Clonar el repo**:
   ```bash
   git clone <url-del-repo>
   cd Central
   ```

2. **Levantar el sistema**:
   ```bash
   docker-compose up --build
   ```

---

## 🔑 Cuentas de Prueba (Autogeneradas)

El sistema se autopuebla con datos reales y las siguientes cuentas:

*   **Jefe de Unidad**: `jefe` / `jefepassword123` (Acceso total + Panel de control)
*   **Bombero Rescatista**: `bombero` / `bomberopassword123` (Carga de partes de guardia)

---

## 🛠 Características Técnicas
*   **Dockerizado**: Despliegue en un solo paso.
*   **Roles (RBAC)**: Permisos diferenciados por rango.
*   **Recuperación de Clave**: Integración con SMTP de Gmail.
*   **Reportes**: Exportación a Excel, CSV y PDF.
*   **Arquitectura**: Python 3.12, Django 6.0, SQLite.
