import { gameState } from "./state.js";
import { draw } from "./canvas.js";
import { makeAttack, makeMove } from "./api.js";
import { getValidAttacks, getValidMoves, UNIT_TYPES } from "./rules.js";


// Обработка клика по клетке
export function handleCellClick(worldX, worldY) {
    // Ищем юнита на этой клетке
    /** @type {Unit} */
    const clickedUnit = Object.values(gameState.units).find(u => u.x === worldX && u.y === worldY);

    // Если выбран юнит и клик на возможном ходе
    if (gameState.selectedUnitId !== null) {
        const selectedUnit = gameState.units[gameState.selectedUnitId];
        if (gameState.validAttacks?.some(attack => attack.x === worldX && attack.y === worldY)) {
            makeAttack(selectedUnit.id, worldX, worldY);
            return;
        }
        if (gameState.validMoves.some(move => move.x === worldX && move.y === worldY)) {
            makeMove(selectedUnit.id, worldX, worldY);
            return;
        }
    }

    // Если клик на своём юните
    if (clickedUnit && clickedUnit.army === gameState.activeSide) {
        // Проверяем, не действовал ли юнит в этом ходу
        if (clickedUnit.last_used_turn === gameState.turnNumber) {
            document.getElementById("selectedInfo").innerHTML =
                `${UNIT_TYPES[clickedUnit.unit_type].name} уже действовал в этом ходу`;
            return;
        }

        gameState.selectedUnitId = clickedUnit.id;
        gameState.validMoves = getValidMoves(clickedUnit);
        gameState.validAttacks = getValidAttacks(clickedUnit);
        draw();

        /** @type {UnitTypeStats} */
        const unitInfo = UNIT_TYPES[clickedUnit.unit_type];

        // Формируем текст для атаки
        let attackText = "";
        if (unitInfo.attack.cross > 0 && unitInfo.attack.diag > 0) {
            attackText = `крест: ${unitInfo.attack.cross}, диагональ: ${unitInfo.attack.diag}`;
        } else if (unitInfo.attack.cross > 0) {
            attackText = `вертикаль/горизонталь на ${unitInfo.attack.cross}`;
        } else if (unitInfo.attack.diag > 0) {
            attackText = `диагональ на ${unitInfo.attack.diag}`;
        } else {
            attackText = "не может атаковать";
        }

        // Формируем текст для движения
        let moveText = "";
        if (unitInfo.move.cross > 0 && unitInfo.move.diag > 0) {
            moveText = `крест: ${unitInfo.move.cross}, диагональ: ${unitInfo.move.diag}`;
        } else if (unitInfo.move.cross > 0) {
            moveText = `вертикаль/горизонталь на ${unitInfo.move.cross}`;
        } else if (unitInfo.move.diag > 0) {
            moveText = `диагональ на ${unitInfo.move.diag}`;
        } else {
            moveText = "не может ходить";
        }

        // Проходимость препятствий
        const crossCountryText = unitInfo.cross_country ? "✅ может" : "❌ не может";

        document.getElementById("selectedInfo").innerHTML =
            `Выбран: ${unitInfo.name}<br>` +
            `Движение: ${moveText}<br>` +
            `Атака: ${attackText}<br>` +
            `Проход 🌲⛰🐸: ${crossCountryText}`;
    }
    // Снимаем выделение
    else {
        gameState.clearSelection();
        draw();
        document.getElementById("selectedInfo").innerHTML = "Кликните на юнита для выбора";
    }
}


// Обработка старта игры
export function handleGameStart(game) {
    console.log("🎮 Новая игра начата", game.uid);
    gameState.reset(game);
    draw();
    console.log(game)
    const sideName = game.active_side === "russian" ? "русских" : "французов";
    document.getElementById("selectedInfo").innerHTML = `Новая игра начата. Ход ${sideName}.`;
}
