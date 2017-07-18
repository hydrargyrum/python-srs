divert(-1)
#
# Copyright (c) 2004 Alain Knaff (derived from work by asarian-host.net)
#	All rights reserved.
# Copyright (c) 1988, 1993
#	The Regents of the University of California.  All rights reserved.
#
# By using this file, you agree to the terms and conditions set
# forth in the LICENSE file which can be found at the top level of
# the sendmail distribution.
#
#
divert(0)
VERSIONID(`$Id: pysrs.m4,v 1.1 2004/03/23 20:36:26 stuart Exp $')

LOCAL_CONFIG
# Forward SRS program map
Kmake_srs program /usr/bin/envfrom2srs.py
# Reverse SRS program map
Kreverse_srs program /usr/bin/srs2envtol.py

ifdef(`_ARG_',define(`SRS_DOMAIN',_ARG_))
# "To" address is SRS
ifdef(`SRS_DOMAIN',`dnl
Kis_srs regex CONCAT(`^<?SRS[01]=.*@',`SRS_DOMAIN',`\.?>?$')
',`dnl
Kis_srs regex ^<?SRS[01]=.*
')dnl

ifdef(`NO_SRS_FILE', `dnl
# Class of destination mailers not needing SRS
F{noSrsMailers}-o NO_SRS_FILE %[^\#]
')dnl

LOCAL_RULESETS

SEnvFromSMTP
R$+		$: $>MakeSrs $1		make SRS

SIsSrs
# Answers YES or NO whether the address in parameter is srs or not
R$*				$: $( is_srs $1 $)
R$@				$@ YES
R$*				$@ NO


SMakeSrs
#
# Prevent SRS encapsulation if "To" address is SRS
R$*				$: $1 $>IsSrs $&u
R$* YES 			$@ $1
R$* NO				$: $1
ifdef(`NO_SRS_FROM_LOCAL',`dnl
#
# Prevent SRS encapsulation if "From" address is local
# (With a local from address, the forwarder mail will pass any SPF checks
# anyways, so why bother with SRS?)
R$* < @ $=w > $*		$@ $1 < @ $2 > $3
R$* < @ $=w . > $*		$@ $1 < @ $2 . > $3
')dnl
ifdef(`NO_SRS_FILE',`dnl
#
# If destination mailer is in non-SRS list, do not apply SRS
# This is intended for handling communication between secondary MX and
# primary MX
R$*				$: $&h $| $1
R$={noSrsMailers} $| $*		$@ $2
R$* $| $*			$: $2
')dnl
R$*				$: $(make_srs $1 $)

SReverseSrs
R$*				$: $1 $>IsSrs $1
R$* NO				$@ $1
R$* YES				$@ $(reverse_srs $1 $)

SParseLocal=98
R$*				$: $>ReverseSrs $1
