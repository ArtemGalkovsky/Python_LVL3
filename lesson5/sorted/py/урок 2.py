
a=int(input())
b=int(input())
if a>b:
    print(a, '>', b)
elif a==b:
    print(a, '=', b)
else:
    print(a, '<', b)
print('end of program')

'''


a=int(input())
b=int(input())
c=int(input())
if b<a>c:
    print(a)
elif a<b>c:
    print(b)
else:
    print(c)

print('Привет как твоё имя?')
n=str(input('Имя'))
print('В каом ты классе')
a=int(input('Класс'))
if a==8:
    print('Приветик', n, 'молодец!')
elif a==9:
    print('Привет', n, 'ну ты и крутой!')
elif a==10:
    print('Приветище, человечище', n)
else:
    print('Ты кто вообще?')

from random import*
a=int(input())
b=randint(1, 21)
while a!=b:
    if a>b:
        print('Загаданное число меньше')
    elif a<b:
        print('Загаданное число больше')
    a=int(input())        
print('Правильное число!')

y=int(input('Год рождения'))
m=int(input('Месяц'))
d=int(input('День'))
yn=(2022)
mn=(9)
dn=(18)
yl=(yn-y)
ml=(mn-m)
dl=(dn-d)
yd=(yl*365)
md=(ml*30)
dd=(yd+md+dl)
print(dd)
if dd>10000:
    print('Ну ты крут!')


a=int(input('Выбери дверь 1, 2 или 3'))
if a==1:
    a1=int(input('Выбери дверь 11 или 12'))
    if a1==11:
        print('Ты попал в паутину')
    elif a1==12:
        print('Ты подружился с динозавром, но он предал и съел тебя')
elif a==2:
    a2=int(input('Выбери дверь 21'))
    if a2==21:
        a4=int(input('Выбери дверь 211 или 311'))
        if a4==211:
            print('Ты попал в паутину')
        elif a4==311:
            print('Ты проиграл обезьяне с гранатой')
elif a==3:
    a3=int(input('Выбери дверь 31, 32 или 33'))
    if a3==31:
        a5=int(input('Выбери дверь 21 или 311'))
        if a5==21:
            a6=int(input('Выбери дверь 211 или 311'))
            if a6==211:
                print('Ты попал в паутину')
            elif a6==311:
                print('Ты проиграл обезьяне с гранатой')    
        elif a5==311:
            print('Ты проиграл обезьяне с гранатой')
    elif a3==32:
        print('Ты нашёл супер редкого котэ')
    elif a3==33:
        print('Ты попал в паутину')

'''





