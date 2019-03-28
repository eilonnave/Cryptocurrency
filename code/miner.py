# -*- coding: utf-8 -*-
class Miner:
    def __init__(self, wallet):
        """
        constructor
        """
        self.wallet = wallet

    def mine(self):
        """
        mines new block in the
        block chain
        """
        self.wallet.block_chain.add_new_block(self.wallet.address)