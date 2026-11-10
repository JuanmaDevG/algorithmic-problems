from collections.abc import Callable
from typing import override
import unittest

from truck_fleet import TruckFleet


class TestTruckFleet(unittest.TestCase):
    @override
    @classmethod
    def setUpClass(cls) -> None:
        cls.tf: TruckFleet = TruckFleet()
        cls.cases: list[tuple[list[int], int]] = [
            ([400, 400, 300, 300, 300, 300, 100], 3),
            ([600, 600, 600, 100, 100, 100, 100], 4),
            ([500, 500, 500, 500, 200, 200, 200], 4),
            ([233, 233, 233, 233, 233, 233, 2], 3),
            ([699, 350, 350, 1, 1, 1, 1], 3),
            ([698, 698, 698, 2, 2, 2, 2], 4),
            ([350, 350, 350, 350, 350, 349, 349], 4),
            ([699, 698, 697, 1, 2, 3, 4], 4),
            ([699, 699, 699, 1, 1, 1, 1], 4),
            ([250, 250, 250, 2, 50, 200, 200, 200], 3),
        ]

    def validate_callback(
        self, callback: Callable[[int, int, list[int]], int | float | list[int]]
    ):
        for c in self.cases:
            self.assertEqual(callback(self.tf.C, 0, c[0]), c[1])

    def test_01_naive_recursion(self):
        self.validate_callback(self.tf.pdr)

    def test_02_mem_recursion(self):
        self.validate_callback(self.tf.pdr_a)

    def test_03_loadvec_solution(self):
        pass  # TODO: make test cases

    def test_04_indexed_solution(self):
        pass  # TODO: make test cases


if __name__ == "__main__":
    _ = unittest.main()
