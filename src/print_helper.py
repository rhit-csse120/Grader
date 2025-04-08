"""
Code to print in color on a Console.
"""

import sys


COLOR_CODES = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "default": 39,
    "gray": 90,
    "bright red": 91,
    "bright green": 92,
    "bright yellow": 93,
    "bright blue": 94,
    "bright magenta": 95,
    "bright cyan": 96,
    "bright white": 97,
}


# noinspection PyUnusedLocal
def print_colored(*args, color="black", flush=True, **kwargs):
    text = ""
    for arg in args:
        text = text + " " + str(arg)
    text = text.replace(" ", "", 1)
    sys.stdout.write("\033[%sm%s\033[0m" % (COLOR_CODES[color], text))
    print(**kwargs)


def print_error(*args, color="red", flush=True, **kwargs):
    print_colored(*args, color=color, flush=flush, **kwargs)


def show_colors():
    for key in COLOR_CODES:
        print_colored("hello there", color=key)
    print_error("This is an error message")


if __name__ == "__main__":
    show_colors()
