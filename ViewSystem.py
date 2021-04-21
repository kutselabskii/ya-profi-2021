import requests
from time import time
from tkinter import *
from tkinter.ttk import *
import Views
import Common.secrets as sec

API_LINK = "https://sandbox.rightech.io/api/v1"


class System:
    def __init__(self):
        self.closed = False
        self.objects = []

        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.OnClose)
        self.root.geometry("1024x768")
        self.root.title("Интерфейс оператора")

    def Initialize(self):
        self.CreateObjects()

        for object in self.objects:
            object.Initialize()

    def CreateObjects(self):
        # self.objects.append(Costume(sec.CostumeApiId, self.root))
        # self.objects.append(Helicopter(sec.HelicopterApiId, self.root))
        self.objects.append(Mine(sec.MineApiId, self.root))

    def LoopForever(self):
        while True:
            if self.closed:
                break
            self.Update()

    def Update(self):
        self.root.update()

        for object in self.objects:
            object.Update()

    def OnClose(self):
        self.closed = True


class ViewObject(Frame):
    def __init__(self, objectId, root):
        self.objectId = objectId
        self.root = root

        super().__init__(self.root)

        self.views = []
        self.update_interval = 5
        self.last_update = 0

        self.pack()

    def Initialize(self):
        self.CreateViews()

        for view in self.views:
            view.Initialize()

    def CreateViews(self):
        pass

    def Update(self):
        t = time()

        if t - self.last_update > self.update_interval:
            headers = {"Authorization": f"Bearer {sec.API_TOKEN}"}
            unixBegin = round((t - 1800) * 1000)
            unixEnd = round(t * 1000)
            answer = requests.get(f"{API_LINK}/objects/{self.objectId}/packets?from={unixBegin}&to={unixEnd}", headers=headers)
            data = answer.json()
            if len(data) > 0:
                data = data[-1]
                for view in self.views:
                    view.Update(data)

            self.last_update = t


class Costume(ViewObject):
    def CreateViews(self):
        self.update_interval = 5

        self.airPollution = Views.AirPollutionView(self, 300, 300, objectId=sec.CostumeApiId)
        self.airPollution.grid(row=0, column=0)
        self.views.append(self.airPollution)

        self.costumeParams = Views.CostumeParamsView(self, 300, 150, objectId=sec.CostumeApiId)
        self.costumeParams.grid(row=0, column=1)
        self.views.append(self.costumeParams)

        self.coordinatesView = Views.CoordinatesView(self, 300, 100, objectId=sec.CostumeApiId)
        self.coordinatesView.grid(row=1, column=0)
        self.views.append(self.coordinatesView)

        self.beacon = Views.BeaconView(self, 300, 200, objectId=sec.CostumeApiId)
        self.beacon.grid(row=1, column=1)
        self.views.append(self.beacon)


class Helicopter(ViewObject):
    def CreateViews(self):
        self.update_interval = 10

        self.gps = Views.GPS(self, 300, 150, objectId=self.objectId)
        self.gps.grid(row=0, column=0)
        self.views.append(self.gps)

        self.fuel = Views.FuelView(self, 300, 150, objectId=self.objectId)
        self.fuel.grid(row=0, column=1)
        self.views.append(self.fuel)

        self.buzzer = Views.BuzzerView(self, 300, 150, objectId=self.objectId)
        self.buzzer.grid(row=1, column=0)
        self.views.append(self.buzzer)


class Mine(ViewObject):
    def CreateViews(self):
        self.update_interval = 10

        self.power = Views.PowerView(self, 150, 150, objectId=self.objectId)
        self.power.grid(row=0, column=0)
        self.views.append(self.power)

        self.buzzer = Views.BuzzerView(self, 300, 150, objectId=self.objectId)
        self.buzzer.grid(row=0, column=1)
        self.views.append(self.buzzer)

        self.ventilation = Views.VentilationView(self, 300, 150, objectId=self.objectId)
        self.ventilation.grid(row=0, column=2)
        self.views.append(self.ventilation)

        for i in range(2):
            temp = Views.ThermometerView(self, i, 300, 150, objectId=self.objectId)
            temp.grid(row=1, column=i)
            self.views.append(temp)

        for i in range(4):
            move = Views.MovementView(self, i, 300, 150, objectId=self.objectId)
            move.grid(row=2, column=i)
            self.views.append(move)
