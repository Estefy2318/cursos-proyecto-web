from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('crear-curso/', views.crearCurso, name='crearCurso'),
    path('editar-curso/<int:id>/', views.editarCurso, name='editarCurso'),
    path('eliminar-curso/<int:id>/', views.eliminarCurso, name='eliminarCurso'),
    path('matriculas/', views.listaMatriculas, name='matriculas'),
    path('crear-matricula/', views.crearMatricula, name='crearMatricula'),
    path('editar-matricula/<int:id>/', views.editarMatricula, name='editarMatricula'),
    path('eliminar-matricula/<int:id>/', views.eliminarMatricula, name='eliminarMatricula'),
    path('reporte-matriculas/', views.reporteMatricula, name='reporteMatricula'),
    path('reporte-matriculas/pdf/', views.reporteMatriculaPDF, name='reporteMatriculaPDF'),
    path('instructores/', views.listar_instructores, name='listar_instructores'),
    path('agregar-instructor/', views.agregarInstructor, name='agregarInstructor'),
    path('editar-instructor/<int:id>/', views.editarInstructor, name='editarInstructor'),
    path('eliminar-instructor/<int:id>/', views.eliminarInstructor, name='eliminarInstructor'),
]
