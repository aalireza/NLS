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

from Crypto.Cipher import AES
from Crypto.Protocol import KDF
import NumericalToolbox
import binascii

# Blocksize by default is 16 bytes for AES-128.
BLOCKSIZE = 16

# There are randomly generated but hard coded. Thinking the probability of
# someone using this in real life is infinitesimal, I hard coded them to reduce
# the complexity of the interface. If you're actually trying to use it, then
# use the function `Crypto.Random.get_random_bytes` to generate a unique IV and
# a unique SALT for a every password.
SALT = '_\x94\xdb\xbd\xd8\xdd?5\xff\xb5\xe1\x9d\xbe\n\x16\xc2'
IV = '\x03\x0c\x06\xf0B\xdb\xcbv!0\xe4\xea"\xc3;-'

def gen_key(password, salt, dkLen=BLOCKSIZE):
    """
    Implement PBKDF2 to make short passwords match the BLOCKSIZE.

    Parameters
    ---------
    password            str
    salt                str
    dkLen               int

    Returns
    -------
    -                   str
    """
    return KDF.PBKDF2(password, salt, dkLen=BLOCKSIZE)


def pad(plaintext):
    """
    Implements PKCS#7 to pad `plaintext`. Not intended to be used for passwords.

    Parameters
    ----------
    plaintext:  str

    Returns
    -------
    padded:     str
    """
    topad = BLOCKSIZE - (len(plaintext) % BLOCKSIZE)
    padded = str(plaintext + bytearray([topad] * topad))
    return padded


def unpad(padded_plaintext):
    """
    Reverses EncryptionToolbox.pad

    Parameters
    ----------
    padded_plaintext:          str

    Returns
    -------
    plaintext:                 str
    """
    bytestring = bytearray(padded_plaintext)
    padding_char = bytestring[-1]
    plaintext = str(bytestring[: len(bytestring) - padding_char])
    return plaintext


def encrypt(text, password, salt=SALT, IV=IV):
    """
    Encrypts with AES, CBC. Then changes the representation of the ciphertext to
    our previously defined letter formatting in NumericalToolbox.

    Parameters
    ----------
    text:               str
    password:           str

    Returns
    -------
    lettered_ciphertext str
                        In base 10, NLS formatting
    """
    padded_text = pad(text)
    key = gen_key(password, salt)
    cipher = AES.AESCipher(key, AES.MODE_CBC, IV=IV)
    ciphertext = cipher.encrypt(padded_text)
    b16 = binascii.hexlify(bytearray(ciphertext))
    ciphertext_base_10 = NumericalToolbox.letters_to_decimals_change_base(
        b16, 16, standard_formatting=True)
    lettered_ciphertext = NumericalToolbox.decimals_to_letters_change_base(
        ciphertext_base_10, 10)
    return lettered_ciphertext


def decrypt(ciphertext, password, salt=SALT, IV=IV):
    """
    decryptor for EncryptionToolbox.encrypt.

    Parameters
    ----------
    ciphertext:         str
                        In base 10, NLS formatting
    key:                str

    Returns
    -------
    plaintext           str
    """
    ciphertext_decimals = NumericalToolbox.letters_to_decimals_change_base(
        ciphertext, 10)
    ciphertext16 = NumericalToolbox.decimals_to_letters_change_base(
        ciphertext_decimals, 16, standard_formatting=True)
    ciphertext_original = binascii.unhexlify(ciphertext16)
    key = gen_key(password, salt)
    cipher = AES.AESCipher(key, AES.MODE_CBC, IV=IV)
    padded_plaintext = cipher.decrypt(ciphertext_original)
    return unpad(padded_plaintext)
