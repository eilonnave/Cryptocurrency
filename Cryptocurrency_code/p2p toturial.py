# -*- coding: utf-8 -*-
import socket


class Peer:
    def __init__(self, max_peers, server_port, my_id=None, server_host=None):
        self.debug = 0
        self.max_peers = int(max_peers)
        self.server_port = int(server_port)

        # If not supplied, the host name/IP address will be determined
        # by attempting to connect to an Internet host like Google.
        if server_host:
            self.server_host = server_host
        else:
            self.__initserverhost()

        # If not supplied, the peer id will be composed of the host address
        # and port number
        if my_id:
            self.my_id = my_id
        else:
            self.my_id = '%s:%d' % (self.server_host, self.server_port)

        # list (dictionary/hash table) of known peers
        self.peers = {}

        # used to stop the main loop
        self.shutdown = False

        self.handlers = {}
        self.router = None

    @staticmethod
    def make_server_socket(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind('', port)
        s.listen(5)
        return s

    def main_loop(self):
        s = self.make_server_socket(self.server_port)
        s.settimeout(2)
        print 'Server started: %s (%s:%d)' % (self.my_id, self.server_host, self.server_port)
        while not self.shutdown:
            try:
                print 'Listening for connections...'


if __name__ == '__main__':
    pass