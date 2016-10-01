from Crypto.Cipher import AES
from getpass import getpass
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
    padded:     str
    """
    topad = BLOCKSIZE - (len(x) % BLOCKSIZE)
    padded = x + topad * PADDING_CHAR
    return padded


def unpad(x):
    """
    Removes PADDING_CHAR from x

    Parameters
    ----------
    x:          str

    Returns
    -------
    y:          str
    """
    y = x.rstrip(PADDING_CHAR)
    return y


def getEncryptionKey():
    """
    Returns
    -------
    key:        str
                Key used for encryption.
    """
    key = None
    confirmationKey = False
    while confirmationKey != key:
        key = getpass("What is your encryption key? ")
        confirmationKey = getpass("Repeat your key: ")
        if key != confirmationKey:
            print "Your key doesn't match its confirmation"
    return key


def encrypt(text, key):
    """
    Encrypts AES-128 and returns the result in base 10

    Parameters
    ----------
    text:               str
                        Plain text
    key:                str
                        Encryption key

    Returns
    -------
    finalCiphertext:    str
                        Cipher text in base 10
    """
    if len(key) % BLOCKSIZE != 0:
        key = pad(key)
    if len(text) % BLOCKSIZE != 0:
        text = pad(text)
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(text)
    b16 = binascii.hexlify(bytearray(ciphertext))
    ciphertext_base_10 = NumericalToolbox.baseNto10(b16, 16)
    return ciphertext_base_10


def decrypt(ciphertext, key):
    """
    Decrypts AES-128 encrypted ciphertext and returns the plain text.

    Parameters
    ----------
    ciphertext:         str
                        Should be in base 24
    key:                str
                        Encryption key

    Returns
    -------
    plainText:          str
    """
    if len(key) % BLOCKSIZE != 0:
        key = pad(key)
    ciphertext16 = NumericalToolbox.base10toN(ciphertext, 16)
    ct = binascii.unhexlify(ciphertext16)
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    plainText = unpad(cipher.decrypt(ct))
    return plainText
