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
        this.player1Side = null;
        this.player1Score = 0;
        this.player2Side = null;
        this.player2Score = 0;
        this.moveNumber = 1;
        this.roundNumber = 1;
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
        this.player1Side = game.player1_side;
        this.player1Score = game.player1_score;
        this.player2Side = game.player2_side;
        this.player2Score = game.player2_score;
        this.moveNumber = game.move_number;
        this.roundNumber = game.round_number;
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
