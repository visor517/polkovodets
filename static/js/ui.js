import { createNewGame, endTurn } from "./api.js";
import { gameState } from "./state.js";
import { draw } from "./canvas.js";
import { handleGameStart } from "./handlers.js";


export function setupButtons() {
    // Кнопка новой игры
    const newGameButton = document.getElementById("newGameButton");
    if (newGameButton) {
        newGameButton.addEventListener("click", async () => {
            try {
                const result = await createNewGame();
                if (result.success) {
                    handleGameStart(result.game);
                } else {
                    alert("Ошибка создания игры");
                }
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Ошибка соединения с сервером");
            }
        });
    }

    // Кнопка завершения хода
    const endTurnButton = document.getElementById("endTurnButton");
    if (endTurnButton) {
        endTurnButton.addEventListener("click", async () => {
            try {
                const result = await endTurn();

                if (result.success) {
                    gameState.turnNumber = result.turn_number;
                    gameState.activeSide = result.active_side;
                    gameState.clearSelection();
                    draw();
                } else {
                    alert("Ошибка: " + (result.error || "Неизвестная ошибка"));
                }
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Ошибка соединения с сервером");
            }
        });
    }
}
