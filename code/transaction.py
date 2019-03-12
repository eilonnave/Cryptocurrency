# -*- coding: utf-8 -*-
from Crypto.Hash import *
COMMISSION = 5


class Transaction:
    def __init__(self, transaction_id, inputs, outputs):
        """
        constructor
        """
        self.transaction_id = transaction_id
        self.inputs = inputs
        self.outputs = outputs

    def hash_transaction(self):
        """
        the function hashes the transaction's id
        :returns: the hashed id
        """
        return SHA256.new(self.transaction_id)


class Output:
    def __init__(self, value, script_public_key):
        """
        constructor
        """
        self.value = value
        self.script_public_key = script_public_key


class Input:
    def __init__(self, output_id, output_index, script_sig):
        """
        constructor
        """
        self.output_id = output_id
        self.output_index = output_index
        self.script_sig = script_sig