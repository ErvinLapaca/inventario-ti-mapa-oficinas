from django.db.models import Q
from django.http import JsonResponse
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
            | Q(puesto__puntos_red__codigo__icontains=q)
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

    oficinas = piso.oficinas.prefetch_related("puestos").all() if piso else []

    contexto = {
        "pisos": pisos,
        "piso": piso,
        "personas": personas,
        "puestos": puestos,
        "oficinas": oficinas,
        "equipos_total": Equipo.objects.count(),
        "personas_total": Persona.objects.filter(activo=True).count(),
        "q": q,
    }
    return render(request, "inventario/dashboard.html", contexto)


def _mover(persona, destino, motivo=""):
    origen = persona.puesto
    ocupante = Persona.objects.filter(puesto=destino).exclude(pk=persona.pk).first()
    if ocupante:
        return False, f"El puesto {destino.codigo} ya está ocupado por {ocupante.nombre_completo}."

    if origen != destino:
        Movimiento.objects.create(
            persona=persona,
            puesto_origen=origen,
            puesto_destino=destino,
            motivo=motivo,
        )
        persona.puesto = destino
        persona.save(update_fields=["puesto"])

    return True, "Movimiento guardado."


@require_POST
def mover_persona(request, persona_id):
    persona = get_object_or_404(Persona, pk=persona_id)
    destino = get_object_or_404(Puesto, pk=request.POST.get("puesto_destino"), activo=True)
    ok, mensaje = _mover(persona, destino, request.POST.get("motivo", ""))
    if not ok:
        return render(
            request,
            "inventario/error_movimiento.html",
            {"mensaje": mensaje, "piso_id": destino.oficina.piso_id},
            status=409,
        )
    return redirect(f"/?piso={destino.oficina.piso_id}")


@require_POST
def mover_persona_ajax(request, persona_id):
    persona = get_object_or_404(Persona, pk=persona_id)
    destino = get_object_or_404(Puesto, pk=request.POST.get("puesto_destino"), activo=True)
    ok, mensaje = _mover(persona, destino, "Movimiento mediante mapa")
    return JsonResponse(
        {
            "ok": ok,
            "mensaje": mensaje,
            "persona": persona.nombre_completo,
            "puesto": destino.codigo,
            "oficina": destino.oficina.nombre,
        },
        status=200 if ok else 409,
    )
