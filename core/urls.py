from django.contrib import admin
from django.urls import path
from servicios.views import (
    home, 
    info_seguimiento, 
    panel_chofer, 
    actualizar_ubicacion_grua
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    
    # Ruta para el cliente (consulta cada 5 seg)
    path('api/seguimiento/<int:solicitud_id>/', info_seguimiento, name='info_seguimiento'),
    
    # RUTAS PARA EL CHOFER (VOS)
    # 1. Para entrar a la pantalla de control
    path('chofer/<int:solicitud_id>/', panel_chofer, name='panel_chofer'),
    # 2. Para que el celular envíe las coordenadas
    path('api/actualizar-gps/<int:solicitud_id>/', actualizar_ubicacion_grua, name='actualizar_gps'),
]