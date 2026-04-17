import { CONFIG } from "./state.js";
import { initCanvas, draw, loadImages, setupCameraControls, canvas, camera } from "./canvas.js";
import { setupButtons } from "./ui.js";


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
