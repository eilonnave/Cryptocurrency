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
        self.difficulty = 4

    def add_new_block(self, data):
        """
        the function adds new block to the chain
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
        """
        nonce = 0
        while not self.is_valid_proof(block):
            nonce += 1
            block.update_hash(nonce)
        print nonce
        print block.hash_code

    def is_valid_proof(self, block):
        """
        check if the block hash is valid
        """
        return block.hash_code[0:self.difficulty] == '0'*self.difficulty


if __name__ == "__main__":
    block_chain = BlockChain()
    block_data = 'transaction 1: p1<--->p2' \
                 'transaction 2: p2<--->p1'
    block_chain.add_new_block(block_data)