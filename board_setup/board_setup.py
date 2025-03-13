import random

class BoardSetup:
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
        """
        for ship_id, count in self.ships_dict.items():
            for _ in range(count):
                placed = False
                while not placed:
                    x = random.randint(0, self.cols - 1)
                    y = random.randint(0, self.rows - 1)
                    horizontal = random.choice([True, False])

                    if horizontal:
                        if x + ship_id <= self.cols and all(self.board[y][x + i] == 0 for i in range(ship_id)):
                            for i in range(ship_id):
                                self.board[y][x + i] = ship_id
                            placed = True
                    else:
                        if y + ship_id <= self.rows and all(self.board[y + i][x] == 0 for i in range(ship_id)):
                            for i in range(ship_id):
                                self.board[y + i][x] = ship_id
                            placed = True

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