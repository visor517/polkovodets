import { gameState } from "./state.js";


export function applyEvents(events) {
    for (const event of events) {
        switch (event.type) {
            case "move":
                const unit = gameState.units[event.unit_id];
                if (unit) {
                    unit.x = event.to_x;
                    unit.y = event.to_y;
                }
                break;
            case "destroy":
                delete gameState.units[event.unit_id];
                break;
            case "turn_change":
                gameState.turnNumber = event.turn_number;
                gameState.activeSide = event.active_side;
                gameState.clearSelection();
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
}
