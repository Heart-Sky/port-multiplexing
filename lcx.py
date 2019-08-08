#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import threading
import logging
import optparse


class PipeThread(threading.Thread):

    def __init__(self, source_fd, target_fd, data, flag):
        super(PipeThread, self).__init__()
        self.logger = logging.getLogger('PipeThread')
        self.source_fd = source_fd
        self.target_fd = target_fd
        self.source_addr = self.source_fd.getpeername()
        self.target_addr = self.target_fd.getpeername()
        self.data = data
        self.flag = flag

    def run(self):
        while True:
            try:
                if len(self.data) > 0 and self.flag:
                    data = self.data
                    self.data = ''
                else:
                    data = self.source_fd.recv(4096)
                print data
                if len(data) > 0:
                    self.logger.debug('read  %04i from %s:%d', len(data),
                                      self.source_addr[0], self.source_addr[1])
                    sent = self.target_fd.send(data)
                    self.logger.debug('write %04i to   %s:%d', sent,
                                      self.target_addr[0], self.target_addr[1])
                else:
                    break
            except socket.error:
                break
        self.logger.debug('connection %s:%d is closed.', self.source_addr[0],
                          self.source_addr[1])
        self.logger.debug('connection %s:%d is closed.', self.target_addr[0],
                          self.target_addr[1])
        self.source_fd.close()
        self.target_fd.close()


class Forwarder(object):

    def __init__(self, ip, port, remoteip, remoteport, backlog=5):
        self.localip = ip
        self.localport = port
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(backlog)

    def run(self):
        while True:
            client_fd, client_addr = self.sock.accept()
            data = client_fd.recv(4096)
            if data[:4] == 'GET ' or data[:4] == 'POST':
                self.rport = self.localport
            else:
                self.rport = self.remoteport
            target_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_fd.connect((self.remoteip, self.rport))

            threads = [
                PipeThread(client_fd, target_fd, data, 1),
                PipeThread(target_fd, client_fd, data, 0)
            ]

            for t in threads:
                t.setDaemon(True)
                t.start()

    def __del__(self):
        self.sock.close()


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option(
        '-l', '--local-ip', dest='local_ip',
        help='Local IP address to bind to')
    parser.add_option(
        '-p', '--local-port',
        type='int', dest='local_port',
        help='Local port to bind to')
    parser.add_option(
        '-r', '--remote-ip', dest='remote_ip',
        help='Local IP address to bind to')
    parser.add_option(
        '-P', '--remote-port',
        type='int', dest='remote_port',
        help='Remote port to bind to')
    parser.add_option(
        '-v', '--verbose',
        action='store_true', dest='verbose',
        help='verbose')
    opts, args = parser.parse_args()

    if len(sys.argv) == 1 or len(args) > 0:
        parser.print_help()
        exit()

    if not (opts.local_ip and opts.local_port and opts.remote_ip and opts.remote_port):
        parser.print_help()
        exit()

    if opts.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.CRITICAL

    logging.basicConfig(level=log_level, format='%(name)-11s: %(message)s')
    forwarder = Forwarder(opts.local_ip, opts.local_port, opts.remote_ip, opts.remote_port)

    try:
        forwarder.run()
    except KeyboardInterrupt:
        print 'quit'
        exit()