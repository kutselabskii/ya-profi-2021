/**
 * Calculates left battery time
 * @author `iprofi-369937608`
 * @param {number} charge first
 * @param {number} capacity second
 * @param {number} power third
 */
 function process(charge, capacity, power) {
  if (!charge || !capacity || !power) {
    return {}
  }

  const minutes = (charge / 100) * (capacity / power) * 60
  return { minutes };
}