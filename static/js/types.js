/**
 * @typedef {Object} Unit
 * @property {number} id
 * @property {string} unit_type
 * @property {string} army
 * @property {number} x
 * @property {number} y
 * @property {number} last_used_turn
 */

/**
 * @typedef {Object} Game
 * @property {string} uid
 * @property {string} first_side
 * @property {string} second_side
 * @property {number} turn_number
 * @property {string} active_side
 * @property {boolean} is_finished
 * @property {Object.<number, Unit>} units
 */

/**
 * @typedef {Object} MoveStats
 * @property {number} cross
 * @property {number} diag
 */

/**
 * @typedef {Object} UnitTypeStats
 * @property {string} name
 * @property {MoveStats} move
 * @property {MoveStats} attack
 * @property {boolean} charges
 * @property {string} icon
 * @property {number} cost
 * @property {boolean} cross_country
 * @property {Object.<string, string>} images
 */