from Crypto.Cipher import AES
from getpass import getpass
import NumericalToolbox
import binascii

BLOCKSIZE = 16
PADDING_CHAR = '\x00'


def pad(x):
    topad = BLOCKSIZE - (len(x) % BLOCKSIZE)
    padded = x + topad * PADDING_CHAR
    return padded


def unpad(x):
    y = x.rstrip(PADDING_CHAR)
    return y


def get_key():
    key = None
    confirmation = False
    while confirmation != key:
        key = getpass("What is your encryption key? ")
        confirmation = getpass("Repeat your key: ")
        if key != confirmation:
            print "Your key doesn't match its confirmation"
    return key


def encrypt(text, key):
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
