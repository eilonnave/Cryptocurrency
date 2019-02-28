# -*- coding: utf-8 -*-
from Crypto import Hash
from Crypto import PublicKey
from Crypto import Signature


class Transaction:
    def __init__(self, sender_address, recipient_address, amount):
        """
        constructor
        """
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = amount

    def hash_transaction(self):
        """
        returns a hash of the transaction's
        data
        """
        pass

    def to_string(self):
        """
        converts the transaction to a string
        :returns: the transaction's string
        """
        s = self.sender_address + \
            self.recipient_address\
            + str(self.amount)
        return s