from tkinter import *
root = Tk() 
c = Canvas(root, width=550, height=400, bg='white') 
c.pack()
y=210
y1=290
def kr():
   
    c.create_polygon(375, 100 ,200 ,200 ,550 ,200, fill='purple')
    

c.create_rectangle(80, 380, 120, 400, fill='brown')

for i in range(3):
    c.create_polygon(100, y, 20, y1, 180, y1, fill='green')
    y=y+50
    y1=y1+50

kr1=c.create_rectangle(430 ,60, 470, 260, fill='red')
c.create_rectangle(250, 200, 500, 400, fill='red')
c.create_polygon(375, 100 ,200 ,200 ,550 ,200, fill='red')
c.create_rectangle(300, 270, 350, 220, fill='yellow')
c.create_rectangle(400, 270, 450, 220, fill='yellow')
c.create_rectangle(400, 300, 475, 400, fill='brown')

c.create_oval(10, 10, 150, 150, fill='yellow')
#c.bind('<t>', lambda:kr)
c.bind('<UP>', kr)





root.mainloop()
