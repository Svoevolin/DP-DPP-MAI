import math
import numpy as np
import matplotlib.pyplot as plt


def zero_arr():
    global n
    zero_array = [0] * n
    return zero_array

def inf_arr():
    global n
    inf_array = [math.inf] * n
    return inf_array

def find_max():
    global points
    max1 = 0
    max2 = 0
    for x in np.arange(n):
        if points[x][0] > max1:
            max1 = points[x][0]
        if points[x][1] > max2:
            max2 = points[x][1]
    return max1, max2

def find_min():
    global points
    min1 = math.inf
    min2 = math.inf
    for x in np.arange(n):
        if points[x][0] < min1:
            min1 = points[x][0]
        if points[x][1] < min2:
            min2 = points[x][1]
    return min1, min2

def find_max_time(time):
    global n, points
    max_t = 0
    k1 = 0
    k2 = 0
    for i in range(n):
        if time[i] >= max_t:
            max_t = time[i]
            k2 = k1
            k1 = i
    return k1, k2
def rasst(x, y, x1, y1):
    return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

def top(v1, v2 ): # скалярное произведение
    t = v1[0]*v2[0] + v1[1]*v2[1]
    return t

def down(v1, v2): # произведение длин
    d = (math.sqrt(v1[0] ** 2 + v1[1] ** 2)) * (math.sqrt(v2[0] ** 2 + v2[1] ** 2))
    return d
def peny1(point):
    global gamma, nositel  # Использование глобальных переменных gamma и nositel

    # Задание вектора vect1 в виде [cos(gamma), sin(gamma)]
    vect1 = [math.cos(gamma), math.sin(gamma)]

    # Задание вектора vect2 как разности координат заданной точки и координат nositel
    vect2 = [point[0] - nositel[0], point[1] - nositel[1]]

    # Проверка на деление на 0 и вычисление угла phi между векторами vect1 и vect2
    if point[0] - nositel[0] == 0 or point[1] - nositel[1] == 0:
        phi = 0
    else:
        # Вычисление косинуса угла между векторами vect1 и vect2
        cos_phi = top(vect1, vect2) / down(vect1, vect2)

        # Коррекция значения cos_phi, чтобы оно оставалось в пределах [-1, 1]
        if cos_phi > 1:
            cos_phi = 1
        elif cos_phi < -1:
            cos_phi = -1

        # Вычисление угла phi с использованием арккосинуса
        phi = math.acos(cos_phi)

    return min(phi, math.pi - phi)

def peny2(point1, point2):  # point1 - точка разделения , point2 - точка цели
    global nositel
    vect1 = [point1[0]-nositel[0], point1[1]-nositel[1]]
    vect2 = [point2[0] - point1[0], point2[1] - point1[1]]
    if down(vect1, vect2) == 0:
        phi = 0
    else:
        cos_phi = top(vect1, vect2) / down(vect1, vect2)
        if cos_phi > 1:
            cos_phi = 1
        elif cos_phi < -1:
            cos_phi = -1
        phi = math.acos(cos_phi)
    return min(phi, math.pi - phi)

def optimize1():
    global grid_find, points, n, V, v, t
    opt_point = [0, 0]
    t_iter = zero_arr()
    t_t = list(range(n))
    max_arg = math.inf
    s_now_ts = list(range(n))
    # s_now_nos = 0
    for i in range(grid_find[0], grid_find[1]):
        for j in range(grid_find[2], grid_find[3]):
            s_now_nos = rasst(nositel[0], nositel[1], i, j)
            for step in range(n):
                s_now_ts[step] = rasst(points[step][0], points[step][1], i, j)
                t_iter[step] = (s_now_nos / V) + (s_now_ts[step] / v) + peny1((i, j))*koeff1 + peny2((i,j), (points[step][0], points[step][1]))*koeff2
            if (max(t_iter) <= max_arg):
                max_arg = max(t_iter)
                for k in range(n):
                    t_t[k] = t_iter[k]
                opt_point[0] = i
                opt_point[1] = j
                # print(t_t)
    return t_t, opt_point

