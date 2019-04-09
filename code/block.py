# -*- coding: utf-8 -*-
import hashlib
import time
STARTER_NONCE = 0
DIFFICULTY = 4
BLOCK_STRUCTURE = '(number integer, ' \
                  'nonce integer, ' \
                  'prev text, ' \
                  'difficulty integer, ' \
                  'transactions text, ' \
                  'time_stamp integer, ' \
                  'hash text)'


class Block:
    def __init__(self,
                 number,
                 nonce,
                 prev,
                 difficulty,
                 transactions,
                 time_stamp):
        """
        constructor
        """
        self.number = number
        self.nonce = nonce
        self.prev = prev
        self.difficulty = difficulty
        self.transactions = transactions
        self.time_stamp = time_stamp
        self.hash_code = ''
        self.hash_block()

    @classmethod
    def new_block(cls, number, prev, transactions):
        """
        factory method
        """
        nonce = STARTER_NONCE
        difficulty = DIFFICULTY
        time_stamp = time.time()
        return cls(number, nonce, prev, difficulty, transactions, time_stamp)

    def to_string(self):
        """
        the function converts the block to a string
        :returns: the block's string
        """
        block_string = str(
            self.number)+str(
                self.nonce)+self.prev+str(
                    self.difficulty)+self.hash_transactions()+str(
                        self.time_stamp)
        return block_string

    def hash_block(self):
        """
        the function hashes the block data
        :returns: the hash value of the
        block's properties
        """
        self.hash_code = hashlib.sha256(
            self.to_string().encode(
                'utf-8')).hexdigest()

    def hash_transactions(self):
        """
        the function hashes all the transactions
        together
        :returns: the hash code of all the transactions
        """
        if len(self.transactions) == 0:
            return ''
        transactions_hash = self.transactions[0].hash_transaction()
        for transaction in self.transactions[1:]:
            transaction_hash = transaction.hash_transaction()
            transactions_hash = hashlib.sha256(
                transactions_hash+transaction_hash).hexdigest()
        return transactions_hash

    def add_transaction(self, transaction):
        """
        the function adds the transaction
        to the list in the block
        :param transaction: a transaction to add
        """
        self.transactions.append(transaction)

    def mine_block(self):
        """
        the function mines the block
        """
        self.nonce = STARTER_NONCE
        while not self.is_valid_proof():
            self.nonce += 1
            self.hash_block()

    def is_valid_proof(self):
        """
        check if the block hash is valid
        :returns: whether the proof of work
        on the block is valid
        """
        return self.hash_code[0:self.difficulty] == '0'*self.difficulty

    def serialize(self):
        """
        the function serializes the block
        :returns: the serialized block
        """
        # serializes the transactions
        serialized_transactions = '[]'
        if len(self.transactions) != 0:
            serialized_transactions = '['
            for transaction in self.transactions:
                serialized_transactions += transaction.serialize()+', '
            serialized_transactions = serialized_transactions[:-2]+']'

        return '({0},{1},{2},{3},{4},{5},{6})'.format(
            self.number,
            self.nonce,
            self.prev,
            self.difficulty,
            serialized_transactions,
            self.time_stamp,
            self.hash_code)


if __name__ == "__main__":
    block_1 = Block.new_block(0, '0', [])
    block_2 = Block.new_block(1, block_1.hash_code, [])
    print block_1.serialize()