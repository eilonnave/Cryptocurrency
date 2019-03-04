# -*- coding: utf-8 -*-
import hashlib


class Block:
    def __init__(self, number, nonce, data, prev):
        """
        constructor
        """
        self.number = number
        self.nonce = nonce
        self.data = data
        self.prev = prev
        self.hash_code = self.hash()

    def to_string(self):
        """
        the function converts the block to a string
        :returns: the block's string
        """
        block_string = str(
            self.number)+str(
                self.nonce)+self.data+self.prev
        return block_string

    def hash(self):
        """
        the function hashes the block data
        :returns: the hash value of the
        block's properties
        """
        return hashlib.sha256(
            self.to_string().encode(
                'utf-8')).hexdigest()

    def update_hash(self, nonce):
        """
        update the block hash according to
        to the new nonce
        :param nonce: the new nonce
        """
        self.nonce = nonce
        self.hash_code = self.hash()


if __name__ == "__main__":
    block_1 = Block(0, 0, 'data_1', '0')
    block_2 = Block(1, 0, 'data_1', block_1.hash_code)
    assert block_1.hash_code != block_2.hash_code
    block_2.prev = '0'
    block_2.hash_code = block_2.hash()
    assert block_1.hash_code != block_2.hash_code
    block_2.number = 0
    block_2.hash_code = block_2.hash()
    assert block_1.hash_code == block_2.hash_code