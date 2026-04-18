import { loadUnitStats } from "./api.js";
import { CONFIG, gameState } from "./state.js";


// типы юнитов загружаются с бека
export let UNIT_TYPES = {};

export async function initUnitStats() {
    UNIT_TYPES = await loadUnitStats();
    return UNIT_TYPES;
}


// Получение возможных ходов для юнита
export function getValidMoves(unit) {
    const moves = [];
    const { move_range, move_pattern } = UNIT_TYPES[unit.type];

    for (let dx = -move_range; dx <= move_range; dx++) {
        for (let dy = -move_range; dy <= move_range; dy++) {
            if (dx === 0 && dy === 0) continue;

            if (move_pattern === "cross" && dx !== 0 && dy !== 0) continue;
            if (move_pattern === "diagonal" && Math.abs(dx) !== Math.abs(dy)) continue;
            if (move_pattern === "omni" && dx !== 0 && dy !== 0 && Math.abs(dx) !== Math.abs(dy)) continue;

            const newX = unit.x + dx;
            const newY = unit.y + dy;

            if (newX >= 0 && newX < CONFIG.worldWidth && newY >= 0 && newY < CONFIG.worldHeight) {
                // Проверяем, есть ли свой юнит на целевой клетке
                let isFriendly = false;
                for (const otherUnit of Object.values(gameState.units)) {
                    if (otherUnit.x === newX && otherUnit.y === newY && otherUnit.army === unit.army) {
                        isFriendly = true;
                        break;
                    }
                }
                if (!isFriendly) {
                    moves.push({ x: newX, y: newY });
                }
            }
        }
    }
    return moves;
}


export function getValidAttacks(unit) {
    const attacks = [];
    const { attack_range, attack_pattern } = UNIT_TYPES[unit.type];

    for (let dx = -attack_range; dx <= attack_range; dx++) {
        for (let dy = -attack_range; dy <= attack_range; dy++) {
            if (dx === 0 && dy === 0) continue;

            if (attack_pattern === "cross" && dx !== 0 && dy !== 0) continue;
            if (attack_pattern === "diagonal" && Math.abs(dx) !== Math.abs(dy)) continue;
            if (attack_pattern === "omni" && dx !== 0 && dy !== 0 && Math.abs(dx) !== Math.abs(dy)) continue;

            const newX = unit.x + dx;
            const newY = unit.y + dy;

            if (newX >= 0 && newX < CONFIG.worldWidth && newY >= 0 && newY < CONFIG.worldHeight) {
                // Проверяем, есть ли враг на целевой клетке
                let isEnemy = false;
                for (const otherUnit of Object.values(gameState.units)) {
                    if (otherUnit.x === newX && otherUnit.y === newY && otherUnit.army !== unit.army) {
                        isEnemy = true;
                        break;
                    }
                }
                if (isEnemy) {
                    attacks.push({ x: newX, y: newY });
                }
            }
        }
    }
    return attacks;
}

