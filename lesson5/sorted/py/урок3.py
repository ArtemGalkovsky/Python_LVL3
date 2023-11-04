'''
a=int(input('Введи первое число'))
b=int(input('Введи второе число'))
c=int(input('Введи третье число'))
if a>=0:
    print(a**2)
else:
    print(a**3)
if b>=0:
    print(b**2)
else:
    print(b**3)
if c>=0:
    print(c**2)
else:
    print(c**3)
'''
import math 
x1=int(input('Введите x координату первой точки'))
y1=int(input('Введите y координату первой точки'))
x2=int(input('Введите x координату второй точки'))
y2=int(input('Введите y координату второй точки'))
x3=int(input('Введите x координату третьей точки'))
y3=int(input('Введите y координату третьей точки'))
if math.sqrt(x3*x3+y3*y3)>math.sqrt(x1*x1+y1*y1)<math.sqrt(x2*x2+y2*y2):
    print('Точка 1 ближе')
elif math.sqrt(x1*x1+y1*y1)>math.sqrt(x2*x2+y2*y2)<math.sqrt(x3*x3+y3*y3):
    print('Точка 2 ближе')
elif math.sqrt(x1*x1+y1*y1)>math.sqrt(x3*x3+y3*y3)<math.sqrt(x2*x2+y2*y2):
    print('Точка 3 ближе')

