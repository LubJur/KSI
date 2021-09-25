class Person:
    def __init__(self, name: str) -> None:
        self.__name: str = name

    def get_name(self) -> str:
        return self.__name


class Student(Person):
    def __init__(self, name: str, student_id: int) -> None:
        super().__init__(name)

        self.__student_id: int = student_id

    def get_student_id(self) -> int:
        return self.__student_id

    def get_profile(self) -> str:
        return self.__name +  " " + str(self.get_student_id())