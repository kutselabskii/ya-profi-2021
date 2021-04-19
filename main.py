import tkinter as tk
from Devices import AirPollutionSensor
from Views import AirPollutionView
import Common.secrets as sec

destroyed = False


def OnClose():
    global destroyed
    destroyed = True


def main():
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", OnClose)

    airSensor = AirPollutionSensor(sec.AirPollutionSensorClientId, 10, emulation=True)
    airSensorView = AirPollutionView(airSensor, root)

    while True:
        airSensor.Update()
        airSensor.Publish()
        if not destroyed:
            root.update()
        else:
            break


if __name__ == "__main__":
    main()
