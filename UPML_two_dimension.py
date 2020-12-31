import math
import matplotlib.pyplot as plt
import time
import copy

def fun():
    start_time = time.time()
    r, n, d, m = 10 ** (-6), 377, 20, 4
    E0, U0 = 8.85 * 10 ** (-12), 4 * math.pi * 10 ** (-7)
    dt = (E0 * U0 / 2) ** (1 / 2)
    t, N, f, L, C, M = dt * 100, 100, 3 * 10 ** 7, 100, 1 / (E0 * U0) ** (1 / 2), 100
    dx = dy = L / M
    sxmax = -(m + 1) * math.log(r) / (2 * n * d * dx)
    sx = []
    sy = []
    data = []
    E1 = []
    Bxnew = []
    Bynew = []
    S = []

    for i in range(M + 1):
        S.append([])
        sx.append(0.0)
        sy.append(0.0)
        E1.append([])
        Bxnew.append([])
        Bynew.append([])
        for j in range(M + 1):
            S[i].append(0.0)
            E1[i].append(0.0)
            Bxnew[i].append(0.0)
            Bynew[i].append(0.0)

    for i in range(0, 20):
        sx[i] = ((20 - i) / d) ** m * sxmax
        sy[i] = ((20 - i) / d) ** m * sxmax
        sx[M - i] = ((20 - i) / d) ** m * sxmax
        sy[M - i] = ((20 - i) / d) ** m * sxmax

    for i in range(0, M + 1):
        for j in range(0, M + 1):
            S[i][j] = sy[i] + sx[j]

    def g1i(z, y):
        return (2 * E0 - dt * S[z][y]) / (2 * E0 + dt * S[z][y])

    def g2i(z, y):
        return 2 * dt / (2 * E0 + dt * S[z][y])

    def f2i(z, y):
        return (2 * dt * E0 / (2 * E0 + dt * S[z][y])) / U0

    for i in range(1, N):
        E1[50][50] = math.sin(2 * math.pi * f * i * dt)

        for j in range(0, M + 1):
            for k in range(0, M):
                Bynew[j][k] = g1i(j, k) * Bynew[j][k] + f2i(j, k) * (E1[j][k + 1] - E1[j][k]) / dx
        for j in range(0, M):
            for k in range(0, M + 1):
                Bxnew[j][k] = g1i(j, k) * Bxnew[j][k] + f2i(j, k) * (E1[j][k] - E1[j + 1][k]) / dy

        for j in range(0, M + 1):
            for k in range(0, M + 1):
                if j == 0:
                    E1[j][k] = g1i(j, k) * E1[j][k] + g2i(j, k) * \
                               ((Bynew[j][k] - Bynew[j][k - 1]) / dx - (Bxnew[j][k] - 0) / dy)
                elif k == 0:
                    E1[j][k] = g1i(j, k) * E1[j][k] + g2i(j, k) * \
                               ((Bynew[j][k] - 0) / dx - (Bxnew[j][k] - Bxnew[j - 1][k]) / dy)
                else:
                    E1[j][k] = g1i(j, k) * E1[j][k] + g2i(j, k) * \
                                ((Bynew[j][k] - Bynew[j][k - 1]) / dx - (Bxnew[j][k] - Bxnew[j - 1][k]) / dy)
        data.append(copy.deepcopy(E1))
    end_time = time.time()
    print("运行时间：" + str(end_time - start_time))
    j = 1
    for i in range(0, 98, 5):
        plt.subplot(5, 4, j)
        j = j + 1
        plt.imshow(data[i])
     # 最后一个图
    plt.figure()
    plt.imshow(data[98])
    plt.show()
if __name__=="__main__":
    fun()


