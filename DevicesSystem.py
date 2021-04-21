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
        self.objects.append(Helicopter(sec.HelicopterClientId))
        self.objects.append(Mine(sec.MineClientId))

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


class Helicopter(DeviceObject):
    def CreateDevices(self):
        self.devices.append(Devices.Buzzer(self.client, 5))
        self.devices.append(Devices.FuelSensor(self.client, 6, emulation=True))
        self.devices.append(Devices.GPS(self.client, 10, emulation=True))


class Mine(DeviceObject):
    def CreateDevices(self):
        self.devices.append(Devices.Buzzer(self.client, 7))
        self.devices.append(Devices.Ventilation(self.client, 9))
        self.devices.append(Devices.Power(self.client, 20))
        self.devices.append(Devices.NoiseSensor(self.client, 12, emulation=True))
        for i in range(2):
            self.devices.append(Devices.Thermometer(self.client, i, 15, emulation=True))
        for i in range(4):
            self.devices.append(Devices.MovementSensor(self.client, i, 10, emulation=True))
