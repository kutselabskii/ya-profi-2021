import paho.mqtt.client as mqtt
from Devices import AirPollutionSensor
import Common.secrets as sec


class System:
    def __init__(self):
        self.objects = []

    def Initialize(self):
        self.CreateObjects()

        for object in self.objects:
            object.Initialize()

    def CreateObjects(self):
        self.objects.append(Costume(sec.CostumeClientId))

    def LoopForever(self):
        while True:
            self.Update()

    def Update(self):
        for object in self.objects:
            object.Update()


class DeviceObject:
    def __init__(self, clientId):
        self.devices = []
        self.clientId = clientId

    def Initialize(self):
        self.client = mqtt.Client(self.clientId)
        self.client.connect("sandbox.rightech.io")
        self.client.loop_start()

        self.CreateDevices()

    def CreateDevices(self):
        pass

        for device in self.devices:
            device.Initialize()

    def Update(self):
        for device in self.devices:
            device.Update()
            device.Publish()


class Costume(DeviceObject):
    def CreateDevices(self):
        self.devices.append(AirPollutionSensor(self.client, 5, emulation=True))
