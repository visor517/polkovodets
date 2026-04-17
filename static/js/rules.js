import { CONFIG, gameState } from "./state.js";


// Типы юнитов с их характеристиками
export const UNIT_TYPES = {
    infantry: {
        name: "Линейная пехота",
        movePattern: "omni",
        moveRange: 1,
        attackPattern: "omni",
        attackRange: 1,
        icon: "⚔️",
        cost: 1,
        crossCountry: false,
        images: {
            french: "/static/images/fr_infantry.png",
            russian: "/static/images/rus_infantry.png",
        }
    },
    hussar: {
        name: "Гусары",
        movePattern: "diagonal",
        moveRange: 3,
        attackPattern: "diagonal",
        attackRange: 3,
        icon: "🐎",
        cost: 2,
        crossCountry: false,
        images: {
            french: "/static/images/fr_hussar.png",
            russian: "/static/images/rus_hussar.png",
        }
    },
    cuirassier: {
        name: "Кирасиры",
        movePattern: "cross",
        moveRange: 4,
        attackPattern: "cross",
        attackRange: 4,
        icon: "🏇",
        cost: 4,
        crossCountry: false,
        images: {
            french: "/static/images/fr_cuirassier.png",
            russian: "/static/images/rus_cuirassier.png",
        }
    },
    artillery: {
        name: "Артиллерия",
        movePattern: "omni",
        moveRange: 1,
        attackPattern: "cross",
        attackRange: 5,
        icon: "💣",
        cost: 5,
        crossCountry: false,
        images: {
            french: "/static/images/fr_artillery.png",
            russian: "/static/images/rus_artillery.png",
        }
    }
};

// Получение возможных ходов для юнита
export function getValidMoves(unit) {
    const moves = [];
    const { moveRange, movePattern } = UNIT_TYPES[unit.type];

    for (let dx = -moveRange; dx <= moveRange; dx++) {
        for (let dy = -moveRange; dy <= moveRange; dy++) {
            if (dx === 0 && dy === 0) continue;

            if (movePattern === "cross" && dx !== 0 && dy !== 0) continue;
            if (movePattern === "diagonal" && Math.abs(dx) !== Math.abs(dy)) continue;

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
    const { attackRange, attackPattern } = UNIT_TYPES[unit.type];

    for (let dx = -attackRange; dx <= attackRange; dx++) {
        for (let dy = -attackRange; dy <= attackRange; dy++) {
            if (dx === 0 && dy === 0) continue;

            if (attackPattern === "cross" && dx !== 0 && dy !== 0) continue;
            if (attackPattern === "diagonal" && Math.abs(dx) !== Math.abs(dy)) continue;

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

