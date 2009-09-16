#!/usr/bin/env python

import socket
import BaseHTTPServer
import CGIHTTPServer

if __name__ == '__main__':
    port = 80
    server = None
    while not server:
        try:
            server = BaseHTTPServer.HTTPServer(('', port),
                CGIHTTPServer.CGIHTTPRequestHandler)
        except socket.error:
            print 'Error serving on port ' + str(port) + '.'
            print 'You may want to run as a super user.'
            if port < 8000:
                port += 8000
            else:
                port += 1000
            print 'Attempting to serve on port ' + str(port) + ' instead.'
    server.serve_forever()
