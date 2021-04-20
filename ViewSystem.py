import requests
from time import time
import tkinter as tk
from Views import AirPollutionView
import Common.secrets as sec

API_LINK = "https://sandbox.rightech.io/api/v1"


class System:
    def __init__(self):
        self.closed = False
        self.objects = []

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.OnClose)
        self.root.geometry("1024x768")
        self.root.title("Интерфейс оператора")

    def Initialize(self):
        self.CreateObjects()

        for object in self.objects:
            object.Initialize()

    def CreateObjects(self):
        self.objects.append(Costume(sec.CostumeApiId, self.root))

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


class ViewObject:
    def __init__(self, objectId, root):
        self.objectId = objectId
        self.root = root

        self.views = []
        self.update_interval = 2
        self.last_update = 0

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
            answer = requests.get(f"{API_LINK}/objects/{self.objectId}/packets?ofType=processed&nolimit=true&streamed=true&from={unixBegin}&to={unixEnd}", headers=headers)
            data = answer.json()
            if len(data) > 0:
                data = data[-1]
                for view in self.views:
                    view.Update(data)

            self.last_update = t


class Costume(ViewObject):
    def CreateViews(self):
        self.views.append(AirPollutionView(self.root))
