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