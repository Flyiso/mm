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

    def make_guess(self, guess) -> dict:
        """
        compare input to self.correct.
        returns number of guesses present in
        self.correct and number of guesses both present
        and number of guesses present AND in right position
        """
        correct = [color.name for color in [color() for color in self.correct]]
        if correct == guess:
            return {'correct': len(guess), 'present': 0}
        score_dict = {'correct': 0, 'present': 0}
        for c_id, (guess_c, correct_c) in enumerate(zip(guess, correct)):
            if guess_c == correct_c:
                score_dict['correct'] += 1
                guess[c_id] = False
                correct[c_id] = False

        for guess_c in guess:
            if guess_c in correct and guess_c is not False:
                correct.remove(guess_c)
                score_dict['present'] += 1
        return score_dict


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
        return cls('orange', (255, 125, 0))

    @classmethod
    def turquoise(cls):
        return cls('turquoise', (64, 224, 208))

    @classmethod
    def lime(cls):
        return cls('lime', (130, 180, 1))

    @classmethod
    def magenta(cls):
        return cls('magenta', (255, 0, 255))
