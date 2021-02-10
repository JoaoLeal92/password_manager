from tkinter import *


class PasswordPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # Header container
        self.header_container = Frame(master)
        self.header_container.pack()
        self.header_container['pady'] = 10
        # Header Text
        self.header = Label(self.header_container, text='Pagina das senhas')
        self.header.pack()
