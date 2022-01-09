from tkinter import *
import tkinter as tk
from tkinter import ttk
from log_possibiliste_qualitative import main


st=main("possibility/test.txt", "7 0") 
print(st)
l=len(st)  
     
canvas = Canvas(width=500, height=800, bg='white')
canvas.pack(expand=YES, fill=BOTH)                
     

canvas.create_rectangle(100, 10, 400, 700, width=3, fill='white')

h1=700/l
a=10+h1
h2=h1/2
b=10+h2

for i in range(l):

    canvas.create_line(100, a, 400, a, width=2)
    txt=str(st[i])
    txt=txt.replace("formule  seuil", "")
    txt=txt.replace("\n", "       ")
    widget = Label(canvas, text=txt, fg='black', bg='white')
    widget.pack()
    canvas.create_window(250, b, window=widget)
    a=a+h1
    b=b+h1


 
mainloop()