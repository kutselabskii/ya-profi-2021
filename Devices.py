from time import time
import json
import Common.Emulation as emu
import Common.base64encoder as b64
import Common.secrets as sec

if sec.Raspberry:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


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
        self.Subscribe()

    def Update(self):
        t = time()
        if t - self.clock > self.clockInterval:
            self.clock = t
            return True
        return False

    def Subscribe(self):
        pass

    def Publish(self):
        if not self.needPublish:
            return

        self.Send()
        self.needPublish = False


class AirPollutionSensor(Device):
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

    def Send(self):
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


class CostumeParams(Device):
    def Initialize(self):
        super().Initialize()

        self.active = False
        self.charge = 100
        self.needPublish = True
        
        self.ledPin = 14
        
        if sec.Raspberry:
            GPIO.setup(self.ledPin, GPIO.OUT)
            GPIO.output(self.ledPin, GPIO.LOW)

    def Subscribe(self):
        self.client.on_message = self.OnMessage
        self.client.subscribe("activation")

    def Update(self):
        if not super().Update():
            return

        if self.emulation:
            if self.active:
                self.charge = emu.ReduceInt(self.charge, 1, 0)

            self.needPublish = True
        
        if sec.Raspberry:
            GPIO.output(self.ledPin, GPIO.HIGH if self.active else GPIO.LOW)

    def Send(self):
        self.client.publish("active", self.active)
        self.client.publish("charge", self.charge)

    def OnMessage(self, client, userdata, message):
        data = json.loads(message.payload.decode('utf-8'))

        self.active = data["activate"]
        self.needPublish = True


class Coords(Device):
    def Initialize(self):
        super().Initialize()

        self.x = 0
        self.y = 0
        self.z = 0

    def Update(self):
        if not super().Update():
            return

        if self.emulation:
            self.x = emu.GetInt(0, 50)
            self.y = emu.GetInt(0, 50)
            self.z = emu.GetInt(-30, -25)

            self.needPublish = True

    def Send(self):
        self.client.publish("coords", json.dumps({
            "x": self.x,
            "y": self.y,
            "z": self.z
        }))


class Beacon(Device):
    def Initialize(self):
        super().Initialize()

        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.time = 0
        self.visible = [False] * 8
        self.rssi = {'98:12': -127, '0a:35': -127, '29:39': -127, 'd3:96': -127, 'f7:41': -127, '01:dd': -127, '08:cd': -127, '0e:60': -127}

    def Update(self):
        if not super().Update():
            return

        if self.emulation:
            self.latitude = emu.GetFloat(68, 69)
            self.longitude = emu.GetFloat(64, 66)
            self.altitude = emu.GetFloat(0.9, 1.75)
            self.time = round(time())
            self.visible = emu.RandomBoolArray(8)

            for i, k in enumerate(self.rssi):
                self.rssi[k] = emu.GetInt(-127, 0) if self.visible[i] else -127

            self.needPublish = True

    def Send(self):
        data = {}
        for k in self.rssi.keys():
            if self.rssi[k] > -127:
                data[k] = self.rssi[k]
        self.client.publish(
            "beacon",
            b64.encode(self.latitude, self.longitude, self.altitude, self.time, data)
        )


class Buzzer(Device):
    def __init__(
        self, client, pin, clockInterval=1, *, emulation=False
    ):
        self.ledPin = pin
        super().__init__(client, clockInterval, emulation=emulation)
    
    def Initialize(self):
        super().Initialize()
        self.buzzer = False
        
        if sec.Raspberry:
            GPIO.setup(self.ledPin, GPIO.OUT)
            GPIO.output(self.ledPin, GPIO.LOW)

    def Subscribe(self):
        self.client.subscribe("buzzer_activation")
        self.client.message_callback_add("buzzer_activation", self.OnMessage)

    def Update(self):
        if not super().Update():
            return
            
        self.needPublish = True
        
        if sec.Raspberry:
            GPIO.output(self.ledPin, GPIO.HIGH if self.buzzer else GPIO.LOW)

    def Send(self):
        self.client.publish("buzzer", self.buzzer)

    def OnMessage(self, client, userdata, message):
        data = json.loads(message.payload.decode('utf-8'))
        self.buzzer = data["activate"]
        if sec.Raspberry:
            GPIO.output(self.ledPin, GPIO.HIGH if self.buzzer else GPIO.LOW)
        self.needPublish = True


class Ventilation(Device):
    def Initialize(self):
        super().Initialize()
        self.ventilation = False
        
        if sec.Raspberry:
            self.ventPin = 18
            GPIO.setup(self.ventPin, GPIO.OUT)
            GPIO.output(self.ventPin, GPIO.LOW)

    def Subscribe(self):
        self.client.subscribe("ventilation_activation")
        self.client.message_callback_add("ventilation_activation", self.OnMessage)

    def Update(self):
        if not super().Update():
            return
        
        self.needPublish = True
            
        if sec.Raspberry:
            GPIO.output(self.ventPin, GPIO.HIGH if self.ventilation else GPIO.LOW)

    def Send(self):
        self.client.publish("ventilation", self.ventilation)

    def OnMessage(self, client, userdata, message):
        data = json.loads(message.payload.decode('utf-8'))

        self.ventilation = data["activate"]
        self.needPublish = True
        if sec.Raspberry:
            GPIO.output(self.ventPin, GPIO.HIGH if self.ventilation else GPIO.LOW)


class FuelSensor(Device):
    def Initialize(self):
        super().Initialize()
        self.adc = 5042

    def Update(self):
        if not super().Update():
            return

        if self.emulation:
            self.adc = emu.ReduceInt(self.adc, 11, 0)
            self.needPublish = True

    def Send(self):
        self.client.publish("adc", self.adc)


class GPS(Device):
    def Initialize(self):
        super().Initialize()
        self.latitude = 0
        self.longitude = 0

    def Update(self):
        if not super().Update():
            return

        if self.emulation:
            self.latitude = emu.GetFloat(64, 67)
            self.longitude = emu.GetFloat(60, 68)
            self.needPublish = True

    def Send(self):
        self.client.publish("lat", self.latitude)
        self.client.publish("lon", self.longitude)


class Power(Device):
    def Initialize(self):
        super().Initialize()
        self.active = True

    def Update(self):
        if not super().Update():
            return

    def Send(self):
        self.client.publish("electro", self.active)


class NoiseSensor(Device):
    def Initialize(self):
        super().Initialize()
        self.noise = 0

    def Update(self):
        if not super().Update():
            return

        if self.emulation:
            self.noise = emu.GetInt(0, 80)
            self.needPublish = True

    def Send(self):
        self.client.publish("noise", self.noise)


class Thermometer(Device):
    def __init__(
        self, client, index, clockInterval=1, *, emulation=False
    ):
        super().__init__(client, clockInterval, emulation=emulation)
        self.index = index

    def Initialize(self):
        super().Initialize()
        self.temperature = 0

    def Update(self):
        if not super().Update():
            return

        if self.emulation:
            self.temperature = emu.GetFloat(15, 60)
            self.needPublish = True

    def Send(self):
        self.client.publish(f"temp{self.index}", self.temperature)


class MovementSensor(Device):
    def __init__(
        self, client, index, clockInterval=1, *, emulation=False
    ):
        super().__init__(client, clockInterval, emulation=emulation)
        self.index = index

    def Initialize(self):
        super().Initialize()
        self.movement = False

    def Update(self):
        if not super().Update():
            return

        if self.emulation:
            self.movement = emu.GetBool()
            self.needPublish = True

    def Send(self):
        self.client.publish(f"move{self.index}", self.movement)
