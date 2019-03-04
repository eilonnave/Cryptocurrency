# -*- coding: utf-8 -*-
from Crypto.Hash import *
from Crypto.Signature import *
from Crypto.PublicKey import *
ENCRYPTION_PARAMETER = 32


class Transaction:
    def __init__(self, sender_address, recipient_address, amount):
        """
        constructor
        """
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = amount
        self.hash = self.hash_transaction()

    def hash_transaction(self):
        """
        returns a hash of the transaction's
        data
        :returns: the transaction's hash
        """
        return SHA256.new(self.to_string()).hexdigest()

    def to_string(self):
        """
        converts the transaction to a string
        :returns: the transaction's string
        """
        s = self.sender_address + \
            self.recipient_address\
            + str(self.amount)
        return s

    def encrypt_transaction(self, recipient_public_key):
        """
        the function encrypts the message with
        the sender private key
        :param recipient_public_key: the private key
        for the sender
        :returns: the encrypted message
        """
        return recipient_public_key.encrypt(self.to_string(), 32)

    def sign_transaction(self):
        pass


if __name__ == "__main__":
    t_1 = Transaction('1', '1', 1)
    t_2 = Transaction('2', '2', 2)
    assert t_1.hash != t_2.hash