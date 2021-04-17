/**
 * Makes the sum of two numbers
 * @author `iprofi-369937608`
 * @param {string} calibration_string String encoded calibration table
 * @param {number} adc Value from adc
 * @param {number} max_fuel Maximum fuel level
 */
 function process(calibration_string, adc, max_fuel) {
    if (!calibration_string || !adc || !max_fuel) {
      return {}
    }
  
    const ct = JSON.parse(calibration_string);
  
    let num = 0;
    for (let i = 0; i < ct.length; ++i) {
      if (adc >= ct[i][0]) {
        num = i;
      }
    }
  
    const res = ct[num][1] + (ct[num + 1][1] - ct[num][1]) / (ct[num + 1][0] - ct[num][0]) * (adc - ct[num][0]);
    const percentage = res / max_fuel * 100;
  
    return { res, percentage };
  }