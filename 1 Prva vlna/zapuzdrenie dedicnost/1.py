from typing import List


class Animal:
    def make_sound(self) -> str:
        return "sound"


class Cat(Animal):
    def make_sound(self) -> str:
        return "meow"


class Garfield(Cat):
    def __init__(self):
        self.__favorite_food = "lasagne"


animals: List[Animal] = [Cat(), Animal(), Garfield()]

sounds = ""

for animal in animals:
    sounds += animal.make_sound() + " "

print(sounds)