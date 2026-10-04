'''
We have a fleet of trucks with a capacity of 700 tons
and N items of cargo with sizes w_1, w_2... , w_N,
all weighing less than 700 tons. We want to determine
the minimum number of trucks needed to transport the N
items, bearing in mind that no single item can be split
across different trucks.
'''

from copy import copy

class P010:
    def __init__(self):
        self.C: int = 700
        self.V: list[int]
        self.A: dict[tuple[int, int, tuple[int, ...]], int]

    def init(self, data: str):
        self.V = list(map(int, data.split()))
        self.A = {}

    # Naive recursion
    def pdr(self, c: int, base: int, v: list[int]) -> int:
        if base >= len(v):
            if c < self.C:
                return 1
            else:
                return 0

        tmp, best = 0, float('inf')
        top = base
        while top < len(v):
            v[base], v[top] = v[top], v[base]
            avail = c - v[base]
            if avail >= 0:
                tmp = 0
            else:
                tmp = 1
                avail = self.C - v[base]

            tmp += self.pdr(avail, base +1, v)
            if tmp < best:
                best = tmp
            v[top], v[base] = v[base], v[top]
            top += 1

        return best

    # Recursion with memory
    def pdr_a(self, c: int, base: int, v: list[int]) -> int:
        if base >= len(v):
            if c < self.C:
                return 1
            else:
                return 0

        if (c, base, tuple(v[base:])) in self.A:
            return self.A[(c, base, tuple(v[base:]))]

        tmp, best = 0, float('inf')
        top = base
        while top < len(v):
            v[base], v[top] = v[top], v[base]
            avail = c - v[base]
            if avail >= 0:
                tmp = 0
            else:
                tmp = 1
                avail = self.C - v[base]

            tmp += self.pdr_a(avail, base +1, v)
            if tmp < best:
                best = tmp
            v[top], v[base] = v[base], v[top]
            top += 1

        self.A[(c, base, tuple(v[base:]))] = best
        return best

    # WARNING: NO iterative version, same but manual state stack
    def pdi(self, c: int, base: int, v: list[int]) -> int:
        if len(v) == 0:
            return 0
        if len(v) == 1:
            return 1

        if (c, base, tuple(v[base:])) in self.A:
            return self.A[(c, base, tuple(v[base:]))]

        tmp, best = 0, float('inf')
        top = base
        while top < len(v):
            v[base], v[top] = v[top], v[base]
            avail = c - v[base]
            if avail >= 0:
                tmp = 0
            else:
                tmp = 1
                avail = self.C - v[base]

            tmp += self.pdr_a(avail, base +1, v)
            if tmp < best:
                best = tmp
            v[top], v[base] = v[base], v[top]
            top += 1

        self.A[(c, base, tuple(v[base:]))] = best
        return best

    def loadvec_solution(self, base: int, v: list[int],
                          w: list[int]) -> list[int]:
        if base == len(v) -1:
            loaded = w[-1] + v[base]
            if loaded > self.C:
                return w + [v[base]]
            else:
                ret = copy(w)
                ret[-1] = loaded
                return ret

        key = (w[-1], base, tuple(sorted(v[base:])))
        if key in self.A:
            return self.A[key]

        nbest, best_result = float('inf'), []
        top = base

        while top < len(v):
            v[base], v[top] = v[top], v[base]

            loaded = w[-1] + v[base]
            if loaded > self.C:
                wtmp = w + [v[base]]
            else:
                wtmp = w[:-1] + [loaded]

            result = self.loadvec_solution(base +1, v, wtmp)
            if len(result) < nbest:
                best_result = result
                nbest = len(best_result)

            v[top], v[base] = v[base], v[top]
            top += 1

        self.A[key] = best_result
        return best_result

    # Return vector of truck indices
    def indexed_solution(self, c: int, base: int, v: list[int],
                         w: list[int], truck: int = 1) -> list[int]:
        if base == len(v) -1:
            avail = c - v[base]
            if avail < 0:
                w[base] = truck +1
                return w
            else:
                w[base] = truck
                return w

        key = (c, base, truck, tuple(v[base:]))
        if key in self.A:
            return self.A[key]

        best, least = [], float('inf')
        for top in range(base, len(v)):
            v[base], v[top] = v[top], v[base]
            tmp = copy(w)
            avail = c - v[base]
            if avail < 0:
                cur_truck = truck +1
                avail = self.C - v[base]
            else:
                cur_truck = truck
            tmp[base] = cur_truck

            result = self.indexed_solution(avail, base +1, v, tmp, cur_truck)
            if max(result) < least:
                best = result
                least = max(result)
            v[top], v[base] = v[base], v[top]

        self.A[(c, base, tuple(v[base:]))] = best
        return best

    def best(self, s: str) -> int | list[int]:
        self.init(s)
        #return self.pdr(self.C, 0, self.V)
        #return self.pdr_a(self.C, 0, self.V)
        #return self.pdi(self.N)
        #return self.loadvec_solution(0, self.V, [0])
        return self.indexed_solution(self.C, 0, self.V, [0] * len(self.V), 1)

if __name__ == "__main__":
    p = P010()
    for case in [
        "400 400 300 300 300 300 100",  # Needed: 3
        "600 600 600 100 100 100 100",  # Needed: 4
        "500 500 500 500 200 200 200",  # Needed: 4
        "233 233 233 233 233 233 2",    # Needed: 3
        "699 350 350 1 1 1 1",          # Needed: 3
        "698 698 698 2 2 2 2",          # Needed: 4
        "350 350 350 350 350 349 349",  # Needed: 4
        "699 698 697 1 2 3 4",          # Needed: 4
        "699 699 699 1 1 1 1",          # Needed: 4
        "250 250 250 250 200 200 200",  # Needed: 3
    ]:
        print(f'data: {case} best:', p.best(case))

