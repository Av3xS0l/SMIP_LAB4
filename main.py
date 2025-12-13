# Patriks Gustavs Rinkevičs

# Sākuma gadījuma skaitļu tabula
# 0tajā pozīcijā 0, lai būtu vienkāršāka indeksācija
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


# palīgfunkcija teksta centrēšanai
def center(val: int|str, size: int) -> str:
    spaces = size - len(str(val))
    return f"{" "*(spaces-(spaces//2))}{val}{" "*(spaces//2)}"


# Klase, kas uztur izmantoto gadījuma skaitļu skaitu
class N:
    def __init__(self):
        self.N = 0

    def get(self) -> int:
        self.N += 1
        return self.N

# Gadījuma skaitļu skaitītājs
NUM = N()

# Rindas implementācija
class Rinda:
    def __init__(self) -> None:
        self.rinda: int = 0     # Rindas garums
        self.accSize: int = 0   # Rindas akmulētais garums
        self.ienak: int = 0     # Rindā ienākušo pieprasījumu skaits

    # Elementa ienākšana rindā
    def push(self) -> None:
        self.ienak += 1
        self.rinda += 1

    # Elementa iziešana no rindas
    def pull(self) -> bool:
        if self.rinda > 0:
            self.rinda -= 1
            return True
        return False

    # Rindas "laukuma" akmulēšana 
    def updateAcc(self) -> None:
        self.accSize += self.rinda

# Visi gadījuma skaitļu sadalījumu aprēķini
class Sadalijums:
    def __init__(self, distrib: tuple[int,int]):
        self.distrib: tuple[int, int] = distrib
        self._size: float = 1 / (distrib[1] - distrib[0] + 1)
    
    # Funkcija nepieciešamā laika iegūšanai no gadījuma skaitļu tabulas
    def _getTime(self) -> int:
        num = self.distrib[0] + (GAD_SK[NUM.get()] // self._size)
        return int(num)

# Avota implementācija
class Avots(Sadalijums):
    def __init__(self, distrib: tuple[int, int], rinda: Rinda) -> None:
        super().__init__(distrib)

        self.rinda = rinda          # Rinda, kurā padod elementus
        self.nextEventAt: int = 0   # Nākamā notikuma laiks
        self.busy: bool = False     # Vai šobrīd gaida nākamo notikumu (nepieciešams 1. pieprasījuma pareizai apstrādei)

    # Pārbaude laika momentā t
    def run(self, t: int) -> int:
        # Vai ir sasniedzis nākamo notikumu?
        if t != self.nextEventAt:
            return None

        # Nav pirmais elements
        if self.busy:
            self.rinda.push()

        self.nextEventAt = t+self._getTime()    # Iegūst nākamā notikuma laiku
        self.busy = True
        return NUM.N

# Pieprasījumu apstrādes kanāla 
class Kanals(Sadalijums):
    def __init__(self, distrib: tuple[int, int], r1: Rinda, r2: Rinda) -> None:
        super().__init__(distrib)


        self.r1: Rinda = r1             # Pirmā rinda no kuras iegūst pieprasījumus
        self.r2: Rinda = r2             # Otrā rinda no kuras iegūst pieprasījumus
        self.from1 = True               # Jāsaņem nākamais pieprasījums no 1. rindas
        self.nextEventAt: int = 0       # Nākamā pieprasījuma apstrādes laiks
        self.isWorking: bool = False    # Pašlaik apstrādā pieprasījumu
        self.apstr: int = 0             # Apstrādāto pieprasījumu skaits
        self.t_start: int = -1          # 1. Pieprasījuma apstrādes sākuma laiks | -1 -> Nav apstrādāts neviens notikums

    # Pārbaude laika momentā t
    def run(self, t: int) -> int:
        # Vai ir pienācis nākamais notikums
        if self.nextEventAt > t:
            return None

        if self.isWorking:
            self.apstr += 1
            self.isWorking = False
        else:
            self.t_start = t  # pirmā pieprasījuma apstrādes uzsākšanas moments

        # Pārbauda vai rindā ir pieprasījums, kuru apstrādāt
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
    # Objektu izveide
    R1 = Rinda()
    R2 = Rinda()
    A1 = Avots((3, 6), R1)
    A2 = Avots((4, 7), R2)
    K1 = Kanals((2, 6), R1, R2)
    t: int = 0                  # Laika moments
    MAX_APSTR: int = 5          # Nepieciešamais apstrādāto pieprasījumu skaits

    # Darbību secība:
    # 1. Pārbauda vai K1 nepieciešams apstrādāt pieprasījumu
    # 2. Pārbauda vai A1 nepieciešams radīt pieprasījumu
    # 3. Pārbauda vai A2 nepieciešams radīt pieprasījumu
    # 4. Ja K1 vēl nav apstrādājis pieprsaījumu un A1 vai A2 ir ģenerējis pieprasījumu:
    #     > Vēlreiz pārbauda K1
    # 5. Atjauno rindu apstrādāto pieprasījumu skaitu.
    # 6. Palielina laiku par 1

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

    # Aprēķina platākā elementa platumu
    MAX_WIDTH = max([len(x[0]) for x in RESULTS])+2

    # Rezultātu izvade uz ekrāna
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
