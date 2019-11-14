import numpy as np

thresholdError = 7.5

fs = 360

def getErrors(signal, periodSignal):
    acum = 0

    output = np.zeros(len(signal))
    wavgSum = 0
    errorCount = 0

    for i in range(len(signal)):
        acum += signal[i]**2
        wavgSum += signal[i]**2 * i

        if periodSignal[i] > 0.5:
            #print(acum)
            if acum > thresholdError:
                wavg = int(round(wavgSum /acum))

                output[wavg] = 1
                errorCount += 1
            wavgSum = 0
            acum = 0 # reset

    return output, errorCount


def cuantificarError(erroresReales, erroresCalculados):
    falsosPositivos = 0
    verdaderosNegativos = 0

    minDistance = 10 * fs

    okRange = np.zeros(len(erroresReales))

    for i in range(len(erroresCalculados)):
        if erroresCalculados[i] > 0.5:
            okRange[i-minDistance:i+minDistance] = 1

    for i in range(len(erroresReales)):
        if erroresReales[i] > 0.5 and okRange[i] < 0.5:
            #print("Verdadero negativo en %0.2f" % ((i + 90 * fs) / fs))
            verdaderosNegativos += 1

    okRange = np.zeros(len(erroresReales))

    for i in range(len(erroresReales)):
        if erroresReales[i] > 0.5:
            okRange[i - minDistance:i + minDistance] = 1

    for i in range(len(erroresCalculados)):
        if erroresCalculados[i] and okRange[i] < 0.5:
            #print("Falso positivo en %0.2f" % ((i+90*fs)/fs) )
            falsosPositivos += 1

    return falsosPositivos, verdaderosNegativos




