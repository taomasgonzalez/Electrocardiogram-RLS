# https://github.com/MIT-LCP/wfdb-python
# https://wfdb.readthedocs.io/en/latest/
import numpy as np
import wfdb
import matplotlib.pyplot as plt
import padasip as pa


def get_data(file_path, sampto='end'):
    """
    get_data devuelve las señales del primer y segundo canal de un archivo que cumple con el estándar wfdb,
    la metadata del mismo y las anotaciones del mismo en caso de haberlas (archivo con el mismo nombre pero con extensión .atr)

    Parámetros:
      file_path: path del archivo de donde conseguir las señales a leer.
      sampto: cantidad de samples a leer. Si 'end', lee todas las samples del archivo.
    Returns:
      signal_0: Señal del primer canal.
      signal_1: Señal del segundo canal.
      metadata: metadata que contiene, entre otras cosas, la sample frequency utilizada para tomar los datos.
      annotation: anotaciones correspondientes al archivo
    """
    # Cada columna de la matriz signals es un canal de las señales grabadas del paciente(signals[0] es el primer canal)
    # metadata tiene información como la sample frequency, importante para el resto del trabajo.
    signals, metadata = wfdb.rdsamp(record_name=file_path, sampto=sampto)
    annotation = wfdb.rdann(record_name=file_path, extension='atr', sampto=sampto)

    return signals[:, 0], signals[:, 1], metadata, annotation

all_signals = {str(i): dict() for j in (range(100, 125), range(200, 224)) for i in j}
# borramos del dictionary a los archivos que no estan pero que fueron agregados por comodidad
for i in ['110', '120', '204', '206', '211', '216', '218']: del all_signals[i]
all_signals['228'] = None
for i in range(230, 235): all_signals[str(i)] = None

for signal_name in all_signals.keys():
    upper_signal, lower_signal, metadata, annotations =  get_data(file_path='data/' + signal_name,sampto=None)
    #print(metadata)
    all_signals[signal_name] = {'upper' : upper_signal, 'lower' : lower_signal, 'meta':metadata, 'annot': annotations}

for key in all_signals.keys():
    anot = all_signals[key]['annot']
    anot.symbol = ['A' if i is not 'N' else 'N' for i in anot.symbol]
    # guardamos el sample en el que se produce la anomalia y el indice de la misma en el anot.sample
    all_signals[key]['anomalies'] = {anot.sample[i]: i for i in range(len(anot.symbol)) if anot.symbol[i] is 'A'}
    # guardamos el sample en el que se produce la anotacion normal y el indice de la misma en el anot.sample
    all_signals[key]['not_anomalies'] = {anot.sample[i]: i for i in range(len(anot.symbol)) if anot.symbol[i] is 'N'}

# anot = all_signals[list(all_signals.keys())[0]]['annot']
