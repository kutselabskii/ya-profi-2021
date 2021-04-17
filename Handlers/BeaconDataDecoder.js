/**
 * Decodes data from "Beacon" system
 * @author `iprofi-369937608`
 * @param {string} data encoded data from beacon
 */
function process(data) {
  const view = ric.base64.decode(data);

  const latitude = view.getFloat32(0, true);
  const longitude = view.getFloat32(4, true);
  const altitude = view.getFloat32(8, true);
  const time = view.getInt32(12, true)
  const amount = view.getUint8(16);

  const hexChar = ["0", "1", "2", "3", "4", "5", "6", "7","8", "9", "A", "B", "C", "D", "E", "F"];

  var byte2hex = 
    function byte2hex(b) {
      return hexChar[(b >> 4) & 0x0f] + hexChar[b & 0x0f];
    };

  let rssi9812 = -127;
  let rssi0a35 = -127;
  let rssi2939 = -127;
  let rssid396 = -127;
  let rssif741 = -127;
  let rssi01dd = -127;
  let rssi08cd = -127;
  let rssi0e60 = -127;

  for (let i = 0; i < amount; ++i) {
    const offset = 17 + i * 3;
    const byte2 = byte2hex(view.getInt8(offset));
    const byte1 = byte2hex(view.getInt8(offset + 1));
    const power = view.getInt8(offset + 2);
    const name = byte1 + '' + byte2;

    switch (name) {
      case "9812":
        rssi9812 = power;
        break;
      case "0a35":
        rssi0a35 = power;
        break;
      case "2939":
        rssi2939 = power;
        break;
      case "d396":
        rssid396 = power;
        break;
      case "f741":
        rssif741 = power;
        break;
      case "01dd":
        rssi01dd = power;
        break;
      case "08cd":
        rssi08cd = power;
        break;
      case "0e60":
        rssi0e60 = power;
        break;
    }
  }
  
  return { latitude, longitude, altitude, time, amount, rssi9812, rssi0a35, rssi2939, rssid396, rssif741, rssi01dd, rssi08cd, rssi0e60 };
}