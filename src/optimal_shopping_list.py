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
        self.best_pb: int

    def fill(self, data: list[str]):
        self.C.clear()
        self.K.clear()
        for k in data:
            k_iter: map[int] = map(int, k.split())
            self.C.append(next(k_iter))
            self.K.append(list(k_iter))
        self.best_pb = cast(int, float("inf"))
        # TODO: self.known_pbs: dict[(k, i)] (would it even work?)

    def best_solution(self, data: list[str]) -> int:
        self.fill(data)
        return self.naive_recursive(self.K, self.C)

    def best_solution_klist(self, data: list[str]) -> list[int]:
        self.fill(data)
        return []  # TODO: implement naive_recursive_klist and bounded later

    def travel_cost(self, C: list[int], current: int | None, next: int) -> int:
        return C[next] if current != next else 0

    def optimistic_bonund(self, K: list[list[int]], i: int) -> int:
        """
        Assume the travel cost does not exist and take the minimum
        """
        return min(sum(islice(k, i, len(k))) for k in K)

    def pessimistic_bound(
        self, K: list[list[int]], C: list[int], k: int, i: int
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
            best += best
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
            return 0
        best: int = cast(int, float("inf"))

        for l, v_l in enumerate(K):
            ob = accum + self.optimistic_bonund(K, i)
            if best <= ob:
                continue
            pb = accum + self.pessimistic_bound(K, C, l, i)
            if self.best_pb <= pb:
                continue
            else:
                self.best_pb = pb
            expected = v_l[i] + self.travel_cost(C, k, l)
            best = min(
                best,
                expected
                + self.branching_and_bounding(K, C, i + 1, l, accum + expected),
            )

        return best

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
        branches: list[int] = [
            K[l][i] + self.travel_cost(C, k, l) for l in range(len(K))
        ]
        branches.sort()

        # TODO: explore the best branches first
        for expected in branches:
            pass

        # TODO: trash this loop later
        for l, v_l in enumerate(K):
            ob = accum + self.optimistic_bonund(K, i)
            if best <= ob:
                continue
            pb = accum + self.pessimistic_bound(K, C, l, i)
            if self.best_pb <= pb:
                continue
            else:
                self.best_pb = pb
            expected = self.travel_cost(C, k, l) + v_l[i]
            best = min(
                best,
                expected
                + self.branching_and_bounding(K, C, i + 1, l, accum + expected),
            )

        return best

    def naive_recursive_klist(self) -> list[int]:
        return []
