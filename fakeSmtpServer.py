#! /usr/bin/python

# Fake SMTP server to see the traffic
# We should develop an API running on different port
# to be able to stop it, force to return error or
# to get last send message in the tests.

__author__ = "Martin Malek <martin.malek@nodus.cz>"
__date__ = "$Dec 12, 2013 9:14:25 PM$"

import asyncore
import smtpd
import threading
import time
import SocketServer
import subprocess

class FakeSMTPServer(smtpd.SMTPServer):
    """Dummy fake smtp server"""

    def __init__(self, * args, ** kwargs):
        print "Running fake smtp server on port 25"
        smtpd.SMTPServer.__init__(self, * args, ** kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data):
        subprocess.Popen(['notify-send', "Fake smtp server", "From %s | To %s" % (mailfrom, rcpttos)])
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print data
        print "\n\n"
        c = Communication()
        if not c.get_status():
		    return '554 bad recipients'

	def print_api_message(self, message):
		print message

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()
        print "%s wrote: " % self.client_address[0]
        print data
        c = Communication()
        c.set_status(False)
        #self.request.send(self.data.upper())


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class _CommunicationData(object):

    nextStatus = True

    def __init__(self):
        pass

    def set_status(self, value):
        self.nextStatus = value

    def get_status(self):
        return self.nextStatus


_communicationData = _CommunicationData()

def Communication():
    return _communicationData

if __name__ == "__main__":
    server_A = ThreadedTCPServer(('localhost', 5559), ThreadedTCPRequestHandler)
    server_A_thread = threading.Thread(target=server_A.serve_forever)
    server_A_thread.setDaemon(True)
    server_A_thread.start()

    smtp_server = FakeSMTPServer(('localhost', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()

