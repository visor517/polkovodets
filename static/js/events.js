import { gameState } from "./state.js";


export function applyEvents(events) {
    for (const event of events) {
        switch (event.type) {
            case "unit_updated":
                console.log("unit_before:", gameState.units[event.unit.id]);
                gameState.units[event.unit.id] = event.unit
                console.log("unit_after:", gameState.units[event.unit.id]);
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
