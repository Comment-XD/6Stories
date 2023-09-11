class Weapon:
    def __init__(self, name, desc, dmg, range) -> None:
        self.name = name
        self.desc = desc
        self.dmg = dmg
        self.range = range

    def __str__(self) -> str:
        return self.name