from django.core.management.base import BaseCommand
from inventario.models import Edificio, Piso, Oficina, Puesto, Persona, PuntoRed, Equipo

class Command(BaseCommand):
    help = "Crea datos de demostración"

    def handle(self, *args, **options):
        edificio, _ = Edificio.objects.get_or_create(nombre="Edificio Central")
        piso, _ = Piso.objects.get_or_create(edificio=edificio, nombre="Piso 2", defaults={"orden": 2})

        contabilidad, _ = Oficina.objects.get_or_create(piso=piso, nombre="Contabilidad", codigo="203")
        rrhh, _ = Oficina.objects.get_or_create(piso=piso, nombre="Recursos Humanos", codigo="202")
        sistemas, _ = Oficina.objects.get_or_create(piso=piso, nombre="Sistemas", codigo="205")

        p1, _ = Puesto.objects.get_or_create(oficina=contabilidad, codigo="P-01", defaults={"x": 26, "y": 35})
        p2, _ = Puesto.objects.get_or_create(oficina=rrhh, codigo="P-02", defaults={"x": 60, "y": 35})
        p3, _ = Puesto.objects.get_or_create(oficina=sistemas, codigo="P-03", defaults={"x": 43, "y": 70})

        maria, _ = Persona.objects.get_or_create(
            nombre_completo="María González Pérez",
            defaults={"cargo": "Contadora", "area": "Contabilidad", "correo": "maria@empresa.local", "puesto": p1},
        )
        juan, _ = Persona.objects.get_or_create(
            nombre_completo="Juan Pérez",
            defaults={"cargo": "Analista", "area": "Recursos Humanos", "correo": "juan@empresa.local", "puesto": p2},
        )
        carlos, _ = Persona.objects.get_or_create(
            nombre_completo="Carlos Rojas",
            defaults={"cargo": "Soporte TI", "area": "Sistemas", "correo": "carlos@empresa.local", "puesto": p3},
        )

        red1, _ = PuntoRed.objects.get_or_create(
            codigo="RED-22",
            defaults={"puesto": p1, "switch": "SW-P2-01", "puerto_switch": "Gi0/22", "patch_panel": "PP-02", "puerto_patch": "22", "vlan": "20"},
        )

        Equipo.objects.get_or_create(
            codigo_activo="PC-031",
            defaults={"tipo": "PC", "marca": "Dell", "modelo": "OptiPlex", "persona": maria, "puesto": p1, "punto_red": red1, "ip": "192.168.20.31", "mac": "00:11:22:33:44:31", "sistema_operativo": "Windows 11 Pro"},
        )
        Equipo.objects.get_or_create(codigo_activo="PC-023", defaults={"tipo": "PC", "marca": "HP", "persona": juan, "puesto": p2})
        Equipo.objects.get_or_create(codigo_activo="PC-045", defaults={"tipo": "PC", "marca": "Lenovo", "persona": carlos, "puesto": p3})

        self.stdout.write(self.style.SUCCESS("Datos demo creados correctamente."))
