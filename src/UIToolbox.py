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

from getpass import getpass
import EncodingToolbox
import EncryptionToolbox
import MarkovToolbox
import argparse
import os


def argument_handler():
    parser = argparse.ArgumentParser()
    arg_group = parser.add_mutually_exclusive_group()
    arg_group.add_argument("-e", "--encrypt", help="Encrypt a text",
                           action='store_true')
    arg_group.add_argument("-d", "--decrypt", help="Decrypt a text",
                           action='store_true')
    arg_group.add_argument("-i", "--is_interactive", help="make interactive",
                           action='store_true')
    parser.add_argument("-t", "--threshold",
                        help=str("What's the lower limit on the most used " +
                                 "letter to start a sentence or a word?"),
                        type=int, default=10)
    parser.add_argument("-m", "--model_loc",
                        help="Absolute path to the markovify text model")
    parser.add_argument("-f", "--textfile",
                        help=str("Absolute path to the location of the text " +
                                 "file which either contains or will contain" +
                                 "the encoded sentences"))
    parser.add_argument("-s", "--is_silent",
                        help="suppress output", default=False)
    args = parser.parse_args()
    return (args.encrypt, args.decrypt, args.threshold, args.model_loc,
            args.textfile, args.is_interactive, args.is_silent)


def choice_handler():
    """
    It'd called from the main program and provides the needed functions.

    Returns
    -------
    encrypt             (str x str x int x bool x bool) -> bool
    decrypt             (str x int x bool)
    interactive         (str x str x int x bool)

    """
    def vote(question):
        choice = None
        while choice not in ["y", "n"]:
            choice = str(raw_input("{} (y/n): ".format(question))).lower()
            if choice not in ["y", "n"]:
                print "Invalid choice"
        return choice

    def encrypt(model_loc, text_file_abs_path, threshold=10, silent=False,
                text_model_object=None):
        raw_text = str(raw_input("What is your message? "))
        key = get_key()
        ciphertext = EncryptionToolbox.encrypt(raw_text, key)
        if text_model_object is not None:
            text_model = text_model_object
        else:
            if not silent:
                print "Loading Text model..."
            text_model = MarkovToolbox.load_text_model(model_loc)
        if text_model is not None:
            if not silent:
                print "Encoding..."
            encoding = EncodingToolbox.encode(ciphertext, text_model,
                                              text_file_abs_path, threshold,
                                              silent)
            if encoding is not None:
                if not silent:
                    choice = vote("Do you want to see the generated text?")
                    if choice == "y":
                        print encoding[0]
        return None

    def decrypt(text_file_abs_path, threshold=10, silent=False):
        key = get_key()
        if not silent:
            print "Decoding"
        ciphertext = EncodingToolbox.decode(text_file_abs_path, threshold)
        if not silent:
            print "Decrypting"
        plaintext = EncryptionToolbox.decrypt(ciphertext, key)
        choice = vote("Do yo want to see the plaintext?")
        if choice == "y":
            print plaintext

    def interactive(model_loc, text_file_abs_path, threshold=10, silent=False):
        text_file_abs_path = text_file_path_validity(text_file_abs_path)
        if not silent:
            print "Loading Text model..."
        text_model = MarkovToolbox.load_text_model(model_loc)
        if text_model is None:
            print "Model can't be loaded"
        choice = None
        while True:
            if choice not in ["e", "d", "q"]:
                choice = str(
                    raw_input("(e)ncrypt or (d)ecrypt or (q)uit: ")
                ).rstrip().lower()
                if choice == "e":
                    encrypt(model_loc, text_file_abs_path, threshold, silent,
                            text_model_object=text_model)
                elif choice == "d":
                    decrypt(text_file_abs_path, threshold, silent)
                elif choice == "q":
                    raise SystemExit
                else:
                    print "Invalid choice"
                choice = None

    return encrypt, decrypt, interactive


def get_key():
    """
    The value would be directly passed to an encryption function. The shadowing
    is only for UI purposes.

    Returns
    -------
    key:        str
    """
    key = None
    confirmation = False
    while confirmation != key:
        key = getpass("What is your encryption key? ")
        confirmation = getpass("Repeat your key: ")
        if key != confirmation:
            print "Your key doesn't match its confirmation"
    return key


def text_file_path_validity(textfile):
    """
    Is used to either receive the location of the text file which is going to
    contain encoded sentences, or to verify the location of the existing file.

    Arguments
    ---------
    textfile    str

    Returns
    ---------
    textfile    str
    """
    if textfile is None:
        textfile = str(raw_input("Enter absolute path to text file: "))
    if not os.path.exists(textfile):
        if not os.access(os.path.dirname(textfile), os.W_OK):
            while not os.access(os.path.dirname(textfile), os.W_OK):
                textfile = str(
                    raw_input("Invalid or unaccessible path. " +
                              "Enter absolute path to the file: "))
    return textfile


def model_loc_handler():
    # Not yet implemented.
    pass
