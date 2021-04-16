import base64
import struct
from datetime import datetime


def decode(s):
    bytes = base64.b64decode("CtSLQu35ckLNO4Y/vpUOYAQSmIE1CoE5KYGW04E=")

    latitude = struct.unpack("<f", bytes[:4])[0]
    longitude = struct.unpack("<f", bytes[4:8])[0]
    altitude = struct.unpack("<f", bytes[8:12])[0]
    time = datetime.utcfromtimestamp(struct.unpack("<i", bytes[12:16])[0])
    amount = struct.unpack("<B", bytes[16:17])[0]

    rssi = {}
    for i in range(amount):
        offset = 17 + i * 3

        byte2 = struct.unpack("c", bytes[offset:offset + 1])[0].hex()
        byte1 = struct.unpack("c", bytes[offset + 1:offset + 2])[0].hex()
        power = struct.unpack("b", bytes[offset + 2:offset + 3])
        rssi[f"{byte1}:{byte2}"] = power

    return latitude, longitude, altitude, time, amount, rssi


if __name__ == "__main__":
    print(decode("CtSLQu35ckLNO4Y/vpUOYAQSmIE1CoE5KYGW04E="))
