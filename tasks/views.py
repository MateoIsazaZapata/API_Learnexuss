# from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets
from rest_framework import serializers
from .models import Roles, Coordinador, Docente, Estudiante, Nivel_educativo, Aulas, Lista_asistencia
from .models import Actividades, Temas, Plan_leccion, Materia, Plan_estudio, Calificacion
from .serializer import CoordinadorSerializer, DocenteSerializer, EstudianteSerializer, RolesSerializer, NivelEducativoSerializer, AulasSerializer, MateriaSerializer, PlanEstudioSerializer, ActividadesSerializer, TemasSerializer, PlanLeccionSerializer, CalificacionSerializer
# Create your views here.

class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()  
    serializer_class = RolesSerializer
    
class NivelEducativoViewSet(viewsets.ModelViewSet):
    queryset = Nivel_educativo.objects.all()
    serializer_class = NivelEducativoSerializer
    
class CoordinadorViewSet(viewsets.ModelViewSet):    
    queryset = Coordinador.objects.all()
    serializer_class = CoordinadorSerializer
    
class DocenteViewSet(viewsets.ModelViewSet):    
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer
    
class EstudianteViewSet(viewsets.ModelViewSet):    
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

class AulasViewSet(viewsets.ModelViewSet):
    queryset = Aulas.objects.prefetch_related('docentes', 'estudiantes')
    serializer_class = AulasSerializer
        
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