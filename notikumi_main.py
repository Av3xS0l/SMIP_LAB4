# 0 = bufera skaitlis
GAD_SK = [0, 0.957, 0.934, 0.564, 0.088, 0.464,
          0.822, 0.870, 0.077, 0.161, 0.042,
          0.711, 0.613, 0.301, 0.809, 0.504,
          0.886, 0.967, 0.984, 0.874, 0.798,
          0.616, 0.572, 0.077, 0.913, 0.797,
          0.637, 0.938, 0.023, 0.168, 0.194,
          0.209, 0.369, 0.405, 0.189, 0.679,
          0.509, 0.969, 0.861, 0.626, 0.610,
          0.336, 0.721, 0.613, 0.061, 0.919,
          0.674, 0.100, 0.777, 0.940, 0.101]


class N:
    def __init__(self):
        self.N = 0

    def get(self) -> int:
        self.N += 1
        return self.N


NUM = N()


class Rinda:
    def __init__(self) -> None:
        self.rinda = 0

    def push(self) -> None:
        self.rinda += 1

    def pull(self) -> bool:
        if self.rinda > 0:
            self.rinda -= 1
            return True
        return False


class Avots:
    global NUM

    def __init__(self, distrib: tuple[int, int], rinda: Rinda) -> None:
        # for distribution
        self.distrib = distrib
        self._size: float = 1 / (distrib[1] - distrib[0] + 1)

        self.rinda = rinda
        self.nextEventAt: int = 0
        self.busy: bool = False

    def _getTime(self) -> int:
        num = self.distrib[0] + (GAD_SK[NUM.get()] // self._size)
        return int(num)

    def run(self, t: int) -> int:
        if t != self.nextEventAt:
            return None

        if self.busy:
            self.rinda.push()

        self.nextEventAt = t+self._getTime()
        self.busy = True
        return NUM.N


class Kanals:
    def __init__(self, distrib: tuple[int, int], r1: Rinda, r2: Rinda) -> None:
        # for distribution
        self.distrib = distrib
        self._size: float = 1 / (distrib[1] - distrib[0] + 1)
        self.r1: Rinda = r1
        self.r2: Rinda = r2
        self.from1 = True
        self.nextEventAt: int = 0
        self.isWorking: bool = False
        self.apstr: int = 0

    def _getTime(self) -> int:
        num = self.distrib[0] + (GAD_SK[NUM.get()] // self._size)
        return int(num)

    def run(self, t: int) -> int:
        if self.nextEventAt > t:
            return None

        if self.isWorking:
            self.apstr += 1
            self.isWorking = False

        if self.from1:
            if self.r1.pull():
                self.isWorking = True
                self.nextEventAt = t + self._getTime()
                self.from1 = False
                return 1
            if self.r2.pull():
                self.isWorking = True
                self.nextEventAt = t + self._getTime()
                return 2
            return None
        else:
            if self.r2.pull():
                self.isWorking = True
                self.nextEventAt = t + self._getTime()
                self.from1 = True
                return 2
            if self.r1.pull():
                self.isWorking = True
                self.nextEventAt = t + self._getTime()
                return 1
            return None

# Notikumu tabulas izvadei - pašpārbaudei
def pprint(cur, old) -> None:
    if cur[0] != old[0]:
        print("├────┼────┼────┼────┼────┼────┼────┼────┼───┤")

    def fmt(X): return str(cur[X])+" " * \
        (2-len(str(cur[X]))) if (cur[X] != old[X]) and (cur[X] != None) else "  "

    last = str(cur[8]) if cur[8] != old[8] else " "
    row = (
        f"│ {fmt(0)} │ {fmt(1)} │ {fmt(2)} │ {fmt(3)} │ {fmt(4)} │ "
        f"{fmt(5)} │ {fmt(6)} │ {fmt(7)} │ {last} │"
    )
    print(row)


def main() -> None:
    R1 = Rinda()
    R2 = Rinda()
    A1 = Avots((3, 6), R1)
    A2 = Avots((4, 7), R2)
    K1 = Kanals((2, 6), R1, R2)
    t: int = 0
    MAX_APSTR: int = 5
    curent: list[int] = [None]*9
    old: list[int] = [None]*9

    print("┌────┬────┬────┬────┬────┬────┬────┬────┬───┐")
    print("│ t  │ n  │ A1 │ A2 │ K1 │ R1 │ R2 │ K1 │ N │")

    while (K1.apstr < MAX_APSTR):
        ek1 = K1.run(t)
        if ek1 != None:
            old = curent.copy()
            curent[0] = t
            curent[1] = NUM.N
            curent[4] = K1.nextEventAt
            curent[7] = int(K1.isWorking)
            curent[8] = K1.apstr
            if ek1 == 1:
                curent[5] = R1.rinda
            if ek1 == 2:
                curent[6] = R2.rinda

            pprint(curent, old)
        ea1 = A1.run(t)
        if ea1 != None:
            old = curent.copy()
            curent[0] = t
            curent[1] = NUM.N
            curent[2] = A1.nextEventAt
            curent[5] = R1.rinda

            pprint(curent, old)

        ea2 = A2.run(t)
        if ea2 != None:
            old = curent.copy()
            curent[0] = t
            curent[1] = NUM.N
            curent[3] = A2.nextEventAt
            curent[6] = R2.rinda

            pprint(curent, old)
        
        if (ek1 == None and (ea1 != None or ea2 != None)):
            ek2 = K1.run(t)
            if ek2 != None:
                old = curent.copy()
                curent[0] = t
                curent[1] = NUM.N
                curent[4] = K1.nextEventAt
                curent[7] = int(K1.isWorking)
                curent[8] = K1.apstr
                if ek2 == 1:
                    curent[5] = R1.rinda
                if ek2 == 2:
                    curent[6] = R2.rinda

                pprint(curent, old)

        t += 1
    print("└────┴────┴────┴────┴────┴────┴────┴────┴───┘")






if __name__ == "__main__":
    main()
