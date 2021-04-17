/**
 * Calculates distance to each beacon
 * @author `iprofi-369937608`
 * @param {object} x X
 * @param {object} y Y
 * @param {object} z Z
 */
 function process(x, y, z) {
    var calc = function (costume, beacon) {
      return Math.sqrt(Math.pow(costume['x'] - beacon['x'], 2) + Math.pow(costume['y'] - beacon['y'], 2) + Math.pow(costume['z'] - beacon['z'], 2));
    }
    
    const coords = {'x': x, 'y': y, 'z': z};
  
    const c9812 = {'x': 10, 'y': 25, 'z': -27};
    const c0a35 = {'x': 90, 'y': 5, 'z': -27};
    const c2939 = {'x': 10, 'y': 5, 'z': -27};
    const cd396 = {'x': 90, 'y': 25, 'z': -27};
    const cf741 = {'x': 37, 'y': 25, 'z': -27};
    const c01dd = {'x': 64, 'y': 25, 'z': -27};
    const c08cd = {'x': 37, 'y': 5, 'z': -27};
    const c0e60 = {'x': 64, 'y': 5, 'z': -27};
  
    const r9812 = calc(coords, c9812);
    const r0a35 = calc(coords, c0a35);
    const r2939 = calc(coords, c2939);
    const rd396 = calc(coords, cd396);
    const rf741 = calc(coords, cf741);
    const r01dd = calc(coords, c01dd);
    const r08cd = calc(coords, c08cd);
    const r0e60 = calc(coords, c0e60);
  
    return { r9812, r0a35, r2939, rd396, rf741, r01dd, r08cd, r0e60 };
  }