"""
Module returns the values for the game,
generates active colors, the winning sequence
and values(name, channels) for each color.
"""

import random


class GameParams:
    def __init__(self, n_colors: int = 4,
                 n_slots: int = 4, n_turns: int = 10):
        self.active_colors = self.get_colors(n_colors)
        self.correct = self.get_correct(n_slots)
        self.max_guess = n_turns
        self.n_slots = n_slots
        self.n_turns = n_turns

        # REMOVE WHEN DONE
        self.guesses = [
            [random.choice(self.active_colors) for n in range(n_slots)]
            for n in range(5)]

    @staticmethod
    def get_colors(n_colors):
        """
        assigns self.color to list of n_var different values.
        """
        colors = [
            Color.red,
            Color.blue,
            Color.green,
            Color.yellow,
            Color.purple,
            Color.turquoise,
            Color.lime,
            Color.pink,
            Color.orange,
            Color.magenta,
        ]
        active_colors = random.sample(colors,  n_colors)
        return active_colors

    def get_correct(self, n_slots):
        """
        return n_spots long list of random items, with
        a maximum variation of n_var
        """
        correct = [random.choice(self.active_colors) for cor in range(n_slots)]
        return correct


class Color:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @classmethod
    def red(cls):
        return cls('red', (255, 0, 0))

    @classmethod
    def blue(cls):
        return cls('blue', (0, 0, 255))

    @classmethod
    def green(cls):
        return cls('green', (0, 255, 0))

    @classmethod
    def yellow(cls):
        return cls('yellow', (255, 255, 0))

    @classmethod
    def purple(cls):
        return cls('purple', (128, 0, 128))

    @classmethod
    def pink(cls):
        return cls('pink', (255, 192, 203))

    @classmethod
    def orange(cls):
        return cls('orange', (255, 165, 0))

    @classmethod
    def turquoise(cls):
        return cls('turquoise', (64, 224, 208))

    @classmethod
    def lime(cls):
        return cls('lime', (0, 255, 0))

    @classmethod
    def magenta(cls):
        return cls('magenta', (255, 0, 255))
