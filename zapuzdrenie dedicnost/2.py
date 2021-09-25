class A:
    def __init__(self, number: float) -> None:
        self._number: float = number
    
    def get_number(self):
        return self._number * self._number


class B(A):
    def __init__(self, number: float, constant: float) -> None:
        super().__init__(number)

        self._constant = constant
    
    def get_number(self):
        return super().get_number() * self._constant
    
print(B(10, 5).get_number())