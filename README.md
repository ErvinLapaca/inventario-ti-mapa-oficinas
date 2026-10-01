# Inventario TI – Mapa de Oficinas

Aplicación web para visualizar y administrar usuarios, oficinas, puestos, equipos y puntos de red en un mapa interactivo.

## Funciones de esta versión
- Edificios, pisos, oficinas y puestos.
- Personas con nombre, cargo, área, correo y teléfono.
- Equipos: PC, laptop, monitor, impresora, teléfono y otros.
- Datos de red: IP, MAC, punto de red, switch, puerto, patch panel y VLAN.
- Asignación de equipos a personas.
- Ubicación visual mediante coordenadas X/Y.
- Movimiento de usuarios entre puestos con historial.
- Buscador básico.
- Panel de administración Django.
- Dashboard visual por piso.

## Requisitos
- Python 3.11+
- pip

## Instalación local

```bash
git clone https://github.com/ErvinLapaca/inventario-ti-mapa-oficinas.git
cd inventario-ti-mapa-oficinas

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Abrir:

- Sistema: http://127.0.0.1:8000/
- Administración: http://127.0.0.1:8000/admin/

## Estructura
- `config/`: configuración Django.
- `inventario/`: modelos, vistas, admin, URLs y comandos.
- `templates/`: interfaz.
- `static/`: estilos.
- `db.sqlite3`: se crea localmente y no se versiona.

## Próximas mejoras
- Arrastrar y soltar usuarios/equipos en el plano.
- Carga de plano de planta como imagen/SVG.
- Exportación Excel/PDF.
- Códigos QR.
- Roles y permisos detallados.
- PostgreSQL + Docker.
- Auditoría avanzada y API REST.
