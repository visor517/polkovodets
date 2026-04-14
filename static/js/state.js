// Конфигурация
export const CONFIG = {
    worldWidth: 10,
    worldHeight: 10,
    cellSize: 80,
    minZoom: 0.3,
    maxZoom: 2.0
};

// Игровое состояние
export let gameState = {
    units: [],
    currentTurn: "russian",
    selectedUnitId: null,
    validMoves: []
};

// Инициализация тестовых юнитов
export function initTestUnits() {
    return [
        // Русские юниты (левая сторона)
        { id: 1, type: "infantry", army: "russian", x: 0, y: 1},
        { id: 2, type: "infantry", army: "russian", x: 0, y: 2},
        { id: 3, type: "cuirassier", army: "russian", x: 0, y: 4},
        { id: 4, type: "cuirassier", army: "russian", x: 0, y: 5},
        { id: 5, type: "hussar", army: "russian", x: 0, y: 7},
        { id: 6, type: "hussar", army: "russian", x: 0, y: 8},
        { id: 7, type: "artillery", army: "russian", x: 2, y: 5},

        // Французские юниты (правая сторона)
        { id: 11, type: "infantry", army: "french", x: 8, y: 3},
        { id: 12, type: "infantry", army: "french", x: 8, y: 4},
        { id: 13, type: "infantry", army: "french", x: 8, y: 5},
        { id: 14, type: "infantry", army: "french", x: 8, y: 6},
        { id: 15, type: "infantry", army: "french", x: 9, y: 3},
        { id: 16, type: "infantry", army: "french", x: 9, y: 4},
        { id: 17, type: "infantry", army: "french", x: 9, y: 5},
        { id: 18, type: "infantry", army: "french", x: 9, y: 6},

    ];
}
