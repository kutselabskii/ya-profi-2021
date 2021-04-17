import base64
import struct
from datetime import datetime


def decode(s):
    bytes = base64.b64decode(s)

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
        power = struct.unpack("b", bytes[offset + 2:offset + 3])[0]
        rssi[f"{byte1}:{byte2}"] = power

    return latitude, longitude, altitude, time, amount, rssi


def encode(latitude, longitude, altitude, time, rssi):
    data = bytearray()

    data.extend(struct.pack("<fffiB", latitude, longitude, altitude, time, len(rssi)))

    for i in rssi.keys():
        byte1, byte2 = list(map(lambda x: bytes([int(x, 16)]), i.split(':')))
        data.extend(struct.pack("ccb", byte2, byte1, rssi[i]))

    return base64.b64encode(data)


if __name__ == "__main__":
    print(decode("CtSLQu35ckJmZoY/vpUOYAgSmIY1CvQ5KQCW0/9B9+LdAZzNCM5gA+w="))
    print(encode(69.914139, 60.744068, 1.05, 1611568574, {'98:12': -122, '0a:35': -12, '29:39': 0, 'd3:96': -1, 'f7:41': -30, '01:dd': -100, '08:cd': -50, '03:60': -20}))
