import datetime as dt
from polls.utils.constantes import *
from datetime import timezone, datetime, timedelta

# Diccionario que contiene el horario, el salon y cantidad de alumnos
# Ejemplo
# salones_alumnos = {
#   "08:00-09:00":{
#     "501": 1
#     }
# }

dia_semana_actual = datetime.now(UTC_MINUS_6).weekday()

salones_alumnos_actualmente = {}


def ocuparSalon(salon, horario):
    """
    Función que ocupa un salón en un horario específico
    :param salon: str; Numero del salón
    :param horario: str; Horario en formato HH:MM-HH:MM (Inicio-Fin) 24 horas
    :return: str; Mensaje de éxito
    """

    # Si ya hay un horario en el diccionario y no es el mismo que el actual, se limpia
    if len(salones_alumnos_actualmente.keys()) > 0 and list(salones_alumnos_actualmente.keys())[0] != horario:
        salones_alumnos_actualmente.clear()

    if horario not in salones_alumnos_actualmente:
        salones_alumnos_actualmente[horario] = {
            salon: 1
        }
        return

    if salon not in salones_alumnos_actualmente[horario]:
        salones_alumnos_actualmente[horario][salon] = 1
        return

    salones_alumnos_actualmente[horario][salon] += 1


def getSalonesAlumnos(horario_cmp):
    global dia_semana_actual

    if dia_semana_actual != datetime.now(UTC_MINUS_6).weekday():  # Si el día cambió, se limpia el diccionario
        salones_alumnos_actualmente.clear()
        dia_semana_actual = datetime.now(UTC_MINUS_6).weekday()

    if horario_cmp not in salones_alumnos_actualmente.keys():
        return []

    # Se retorna los salones que tienen más de 2 alumnos
    return [salon for salon, alumnos in salones_alumnos_actualmente[horario_cmp].items() if alumnos >= 2]
