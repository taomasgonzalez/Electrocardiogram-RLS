from get_data import all_signals
import matplotlib.pyplot as plt
from getPeaks import getPeaks
from scipy.signal import detrend
from filterARF import filterARF
import numpy as np
import random
from test02filterTrain import plotSignal
from detectError import *
import pandas as pd


def anomaly_plotter(axis, anomalies, timespan, min, max):
    for ai in anomalies:
        if ai < timespan:
            axis.plot([ai, ai], [min, max], 'orange')

minimo = 100000
maximo = -100000

fs = 360
timespan = 5000
time_cycle = 1.4
output = "Nombre | Falsos Positivos | Verdaderos Negativos"

data = {
        "Caso": [],
        "Falsos Positivos": [],
        "Positivos": [],
        "Verdaderos Negativos": [],
        "Negativos": [],
        "Efectividad 1": [],
        "Efectividad 2": []
}

for nombre in all_signals.keys():

    #plotSignal(nombre)

    # plt.savefig("output/%s.png" % nombre, dpi=1000)
    # print("Almacenado output/%s.png" % nombre)
    # plt.close()

    erroresReales, erroresCalculados, countReal, countCalculado = plotSignal(nombre)

    falsosPositivos, verdaderosNegativos = cuantificarError(erroresReales[90 * fs:], erroresCalculados[90 * fs:])

    #output += """%s |
    #%d/%d | %d/%d""" % (nombre, falsosPositivos, countCalculado,verdaderosNegativos, countReal)
    data["Caso"].append(nombre)
    data["Falsos Positivos"].append(falsosPositivos)
    data["Positivos"].append(countCalculado)
    data["Verdaderos Negativos"].append(verdaderosNegativos)
    data["Negativos"].append(countReal)
    data["Efectividad 1"].append(100 - falsosPositivos / countCalculado * 100)
    data["Efectividad 2"].append(100 - verdaderosNegativos / countReal * 100)

    #plt.show()
    print("%s => %d/%d | %d/%d" % (nombre, falsosPositivos, countCalculado,verdaderosNegativos, countReal))
    plt.close()

pd.DataFrame.from_dict(data).to_excel("Efectividad.xlsx", sheet_name='Efectividad')

print(output)
