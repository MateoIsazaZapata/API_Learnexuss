from django.contrib import admin
from .models import Roles,Nivel_educativo, Aulas, Lista_asistencia, Coordinador, Docente, Estudiante
from .models import Actividades, Temas, Plan_leccion, Materia, Plan_estudio, Calificacion

from django.contrib import admin
from .models import Coordinador, Docente, Estudiante

# class CoordinadorAdmin(admin.ModelAdmin):
#     readonly_fields = ('roles',)

# class DocenteAdmin(admin.ModelAdmin):
#     readonly_fields = ('roles',)

# class EstudianteAdmin(admin.ModelAdmin):
#     readonly_fields = ('roles',)

#Listado de registro de cada modelo
admin.site.register(Roles) 
admin.site.register(Nivel_educativo) 
admin.site.register(Aulas) 
admin.site.register(Coordinador)
admin.site.register(Docente)
admin.site.register(Estudiante) 
admin.site.register(Actividades)
admin.site.register(Temas) 
admin.site.register(Plan_leccion)
admin.site.register(Materia)
admin.site.register(Plan_estudio)
admin.site.register(Calificacion)