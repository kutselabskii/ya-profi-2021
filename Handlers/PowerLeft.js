//@ts-check : enable more type checks for editor
//@handler  : Расчет запаса заряда аккумулятора защитного костюма
//@author   : Iprofi-369937608

/**
 * Makes the sum of two numbers
 * @author `iprofi-369937608`
 * @param {number} charge first
 * @param {number} capacity second
 * @param {number} power third
 */
function process(charge, capacity, power) {
  const minutes = (charge / 100) * (capacity / power) * 60
  return { minutes };
}

/* ↑ here ends original handler code  */
/* ↓ here goes generated debug  code  */

/* 01. define test values */
const config = {};
const packet = {
  "charge": 57,
  "capacity": 10,
  "power": 24
};

/* 02. run handler code */
const result = process(
  packet["charge"],
  packet["capacity"],
  packet["power"]
);

/* 03. log handler results */
console.log({
  "minutes": result["minutes"]
});

