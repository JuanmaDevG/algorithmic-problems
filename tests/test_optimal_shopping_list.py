import unittest
from typing import override

from optimal_shopping_list import OptimalShoppingList


class TestOptimalShoppingList(unittest.TestCase):
    @override
    @classmethod
    def setUpClass(cls):
        cls.osl: OptimalShoppingList = OptimalShoppingList()

    def test_01_list_naive_recursive(self):
        pass

    def test_02_mem_recursion(self):
        pass


if __name__ == "__main__":
    _ = unittest.main()
