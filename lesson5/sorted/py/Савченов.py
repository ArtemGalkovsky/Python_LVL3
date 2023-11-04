from tkinter import*
import time
def dd():
    c.move(solnce, 10,3)
    root.after(10, dd)
    
def ff():
    c.move(luna, 20,12)
    root.after(100, ff)
    
def bb():
    c.move(luna, 55, -15)
    if c.coords(luna)[2] < 400:
        c.after(100, bb)

def vv():
    c.move(solnce, 55, -15 )
    if c.coords(luna)[2] < 400: 
        root.after(100, vv)
    
         
def svet():   
    c.delete(okno1)
    c.delete(okno2)
    c.create_oval(650, 600, 700, 460, fill='#CCCC33', outline='black', width=3)
    c.create_oval(480, 300, 520, 250, fill='#CCCC33', outline='black', width=3)
    
def svet2():
   c.delete(okno1)
   c.delete(okno2)
   c.create_oval(650, 600, 700, 460, fill='blue')
   c.create_oval(480, 300, 520, 250, fill='blue')
   
def noch():
    global solnce, luna
    dd()
    c.config(bg='#003366')
    
    luna = c.create_oval(0, 90, 90 , 180, fill='grey', width=1)
    time.sleep(1)
    bb()

    
def den():
    global solnce, luna
    c.config(bg='#3399FF')
    ff()
    solnce = c.create_oval(0, 90, 90 , 180, fill='yellow', width=1)
    time.sleep(1)
    vv()
    

root = Tk()
root.geometry('800x800')
c = Canvas(root, width=800, height=800, bg='#3399FF')
c.place(x=5, y=5)
c.create_rectangle(0, 650, 800, 800, fill='#00FF33', outline='black', width=0)
c.create_rectangle(400, 650, 600, 350, fill='#663300', outline='black', width=0)
c.create_polygon(400, 350, 600, 350, 500, 200, fill='red', outline='black', width=0)
c.create_rectangle(460, 650, 540, 450, fill='black', outline='black', width=0)
okno2=c.create_oval(480, 300, 520, 250, fill='blue', outline='black', width=3)
c.create_rectangle(200, 650, 230, 500, fill='brown', outline='black', width=0)
c.create_polygon(110, 500, 320, 500, 215, 420, fill='green', width=0)
c.create_polygon(110, 450, 320, 450, 215, 350, fill='green', width=0)
c.create_polygon(110, 400, 320, 400, 215, 220, fill='green', width=0)
c.create_polygon(110, 350, 320, 350, 215, 180, fill='green', width=0)
c.create_text(50, 100, text="Свет", fill='black', font='Dubai 13 "bold"')
c.create_text(50, 250, text="Время", fill='black', font='Dubai 13 "bold"')
c.create_text(700, 750, text="Кирюшка", fill='white', font='Dubai 14 "bold"')
solnce=c.create_oval(350, 90, 450, 0, fill='yellow', width=0)
c.create_rectangle(600, 650, 750, 400, fill='#663300', outline='black', width=0)
okno1=c.create_oval(650, 600, 700, 460, fill='blue', outline='black', width=3)
c.create_polygon(600, 400, 750, 400, 600, 350, fill='red')
but1=Button(root, text='Включить',width=10,font='Dubai 10', command=svet )
but2=Button(root, text='Выключить',width=10,font='Dubai 10', command=svet2 )
but3=Button(root, text='Ночь',width=10,font='Dubai 10', command=noch )
but4=Button(root, text='День',width=10,font='Dubai 10', command=den )


but1.place(x=10, y=130)
but2.place(x=10, y=180)
but3.place(x=10, y=270)
but4.place(x=10, y=320)



root.mainloop()
