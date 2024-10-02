# title: 6
# aim: Program to implement Tower of Hanoi using Python.


class TowerOfHanoi:
    def __init__(self, n):
        self.n = n

    def solve(self, n=None, source="A", target="C", auxiliary="B"):
        if n is None:
            n = self.n
        if n == 1:
            print(f"Move disk 1 from {source} to {target}")
            return
        self.solve(n - 1, source, auxiliary, target)
        print(f"Move disk {n} from {source} to {target}")
        self.solve(n - 1, auxiliary, target, source)


hanoi = TowerOfHanoi(3)
hanoi.solve()