def optimize2(d):
    global points, point_razd, nositel, min_time, V, v, rect_nos_razd
    t_iter = zero_arr()
    t_time = zero_arr()
    s_now_ts = list(range(n))
    opt_point = [0, 0]
    point_start = [point_razd[0]-1, point_razd[1]-1]
    min_iter = max(min_time)
    rec =0
    for i in range(0, int(2/d)):
        for j in range(0, int(2/d)):
            s_now_nos = rasst(nositel[0], nositel[1], point_start[0] + i*d, point_start[1] + j*d)
            rect1 = peny1((point_start[0] + i * d, point_start[1] + j * d))
            for step in range(n):
                rect2 = peny2((point_start[0] + i*d, point_start[1] + j*d), (points[step][0], points[step][1]))
                s_now_ts[step] = rasst(points[step][0], points[step][1], point_start[0] + i*d, point_start[1] + j*d)
                t_iter[step] = (s_now_nos / V) + (s_now_ts[step] / v) + rect1*koeff1 + rect2*koeff2

            if max(t_iter) < min_iter:
                min_iter = max(t_iter)
                for k in range(n):
                    t_time[k] = t_iter[k]
                opt_point[0] = i * d + point_start[0]
                opt_point[1] = j * d + point_start[1]
                rec = rect1


    return t_time, opt_point, rec




# количество точек и точки
points = [[3, 4], [2, 6], [3, 8], [5, 9], [8, 7], [9,6], [9,5], [8,4], [6,3], [5,3]]
n = len(points)
t = zero_arr()


koeff1 = 0
koeff2 = 0
# расположение носителя
nositel = [12, 12]

gamma = 0.3*math.pi   # угол по отношению к горизонту

V = 6  # скорость носителя

v = 1  # скорость частей

# максимальное значние сетки по х, y

max_x, max_y = find_max()

# минимальное значение сетки по у и х

min_x, min_y = find_min()

# отступ по сетке

delta_step = 3

# размер сетки

grid_find = [min_x - delta_step, max_x + delta_step, min_y - delta_step, max_y + delta_step]  # начало по х, конец по х, начало по у, конец по у

# поиск точки по целочисленным координатам

min_time = list(range(n))
point_razd = [0, 0]

min_time, point_razd = optimize1()

# проверочный вывод

print("лучшее время1",  min_time)
print("точка разделения1",  point_razd)
print("максимальное время1",  max(min_time))

# поиск точки вокруг найденной

min_time, point_razd, rectangle = optimize2(0.1)
n1, n2 = find_max_time(min_time)
# проверочный вывод


# # print("массив точек",  points)
# # print( "max_x:", max_x, "max_y:", max_y, "min_x:", min_x, "min_y:", min_y)
print("лучшее время2",  min_time)
print("точка разделения2",  point_razd)
print("max время2",  max(min_time))
print("max_время", min_time[n1], min_time[n2])
print("Угол поворота", rectangle*57.3)

# график

Arrow_point = [math.cos(gamma) + nositel[0], math.sin(gamma) + nositel[1]]

arrowprops = {
        'arrowstyle': '->',
    }

arrowprops2 = {
        'color': 'r',
        'arrowstyle': '->',
    }
xy_nos = [point_razd[0], point_razd[1], nositel[0], nositel[1]]

xy_p = [[0] * 4 for i in range(n)]



for k in range(n):
    xy_p[k] = [points[k][0], points[k][1], point_razd[0], point_razd[1]]
    print("[", point_razd[0],";", point_razd[1],"]","[",points[k][0],";", points[k][1],"]" )

fig, ax = plt.subplots()
ax.axis('equal')

ax.plot(nositel[0], nositel[1], marker = '*', color = 'r')
ax.plot(point_razd[0], point_razd[1], marker = 'o', color = 'm')

for k in range(n):
    ax.plot(points[k][0], points[k][1], marker='s', color='b')
    if k != n1 and k != n2:
        plt.annotate('',
                     xy=(xy_p[k][0], xy_p[k][1]),
                     xytext=(xy_p[k][2], xy_p[k][3]),
                     arrowprops=arrowprops)

plt.annotate('',
                     xy=(xy_p[n1][0], xy_p[n1][1]),
                     xytext=(xy_p[n1][2], xy_p[n1][3]),
                     arrowprops=arrowprops2)
plt.annotate('',
                     xy=(xy_p[n2][0], xy_p[n2][1]),
                     xytext=(xy_p[n2][2], xy_p[n2][3]),
                     arrowprops=arrowprops2)

plt.annotate('',
                 xy=(xy_nos[0], xy_nos[1]),
                 xytext=(xy_nos[2], xy_nos[3]),
                 arrowprops=arrowprops)
plt.annotate('',
                 xy=(Arrow_point[0], Arrow_point[1]),
                 xytext=(nositel[0], nositel[1]),
                 arrowprops=arrowprops)

plt.grid(which='major', linestyle=':')
fig.tight_layout()

plt.show()
