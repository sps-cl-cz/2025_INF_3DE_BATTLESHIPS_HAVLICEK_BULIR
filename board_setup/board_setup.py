import random

class BoardSetup:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
    
    def get_board(self) -> list[list[int]]:
        return self.board
    
    def get_tile(self, x: int, y: int) -> int:
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return self.board[y][x]
        else:
            raise IndexError("Coordinates out of bounds.")
    def place_ships(self) -> None:
        def is_valid_placement(x, y, length, horizontal):
            if horizontal:
                if x + length > self.cols:
                    return False
                for i in range(length):
                    if self.board[y][x + i] != 0 or not is_space_free(x + i, y):
                        return False
            else:
                if y + length > self.rows:
                    return False
                for i in range(length):
                    if self.board[y + i][x] != 0 or not is_space_free(x, y + i):
                        return False
            return True
        
        def is_space_free(x, y):
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows and self.board[ny][nx] != 0:
                    return False
            return True
        
        for ship_id, count in self.ships_dict.items():
            for _ in range(count):
                placed = False
                while not placed:
                    x = random.randint(0, self.cols - 1)
                    y = random.randint(0, self.rows - 1)
                    horizontal = random.choice([True, False])
                    if is_valid_placement(x, y, ship_id, horizontal):
                        for i in range(ship_id):
                            if horizontal:
                                self.board[y][x + i] = ship_id
                            else:
                                self.board[y + i][x] = ship_id
                        placed = True
        
    def reset_board(self) -> None:
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
    
    def board_stats(self) -> dict:
        empty_spaces = sum(row.count(0) for row in self.board)
        occupied_spaces = self.rows * self.cols - empty_spaces
        return {"empty_spaces": empty_spaces, "occupied_spaces": occupied_spaces}