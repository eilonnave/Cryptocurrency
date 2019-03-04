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
        return recipient_public_key.encrypt(self.to_string(), 32)[0]

    def sign_transaction(self, sender_private_key):
        """
        the function signs the transaction
        using the sender private key
        :param sender_private_key: the server's private
        key
        :return: the signature that created from
        the key and the transaction
        """
        return sender_private_key.sign(self.hash, '')


if __name__ == "__main__":
    t_1 = Transaction('1', '1', 1)
    t_2 = Transaction('2', '2', 2)
    assert t_1.hash != t_2.hash
    private_key_1 = RSA.generate(2048)
    public_key_1 = private_key_1.publickey()
    private_key_2 = RSA.generate(2048)
    public_key_2 = private_key_2.publickey()
    encrypted_transaction = t_1.encrypt_transaction(public_key_2)
    decrypted_transaction = private_key_2.decrypt(encrypted_transaction)
    assert decrypted_transaction == t_1.to_string()
    decrypted_transaction = private_key_1.decrypt(encrypted_transaction)
    assert decrypted_transaction != t_1.to_string()
    signature = t_1.sign_transaction(private_key_1)
    assert public_key_1.verify(t_1.hash, signature)
