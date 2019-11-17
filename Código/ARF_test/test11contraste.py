import padasip as pa
from get_data import all_signals
import matplotlib.pyplot as plt
from getPeaks import getPeaks
from scipy.signal import detrend
import scipy.signal as scisig
import numpy as np
from scipy.signal import find_peaks
from scipy.linalg import toeplitz

fs = 360
timespan = 60
time_cycle = 1.4


original = all_signals["202"]["upper"][:fs * timespan]

b, a = scisig.butter(4, 0.1 * 2 * np.pi, btype='highpass', fs=360)
señal = scisig.filtfilt(b, a, original)

peaksList, _ = find_peaks(señal, height=0.5, distance=time_cycle/4*fs)
peaks = getPeaks(señal, fs, time_cycle / 2, time_cycle / 10)

impulse_distance = int(time_cycle / 2 * fs)

peaks = np.zeros(len(señal))

for peak in peaksList:
    if peak - impulse_distance >= 0:
        peaks[peak - impulse_distance] = 1

t = np.arange(len(original)) / fs
output = np.zeros(len(señal))

fig, (ax0, ax1, ax2) = plt.subplots(3, sharex=True)

filt = pa.filters.FilterLMS(500, mu=0.5, w='zeros')
filt2 = pa.filters.FilterRLS(500, mu=0.9, w='zeros')

x = np.zeros((len(señal), 500))

for i in range(len(señal)):
    arr = np.zeros(500)
    for j in range(500):
        if i - j >= 0:
            arr[j] = peaks[i - j]
    x[i] = arr

y, e, w = filt.run(señal, x)
y2, e, w = filt2.run(señal, x)

ax0.plot(t, señal)

ax1.plot(t, y)
ax2.plot(t, y2)

plt.show()