# $Log$
#
# AUTHOR
# Shevek
# CPAN ID: SHEVEK
# cpan@anarres.org
# http://www.anarres.org/projects/
#
# Translated to Python by stuart@bmsi.com
# http://bmsi.com/python/milter.html
#
# Portions Copyright (c) 2004 Shevek. All rights reserved.
# Portions Copyright (c) 2004 Business Management Systems. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the same terms as Python itself.

import unittest
from SRS.Guarded import Guarded
from SRS.DB import DB
from SRS.Reversible import Reversible
from SRS.Daemon import Daemon
import SRS
import threading
import socket

class SRSTestCase(unittest.TestCase):
  
  def setUp(self):
    # make sure user modified tag works
    SRS.SRS0TAG = 'ALT0'
    SRS.SRS1TAG = 'ALT1'

  # There and back again
  def testGuarded(self):
    srs = Guarded()
    self.assertRaises(AssertionError,srs.forward,
    	'mouse@disney.com','mydomain.com')
    srs.set_secret('shhhh!')
    srs.separator = '+'
    sender = 'mouse@orig.com'
    srsaddr = srs.forward(sender,sender)
    self.assertEqual(srsaddr,sender)
    srsaddr = srs.forward(sender,'second.com')
    #print srsaddr
    self.failUnless(srsaddr.startswith(SRS.SRS0TAG))
    srsaddr1 = srs.forward(srsaddr,'third.com')
    #print srsaddr1
    self.failUnless(srsaddr1.startswith(SRS.SRS1TAG))
    srsaddr2 = srs.forward(srsaddr1,'fourth.com')
    #print srsaddr2
    self.failUnless(srsaddr2.startswith(SRS.SRS1TAG))
    addr = srs.reverse(srsaddr2)
    self.assertEqual(srsaddr,addr)
    addr = srs.reverse(srsaddr1)
    self.assertEqual(srsaddr,addr)
    addr = srs.reverse(srsaddr)
    self.assertEqual(sender,addr)

  def testReversible(self):
    srs = Reversible()
    self.assertRaises(AssertionError,srs.forward,
    	'mouse@disney.com','mydomain.com')
    srs.set_secret('shhhh!')
    srs.separator = '+'
    sender = 'mouse@orig.com'
    srsaddr = srs.forward(sender,sender)
    self.assertEqual(srsaddr,sender)
    srsaddr = srs.forward(sender,'second.com')
    #print srsaddr
    self.failUnless(srsaddr.startswith(SRS.SRS0TAG))
    srsaddr1 = srs.forward(srsaddr,'third.com')
    #print srsaddr1
    self.failUnless(srsaddr1.startswith(SRS.SRS0TAG))
    srsaddr2 = srs.forward(srsaddr1,'fourth.com')
    #print srsaddr2
    self.failUnless(srsaddr2.startswith(SRS.SRS0TAG))
    addr = srs.reverse(srsaddr2)
    self.assertEqual(srsaddr1,addr)
    addr = srs.reverse(srsaddr1)
    self.assertEqual(srsaddr,addr)
    addr = srs.reverse(srsaddr)
    self.assertEqual(sender,addr)

  def testDB(self,database='/tmp/srstest'):
    srs = DB(database=database)
    self.assertRaises(AssertionError,srs.forward,
    	'mouse@disney.com','mydomain.com')
    srs.set_secret('shhhh!')
    sender = 'mouse@orig.com'
    srsaddr = srs.forward(sender,sender)
    self.assertEqual(srsaddr,sender)
    srsaddr = srs.forward(sender,'second.com')
    #print srsaddr
    self.failUnless(srsaddr.startswith(SRS.SRS0TAG))
    srsaddr1 = srs.forward(srsaddr,'third.com')
    #print srsaddr1
    self.failUnless(srsaddr1.startswith(SRS.SRS0TAG))
    srsaddr2 = srs.forward(srsaddr1,'fourth.com')
    #print srsaddr2
    self.failUnless(srsaddr2.startswith(SRS.SRS0TAG))
    addr = srs.reverse(srsaddr2)
    self.assertEqual(srsaddr1,addr)
    addr = srs.reverse(srsaddr1)
    self.assertEqual(srsaddr,addr)
    addr = srs.reverse(srsaddr)
    self.assertEqual(sender,addr)

  def run2(self): # handle two requests
    self.daemon.server.handle_request()
    self.daemon.server.handle_request()

  def sendcmd(self,*args):
    sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    sock.connect(self.sockname)
    sock.send(' '.join(args)+'\n')
    res = sock.recv(128).strip()
    sock.close()
    return res

  def testDaemon(self,sockname='/tmp/srsd',secret="shhhh!"):
    self.sockname = sockname
    self.daemon = Daemon(socket=sockname,secret=secret)
    server = threading.Thread(target=self.run2,name='srsd')
    server.start()
    sender = 'mouse@orig.com'
    srsaddr = self.sendcmd('FORWARD',sender,'second.com')
    addr = self.sendcmd('REVERSE',srsaddr)
    server.join()
    self.assertEqual(sender,addr)

  def testSendmailMap(self):
    import envfrom2srs
    import srs2envtol
    orig = 'mickey<@mouse.com.>'
    newaddr = envfrom2srs.forward('mickey<@mouse.com.>')
    self.failUnless(newaddr.endswith('.>'))
    addr2 = srs2envtol.reverse(newaddr)
    self.assertEqual(addr2,orig)

def suite(): return unittest.makeSuite(SRSTestCase,'test')

if __name__ == '__main__':
    unittest.main()
