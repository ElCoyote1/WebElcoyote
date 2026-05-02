from django.contrib import admin
from django.utils.html import format_html # Importante para meter el botón
from django.urls import reverse # Para generar la URL automáticamente
from .models import Solicitud

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    # Agregamos 'ir_al_panel' al final de la lista
    list_display = ('id', 'vehiculo', 'tipo', 'fecha_creacion', 'completado', 'ir_al_panel')
    list_filter = ('completado', 'tipo', 'fecha_creacion')
    search_fields = ('vehiculo', 'descripcion')
    list_editable = ('completado',)
    ordering = ('-fecha_creacion',)

    # ESTA ES LA FUNCIÓN QUE CREA EL BOTÓN
    def ir_al_panel(self, obj):
        # Genera la URL para la vista 'panel_chofer' con el ID del pedido
        url = reverse('panel_chofer', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank" '
            'style="background-color: #ccff00; color: black; font-weight: bold; padding: 5px 10px; border-radius: 4px; text-decoration: none;">'
            '🚚 INICIAR VIAJE</a>', 
            url
        )
    
    ir_al_panel.short_description = 'Acción rápida' # Nombre de la columna en el Admin