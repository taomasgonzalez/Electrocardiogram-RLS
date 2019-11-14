import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



archivo = pd.read_excel("Efectividad.xlsx")
data = archivo.to_dict("list")

nombres = data["Caso"]


performance1 = 100 - np.divide(data["Falsos Positivos"] , data["Positivos"])*100
performance2 = 100 - np.divide(data["Verdaderos Negativos"], data["Negativos"])*100


plt.rcdefaults()
fig, ax = plt.subplots(figsize=(6, 15))
y_pos = np.arange(len(nombres))
ax.barh(y_pos, performance1, xerr=np.zeros(len(nombres)), align='center')

ax.set_yticks(y_pos)
ax.set_yticklabels(nombres)
ax.invert_yaxis()

ax.set_xlabel('Efectividad en positivos bien detectados/positivos detectados(%)')

plt.savefig("Efectividad en detectados.png")
plt.close()

plt.rcdefaults()
fig, ax = plt.subplots(figsize=(6, 15))

y_pos = np.arange(len(nombres))
ax.barh(y_pos, performance2, xerr=np.zeros(len(nombres)), align='center', color="orange")

ax.set_yticklabels(nombres)
ax.set_yticks(y_pos)

ax.invert_yaxis()

ax.set_xlabel('Efectividad en positivos existentes bien detectados/positivos existentes(%)')

plt.savefig("Efectividad en existentes.png")
plt.close()
