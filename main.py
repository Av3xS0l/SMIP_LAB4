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

def center(val: int|str, size: int) -> str:
    spaces = size - len(str(val))
    return f"{" "*(spaces-(spaces//2))}{val}{" "*(spaces//2)}"

class N:
    def __init__(self):
        self.N = 0

    def get(self) -> int:
        self.N += 1
        return self.N


NUM = N()


class Rinda:
    def __init__(self) -> None:
        self.rinda: int = 0
        self.accSize: int = 0
        self.ienak: int = 0

    def push(self) -> None:
        self.ienak += 1
        self.rinda += 1

    def pull(self) -> bool:
        if self.rinda > 0:
            self.rinda -= 1
            return True
        return False

    def updateAcc(self) -> None:
        self.accSize += self.rinda


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
        self.t_start: int = -1

    def _getTime(self) -> int:
        num = self.distrib[0] + (GAD_SK[NUM.get()] // self._size)
        return int(num)

    def run(self, t: int) -> int:
        if self.nextEventAt > t:
            return None

        if self.isWorking:
            self.apstr += 1
            self.isWorking = False
        else:
            self.t_start = t  # pirmā pieprasījuma apstrādes uzsākšanas moments

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


def main() -> None:
    R1 = Rinda()
    R2 = Rinda()
    A1 = Avots((3, 6), R1)
    A2 = Avots((4, 7), R2)
    K1 = Kanals((2, 6), R1, R2)
    t: int = 0
    MAX_APSTR: int = 5

    while (K1.apstr < MAX_APSTR):
        ek1 = K1.run(t)
        ea1 = A1.run(t)
        ea2 = A2.run(t)
        if (ek1 == None and (ea1 != None or ea2 != None)):
            K1.run(t)
        R1.updateAcc()
        R2.updateAcc()
        t += 1

    # Izvada modelēšanas rezultātus tabulas formātā

    t = t - 1  # Pēdējais cikls palielināja t pēc pabeigšanas.
    RESULTS: list[tuple[str,int|float]] = []
    RESULTS.append(("L1", R1.accSize / t ))
    RESULTS.append(("T1", R1.accSize / R1.ienak))
    RESULTS.append(("L2", R2.accSize / t))
    RESULTS.append(("T2", R2.accSize / R2.ienak))
    RESULTS.append(("N1", (t - K1.t_start) / t))
    RESULTS.append(("Modelēšanas laiks", t))
    RESULTS.append(("Izmantotie gadījuma skaitļi", NUM.N-1))

    MAX_WIDTH = max([len(x[0]) for x in RESULTS])+2
    print(f"┌{"─"*MAX_WIDTH}┬───────┐")
    for i, item in enumerate(RESULTS):

        key, val = item
        if type(val) == float:
            print(f"│{center(key, MAX_WIDTH)}│ {center(format(val, ".3f"),5)} │")
        else:
            print(f"│{center(key,MAX_WIDTH)}│ {center(val,5)} │")
        if i+1 != len(RESULTS): print(f"├{"─"*MAX_WIDTH}┼───────┤")

    print(f"└{"─"*MAX_WIDTH}┴───────┘")
   

    


if __name__ == "__main__":
    main()
