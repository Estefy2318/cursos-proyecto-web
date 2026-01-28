from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Curso, Matricula
from .models import Instructor
from django.db.models import ProtectedError

def listar_instructores(request):
    instructores = Instructor.objects.all()
    return render(request, 'instructores.html', {'instructores': instructores})


def index(request):
    cursos = Curso.objects.all()
    return render(request, 'index.html', {'cursos': cursos})


def crearCurso(request):
    instructores = Instructor.objects.all()
    
    if request.method == 'POST':
        try:
            Curso.objects.create(
                nombre=request.POST['nombre'],
                area=request.POST['area'],
                duracion_horas=request.POST['duracion_horas'],
                cupo_maximo=request.POST['cupo_maximo'],
                estado=request.POST['estado'],
                instructor_id=request.POST['instructor']
            )
            messages.success(request, 'Agregado ok')
            return redirect('index')
        except Exception as e:
            messages.error(request, 'Error al agregar curso')
            return redirect('crearCurso')

    return render(request, 'crearCurso.html', {'instructores': instructores})


def editarCurso(request, id):
    curso = get_object_or_404(Curso, id=id)
    instructores = Instructor.objects.all()

    if request.method == 'POST':
        try:
            curso.nombre = request.POST['nombre']
            curso.area = request.POST['area']
            curso.duracion_horas = request.POST['duracion_horas']
            curso.cupo_maximo = request.POST['cupo_maximo']
            curso.estado = request.POST['estado']
            curso.instructor_id = request.POST['instructor']
            curso.save()
            messages.success(request, 'Editado ok')
            return redirect('index')
        except Exception as e:
            messages.error(request, 'Error al editar curso')
            return redirect('editarCurso', id=id)

    return render(request, 'editarCurso.html', {'curso': curso, 'instructores': instructores})


def eliminarCurso(request, id):
    curso = get_object_or_404(Curso, id=id)
    
    try:
        curso.delete()
        messages.success(request, 'Curso eliminado correctamente')
        
    except ProtectedError:
        # Capturar error cuando hay matrículas asociadas
        matriculas_count = curso.matriculas.count()
        
        messages.error(
            request,
            f'❌ No se puede eliminar el curso "{curso.nombre}". '
            f'Tiene {matriculas_count} matrícula(s) asociadas. '
            f'Debe eliminar estas matrículas primero o inactivar el curso.'
        )
    
    except Exception as e:
        messages.error(request, f'Error al eliminar curso: {str(e)}')
    
    return redirect('index')


def listaMatriculas(request):
    matriculas = Matricula.objects.select_related('curso')
    return render(request, 'matriculas.html', {'matriculas': matriculas})


def crearMatricula(request):
    cursos = Curso.objects.filter(estado='ACT')
    instructores = Instructor.objects.all()  # <-- AGREGADO
    error = None

    if request.method == 'POST':
        try:
            Matricula.objects.create(
                nombre_estudiante=request.POST['nombre_estudiante'],
                documento_identidad=request.POST['documento_identidad'],
                fecha_matricula=request.POST['fecha_matricula'],
                curso_id=request.POST['curso'],
                instructor_id=request.POST['instructor']  # <-- AGREGADO
            )
            messages.success(request, 'Agregado ok')
            return redirect('matriculas')
        except ValidationError as e:
            error = e.messages[0] if e.messages else "Error desconocido"
            messages.error(request, error)

    return render(request, 'crearMatricula.html', {
        'cursos': cursos,
        'instructores': instructores,  # <-- AGREGADO
        'error': error
    })


def editarMatricula(request, id):
    matricula = get_object_or_404(Matricula, id=id)
    cursos = Curso.objects.filter(estado='ACT')
    instructores = Instructor.objects.all()  # <-- AGREGADO
    error = None

    if request.method == 'POST':
        try:
            matricula.nombre_estudiante = request.POST['nombre_estudiante']
            matricula.documento_identidad = request.POST['documento_identidad']
            matricula.fecha_matricula = request.POST['fecha_matricula']
            matricula.curso_id = request.POST['curso']
            matricula.instructor_id = request.POST['instructor']  # <-- AGREGADO
            matricula.save()
            messages.success(request, 'Editado ok')
            return redirect('matriculas')
        except ValidationError as e:
            error = e.messages[0] if e.messages else "Error desconocido"
            messages.error(request, error)

    return render(request, 'editarMatricula.html', {
        'matricula': matricula,
        'cursos': cursos,
        'instructores': instructores,  # <-- AGREGADO
        'error': error
    })


def eliminarMatricula(request, id):
    matricula = get_object_or_404(Matricula, id=id)
    matricula.delete()
    messages.success(request, 'Eliminado ok')
    return redirect('matriculas')


def agregarInstructor(request):
    if request.method == 'POST':
        try:
            Instructor.objects.create(
                cedula=request.POST['cedula'],
                apellido=request.POST['apellido'],
                nombre=request.POST['nombre'],
                titulacion=request.POST['titulacion'],
                imginstructor=request.FILES.get('imginstructor')
            )
            messages.success(request, 'Instructor agregado correctamente')
            return redirect('listar_instructores')
        except Exception as e:
            messages.error(request, 'Error al agregar instructor')
            return redirect('agregarInstructor')
    
    return render(request, 'agregarInstructor.html')


def editarInstructor(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    
    if request.method == 'POST':
        try:
            instructor.cedula = request.POST['cedula']
            instructor.apellido = request.POST['apellido']
            instructor.nombre = request.POST['nombre']
            instructor.titulacion = request.POST['titulacion']
            
            if request.FILES.get('imginstructor'):
                instructor.imginstructor = request.FILES.get('imginstructor')
            
            instructor.save()
            messages.success(request, 'Instructor editado correctamente')
            return redirect('listar_instructores')
        except Exception as e:
            messages.error(request, 'Error al editar instructor')
            return redirect('editarInstructor', id=id)
    
    return render(request, 'editarInstructor.html', {'instructor': instructor})


def eliminarInstructor(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    
    try:
        instructor.delete()
        messages.success(request, 'Instructor eliminado correctamente')
        
    except ProtectedError as e:
    
        cursos = instructor.cursos.all()
        matriculas = instructor.matriculas.all()
        cursos_count = cursos.count()
        matriculas_count = matriculas.count()
        
        # Mostrar mensaje de error
        messages.error(
            request,
            f'❌ No se puede eliminar al instructor "{instructor.nombre} {instructor.apellido}" '
            f'porque tiene {cursos_count} curso(s) y {matriculas_count} matrícula(s) asociados.'
        )
    
        return redirect('listar_instructores')
    
    except Exception as e:
        messages.error(request, f'Error al eliminar instructor: {str(e)}')
    
    return redirect('listar_instructores')


def reporteMatricula(request):
    cursos = Curso.objects.annotate(
        total_matriculados=Count('matriculas')
    )
    return render(request, 'matriculaReporte.html', {'cursos': cursos})


def reporteMatriculaPDF(request):
    import weasyprint
    
    cursos = Curso.objects.annotate(total_matriculados=Count('matriculas'))
    html_string = render_to_string('matriculaReporte.html', {'cursos': cursos})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_matriculas.pdf"'

    weasyprint.HTHTML(string=html_string).write_pdf(response)

    return response