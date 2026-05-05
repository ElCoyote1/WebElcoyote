import json
import requests
import os  # Necesario para leer la API KEY desde Render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Solicitud
from django.views.decorators.csrf import csrf_exempt

# --- FUNCIÓN DE NOTIFICACIÓN AUTOMÁTICA ---
def avisar_al_dueno(pedido, request):
    """
    Toma los datos del pedido recién creado y envía un WhatsApp al dueño.
    """
    # 1. Datos del dueño
    telefono_dueno = "5493584163655"
    
    # Buscamos la clave en las variables de entorno de Render. 
    # Si no existe, usamos la temporal para que no explote.
    api_key = os.getenv('WHATSAPP_API_KEY', '8706117')
    
    if api_key == '12345':
        print("⚠️ DEBUG: WhatsApp no enviado (Clave por defecto). Configura WHATSAPP_API_KEY en Render.")
        return

    # 2. Generar el link al mapa dinámicamente
    dominio = request.get_host() 
    protocolo = "https" if request.is_secure() else "http"
    url_panel = f"{protocolo}://{dominio}/chofer/{pedido.id}/"
    
    # 3. Armar el mensaje con los datos que cargó el cliente
    texto = (
        f"🚨 *NUEVO AUXILIO COYOTE* 🚨\n\n"
        f"🚗 *Vehículo:* {pedido.vehiculo}\n"
        f"🛠 *Servicio:* {pedido.get_tipo_display()}\n"
        f"📍 *Destino:* {pedido.ubicacion}\n"
        f"📝 *Detalle:* {pedido.descripcion if pedido.descripcion else 'Sin detalles'}\n\n"
        f"📱 *Abrir Panel de Seguimiento:* \n{url_panel}"
    )

    url_api = "https://api.callmebot.com/whatsapp.php"
    params = {
        "phone": telefono_dueno,
        "text": texto,
        "apikey": api_key
    }
    
    try:
        # Enviamos la petición al bot para que despache el WhatsApp
        requests.get(url_api, params=params, timeout=10)
    except Exception as e:
        print(f"Error de conexión con WhatsApp: {e}")


def home(request):
    if request.method == 'POST':
        vehiculo = request.POST.get('vehiculo')
        tipo = request.POST.get('tipo')
        ubicacion = request.POST.get('ubicacion')
        descripcion = request.POST.get('descripcion')
        lat = request.POST.get('latitud')
        lng = request.POST.get('longitud')

        # 1. Creamos el pedido
        try:
            nuevo_pedido = Solicitud.objects.create(
                vehiculo=vehiculo,
                tipo=tipo,
                ubicacion=ubicacion,
                descripcion=descripcion,
                latitud=lat,
                longitud=lng,
                cliente=request.user if request.user.is_authenticated else None
            )
        except Exception as e:
            print(f"Error al crear el pedido: {e}")
            messages.error(request, "Hubo un error al procesar tu solicitud. Intentalo de nuevo.")
            return redirect('home')

        # 2. INTENTO DE WHATSAPP (Envoltorio de seguridad total)
        try:
            avisar_al_dueno(nuevo_pedido, request)
        except Exception as e:
            print(f"DEBUG: Error en la función avisar_al_dueno: {e}")

        # 3. Éxito y Renderizado
        # Agregamos el mensaje largo que me pediste para el cartel amarillo del HTML
        messages.success(request, "Solicitud enviada con éxito. Pronto tu solicitud será aceptada y se te mostrará en vivo el recorrido de tu auxilio.")
        
        # Pasamos el 'pedido' al contexto para que el JS del mapa sepa a quién seguir
        return render(request, 'servicios/home.html', {'pedido': nuevo_pedido})

    return render(request, 'servicios/home.html')


# 2. VISTA PARA EL PANEL DEL CHOFER: Donde el chofer comparte su GPS
def panel_chofer(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    return render(request, 'servicios/panel_chofer.html', {'solicitud': solicitud})


# 3. API PARA RECIBIR EL GPS DEL CHOFER (Se llama desde JS cada pocos segundos)
@csrf_exempt
def actualizar_ubicacion_grua(request, solicitud_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            solicitud = Solicitud.objects.get(id=solicitud_id)
            
            solicitud.latitud_coyote = data.get('lat')
            solicitud.longitud_coyote = data.get('lng')
            solicitud.save()
            
            return JsonResponse({'status': 'ok', 'message': 'Ubicación actualizada'})
        except Solicitud.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'invalid method'}, status=405)


# 4. API PARA EL CLIENTE: Su mapa consulta aquí para mover la grúa
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