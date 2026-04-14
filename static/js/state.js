// Конфигурация
export const CONFIG = {
    worldWidth: 10,
    worldHeight: 10,
    cellSize: 80,
    minZoom: 0.3,
    maxZoom: 2.0
};

// Игровое состояние
export class GameState {
    constructor(units = {}, firstSide = "russian", secondSide = "french", turnNumber = 1, activeSide = "russian", gameUid = null) {
        this.units = units;
        this.firstSide = firstSide;
        this.secondSide = secondSide;
        this.turnNumber = turnNumber;
        this.activeSide = activeSide;
        this.gameUid = gameUid;
        this.selectedUnitId = null;
        this.validMoves = [];
    }

    reset(data) {
        this.units = data.units;
        this.firstSide = data.first_side;
        this.secondSide = data.second_side;
        this.turnNumber = data.turn_number;
        this.activeSide = data.active_side;
        this.gameUid = data.game_uid;
        this.selectedUnitId = null;
        this.validMoves = [];
    }

    clearSelection() {
        this.selectedUnitId = null;
        this.validMoves = [];
    }

    switchTurn() {
        this.turnNumber += 1;
        this.activeSide = this.turnNumber % 2 === 1 ? this.firstSide : this.secondSide;
        this.clearSelection();
    }
}

export let gameState = new GameState();
