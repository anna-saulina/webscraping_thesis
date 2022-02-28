from constants import ALPHABET


def convert_string_to_set(string):
    res = {char for char in string if char in ALPHABET}
    return res