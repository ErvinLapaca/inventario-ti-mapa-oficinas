# Inventario TI – Mapa de Oficinas

Aplicación web para visualizar y administrar usuarios, oficinas, puestos, equipos y puntos de red en un mapa interactivo.

## Versión 0.2

Incluye:

- Edificios, pisos, oficinas y puestos.
- Personas con nombre, cargo, área, correo y teléfono.
- Equipos: PC, laptop, monitor, impresora, teléfono y otros.
- Red: IP, MAC, punto, switch, puerto, patch panel y VLAN.
- Asignación de equipos y puntos de red.
- Mapa visual por coordenadas X/Y.
- Ficha emergente de usuario.
- Iconos visuales para equipos y red.
- Movimiento manual de usuarios.
- **Arrastrar y soltar usuarios entre puestos**.
- Registro automático del historial de movimientos.
- Validación para evitar colocar dos personas en el mismo puesto.
- Buscador por persona, cargo, área, equipo, IP, MAC o punto de red.
- Panel de administración Django.

## Instalación / actualización

```bash
git clone https://github.com/ErvinLapaca/inventario-ti-mapa-oficinas.git
cd inventario-ti-mapa-oficinas

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Si ya lo habías descargado:

```bash
git pull
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrir:

- Sistema: http://127.0.0.1:8000/
- Administración: http://127.0.0.1:8000/admin/

## Uso del mapa

1. Crea edificios, pisos, oficinas y puestos.
2. Cada puesto tiene coordenadas X/Y entre 0 y 100.
3. Asigna una persona a un puesto.
4. Asigna equipos y puntos de red al mismo puesto.
5. En el mapa, arrastra una persona sobre otro puesto para moverla.
6. Cada movimiento queda guardado en **Movimientos**.

## Próximas etapas

- Subir un plano real de cada piso como fondo.
- Editor visual para colocar puestos sobre el plano.
- Movimiento de equipos independiente del usuario.
- Exportación Excel/PDF.
- Códigos QR.
- Roles y permisos.
- PostgreSQL + Docker.
- API REST y auditoría avanzada.
