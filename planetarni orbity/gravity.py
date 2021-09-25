import math
from typing import List

from point import Point, Vector

GRAVITATION_CONSTANT = 6.67430 * 10**(-11)


class Body:
    def __init__(self,
                 location: Point,
                 mass: float,
                 motion_vector: Vector,
                 name: str):

        self.location = location  # location x, y in meters
        self.mass = mass  # mass in kilograms
        self.motion_vector = motion_vector  # motion vector x,y in meters per second
        self.name = name

    def __str__(self):
        return f"{self.name.ljust(20)}: Location {self.location}; Mass: {round(self.mass, 2)}; Motion vector: {self.motion_vector}"

    __repr__ = __str__

    # todo: implement the movement



# --- The following functions are not for the movement itself, but just for validation that the law of conservation of energy roughly holds. ---

def calculate_system_energy(bodies: List[Body]) -> float:
    """
        System energy level is kinetic + potential energy, BUT BEWARE!
        IT CAN BE (and often is) NEGATE. It's not meant as an absolute level of energy. Use it only in comparison with
        previously returned values - for example with the initial state.
    """
    kinetic_energy = __calculate_kinetic_energy(bodies)
    potential_energy = __calculate_potential_energy(bodies)  # This is negative.
    total_energy = kinetic_energy + potential_energy
    return total_energy


def __calculate_kinetic_energy(bodies: List[Body]) -> float:
    def kinetic_energy(body: Body):
        return 1/2 * body.mass * (body.motion_vector.x**2 + body.motion_vector.y**2)  # 1/2 * m * v**2

    return sum([kinetic_energy(x) for x in bodies])


def __calculate_potential_energy(bodies: List[Body]) -> float:
    """
        Beware that this is a negative number.
        Partial explanation is for example here:
        https://physics.stackexchange.com/questions/17082/why-is-gravitational-potential-energy-negative-and-what-does-that-mean
    """
    total_potential_energy = 0
    for a in range(len(bodies)):
        for b in range(a + 1, len(bodies)):
            distance = bodies[a].location.distance(bodies[b].location)
            new_potential_energy = - 1 * GRAVITATION_CONSTANT * (bodies[a].mass * bodies[b].mass) * (1.0/distance)
            total_potential_energy += new_potential_energy

    return total_potential_energy