# $Log: __init__.py,v $
# Revision 1.3  2004/03/23 20:36:39  stuart
# Version 0.30.6
#
# Revision 1.2  2004/03/22 18:20:19  stuart
# Missing import
#
# Revision 1.1.1.1  2004/03/19 05:23:13  stuart
# Import to CVS
#
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

__version__ = '0.30.6'

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
import Guarded

def new(secret=None,*args,**kw):
  return Guarded.Guarded(secret,*args,**kw)
