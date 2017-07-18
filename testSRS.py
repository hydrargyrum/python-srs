import unittest
from SRS import *
import SRS.Base as Base

class SRSTestCase(unittest.TestCase):
  
  def setUp(self):
    Base.SRS0TAG = 'ALT0'
    Base.SRS1TAG = 'ALT1'

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
    self.failUnless(srsaddr.startswith(Base.SRS0TAG))
    srsaddr1 = srs.forward(srsaddr,'third.com')
    #print srsaddr1
    self.failUnless(srsaddr1.startswith(Base.SRS1TAG))
    srsaddr2 = srs.forward(srsaddr1,'fourth.com')
    #print srsaddr2
    self.failUnless(srsaddr2.startswith(Base.SRS1TAG))
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
    self.failUnless(srsaddr.startswith(Base.SRS0TAG))
    srsaddr1 = srs.forward(srsaddr,'third.com')
    #print srsaddr1
    self.failUnless(srsaddr1.startswith(Base.SRS0TAG))
    srsaddr2 = srs.forward(srsaddr1,'fourth.com')
    #print srsaddr2
    self.failUnless(srsaddr2.startswith(Base.SRS0TAG))
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
    self.failUnless(srsaddr.startswith(Base.SRS0TAG))
    srsaddr1 = srs.forward(srsaddr,'third.com')
    #print srsaddr1
    self.failUnless(srsaddr1.startswith(Base.SRS0TAG))
    srsaddr2 = srs.forward(srsaddr1,'fourth.com')
    #print srsaddr2
    self.failUnless(srsaddr2.startswith(Base.SRS0TAG))
    addr = srs.reverse(srsaddr2)
    self.assertEqual(srsaddr1,addr)
    addr = srs.reverse(srsaddr1)
    self.assertEqual(srsaddr,addr)
    addr = srs.reverse(srsaddr)
    self.assertEqual(sender,addr)

def suite(): return unittest.makeSuite(SRSTestCase,'test')

if __name__ == '__main__':
    unittest.main()
