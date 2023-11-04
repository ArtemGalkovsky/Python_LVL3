'''a= int(input())
b= int(input())
for i in range(a,b,1):
    print(i)
a1= int(input())
b1= int(input())
for q in range(b1,a1,-1):
    print(q)
child=0
for c in range (2019,2023,1):
    print(c, child)
    child=child+1
s= input("Введите строку:")
s1=""
for c in s:
  if c=="а":
    c="б"
  s1=s1+c
print(s1)
'''
'''
s= input("Введите строку:")
s2=''
for i in s:
 if i=="м":
     i="!м!"
 s2=s2+i
print(s2)
for i in s2:
    print(i)
'''

s= input("Введите строку:")
for i in s:
    print("----"+i+"======")
