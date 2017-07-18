#! /usr/bin/env python
# 
# $Id: setup.py,v 1.4 2002/05/06 06:32:07 anthonybaxter Exp $
#

import sys,os

sys.path.insert(0,os.getcwd())

from distutils.core import setup

import SRS

setup(
        #-- Package description
        name = 'pysrs',
        license = 'Python license',
        version = SRS.__version__,
        description = 'Python SRS library',
        long_description = """Python SRS library:
""",
        author = 'Shevek (Perl version) and Stuart Gathman', 
        author_email = 'stuart@bmsi.com',
        url = 'http://bmsi.com/python/srs.html',
        packages = ['SRS'],
	scripts = ['envfrom2srs.py','srs2envtol.py']
)
