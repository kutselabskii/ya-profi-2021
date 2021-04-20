# coding=utf-8

import json
from tkinter import *
from tkinter.ttk import *


class DeviceView(Frame):
    def __init__(self, master, width, height):
        self.master = master

        super().__init__(self.master, width=width, height=height)

        self.pack()

    def Initialize(self):
        pass

    def Update(self, data):
        pass


class AirPollutionView(DeviceView):
    def __init__(self, master=None):
        super().__init__(master, 300, 300)

        self.title = Label(self, text="Состояние воздуха")
        self.title.grid(row=0, column=0, columnspan=4)

        row = 1
        column = 0
        self.humidity = MakeVariable(self, "Влажность", row, 0, row, 1)
        self.oxygen = MakeVariable(self, "Кислород", row, 2, row, 3)
        row += 1
        self.carbon = MakeVariable(self, "Углекислый газ", row, 0, row, 1)
        self.nitric = MakeVariable(self, "Оксид азота", row, 2, row, 3)
        row += 1
        self.sulfurous = MakeVariable(self, "Сернистый ангидрид", row, 0, row, 1)
        self.hydrogen_sulfide = MakeVariable(self, "Сероводород", row, 2, row, 3)
        row += 1
        self.methane = MakeVariable(self, "Метан", row, 0, row, 1)
        self.dust = MakeVariable(self, "Угольная пыль", row, 2, row, 3)

    def Initialize(self):
        super().Initialize()

    def Update(self, data):
        self.humidity.set(data["environment"]["humidity"])
        self.oxygen.set(data["environment"]["oxygen"])
        self.carbon.set(data["environment"]["carbon"])
        self.nitric.set(RoundFloatStr(data["environment"]["nitric"], 5))
        self.sulfurous.set(RoundFloatStr(data["environment"]["sulfurous"], 5))
        self.hydrogen_sulfide.set(RoundFloatStr(data["environment"]["hydrogen_sulfide"], 5))
        self.methane.set(RoundFloatStr(data["environment"]["methane"], 3))
        self.dust.set(RoundFloatStr(data["environment"]["dust"], 3))


def MakeVariable(
        root,
        title,
        title_row, title_column,
        label_row, label_column,
        title_rowspan=1, title_columnspan=1,
        label_rowspan=1, label_columnspan=1):

    title = Label(root, text=f"{title}:")
    title.grid(row=title_row, column=title_column, rowspan=title_rowspan, columnspan=title_columnspan)

    variable = StringVar()
    label = Label(root, textvariable=variable)
    label.grid(row=label_row, column=label_column, rowspan=label_rowspan, columnspan=label_columnspan)

    return variable


def RoundFloatStr(s, digits):
    return str(round(float(s), digits))
