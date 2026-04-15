// Конфигурация
export const CONFIG = {
    worldWidth: 12,
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

    reset(game) {
        this.units = game.units;
        this.firstSide = game.first_side;
        this.secondSide = game.second_side;
        this.turnNumber = game.turn_number;
        this.activeSide = game.active_side;
        this.gameUid = game.uid;
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
