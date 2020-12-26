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
dt = (E0 * U0/2)**(1/2)
t, N, f, L, C, M = dt*100, 100, 3*10**7, 100, 1/(E0 * U0)**(1/2), 100
dx = dy = L / M
c = dt * C * 2**(1/2)
sxmax = -(m + 1) * math.log(r) / (2 * n * d * dx)
sx0 = -math.log(r) * math.log(3)/(2 * n * dx * (3**d - 1))
sx = []
sy = []
data = []
E1 = []
E2 = []
Bxnew = []
Bynew = []
S = []
for i in range(M+1):
    S.append([])
    sx.append(0.0)
    sy.append(0.0)
    E1.append([])
    E2.append([])
    Bxnew.append([])
    Bynew.append([])
    for j in range(M+1):
        S[i].append(0.0)
        E1[i].append(0.0)
        E2[i].append(0.0)
        Bxnew[i].append(0.0)
        Bynew[i].append(0.0)

for i in range(0, 20):  # 电导率进行初始化
    sx[i] = ((20 - i) / d)**m * sxmax
    sy[i] = ((20 - i) / d)**m * sxmax
    sx[M - i] = ((20 - i)/d)**m * sxmax
    sy[M - i] = ((20 - i)/d)**m * sxmax
for i in range(0, M+1):
    for j in range(0, M+1):
        S[i][j] = sy[i] + sx[j]

# 之后四个函数表示迭代方程前面的四个系数。
def g1i(z, y):
    return (2 * E0 - dt * S[z][y])/(2 * E0 + dt * S[z][y])

def g2i(z, y):
    return 2 * dt/(2 * E0 + dt * S[z][y])

def f1i(z, y):
    return (2 * E0 - dt * S[z][y])/(2 * E0 + dt * S[z][y])

def f2i(z, y):
    return (2 * dt * E0/(2 * E0 + dt * S[z][y]))/U0

#E2[50][50] = math.sin(2 * math.pi * f * 1 * dt)
for i in range(1, N):
    E2[50][50] = math.sin(2 * math.pi * f * i * dt)
    for j in range(0, M+1):
        for k in range(0, M):
            Bynew[j][k] = f1i(j, k) * Bynew[j][k] + f2i(j, k) * (E2[j][k+1] - E2[j][k])/dx
    for j in range(0, M):
        for k in range(0, M + 1):
            Bxnew[j][k] = f1i(j, k) * Bxnew[j][k] + f2i(j, k) * (E2[j][k] - E2[j+1][k]) / dy
        # 此处要保存数据
    for j in range(0, M+1):
        for k in range(0, M+1):
            if j == 0:
                E1[j][k] = g1i(j, k) * E2[j][k] + g2i(j, k) * \
                           ((Bynew[j][k] - Bynew[j][k - 1]) / dx - (Bxnew[j][k] - 0) / dy)
            elif k == 0:
                E1[j][k] = g1i(j, k) * E2[j][k] + g2i(j, k) * \
                           ((Bynew[j][k] - 0) / dx - (Bxnew[j][k] - Bxnew[j - 1][k]) / dy)
            else:
                E1[j][k] = g1i(j, k) * E2[j][k] + g2i(j, k) * \
                           ((Bynew[j][k] - Bynew[j][k-1])/dx-(Bxnew[j][k] - Bxnew[j-1][k])/dy)
    data.append(copy.deepcopy(E1))
    for j in range(M+1):
        for k in range(M+1):
            E2[j][k] = E1[j][k]
# 此处可以设置数据的输出方式，如果只想输出某个时刻的图像，去掉循环，将i（小于99）改为具体的值即可
for i in range(0, 98, 5):
    plt.imshow(data[i])
    plt.show()