import { CONFIG, gameState } from "./state.js";
import { applyEvents } from "./events.js";
import { getCookie } from "./utils.js";
import { draw } from "./canvas.js";


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
        crossCountry: false
    },
    hussar: {
        name: "Гусары",
        movePattern: "diagonal",
        moveRange: 3,
        attackPattern: "diagonal",
        attackRange: 3,
        icon: "🐎",
        cost: 2,
        crossCountry: false
    },
    cuirassier: {
        name: "Кирасиры",
        movePattern: "cross",
        moveRange: 4,
        attackPattern: "cross",
        attackRange: 4,
        icon: "🏇",
        cost: 4,
        crossCountry: false
    },
    artillery: {
        name: "Артиллерия",
        movePattern: "omni",
        moveRange: 1,
        attackPattern: "cross",
        attackRange: 5,
        icon: "💣",
        cost: 5,
        crossCountry: false
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

// AJAX запрос на ход
export async function makeMove(unitId, targetX, targetY) {
    try {
        const response = await fetch("/api/move/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                game_uid: gameState.gameUid,
                unit_id: unitId,
                to_x: targetX,
                to_y: targetY
            })
        });

        const result = await response.json();

        if (result.success) {
            applyEvents(result.events);
            gameState.selectedUnitId = null;
            gameState.validMoves = [];
            draw();
        } else {
            alert("Ошибка: " + (result.error || "Неизвестная ошибка"));
            gameState.selectedUnitId = null;
            gameState.validMoves = [];
            draw();
        }
    } catch (error) {
        console.error("Ошибка:", error);
        alert("Ошибка соединения с сервером");
        gameState.selectedUnitId = null;
        gameState.validMoves = [];
        draw();
    }
}
