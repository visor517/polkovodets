import { CONFIG, gameState } from "./state.js";
import { handleCellClick } from "./handlers.js";
import { UNIT_TYPES} from "./rules.js";


// Canvas и управление
export let canvas, ctx;
export let camera = {
    offsetX: 0,
    offsetY: 0,
    zoom: 0.8,
    isPanning: false,
    panStartX: 0,
    panStartY: 0
};

// Инициализация canvas
export function initCanvas() {
    canvas = document.getElementById("gameCanvas");
    ctx = canvas.getContext("2d");
}

// Загрузка изображений
export const images = {};

// Загрузка всех изображений
export function loadImages() {
    const promises = [];
    for (const unitType of Object.values(UNIT_TYPES)) {
        for (const army of ["french", "russian"]) {
            const path = unitType.images?.[army];
            if (path && !images[path]) {
                const img = new Image();
                img.src = path;
                images[path] = img;
                promises.push(new Promise((resolve) => {
                    img.onload = resolve;
                    img.onerror = () => {
                        console.warn(`Не удалось загрузить ${path}`);
                        resolve();
                    };
                }));
            }
        }
    }
    return Promise.all(promises);
}

// Рисование клетки
function drawCell(x, y, screenX, screenY, cellSize) {
    ctx.fillStyle = "#090";
    ctx.fillRect(screenX, screenY, cellSize, cellSize);

    // Рисуем границу
    ctx.strokeStyle = "#111";
    ctx.lineWidth = 1;
    ctx.strokeRect(screenX, screenY, cellSize, cellSize);

    // Подсветка возможных ходов зеленым
    if (gameState.validMoves.some(move => move.x === x && move.y === y)) {
        ctx.fillStyle = "rgba(250,239,47,0.5)";
        ctx.fillRect(screenX, screenY, cellSize, cellSize);
    }
    // Подсветка атак (красным)
    if (gameState.validAttacks && gameState.validAttacks.some(attack => attack.x === x && attack.y === y)) {
        ctx.fillStyle = "rgba(255, 0, 0, 0.5)";
        ctx.fillRect(screenX, screenY, cellSize, cellSize);
    } else if (gameState.validMoves.some(move => move.x === x && move.y === y)) {
        ctx.fillStyle = "rgba(250,239,47,0.5)";
        ctx.fillRect(screenX, screenY, cellSize, cellSize);
}
}

// Рисование юнита
function drawUnit(unit, screenX, screenY, cellSize) {
    const imagePath = UNIT_TYPES[unit.unit_type]?.images?.[unit.army];
    const img = imagePath ? images[imagePath] : null;

    // Использованный юнит прозрачнее
    const isUsed = (unit.last_used_turn === gameState.turnNumber && unit.army === gameState.activeSide);
    if (isUsed) ctx.globalAlpha = 0.7;

    if (img && img.complete && img.naturalWidth > 0) {
        // Рисуем PNG картинку
        const padding = cellSize * 0.1;
        ctx.drawImage(img, screenX + padding, screenY + padding, cellSize - padding * 2, cellSize - padding * 2);
    } else {
        // Запасной вариант - цветной прямоугольник с иконкой
        const color = unit.army === "french" ? "#1a3a8a" : "#8b1a1a";
        ctx.fillStyle = color;
        ctx.fillRect(screenX + 5, screenY + 5, cellSize - 10, cellSize - 10);

        // Иконка типа юнита
        ctx.fillStyle = "white";
        ctx.font = `${Math.floor(cellSize * 0.4)}px Arial`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        let icon = UNIT_TYPES[unit.unit_type].icon;
        ctx.fillText(icon, screenX + cellSize / 2, screenY + cellSize / 2);
    }

    if (isUsed) ctx.globalAlpha = 1.0;  // сброс

    // Рамка выделения
    if (gameState.selectedUnitId === unit.id) {
        ctx.strokeStyle = "#ffd700";
        ctx.lineWidth = 4;
        ctx.strokeRect(screenX + 2, screenY + 2, cellSize - 4, cellSize - 4);
    }
}

