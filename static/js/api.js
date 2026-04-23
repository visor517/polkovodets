import {getCookie} from "./utils.js";
import {gameState} from "./state.js";
import {applyEvents} from "./events.js";
import {draw} from "./canvas.js";


export async function makeAttack(unitId, targetX, targetY) {
    try {
        const response = await fetch("/api/attack/", {
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

export async function loadUnitStats() {
    const response = await fetch("/api/unit_stats/");
    return await response.json();
}

export async function loadCurrentGame() {
    const response = await fetch("/api/current_game/");
    return await response.json();
}

export async function createNewGame() {
    const response = await fetch("/api/new_game/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        }
    });
    return await response.json();
}

export async function endTurn() {
    const response = await fetch("/api/end_turn/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            game_uid: gameState.gameUid
        })
    });
    return await response.json();
}
