from typing import Set


class Penguin:
    def __init__(self, name: str, age: int, name_id: int):
        self.name: str = name
        self.age: int = age
        self.name_id: int = name_id
        self.children: Set['Penguin'] = set()

    def add_children(self, child: 'Penguin'):
        self.children.add(child)

    def __eq__(self, __o) -> bool:
        return __o.name == self.name and __o.name_id == len(self.children)

    def __hash__(self) -> int:
        return hash(self.name)

karlik = Penguin("Karlik", 15, 0)
print(karlik.children)