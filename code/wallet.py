# -*- coding: utf-8 -*-
from encryption import EncryptionSet
from Crypto.PublicKey import *
from Crypto.Hash import *
from blockchain import BlockChain


class Wallet(EncryptionSet):
    def __init__(self, private_key, block_chain):
        """
        constructor
        """
        super(Wallet, self).__init__(private_key)
        self.address = SHA256.new(self.public_key.exportKey())
        self.block_chain = block_chain

    def can_unlock_output(self, transaction_output):
        """
        the function checks if the wallet
        can unlock the output
        :param transaction_output: an output from a transaction
        :returns: true if the output can be unlocked and
        the proof,
        otherwise false
        """
        unlock_address = transaction_output.address
        if unlock_address != self.address:
            return False
        """
        code that verefies the signature
        """
        signature = ''
        return True, (signature, self.public_key)

    def was_output_spent(self, transaction_to_check, output_index):
        """
        the function checks if the given output
        was spent by going throw the block_chain
        :param transaction_to_check: a transaction that contains the
        output to check
        :param output_index: the index of the output
        inside the transaction
        :returns: true if the output was spent
        and false otherwise
        """
        for block in self.block_chain.chain:
            for transaction in block.transactions:
                for transaction_input in transaction.inputs:
                    if transaction_input.transaction_id == \
                            transaction_to_check.transaction_id:
                        if transaction_input.output_index == output_index:
                            return True



def new_wallet(block_chain):
    """
    the function creates new wallet
    and returns it
    :param block_chain: the block_chain that the wallet
    is belong to
    :returns: the new wallet
    """
    private_key = RSA.generate(2048)
    wallet = Wallet(private_key, block_chain)
    return wallet


if __name__ == "__main__":
    block_chain = BlockChain()
    w1 = new_wallet(block_chain)
    pub1 = w1.public_key.exportKey()
    w2 = new_wallet(block_chain)
    pub2 = w2.public_key.exportKey()
    w3 = new_wallet(block_chain)
    pub3 = w3.public_key.exportKey()
    assert pub1 != pub2
    assert pub1 != pub3
    assert pub2 != pub3