// Конфигурация
export const CONFIG = {
    cellSize: 80,
    minZoom: 0.3,
    maxZoom: 2.0
};

// Игровое состояние
export class GameState {
    constructor() {
        this.gameUid = null;
        this.worldWidth = 16;
        this.worldHeight = 12;
        this.firstSide = null;
        this.secondSide = null;
        this.turnNumber = 1;
        this.activeSide = null;
        this.units = {};
        this.selectedUnitId = null;
        this.validMoves = [];
        this.validAttacks = [];
    }

    reset(game) {
        this.gameUid = game.uid;
        this.worldWidth = game.world_width;
        this.worldHeight = game.world_height;
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
