from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. MODELO DE USUARIO: Nos permite tener Jefe/Rescatista y DNI
class UsuarioBombero(AbstractUser):
    # Definimos los niveles de acceso. El primer valor va a la base de datos, el segundo se ve en pantalla.
    ROLES = [       
        ('jefe', 'Jefe de Unidad'),
        ('rescatista', 'Bombero Rescatista'),
    ]
    
    email = models.EmailField(unique=True, blank=False, null=False)
    documento = models.CharField(max_length=20, unique=True, verbose_name="DNI")
    rol = models.CharField(max_length=20, choices=ROLES, default='rescatista')
    is_approved = models.BooleanField(default=False, verbose_name="Aprobado por Jefe")

    def save(self, *args, **kwargs):
        # Solo el superusuario se aprueba automáticamente.
        # Los jefes y bomberos registrados quedan pendientes de aprobación.
        if self.is_superuser:
            self.is_approved = True
        super().save(*args, **kwargs)

    def __str__(self):
        estado_aprob = "Aprobado" if self.is_approved else "Pendiente"
        return f"{self.username} ({self.get_rol_display()}) - [{estado_aprob}]"


class Herramienta(models.Model):
    UBICACION_CHOICES = [
        ('estructural', 'Unidad Estructural'),
        ('rescate', 'Unidad de Rescate'),
        ('forestal', 'Unidad Forestal'),
        ('cisterna', 'Unidad Cisterna / Hidrante'),
        ('deposito', 'Depósito Central'),
    ]
    DISPONIBILIDAD_CHOICES = [
        ('Disponible', 'Disponible'),
        ('En Stock', 'En Stock'),
        ('En Uso', 'En Uso'),
        ('No Disponible', 'No Disponible'),
    ]
    ESTADO_CHOICES = [
        ('Funcional', 'Funcional'),
        ('En uso', 'En uso'),
        ('No funcional', 'No funcional'),
    ]

    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Funcional')
    disponibilidad = models.CharField(max_length=50, choices=DISPONIBILIDAD_CHOICES, default='Disponible')
    ubicacion = models.CharField(max_length=20, choices=UBICACION_CHOICES)
    unidad = models.ForeignKey('UnidadMovil', on_delete=models.SET_NULL, null=True, blank=True, related_name='herramientas', verbose_name="Unidad móvil")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}" 

# 3. MODELO DE NOTAS: Vincula una herramienta con el bombero que la usó/reportó
class NotaHerramienta(models.Model):

    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE, related_name='notas')

    usuario = models.ForeignKey(UsuarioBombero, on_delete=models.CASCADE)
    detalle = models.TextField(help_text="Describa el estado o qué sucedió con la herramienta.")
    fecha = models.DateTimeField(auto_now_add=True) # Se llena solo al crear la nota

    def __str__(self):
        return f"Nota de {self.herramienta.nombre} por {self.usuario.username}"


class RegistroActividad(models.Model):
    ACCIONES = [
        ('crear', 'Creación'),
        ('editar', 'Edición'),
        ('eliminar', 'Eliminación'),
    ]

    usuario = models.ForeignKey(UsuarioBombero, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    herramienta_codigo = models.CharField(max_length=10)
    herramienta_nombre = models.CharField(max_length=100)
    detalle = models.TextField(blank=True, default='')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_accion_display()} - {self.herramienta_codigo} por {self.usuario}"


