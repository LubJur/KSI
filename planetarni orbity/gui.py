from typing import List, Optional

from gravity import Body, calculate_system_energy
from initial_states import solar_bodies, n_nary_stable_system
from point import Point, Vector

SCALE = 10**9


# Todo: Implement GUI and the simulation itself.


if __name__ == '__main__':
    # Example 1 of initial planetary states
    # step_size = 10 ** 7  # seconds;
    bodies = n_nary_stable_system(3, scale=SCALE, screen_size=(400, 400))

    # Example 2 of initial planetary states
    # step_size = 10 ** 5  # seconds; The solar system simulation needs to be simulated with smaller steps to avoid massive errors.
    # bodies = solar_bodies(only_first_n_planets=4)

    for x in bodies:
        print(x)

    # Beware this is negative. Only check the % difference from the initial state.
    initial_energy_level = calculate_system_energy(bodies)