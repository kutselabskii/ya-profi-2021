import tkinter as tk


class System:
    def __init__(self):
        self.closed = False

        self.view = tk.Tk()
        self.protocol("WM_DELETE_WINDOW", self.OnClose)

    def LoopForever(self):
        while True:
            self.Update()

    def Update(self):
        pass

    def OnClose(self):
        self.closed = True
