# -*- coding: utf-8 -*-
from Tkinter import *
import tkFileDialog
# import correlate
import points

def start():
    '''if F.get()=='C':
        window=Toplevel(root)
        window.title("Fingerprint Check")
        r=correlate.checkFinger(pathImage1.get(),pathImage2.get())
        Label(window, text="Match: "+str(r*100)+"%").pack()
    if F.get()=='P':'''
    print pathImage1.get()
    print type(pathImage1.get())
    exit()
    points.checkFinger(pathImage1.get(), pathImage2.get())

def openImage1(event):
    """Функция для открытия изображение 1"""
    options = {}
    options['defaultextension'] = ''
    options['filetypes'] = [('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['parent'] = root
    options['title'] = 'Открыть изображение 1'
    
    input=tkFileDialog.askopenfilename()
    if input:
        pathImage1.set(input)

def openImage2(event):
    """Функция для открытия изображение 1"""
    options = {}
    options['defaultextension'] = ''
    options['filetypes'] = [('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['parent'] = root
    options['title'] = 'Открыть изображение 2'
    
    output = tkFileDialog.askopenfilename()
    if output:
        pathImage2.set(output)

global root
root = Tk()
root.title("Лучшая программа")
root.iconbitmap('donut.ico')
# root.geometry('300x200+200+100')

# Глобальные и tkinterровские переменные
global pathImage1
global pathImage2
global autoGraph
pathImage1 = StringVar()
pathImage1.set('')
pathImage2 = StringVar()
pathImage2.set('')
autoGraph = StringVar()
autoGraph.set('')

# Поля в которых указываются пути к файлам
inEntry = Entry(root, textvariable=pathImage1)
outEntry = Entry(root, textvariable=pathImage2)

# Кнопки для открытия файла
getImage1 = Button(root, text='Изображение 1')
getImage2 = Button(root, text='Изображение 2')

# Привязываем кнопки к функкциям открытия файла
getImage1.bind('<1>', openImage1)
getImage2.bind('<1>', openImage2)

# Кнопка старта
startButton = Button(root, text='Сравнить', command=start)

# Прикрепляем все к root
inEntry.grid(row=0, column=0)
outEntry.grid(row=1, column=0)

getImage1.grid(row=0, column=1)
getImage2.grid(row=1, column=1)

startButton.grid(row=3, column=1)


root.mainloop()
