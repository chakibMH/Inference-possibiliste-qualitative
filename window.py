from tkinter import *
import tkinter as tk
from tkinter import ttk
from log_possibiliste_qualitative import main,first_step,get_st,inf_qualitative
 
     
canvas = Canvas(width=900, height=610, bg='#95B2FF')
canvas.pack(expand=YES, fill=BOTH)                
     



def btn_clicked():
    input = text2.get("1.0",'end-1c')
    first_step(input)
    var_interet=text3.get("1.0",'end-1c')
    st,st_affich = get_st()
    val = inf_qualitative(st, var_interet)
    text4.insert(1.0,val )
    l=len(st_affich)

    canvas.create_rectangle(100, 10, 400, 600, width=3, fill='white')

    h1=600/l
    a=10+h1
    h2=h1/2
    b=10+h2
    for i in range(l):

        canvas.create_line(100, a, 400, a, width=2)
        txt=str(st_affich[i])
        txt=txt.replace("formule  seuil", "")
        txt=txt.replace("\n", "       ")
        widget = Label(canvas, text=txt, fg='black', bg='white')
        widget.pack()
        canvas.create_window(250, b, window=widget)
        a=a+h1
        b=b+h1

canvas.create_text(650, 45, text="La base ponderee :", fill="black")
canvas.pack()

text2 = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,width =25,height = 10)


canvas.create_window(700, 140, window=text2)

#*********************but******************

canvas.create_text(620, 250, text="Le but :", fill="black")
canvas.pack()

text3 = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,width =25,height = 5)


canvas.create_window(700, 310, window=text3)

#*********************button******************
b0 = Button(
    bd = '5',
    command = btn_clicked,
    relief = "flat",text = 'Exécuter')

canvas.create_window(500, 250, window=b0)
 
#*********************le resultat******************

canvas.create_text(450, 430, text="Resultat :", fill="black")
canvas.pack()

text4 = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,width =35,height = 10)


canvas.create_window(650,500, window=text4)

mainloop()



