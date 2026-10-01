from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Equipo, Persona, Piso, Puesto, Movimiento


def dashboard(request):
    pisos = Piso.objects.select_related("edificio").all()
    piso_id = request.GET.get("piso")
    piso = get_object_or_404(Piso, pk=piso_id) if piso_id else pisos.first()

    personas = Persona.objects.select_related(
        "puesto__oficina__piso__edificio"
    ).prefetch_related("equipos", "puesto__puntos_red")

    q = request.GET.get("q", "").strip()
    if q:
        personas = personas.filter(
            Q(nombre_completo__icontains=q)
            | Q(cargo__icontains=q)
            | Q(area__icontains=q)
            | Q(equipos__codigo_activo__icontains=q)
            | Q(equipos__ip__icontains=q)
            | Q(equipos__mac__icontains=q)
        ).distinct()

    if piso:
        personas = personas.filter(puesto__oficina__piso=piso)

    puestos = (
        Puesto.objects.select_related("oficina")
        .prefetch_related("equipos", "puntos_red")
        .filter(oficina__piso=piso, activo=True)
        if piso
        else Puesto.objects.none()
    )

    contexto = {
        "pisos": pisos,
        "piso": piso,
        "personas": personas,
        "puestos": puestos,
        "equipos_total": Equipo.objects.count(),
        "personas_total": Persona.objects.filter(activo=True).count(),
        "q": q,
    }
    return render(request, "inventario/dashboard.html", contexto)


@require_POST
def mover_persona(request, persona_id):
    persona = get_object_or_404(Persona, pk=persona_id)
    destino = get_object_or_404(Puesto, pk=request.POST.get("puesto_destino"), activo=True)
    origen = persona.puesto

    if origen != destino:
        Movimiento.objects.create(
            persona=persona,
            puesto_origen=origen,
            puesto_destino=destino,
            motivo=request.POST.get("motivo", ""),
        )
        persona.puesto = destino
        persona.save(update_fields=["puesto"])

    return redirect(f"/?piso={destino.oficina.piso_id}")
