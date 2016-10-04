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

import DataValues
import NumericalToolbox
import MarkovToolbox


def limit_freq_threshold(num):
    # To be Implement https://glossarch.wordpress.com/2014/01/14/the-most-common-letter-to-start-a-sentence-with-in-english/
    """
    Gets a list of `num` English letters that are most frequently appear based
    on a given criterea. For example: 10 most used letters for starting a word
    or a sentence.

    Arguments
    ---------
    num:                int

    Returns
    -------
    acceptable_letters  [str]
    """
    freq_repo = dict(zip(DataValues.FIRST_LETTER_FREQ.values(),
                         DataValues.FIRST_LETTER_FREQ.keys()))
    acceptable_freq = sorted(freq_repo.keys())[::-1][:num]
    acceptable_letters = [freq_repo[freq] for freq in acceptable_freq]
    return acceptable_letters


def first_letter_based_freq_rename(number, letters):
    """
    Remaps each character that appears in a number in letter formatting to a set
    of letters. This is needed because if criterea for choosing words changes,
    it'd be better to not change the entire formatting, but, if needed, define a
    remapping for the aforementioned changed criterea.

    Arguments
    ---------
    number              str
    letters             [str]

    Returns
    -------
    renamed             str
    """
    # The base of the number must match the number of the provided letters.
    # Requires number in letter formatting (non-standard)
    renamed = ''.join(
        [letters[NumericalToolbox.letter_to_decimal(letter_digit)]
         for letter_digit in list(number)])
    return renamed


def revert_renamed_number(renamed, letters):
    """
    Reverse of EncodingToolbox.first_letter_based_freq_rename to get the
    original formatting

    Arguments
    ---------
    renamed             str
    letters             [str]

    Returns
    -------
    number              str
    """
    number = ''.join(
        [NumericalToolbox.decimal_to_letter(letters.index(letter_digit))
         for letter_digit in renamed])
    return number


def encode(ciphertext, text_model, text_file_abs_path, threshold=10,
           silent=False):
    """
    Given a ciphertext, it writes the natural language representation of it in
    `text_file_abs_path`

    Arguments
    ---------
    ciphertext:             str
    text_model:             object
    text_file_abs_path:     str
    threshold:              int
    silent:                 bool
                            - `True`    if progress is to be printed
                            - `False`   Otherwise

    Returns
    -------
    -                       If the `text_file_abs_path` is sucessfully created:
                            text, text_file_abs_path:      (str, str)
                            Otherwise:
                            None
    """
    if threshold != 10:
        ciphertext = NumericalToolbox.change_base(ciphertext, 10, threshold,
                                                  standard_formatting=False)
    freq_limit = limit_freq_threshold(threshold)
    renamed = first_letter_based_freq_rename(ciphertext, freq_limit)
    text = MarkovToolbox.generate_text_based_on_letter_list(renamed, text_model,
                                                            silent)
    try:
        with open(text_file_abs_path, "wb") as f:
            f.write(text)
        return text, text_file_abs_path
    except Exception:
        return None, None


def decode(text_file_abs_path, threshold=10):
    """
    Decodes a text into a ciphertext.

    Arguments
    ---------
    text_file_abs_path:     str

    Returns
    -------
    ciphertext:             str
    """
    try:
        with open(text_file_abs_path, "rb") as f:
            text = f.read()
    except Exception:
        return None
    freq_limit = limit_freq_threshold(threshold)
    renamed_ciphertext = ''.join(
        MarkovToolbox.derive_first_letter_of_every_sentence(text))
    ciphertext = revert_renamed_number(renamed_ciphertext, freq_limit)
    if threshold != 10:
        ciphertext = NumericalToolbox.change_base(ciphertext, threshold, 10,
                                                  standard_formatting=False)
    return ciphertext
