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

    def execute(self):
        """ Execute the keypress """
        keyboard = Controller()
        if self.q:
            keyboard.press('q')
        if self.w:
            keyboard.press('w')
        if self.o:
            keyboard.press('o')
        if self.p:
            keyboard.press('p')
        time.sleep(self.duration)
        if self.q:
            keyboard.release('q')
        if self.w:
            keyboard.release('w')
        if self.o:
            keyboard.release('o')
        if self.p:
            keyboard.release('p')

    def __str__(self):
        keypress_string_representation = str(self.q) + ' ' + str(self.w) + ' ' + str(self.o) + ' ' + str(self.p) + ' ' + str(self.n) + ' ' + str(self.duration)
        return keypress_string_representation


class Individual:
    """ An individual in the population containing their KeyPress sequence and fitness """
    def __init__(self):
        self.keypress_sequence = deque([KeyPress()])  # keypress_sequence initialised to one key press
        self.fitness = 0
        self.distance = 0
        self.time = 0

    # TODO: Stephan - could you use your code to provide this function with the distance and time?
    def calculate_fitness(self):
        self.fitness = self.distance - self.time  # TODO: Might wna scale distance or time later

    def __str__(self):
        individual_string_representation = ''
        for kp in self.keypress_sequence:
            individual_string_representation += ' ' + str(kp)

        individual_string_representation += (' ' + str(self.fitness))
        return individual_string_representation


class Population:
    """ Contains all the individuals in the population """
    def __init__(self, n):  # n is the number of individuals in the population
        self.population = [Individual() for _ in range(n)]

    def crossover(self, mom, dad):
        """ This is where mommy and daddy (top 2 individuals) have sexy time """

        """
        |__a__|_b_|_____________c______________|_d_|_____________e______________|
           6%   2%             40%               2%             40%  
        a = add new keypress object to keypress list
        b = mutate mom
        c = choose moms keypress object 
        d = mutate dad
        e = choose dads keypress object
        """

        # Note: length below refers to how many keypresses in the keypress sequence, not the duration of the keypress.
        mom_keypress_length = len(mom.keypress_sequence)
        dad_keypress_length = len(dad.keypress_sequence)
        longest_keypress_length = max(mom_keypress_length, dad_keypress_length)
        # print("longest_keypress_length: ", longest_keypress_length)

        # Build up the next population
        next_population = Population(len(self.population))

        # Perform crossover once for each individual in the next population
        for individual_index in range(0, len(self.population)):
            keypress_index = 0  # the index of the keypress sequence we are crossing over
            #  While the mom or dad still has a keypress in their keypress sequence
            while keypress_index < longest_keypress_length:
                # If the mom no longer has key presses while the dad still does, only let the random number fall in the
                # ranges (0.00, 0.06) and (0.50, 1.00).
                if keypress_index >= mom_keypress_length:
                    ran_num = random.choice([random.uniform(0, 0.06)] + [random.uniform(0.5, 1)])
                # If the dad no longer has key presses while the mom still does, only let the random number fall in the
                # range (0.00, 0.06) and (0.50, 1.00).
                elif keypress_index >= dad_keypress_length:
                    ran_num = random.uniform(0, 0.49999)
                else:
                    ran_num = random.uniform(0, 1)

                #  Build up the new individuals keypress from the parents keypress at the current keypress index based
                #  on the random number generated.
                if ran_num <= 0.06:  # Insert new keypress into current keypress index
                    keypress = KeyPress()
                    keypress.mutate()
                    next_population.population[individual_index].keypress_sequence.insert(keypress_index - 1, keypress)

                elif ran_num <= 0.08:  # Mutate the mom's keypress sequence at the current keypress index
                    next_population.population[individual_index].keypress_sequence[keypress_index] = mom.keypress_sequence[keypress_index].mutate()

                elif ran_num <= 0.5:  # Choose the mom's keypress sequence at the current keypress index
                    next_population.population[individual_index].keypress_sequence[keypress_index] = mom.keypress_sequence

                elif ran_num <= 0.52:  # Mutate the dad's keypress sequence at the current keypress index
                    next_population.population[individual_index].keypress_sequence[keypress_index] = dad.keypress_sequence[keypress_index].mutate()

                elif ran_num <= 1:  # Choose the dad's keypress sequence at the current keypress index
                    next_population.population[individual_index].keypress_sequence[keypress_index] = mom.keypress_sequence

                keypress_index += 1

                print(next_population.population[individual_index])


pop = Population(10)
pop.crossover(pop.population[1], pop.population[2])

# Example of mutating each key press in the individuals keypress sequence
#guy = Individual()
#for kp in guy.keypress_sequence:
#    kp.mutate()

# Format of printout is: Q W O P N duration fitness
#print(guy)
