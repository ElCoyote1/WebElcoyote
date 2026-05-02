from django.db import models
from django.contrib.auth.models import User

class Solicitud(models.Model):
    TIPO_PROBLEMA = [
        ('MEC', 'Mecánica Ligera'),
        ('BAT', 'Batería / Arranque'),
        ('NEU', 'Neumáticos'),
        ('GRU', 'Grúa (Local)'),
        ('GRL', 'Grúa (Larga Distancia)'),
    ]
    # Ubicación en tiempo real de la grúa (El Coyote)
    latitud_coyote = models.FloatField(null=True, blank=True)
    longitud_coyote = models.FloatField(null=True, blank=True)

    # Cambiamos cliente a null=True por si no está registrado al pedir
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    vehiculo = models.CharField(max_length=100, verbose_name="Vehículo")
    descripcion = models.TextField(verbose_name="¿Qué sucede?", blank=True)
    ubicacion = models.CharField(max_length=255, verbose_name="Destino Final")
    tipo = models.CharField(max_length=3, choices=TIPO_PROBLEMA, default='MEC')
    
    # CAMPOS CLAVE PARA EL MAPA
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

    def __str__(self):
        return f"Auxilio para {self.vehiculo} - {self.tipo}"