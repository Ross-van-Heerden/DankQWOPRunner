import Individual
import Population

import time


class Master:
    """ This class controls the Population / Individuals, kind like a master uses his whip to control his slaves. """

    time.sleep(5)
    population = Population.Population(2)
    print(population)
    uinsane_bolt = population.population[1]
    uinsane_bolt.run()
