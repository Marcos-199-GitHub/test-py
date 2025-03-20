# Librerías
import pandas as pd
import numpy as np
import datetime as dt
from polls.utils.constantes import *
from pandas.tseries.holiday import Holiday
from polls.utils.acciones import salones_alumnos_actualmente, getSalonesAlumnos
from datetime import timezone


# Deprecated
def obtener_datos():
    """
    Función que obtiene los datos de los horarios de los profesores
    :return:
        horaActual : str; Hora actual en formato HH:MM
        horaCompar : datetime.time; Hora actual en formato datetime.time
        diaSemActual : int; Día de la semana actual
        profesores : list; Lista de nombres de profesores
        seleccion : str; Horario de un profesor seleccionado
        horario[colSem[int(diaSemActual)]] : list; Horario de un día de la semana
        eRooms : list; Salones vacíos en la hora actual
        salon : str; Horario de un salón seleccionado

    """
    # CARGAR LA FECHA ACTUAL
    fechaActual = dt.datetime.now()
    # Formatear el objeto fecha actual para obtener la
    # hora actual
    horaActual = fechaActual.strftime('%H:%M')
    horaCompar = dt.datetime.strptime(horaActual, '%H:%M').time()
    # Día actual
    diaSemActual = int(fechaActual.strftime('%w'))
    diaSemActual -= 1
    # print(f'{horaActual}\t{horaCompar}\t{diaSemActual}')

    # %%
    # Obtener la lista de profesores ordenados alfabéticamente
    # Se obtiene, leyendo de la tabla 'horario', la columna COLUMNA_PROFESOR
    # luego a esto se le aplica el método unique() que regresa una columna de datos
    # con valores únicos (sin repetición) y finalmente, se convierte en lista
    profesores = HORARIO_SELECCIONADO[COLUMNA_PROFESOR].unique().tolist()

    # TODO: Usando la lista profesores se puede rellenar un control para seleccionar
    #       por ejemplo
    # print("--PROFESORES--")
    # print(profesores)

    # %%
    # Por ejemplo para obtener los grupos que lleva un profesor en particular
    # Se usa de la tabla 'horario' se busca donde el valor de la columna COLUMNA_PROFESOR sea igual
    # a algún valor
    seleccion = HORARIO_SELECCIONADO[HORARIO_SELECCIONADO[COLUMNA_PROFESOR] == 'CASTAÑEDA GALVAN ADRIAN ANTONIO']
    # Mostrar el horario del profesor seleccionado
    # print("--HORARIO--")
    # print(seleccion.to_string())
    # seleccion.to_csv('tmp', index=False)

    # TODO: Agregar una hora en específico para conocer disponibilidad de salón
    # Revisar que salones están vacíos en la hora actual
    # Generar una lista con los valores de los días de la semana en columnas
    colSem = HORARIO_SELECCIONADO.columns[5:10].tolist()
    # Recorrer todos los horarios
    vac = []
    vac2 = []
    for j, dd in enumerate(HORARIO_SELECCIONADO[colSem[int(diaSemActual)]]):
        # Si es diferente de cero
        if dd != '0':
            try:
                # Separar el tiempo en horas y minutos inicial y final de la clase
                ini, fin = dd.split('-')
                ini = dt.datetime.strptime(ini, '%H:%M').time()
                fin = dt.datetime.strptime(fin, '%H:%M').time()
                # Cuando el salón está ocupado
                if ini <= horaCompar <= fin:
                    pass
                    # print('', end="")
                else:
                    vac.append(j)
            except:
                pass
                # print('', end="")
        # en otro caso
        else:
            vac.append(j)
    # Mostrar los salones vacíos en esa hora
    # print("--SALONES VACÍOS--")
    eRooms = np.sort(HORARIO_SELECCIONADO.loc[vac, COLUMNA_SALON].unique()).tolist()
    # print(eRooms)

    # En otro caso, colocar un salón y buscar que horarios está ocupado
    salon = HORARIO_SELECCIONADO[HORARIO_SELECCIONADO[COLUMNA_SALON] == '318']
    print("--OCUPABILIDAD SALÓN--")
    # print(salon.to_string())
    # salon.to_csv('tmp3', index=False)

    return (horaActual, horaCompar, diaSemActual, profesores, seleccion.to_dict(orient='records'),
            HORARIO_SELECCIONADO[colSem[int(diaSemActual)]].to_string(), eRooms, salon.to_dict(orient='list'))


def getProfesores():
    """
    Función que obtiene los nombres de los profesores
    :return:
        profesores : list[str]; Lista de nombres de profesores
    """
    profesores = HORARIO_SELECCIONADO[COLUMNA_PROFESOR].unique().tolist()
    return profesores


def getHorarioProfesor(profesor):
    """
    Función que obtiene el horario de un profesor
    :param profesor: str; Nombre del profesor
    :return:
        horario : dict; Horario del profesor
    """
    seleccion = HORARIO_SELECCIONADO[HORARIO_SELECCIONADO[COLUMNA_PROFESOR] == profesor]
    return seleccion.to_dict(orient='records')


def getSalonesLibresYOcupados(horario_cmp, dia_sem):
    """
    Función que obtiene los salones libres en la hora actual
    :param horario_cmp: str; Horario en formato HH:MM-HH:MM (Inicio-Fin) 24 horas
    :param dia_sem: int; Día de la semana 0-5 (Lunes-Sabado)
    :return: list[str]; Salones vacíos en la hora actual y list[str]; Salones ocupados en la hora actual
    """
    horaCompar = dt.datetime.strptime(horario_cmp.split('-')[0], '%H:%M').time()
    diaSemActual = dia_sem

    colSem = HORARIO_SELECCIONADO.columns[5:11].tolist()
    vac = []
    ocupados = []
    for j, dd in enumerate(HORARIO_SELECCIONADO[colSem[diaSemActual]]):
        # print(dd)
        if dd == '0':  # Si no hay horario
            vac.append(j)
        else:
            try:
                ini, fin = dd.split('-')
                ini = dt.datetime.strptime(ini, '%H:%M').time()
                fin = dt.datetime.strptime(fin, '%H:%M').time()
                if ini <= horaCompar < fin:
                    ocupados.append(j)
                else:
                    vac.append(j)
            except:
                pass

    salones_libres = np.sort(HORARIO_SELECCIONADO.loc[vac, COLUMNA_SALON].unique()).tolist()
    salones_ocupados = np.sort(HORARIO_SELECCIONADO.loc[ocupados, COLUMNA_SALON].unique()).tolist()
    salones_alumnos = []

    for salon in getSalonesAlumnos(horario_cmp):
        if salon in salones_libres:
            salones_libres.remove(salon)
            salones_alumnos.append(salon)

    return [i for i in salones_libres if i not in salones_ocupados], salones_ocupados, salones_alumnos


def getHorarioSalon(salon):
    """
    Función que obtiene el horario de un salón
    :param salon: str; Nombre del salón
    :return:
        horario : dict; Horario del salón
    """
    seleccion = HORARIO_SELECCIONADO[HORARIO_SELECCIONADO[COLUMNA_SALON] == salon]
    return seleccion.to_dict(orient='records')
