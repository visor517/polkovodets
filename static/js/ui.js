import { gameState } from "./state.js";
import { draw } from "./canvas.js";
import { handleGameStart } from "./events.js";
import { getCookie } from "./utils.js";

export function setupButtons() {
    // Кнопка новой игры
    const newGameButton = document.getElementById("newGameButton");
    if (newGameButton) {
        newGameButton.addEventListener("click", async () => {
            try {
                const response = await fetch("/api/new_game/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    }
                });

                const result = await response.json();

                if (result.success) {
                    handleGameStart(result);
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
        endTurnButton.addEventListener("click", () => {
            gameState.switchTurn();
            draw();

            const sideName = gameState.activeSide === "russian" ? "русских" : "французов";
            document.getElementById("selectedInfo").innerHTML = `Ход передан. Ход ${sideName}.`;
        });
    }
}
