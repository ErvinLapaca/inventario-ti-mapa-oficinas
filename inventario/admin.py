from django.contrib import admin
from .models import Edificio, Piso, Oficina, Puesto, Persona, PuntoRed, Equipo, Movimiento

@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    search_fields = ("nombre", "direccion")

@admin.register(Piso)
class PisoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "edificio", "orden")
    list_filter = ("edificio",)

@admin.register(Oficina)
class OficinaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "piso")
    list_filter = ("piso__edificio", "piso")
    search_fields = ("nombre", "codigo")

@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "oficina", "x", "y", "activo")
    list_filter = ("activo", "oficina__piso")

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "cargo", "area", "puesto", "activo")
    list_filter = ("activo", "area")
    search_fields = ("nombre_completo", "cargo", "area", "correo")

@admin.register(PuntoRed)
class PuntoRedAdmin(admin.ModelAdmin):
    list_display = ("codigo", "puesto", "switch", "puerto_switch", "vlan", "activo")
    list_filter = ("activo", "vlan")
    search_fields = ("codigo", "switch", "puerto_switch", "patch_panel")

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("codigo_activo", "tipo", "marca", "modelo", "persona", "ip", "estado")
    list_filter = ("tipo", "estado", "marca")
    search_fields = ("codigo_activo", "numero_serie", "ip", "mac", "persona__nombre_completo")

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("persona", "puesto_origen", "puesto_destino", "fecha", "motivo")
    search_fields = ("persona__nombre_completo", "motivo")
