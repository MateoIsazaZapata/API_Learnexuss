# from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets, serializers
from .models import Roles, Usuarios_registrados, Nivel_educativo, Aulas, Lista_asistencia
from .models import Actividades, Temas, Plan_leccion, Materia, Plan_estudio, Calificacion
from .serializer import UsuariosRegistradosSerializer, RolesSerializer, NivelEducativoSerializer, AulasSerializer, MateriaSerializer, PlanEstudioSerializer, ActividadesSerializer, TemasSerializer, PlanLeccionSerializer, CalificacionSerializer
# Create your views here.

class UsuariosRegistradosViewSet(viewsets.ModelViewSet): #CRUD de la clase Usuarios_registrados    
    queryset = Usuarios_registrados.objects.all()
    serializer_class = UsuariosRegistradosSerializer

class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    
class NivelEducativoViewSet(viewsets.ModelViewSet):
    queryset = Nivel_educativo.objects.all()
    serializer_class = NivelEducativoSerializer
    
class AulasViewSet(viewsets.ModelViewSet):
    queryset = Aulas.objects.prefetch_related('estudiantes')
    serializer_class = AulasSerializer

    def perform_update(self, serializer):
        aula = serializer.instance
        estudiantes_nuevos = serializer.validated_data.get("estudiantes", [])

        for estudiante in estudiantes_nuevos:
            if Aulas.objects.filter(estudiantes=estudiante).exclude(id=aula.id).exists():
                raise serializers.ValidationError(f"El estudiante {estudiante.nombre_usuario} ya está asignado a otra aula.")

        aula.estudiantes.set(estudiantes_nuevos)  # 🔹 Reemplaza la lista con los estudiantes nuevos permitir duplicaciones
        serializer.save()
        
class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.prefetch_related('aulas', 'actividades', 'temas')
    serializer_class = MateriaSerializer
    
class PlanEstudioViewSet(viewsets.ModelViewSet):
    queryset = Plan_estudio.objects.all()
    serializer_class = PlanEstudioSerializer
    
class ActividadesViewSet(viewsets.ModelViewSet):
    queryset = Actividades.objects.all()
    serializer_class = ActividadesSerializer
    
class TemasViewSet(viewsets.ModelViewSet):
    queryset = Temas.objects.all()
    serializer_class = TemasSerializer
    
class PlanLeccionViewSet(viewsets.ModelViewSet):
    queryset = Plan_leccion.objects.all()
    serializer_class = PlanLeccionSerializer
    
class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer