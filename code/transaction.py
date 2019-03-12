# -*- coding: utf-8 -*-
from Crypto.Hash import *
COMMISSION = 5


class Transaction:
    def __init__(self, inputs, outputs):
        """
        constructor
        """
        self.inputs = inputs
        self.outputs = outputs
        self.transaction_id = self.hash_transaction()

    def hash_transaction(self):
        """
        the function hashes the transaction's id
        :returns: the hashed id
        """
        transaction_hash = ''
        if len(self.inputs) != 0:
            transaction_hash = self.inputs[0].hash_input()
            for transaction_input in self.inputs[1:]:
                transaction_hash += transaction_input.hash_input()
                transaction_hash = SHA256.new(transaction_hash).hexdigest()
        if len(self.outputs) == 0:
            return transaction_hash
        for transaction_output in self.outputs:
            transaction_hash += transaction_output.hash_output()
            transaction_hash = SHA256.new(transaction_hash).hexdigest()
        return transaction_hash


class Output:
    def __init__(self, value, address):
        """
        constructor
        """
        self.value = value
        # address which belongs to the wallet that can use the output
        self.address = address

    def hash_output(self):
        """
        the function hashes the input
        :returns: the hash code of the
        input
        """
        return SHA256.new(self.to_string()).hex_digesst()

    def to_string(self):
        """
        the function converts the outputs to a string
        :returns: the output's string
        """
        output_string = str(self.value)
        output_string += self.address
        return output_string


class Input:
    def __init__(self, transaction_id, output_index, proof):
        """
        constructor
        """
        self.transaction_id = transaction_id
        self.output_index = output_index
        # the proof is the tuple that contains the signature and the public key
        self.proof = proof

    def hash_input(self):
        """
        the function hashes the input
        :returns: the hash code of the
        input
        """
        return SHA256.new(self.to_string()).hex_digest()

    def to_string(self):
        """
        the function converts the input to a string
        :returns: the input's string
        """
        input_string = self.transaction_id
        input_string += str(self.output_index)
        input_string += self.proof
        return input_string