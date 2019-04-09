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

    def serialize(self):
        """
        the function serializes the transaction
        :returns: the serialized transaction
        """
        # serializes the inputs
        serialized_inputs = '['
        for transaction_input in self.inputs:
            serialized_inputs += transaction_input.serialize()+', '
        serialized_inputs = serialized_inputs[:-2]+']'

        # serializes the outputs
        serialized_outputs = '['
        for transaction_output in self.outputs:
            serialized_outputs += transaction_output.serialize()+', '
        serialized_outputs = serialized_outputs[:-2]+']'

        serialized_transaction = {'inputs': serialized_inputs,
                                  'outputs': serialized_outputs,
                                  'transaction_id': self.transaction_id}
        return str(serialized_transaction)


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

    def serialize(self):
        """
        the function serializes the output
        :returns: the serialized output
        """
        return str({'value': str(self.value),
                    'address': self.address})


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

    def serialize(self):
        """
        the function serializes the input
        :returns: the serialized input
        """
        serialized_input = self.__dict__
        serialized_input['proof'] = str((str(self.proof[0]), self.proof[1].exportKey()))
        """
        return str({'transaction_id': self.transaction_id,
                    'output_index': str(self.output_index),
                    'proof': '('+str(self.proof[0])
                                + ', ' +
                             self.proof[1].exportKey()+')'})
                             """
        return str(serialized_input)


class UnspentOutput:
    def __init__(self, output, transaction_id, output_index):
        """
        constructor
        """
        self.output = output
        self.transaction_id = transaction_id
        self.output_index = output_index