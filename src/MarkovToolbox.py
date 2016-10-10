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

import cPickle as pickle
import markovify


def make_text_model(text_file_abs_path):
    """
    Trains a Hidden Markov Model with Markovify.

    Arguments
    ---------
    text_file_abs_path      str
                            The absolute path to the text file

    Returns
    -------
    text_model              object
                            The text_model object
    """
    try:
        with open(text_file_abs_path, "r") as f:
            text = f.read()
        text_model = markovify.Text(text)
        return text_model
    except:
        print "There was something wrong with opening up the text file"
        raise SystemExit


def save_text_model(text_model, model_dump_abs_path):
    """
    It saves text_model (which supposed to be present in the memory when it's
    being called) to a binary file located at `model_dump_abs_path`

    Arguments
    ---------
    text_model:             object
    model_dump_abs_path:    str
                            The absolute path to the saved model

    Returns
    -------
    -                       One of:
                            - `True`    if the model was sucessfully saved
                            - `None`    otherwise
    """
    try:
        with open(model_dump_abs_path, "wb") as f:
            pickle.dump(text_model, f, protocol=2)
        return True
    except Exception:
        print "There was something wrong with saving your model"
        raise SystemExit


def load_text_model(model_dump_abs_path):
    """
    loads the outcome of MarkovToolbox.save_text_model

    Arguments
    ---------
    model_dump_abs_path:    str
                            The absolute path to the saved model

    Returns
    -------
    -                       One of:
                            -text_model:     object
                                             If model was successfully loaded
                            -`None`          if otherwise
    """
    try:
        with open(model_dump_abs_path, "rb") as f:
            text_model = pickle.load(f)
            return text_model
    except Exception:
        return None


def make_sentence_starting_with_letter(letter, text_model):
    """
    Makes a valid sentence that starts with `letter`

    Arguments
    ---------
    letter:                 str
    text_model:             Object

    Returns
    -------
    sentence:               str
    """
    sentence = None
    while sentence is None:
        first_word = None
        while first_word is None:
            candidates = list(text_model.chain.gen())
            try:
                first_word = filter(
                    lambda word: word[0] in [letter.upper(), letter.lower()],
                    candidates[:len(candidates) - 1])[0]
                second_word = candidates[candidates.index(first_word) + 1]
            except IndexError:
                pass
        sentence = text_model.make_sentence((first_word, second_word))
        if sentence is not None:
            # Ensuring that the sentence doesn't contain initials like U.S. or
            # A.M. to facilitate spliting by sentences.
            if sentence.count('.') != 1:
                sentence = None
            else:
                # Make first letter of every sentence capitalized.
                sentence = sentence[0].upper() + sentence[1:]
                return sentence


def generate_text_based_on_letter_list(letters, text_model, silent=False):
    """
    Generates a text by repeatedly calling
    MarkovToolbox.make_sentence_starting_with_letter over a list of letters

    Arguments
    ---------
    letters:            [str]
    text_model:         object
    silent              bool
                        - `True`    if progress is printed
                        - `False`   otherwise

    Returns
    -------
    text:               str
    """
    text_list = []
    for i, letter in enumerate(letters):
        text_list.append(make_sentence_starting_with_letter(letter, text_model))
        if not silent:
            print "sentence number {} found. Need {} more.".format(
                i + 1, len(letters) - i - 1)
    text = ' '.join(text_list)
    return text


def derive_first_letter_of_every_sentence(text):
    """
    Given a text, generates a list of first letters of every sentence.

    Arguments
    ---------
    text:               str

    Returns
    -------
    letters             [str]
    """
    sentences = [text[0]] + [text[j]
                             for j in xrange(2, len(text))
                             if (text[j - 2] == '.' and
                                 text[j - 1] == ' ')]
    letters = [sentence[0].lower() for sentence in sentences]
    return letters
