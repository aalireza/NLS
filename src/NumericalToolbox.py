import string


NUM_REPO = {i: letter for i, letter in zip(xrange(26), string.lowercase)}
STANDARD_NUM_REPO = dict(
    dict({i: str(i) for i in xrange(10)}).items() +
    dict({10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g',
          17: 'h', 18: 'i', 19: 'j', 20: 'k', 21: 'l', 22: 'm', 23: 'n',
          24: 'o', 25: 'q'}).items())


def letter_to_decimal(letter):
    decimal = dict(zip(NUM_REPO.values(), NUM_REPO.keys()))[letter]
    return decimal


def decimal_to_letter(decimal):
    letter = NUM_REPO[decimal]
    return letter


def decimals_to_letters_change_base(number, n, standard_formatting=False):
    new_num_string = ''
    current = number
    while current != 0:
        remainder = current % n
        if standard_formatting:
            if 26 > remainder > 9:
                remainder_string = STANDARD_NUM_REPO[remainder]
            else:
                remainder_string = str(remainder)
        else:
            remainder_string = NUM_REPO[remainder]
        new_num_string = remainder_string + new_num_string
        current = current / n
    return new_num_string


def letters_to_decimals_change_base(number, base, standard_formatting=False):
    result = 0
    number = list(str(number))
    number.reverse()
    if standard_formatting:
        repo = STANDARD_NUM_REPO
    else:
        repo = NUM_REPO
    for i in xrange(len(number)):
        for j in repo:
            if number[i] == repo[j]:
                result += int(j) * base ** int(i)
    return result


def change_base(letter_based_number, origin_base, target_base,
                standard_formatting):
    letter_based_number = decimals_to_letters_change_base(
        letters_to_decimals_change_base(
            letter_based_number, origin_base, standard_formatting
        ), target_base, standard_formatting)
    return letter_based_number
