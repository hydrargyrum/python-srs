import bsddb
import time
import Base
from cPickle import dumps, loads

class DB(Base.SRS):
  """A MLDBM based Sender Rewriting Scheme

SYNOPSIS

	import SRS
	srs = SRS.DB(Database='/var/run/srs.db', ...)

DESCRIPTION

See SRS.py for details of the standard SRS subclass interface.
This module provides the methods compile() and parse().

This module requires one extra parameter to the constructor, a filename
for a Berkeley DB_File database.

BUGS

This code relies on not getting collisions in the cryptographic
hash. This can and should be fixed.

The database is not garbage collected."""

  def __init__(self,database='/var/run/srs.db',hashlength=20,*args,**kw):
    Base.SRS.__init__(self,hashlength=hashlength,*args,**kw)
    assert database, "No database specified for SRS.DB"
    self.dbm = bsddb.btopen(database,'c')

  def compile(self,sendhost,senduser):
    ts = time.time()

    data = dumps((ts,sendhost,senduser))

    # We rely on not getting collisions in this hash.
    hash = self.hash_create(sendhost,senduser)

    self.dbm[hash] = data

    # Note that there are 4 fields here and that sendhost may
    # not contain a + sign. Therefore, we do not need to escape
    # + signs anywhere in order to reverse this transformation.
    return Base.SRS0TAG + self.separator + hash

  def parse(self,user):
    user,m = self.srs0re.subn('',user,1)
    assert m, "Reverse address does not match %s." % self.srs0re.pattern

    hash = user
    data = self.dbm[hash]
    ts,sendhost,senduser = loads(data)

    assert self.hash_verify(hash,sendhost,senduser), "Invalid hash"

    assert self.time_check(ts), "Invalid timestamp"

    return (sendhost, senduser)
