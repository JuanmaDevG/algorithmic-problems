"""
Problem: In a cost-saving and expense-optimization
context, we want to minimize the total cost of
acquiring N necessary products, which can be
purchased at any of the K available supermarkets.

Each supermarket k has the following characteristics:
  - Fixed travel cost (c_k): every time we decide to
    buy at a supermarket, we must assume a fixed cost
    associated with traveling there. This cost is paid
    only once per supermarket, regardless of the
    number of products we buy there. Therefore, if we
    purchase several products at the same store, they
    are all bought in a single trip.
  - Product prices (p_ki): each supermarket offers a
    specific price for each product i, which may vary
    between stores.

Objective: determine which products should be
purchased at each supermarket to minimize the total
purchase cost, taking into account both the individual
prices of the products and the fixed travel costs to
the selected supermarkets.
"""


# problem id: P101
class OptimalShoppingList:
    def __init__(self):
        self.C: list[int] = []
        self.K: list[list[int]] = []

    def fill(self, data: list[str]):
        self.C.clear()
        self.K.clear()
        for market in data:
            m_iter: map[int] = map(int, market.split())
            self.C.append(next(m_iter))
            self.K.append(list(m_iter))

    def best_solution(self, data: list[str]) -> list[int]:
        return []
