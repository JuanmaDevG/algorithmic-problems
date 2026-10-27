import unittest

from nim_game import NimGame


class TestNimGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.game = NimGame()

    def test_okay_value(self) -> None:
        self.assertEqual(self.game.best("8 4"), 3)

    def test_no_solution_value(self) -> None:
        self.assertEqual(self.game.best("5 4"), -1)


if __name__ == "__main__":
    unittest.main()
