#!/usr/bin/python2.3

import SRS
import re
from ConfigParser import ConfigParser, DuplicateSectionError

# get SRS parameters from milter configuration
cp = ConfigParser({
  'secret': 'shhhh!',
  'maxage': '8',
  'hashlength': '8',
  'fwdomain': 'mydomain.com',
  'separator': '='
})
cp.read(["/etc/mail/pysrs.cfg"])
try:
  cp.add_section('srs')
except DuplicateSectionError:
  pass
srs = SRS.new(
  secret=cp.get('srs','secret'),
  maxage=cp.getint('srs','maxage'),
  hashlength=cp.getint('srs','hashlength'),
  separator=cp.get('srs','separator'),
  alwaysrewrite=True	# pysrs.m4 can skip calling us for local domains
)
fwdomain = cp.get('srs','fwdomain')
del cp

# Our original envelope-from may look funny on entry
# of this Ruleset:
#
#     admin<@asarian-host.net.>
#
# We need to preprocess it some:
def forward(old_address):
  if old_address == '<@>':
    return old_address
  use_address = re.compile(r'[<>]').sub('',old_address)
  use_address = re.compile(r'\.$').sub('',use_address)

  # Ok, first check whether we already have a signed SRS address;
  # if so, just return the old address: we do not want to double-sign
  # by accident!
  #
  # Else, gimme a valid SRS signed address, munge it back the way
  # sendmail wants it at this point; or just return the old address,
  # in case nothing went.

  try:
    new_address = srs.reverse(use_address)
    return old_address
  except:
    try:
      new_address = srs.forward(use_address,fwdomain)
      return new_address.replace('@','<@',1)+'.>'
    except:
      return old_address

if __name__ == "__main__":
  import sys
  # No funny business in our output, please
  sys.stderr.close()
  print forward(sys.argv[1])
