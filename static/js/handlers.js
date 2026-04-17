import { gameState } from "./state.js";
import { draw } from "./canvas.js";
import { makeAttack, makeMove } from "./api.js";
import { getValidAttacks, getValidMoves, UNIT_TYPES } from "./rules.js";


// Обработка клика по клетке
export function handleCellClick(worldX, worldY) {
    // Ищем юнита на этой клетке
    const clickedUnit = Object.values(gameState.units).find(u => u.x === worldX && u.y === worldY);

    // Если выбран юнит и клик на возможном ходе
    if (gameState.selectedUnitId !== null) {
        const selectedUnit = gameState.units[gameState.selectedUnitId];

        // Атака по врагу
        if (gameState.validAttacks?.some(attack => attack.x === worldX && attack.y === worldY)) {
            makeAttack(selectedUnit.id, worldX, worldY);
        }
        // Перемещение на пустую клетку
        else if (gameState.validMoves.some(move => move.x === worldX && move.y === worldY)) {
            makeMove(selectedUnit.id, worldX, worldY);
        }
        // Клик мимо — сброс выделения
        else {
            gameState.clearSelection();
            draw();
        }
    }
    // Если клик на своём юните
    else if (clickedUnit && clickedUnit.army === gameState.activeSide) {
        gameState.selectedUnitId = clickedUnit.id;
        gameState.validMoves = getValidMoves(clickedUnit);
        gameState.validAttacks = getValidAttacks(clickedUnit);
        draw();

        const unitInfo = UNIT_TYPES[clickedUnit.type];

        // Формируем текст для атаки
        let attackText = "";
        if (unitInfo.attackPattern === "omni") {
            attackText = `во все стороны на ${unitInfo.attackRange}`;
        } else if (unitInfo.attackPattern === "cross") {
            attackText = `вертикаль/горизонталь на ${unitInfo.attackRange}`;
        } else if (unitInfo.attackPattern === "diagonal") {
            attackText = `диагональ на ${unitInfo.attackRange}`;
        }

        // Формируем текст для движения
        let moveText = "";
        if (unitInfo.movePattern === "omni") {
            moveText = `во все стороны на ${unitInfo.moveRange}`;
        } else if (unitInfo.movePattern === "cross") {
            moveText = `вертикаль/горизонталь на ${unitInfo.moveRange}`;
        } else if (unitInfo.movePattern === "diagonal") {
            moveText = `диагональ на ${unitInfo.moveRange}`;
        }

        // Проходимость препятствий
        const crossCountryText = unitInfo.crossCountry ? "✅ может" : "❌ не может";

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
export function handleGameStart(data) {
    console.log("🎮 Новая игра начата", data.game.uid);
    gameState.reset(data.game);
    draw();

    const sideName = data.active_side === "russian" ? "русских" : "французов";
    document.getElementById("selectedInfo").innerHTML = `Новая игра начата. Ход ${sideName}.`;
}
