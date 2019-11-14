import numpy as np


def getPeaks(signal, fs, min_distance, impulse_distance=0):
    """
    signal: samples
    min_distance: distance of peaks
    fs: sample frecuency
    """
    power_signal = np.power(signal, 2)

    # Consideramos que la señal no variara considerablemente en al menos 10 periodos del filtro
    stationarity_size = 10 * 500

    max_value = max(power_signal[:stationarity_size])  # maximo valor de la potencia en el primer intervalo estacionario

    peakSignal = np.zeros(len(signal))  # señal donde almacenamos los picos

    counter = 0
    impulse_ticks = int(impulse_distance * fs)

    for i in range(len(signal)):
        if i % stationarity_size == 0:
            max_value = max(power_signal[:stationarity_size])

        if counter > 0:
            counter -= 1
        elif power_signal[i] > max_value * 0.43:
            counter = min_distance * fs
            if i > impulse_ticks:
                peakSignal[i - impulse_ticks] = 1

    return peakSignal
