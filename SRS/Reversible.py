import Base
from Shortcut import Shortcut

class Reversible(Shortcut):

  """A fully reversible Sender Rewriting Scheme

See SRS for details of the standard SRS subclass interface.
This module provides the methods compile() and parse(). It operates
without store."""

  def compile(self,sendhost,senduser):
    timestamp = self.timestamp_create()
    # This has to be done in compile, because we might need access
    # to it for storing in a database.
    hash = self.hash_create(timestamp,sendhost,senduser)
    # Note that there are 4 fields here and that sendhost may
    # not contain a + sign. Therefore, we do not need to escape
    # + signs anywhere in order to reverse this transformation.
    return Base.SRS0TAG + self.separator + \
	Base.SRSSEP.join((hash,timestamp,sendhost,senduser))
