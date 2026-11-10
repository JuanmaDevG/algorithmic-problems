"""
We have a fleet of trucks with a capacity of 700 tons
and N items of cargo with sizes w_1, w_2... , w_N,
all weighing less than 700 tons. We want to determine
the minimum number of trucks needed to transport the N
items, bearing in mind that no single item can be split
across different trucks.
"""

from copy import copy


class TruckFleet:
    def __init__(self):
        self.C: int = 700
        self.V: list[int] = []
        self.A: dict[tuple[int, int, tuple[int, ...]], int | float] = {}
        self.A_L: dict[tuple[int, int, tuple[int, ...]], list[int]] = {}

    def init(self, data: str):
        self.V.clear()
        self.V.extend(map(int, data.split()))
        self.A.clear()
        self.A_L.clear()

    # Naive recursion
    def pdr(self, c: int, base: int, v: list[int]) -> int | float:
        if base >= len(v):
            if c < self.C:
                return 1
            else:
                return 0

        tmp, best = 0, float("inf")
        top = base
        while top < len(v):
            v[base], v[top] = v[top], v[base]
            avail = c - v[base]
            if avail >= 0:
                tmp = 0
            else:
                tmp = 1
                avail = self.C - v[base]

            tmp += self.pdr(avail, base + 1, v)
            best = min(tmp, best)
            v[top], v[base] = v[base], v[top]
            top += 1

        return best

    # Recursion with memory
    def pdr_a(self, c: int, base: int, v: list[int]) -> int | float:
        if base >= len(v):
            if c < self.C:
                return 1
            else:
                return 0

        if (c, base, tuple(v[base:])) in self.A:
            return self.A[(c, base, tuple(v[base:]))]

        tmp, best = 0, float("inf")
        top = base
        while top < len(v):
            v[base], v[top] = v[top], v[base]
            avail = c - v[base]
            if avail >= 0:
                tmp = 0
            else:
                tmp = 1
                avail = self.C - v[base]

            tmp += self.pdr_a(avail, base + 1, v)
            best = min(best, tmp)
            v[top], v[base] = v[base], v[top]
            top += 1

        self.A[(c, base, tuple(v[base:]))] = best
        return best

    def loadvec_solution(self, base: int, v: list[int], w: list[int]) -> list[int]:
        if base == len(v) - 1:
            loaded = w[-1] + v[base]
            if loaded > self.C:
                return w + [v[base]]
            else:
                ret = copy(w)
                ret[-1] = loaded
                return ret

        key = (w[-1], base, tuple(sorted(v[base:])))
        if key in self.A:
            return self.A_L[key]

        nbest, best_result = float("inf"), []
        top = base

        while top < len(v):
            v[base], v[top] = v[top], v[base]

            loaded = w[-1] + v[base]
            if loaded > self.C:
                wtmp = w + [v[base]]
            else:
                wtmp = w[:-1] + [loaded]

            result = self.loadvec_solution(base + 1, v, wtmp)
            if len(result) < nbest:
                best_result = result
                nbest = len(best_result)

            v[top], v[base] = v[base], v[top]
            top += 1

        self.A_L[key] = best_result
        return best_result

    # Return vector of truck indices (+ branching and bounding)
    def indexed_solution(
        self, c: int, base: int, v: list[int], w: list[int], truck: int = 1
    ) -> list[int]:
        if base == len(v) - 1:
            avail = c - v[base]
            if avail < 0:
                w[base] = truck + 1
                return w
            else:
                w[base] = truck
                return w

        key = (c, base, tuple(w[base:]))
        if key in self.A:
            return self.A_L[key]

        best, least = [], float("inf")
        for top in range(base, len(v)):
            v[base], v[top] = v[top], v[base]
            w[base], w[top] = w[top], w[base]
            avail = c - v[base]
            if avail < 0:
                cur_truck = truck + 1
                avail = self.C - v[base]
            else:
                cur_truck = truck

            if cur_truck >= least:
                v[top], v[base] = v[base], v[top]
                continue
            tmp = copy(w)
            tmp[base] = cur_truck

            result = self.indexed_solution(avail, base + 1, v, tmp, cur_truck)
            if max(result) < least:
                best = result
                least = max(result)
            v[top], v[base] = v[base], v[top]
            w[top], w[base] = w[base], w[top]

        self.A_L[key] = best
        return best

    def best_solution(self, s: str) -> int | float | list[int]:
        self.init(s)
        # return self.pdr(self.C, 0, self.V)
        # return self.pdr_a(self.C, 0, self.V)
        # return self.loadvec_solution(0, self.V, [0])
        return self.indexed_solution(self.C, 0, self.V, [0] * len(self.V), 1)
