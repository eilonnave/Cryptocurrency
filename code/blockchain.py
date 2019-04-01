# -*- coding: utf-8 -*-
from block import Block
from transaction import Transaction, Input, Output
BLOCK_HASH_SIZE = 256
REWORD = 50


class BlockChain:
    def __init__(self, chain, logger):
        """
        constructor
        """
        self.chain = chain
        self.transactions_pool = []
        self.logger = logger

    @classmethod
    def new_block_chain(cls, logger):
        """
        factory method
        """
        return cls([], logger)

    def add_new_block(self, miner_address):
        """
        the function adds new block to the chain
        and rewards the miner
        :param miner_address: the miner address
        to reward
        """
        number = len(self.chain)

        # handle genesis block
        if number == 0:
            prev = '0'*32
        else:
            prev = self.chain[-1].hash_code

        # transaction that rewards the miner
        transaction_input = Input(str(len(self.chain)), -1, miner_address)
        """
        for checking that the block is legit, I must add
        checking that in the input the implementation of
        the chain's length is right
        """
        transaction_output = Output(REWORD, miner_address)
        new_transaction = Transaction([transaction_input],
                                      [transaction_output])
        self.add_transaction(new_transaction)

        # create the block
        block = Block(number, prev, self.transactions_pool)
        self.logger.info('Mining new block')
        block.mine_block()

        # set the block chain
        self.chain.append(block)
        self.transactions_pool = []
        self.logger.info('The new bock was added to the block chain')

    def add_transaction(self, transaction):
        """
        the function adds new transaction
        to the transactions pool
        :param transaction: new transaction to add
        """
        self.transactions_pool.append(transaction)
