from tkinter import *
import tkinter.font


class GUI:
    def __init__(self, home):
        self.myHome = home
        self.state = home.get_lookout()
        self.light = home.get_light()
        print("new GUI object")

    def config(self):
        self.win = Tk()
        self.win.title("SmartHome UdeA")
        for x in range(3):
            Grid.rowconfigure(self.win, x, weight=1)
            Grid.columnconfigure(self.win, x, weight=1)
        self.myFont = tkinter.font.Font(family='Helvetica', size=12, weight="bold")
        self.win.attributes('-fullscreen', True)
        self.win.bind('<Escape>', lambda e: self.exit())
        self.panel = Label(self.win, text='SmartHome UdeA', font=self.myFont, anchor="center")
        self.panel.grid(row=0, columnspan=3, sticky=N+S+E+W)
        self.lightButton = Button(self.win, text='On/Off', font=self.myFont, command=self.toggle_light,
                                  bg='ghost white', borderwidth=1)
        self.lightButton.grid(row=1, column=0, sticky=N+S+E+W)

        self.lookoutButton = Button(self.win, text='Vigía', font=self.myFont, command=self.lookout,
                                    bg='ghost white', borderwidth=1)
        self.lookoutButton.grid(row=1, column=1, sticky=N+S+E+W)
        self.exitButton = Button(self.win, text='Exit', font=self.myFont, command=self.exit,
                                 bg='ghost white', borderwidth=1)
        self.exitButton.grid(row=1, column=2, sticky=N+S+E+W)

    def lookout(self):
        self.state = self.myHome.toggle_lookout()
        if self.state:
            self.lookoutButton.configure(bg='red')
        else:
            self.lookoutButton.configure(bg='ghost white')

    def toggle_light(self):
        self.light = self.myHome.toggle_light()
        if self.light:
            self.lightButton.configure(bg='yellow')
        else:
            self.lightButton.configure(bg='ghost white')

    def exit(self):
        self.win.destroy()
        self.myHome.end_program()

    def start(self):
        self.config()
        mainloop()
