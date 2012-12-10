#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Produit une carte de touches à partir d'un fichier xkb
#
# Copyright (C) 2008 Gaëtan Lehmann <gaetan.lehmann@jouy.inra.fr>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#

import defaults, sys
defaults.xkbFile = sys.argv[1]

import xkb, dead_keys, codecs
from terminators import terminators


fullMapTmpl = keyboardTemplate = u"""%(TLDE)s%(AE01)s%(AE02)s%(AE03)s%(AE04)s%(AE05)s%(AE06)s%(AE07)s%(AE08)s%(AE09)s%(AE10)s%(AE11)s%(AE12)s
%(AD01)s%(AD02)s%(AD03)s%(AD04)s%(AD05)s%(AD06)s%(AD07)s%(AD08)s%(AD09)s%(AD10)s%(AD11)s%(AD12)s
%(AC01)s%(AC02)s%(AC03)s%(AC04)s%(AC05)s%(AC06)s%(AC07)s%(AC08)s%(AC09)s%(AC10)s%(AC11)s%(BKSL)s
%(LSGT)s%(AB01)s%(AB02)s%(AB03)s%(AB04)s%(AB05)s%(AB06)s%(AB07)s%(AB08)s%(AB09)s%(AB10)s
%(TLDE_shift)s%(AE01_shift)s%(AE02_shift)s%(AE03_shift)s%(AE04_shift)s%(AE05_shift)s%(AE06_shift)s%(AE07_shift)s%(AE08_shift)s%(AE09_shift)s%(AE10_shift)s%(AE11_shift)s%(AE12_shift)s
%(AD01_shift)s%(AD02_shift)s%(AD03_shift)s%(AD04_shift)s%(AD05_shift)s%(AD06_shift)s%(AD07_shift)s%(AD08_shift)s%(AD09_shift)s%(AD10_shift)s%(AD11_shift)s%(AD12_shift)s
%(AC01_shift)s%(AC02_shift)s%(AC03_shift)s%(AC04_shift)s%(AC05_shift)s%(AC06_shift)s%(AC07_shift)s%(AC08_shift)s%(AC09_shift)s%(AC10_shift)s%(AC11_shift)s%(BKSL_shift)s
%(LSGT_shift)s%(AB01_shift)s%(AB02_shift)s%(AB03_shift)s%(AB04_shift)s%(AB05_shift)s%(AB06_shift)s%(AB07_shift)s%(AB08_shift)s%(AB09_shift)s%(AB10_shift)s
"""

fullMapValues = {}
for k, v in xkb.tmplValues.iteritems():
   v = terminators.get( v, v )
   if v == "":
     v = " "
   fullMapValues[k] = v
out = codecs.open(sys.argv[2], "w", "utf8")
out.write( fullMapTmpl % fullMapValues )
