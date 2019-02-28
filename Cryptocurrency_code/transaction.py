# -*- coding: utf-8 -*-
import Crypto


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
        :returns: the transaction's hash
        """
        return Crypto.HashHash.SHA256.new(self.to_string()).hehexdigest()

    def to_string(self):
        """
        converts the transaction to a string
        :returns: the transaction's string
        """
        s = self.sender_address + \
            self.recipient_address\
            + str(self.amount)
        return s


if __name__ == "__main__":
    t = Transaction('1', '1', 1)
    print t.hash_transaction()