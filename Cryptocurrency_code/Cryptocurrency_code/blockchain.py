# -*- coding: utf-8 -*-
from block import Block
STARTER_NONCE = 0


class BlockChain:
    def __init__(self):
        """
        constructor
        """
        self.chain = []
        self.transactions = []
        self.difficulty = 2

    def add_new_block(self, data):
        """
        the function adds new block to the chain
        :param data: the block's data
        """
        number = len(self.chain)
        if number == 0:
            prev = '0'
        else:
            prev = self.chain[-1].hash_code

        block = Block(number, STARTER_NONCE, data, prev)
        self.mine_block(block)
        self.chain.append(block)

    def mine_block(self, block):
        """
        the function mines a specific block
        and returns it
        :param block: the block to mine
        """
        nonce = 0
        while not self.is_valid_proof(block):
            nonce += 1
            block.update_hash(nonce)

    def is_valid_proof(self, block):
        """
        check if the block hash is valid
        :param block: the block to check if
        it is valid
        :returns: whether the proof of work
        on the block is valid
        """
        return block.hash_code[0:self.difficulty] == '0'*self.difficulty


if __name__ == "__main__":
    block_chain = BlockChain()
    block_data = 'transaction 1: p1<--->p2' \
                 'transaction 2: p2<--->p1'
    block_chain.add_new_block(block_data)
    assert block_chain.is_valid_proof(block_chain.chain[0])