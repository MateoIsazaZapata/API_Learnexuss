from rest_framework import serializers
from .models  import Roles, Usuarios_registrados, Nivel_educativo, Aulas, Lista_asistencia
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
        
        
class UsuariosRegistradosSerializer(serializers.ModelSerializer):
    tipo_rol = serializers.SerializerMethodField()
    class Meta:
        model = Usuarios_registrados
        fields = ('id_usuario','tipo_doc', 'numero_doc', 'nombre_usuario', 'roles', 'tipo_rol', 'email', 'estado_usuario') #muestra todos los campos del modelo
        
    def get_tipo_rol(self, obj):
        return obj.roles.rol
    
    def validate(self, data):
        if data['roles'].rol == "ESTUDIANTE":
            aulas_asignadas = Aulas.objects.filter(estudiantes__id_usuario=self.instance.id_usuario)
            if aulas_asignadas.exists():
                raise serializers.ValidationError("El estudiante ya tiene un aula asignada.")
        return data
    

class AulasSerializer(serializers.ModelSerializer):
    docentes_asignados = serializers.SerializerMethodField()
    estudiantes_asignados = serializers.SerializerMethodField()

    docentes = serializers.PrimaryKeyRelatedField(many=True, queryset=Usuarios_registrados.objects.filter(roles__rol="DOCENTE"))
    estudiantes = serializers.PrimaryKeyRelatedField(many=True, queryset=Usuarios_registrados.objects.filter(roles__rol="ESTUDIANTE"))

    class Meta:
        model = Aulas
        fields = ('id_aula', 'nombre_aula', 'nivel_educativo', 'docentes', 'docentes_asignados', 'estudiantes', 'estudiantes_asignados')
        
    def get_docentes_asignados(self, obj):
        return ', '.join([docente.nombre_usuario for docente in obj.docentes.all()])
    
    def get_estudiantes_asignados(self, obj):
        return ', '.join([estudiante.nombre_usuario for estudiante in obj.estudiantes.all()])
    
    def validate_estudiantes(self, estudiantes):
        # Si es una instancia en edición, la excluimos de la validación
        aula_actual = self.instance if self.instance else None
    
        for estudiante in estudiantes:
            # Buscar si el estudiante ya pertenece a otra aula
            aulas = Aulas.objects.filter(estudiantes=estudiante)
            if aula_actual:
                aulas = aulas.exclude(id_aula=aula_actual.id_aula)
    
            if aulas.exists():
                raise serializers.ValidationError(
                    f"El estudiante '{estudiante.nombre_usuario}' ya está asignado a otra   aula."
                )
        return estudiantes

    
class MateriaSerializer(serializers.ModelSerializer):
    aulas = serializers.PrimaryKeyRelatedField(many=True, queryset=Aulas.objects.all())
    actividades = serializers.PrimaryKeyRelatedField(many=True, queryset=Actividades.objects.all())
    temas = serializers.PrimaryKeyRelatedField(many=True, queryset=Temas.objects.all())
    plan_estudio = serializers.PrimaryKeyRelatedField(queryset= Plan_estudio.objects.all(), allow_null=True, required=False)
    class Meta:
        model = Materia
        fields = 'id_materia', 'nombre_materia', 'aulas', 'actividades', 'temas', 'plan_estudio'
        
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
