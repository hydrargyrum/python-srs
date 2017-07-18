#!/usr/bin/python2.3

import SRS
import sys
import re

# No funny business in our output, please

sys.stderr.close()

secret = 'shhhh!'

def reverse(old_address):
  srs = SRS.new(secret=secret,maxage=8,hashlength=8)

  # Munge ParseLocal recipient in the same manner as required
  # in EnvFromSMTP.

  use_address = re.compile(r'[<>]').sub('',old_address)
  use_address = re.compile(r'\.$').sub('',use_address)

  # Just try and reverse the address. If we succeed, return this
  # new address; else, return the old address (quoted if it was
  # a piped alias).

  try:
    use_address = srs.reverse(use_address)
    while True:
      try:
	use_address = srs.reverse(use_address)
      except: break
    return use_address.replace('@','<@',1)+'.>'
  except:
    if use_address.startswith('|'):
      return '"%s"' % old_address
    else:
      return old_address

print reverse(sys.argv[1])
