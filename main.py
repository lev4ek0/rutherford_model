import math
import os

import imageio as imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.style.use('seaborn-whitegrid')
fig, xy = plt.subplots()

# входные даные. их можно изменять

mashtab = 10
const = 1e-12
h = 1.0e-24  # шаг
Vx0 = 1.0e7  # скорость вылета частицы из точки О вдоль оси оx
Vy0 = 0  # скорость вылета частицы из точки О вдоль оси оу
q = 1.6e-19  # заряд изотопов
aem = 1.661e-27  # 1 а.е.м.
x0 = -mashtab*const  # начальная координата по X
k = 1 / (4 * math.pi * 8.85e-12)
m = 4 * aem
q1 = 79 * q
q2 = 2 * q


# тело программы. Тут уже ничего не трогать.

def getYY(qa, qb, r1, r2, mass):
    return k * qa * qb / (math.sqrt(r1 ** 2 + r2 ** 2)) ** 2 / mass


# params = [5e-13]
# params = [2e-13]
# params = [1e-13]
# params = [5e-14]
# params = [2e-14]
params = [5e-12]
# for i in range(-2, 1, 1):
#     if i != 0:
#         params.append(i * 1e-14)

arrayy = []
for y0 in params:
    X = [x0]
    Y = [y0]
    x = x0 + h * Vx0 + h ** 2 / 2 * getYY(q1, q2, x0, y0, m) * x0 / math.sqrt(x0 ** 2 + y0 ** 2)
    y = y0 + h * Vy0 + h ** 2 / 2 * getYY(q1, q2, y0, y0, m) * y0 / math.sqrt(x0 ** 2 + y0 ** 2)

    Vx = Vx0 + getYY(q1, q2, x, y, m) * x / math.sqrt(x ** 2 + y ** 2) * h
    Vy = Vy0 + getYY(q1, q2, x, y, m) * y / math.sqrt(x ** 2 + y ** 2) * h

    prev_Vx = Vx0
    prev_Vy = Vy0

    prev_x = x0
    prev_y = y0
    counter = 0
    while np.isfinite(y) and -mashtab * const < x < mashtab * const and -mashtab * const < y < mashtab * const:
        X.append(x)
        Y.append(y)
        counter += 1
        constAx = getYY(q1, q2, x, y, m) * x / math.sqrt(x ** 2 + y ** 2)
        constAy = getYY(q1, q2, x, y, m) * y / math.sqrt(x ** 2 + y ** 2)

        val1 = x
        x = h ** 2 * constAx + 2 * x - prev_x
        prev_x = val1

        val2 = y
        y = h ** 2 * constAy + 2 * y - prev_y
        prev_y = val2

        val3 = Vx
        Vx = prev_Vx + constAx * h
        prev_Vx = val3

        val4 = Vy
        Vy = prev_Vy + constAy * h
        prev_Vy = val4

        if counter % (1000 * mashtab) == 0:
            plt.title("Моделирование частицы")
            plt.xlabel("X")
            plt.ylabel("Y")
            xy.xaxis.set_major_locator(ticker.MultipleLocator(const / 10 * mashtab))
            xy.yaxis.set_major_locator(ticker.MultipleLocator(const / 10 * mashtab))
            plt.grid(True)
            xy.plot(X, Y, c='deeppink')
            xy.scatter(0, 0, c='deeppink')
            # plt.xlim(-3.0e-13, 5.0e-13)
            # plt.ylim(-3.0e-13, 3.0e-13)
            plt.xlim(-mashtab * const, mashtab * const)
            plt.ylim(-mashtab * const, mashtab * const)
            arrayy.append('{}-{}.png'.format(x, y))
            plt.savefig('{}-{}.png'.format(x, y))

with imageio.get_writer('{}-{}.gif'.format(params[0], mashtab), mode='I', duration=0.02) as writer:
    for filename in arrayy:
        image = imageio.imread(filename)
        writer.append_data(image)
    writer.close()

for filename in set(arrayy):
    os.remove(filename)
