from django.urls import path, include
from rest_framework import routers
from .views import CoordinadorViewSet,DocenteViewSet,EstudianteViewSet,RolesViewSet, NivelEducativoViewSet, AulasViewSet, MateriaViewSet, CalificacionViewSet

router = routers.DefaultRouter()
router.register(r'coordinador', CoordinadorViewSet)
router.register(r'docente', DocenteViewSet)
router.register(r'estudiante', EstudianteViewSet)
router.register(r'roles', RolesViewSet)
router.register(r'nivelEducativo', NivelEducativoViewSet)
router.register(r'aulas', AulasViewSet)
router.register(r'materia', MateriaViewSet)
router.register(r'calificacion', CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls))
] 