from get_data import all_signals
import matplotlib.pyplot as plt
from getPeaks import getPeaks
from scipy.signal import detrend

### revisamos el funcionamiento de getPeaks

## usamos la 202

fs = 360
timespan = 15
time_cycle = 1.4

señal = all_signals["202"]["upper"][:fs * timespan]
señal = detrend(señal)

peaks = getPeaks(señal, fs, time_cycle / 2, time_cycle / 10)

plt.figure()


plt.subplot(211)
plt.plot(señal)

plt.subplot(212)
plt.plot(peaks)

plt.show()