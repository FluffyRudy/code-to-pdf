# title: 4
# aim: Program to implement Water-Jug problem using Python.


def water_jug(a, b, target):
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    if target > max(a, b) or target % gcd(a, b) != 0:
        print("Not possible")
        return

    x, y = 0, 0
    steps = []

    while x != target and y != target:
        if x == 0:
            x = a
            steps.append(f"Fill Jug A: ({x}, {y})")
        elif y == b:
            y = 0
            steps.append(f"Empty Jug B: ({x}, {y})")
        else:
            transfer = min(x, b - y)
            x -= transfer
            y += transfer
            steps.append(f"Transfer from A to B: ({x}, {y})")

    for step in steps:
        print(step)


water_jug(3, 5, 4)
