'''
In the two-player game of Nim, there are N tokens on the board,
and each player takes turns removing one or more tokens from the table,
up to a maximum of M. The game ends when no tokens remain
on the table, and the player whose turn it is—but who cannot
remove any tokens—loses.

This time it comes with a restriction, the immediate last play chosen
can't be played in the current turn.
'''

class NimGameRestricted:
    def __init__(self):
        self.N: int = 0
        self.M: int = 0
        self.A: dict[int, int] = {}

    def init(self, data: str):
        tokens = data.split()
        self.N = int(tokens[0])
        self.M = int(tokens[1])
        self.A = {}

    # Naive recursion
    def pdr(self, n: int, m: int) -> int:
        if n == 0 or (n == 1 and m == 1):
            return -1

        for k in range(1, min(n, self.M) + 1):
            if k != m and self.pdr(n - k, k) < 0:
                return k
        return -1

    # Recursion with storage
    def pdr_a(self, n: int, m: int) -> int:
        key = (n,m)
        if key in self.A:
            return self.A[key]

        if n == 0 or (n == 1 and m == 1):
            return -1

        res = -1
        for k in range(1, min(n, self.M) + 1):
            if k != m and self.pdr(n - k, k) < 0:
                res = k
                break

        self.A[key] = res
        return res

    # Iterative programming
    def pdi(self, n: int) -> int:
        A = {0: -1}

        for i in range(1, n + 1):
            res = -1
            for k in range(1, min(i, self.M) + 1):
                if A[i - k] < 0:
                    res = k
            A[i] = res

        return A[n]

    def best(self, s: str) -> bool:
        self.init(s)
        return self.pdr(self.N, 0)
        #return self.pdr_a(self.N)
        #return self.pdi(self.N)

if __name__ == "__main__":
    p = NimGameRestricted()
    data = "8 4" # Salida: 3
    print(f'data: {data} best:', p.best(data))

    data = "5 4" #Salida: -1
    print(f'data: {data} best:', p.best(data))

    data = "60 3"
    print(f'data: {data} best:', p.best(data))

