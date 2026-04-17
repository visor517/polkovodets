import {getCookie} from "./utils.js";
import {gameState} from "./state.js";
import {applyEvents} from "./events.js";
import {draw} from "./canvas.js";


export async function makeAttack(unitId, targetX, targetY) {
    console.log("⚔️ Атака:", unitId, "→", targetX, targetY);
    // Пока просто перенаправляем на makeMove
    return makeMove(unitId, targetX, targetY);
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
        } else {
            alert("Ошибка: " + (result.error || "Неизвестная ошибка"));
        }
    } catch (error) {
        console.error("Ошибка:", error);
        alert("Ошибка соединения с сервером");
    } finally {
        gameState.clearSelection();
        draw();
    }
}
