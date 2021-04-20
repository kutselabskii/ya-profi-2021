import paho.mqtt.client as mqtt
import Devices
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
        self.devices.append(Devices.AirPollutionSensor(self.client, 7, emulation=True))
        self.devices.append(Devices.CostumeParams(self.client, 9, emulation=True))
        self.devices.append(Devices.Coords(self.client, 11, emulation=True))
        self.devices.append(Devices.Beacon(self.client, 12, emulation=True))
