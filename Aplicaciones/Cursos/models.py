from django.db import models

# Create your models here.

class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20, unique=True)
    apellido = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    titulacion = models.CharField(max_length=100)
    imginstructor = models.ImageField(upload_to='imginstructor/', blank=True, null=True)
    
    def __str__(self):
        if self.imginstructor:
            return f"{self.nombre} {self.apellido} ({self.imginstructor.name})"
        return f"{self.nombre} {self.apellido}"

class Curso(models.Model):
    id = models.AutoField(primary_key=True)

    AREA_CHOICES = [
        ('TEC', 'Tecnología'),
        ('ADM', 'Administración'),
        ('IDI', 'Idiomas'),
    ]

    ESTADO_CHOICES = [
        ('ACT', 'Activo'),
        ('INA', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=100)
    area = models.CharField(max_length=3, choices=AREA_CHOICES)
    duracion_horas = models.PositiveIntegerField()
    cupo_maximo = models.PositiveIntegerField()
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='ACT')
    instructor = models.ForeignKey(
        Instructor,
        related_name='cursos',
        on_delete=models.PROTECT  # CAMBIADO: de CASCADE a PROTECT
    )

    def __str__(self):
        return self.nombre

    def cupos_disponibles(self):
        return self.cupo_maximo - self.matriculas.count()

from django.core.exceptions import ValidationError
from django.utils.timezone import now

class Matricula(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_estudiante = models.CharField(max_length=100)
    documento_identidad = models.CharField(max_length=20)

    fecha_matricula = models.DateField(default=now)

    curso = models.ForeignKey(
        Curso,
        related_name='matriculas',
        on_delete=models.PROTECT  # CAMBIADO: de CASCADE a PROTECT
    )

    instructor = models.ForeignKey(
        Instructor,
        related_name='matriculas',
        on_delete=models.PROTECT  # CAMBIADO: de CASCADE a PROTECT
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['documento_identidad', 'curso'],
                name='unique_estudiante_curso'
            )
        ]

    def clean(self):
        if self.curso.estado != 'ACT':
            raise ValidationError("No se puede matricular en un curso inactivo.")

        if self.curso.matriculas.exclude(id=self.id).count() >= self.curso.cupo_maximo:
            raise ValidationError("El curso ya alcanzó su cupo maximo.")

        if self.fecha_matricula > now().date():
            raise ValidationError("La fecha de matricula no puede ser posterior a hoy.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_estudiante} - {self.curso.nombre}"