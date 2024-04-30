from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other: "Coordinate"):
        n_x = self.x + other.x
        n_y = self.y + other.y
        return Coordinate(n_x, n_y)

    def __eq__(self, other: "Coordinate"):
        return self.x == other.x and self.y == other.y
