# -*- coding: utf-8 -*-
from wallet import Wallet
from blockchain import BlockChain
from miner import Miner


def test1():
    """
    tests wallets without p2p network
    """
    block_chain = BlockChain()
    wallet1 = Wallet.new_wallet(block_chain)
    wallet2 = Wallet.new_wallet(block_chain)
    assert wallet1.balance == 0
    assert wallet2.balance == 0
    wallet3 = Wallet.new_wallet(block_chain)
    miner = Miner(wallet3)
    miner.mine()
    first_balance = miner.wallet.get_balance()
    assert first_balance > 0
    assert miner.wallet.create_transaction(miner.wallet.balance, wallet1.address)
    miner.mine()
    assert wallet1.get_balance() == first_balance
    second_balance = miner.wallet.get_balance()
    assert second_balance > 0
    wallet1.create_transaction(wallet1.get_balance(), wallet2.address)
    miner.wallet.create_transaction(second_balance, wallet2.address)
    miner.mine()
    assert wallet2.get_balance() == (first_balance+second_balance)
    assert miner.wallet.get_balance() > 0


if __name__ == '__main__':
    test1()