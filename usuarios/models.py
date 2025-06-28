from django.db import models

# usuarios/models.py
class Usuario(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    )

    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=10, choices=ROLES, default='viewer')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
