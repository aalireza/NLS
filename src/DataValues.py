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

# Below are the frequency of the letters at the start of a word in English.
# Data from: https://en.wikipedia.org/wiki/Letter_frequency
FIRST_LETTER_WORD_FREQ = {
    "a": 11.62, "b": 4.7, "c": 3.51, "d": 2.67, "e": 2, "f": 3.78, "g": 1.95,
    "h": 7.23, "i": 6.29, "j": 0.597, "k": 0.59, "l": 2.705, "m": 4.383,
    "n": 2.365, "o": 6.264, "p": 2.545, "q": 0.173, "r": 1.653, "s": 7.755,
    "t": 16.671, "u": 1.487, "v": 0.649, "w": 6.753, "x": 0.017, "y": 1.62,
    "z": 0.034
}

# Below are the order of the words that start an English sentence.
# https://glossarch.wordpress.com/2014/01/14/the-most-common-letter-to-start-a-sentence-with-in-english/
# It's at the form of a dictionary to match the structures between
# `first_letter_freq` and `first_letter_word_freq`. These two would be used in
# EncodingToolbox.
# For the dict below, keys are letters and values are occurrences in brown
# corpus.
FIRST_LETTER_FREQ = {"t": 11928, "i": 7006, "a": 4830, "h": 4653, "s": 3225,
                     "w": 3100, "b": 2412, "m": 1836, "o": 1735, "f": 1462,
                     "n": 1314, "p": 1034, "c": 981, "d": 941,
                     "e": 868, "y": 859, "l": 713, "r": 666, "g": 517, "j": 354,
                     "u": 299, "v": 143, "k": 143, "q": 41, "z": 10, "x": 2}
