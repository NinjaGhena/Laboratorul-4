from abc import ABC, abstractmethod
import random

class EntitateEcosistem(ABC):
    def __init__(self, nume, energie, pozitie_x, pozitie_y, rata_supravietuire):
        self.nume = nume
        self.energie = energie
        self.pozitie_x = pozitie_x
        self.pozitie_y = pozitie_y
        self.rata_supravietuire = rata_supravietuire

    @abstractmethod
    def actioneaza(self):
        pass

    def pozitie(self):
        return self.pozitie_x, self.pozitie_y

class Planta(EntitateEcosistem):
    def __init__(self, nume, pozitie_x, pozitie_y, rata_supravietuire):
        super().__init__(nume, energie=15, pozitie_x=pozitie_x, pozitie_y=pozitie_y, rata_supravietuire=rata_supravietuire)

    def actioneaza(self):
        self.energie += 2

    def reproduce(self):
        # Prag >20, cost 7 (intermediar)
        if self.energie > 20:
            self.energie -= 10
            return Planta(
                f"{self.nume}_copil",
                self.pozitie_x + random.randint(-1, 1),
                self.pozitie_y + random.randint(-1, 1),
                self.rata_supravietuire,
            )
        return None

class Animal(EntitateEcosistem):
    def __init__(self, nume, energie, pozitie_x, pozitie_y, rata_supravietuire, viteza, tip_hrana):
        super().__init__(nume, energie, pozitie_x, pozitie_y, rata_supravietuire)
        self.viteza = viteza
        self.tip_hrana = tip_hrana

    def deplaseaza(self):
        self.pozitie_x += random.randint(-self.viteza, self.viteza)
        self.pozitie_y += random.randint(-self.viteza, self.viteza)

    def actioneaza(self):
        self.deplaseaza()
        self.energie -= 1

    def mananca(self, prada):
        # Triplează beneficiul energetic pentru prăzi "corespunzătoare"
        if isinstance(self, Erbivor) and isinstance(prada, Planta):
            self.energie += prada.energie * 2.5
        elif isinstance(self, Carnivor) and isinstance(prada, Erbivor):
            self.energie += prada.energie * 2
        else:
            self.energie += prada.energie
        prada.energie = 0

    def reproduce(self):
        # Prag >40, cost 15, intermediar
        # Copilul va avea o energie scăzută (20), sub pragul de reproducere
        if self.energie > 45:
            self.energie -= 20
            copil_energie = 20
            if isinstance(self, Erbivor):
                copil = Erbivor(
                    f"{self.nume}_copil",
                    self.pozitie_x + random.randint(-1, 1),
                    self.pozitie_y + random.randint(-1, 1)
                )
                copil.energie = copil_energie
                return copil
            elif isinstance(self, Carnivor):
                copil = Carnivor(
                    f"{self.nume}_copil",
                    self.pozitie_x + random.randint(-1, 1),
                    self.pozitie_y + random.randint(-1, 1)
                )
                copil.energie = copil_energie
                return copil
        return None

class Erbivor(Animal):
    def __init__(self, nume, pozitie_x, pozitie_y):
        # Energie inițială 50, viteză 8
        super().__init__(nume, energie=40, pozitie_x=pozitie_x, pozitie_y=pozitie_y, rata_supravietuire=0.9, viteza=10, tip_hrana="plante")

class Carnivor(Animal):
    def __init__(self, nume, pozitie_x, pozitie_y):
        # Energie inițială 45, viteză 7
        super().__init__(nume, energie=40, pozitie_x=pozitie_x, pozitie_y=pozitie_y, rata_supravietuire=0.7, viteza=7, tip_hrana="animale")

    def actioneaza(self):
        self.deplaseaza()
        self.energie -= 0.5

def sunt_apropiate(poz1, poz2, raza=6):
    return abs(poz1[0] - poz2[0]) <= raza and abs(poz1[1] - poz2[1]) <= raza

class Ecosistem:
    def __init__(self, dimensiune_harta_x, dimensiune_harta_y):
        self.dimensiune_harta_x = dimensiune_harta_x
        self.dimensiune_harta_y = dimensiune_harta_y
        self.entitati = []

    def adauga_entitate(self, entitate):
        self.entitati.append(entitate)

    def elimina_entitate(self, entitate):
        if entitate in self.entitati:
            self.entitati.remove(entitate)

    def simuleaza_pas(self):
        for entitate in self.entitati[:]:
            entitate.actioneaza()
            if entitate.energie <= 0 and entitate in self.entitati:
                print(f"{entitate.nume} a murit din cauza energiei scăzute.")
                self.elimina_entitate(entitate)
                continue

            copil = entitate.reproduce()
            if copil:
                print(f"{entitate.nume} s-a reprodus, creând {copil.nume}!")
                self.adauga_entitate(copil)

            if isinstance(entitate, Erbivor):
                for planta in self.entitati[:]:
                    if isinstance(planta, Planta) and sunt_apropiate(entitate.pozitie(), planta.pozitie()):
                        print(f"{entitate.nume} mănâncă {planta.nume} (Plantă) cu un beneficiu mărit!")
                        entitate.mananca(planta)
                        if planta.energie <= 0 and planta in self.entitati:
                            self.elimina_entitate(planta)
                        break

            if isinstance(entitate, Carnivor):
                for prada in self.entitati[:]:
                    if isinstance(prada, Erbivor) and sunt_apropiate(entitate.pozitie(), prada.pozitie()):
                        print(f"{entitate.nume} atacă și mănâncă {prada.nume} (Erbivor) cu un beneficiu mărit!")
                        entitate.mananca(prada)
                        if prada.energie <= 0 and prada in self.entitati:
                            self.elimina_entitate(prada)
                        break

    def afiseaza_stare(self):
        print("\nStarea ecosistemului:")
        for entitate in self.entitati:
            print(f"{entitate.nume} ({entitate.__class__.__name__}) - Energie: {entitate.energie}, Pozitie: {entitate.pozitie()}")

if __name__ == "__main__":
    ecosistem = Ecosistem(100, 100)

    # Mai multe animale inițiale
    # Plante
    for i in range(7):
        ecosistem.adauga_entitate(Planta(f"Planta{i+1}", random.randint(0, 100), random.randint(0, 100), 0.8))

    # Mai multe erbivore inițiale
    for i in range(8):
        ecosistem.adauga_entitate(Erbivor(f"Iepure{i+1}", random.randint(0, 100), random.randint(0, 100)))

    # Mai multe carnivore inițiale
    for i in range(5):
        ecosistem.adauga_entitate(Carnivor(f"Lup{i+1}", random.randint(0, 100), random.randint(0, 100)))

    for pas in range(10):
        print(f"\nPASUL {pas + 1}")
        ecosistem.simuleaza_pas()
        ecosistem.afiseaza_stare()
