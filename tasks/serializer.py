from rest_framework import serializers
from .models  import Roles, Coordinador, Docente, Estudiante, Nivel_educativo, Aulas, Lista_asistencia
from .models import Actividades, Temas, Plan_leccion, Materia, Plan_estudio

#Serializer para cada modelo
    
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'
        
        
class NivelEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel_educativo
        fields = '__all__'
        
        
class CoordinadorSerializer(serializers.ModelSerializer):
    tipo_rol = serializers.SerializerMethodField()
    class Meta:
        model = Coordinador
        fields = '__all__' #muestra todos los campos del modelo
        
class DocenteSerializer(serializers.ModelSerializer):
    tipo_rol = serializers.SerializerMethodField()
    class Meta:
        model = Docente
        fields = '__all__' #muestra todos los campos del modelo

    def get_tipo_rol(self, obj):
        return obj.roles.rol
        
class EstudianteSerializer(serializers.ModelSerializer):
    tipo_rol = serializers.SerializerMethodField()
    class Meta:
        model = Estudiante
        fields = '__all__' #muestra todos los campos del modelo
    
    def get_tipo_rol(self, obj):
        return obj.roles.rol
    

class AulasSerializer(serializers.ModelSerializer):
    docentes_asignados = serializers.SerializerMethodField()
    estudiantes_asignados = serializers.SerializerMethodField()

    class Meta:
        model = Aulas
        fields = ('id_aula', 'nombre_aula', 'nivel_educativo', 'docentes_asignados', 'estudiantes_asignados')

    def get_docentes_asignados(self, obj):
        return [docente.primer_nombre for docente in obj.docentes.all()]

    def get_estudiantes_asignados(self, obj):
        return [estudiante.primer_nombre for estudiante in obj.estudiantes.all()]

    
class MateriaSerializer(serializers.ModelSerializer):
    aulas = serializers.PrimaryKeyRelatedField(many=True, queryset=Aulas.objects.all())
    actividades = serializers.PrimaryKeyRelatedField(many=True, queryset=Actividades.objects.all())
    temas = serializers.PrimaryKeyRelatedField(many=True, queryset=Temas.objects.all())
    plan_estudio = serializers.PrimaryKeyRelatedField(queryset= Plan_estudio.objects.all(), allow_null=True, required=False)
    docentes = serializers.PrimaryKeyRelatedField(queryset=Docente.objects.all(), allow_null=True)
    
    class Meta:
        model = Materia
        fields = 'id_materia', 'nombre_materia', 'aulas', 'actividades', 'temas', 'plan_estudio', 'docentes'
        
class PlanEstudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan_estudio
        fields = '__all__'
        
class ActividadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividades
        fields = '__all__'
        
class TemasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temas
        fields = '__all__'

class PlanLeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan_leccion
        fields = '__all__'
        
        
class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividades
        fields = '__all__'