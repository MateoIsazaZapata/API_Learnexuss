from django.db import models

# Create your models here.
#Datos de desplegables
DOCUMENTO = [
    ('CC', 'Cédula de Ciudadanía'),
    ('TI', 'Tarjeta de Identidad'),
    ('CE', 'Cédula de Extranjería'),
]

#Rol de cada usuario
class Roles(models.Model): 
    ROLES = [
    ('DOCENTE', 'Docente'), 
    ('ESTUDIANTE', 'Estudiante'),
    ('COORDINADOR', 'Coordinador'),
]
    id_rol = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='DOCENTE', unique=True, null=True, blank=False)
#funcion para mostrar tareas en el admin
    def __str__(self):
        return f"ID: {self.id_rol},- {self.rol}" 

#Informacion de cada usuario
class Usuarios(models.Model):
    tipo_doc = models.CharField(max_length=3, choices=DOCUMENTO, default='CC', null=False, blank=False)
    numero_doc = models.CharField(max_length=20, null=False, blank=False)
    primer_nombre = models.CharField(max_length=20, null=False, blank=False)
    segundo_nombre = models.CharField(max_length=20, null=False, blank=True)
    primer_apellido = models.CharField(max_length=20, null=False, blank=False)
    segundo_apellido = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    estado_usuario = models.BooleanField(default=False, choices=[(True, 'activo'), (False, 'inactivo')])
    contraseña = models.CharField(max_length=20, null=False, blank=True)
    telefono = models.CharField(max_length=11, null=True, blank=True)
    foto_usuario =  models.CharField(max_length=240, null=True, blank=True)

    class Meta:
        abstract = True # clase padre para heredar en otras clases y no crear una tabla en la base de datos

#clases que heredan de Usuarios_registrados
class Coordinador(Usuarios):
    id_coordinador = models.AutoField(primary_key=True)
    roles = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
    nivel_educativo = models.ForeignKey('Nivel_educativo', on_delete=models.CASCADE, null=False, blank=False)
    
    def asignar_rol(self, *args, **kwargs):
        if not self.id_rol:
            self.rol_coordinador = Roles.objects.get(rol='COORDINADOR')
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Id: {self.id_coordinador} - Nombre: {self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido} - Email: {self.email}"
    
            

class Docente(Usuarios):
    id_docente = models.AutoField(primary_key=True)
    especialidad = models.CharField(max_length=100, null=False, blank=False)
    roles = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
    nivel_educativo = models.ForeignKey('Nivel_educativo', on_delete=models.CASCADE, null=False, blank=False)
    materias = models.ManyToManyField('Materia', blank=True, related_name='docentes_asignados')
    
    def asignar_rol(self, *args, **kwargs):
        if not self.id_rol:
            self.rol_docente = Roles.objects.get(rol='DOCENTE')
        super().save(*args, **kwargs)  
        
    def __str__(self):
        return f"Id: {self.id_docente} - Nombre: {self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido} - Email: {self.email}"
    
class Estudiante(Usuarios):
    id_estudiante = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=20, null=False, blank=False)
    roles = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
    nivel_educativo = models.ForeignKey('Nivel_educativo', on_delete=models.CASCADE, null=False, blank=False)
    
    def asignar_rol(self, *args, **kwargs):
        if not self.id_rol:
            self.rol_estudiante = Roles.objects.get(rol='ESTUDIANTE')
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Id: {self.id_estudiante} - Nombre: {self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido} - Email: {self.email}" 
    


#Nivel educativo de cada estudiante
class Nivel_educativo(models.Model):
    NIVEL_EDUCATIVO = [
    ('PREESCOLAR', 'Preescolar'),
    ('PRIMARIA', 'Primaria'),
    ('SECUNDARIA', 'Secundaria')]

    id_nivel_educativo = models.AutoField(primary_key=True)
    nombre_nivel = models.CharField(max_length=20, choices=NIVEL_EDUCATIVO, default='PRIMARIA', null=False, blank=False)
#funcion para mostrar tareas en el admin
    def __str__(self):
        return f"Id: {self.id_nivel_educativo}- Nivel educativo: {self.nombre_nivel} "


#Nombre de cada aula
class Aulas(models.Model):
    id_aula = models.AutoField(primary_key=True)
    nombre_aula = models.CharField(max_length=100, null=False, blank=False)
#Llaves foraneas
    nivel_educativo = models.ForeignKey(Nivel_educativo, on_delete=models.CASCADE, null=False, blank=False)
    docentes = models.ManyToManyField(Docente, blank=True)
    estudiantes = models.ManyToManyField(Estudiante, blank=True)
