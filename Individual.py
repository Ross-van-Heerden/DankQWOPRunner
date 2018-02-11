from collections import deque
import random

# Example of how to use deque (We will have a deque of KeyPress objects)
d = deque([1, 2, 3, 4])
print(d)
d.pop()
print(d)
d.append(5)
print(d)
d.insert(3, 8)  # Note insert starts indexing at 0
print(d)


class KeyPress:
    """ KeyPress class represents an key press action performed by the bot """

    def __init__(self):
        """ Create a new KeyPress object """
        # Should we make this completely random? (will be used when a mutation makes a new keypress get inserted
        self.q = False
        self.w = False
        self.o = False
        self.p = False
        self.n = False
        self.duration = 0

    def mutate(self):
        """ Mutate this object with 10% chance to add/remove a key and change the duration by a random amount """
        self.q = random.choice([self.q] * 9 + [not self.q])  # 10% chance to change
        self.w = random.choice([self.w] * 9 + [not self.q])
        self.o = random.choice([self.o] * 9 + [not self.q])
        self.p = random.choice([self.p] * 9 + [not self.q])
        self.n = not (self.q | self.w | self.o | self.p)
        # Could change the line below to only change duration within 20% of its original value but leaving it for now.
        self.duration = random.choice([self.duration] * 2 + [abs(self.duration + random.uniform(-1, 1))])  # 33% chance to change

    def __str__(self):
        keypress_string_representation = str(self.q) + ' ' + str(self.w) + ' ' + str(self.o) + ' ' + str(self.p) + ' ' + str(self.n) + ' ' + str(self.duration)
        return keypress_string_representation


class Individual:
    """ An individual in the population containing their KeyPress sequence and fitness """
    def __init__(self):
        self.keypress_sequence = deque([KeyPress()])  # keypress_sequence initialised to one key press
        self.fitness = 0

    def __str__(self):
        individual_string_representation = ''
        for kp in self.keypress_sequence:
            individual_string_representation += ' ' + str(kp)

        individual_string_representation += (' ' + str(self.fitness))
        return individual_string_representation


# Example of mutating each key press in the individuals keypress sequence
guy = Individual()
for kp in guy.keypress_sequence:
    kp.mutate()

# Format of printout is: Q W O P N duration fitness
print(guy)
