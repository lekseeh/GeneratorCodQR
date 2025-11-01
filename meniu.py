import random


class Meniu:
    def __init__(self, nume, pret):
        self.nume = nume
        self.pret = pret


class FelPrincipal(Meniu):
    pass


class FelSecundar(Meniu):
    pass


class Desert(Meniu):
    pass


fel_principal = [
    FelPrincipal("Ciorba de fasole", 15),
    FelPrincipal("Supa de pui", 15),
]

fel_secundar = [
    FelSecundar("Cartofi prajiti cu piept de pui", 21),
    FelSecundar("Orez cu legume", 23),
]

desert = [
    Desert("Tiramisu", 11),
    Desert("Inghetata", 8),
]


def meniu_aleatoriu():
    fp = random.choice(fel_principal)
    fs = random.choice(fel_secundar)
    d = random.choice(desert)
    total = fp.pret + fs.pret + d.pret
    return fp, fs, d, total
