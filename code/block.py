# -*- coding: utf-8 -*-
import hashlib
STARTER_NONCE = 0
DIFFICULTY = 4


class Block:
    def __init__(self, number, prev, transactions):
        """
        constructor
        """
        self.number = number
        self.nonce = STARTER_NONCE
        self.prev = prev
        self.difficulty = DIFFICULTY
        self.transactions = transactions
        self.hash_code = ''
        self.hash_block()

    def to_string(self):
        """
        the function converts the block to a string
        :returns: the block's string
        """
        block_string = str(
            self.number)+str(
                self.nonce)+self.prev+str(
                    self.difficulty)+self.hash_transactions()
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


if __name__ == "__main__":
    block_1 = Block(0, '0', [])
    block_2 = Block(1, block_1.hash_code, [])
    assert block_1.hash_code != block_2.hash_code
    block_2.prev = '0'
    block_2.hash_block()
    assert block_1.hash_code != block_2.hash_code
    block_2.number = 0
    block_2.hash_block()
    assert block_1.hash_code == block_2.hash_code