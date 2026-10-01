from django.db import models


class Edificio(models.Model):
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.nombre


class Piso(models.Model):
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="pisos")
    nombre = models.CharField(max_length=80)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["edificio", "orden"]

    def __str__(self):
        return f"{self.edificio} - {self.nombre}"


class Oficina(models.Model):
    piso = models.ForeignKey(Piso, on_delete=models.CASCADE, related_name="oficinas")
    nombre = models.CharField(max_length=120)
    codigo = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.piso})"


class Puesto(models.Model):
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE, related_name="puestos")
    codigo = models.CharField(max_length=40)
    x = models.PositiveSmallIntegerField(default=50, help_text="Posición horizontal 0-100")
    y = models.PositiveSmallIntegerField(default=50, help_text="Posición vertical 0-100")
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ("oficina", "codigo")

    def __str__(self):
        return f"{self.oficina.nombre} - {self.codigo}"


class Persona(models.Model):
    nombre_completo = models.CharField(max_length=160)
    cargo = models.CharField(max_length=120, blank=True)
    area = models.CharField(max_length=120, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=40, blank=True)
    puesto = models.OneToOneField(
        Puesto, on_delete=models.SET_NULL, null=True, blank=True, related_name="persona"
    )
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre_completo"]

    def __str__(self):
        return self.nombre_completo


class PuntoRed(models.Model):
    puesto = models.ForeignKey(Puesto, on_delete=models.SET_NULL, null=True, blank=True, related_name="puntos_red")
    codigo = models.CharField(max_length=60, unique=True)
    switch = models.CharField(max_length=80, blank=True)
    puerto_switch = models.CharField(max_length=30, blank=True)
    patch_panel = models.CharField(max_length=80, blank=True)
    puerto_patch = models.CharField(max_length=30, blank=True)
    vlan = models.CharField(max_length=30, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo


class Equipo(models.Model):
    TIPOS = [
        ("PC", "Computadora"),
        ("LAPTOP", "Laptop"),
        ("MONITOR", "Monitor"),
        ("IMPRESORA", "Impresora"),
        ("TELEFONO", "Teléfono IP"),
        ("OTRO", "Otro"),
    ]
    ESTADOS = [
        ("ACTIVO", "Activo"),
        ("ALMACEN", "Almacén"),
        ("REPARACION", "En reparación"),
        ("BAJA", "Baja"),
    ]

    codigo_activo = models.CharField(max_length=60, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default="PC")
    marca = models.CharField(max_length=80, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=120, blank=True)
    sistema_operativo = models.CharField(max_length=120, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    mac = models.CharField(max_length=30, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="ACTIVO")
    persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipos")
    puesto = models.ForeignKey(Puesto, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipos")
    punto_red = models.ForeignKey(PuntoRed, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipos")
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.codigo_activo} - {self.get_tipo_display()}"


class Movimiento(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="movimientos")
    puesto_origen = models.ForeignKey(Puesto, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimientos_origen")
    puesto_destino = models.ForeignKey(Puesto, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimientos_destino")
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.persona} - {self.fecha:%d/%m/%Y %H:%M}"
