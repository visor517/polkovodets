import { CONFIG, gameState } from "./state.js";


// типы юнитов передаются в шаблон с бека
export let UNIT_TYPES = window.unitStats;

// Получение возможных ходов для юнита
export function getValidMoves(unit) {
    const moves = [];
    const unitType = UNIT_TYPES[unit.unit_type];
    if (!unitType) return moves;
    const maxCross = unitType.move.cross;
    const maxDiag = unitType.move.diag;

    // 8 направлений: 4 крестовых + 4 диагональных
    const directions = [
        [1, 0, maxCross], [-1, 0, maxCross], [0, 1, maxCross], [0, -1, maxCross],
        [1, 1, maxDiag], [1, -1, maxDiag], [-1, 1, maxDiag], [-1, -1, maxDiag]
    ];
    for (const [dx, dy, maxRange] of directions) {
        for (let step = 1; step <= maxRange; step++) {
            const newX = unit.x + dx * step;
            const newY = unit.y + dy * step;

            if (newX < 0 || newX >= CONFIG.worldWidth || newY < 0 || newY >= CONFIG.worldHeight) break;

            const targetUnit = Object.values(gameState.units).find(u => u.x === newX && u.y === newY);
            if (targetUnit) break;  // любой юнит блокирует

            moves.push({ x: newX, y: newY });
        }
    }
    return moves;
}


export function getValidAttacks(unit) {
    const attacks = [];
    const unitType = UNIT_TYPES[unit.unit_type];
    if (!unitType) return attacks;
    const maxCross = unitType.attack.cross;
    const maxDiag = unitType.attack.diag;

    // 8 направлений: 4 крестовых + 4 диагональных
    const directions = [
        [1, 0, maxCross], [-1, 0, maxCross], [0, 1, maxCross], [0, -1, maxCross],
        [1, 1, maxDiag], [1, -1, maxDiag], [-1, 1, maxDiag], [-1, -1, maxDiag]
    ];
    for (const [dx, dy, maxRange] of directions) {
        for (let step = 1; step <= maxRange; step++) {
            const newX = unit.x + dx * step;
            const newY = unit.y + dy * step;

            if (newX < 0 || newX >= CONFIG.worldWidth || newY < 0 || newY >= CONFIG.worldHeight) break;

            const targetUnit = Object.values(gameState.units).find(u => u.x === newX && u.y === newY);

            if (targetUnit) {
                if (targetUnit.army !== unit.army) {
                    attacks.push({ x: newX, y: newY });  // враг — цель для атаки
                }
                break;  // любой юнит (свой или чужой) блокирует дальнейший путь
            }
        }
    }
    return attacks;
}
