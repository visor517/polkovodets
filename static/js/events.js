import { gameState } from "./state.js";
import {draw} from "./canvas.js";


export function handleGameStart(data) {
    console.log("🎮 Новая игра начата", data.game_uid);
    gameState.reset(data);
    draw();

    const sideName = data.active_side === "russian" ? "русских" : "французов";
    document.getElementById("selectedInfo").innerHTML = `Новая игра начата. Ход ${sideName}.`;
}


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

            default:
                console.warn("Неизвестный тип события:", event.type);
        }
    }
}
