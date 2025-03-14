import random

class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict.copy()
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]
        self.remaining_positions = [(x, y) for y in range(rows) for x in range(cols)]

    def get_next_attack(self) -> tuple[int, int]:
        """
        Returns the next (x, y) coordinates to attack.
        Always selects randomly from untried positions.
        """
        if not self.remaining_positions:
            raise ValueError("No more available positions to attack.")

        # Extra safety check for corrupted state
        attack = None
        attempts = 0
        while not attack and attempts < 100:
            candidate = random.choice(self.remaining_positions)
            x, y = candidate
            if 0 <= x < self.cols and 0 <= y < self.rows:
                attack = candidate
            attempts += 1

        if attack is None:
            raise RuntimeError("Failed to find a valid attack position after 100 attempts.")

        self.remaining_positions.remove(attack)
        return attack

    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        """
        Records the result of an attack on the enemy board and updates ship tracking.
        """
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            raise ValueError(f"Attack out of bounds: ({x}, {y}).")

        if self.enemy_board[y][x] != '?':
            raise ValueError(f"Position ({x}, {y}) has already been attacked.")

        self.enemy_board[y][x] = 'H' if is_hit else 'M'

        if is_sunk:
            for ship_id in sorted(self.ships_dict.keys(), reverse=True):
                if self.ships_dict[ship_id] > 0:
                    self.ships_dict[ship_id] -= 1
                    break

    def get_enemy_board(self) -> list[list[str]]:
        """Returns the current known state of the enemy board."""
        return self.enemy_board

    def get_remaining_ships(self) -> dict[int, int]:
        """Returns a dictionary of remaining ships."""
        return self.ships_dict.copy()

    def all_ships_sunk(self) -> bool:
        """Checks if all ships are sunk."""
        return all(count == 0 for count in self.ships_dict.values())
