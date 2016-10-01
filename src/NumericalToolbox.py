import string

NUM_REPO = {i: letter for i, letter in zip(xrange(26), string.lowercase)}


def base10toN(number, n):
    """
    Parameters
    ----------
    number:         int
                    A number in base 10
    n:              int
                    The target base, maximum 26

    Returns
    -------
    newNumString:   str
                    `number` in base `n` using NUM_REPO to represent digits
    """
    newNumString = ''
    current = number
    while current != 0:
        remainder = current % n
        remainderString = NUM_REPO[remainder]
        newNumString = remainderString + newNumString
        current = current / n
    return newNumString


def baseNto10(number, base):
    """
    Parameters
    ----------
    number:     str
                A number is base `base`
    base:       int
                The current base

    Returns
    -------
    result:     int
                `number` in base 10
    """
    result = 0
    number = list(str(number))
    number.reverse()
    for i in range(len(number)):
        for j in NUM_REPO:
            if number[i] == NUM_REPO[j]:
                result += int(j) * base ** int(i)
    return result
