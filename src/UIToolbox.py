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
    arg_group = parser.add_mutually_exclusive_group(required=True)
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
    parser.add_argument("-p", "--plaintext", help="What's your message?",
                        type=str)
    parser.add_argument("-k", "--key", help="What's your key?", type=str)
    parser.add_argument("-m", "--model_loc",
                        help="Absolute path to the markovify text model")
    parser.add_argument("-f", "--textfile",
                        help=str("Absolute path to the location of the text " +
                                 "file which either contains or will contain" +
                                 "the encoded sentences"))
    parser.add_argument("-s", "--is_silent",
                        help="suppress output", action='store_true')
    args = parser.parse_args()
    if args.is_interactive:
        if any([args.plaintext, args.key]):
            print "Cannot use -p or -k with -i"
            raise SystemExit
    return (args.encrypt, args.decrypt, args.plaintext, args.key,
            args.threshold, args.model_loc, args.textfile, args.is_interactive,
            args.is_silent)


def choice_handler():
    """
    It'd called from the main program and provides the needed functions.

    Returns
    -------
    encrypt             (str x str x str x str x int x bool x bool) -> str
    decrypt             (str x str x int x bool)
    interactive         (str x str x int x bool)
    vote                (str, [str])

    """
    def vote(question, choices):
        """
        Asks for a valid choice defined by existence in a list of available
        choices.

        Arguments
        ---------
        question        str
        choices         [str]

        Returns
        -------
        choice          str
        """
        choice = None
        while choice not in choices:
            choice = str(raw_input("{} ({}): ".format(
                question, "/".join(choices)))).rstrip().lower()
            if choice not in choices:
                print "Invalid choice"
        return choice

    def encrypt(model_loc, text_file_abs_path, plaintext=None, key=None,
                threshold=10, silent=False, text_model_loaded=False):
        """
        The main interface for encrypting and encoding.

        Arguments
        ---------
        model_loc               str
                                Absolute path to the save text model
        text_file_abs_path      str
                                Absolute path to text file which will contain
                                the result
        plaintext               str
                                The message to be encrypted.
        key                     str
                                The key for encryption
        threshold               int
                                The number of most probable letters
        silent                  bool
                                - `True` to print the output
                                - `False` otherwise
        text_model_object       bool
                                - `True` if model is already loaded in memory
                                - `False` otherwise

        Returns
        -------
        text                    str
                                The encoded ciphertext
        """
        text_file_abs_path, _, _ = abs_path_validity(
                text_file_abs_path, "Text file",
                addenda="That'll be created to contain the encoded results")
        model_loc, _ = model_loc_handler(model_loc, silent)
        if plaintext is None:
            plaintext = str(raw_input("What is your message? "))
        if key is None:
            key = get_key()
        ciphertext = EncryptionToolbox.encrypt(plaintext, key)
        if text_model_object is not None:
            text_model = text_model_loaded
        else:
            if not silent:
                print "Loading Text model..."
            text_model = MarkovToolbox.load_text_model(model_loc)
        if text_model is not None:
            if not silent:
                print "Encoding..."
            text, _ = EncodingToolbox.encode(ciphertext, text_model,
                                             text_file_abs_path, threshold,
                                             silent)
            if text is not None:
                if not silent:
                    choice = vote("Do you want to see the generated text?",
                                  ["y", "n"])
                    if choice == "y":
                        print "\n{}\n".format(text)
        return text

    def decrypt(text_file_abs_path, key=None, threshold=10, silent=False):
        """
        The main interface for decoding and decrypting

        Arguments
        ---------
        text_file_abs_path      str
                                Absolute path to the file containing the encoded
                                ciphertext
        key                     str
        threshold               int
                                Number of probable letters
        silent                  bool
                                - `True` if output is printed
                                - `False` otherwise

        Returns
        -------
        plaintext               str
        """
        text_file_abs_path, _, _ = abs_path_validity(
            text_file_abs_path, file_name="Text file", must_exist=True,
            addenda=("-That already exists- which contain the encoded results"))
        if key is None:
            key = get_key()
        if not silent:
            print "Decoding"
        ciphertext = EncodingToolbox.decode(text_file_abs_path, threshold)
        if not silent:
            print "Decrypting"
        plaintext = EncryptionToolbox.decrypt(ciphertext, key)
        print "\n{}\n".format(plaintext)
        return plaintext

    def interactive(model_loc, text_file_abs_path, threshold=10, silent=False):
        """
        The interactive method.

        Arguments
        ---------
        model_loc               str
        text_file_abs_path      str
        threshold               int
        silent                  bool

        Raises
        -------
        SystemExit              if choice == `q`
        """
        text_file_abs_path, _, _ = abs_path_validity(
            text_file_abs_path,
            file_name="text file containg the encoded ciphertext",
            addenda="(if file doesn't exists, it'll be created)")
        model_loc, model_exists = model_loc_handler(model_loc, silent)
        if not silent:
            print "Loading Text model..."
        text_model = MarkovToolbox.load_text_model(model_loc)
        if text_model is None:
            print "Model can't be loaded"
        while True:
            choice = vote("Encrypt or Decrypt or Quit ", ["e", "d", "q"])
            if choice == "e":
                encrypt(model_loc, text_file_abs_path, threshold=threshold,
                        silent=silent, text_model_object=text_model)
            elif choice == "d":
                decrypt(text_file_abs_path, threshold, silent)
            elif choice == "q":
                raise SystemExit

    return encrypt, decrypt, interactive, vote


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


def abs_path_validity(abs_path, file_name, must_exist=False, addenda=""):
    """
    It used to verify the validity of a path and to indicate whether it exists
    or it's a path that can exist.

    Arguments
    ---------
    abs_path        str
    file_name       str
    must_exist      bool
    addenda         str

    Returns
    ---------
    abs_path        str
    exists          bool
    can_exist       bool
    """
    while abs_path is None:
        abs_path = str(
            raw_input("Enter absolute path to {} {}: ".format(
                file_name, addenda)))
    while not os.access(os.path.dirname(abs_path), os.W_OK):
        abs_path = str(
            raw_input("Invalid or unaccessible path. " +
                      "Enter absolute path to {} {}: ".format(
                            file_name, addenda)))
    if must_exist and not os.path.exists(abs_path):
        return None, False, False
    exists = os.path.exists(abs_path)
    can_exist = os.access(os.path.dirname(abs_path), os.W_OK)
    return abs_path, exists, can_exist


def model_loc_handler(model_loc, silent=False):
    """
    Asks for text model location. If not found, trains the hmm model.

    Arguments
    ---------
    model_loc           str
                        Absolute path to text model
    silent              bool

    Returns
    -------
    model_loc           str
    model_exists        bool
    """
    model_loc, model_exists, _ = abs_path_validity(
        model_loc, "text model",
        addenda="(if file doesn't exists, it'll be created)")
    if not model_exists:
        training_text_abs_path, training_text_exists, _ = abs_path_validity(
            None, "Training text", must_exist=True)
        while not training_text_exists:
            training_text_abs_path, training_text_exists, _ = abs_path_validity(
                None, "Training text", must_exist=True)
        if not silent:
            print "Training the HMM..."
        text_model = MarkovToolbox.make_text_model(training_text_abs_path)
        if not silent:
            print "Saving the model in {}".format(model_loc)
        MarkovToolbox.save_text_model(text_model, model_loc)
    return model_loc, model_exists
