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

    def complete_solution(self, t: int, w: list[int], base: int,
                          v: list[int]) -> list[int]:
        if base >= len(v):
            return []

        if (c, base, tuple(v[base:])) in self.A:
            return self.A[(c, base, tuple(v[base:]))]

        tmp, best = copy(w), [float('inf')] * (len(v) - base)
        top = base
        while top < len(v):
            v[base], v[top] = v[top], v[base]

            # TODO: how to stack lists
            tmp[base] -= v[base] # TODO: tmp[base] no, tmp[t] truck index
            if tmp[base] < 0:
                tmp[base] += v[base]
                w.append(self.C)
                tmp[base +1] -= v[base]
            elif tmp[base] == 0:
                tmp.append(self.C)

            tmp += self.complete_solution(tmp, base +1, v)
            if tmp < best:
                best = tmp

            # TODO: revert changes
            v[top], v[base] = v[base], v[top]
            top += 1

        self.A[(c, base, tuple(v[base:]))] = copy(w)
        return w

    def best(self, s: str) -> int | list[int]:
        self.init(s)
        #return self.pdr(self.C, 0, self.V)
        #return self.pdr_a(self.C, 0, self.V)
        #return self.pdi(self.N)
        return self.complete_solution(self.C, 0,
                                      self.V, [self.C])

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

