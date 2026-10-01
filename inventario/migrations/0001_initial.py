# Generated for Inventario TI
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Edificio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("direccion", models.CharField(blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name="Piso",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=80)),
                ("orden", models.PositiveIntegerField(default=1)),
                ("edificio", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="pisos", to="inventario.edificio")),
            ],
            options={"ordering": ["edificio", "orden"]},
        ),
        migrations.CreateModel(
            name="Oficina",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("codigo", models.CharField(blank=True, max_length=30)),
                ("piso", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="oficinas", to="inventario.piso")),
            ],
        ),
        migrations.CreateModel(
            name="Puesto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=40)),
                ("x", models.PositiveSmallIntegerField(default=50, help_text="Posición horizontal 0-100")),
                ("y", models.PositiveSmallIntegerField(default=50, help_text="Posición vertical 0-100")),
                ("activo", models.BooleanField(default=True)),
                ("oficina", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="puestos", to="inventario.oficina")),
            ],
            options={"unique_together": {("oficina", "codigo")}},
        ),
        migrations.CreateModel(
            name="Persona",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre_completo", models.CharField(max_length=160)),
                ("cargo", models.CharField(blank=True, max_length=120)),
                ("area", models.CharField(blank=True, max_length=120)),
                ("correo", models.EmailField(blank=True, max_length=254)),
                ("telefono", models.CharField(blank=True, max_length=40)),
                ("activo", models.BooleanField(default=True)),
                ("puesto", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="persona", to="inventario.puesto")),
            ],
            options={"ordering": ["nombre_completo"]},
        ),
        migrations.CreateModel(
            name="PuntoRed",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=60, unique=True)),
                ("switch", models.CharField(blank=True, max_length=80)),
                ("puerto_switch", models.CharField(blank=True, max_length=30)),
                ("patch_panel", models.CharField(blank=True, max_length=80)),
                ("puerto_patch", models.CharField(blank=True, max_length=30)),
                ("vlan", models.CharField(blank=True, max_length=30)),
                ("activo", models.BooleanField(default=True)),
                ("puesto", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="puntos_red", to="inventario.puesto")),
            ],
        ),
        migrations.CreateModel(
            name="Equipo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo_activo", models.CharField(max_length=60, unique=True)),
                ("tipo", models.CharField(choices=[("PC", "Computadora"), ("LAPTOP", "Laptop"), ("MONITOR", "Monitor"), ("IMPRESORA", "Impresora"), ("TELEFONO", "Teléfono IP"), ("OTRO", "Otro")], default="PC", max_length=20)),
                ("marca", models.CharField(blank=True, max_length=80)),
                ("modelo", models.CharField(blank=True, max_length=100)),
                ("numero_serie", models.CharField(blank=True, max_length=120)),
                ("sistema_operativo", models.CharField(blank=True, max_length=120)),
                ("ip", models.GenericIPAddressField(blank=True, null=True)),
                ("mac", models.CharField(blank=True, max_length=30)),
                ("estado", models.CharField(choices=[("ACTIVO", "Activo"), ("ALMACEN", "Almacén"), ("REPARACION", "En reparación"), ("BAJA", "Baja")], default="ACTIVO", max_length=20)),
                ("observaciones", models.TextField(blank=True)),
                ("persona", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="equipos", to="inventario.persona")),
                ("puesto", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="equipos", to="inventario.puesto")),
                ("punto_red", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="equipos", to="inventario.puntored")),
            ],
        ),
        migrations.CreateModel(
            name="Movimiento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateTimeField(auto_now_add=True)),
                ("motivo", models.CharField(blank=True, max_length=250)),
                ("persona", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="movimientos", to="inventario.persona")),
                ("puesto_destino", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="movimientos_destino", to="inventario.puesto")),
                ("puesto_origen", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="movimientos_origen", to="inventario.puesto")),
            ],
            options={"ordering": ["-fecha"]},
        ),
    ]
