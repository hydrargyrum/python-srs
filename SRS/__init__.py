__version__ = '0.30'

from Base import SRS
from Guarded import Guarded
from Shortcut import Shortcut
from Reversible import Reversible
from DB import DB

def new(secret=None,*args,**kw):
  return Guarded(secret,*args,**kw)

