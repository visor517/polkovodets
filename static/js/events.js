import { gameState } from "./state.js";
import { draw } from "./canvas.js";


export function applyEvents(events) {
    for (const event of events) {
        switch (event.type) {
            case "unit_updated":
                gameState.units[event.unit.id] = event.unit
                break;
            case "destroy":
                delete gameState.units[event.unit_id];
                break;
            case "turn_change":
                gameState.turnNumber = event.turn_number;
                gameState.activeSide = event.active_side;
                gameState.clearSelection();
                // Очищаем сообщение о выбранном юните
                document.getElementById("selectedInfo").innerHTML = "Кликните на юнита для выбора";
                break;
            case "game_over":
                gameState.isFinished = true;
                const winnerName = event.winner === "russian" ? "Русская армия" : "Французская армия";
                alert(`🏆 Игра окончена! Победила ${winnerName}!`);
                break;

            default:
                console.warn("Неизвестный тип события:", event.type);
        }
    }
    draw();
}
