# coding=utf-8

from tkinter import *
from tkinter.ttk import *


class DeviceView(Frame):
    def __init__(self, device, master, width, height):
        self.master = master
        self.device = device

        super().__init__(self.master, width=width, height=height)

        self.pack()

    def Render(self):
        pass


class AirPollutionView(DeviceView):
    def __init__(self, device, master=None):
        super().__init__(device, master, 300, 300)

        self.title = Label(self, text="Состояние воздуха")
        self.title.grid(row=0, column=0, columnspan=4)

        self.humidity = MakeVariable(self, "Влажность", 1, 0, 1, 1, 1, 1, 1, 1)

    def Render(self):
        super().Render()

        self.humidity.set(str(self.device.humidity))


def MakeVariable(
        root,
        title, title_row, title_column, title_rowspan, title_columnspan,
        label_row, label_column, label_rowspan, label_columnspan):

    title = Label(root, text=f"{title}:")
    title.grid(row=title_row, column=title_column, rowspan=title_rowspan, columnspan=title_columnspan)

    variable = StringVar()
    label = Label(root, textvariable=variable)
    label.grid(row=label_row, column=label_column, rowspan=label_rowspan, columnspan=label_columnspan)

    return variable
