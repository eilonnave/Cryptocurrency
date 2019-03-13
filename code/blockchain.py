# -*- coding: utf-8 -*-
from block import Block
BLOCK_HASH_SIZE = 256


class BlockChain:
    def __init__(self):
        """
        constructor
        """
        self.chain = []
        self.transactions_pool = []

    def add_new_block(self):
        """
        the function adds new block to the chain
        """
        number = len(self.chain)
        if number == 0:
            prev = '0'*256
        else:
            prev = self.chain[-1].hash_code

        block = Block(number, prev, self.transactions_pool)
        block.mine_block()
        self.chain.append(block)
        self.transactions_pool = []

    def add_transaction(self, transaction):
        """
        the function adds new transaction
        to the transactions pool
        :param transaction: new transaction to add
        """
        self.transactions_pool.append(transaction)


if __name__ == "__main__":
    block_chain = BlockChain()
    block_chain.add_new_block()
    assert block_chain.chain[0].is_valid_proof()