// Основная отрисовка
export function draw() {
    if (!ctx) return;

    const cellSize = CONFIG.cellSize * camera.zoom;

    // Вычисляем видимую область
    const startCol = Math.max(0, Math.floor(-camera.offsetX / cellSize));
    const endCol = Math.min(CONFIG.worldWidth, Math.ceil((canvas.width - camera.offsetX) / cellSize) + 1);
    const startRow = Math.max(0, Math.floor(-camera.offsetY / cellSize));
    const endRow = Math.min(CONFIG.worldHeight, Math.ceil((canvas.height - camera.offsetY) / cellSize) + 1);

    // Очищаем canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Рисуем фон для невидимой области
    ctx.fillStyle = "#2c1810";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Рисуем только видимые клетки
    for (let row = startRow; row < endRow; row++) {
        for (let col = startCol; col < endCol; col++) {
            const screenX = col * cellSize + camera.offsetX;
            const screenY = row * cellSize + camera.offsetY;
            drawCell(col, row, screenX, screenY, cellSize);
        }
    }

    // Рисуем юнитов
    for (const unit of Object.values(gameState.units)) {
        if (unit.x >= startCol && unit.x < endCol && unit.y >= startRow && unit.y < endRow) {
            const screenX = unit.x * cellSize + camera.offsetX;
            const screenY = unit.y * cellSize + camera.offsetY;
            drawUnit(unit, screenX, screenY, cellSize);
        }
    }

    // Обновляем информационную панель
    document.getElementById("infoPanel").innerHTML =
        `Ход ${gameState.turnNumber}: ${gameState.activeSide === "french" ? "Французская армия" : "Русская армия"} | Зум: ${camera.zoom.toFixed(2)}x | ${gameState.gameUid}`;
}

// Настройка управления камерой
export function setupCameraControls() {
    // Зум колесиком
    canvas.addEventListener("wheel", (e) => {
        e.preventDefault();
        const delta = e.deltaY > 0 ? 0.9 : 1.1;
        const newZoom = Math.min(CONFIG.maxZoom, Math.max(CONFIG.minZoom, camera.zoom * delta));

        if (newZoom !== camera.zoom) {
            // Зум относительно позиции мыши
            const mouseX = e.clientX - canvas.offsetLeft;
            const mouseY = e.clientY - canvas.offsetTop;
            const worldX = (mouseX - camera.offsetX) / (CONFIG.cellSize * camera.zoom);
            const worldY = (mouseY - camera.offsetY) / (CONFIG.cellSize * camera.zoom);

            camera.zoom = newZoom;

            camera.offsetX = mouseX - worldX * CONFIG.cellSize * camera.zoom;
            camera.offsetY = mouseY - worldY * CONFIG.cellSize * camera.zoom;

            draw();
        }
    });

    // Панорамирование правой кнопкой
    canvas.addEventListener("mousedown", (e) => {
        if (e.button === 2) {
            e.preventDefault();
            camera.isPanning = true;
            camera.panStartX = e.clientX - camera.offsetX;
            camera.panStartY = e.clientY - camera.offsetY;
            canvas.style.cursor = "grabbing";
        }
    });

    window.addEventListener("mousemove", (e) => {
        if (camera.isPanning) {
            camera.offsetX = e.clientX - camera.panStartX;
            camera.offsetY = e.clientY - camera.panStartY;

            // Ограничиваем панорамирование
            const maxOffsetX = CONFIG.cellSize * camera.zoom * CONFIG.worldWidth - canvas.width;
            const maxOffsetY = CONFIG.cellSize * camera.zoom * CONFIG.worldHeight - canvas.height;
            camera.offsetX = Math.min(0, Math.max(-maxOffsetX, camera.offsetX));
            camera.offsetY = Math.min(0, Math.max(-maxOffsetY, camera.offsetY));

            draw();
        }
    });

    window.addEventListener("mouseup", (e) => {
        if (e.button === 2) {
            camera.isPanning = false;
            canvas.style.cursor = "grab";
        }
    });

    // Левый клик для игры
    canvas.addEventListener("click", (e) => {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;

        const mouseX = (e.clientX - rect.left) * scaleX;
        const mouseY = (e.clientY - rect.top) * scaleY;

        const worldX = Math.floor((mouseX - camera.offsetX) / (CONFIG.cellSize * camera.zoom));
        const worldY = Math.floor((mouseY - camera.offsetY) / (CONFIG.cellSize * camera.zoom));

        if (worldX >= 0 && worldX < CONFIG.worldWidth && worldY >= 0 && worldY < CONFIG.worldHeight) {
            handleCellClick(worldX, worldY);
        }
    });

    canvas.addEventListener("contextmenu", (e) => {
        e.preventDefault();
        return false;
    });
}
