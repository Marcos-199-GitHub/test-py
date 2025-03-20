# Librerías
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timezone, timedelta
from pandas.tseries.holiday import Holiday

UTC_MINUS_6 = timezone(timedelta(hours=-6))

# %%
# Cargar la información de horarios del archivo de la base de datos
# Corresponde a una tabla
# Esto se realiza mediante la librería Pandas que trabaja perfectamente
# con archivos .csv
# En esta tabla, dado que hay valores vacíos (NaN) se eliminan, pues es
# complicado trabajar con ellos
HORARIO25_1 = pd.read_csv('archivos/horarios25_1.csv', encoding='utf-8')
HORARIO25_2 = pd.read_csv('archivos/horarios25_2.csv', encoding='utf-8')

COLUMNA_PROFESOR = 'Profesor'
COLUMNA_SALON = 'Salon'


def acondicionarHorario(horario):
    """
    Función que acondiciona el horario con los requerimientos necesarios
    :param horario: df; Horario a acondicionar
    :return:
        horario : df; Horario acondicionado
    """
    horario = horario.fillna(0)
    if horario[COLUMNA_SALON].dtype == 'float64':
        horario[COLUMNA_SALON] = horario[COLUMNA_SALON].astype(int)

    horario[COLUMNA_SALON] = horario[COLUMNA_SALON].astype(str)
    return horario


HORARIO25_1 = acondicionarHorario(HORARIO25_1)
HORARIO25_2 = acondicionarHorario(HORARIO25_2)


HORARIO_SELECCIONADO = HORARIO25_2