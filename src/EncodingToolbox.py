import NumericalToolbox
import EncryptionToolbox

# Data from: https://en.wikipedia.org/wiki/Letter_frequency
FIRST_LETTER_FREQ = {
    "a": 11.62, "b": 4.7, "c": 3.51, "d": 2.67, "e": 2, "f": 3.78, "g": 1.95,
    "h": 7.23, "i": 6.29, "j": 0.597, "k": 0.59, "l": 2.705, "m": 4.383,
    "n": 2.365, "o": 6.264, "p": 2.545, "q": 0.173, "r": 1.653, "s": 7.755,
    "t": 16.671, "u": 1.487, "v": 0.649, "w": 6.753, "x": 0.017, "y": 1.62,
    "z": 0.034
}


def limit_freq_threshold(num):
    freq_repo = dict(zip(FIRST_LETTER_FREQ.values(), FIRST_LETTER_FREQ.keys()))
    acceptable_freq = sorted(freq_repo.keys())[::-1][:num]
    acceptable_letters = [freq_repo[freq] for freq in acceptable_freq]
    return acceptable_letters


def first_letter_based_freq_rename(number, letters):
    # The base of the number must match the number of the provided letters.
    # Requires number in letter formatting
    renamed = ''.join(
        [letters[NumericalToolbox.letter_to_decimal(letter_digit)]
         for letter_digit in list(number)])
    return renamed


def revert_renamed_number(renamed, letters):
    number = ''.join(
        [NumericalToolbox.decimal_to_letter(letters.index(letter_digit))
         for letter_digit in renamed])
    return number


def regex_pattern_generator(text):
    # Fix Regex
    pattern_blocks = map(lambda x: "({}|{})\w*".format(x.lower(), x.upper()),
                         list(text))
    pattern = "\\b" + " ".join(pattern_blocks)
    return pattern


def encode(ciphertext, threshold=10):
    # Implement Grep
    freq_limit = limit_freq_threshold(threshold)
    renamed_ciphertext = first_letter_based_freq_rename(ciphertext, freq_limit)
    pattern = regex_pattern_generator(renamed_ciphertext)
    print pattern
