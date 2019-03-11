# -*- coding: utf-8 -*-
from block import Block


class BlockChain:
    def __init__(self):
        """
        constructor
        """
        self.chain = []

    def add_new_block(self, transactions):
        """
        the function adds new block to the chain
        :param transactions: the transactions in the block
        """
        number = len(self.chain)
        if number == 0:
            prev = '0'
        else:
            prev = self.chain[-1].hash_code

        block = Block(number, prev, transactions)
        block.mine_block()
        self.chain.append(block)


if __name__ == "__main__":
    block_chain = BlockChain()
    block_transactions = []
    block_chain.add_new_block(block_transactions)
    assert block_chain.chain[0].is_valid_proof()