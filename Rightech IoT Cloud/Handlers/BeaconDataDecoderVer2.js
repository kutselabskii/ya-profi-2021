//@ts-check : enable more type checks for editor
//@handler  : Парсинг данных согласно протоколу
//@author   : Iprofi-369937608

/**
 * Decodes data from "Beacon" system
 * @author `iprofi-369937608`
 * @param {string} data encoded data from beacon
 */
function process(data) {
  if (!data) {
    return {}
  }

  const view = ric.base64.decode(data);

  const latitude = view.getFloat32(0, true);
  const longitude = view.getFloat32(4, true);
  const altitude = view.getFloat32(8, true);
  const time = view.getInt32(12, true)
  const amount = view.getUint8(16);

  const hexChar = ["0", "1", "2", "3", "4", "5", "6", "7","8", "9", "a", "b", "c", "d", "e", "f"];

  var byte2hex = 
    function byte2hex(b) {
      return hexChar[(b >> 4) & 0x0f] + hexChar[b & 0x0f];
    };

  let rssi = {
    "98_12": -127,
    "0a_35": -127,
    "29_39": -127,
    "d3_96": -127,
    "f7_41": -127,
    "01_dd": -127,
    "08_cd": -127,
    "0e_60": -127
  };


  for (let i = 0; i < amount; ++i) {
    const offset = 17 + i * 3;
    const byte2 = byte2hex(view.getInt8(offset));
    const byte1 = byte2hex(view.getInt8(offset + 1));
    const power = view.getInt8(offset + 2);
    const name = byte1 + '_' + byte2;
    rssi[name] = power;
  }
  
  return { latitude, longitude, altitude, time, amount, rssi };
}

/* ↑ here ends original handler code  */
/* ↓ here goes generated debug  code  */

/* 01. define test values */
const config = {};
const packet = {
  "data": "string"
};

/* 02. run handler code */
const result = process(
  packet["data"]
);

/* 03. log handler results */
console.log({
  "latitude": result["latitude"],
  "longitude": result["longitude"],
  "altitude": result["altitude"],
  "time": result["time"],
  "amount": result["amount"],
  "rssi": result["rssi"]
});

