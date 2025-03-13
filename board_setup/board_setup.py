import random

class BoardSetup:
    SHIP_LENGTHS = {
        1: 2,  # ID=1 -> Length 2
        2: 3,  # ID=2 -> Length 3
        3: 4,  # ID=3 -> Length 4
        4: 5,  # ID=4 -> Length 5
        5: "L-shape" # ID=5 -> L-shape
    }

    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.attacked_positions = set()

    def get_board(self) -> list[list[int]]:
        return self.board

    def get_tile(self, x: int, y: int) -> int:
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return self.board[y][x]
        else:
            raise IndexError("Coordinates out of bounds.")

    def place_ships(self) -> None:
        """
        Place ships randomly on the board without overlap.
        Handles both straight and L-shaped ships.
        """
        for ship_id, count in self.ships_dict.items():
            for _ in range(count):
                placed = False
                while not placed:
                    x = random.randint(0, self.cols - 1)
                    y = random.randint(0, self.rows - 1)

                    if self.SHIP_LENGTHS.get(ship_id) == "L-shape":
                        placed = self._place_l_shape(x, y, ship_id)
                    else:
                        length = self.SHIP_LENGTHS.get(ship_id, ship_id)
                        horizontal = random.choice([True, False])
                        if horizontal:
                            if x + length <= self.cols and all(self.board[y][x + i] == 0 for i in range(length)):
                                for i in range(length):
                                    self.board[y][x + i] = ship_id
                                placed = True
                        else:
                            if y + length <= self.rows and all(self.board[y + i][x] == 0 for i in range(length)):
                                for i in range(length):
                                    self.board[y + i][x] = ship_id
                                placed = True

    def _place_l_shape(self, x, y, ship_id) -> bool:
        """
        Attempt to place an L-shaped ship.
        """
        L_SHAPE_OFFSETS = [
            [(0, 0), (1, 0), (2, 0), (2, 1)],   # Standard L
            [(0, 0), (0, 1), (0, 2), (1, 2)],   # Rotated 90°
            [(0, 1), (1, 1), (2, 1), (2, 0)],   # Rotated 180°
            [(1, 0), (1, 1), (1, 2), (0, 2)]    # Rotated 270°
        ]

        random.shuffle(L_SHAPE_OFFSETS)

        for shape in L_SHAPE_OFFSETS:
            if all(0 <= x + dx < self.cols and 0 <= y + dy < self.rows and self.board[y + dy][x + dx] == 0 for dx, dy in shape):
                for dx, dy in shape:
                    self.board[y + dy][x + dx] = ship_id
                return True

        return False

    def reset_board(self) -> None:
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.attacked_positions.clear()

    def attack(self, x: int, y: int) -> int:
        if (x, y) in self.attacked_positions:
            raise ValueError(f"Position ({x}, {y}) has already been attacked.")

        self.attacked_positions.add((x, y))
        return self.board[y][x]

    def board_stats(self) -> dict:
        empty_spaces = sum(row.count(0) for row in self.board)
        occupied_spaces = self.rows * self.cols - empty_spaces
        return {"empty_spaces": empty_spaces, "occupied_spaces": occupied_spaces}