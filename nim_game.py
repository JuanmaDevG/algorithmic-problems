'''
In the two-player game of Nim, there are N tokens on the board,
and each player takes turns removing one or more tokens from the table,
up to a maximum of M. The game ends when no tokens remain
on the table, and the player whose turn it is—but who cannot
remove any tokens—loses.
'''

class P004:
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
    def pdr(self, n: int) -> int:
        if n <= 0:
            return -1

        res = -1
        for k in range(1, min(n, self.M) + 1):
            if self.pdr(n - k) < 0:
                res = k
        return res

    # Recursion with storage
    def pdr_a(self, n: int) -> int:
        if n <= 0:
            return -1

        if n in self.A:
            return self.A[n]

        res = -1
        for k in range(1, min(n, self.M) + 1):
            if self.pdr_a(n - k) < 0:
                res = k

        self.A[n] = res
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

    def best(self, s: str) -> int:
        self.init(s)
        #return self.pdr(self.N)
        #return self.pdr_a(self.N)
        return self.pdi(self.N)

if __name__ == "__main__":
    p = P004()
    data = "8 4" # Salida: 3
    print(f'data: {data} best:', p.best(data))

    data = "5 4" #Salida: -1
    print(f'data: {data} best:', p.best(data))

