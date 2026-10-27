import unittest

from nim_game_restricted import NimGameRestricted


class TestNimGameRestricted(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.nim = NimGameRestricted()

    def test_ok_params(self) -> None:
        self.assertEqual(self.nim.best("8 4"), 3)

    def test_nosolution_params(self) -> None:
        self.assertEqual(self.nim.best("5 4"), -1)


if __name__ == "__main__":
    unittest.main()
