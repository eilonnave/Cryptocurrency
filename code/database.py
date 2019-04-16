# -*- coding: utf-8 -*-
import sqlite3
from references import References
from abc import abstractmethod, ABCMeta
from block import BLOCK_STRUCTURE, Block, BLOCKS_TABLE_NAME
from transaction import *
from encryption import *


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
    def serialize(self, obj):
        """
        the function serializes the object
        :param obj: the object to serialize
        :returns: the serialize object
        """
        pass

    @abstractmethod
    def deserialize(self, serialize_obj):
        """
        the function deserializes object
        :param serialize_obj: the object to de serialize
        :returns: the deserialized object
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

    def insert(self, obj):
        """
        the function inserts object to the table
        :param obj: the object to insert
        """
        self.cursor.execute('insert into '
                            ''+self.table_name+' values ?'
                                               '', obj.serialize())
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
                                        )




if __name__ == "__main__":
    encryption_set = EncryptionSet(RSA.generate(2048))
    db = BlockChainDB()
    i = Input('111', 1, ('1234', encryption_set.public_key))
    print i.serialize()
    i = [Input('111', 1, ('1234', encryption_set.public_key))]
    o = [Output(43, encryption_set.hash(encryption_set.public_key.exportKey()).hexdigest())]
    t = Transaction(i, o)
    print vars(t)
    print eval(t.serialize())