import KeyPress
from collections import deque
import random
from pynput.keyboard import Key, Controller
import time

# Example of how to use deque (We will have a deque of KeyPress objects)
# de = deque([1, 2, 3, 4])
# print(de)
# de.pop()
# print(de)
# de.append(5)
# print(de)
# de.insert(3, 8)  # Note insert starts indexing at 0
# print(de)


class Individual:
    """ An individual in the population containing their KeyPress sequence and fitness """
    def __init__(self):
        self.keypress_sequence = deque([KeyPress.KeyPress()])  # keypress_sequence initialised to one key press
        self.fitness = 0
        self.distance = 0
        self.time = 0

    # TODO: Stephan - could you use your code to provide this function with the distance and time?
    def calculate_fitness(self):
        self.fitness = self.distance - self.time  # TODO: Might wna scale distance or time later

    def run(self):
        """ Makes the individual execute the entirety of it's keypress sequence. i.e. makes it run """
        for kp in self.keypress_sequence:
            print('Pressing: ', kp)
            kp.execute()

    def __str__(self):
        individual_string_representation = ''
        for kp in self.keypress_sequence:
            individual_string_representation += ' ' + str(kp)

        individual_string_representation += (' ' + str(self.fitness))
        return individual_string_representation
