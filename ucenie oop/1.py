class Vehicle():
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

class Bus(Vehicle):
    def __init__(self, capacity):
        self.capacity = capacity

    def seating_cap(self, capacity):
        return ("The of:", self.name, "is", self.capacity)

