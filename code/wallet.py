# -*- coding: utf-8 -*-
from encryption import EncryptionSet
from Crypto.PublicKey import *
from Crypto.Hash import *
from blockchain import BlockChain
from transaction import *


class Wallet(EncryptionSet):
    def __init__(self, private_key, block_chain):
        """
        constructor
        """
        super(Wallet, self).__init__(private_key)
        self.address = SHA256.new(self.public_key.exportKey())
        self.block_chain = block_chain
        self.unspent_outputs = []
        self.update_unspent_outputs()
        self.balance = 0
        self.update_balance()

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
            return False, ''
        """
        code that verifies the signature
        """
        signature = ''
        return True, (signature, self.public_key)

    def is_unspent_output(self, transaction_to_check, output_index):
        """
        the function checks if the given output
        was spent by going throw the block_chain
        :param transaction_to_check: a transaction that contains the
        output to check
        :param output_index: the index of the output
        inside the transaction
        :returns: false if the output was spent
        and true otherwise
        """
        for block in self.block_chain.chain:
            for transaction in block.transactions:
                for transaction_input in transaction.inputs:
                    if transaction_input.transaction_id == \
                            transaction_to_check.transaction_id:
                        if transaction_input.output_index == output_index:
                            return False
        return True
        """
        need to be done by unspent transactions data base data base
        """

    def update_balance(self):
        """
        the function calculate and
        updates the wallet's balance
        """
        balance = 0
        for unspent_output in self.unspent_outputs:
            balance += unspent_output.output.value
        self.balance = balance

    def update_unspent_outputs(self):
        """
        the function finds all the unspent
        outputs which belongs to the wallet
        and updates it
        """
        unspent_outputs = []
        for block in self.block_chain.chain:
            for transaction in block.transactions:
                output_index = 0
                for transaction_output in transaction.outputs:
                    can_unlock, proof = self.can_unlock_output(transaction_output)
                    if can_unlock and self.is_unspent_output(
                            transaction, output_index):
                        unspent_outputs.append(UnspentOutput(
                            transaction_output,
                            transaction.transaction_id,
                            output_index,
                            proof))
                    output_index += 1
        self.unspent_outputs = unspent_outputs

    def create_transaction(self, amount, recipient_address):
        """
        the functions creates transaction which
        contains the amount of coins to send
        the recipient address, the function implements
        the transaction in the block chain
        :param amount: the amount to send
        :param recipient_address: the address to send the
        coins to
        :returns: true if the transaction has been
        implemented to the block chain and false if
        there is a problem with it
        """
        self.update_unspent_outputs()
        self.update_balance()
        if amount > self.balance:
            print 'not enough money to send\n' \
                  'money to send: '+str(amount)+'\n current balance: '+str(self.balance)
            return False
        new_transaction = Transaction([], [])
        sending_amount = 0
        for unspent_output in self.unspent_outputs:
            new_transaction.add_input(Input(
                unspent_output.transaction_id,
                unspent_output.output_index,
                unspent_output.proof))
            sending_amount += unspent_output.output.value
            if sending_amount >= amount:
                break
        new_transaction.add_output(
            Output(sending_amount,
                   recipient_address))
        """
        need to insert change option
        """
        self.block_chain.add_transaction(new_transaction)


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
    test_block_chain = BlockChain()
    w1 = new_wallet(test_block_chain)
    pub1 = w1.public_key.exportKey()
    w2 = new_wallet(test_block_chain)
    pub2 = w2.public_key.exportKey()
    w3 = new_wallet(test_block_chain)
    pub3 = w3.public_key.exportKey()
    assert pub1 != pub2
    assert pub1 != pub3
    assert pub2 != pub3