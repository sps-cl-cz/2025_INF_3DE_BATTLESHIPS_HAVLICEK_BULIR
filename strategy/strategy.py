import random

class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict.copy()
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]
        self.remaining_positions = [(x, y) for y in range(rows) for x in range(cols)]
        self.hit_positions = []  # Track hits for smarter targeting

    def get_next_attack(self) -> tuple[int, int]:
        """
        Returns the next (x, y) coordinates to attack.
        If there are previous hits, prioritize adjacent attacks.
        """
        if self.hit_positions:
            x, y = self.hit_positions[-1]
            neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < self.cols and 0 <= ny < self.rows and (nx, ny) in self.remaining_positions]
            if valid_neighbors:
                attack = random.choice(valid_neighbors)
                self.remaining_positions.remove(attack)
                return attack
        
        return self.remaining_positions.pop(random.randint(0, len(self.remaining_positions) - 1))

    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        """
        Records the result of an attack on the enemy board and updates ship tracking.
        """
        self.enemy_board[y][x] = 'H' if is_hit else 'M'
        
        if is_hit:
            self.hit_positions.append((x, y))
        
        if is_sunk:
            for ship_id in sorted(self.ships_dict.keys(), reverse=True):
                if self.ships_dict[ship_id] > 0:
                    self.ships_dict[ship_id] -= 1
                    break
            self.hit_positions.clear()  # Clear hits since ship is sunk
    
    def get_enemy_board(self) -> list[list[str]]:
        """Returns the current known state of the enemy board."""
        return self.enemy_board
    
    def get_remaining_ships(self) -> dict[int, int]:
        """Returns a dictionary of remaining ships."""
        return self.ships_dict.copy()

    def all_ships_sunk(self) -> bool:
        """Checks if all ships are sunk."""
        return all(count == 0 for count in self.ships_dict.values())