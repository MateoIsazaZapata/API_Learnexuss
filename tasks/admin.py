from django.contrib import admin
from .models import Roles, Usuarios_registrados, Nivel_educativo, Aulas, Lista_asistencia 
from .models import Actividades, Temas, Plan_leccion, Materia, Plan_estudio, Calificacion

# Register your models here.
#Listado de registro de cada modelo
admin.site.register(Roles) 
admin.site.register(Usuarios_registrados) 
admin.site.register(Nivel_educativo) 
admin.site.register(Aulas) 
admin.site.register(Lista_asistencia) 
admin.site.register(Actividades)
admin.site.register(Temas) 
admin.site.register(Plan_leccion)
admin.site.register(Materia)
admin.site.register(Plan_estudio)
admin.site.register(Calificacion)