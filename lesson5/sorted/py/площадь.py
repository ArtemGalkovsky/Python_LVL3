"""
a=int(input("Введите основание "))
h=int(input("Введите высоту "))
s=a*h*0.5
print ("площадь равна",s)
print(int(input("Введите основание ")*int(input("Введите высоту"))))

r=int(input("Введите радиус "))
p=3.14
s=(r**2)*p
print ("площадь равна",s)

print(int(input("Введите радиус ")**2)*3,14))

y=int(input("Введите кол-во квартир "))
n=int(input("Введите кол-во квартир в подъезде  "))
d=y//n
print ("кол-во домофонов равно",d)

a=int(input("Введите возраст "))
h=input("Введите имя")
k=h*a
print (k)

print(int(input("Введите возраст ")*input("Введите имя")))
"""
a=int(input("Введите высоту кирпича"))
h=int(input("Введите ширину кирпича"))
b=int(input("Введите длину кирпича"))

a1=int(input("Введите высоту окна"))
h1=int(input("Введите ширину окна"))

if a<=a1 and h<=h1 or b<=a1 and h<=h1:
    print("True")
else:
 print("False")
