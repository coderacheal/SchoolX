from tkinter import *
import pyttsx3



master_window = Tk()
master_window.title('Text to speech')
master_window.geometry('600x300')
master_window.configure(bg='pink')

msg = StringVar()
the_label = Label(master_window, text='TEXT TO SPEECH APP', font='Calibri 20 bold', background='pink').pack()
entry_field = Entry(master_window, textvariable=msg, width=40, font=15).place(x=120, y=80)
the_label = Label(master_window, font='Calibri 20 bold', background='pink').pack()

def play():
    text_to_speech = pyttsx3.init()
    my_text = msg.get()
    text_to_speech.say(my_text)
    text_to_speech.runAndWait()

def reset():
    msg.set('')

def close():
    master_window.destroy()



my_button=Button(master_window, text='Play', command=play).place(y=130, x=200)
my_button = Button(master_window, text='Reset', command=reset).place(y=130, x=260)
my_button = Button(master_window, text='Close', command=close, background='#2596be').place(y=130, x=320)


master_window.mainloop()