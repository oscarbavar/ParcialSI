from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pagina(models.Model):
    Titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='imagenes/')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Titulo + ' - pertenece a: ' + self.usuario.username
