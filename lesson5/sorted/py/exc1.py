import xlwt, xlrd

# Создаем книку
book = xlwt.Workbook()
font1 = xlwt.easyxf('font:height 222,name Calibri, colour_index green')
st = xlwt.easyxf('pattern: pattern solid;')
st.pattern.pattern_fore_colour = 5

sheet = book.add_sheet('игра1')
sheet.write(0,0,'Имя', st)
sheet.write(0,1,input())
sheet.write(0,2,'Втр')
sheet.write(0,3,'Среда', font1)


sheet.write(1, 1, 126 ) 
sheet.write(2, 1, 23) 
sheet.write (3, 1, 1 ) 
sheet.write (4, 1, 1 ) 
''' for i in range(1,5):
         sheet.write (i, 1, randint(0,100))'''

sheet.row(1).height = 2500

sheet.col(0).width = 20000
sheet.write (5, 1, xlwt.Formula('A1+A2+A3'))
sheet.write (5, 1, xlwt.Formula('sum(A1:A3)'))
book.save('day2.xls')

rb = xlrd.open_workbook('day1.xls')#,formatting_info=True)
#выбираем активный лист
sheet = rb.sheet_by_index(0)
#получаем значение первой ячейки A1
val = sheet.row_values(0)[0]
print(val)

