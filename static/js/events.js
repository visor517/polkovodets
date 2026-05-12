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
            case "score_change":
                gameState.player1Score = event.player1_score
                gameState.player2Score = event.player2_score
                break;
            case "round_change":
                gameState.moveNumber = event.move_number;
                gameState.roundNumber = event.round_number
                gameState.activeSide = event.active_side;
                gameState.clearSelection();
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
