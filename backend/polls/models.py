from django.db import models

# Create your models here.
class Profesor(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre + ' ' + self.apellido

class Asignatura(models.Model):
    #Datos de la asignatura en general
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Asignatura_Profesor(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    #Horarios de la asignatura


    def __str__(self):
        return self.asignatura.nombre + ' - ' + self.profesor.nombre + ' ' + self.profesor.apellido

class Grupo(models.Model):
    asignatura_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)



