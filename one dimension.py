import numpy as np
import pandas as pd
import math
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d
import copy

r, n, d, m = 10**(-6), 377, 20, 4
E0, U0 = 8.85 * 10**(-12), 4 * math.pi * 10**(-7)
dt = (E0 * U0)**(1/2)
t, N, f, L, C, M = dt*100, 100, 3*10**7, 100, 1/(E0 * U0)**(1/2), 100
dx = L / M
c = dt * C
sxmax = -(m + 1) * math.log(r) / (2 * n * d * dx)
sx0 = -math.log(r) * math.log(3)/(2 * n * dx * (3**d - 1))
sx = []
data = []
data1 = []
E1 = []
E2 = []
Bxnew = []

for i in range(M+1):
    sx.append(0.0)
    E1.append(0.0)
    E2.append(0.0)
    Bxnew.append(0.0)

for i in range(0, 20):  # 电导率进行初始化
    sx[i] = ((20 - i) / d)**m * sxmax
    sx[M - i] = ((20 - i)/d)**m * sxmax

def g1i(x):
    return (2 * E0 - dt * sx[x])/(2 * E0 + dt * sx[x])

def g2i(x):
    return 2 * dt/(2 * E0 + dt * sx[x])

def f1i(x):
    return (2 * E0 - dt * sx[x])/(2 * E0 + dt * sx[x])

def f2i(x):
    return (2 * dt * E0/(2 * E0 + dt * sx[x]))/U0

E2[50] = math.cos(2 * math.pi * f * 1 * dt)
for j in range(1, N):
    E2[50] = math.sin(2 * math.pi * f * j * dt)
    for i in range(0, M):
        Bxnew[i] = f1i(i) * Bxnew[i] + f2i(i) * (E2[i+1] - E2[i])/dx
    data1.append(copy.deepcopy(Bxnew))
        # 此处要保存数据
    for i in range(0, M):
        if i == 0:
            E1[i] = g1i(i) * E2[i] + g2i(i) * ((Bxnew[i] - 0) / dx)
        else:
            E1[i] = g1i(i) * E2[i] + g2i(i) * ((Bxnew[i] - Bxnew[i-1])/dx)
    data.append(copy.deepcopy(E1))
    for i in range(M+1):
        E2[i] = E1[i]
# 此处可以设置数据的输出方式，如果只想输出某个时刻的图像，去掉循环，将i（小于99）改为具体的值即可
for i in range(0, 98, 5):
     plt.plot(data[i])
     plt.show()
array_1 = np.array(data)
data = pd.DataFrame(array_1)
writer=pd.ExcelWriter('one dimension.xlsx')
data.to_excel(writer, 'sheet_1', float_format='%.7f')
writer.save()
writer.close()

array_2 = np.array(data1)
data = pd.DataFrame(array_2)
writer=pd.ExcelWriter('one dimension1.xlsx')
data.to_excel(writer, 'sheet_1', float_format='%.7f')
writer.save()
writer.close()
