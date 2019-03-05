# -*- coding: utf-8 -*-
COMMISSION = 5


class Transaction:
    def __init__(self, sender_address, recipient_address, amount):
        """
        constructor
        """
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = amount
        self.commission = COMMISSION

    def to_string(self):
        """
        converts the transaction to a string
        :returns: the transaction's string
        """
        s = self.sender_address+'\n'
        s += self.recipient_address+'\n'
        s += str(self.amount)+'\n'
        s += str(self.commission)
        return s


