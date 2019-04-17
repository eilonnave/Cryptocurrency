# -*- coding: utf-8 -*-
import sqlite3
from references import References
from abc import abstractmethod, ABCMeta
from block import BLOCK_STRUCTURE, \
    BLOCKS_TABLE_NAME, \
    Block
from transaction import *
from encryption import *
from blockchain import BlockChain
EXTRACT_ALL_QUERY = 'select * from '


class DB(object):
    __metaclass__ = ABCMeta

    def __init__(self, reference):
        """
        constructor
        """
        self.connection = None
        self.cursor = None
        self.reference = reference
        self.create_connection()

    def create_connection(self):
        """
        creates new connection to the data
        base
        """
        self.connection = sqlite3.connect(self.reference)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """
        closes the connection and the cursor
        """
        self.cursor.close()
        self.connection.close()

    @abstractmethod
    def insert(self, obj):
        """
        the function inserts object to the database
        :param obj: the object to insert
        """
        pass

    @abstractmethod
    def extract(self, line_index):
        """
        the function extracts from the
        data base the object from the given line
        index
        :param line_index: the line index of the
        object to extract
        :returns: the extracted object
        """
        pass


class Table:
    def __init__(self, connection, cursor, table_name, structure):
        """
        constructor
        """
        self.connection = connection
        self.cursor = cursor
        self.table_name = table_name
        self.structure = structure
        self.create_table()

    def create_table(self):
        """
        creates the table in the data base
        if it does not exist
        """
        query = 'create table if not exists ' \
                ''+self.table_name+' ' \
                                   ''+self.structure
        self.cursor.execute(query)
        self.connection.commit()

    def insert(self, serialized_obj):
        """
        the function inserts object to the table
        :param serialized_obj: the object to insert
        """
        self.cursor.execute('insert into '
                            ''+self.table_name+' values ?'
                                               '', serialized_obj)
        self.connection.commit()


class BlockChainDB(DB):
    def __init__(self):
        """
        constructor
        """
        super(BlockChainDB, self).__init__(
            References().get_block_chain_reference())
        self.blocks_table = Table(self.connection,
                                  self.cursor,
                                  BLOCKS_TABLE_NAME,
                                  BLOCK_STRUCTURE)
        self.transactions_table = Table(self.connection,
                                        self.cursor,
                                        TRANSACTIONS_TABLE_NAME,
                                        TRANSACTION_STRUCTURE
                                        )
        self.inputs_table = Table(self.connection,
                                  self.cursor,
                                  INPUTS_TABLE_NAME,
                                  INPUT_STRUCTURE)
        self.outputs_table = Table(self.connection,
                                   self.cursor,
                                   OUTPUTS_TABLE_NAME,
                                   OUTPUT_STRUCTURE)

    def insert(self, block):
        # insert the block
        self.blocks_table.insert(block.serialize())

        # insert the transactions
        block_number = block.number
        for transaction in block.transactions:
            self.transactions_table.insert(
                transaction.serialize(block_number))
            transaction_number = transaction.transaction_id
            # insert the inputs
            for transaction_input in transaction.inputs:
                self.inputs_table.insert(
                    transaction_input.serialize(transaction_number))
            # insert the outputs
            for transaction_output in transaction.outputs:
                self.outputs_table.insert(
                    transaction_output.serialize(transaction_number))

    def extract(self, line_index):
        query = \
            EXTRACT_ALL_QUERY\
            + self.blocks_table.table_name\
            + ' where number=?'
        self.cursor.execute(query, line_index)
        block_list = self.cursor.fetchall()[0]

        block_number = block_list[0]
        transactions = self.extract_transactions(block_number)
        block_list.append(transactions)

        return Block.deserialize(block_list)

    def extract_inputs(self, transaction_number):
        """
        the function extracts from the database
        all the inputs matching to the transaction
        number
        :param transaction_number: the transaction number
        that the inputs should be belong to
        :returns: the list of the inputs
        """
        inputs = []
        query = \
            EXTRACT_ALL_QUERY\
            + self.inputs_table.table_name\
            + 'where transaction_number=?'
        self.cursor.execute(query, transaction_number)
        inputs_lists = self.cursor.fetchall()
        for input_list in inputs_lists:
            inputs.append(Input.deserialize(input_list))
        return inputs

    def extract_outputs(self, transaction_number):
        """
        the function extracts from the database
        all the outputs matching to the transaction
        number
        :param transaction_number: the transaction number
        that the outputs should be belong to
        :returns: the list of the outputs
        """
        outputs = []
        query = \
            EXTRACT_ALL_QUERY\
            + self.outputs_table.table_name\
            + 'where transaction_number=?'
        self.cursor.execute(query, transaction_number)
        outputs_lists = self.cursor.fetchall()
        for output_list in outputs_lists:
            outputs.append(Output.deserialize(output_list))
        return outputs

    def extract_transactions(self, block_number):
        """
        the function extracts from the database
        all the transactions matching to the block
        number
        :param block_number: the block number
        that the transactions should be belong to
        :returns: the list of the transactions
        """
        # extract the transactions
        query = \
            EXTRACT_ALL_QUERY\
            + self.transactions_table.table_name\
            + 'where block_number=?'
        self.cursor.execute(query, block_number)
        block_transactions = self.cursor.fetchall()

        # build the transactions using the inputs and
        # the outputs
        transactions = []
        for transaction_list in block_transactions:
            transaction_number = transaction_list[0]
            inputs = self.extract_inputs(transaction_number)
            outputs = self.extract_outputs(transaction_number)
            transaction_list.append(inputs)
            transaction_list.append(outputs)
            transactions.append(Transaction.deserialize(transaction_list))
        return transactions

if __name__ == "__main__":
    encryption_set = EncryptionSet(RSA.generate(2048))
    db = BlockChainDB()