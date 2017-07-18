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

__version__ = '0.30.4'

__all__= [
  'Base',
  'Guarded',
  'Shortcut',
  'Reversible',
  'Daemon',
  'DB',
  'new',
  'SRS0TAG',
  'SRS1TAG',
  'SRSSEP',
  'SRSHASHLENGTH',
  'SRSMAXAGE',
  '__version__'
]

SRS0TAG = 'SRS0'
SRS1TAG = 'SRS1'
SRSSEP = '='
SRSHASHLENGTH = 4
SRSMAXAGE = 21

#from Base import SRS
#from Guarded import Guarded
#from Shortcut import Shortcut
#from Reversible import Reversible
#from Daemon import Daemon
#from DB import DB

def new(secret=None,*args,**kw):
  return Guarded.Guarded(secret,*args,**kw)

