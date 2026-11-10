import unittest
from typing import override

from nim_game_restricted import NimGameRestricted


class TestNimGameRestricted(unittest.TestCase):
    @override
    @classmethod
    def setUpClass(cls) -> None:
        cls.nim: NimGameRestricted = NimGameRestricted()

    def test_01_ok_params(self) -> None:
        self.assertEqual(self.nim.best("8 4"), 3)

    def test_02_nosolution_params(self) -> None:
        self.assertEqual(self.nim.best("5 4"), -1)


if __name__ == "__main__":
    _ = unittest.main()