#funcion para mostrar tareas en el admin
    def __str__(self):
        docentes_asignados = ', '.join(self.docentes.values_list('primer_nombre', flat=True)) or "Sin docentes"
        estudiantes_asignados = ', '.join(self.estudiantes.values_list('primer_nombre', flat=True)) or "Sin estudiantes" 
        
        return f"id: {self.id_aula} - Aula {self.nombre_aula} | Nivel: {self.nivel_educativo} | Docentes: {docentes_asignados} | Estudiantes: {estudiantes_asignados}"

#Informacion de asistencia de cada estudiante   
class Lista_asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    fecha_asistencia = models.DateField(null=False, blank=False)
    estado_asistencia = models.BooleanField(default=False)
#Llaves foraneas
    aulas = models.ForeignKey(Aulas, on_delete=models.CASCADE, null=False, blank=False)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, null=False, blank=False)
#funcion para mostrar tareas en el admin
    def __str__(self):
        return f" ID: {self.id_asistencia} - Fecha: {self.fecha_asistencia} - Estado: {self.estado_asistencia} - Aula: {self.aulas.nombre_aula} - Materia: {self.materia.nombre_materia}"#OBSERVACION

#Datos de las materias asignadas en las aulas
class Materia(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre_materia = models.CharField(max_length=100, null=False, blank=False)
#Llaves foraneas
    docentes = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True, blank=True)
    plan_estudio = models.ForeignKey('Plan_estudio', on_delete=models.CASCADE, default=1)
    aulas = models.ManyToManyField(Aulas, blank=True)
    actividades = models.ManyToManyField('Actividades', blank=True)
    temas = models.ManyToManyField('Temas', blank=True)
#funcion para mostrar tareas en el admin
    def __str__(self):
        return f"ID: {self.id_materia} - Nombre materia: {self.nombre_materia} - id del docente: {self.docentes.id_docente if self.docentes else "No hay docente asignado"}" #OBSERVACION
        
#plan de estudio programado para cada aula
class Plan_estudio(models.Model):
    id_plan_estudio = models.AutoField  (primary_key=True)
    nombre_plan_estudio = models.CharField(max_length=100, null=False, blank=False)
    link_plan_estudio = models.CharField(max_length=240, null=False, blank=False)
#funcion para mostrar tareas en el admin
    def __str__(self):
        return f"ID: {self.id_plan_estudio} - Nombre Plan de estudio: {self.nombre_plan_estudio}"#OBSERVACION

#Actividades asignadas a las materias
class Actividades(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    nombre_actividad = models.CharField(max_length=100, null=False, blank=False)
    descripcion_actividad = models.TextField(blank=True)
#funcion para mostrar tareas en el admin
    def __str__(self):
        return f" Actividad: {self.nombre_actividad} - ID: {self.id_actividad}" #OBSERVACION

#Temas de cada materia
class Temas(models.Model):
    id_tema = models.AutoField(primary_key=True)
    nombre_tema = models.CharField(max_length=100, null=False, blank=False)
    periodo_academico = models.CharField(max_length=20, null=False, blank=False)
#Llaves foraneas
    plan_leccion = models.ForeignKey('Plan_leccion', on_delete=models.CASCADE, null=False, blank=False)
#funcion para mostrar tareas en el admin
    def __str__(self):
        return f"Tema: {self.nombre_tema} - ID: {self.id_tema} - Plan leccion: {self.plan_leccion.nombre_plan_leccion} - periodo: {self.periodo_academico}"#OBSERVACION

    
#Lecciones de cada tema
class Plan_leccion(models.Model):
    id_plan_leccion = models.AutoField(primary_key=True)
    nombre_plan_leccion = models.CharField(max_length=80, null=False, blank=False)
    link_plan_leccion = models.CharField(max_length=240, null=False, blank=False)
#funcion para mostrar tareas en el admin
    def __str__(self):
        return f" Plan leccion: {self.nombre_plan_leccion} - ID: {self.id_plan_leccion} - Link: {self.link_plan_leccion}"#OBSERVACION

#calificacion de cada estiduante por actividad
class Calificacion(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    calificacion = models.FloatField(null=True, blank=True)
#Llaves foraneas
    actividades = models.ForeignKey(Actividades, on_delete=models.CASCADE, null=True, blank=True)
    estudiantes = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True, blank=True)
#funcion para mosgtrar calificacion de cada estudiante
    def __str__(self):
        return f"ID: {self.id_calificacion} - Actividad: {self.actividades.nombre_actividad}- Calificacion: {self.calificacion}"#OBSERVACION
