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
from typing import cast


class OptimalShoppingList:
    def __init__(self):
        self.C: list[int] = []
        self.K: list[list[int]] = []

    def fill(self, data: list[str]):
        self.C.clear()
        self.K.clear()
        for k in data:
            k_iter: map[int] = map(int, k.split())
            self.C.append(next(k_iter))
            self.K.append(list(k_iter))

    def best_solution(self, data: list[str]) -> int:
        self.fill(data)
        return self.naive_recursive(self.K, self.C)

    def best_solution_klist(self, data: list[str]) -> list[int]:
        self.fill(data)
        return self.naive_recursive_klist(self.K, self.C)

    def optimistic_bonund(self, K: list[list[int]], i: int) -> int:
        """
        Relax restrictions, pretend that the travel is free
        """
        res = 0
        for prod in range(i, len(K[0])):
            res += min(k[prod] for k in K)
        return res

    def pessimistic_bound(self, k: list[int], i: int) -> int:
        """
        Buy the rest of the objects from the current supermarket
        """
        return sum(k[i:])

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
                (C[l] if k != l else 0) + v_l[i] + self.naive_recursive(K, C, i + 1, l),
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
            expected = (C[l] if k != l else 0) + v_l[i]
            current = accum + expected
            if current > best:
                continue
            if self.optimistic_bonund(K, i) > self.pessimistic_bound(v_l, i):
                continue
            # if optimistic_bound > pessimistic_bound: continue
            best = min(
                best,
                expected + self.branching_and_bounding(K, C, i + 1, l, current),
            )

        return best

    def naive_recursive_klist(
        self, K: list[list[int]], C: list[int], i: int = 0, k: int | None = None
    ) -> list[int]:
        if i >= len(K[0]):
            return []
        best: int | float = float("inf")
        next_k: int = 0
        for i_k, v_k in enumerate(K):
            if (p := C[i_k] if k is None or k != i_k else 0 + v_k[i]) < best:
                best = p
                next_k = i_k

        return [next_k + 1] + self.naive_recursive_klist(K, C, i + 1, next_k)
