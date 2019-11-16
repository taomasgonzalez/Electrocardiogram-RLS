from get_data import all_signals
import matplotlib.pyplot as plt
from getPeaks import getPeaks
from scipy.signal import detrend
from filterARF import filterARF
from scipy.signal import find_peaks
import numpy as np
import scipy.signal as scisig
from detectError import getErrors, cuantificarError
import padasip

fs = 360

def plotSignal(code):

    timespan = 60
    time_cycle = 1.4
    # señal = no_noise_signal
    original = all_signals[code]["upper"][:timespan*fs]
    t = np.arange(len(original)) / fs
    errores = list(all_signals[code]["anomalies"].keys())
    errores = [float(errores[i]) / fs for i in range(len(errores))]


    def anomaly_plotter(axis, anomalies, timespan, min, max):
      for ai in anomalies:
        if ai < timespan:
            axis.plot([ai, ai], [0, max], 'orange')

    def anomaly_plotter2(axis, anomalies, timespan, min, max):
      for ai in anomalies:
        if ai < timespan:
            axis.plot([ai, ai], [min, 0], 'violet')


    b, a = scisig.butter(4, 0.1 * 2 * np.pi, btype='highpass', fs=360)

    señal = scisig.filtfilt(b, a, original)

    #señal = detrend(original)      # quitamos la tendencia que agrega el ruido de línea y de los movimientos corporales
    #peaks = getPeaks(señal, fs, time_cycle / 2, time_cycle / 10)
    peaksList, _ = find_peaks(señal, height=0.5, distance=time_cycle/4*fs)
    peaks = np.zeros(len(señal))

    impulse_distance = int(time_cycle/2*fs)

    for peak in peaksList:
        if peak - impulse_distance >= 0:
            peaks[peak - impulse_distance] = 1

    #myFilterARF = filterARF(500, 0.01)
    #filtered, error = myFilterARF.train(peaks, señal)

    N = 500

    filt = padasip.filters.FilterRLS(N, mu=0.95, w='zeros')

    x = np.zeros((len(señal), N))

    for i in range(len(señal)):
        arr = np.zeros(N)
        for j in range(N):
            if i - j >= 0:
                arr[j] = peaks[i - j]
        x[i] = arr

    filtered, error, w = filt.run(señal, x)

    fig, (ax0, ax1, ax2, ax3, ax4, ax5) = plt.subplots(6, sharex=True, sharey=True)
    ax0.set_ylim(-2.5, 2.5)
    ax3.set_ylim(-2.5, 2.5)

    ax0.plot(t, original)

    ax1.plot(t, señal)
    anomaly_plotter(axis=ax1, anomalies=errores, timespan=timespan, min=min(señal), max=max(señal))

    ax2.plot(t, peaks)
    ax3.plot(t, filtered)

    anomaly_plotter(axis=ax4, anomalies=errores, timespan=timespan, min=min(error), max=max(error))

    ax4.plot(t, abs(error))

    error_points, errorCount = getErrors(error, peaks)

    ax5.plot(t, error_points)

    # erroresReales = np.zeros(len(original))
    #
    # for a in errores:
    #     erroresReales[int(round(a*fs))] = 1
    #
    # erroresCalculados = error_points

    erroresReales = 0
    erroresCalculados = error_points

    return erroresReales, erroresCalculados, len(errores), errorCount

if 1:
    erroresReales, erroresCalculados, countReal, countCalculado = plotSignal("202")


    #falsosPositivos, verdaderosNegativos = cuantificarError(erroresReales[90*fs:], erroresCalculados[90*fs:])

    #print("Falsos positivos: %d/%d" % (falsosPositivos, countCalculado))
    #print("Verdaderos negativos: %d/%d" % (verdaderosNegativos, countReal))

    plt.show()