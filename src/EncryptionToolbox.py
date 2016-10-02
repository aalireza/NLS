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
import NumericalToolbox
import binascii

BLOCKSIZE = 16
PADDING_CHAR = '\x00'


def pad(x):
    """
    Pads `x` to divide BLOCKSIZE

    Parameters
    ----------
    x:          str

    Returns
    -------
    paded       str
    """
    topad = BLOCKSIZE - (len(x) % BLOCKSIZE)
    padded = x + topad * PADDING_CHAR
    return padded


def unpad(x):
    """
    Removes PADDING_CHAR from `x`

    Parameters
    ----------
    x:          str

    Returns
    -------
    y:          str
    """
    y = x.rstrip(PADDING_CHAR)
    return y


def encrypt(text, key):
    """
    Encrypts with AES-128, ECB, constant blocksize.

    Parameters
    ----------
    text:               str
    key:                str

    Returns
    -------
    lettered_ciphertext str
                        In base 10, NLS formatting
    """
    if len(key) % BLOCKSIZE != 0:
        key = pad(key)
    if len(text) % BLOCKSIZE != 0:
        text = pad(text)
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(text)
    b16 = binascii.hexlify(bytearray(ciphertext))
    ciphertext_base_10 = NumericalToolbox.letters_to_decimals_change_base(
        b16, 16, standard_formatting=True)
    lettered_ciphertext = NumericalToolbox.decimals_to_letters_change_base(
        ciphertext_base_10, 10)
    return lettered_ciphertext


def decrypt(ciphertext, key):
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
    if len(key) % BLOCKSIZE != 0:
        key = pad(key)
    ciphertext_decimals = NumericalToolbox.letters_to_decimals_change_base(
        ciphertext, 10)
    ciphertext16 = NumericalToolbox.decimals_to_letters_change_base(
        ciphertext_decimals, 16, standard_formatting=True)
    ct = binascii.unhexlify(ciphertext16)
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ct))
    return plaintext
