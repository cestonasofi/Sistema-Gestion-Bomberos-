from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Herramienta, UsuarioBombero, NotaHerramienta, RegistroActividad, EventoCalendario, ParteGuardia, ParteDetalle, Sitio, UnidadMovil

@admin.register(UsuarioBombero)
class UsuarioBomberoAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('documento', 'rol', 'is_approved')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('documento', 'rol', 'email', 'is_approved')}),
    )
    list_display = ('username', 'email', 'documento', 'rol', 'is_approved', 'is_staff')

@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'ubicacion', 'estado', 'disponibilidad')
    search_fields = ('codigo', 'nombre')

@admin.register(NotaHerramienta)
class NotaHerramientaAdmin(admin.ModelAdmin):
    list_display = ('herramienta', 'usuario', 'fecha')
    list_filter = ('fecha', 'usuario')

@admin.register(RegistroActividad)
class RegistroActividadAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'accion', 'herramienta_codigo', 'herramienta_nombre', 'usuario')
    list_filter = ('accion', 'fecha')
    search_fields = ('herramienta_codigo', 'herramienta_nombre')

@admin.register(EventoCalendario)
class EventoCalendarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'titulo', 'usuario', 'creado')
    list_filter = ('fecha',)

@admin.register(Sitio)
class SitioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'localidad', 'dotacion')

@admin.register(UnidadMovil)
class UnidadMovilAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sitio', 'clasificacion', 'modelo', 'estado_operativo', 'capacidad_agua')
    list_filter = ('sitio', 'clasificacion', 'estado_operativo')
    search_fields = ('nombre', 'modelo')

@admin.register(ParteGuardia)
class ParteGuardiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'turno', 'unidad', 'bombero', 'estado', 'completado')
    list_filter = ('fecha', 'turno', 'estado')
    search_fields = ('bombero__username', 'observaciones')

@admin.register(ParteDetalle)
class ParteDetalleAdmin(admin.ModelAdmin):
    list_display = ('parte', 'herramienta', 'estado_reporte', 'observacion')
    list_filter = ('estado_reporte',)
    search_fields = ('herramienta__codigo', 'herramienta__nombre')