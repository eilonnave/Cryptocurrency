# -*- coding: utf-8 -*-
from encryption import EncryptionSet
from Crypto.PublicKey import *


class Wallet(EncryptionSet):
    def __init__(self, private_key):
        """
        constructor
        """
        super(Wallet, self).__init__(private_key)


def new_wallet():
    """
    the function creates new wallet
    and returns it
    :returns: the new wallet
    """
    private_key = RSA.generate(2048)
    wallet = Wallet(private_key)
    return wallet


if __name__ == "__main__":
    w1 = new_wallet()
    pub1 = w1.public_key.exportKey()
    w2 = new_wallet()
    pub2 = w2.public_key.exportKey()
    w3 = new_wallet()
    pub3 = w3.public_key.exportKey()
    assert pub1 != pub2
    assert pub1 != pub3
    assert pub2 != pub3