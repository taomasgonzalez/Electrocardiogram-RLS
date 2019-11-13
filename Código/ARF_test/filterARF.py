from get_data import all_signals
import numpy as np


class filterARF:
    def __init__(self, n, mu):
        self.w = np.zeros(n + 1)
        self.n = n
        self.mu = mu

        self.w[0] = 1

    def train(self, u, d): # entrenamos el filtro con una señal de impulsos y la señal verdadera
        y = np.zeros(len(u))
        e = np.zeros(len(u))

        last_impulse_position = -1

        for i in range(len(u)):
            if i + 1 >= self.n + 1:
                y[i] = np.dot(self.w, np.flip(u[i + 1 - (self.n + 1):i + 1]))
            else:
                y[i] = np.dot(self.w[:i + 1], np.flip(u[:i + 1]))

            if u[i] == 1:
                last_impulse_position = i

            # calculo error
            e[i] = d[i] - y[i]

            # actualizo coeficientes
            if last_impulse_position != -1:
                k = i - last_impulse_position
                if  k <= self.n:
                    self.w[k] += 2 * self.mu * e[i]# actualizo coeficiente k-esimo

        return y, e

    def run(self, u, d): # ejecutamos el filtro, obtenemos el error
        pass


