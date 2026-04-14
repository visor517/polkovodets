import { CONFIG, gameState } from "./state.js";
import { initCanvas, draw, loadImages, setupCameraControls, canvas, camera } from "./canvas.js";
import { UNIT_TYPES, getValidMoves, makeMove } from "./rules.js";
import { setupButtons } from "./ui.js";


// Обработка клика по клетке
export function handleCellClick(worldX, worldY) {
    // Ищем юнита на этой клетке
    const clickedUnit = Object.values(gameState.units).find(u => u.x === worldX && u.y === worldY);

    // Если выбран юнит и клик на возможном ходе
    if (gameState.selectedUnitId !== null && gameState.validMoves.some(move => move.x === worldX && move.y === worldY)) {
        const selectedUnit = gameState.units[gameState.selectedUnitId];

        if (selectedUnit && selectedUnit.army === gameState.activeSide) {
            // Выполняем ход через AJAX
            makeMove(selectedUnit.id, worldX, worldY);
        } else {
            gameState.selectedUnitId = null;
            gameState.validMoves = [];
            draw();
        }
    }
    // Если клик на своём юните
    else if (clickedUnit && clickedUnit.army === gameState.activeSide) {
        gameState.selectedUnitId = clickedUnit.id;
        gameState.validMoves = getValidMoves(clickedUnit);
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

// Инициализация игры
async function init() {
    // Инициируем canvas
    initCanvas();

    // Загружаем изображения
    await loadImages();

    // Настраиваем начальную позицию камеры, чтобы видеть всё поле
    const totalWidth = CONFIG.cellSize * CONFIG.worldWidth;
    const totalHeight = CONFIG.cellSize * CONFIG.worldHeight;
    camera.zoom = Math.min(canvas.width / totalWidth, canvas.height / totalHeight) * 0.9;
    camera.offsetX = (canvas.width - totalWidth * camera.zoom) / 2;
    camera.offsetY = (canvas.height - totalHeight * camera.zoom) / 2;

    setupCameraControls();
    setupButtons();
    draw();
}

// Запуск игры после загрузки страницы
window.addEventListener("DOMContentLoaded", init);
