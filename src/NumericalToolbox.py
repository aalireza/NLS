"""
 Copyright 2016 Alireza Rafiei

 Licensed under the Apache License, Version 2.0 (the "License"); you may
 not use this file except in compliance with the License. You may obtain
 a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import string

# `NUM_REPO` is the representation that we'd use to map numbers to letters. This
# mapping is not compatible with the standard mapping. For example, `a` in
# standard formatting is `10` in base 10, yet here `a` would be `0` in base 10.
NUM_REPO = {i: letter for i, letter in zip(xrange(26), string.lowercase)}
# `STANDARD_NUM_REPO` is the standard mapping.
STANDARD_NUM_REPO = dict(
    dict({i: str(i) for i in xrange(10)}).items() +
    dict({10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g',
          17: 'h', 18: 'i', 19: 'j', 20: 'k', 21: 'l', 22: 'm', 23: 'n',
          24: 'o', 25: 'q'}).items())


def letter_to_decimal(letter):
    """
    Gets the decimal value of a particular letter in NLS formatting?

    Arguments
    ---------
        letter          str

    Returns
    -------
        decimal         int
    """
    decimal = dict(zip(NUM_REPO.values(), NUM_REPO.keys()))[letter]
    return decimal


def decimal_to_letter(decimal):
    """
    Gets the letter value of a particular decimal in NLS formatting.

    Arguments
    ---------
    decimal         int

    Returns
    -------
    letter          str
    """
    letter = NUM_REPO[decimal]
    return letter


def decimals_to_letters_change_base(decimal, target_base,
                                    standard_formatting=False):
    """
    Changes the base of a decimal to a number in base `target_base`. If
    `standard_formatting` is set to True, then the formatting would standard
    i.e. if target_base = 16 then te return value would be the same as
    hex(decimal).

    Arguments
    ---------
    decimal             int
    target_base         int
                        The base to which decimal would be converted
    standard_formatting bool

    Returns
    -------
    new_num_string      str
    """
    new_num_string = ''
    current = decimal
    while current != 0:
        remainder = current % target_base
        if standard_formatting:
            if 26 > remainder > 9:
                remainder_string = STANDARD_NUM_REPO[remainder]
            else:
                remainder_string = str(remainder)
        else:
            remainder_string = NUM_REPO[remainder]
        new_num_string = remainder_string + new_num_string
        current = current / target_base
    return new_num_string


def letters_to_decimals_change_base(number, base, standard_formatting=False):
    """
    Changes the base of a letter in base `base` to decimal. If
    `standard_formatting` is set to True, then it's assumed that the current
    representation of the number is standard.

    Arguments
    ---------
    number              str
    base                int
    standard_formatting bool

    Returns
    -------
    result              int
    """
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
    """
    Changes the base of a number in letter formatting in base `origin_base` to
    a letter formatting of base `target_base`.

    Arguments
    ---------
    letter_based_number     str
    origin_base             int
    target_base             int
    standard_formatting     bool

    Returns
    -------
    letter_based_number     str
    """
    letter_based_number = decimals_to_letters_change_base(
        letters_to_decimals_change_base(
            letter_based_number, origin_base, standard_formatting
        ), target_base, standard_formatting)
    return letter_based_number
