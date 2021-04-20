# coding=utf-8

import requests
from tkinter import *
from tkinter.ttk import *
import Common.secrets as sec

API_LINK = "https://sandbox.rightech.io/api/v1"


class DeviceView(Frame):
    def __init__(self, master, width, height, objectId=""):
        self.master = master
        self.objectId = objectId

        super().__init__(self.master, width=width, height=height)

    def Initialize(self):
        pass

    def Update(self, data):
        pass


class AirPollutionView(DeviceView):
    def Initialize(self):
        self.title = Label(self, text="Состояние воздуха")
        self.title.grid(row=0, column=0, columnspan=4)

        row = 1
        self.humidity = MakeVariable(self, "Влажность", row, 0, row, 1, variable_type=IntVar)
        self.oxygen = MakeVariable(self, "Кислород", row, 2, row, 3, variable_type=IntVar)
        row += 1
        self.carbon = MakeVariable(self, "Углекислый газ", row, 0, row, 1, variable_type=IntVar)
        self.nitric = MakeVariable(self, "Оксид азота", row, 2, row, 3, variable_type=DoubleVar)
        row += 1
        self.sulfurous = MakeVariable(self, "Сернистый ангидрид", row, 0, row, 1, variable_type=DoubleVar)
        self.hydrogen_sulfide = MakeVariable(self, "Сероводород", row, 2, row, 3, variable_type=DoubleVar)
        row += 1
        self.methane = MakeVariable(self, "Метан", row, 0, row, 1, variable_type=DoubleVar)
        self.dust = MakeVariable(self, "Угольная пыль", row, 2, row, 3, variable_type=DoubleVar)

    def Update(self, data):
        self.humidity.set(data["environment"]["humidity"])
        self.oxygen.set(data["environment"]["oxygen"])
        self.carbon.set(data["environment"]["carbon"])
        self.nitric.set(RoundFloat(data["environment"]["nitric"], 5))
        self.sulfurous.set(RoundFloat(data["environment"]["sulfurous"], 5))
        self.hydrogen_sulfide.set(RoundFloat(data["environment"]["hydrogen_sulfide"], 5))
        self.methane.set(RoundFloat(data["environment"]["methane"], 3))
        self.dust.set(RoundFloat(data["environment"]["dust"], 3))


class CostumeParamsView(DeviceView):
    def Initialize(self):
        self.title = Label(self, text="Параметры костюма")
        self.title.grid(row=0, column=0, columnspan=4)

        row = 1
        self.active = MakeVariable(self, "Включен", row, 0, row, 1, variable_type=BooleanVar)
        self.time_left = MakeVariable(self, "Осталось времени", row, 2, row, 3, variable_type=IntVar)
        row += 1
        button = Button(self, text="Переключить костюм", command=self.ToggleActive)
        button.grid(row=row, column=0, columnspan=4)

    def ToggleActive(self):
        isActive = self.active.get()
        RunCommand(self.objectId, "deactivate" if isActive else "activate")

    def Update(self, data):
        self.active.set(data["active"])
        self.time_left.set(data["time_left"])


class CoordinatesView(DeviceView):
    def Initialize(self):
        self.title = Label(self, text="Координаты")
        self.title.grid(row=0, column=0, columnspan=6)

        row = 1
        self.x = MakeVariable(self, "X", row, 0, row, 1, variable_type=IntVar)
        self.y = MakeVariable(self, "Y", row, 2, row, 3, variable_type=IntVar)
        self.z = MakeVariable(self, "Z", row, 4, row, 5, variable_type=IntVar)
        row += 1
        # self.distance = MakeVariable(self, "Расстояния до маячков", row, 0, row, 1, label_columnspan=5)

    def Update(self, data):
        self.x.set(data["coords"]["x"])
        self.y.set(data["coords"]["y"])
        self.z.set(data["coords"]["z"])

        # TODO Somehow fields doesn't come in dicts
        # s = ""
        # ddist = data["distance"]
        # for d in ddist.keys():
        #     s += f"{d}: {ddist[d]}, "
        # self.distance.set(s[:-2])


def MakeVariable(
        root,
        title,
        title_row, title_column,
        label_row, label_column,
        title_rowspan=1, title_columnspan=1,
        label_rowspan=1, label_columnspan=1,
        variable_type=StringVar):

    title = Label(root, text=f"{title}:")
    title.grid(row=title_row, column=title_column, rowspan=title_rowspan, columnspan=title_columnspan)

    variable = variable_type()
    label = Label(root, textvariable=variable)
    label.grid(row=label_row, column=label_column, rowspan=label_rowspan, columnspan=label_columnspan)

    return variable


def RoundFloat(s, digits):
    return round(float(s), digits)


def RunCommand(id, command):
    headers = {"Authorization": f"Bearer {sec.API_TOKEN}"}
    requests.post(f"{API_LINK}/objects/{id}/commands/{command}", headers=headers)
