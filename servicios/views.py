from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages # Para los carteles de éxito
from .models import Solicitud
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    if request.method == 'POST':
        # 1. Capturamos los datos del formulario
        vehiculo = request.POST.get('vehiculo')
        tipo = request.POST.get('tipo')
        ubicacion = request.POST.get('ubicacion')
        descripcion = request.POST.get('descripcion')
        lat = request.POST.get('latitud')
        lng = request.POST.get('longitud')

        # 2. Creamos la solicitud en la base de datos
        Solicitud.objects.create(
            vehiculo=vehiculo,
            tipo=tipo,
            ubicacion=ubicacion,
            descripcion=descripcion,
            latitud=lat,
            longitud=lng,
            cliente=request.user if request.user.is_authenticated else None
        )

        # 3. Creamos el mensaje que verá el usuario
        messages.success(request, "Solicitud enviada con éxito, espera tu respuesta")
        
        # 4. Redirigimos al home (esto limpia el formulario y permite mostrar el mensaje)
        return redirect('home')

    # Si es un GET (carga normal), solo renderizamos la página
    return render(request, 'servicios/home.html')

# API para que el mapa del cliente consulte la ubicación del Coyote
def info_seguimiento(request, solicitud_id):
    try:
        solicitud = Solicitud.objects.get(id=solicitud_id)
        return JsonResponse({
            'latitud_coyote': solicitud.latitud_coyote,
            'longitud_coyote': solicitud.longitud_coyote,
            'completado': solicitud.completado,
        })
    except Solicitud.DoesNotExist:
        return JsonResponse({'error': 'No encontrado'}, status=404)

# VISTA PARA EL PANEL DEL CHOFER (VOS)
def panel_chofer(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    return render(request, 'servicios/panel_chofer.html', {'solicitud': solicitud})

# API PARA RECIBIR TU GPS DESDE EL CELULAR
@csrf_exempt
def actualizar_ubicacion_grua(request, solicitud_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            solicitud = get_object_or_404(Solicitud, id=solicitud_id)
            solicitud.latitud_coyote = data.get('lat')
            solicitud.longitud_coyote = data.get('lng')
            solicitud.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)