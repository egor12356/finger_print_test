# -*- coding: utf-8 -*-

from Tkinter import *
# import Image
import templateSkeletize2 as sk
from PIL import Image


def binary(img):
    """Переводим изображение в черно-белое, а потом в биты"""
    bImg = []
    for i in range(img.size[0]):
        tmp = []
        for j in range(img.size[1]):
            t = img.getpixel((i, j))
            # print t
            p = t[0] * 0.3 + t[1] * 0.59 + t[2] * 0.11
            if p > 128:
                p = 1
            else:
                p = 0
            tmp.append(p)
        bImg.append(tmp)

    # print bImg
    return bImg
    
def __removeDouble(x, y):
    """возвращает список элементов, у которых нет одинакового в другом списке"""
    z = []
    for i in x:
        c = True
        for j in y:
            if i == j:
                c = False
        if c:
            z.append(i)
    for i in y:
        c = True
        for j in x:
            if i == j:
                c = False
        if c:
            z.append(i)
    return z

def delNoisePoint(r):
    """Дополнительное удаление шумов"""
    tmp = []
    tmp2 = []
    for i in r[1]:
        x = range(i[0]-5, i[0]+5)
        y = range(i[1]-5, i[1]+5)
        for j in r[0]:
            if j[0] in x and j[1] in y: 
                tmp.append(i)
                tmp2.append(j)
    return (__removeDouble(r[0], tmp2), __removeDouble(r[1],tmp))
    
def matchingPoint(arr_point_image1, arr_point_image2):
    """вход: кортеж точек эталона и кортеж проверяемого; выход (совпало, всего)"""
    all = 0
    match = 0
    for i in arr_point_image2[0]:
        x = range(i[0]-15, i[0]+15)
        y = range(i[1]-15, i[1]+15)
        all += 1
        for j in arr_point_image1[0]:
            if j[0] in x and j[1] in y: 
                match += 1
                break
    for i in arr_point_image2[1]:
        x = range(i[0]-15, i[0]+15)
        y = range(i[1]-15, i[1]+15)
        all += 1
        for j in arr_point_image1[1]:
            if j[0] in x and j[1] in y:
                match += 1
                break

    return (match, all)
        

def checkThisPoint(img, x, y):
    """подсчет количества черных в окрестности"""
    c = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if img[i][j] == 0:
                c += 1
    return c-1

def findCheckPoint(img):
    """формирование списков точек (массивы координат) ветвления и конечных"""
    x = len(img)
    y = len(img[0])
    branchPoint = []
    endPoint = []
    for i in range(x):
        for j in range(y):
            if img[i][j] == 0:
                # подсчет количества черных в окрестности
                t = checkThisPoint(img, i, j)
                if t == 1:
                    endPoint.append((i, j))
                if t == 3:
                    branchPoint.append((i, j))
    return (branchPoint, endPoint)
 
def checkFinger(pathImage1_str, pathImage2_str):
    # Открываем изображение 1
    image1 = Image.open(pathImage1_str)
    # Переводим в биты
    image1_byte = binary(image1)

    # Скелетизация
    # вызов процедуры скелетизации, на входе список списков(после бинаризации)
    sk.tmpDelete(image1_byte)

    # формирование списков точек ветвления и конечных
    arr_point_image1 = findCheckPoint(image1_byte)
    # Дополнительное удаление шумов
    arr_point_image1 = delNoisePoint(arr_point_image1)

    # #########################################################
    # Открываем изображение 2
    image2 = Image.open(pathImage2_str)

    # Переводим в биты
    image2_byte = binary(image2)

    # Скелетизация
    # вызов процедуры скелетизации, на входе список списков(после бинаризации)
    sk.tmpDelete(image2_byte)
    # формирование списков точек ветвления и конечных
    arr_point_image2 = findCheckPoint(image2_byte)
    # Дополнительное удаление шумов
    arr_point_image2 = delNoisePoint(arr_point_image2)

    # Простой поиск точки которая попадает в окрестность 30*30 и является точкой того же типа.
    match, all = matchingPoint(arr_point_image1, arr_point_image2)
    result = round(((match / float(all)) * 100), 2)

    
    root=Tk()
    w = len(image2_byte)
    h = len(image2_byte[0])
    C = Canvas(root, width=w*2, height=h)
    # C = Canvas(root, width=600, height=650)


    # Отмечаем на холсте найденные фотки
    for i in range(w):
        for j in range(h):
            if image1_byte[i][j] == 0:
                C.create_line([(i, j), (i+1, j+1)])
            if image2_byte[i][j] == 0:
                C.create_line([(i+w+1, j+1), (i+w, j)])
    for i in arr_point_image1[0]:
        C.create_oval([(i[0]-3, i[1]-3), (i[0]+3, i[1]+3)], outline="#ff0000")
    for i in arr_point_image1[1]:
        C.create_rectangle([(i[0]-3, i[1]-3), (i[0]+3, i[1]+3)], outline="#0000ff")
    for i in arr_point_image2[0]:
        C.create_oval([(i[0]-3+w, i[1]-3), (i[0]+3+w, i[1]+3)], outline="#ff0000")
    for i in arr_point_image2[1]:
        C.create_rectangle([(i[0]-3+w, i[1]-3), (i[0]+3+w, i[1]+3)], outline="#0000ff")

    C.create_text((w, h*0.95), fill="#009900", text=str(result) + "%", font='Arial,72')

    C.pack()
    root.mainloop()
