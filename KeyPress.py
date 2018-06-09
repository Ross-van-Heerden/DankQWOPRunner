from pynput.keyboard import Key, Controller
import random
import time


class KeyPress:
    """ KeyPress class represents a key press action performed by the AI """

    def __init__(self):
        """ Create a new KeyPress object """
        # Should we make this completely random? (will be used when a mutation makes a new keypress get inserted
        self.q = random.choice([True, False])
        self.w = random.choice([True, False])
        self.o = random.choice([True, False])
        self.p = random.choice([True, False])
        self.n = random.choice([True, False])
        self.duration = round(random.uniform(0, 4), 2)

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
        keypress_string_representation = ""
        if self.q:
            keypress_string_representation += "Q"
        else:
            keypress_string_representation += "_"
        if self.w:
            keypress_string_representation += "W"
        else:
            keypress_string_representation += "_"
        if self.o:
            keypress_string_representation += "O"
        else:
            keypress_string_representation += "_"
        if self.p:
            keypress_string_representation += "P"
        else:
            keypress_string_representation += "_"
        keypress_string_representation += " " + str(self.duration)

        return keypress_string_representation