class EventoCalendario(models.Model):
    fecha = models.DateField()
    titulo = models.CharField(max_length=200)
    usuario = models.ForeignKey(UsuarioBombero, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f"{self.fecha} - {self.titulo}"


# 6. MODELO PARTES DE GUARDIA: Asignación de revisiones por unidad y turno
class ParteGuardia(models.Model):
    TURNOS = [
        ('mañana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche'),
    ]
    ESTADO_PARTE = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
    ]

    fecha = models.DateField(verbose_name="Fecha")
    turno = models.CharField(max_length=10, choices=TURNOS, verbose_name="Turno")
    unidad = models.CharField(max_length=20, choices=Herramienta.UBICACION_CHOICES, verbose_name="Unidad")
    bombero = models.ForeignKey(UsuarioBombero, on_delete=models.CASCADE, related_name='partes_asignados', verbose_name="Bombero asignado")
    estado = models.CharField(max_length=20, choices=ESTADO_PARTE, default='pendiente', verbose_name="Estado")
    observaciones = models.TextField(blank=True, default='', verbose_name="Observaciones generales")
    creado = models.DateTimeField(auto_now_add=True)
    completado = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha', '-id']

    def __str__(self):
        return f"Parte {self.fecha} {self.get_turno_display()} - {self.get_unidad_display()}"


# 7. MODELO DETALLE DE PARTE: Estado reportado por herramienta en un parte
class ParteDetalle(models.Model):
    ESTADOS_REPORTE = [
        ('Disponible', 'Disponible'),
        ('En Uso', 'En Uso'),
        ('No Disponible', 'No Disponible'),
    ]

    parte = models.ForeignKey(ParteGuardia, on_delete=models.CASCADE, related_name='detalles')
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    estado_reporte = models.CharField(max_length=50, choices=ESTADOS_REPORTE, verbose_name="Estado reportado")
    observacion = models.CharField(max_length=200, blank=True, default='', verbose_name="Observación")

    def __str__(self):
        return f"{self.herramienta.codigo} - {self.get_estado_reporte_display()}"


# 8. MODELO SITIO: Cuartel Central y Destacamentos
class Sitio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del sitio")
    localidad = models.CharField(max_length=100, blank=True, default='', verbose_name="Localidad")
    dotacion = models.PositiveIntegerField(default=0, verbose_name="Dotación (bomberos activos)")
    descripcion = models.TextField(blank=True, default='', verbose_name="Descripción")

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.localidad})"


# 9. MODELO UNIDAD MÓVIL: Vehículos del parque automotor
class UnidadMovil(models.Model):
    CLASIFICACIONES = [
        ('primera_salida', 'Primera Salida / Estructural'),
        ('rescate_vehicular', 'Rescate Vehicular'),
        ('forestal', 'Incendio Forestal'),
        ('escalera', 'Escalera / Altura'),
        ('cisterna', 'Cisterna / Abastecimiento'),
        ('ambulancia', 'Ambulancia / Sanitario'),
        ('utilitario', 'Utilitario / Transporte'),
        ('especial', 'Equipo Especial'),
    ]
    ESTADOS_OPERATIVOS = [
        ('base', 'En Base'),
        ('servicio', 'En Servicio'),
        ('ruta', 'En Ruta'),
        ('mantenimiento', 'En Mantenimiento'),
    ]

    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name='unidades', verbose_name="Sitio")
    nombre = models.CharField(max_length=100, verbose_name="Denominación", help_text="Ej: Unidad 1, Unidad 21, Unimog...")
    clasificacion = models.CharField(max_length=30, choices=CLASIFICACIONES, verbose_name="Tipo / Función")
    funcion = models.CharField(max_length=200, blank=True, default='', verbose_name="Función detallada")
    modelo = models.CharField(max_length=100, blank=True, default='', verbose_name="Modelo / Marca")
    capacidad_personal = models.PositiveIntegerField(null=True, blank=True, verbose_name="Capacidad de personal")
    capacidad_agua = models.PositiveIntegerField(null=True, blank=True, verbose_name="Capacidad de agua (L)")
    equipamiento = models.TextField(blank=True, default='', verbose_name="Equipamiento técnico")
    estado_operativo = models.CharField(max_length=20, choices=ESTADOS_OPERATIVOS, default='base', verbose_name="Estado operativo")

    class Meta:
        ordering = ['sitio', 'nombre']

    def __str__(self):
        return f"{self.nombre} - {self.sitio.nombre}"