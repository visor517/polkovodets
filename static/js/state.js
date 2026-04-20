// Конфигурация
export const CONFIG = {
    worldWidth: 12,
    worldHeight: 12,
    cellSize: 80,
    minZoom: 0.3,
    maxZoom: 2.0
};

// Игровое состояние
export class GameState {
    constructor(gameUid, firstSide, secondSide, turnNumber = 1, activeSide, units = {}) {
        this.gameUid = gameUid;
        this.firstSide = firstSide;
        this.secondSide = secondSide;
        this.turnNumber = turnNumber;
        this.activeSide = activeSide;
        /** @type {Object.<number, Unit>} */
        this.units = units;
        this.selectedUnitId = null;
        this.validMoves = [];
        this.validAttacks = [];
    }

    reset(game) {
        this.gameUid = game.uid;
        this.firstSide = game.first_side;
        this.secondSide = game.second_side;
        this.turnNumber = game.turn_number;
        this.activeSide = game.active_side;
        this.units = game.units;
        this.selectedUnitId = null;
        this.validMoves = [];
        this.validAttacks = [];
    }

    clearSelection() {
        this.selectedUnitId = null;
        this.validMoves = [];
        this.validAttacks = [];
    }
}

export let gameState = new GameState();
