from tkinter import *
import os
import sys

py = sys.executable

#window

root = Tk()
# root.geometry('600x800')
root.title('Racing Game')
root.config(bg = '#CBD18F')

root.geometry('700x800')

def comp():
    root.destroy()
    os.system('%s %s' % (py, 'quiz.py'))

def solo():
    root.destroy()
    os.system('%s %s' % (py, 'game.py'))

    

button1 = Button(root, text = 'Versus Computer', command = comp)

button2= Button(root, text = 'Time trial', command=solo)

button1.pack(pady = 20)
button2.pack(pady= 20)


root.mainloop()