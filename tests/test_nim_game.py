import unittest
from typing import override

from nim_game import NimGame


class TestNimGame(unittest.TestCase):
    @override
    @classmethod
    def setUpClass(cls) -> None:
        cls.game: NimGame = NimGame()

    def test_01_okay_value(self) -> None:
        self.assertEqual(self.game.best("8 4"), 3)

    def test_02_no_solution_value(self) -> None:
        self.assertEqual(self.game.best("5 4"), -1)


if __name__ == "__main__":
    _ = unittest.main()
