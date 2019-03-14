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
    assert miner.wallet.balance > 0


def main():
    test1()


if __name__ == '__main__':
    main()