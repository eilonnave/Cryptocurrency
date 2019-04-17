# -*- coding: utf-8 -*-
from Crypto.Hash import *


UN_SPENT_OUTPUTS_TABLE_NAME = 'utxo'
TRANSACTIONS_TABLE_NAME = 'transactions'
INPUTS_TABLE_NAME = 'inputs'
OUTPUTS_TABLE_NAME = 'outputs'
TRANSACTION_STRUCTURE = '(transaction_id integer, ' \
                        'block_number integer)'
# the transaction_number in the input and output
# serialization refers to the transaction id (hash)
OUTPUT_STRUCTURE = '(value integer, ' \
                   'address text, ' \
                   'transaction_number text)'
INPUT_STRUCTURE = '(transaction_id text, ' \
                  'output_index integer, ' \
                  'proof text, ' \
                  'transaction_number text)'


class Transaction:
    def __init__(self, inputs, outputs):
        """
        constructor
        """
        self.inputs = inputs
        self.outputs = outputs
        self.transaction_id = self.hash_transaction()

    def add_input(self, transaction_input):
        """
        the function adds the input
        to the transaction and updates the id
        """
        self.inputs.append(transaction_input)
        self.transaction_id = self.hash_transaction()

    def add_output(self, transaction_output):
        """
        the function adds the output
        to the transaction and updates the id
        """
        self.outputs.append(transaction_output)
        self.transaction_id = self.hash_transaction()

    def hash_transaction(self):
        """
        the function hashes the transaction's id
        :returns: the hashed id
        """
        transaction_hash = ''

        # hash the inputs
        if len(self.inputs) != 0:
            transaction_hash = self.inputs[0].hash_input()
            for transaction_input in self.inputs[1:]:
                transaction_hash += transaction_input.hash_input()
                transaction_hash = SHA256.new(transaction_hash).hexdigest()

        # hash the outputs
        if len(self.outputs) == 0:
            return transaction_hash
        for transaction_output in self.outputs:
            transaction_hash += transaction_output.hash_output()
            transaction_hash = SHA256.new(transaction_hash).hexdigest()

        return transaction_hash

    def serialize(self, block_number):
        """
        the function serializes the transaction
        :param block_number: the block number which the
        transaction belongs to
        :returns: the serialized transaction
        """
        return '({0},{1})'.format(
            self.transaction_id,
            block_number)

    @classmethod
    def deserialize(cls, transaction_list):
        """
        the function deserializes the transaction
        from the given list
        :param transaction_list: the serialized transaction in a list
        """
        inputs = transaction_list[2]
        outputs = transaction_list[3]
        return cls(inputs, outputs)


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
        return SHA256.new(self.to_string()).hexdigest()

    def to_string(self):
        """
        the function converts the outputs to a string
        :returns: the output's string
        """
        output_string = str(self.value)
        output_string += self.address
        return output_string

    def serialize(self, transaction_number):
        """
        the function serializes the output
        :param transaction_number: the transaction number which the
        output belongs to
        :returns: the serialized output
        """
        return '({0},{1},{2})'.format(
            self.value,
            self.address,
            transaction_number)

    @classmethod
    def deserialize(cls, output_list):
        """
        the function deserializes the output
        from the given list
        :param output_list: the serialized output in a list
        """
        value = output_list[0]
        address = output_list[1]
        return cls(value, address)


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
        return SHA256.new(self.to_string()).hexdigest()

    def to_string(self):
        """
        the function converts the input to a string
        :returns: the input's string
        """
        input_string = self.transaction_id
        input_string += str(self.output_index)
        if self.output_index != -1:
            input_string += str(self.proof[0])
            input_string += self.proof[1].exportKey()
        else:
            input_string += self.proof
        return input_string

    def serialize(self, transaction_number):
        """
        the function serializes the input
        :param transaction_number: the transaction number which the
        input belongs to
        :returns: the serialized input
        """
        return '({0},{1},{2},{3})'.format(
            self.transaction_id,
            self.output_index,
            str(self.proof),
            transaction_number)

    @classmethod
    def deserialize(cls, input_list):
        """
        the function deserializes the input
        from the given list
        :param input_list: the serialized input in a list
        """
        transaction_id = input_list[0]
        output_index = input_list[1]
        proof = eval(input_list[2])
        return cls(transaction_id, output_index, proof)


class UnspentOutput:
    def __init__(self, output, transaction_id, output_index):
        """
        constructor
        """
        self.output = output
        self.transaction_id = transaction_id
        self.output_index = output_index