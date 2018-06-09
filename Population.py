import Individual

class Population:
    """ Contains all the individuals in the population """
    def __init__(self, n):  # n is the number of individuals in the population
        self.population = [Individual.Individual() for _ in range(n)]

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

        # Note: length below refers to how many key presses in the keypress sequence, not the duration of the keypress.
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