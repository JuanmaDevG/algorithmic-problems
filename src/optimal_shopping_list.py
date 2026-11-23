"""
In a cost-saving and expense-optimization context,
we want to minimize the total cost of acquiring N
necessary products, which can be purchased at any of
the K available supermarkets.

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

For the a solution function, parameters are:
  K: vector of supermarkets with product prices
  C: cost of traveling to a supermarket
  i: current product index
  k: current supermarket
"""

# problem id: P101
from itertools import islice
from typing import cast


class OptimalShoppingList:
    def __init__(self):
        self.C: list[int] = []
        self.K: list[list[int]] = []
        self.best: int

    def fill(self, data: list[str]):
        self.C.clear()
        self.K.clear()
        for k in data:
            k_iter: map[int] = map(int, k.split())
            self.C.append(next(k_iter))
            self.K.append(list(k_iter))
        self.best = cast(int, float("inf"))

    def best_solution(self, data: list[str]) -> int:
        self.fill(data)
        return self.naive_recursive(self.K, self.C)

    def best_solution_klist(self, data: list[str]) -> list[int]:
        self.fill(data)
        return []  # TODO: implement naive_recursive_klist and bounded later

    def travel_cost(self, C: list[int], current: int | None, next: int) -> int:
        return C[next] if current != next else 0

    def optimistic_bound(self, K: list[list[int]], i: int) -> int:
        """
        Assume the travel cost does not exist and take the minimum
        """
        res = 0
        for j in range(i, len(K[0])):
            best_price = cast(int, float("inf"))
            for k in K:
                best_price = min(best_price, k[j])
            res += best_price
        return res

    def pessimistic_bound(
        self, K: list[list[int]], C: list[int], k: int | None, i: int
    ) -> int:
        """
        Get the local minimum without branching, reaches suboptimal
        but feasible solution because computes current path minimum,
        not global minimum
        """
        best = 0
        cur = 0
        for prod in range(i, len(K[0])):
            lprod_best: int = cast(int, float("inf"))
            for l in range(len(K)):
                cur = K[l][prod] + self.travel_cost(C, k, l)
                if cur < lprod_best:
                    lprod_best = cur
                    k = l
            best += lprod_best
        return best

    # ------------- Implementations -------------

    def naive_recursive(
        self, K: list[list[int]], C: list[int], i: int = 0, k: int | None = None
    ) -> int:
        if i >= len(K[0]):
            return 0
        best: int = cast(int, float("inf"))
        for l, v_l in enumerate(K):
            best = min(
                best,
                self.travel_cost(C, k, l)
                + v_l[i]
                + self.naive_recursive(K, C, i + 1, l),
            )

        return best

    def branching_and_bounding(
        self,
        K: list[list[int]],
        C: list[int],
        i: int = 0,
        k: int | None = None,
        accum: int = 0,
    ) -> int:
        if i >= len(K[0]):
            self.best = min(self.best, accum)
            return accum

        ob = accum + self.optimistic_bound(K, i)
        if self.best <= ob:
            return cast(int, float("inf"))
        pb = accum + self.pessimistic_bound(K, C, k, i)
        if ob == pb:
            self.best = min(self.best, ob)
            return self.best

        for l, v_l in enumerate(K):
            expected = v_l[i] + self.travel_cost(C, k, l)
            _ = self.branching_and_bounding(K, C, i + 1, l, accum + expected)

        return self.best

    def bnb_sorted_branches(
        self,
        K: list[list[int]],
        C: list[int],
        i: int = 0,
        k: int | None = None,
        accum: int = 0,
    ):
        if i >= len(K[0]):
            return 0
        best: int = cast(int, float("inf"))
        # TODO: branches must be ordered by the optimistic bound, not like this
        branches: list[int] = [
            K[l][i] + self.travel_cost(C, k, l) for l in range(len(K))
        ]
        branches.sort()

        # TODO: explore the best branches first
        for expected in branches:
            pass

        return best

    def naive_recursive_klist(self) -> list[int]:
        return []
