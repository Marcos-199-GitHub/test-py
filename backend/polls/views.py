from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from polls.utils.extraccion import *
import json


# Create your views here.
def main_view(request):
    horaActual, horaCompar, diaSemActual, profesores, seleccion, horarius, eRooms, salon = obtener_datos()

    context = {
        'horaActual': horaActual,
        'horaCompar': horaCompar,
        'diaSemActual': diaSemActual,
        'profesores': profesores,
        'seleccion': seleccion,
        'horario': horarius,
        'eRooms': eRooms,
        'salon': salon
    }
    return render(request, 'index.html', context)


def profesores_view(request):
    response = JsonResponse({'result': getProfesores()})
    return response


@csrf_exempt
def horario_profesor_view(request):
    profesor = json.loads(request.body).get('profesor')
    response = JsonResponse({'result': getHorarioProfesor(profesor)})
    return response


@csrf_exempt
def salones_libres_view(request):
    hora_cmp = json.loads(request.body).get('hora')
    dia_sem = json.loads(request.body).get('dia_semana')
    response = JsonResponse({'result': getSalonesLibresYOcupados(hora_cmp, dia_sem)[0]})
    return response


@csrf_exempt
def salones_ocupados_view(request):
    hora_cmp = json.loads(request.body).get('hora')
    dia_sem = json.loads(request.body).get('dia_semana')
    response = JsonResponse({'result': getSalonesLibresYOcupados(hora_cmp, dia_sem)[1]})
    return response


@csrf_exempt
def horario_salon_view(request):
    salon = json.loads(request.body).get('salon')
    response = JsonResponse({'result': getHorarioSalon(salon)})
    return response
