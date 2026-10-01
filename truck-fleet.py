'''
We have a fleet of trucks with a capacity of 700 tons
and N items of cargo with sizes w_1, w_2... , w_N,
all weighing less than 700 tons. We want to determine
the minimum number of trucks needed to transport the N
items, bearing in mind that no single item can be split
across different trucks.
'''

from asyncio.windows_events import INFINITE


class P010:
    def __init__(self):
        self.C: int = 700
        self.V: list[int]
        self.A: dict[tuple[int, list[int]], int]

    def init(self, data: str):
        self.V = map(int, data.split())
        self.A = {}

    # Naive recursion
    def pdr(self, c: int, base: int, v: list[int]) -> int:
        if len(v) == 0:
            return 0

        tmp, best = 0, INFINITE
        top = len(v) - 1
        while top > base:
            v[base], v[top] = v[top], v[base]
            avail = c - v[base]
            if avail > 0:
                tmp = 1
            else:
                tmp = 0
                avail = self.C

            tmp += self.pdr(avail, base +1, v)
            if tmp < best:
                best = tmp
            v[top], v[base] = v[base], v[top]
            top -= 1

        return best

    # Recursion with storage
    def pdr_a(self, n: int) -> int:
        return 0

    # Iterative programming
    def pdi(self, n: int) -> int:
        return 0

    def best(self, s: str) -> int:
        self.init(s)
        return self.pdr(self.C, 0, self.V)
        #return self.pdr_a(self.N)
        #return self.pdi(self.N)

if __name__ == "__main__":
    p = P010()
    data = "300 300 340 360" # Needed: 2
    print(f'data: {data} best:', p.best(data))

    data = "600 200 500 100" # Needed: 
    print(f'data: {data} best:', p.best(data))
