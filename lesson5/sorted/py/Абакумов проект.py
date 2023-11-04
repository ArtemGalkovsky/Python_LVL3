from tkinter import*

def click():
    s=sel.get()
    if s==1:
        c.create_rectangle(300,210,400,300,fill='orange',outline='orange',width=2)
        c.create_rectangle(335,255,365,300,fill='black',outline='black',width=2)
        c.create_polygon(345,110,300,210,400,210,fill='blue',outline='blue',width=2)
    
def click1():
      s=sel.get()
      if s==2:
        c.create_oval(360,5,400,40,fill='yellow',outline='yellow',width=2)
def click2():
        c.create_rectangle(55,225,65,301,fill='#BE8641',outline='#BE8641',width=2)
        c.create_oval(42,150,78,225,fill='green',outline='green',width=2)
        c.create_rectangle(125,225,135,301,fill='#BE8641',outline='#BE8641',width=2)
        c.create_oval(112,150,148,225,fill='green',outline='green',width=2)
                         
def click3():
        c.create_oval(10,5,90,50,fill='white',outline='white',width=2)
        c.create_oval(120,5,200,50,fill='white',outline='white',width=2)
        c.create_oval(230,5,310,50,fill='white',outline='white',width=2)

def click4():
    s=sel.get()
    if s==5:
        c.create_rectangle(0,301,400,400,fill='lightgreen',outline='lightgreen',width=2)


def click5():
    s=sel.get()
    if s==6:
        c.configure(bg='aqua')
def click6():
    s=sel.get()
    if s==6:
        c.configure(bg='aqua')
        c.create_rectangle(300,210,400,300,fill='orange',outline='orange',width=2)
        c.create_rectangle(335,255,365,300,fill='black',outline='black',width=2)
        c.create_polygon(345,110,300,210,400,210,fill='blue',outline='blue',width=2)
        c.create_rectangle(0,301,400,400,fill='lightgreen',outline='lightgreen',width=2)
        c.create_oval(10,5,90,50,fill='white',outline='white',width=2)
        c.create_oval(120,5,200,50,fill='white',outline='white',width=2)
        c.create_oval(230,5,310,50,fill='white',outline='white',width=2)
        c.create_rectangle(55,225,65,301,fill='#BE8641',outline='#BE8641',width=2)
        c.create_oval(42,150,78,225,fill='green',outline='green',width=2)
        c.create_oval(112,150,148,225,fill='green',outline='green',width=2)
        c.create_rectangle(125,225,135,301,fill='#BE8641',outline='#BE8641',width=2)
        c.create_oval(360,5,400,40,fill='yellow',outline='yellow',width=2)

def click7():
        s=sel.get()
        c.configure(bg='grey')
        c.create_rectangle(300,210,400,300,fill='orange',outline='orange',width=2)
        c.create_rectangle(335,255,365,300,fill='black',outline='black',width=2)
        c.create_polygon(345,110,300,210,400,210,fill='blue',outline='blue',width=2)
        c.create_oval(10,5,90,50,fill='grey',outline='black',width=2)
        c.create_oval(120,5,200,50,fill='grey',outline='black',width=2)
        c.create_oval(230,5,310,50,fill='grey',outline='black',width=2)
        c.create_rectangle(0,301,400,400,fill='darkgreen',outline='darkgreen',width=2)
        c.create_rectangle(55,225,65,301,fill='#BE8641',outline='#BE8641',width=2)
        c.create_oval(42,150,78,225,fill='yellow',outline='yellow',width=2)
        c.create_rectangle(125,225,135,301,fill='#BE8641',outline='#BE8641',width=2)
        c.create_oval(112,150,148,225,fill='orange',outline='orange',width=2)
        c.create_oval(360,5,400,40,fill='grey',outline='grey',width=2)



def click8():
    s=sel.get()       
    c.configure(bg='aqua')   
    c.create_rectangle(300,210,400,300,fill='orange',outline='orange',width=2)
    c.create_rectangle(335,255,365,300,fill='black',outline='black',width=2)
    c.create_polygon(345,110,300,210,400,210,fill='white',outline='white',width=2)
    c.create_rectangle(0,301,400,400,fill='white',outline='white',width=2)
    c.create_oval(10,5,90,50,fill='white',outline='white',width=2)
    c.create_oval(120,5,200,50,fill='white',outline='white',width=2)
    c.create_oval(230,5,310,50,fill='white',outline='white',width=2)
    c.create_rectangle(55,225,65,301,fill='#BE8641',outline='#BE8641',width=2)
    c.create_oval(42,150,78,225,fill='aqua',outline='aqua',width=2)
    c.create_rectangle(125,225,135,301,fill='#BE8641',outline='#BE8641',width=2)
    c.create_oval(112,150,148,225,fill='aqua',outline='aqua',width=2)
    c.create_oval(360,5,400,40,fill='yellow',outline='yellow',width=2)



def click9():
    s=sel.get()
    if s==6:
        c.configure(bg='aqua')
        c.create_rectangle(300,210,400,300,fill='orange',outline='orange',width=2)
        c.create_rectangle(335,255,365,300,fill='black',outline='black',width=2)
        c.create_polygon(345,110,300,210,400,210,fill='blue',outline='blue',width=2)
        c.create_rectangle(0,301,400,400,fill='#BE8641',outline='#BE8641',width=2)
        c.create_oval(10,5,90,50,fill='white',outline='white',width=2)
        c.create_oval(120,5,200,50,fill='white',outline='white',width=2)
        c.create_oval(230,5,310,50,fill='white',outline='white',width=2)
        c.create_rectangle(55,225,65,301,fill='#BE8641',outline='#BE8641',width=2)
        c.create_rectangle(125,225,135,301,fill='#BE8641',outline='#BE8641',width=2)
        c.create_oval(42,150,78,225,fill='aqua',outline='aqua',width=2)
        c.create_oval(112,150,148,225,fill='aqua',outline='aqua',width=2)
        c.create_oval(360,5,400,40,fill='yellow',outline='yellow',width=2)














window=Tk()
window.title('Составь свой мир')
window.geometry('900x900')
c=Canvas(window,width= 400,height=400,bg='white')
c.place(x=400,y=200)
sel=IntVar()
lab=Label(window,text='Выбери пору года,и то что должно быть на рисунке',font='Arial,10').grid(column=0,row=0)
rad1=Radiobutton(window,text='Дом',value=1,variable=sel,command=click)
rad2=Radiobutton(window,text='Солнце',value=2,variable=sel,command=click1)
rad3=Radiobutton(window,text='Дерево',value=3,variable=sel,command=click2)
rad4=Radiobutton(window,text='Облака',value=4,variable=sel,command=click3)
rad5=Radiobutton(window,text='Трава',value=5,variable=sel,command=click4)
rad6=Radiobutton(window,text='Небо',value=6,variable=sel,command=click5)
bt1=Button(window, text = 'Лето',command=click6,font='Arial 30')
bt2=Button(window, text = 'Осень',command=click7,font='Arial 30')
bt3=Button(window, text = 'Зима',command=click8,font='Arial 30')
bt4=Button(window, text = 'Весна',command=click9,font='Arial 30')
rad1.place(x=820, y=220)
rad2.place(x=820, y=240)
rad3.place(x=820, y=260)
rad4.place(x=820, y=280)
rad5.place(x=820, y=300)
rad6.place(x=820, y=320)
bt1.place(x=0, y=220)
bt2.place(x=0, y=295)
bt3.place(x=0, y=370)
bt4.place(x=0, y=450)



