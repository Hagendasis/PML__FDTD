import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
import time

def fun():
    start_time = time.time()
    r, n, d, m = 10 ** (-6), 377, 20, 4
    E0, U0 = 8.85 * 10 ** (-12), 4 * math.pi * 10 ** (-7)
    dt = (E0 * U0) ** (1 / 2)
    t, N, f, L, C, M = dt * 100, 100, 3 * 10 ** 7, 100, 1 / (E0 * U0) ** (1 / 2), 100
    dx = L / M
    sxmax = -(m + 1) * math.log(r) / (2 * n * d * dx)
    sx = []
    data = []
    data1 = []
    E1 = []
    Bxnew = []

    for i in range(M + 1):
        sx.append(0.0)
        E1.append(0.0)
        Bxnew.append(0.0)

    for i in range(0, 20):
        sx[i] = ((20 - i) / d) ** m * sxmax
        sx[M - i] = ((20 - i) / d) ** m * sxmax

    def g1i(x):
        return (2 * E0 - dt * sx[x]) / (2 * E0 + dt * sx[x])

    def g2i(x):
        return 2 * dt / (2 * E0 + dt * sx[x])

    def f2i(x):
        return (2 * dt * E0 / (2 * E0 + dt * sx[x])) / U0

    E1[50] = math.cos(2 * math.pi * f * 1 * dt)
    for j in range(1, N):
        E1[50] = math.sin(2 * math.pi * f * j * dt)
        for i in range(0, M):
            Bxnew[i] = g1i(i) * Bxnew[i] + f2i(i) * (E1[i + 1] - E1[i]) / dx
        data1.append(copy.deepcopy(Bxnew))

        for i in range(0, M):
            if i == 0:
                E1[i] = g1i(i) * E1[i] + g2i(i) * ((Bxnew[i] - 0) / dx)
            else:
                E1[i] = g1i(i) * E1[i] + g2i(i) * ((Bxnew[i] - Bxnew[i - 1]) / dx)
        data.append(copy.deepcopy(E1))

    plot_data = data  # 最后画图

    array_1 = np.array(data)
    data = pd.DataFrame(array_1)
    data.to_csv('one dimension.csv', float_format='%.7f')

    array_2 = np.array(data1)
    data = pd.DataFrame(array_2)
    data.to_csv('one dimension1.csv', float_format='%.7f')
    end_time = time.time()
    print("运行时间：" + str(end_time - start_time))
    # 此处可以设置数据的输出方式，如果只想输出某个时刻的图像，去掉循环，将i（小于99）改为具体的值即可
    j=1
    for i in range(0, 98, 5):
        plt.subplot(5,4,j)
        j=j+1
        plt.plot(plot_data[i])
    plt.show()

if __name__=="__main__":
    fun()



