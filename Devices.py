from time import time
import json
import Common.Emulation as emu


class Device:
    def __init__(
        self, client, clockInterval=1, *, emulation=False
    ):
        self.client = client
        self.emulation = emulation
        self.clockInterval = clockInterval
        self.needPublish = False

        self.Initialize()

    def Initialize(self):
        self.clock = time()

    def Update(self):
        t = time()
        if t - self.clock > self.clockInterval:
            self.clock = t
            return True
        return False

    def Publish(self):
        pass


class AirPollutionSensor(Device):
    def __init__(
        self, client, clockInterval=1, *, emulation=False
    ):
        super().__init__(client, clockInterval, emulation=emulation)

    def Initialize(self):
        super().Initialize()

        self.humidity = 0
        self.oxygen = 0
        self.carbon = 0
        self.nitric = 0
        self.sulfurous = 0
        self.hydrogen_sulfide = 0
        self.methane = 0
        self.dust = 0

    def Update(self):
        if not super().Update():
            return

        if self.emulation:
            self.humidity = emu.GetInt(40, 85)
            self.oxygen = emu.GetInt(15, 40)
            self.carbon = emu.GetInt(5, 15)
            self.nitric = emu.GetFloat(10 ** -5, 1)
            self.sulfurous = emu.GetFloat(10 ** -5, 10 ** -4)
            self.hydrogen_sulfide = emu.GetFloat(10 ** -5, 10 ** -4)
            self.methane = emu.GetFloat(0.5, 2)
            self.dust = emu.GetFloat(0.5, 5)

            self.needPublish = True

    def Publish(self):
        if not self.needPublish:
            return

        super().Publish()

        self.needPublish = False

        self.client.publish("environment", json.dumps(
                {
                    "humidity": self.humidity,
                    "oxygen": self.oxygen,
                    "carbon": self.carbon,
                    "nitric": self.nitric,
                    "sulfurous": self.sulfurous,
                    "hydrogen_sulfide": self.hydrogen_sulfide,
                    "methane": self.methane,
                    "dust": self.dust,
                }
            )
        )

# class 