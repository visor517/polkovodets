import { gameState } from "./state.js";


export function applyEvents(events) {
    for (const event of events) {
        switch (event.type) {
            case "move":
                const unit = gameState.units.find(u => u.id === event.unit_id);
                if (unit) {
                    unit.x = event.to_x;
                    unit.y = event.to_y;
                }
                break;

            // Сюда позже добавятся:
            // case "destroy": ...
            // case "damage": ...
            // case "turn_change": ...
            // case "spawn": ...

            default:
                console.warn("Неизвестный тип события:", event.type);
        }
    }
}
