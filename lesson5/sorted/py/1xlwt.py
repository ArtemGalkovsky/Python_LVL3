import xlwt
import xlrd
from random import randint

# Создаем книку
bk = xlwt.Workbook()
sheet = bk.add_sheet('день1')

sheet.write(0,0,'Имя')
sheet.write(0,1,'Понедельник')
sheet.write(0,2,'Вторник')
sheet.write(0,3,'среда')
sheet.write(0,4,'четверг')
sheet.write(0,5,'пятница')
sheet.write(0,6,'субота')
sheet.write(0,7,'воскресенье')
for q in range (1,8):
   sheet.write(q,0,input('Введите Имя'))


'''for q in range (5):
    
    a=randint(1,10)
    sheet.write(q,1,a)
for q in range (5):
    
    a=randint(1,10)
    sheet.write(q,2,a)
for q in range (5):
   
    a=randint(1,10)
    sheet.write(q,3,a)
#a=1
for q in range (5):
#    a+=1
    q+=1
    a=randint(1,10)
    sheet.write(q,4,a)
for q in range (5):
   
    a=randint(1,10)
    sheet.write(q,5,a)
for q in range (5):
    
    a=randint(1,10)
    sheet.write(q,6,a)
for q in range (5):
    q+=1
    a=randint(1,10)
    sheet.write(q,7,a)
for q in range (5):
    q+=1
    a=randint(1,10)
    sheet.write(q,8,a)

#    sheet.write(q,4,xlwt.Formula(f"($B{a} + $C{a} + $D{a})/3"))
#a=xlwt.Formula(f"")
#print (a)

# Высота строки
sheet.row(1).height = 2500
# Ширина колонки
sheet.col(0).width = 2000'''
bk.save('day1.xls')
