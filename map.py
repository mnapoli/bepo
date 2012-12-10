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

import xkb, dead_keys, codecs, unicodedata
from terminators import terminators, combiningTerminators, spaceTerminators


fullMapTmpl = keyboardTemplate = u"""
  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────╔═════════╗
  │ %(TLDE_shift)s %(TLDE_shift_option)s│ %(AE01_shift)s %(AE01_shift_option)s│ %(AE02_shift)s %(AE02_shift_option)s│ %(AE03_shift)s %(AE03_shift_option)s│ %(AE04_shift)s %(AE04_shift_option)s│ %(AE05_shift)s %(AE05_shift_option)s│ %(AE06_shift)s %(AE06_shift_option)s│ %(AE07_shift)s %(AE07_shift_option)s│ %(AE08_shift)s %(AE08_shift_option)s│ %(AE09_shift)s %(AE09_shift_option)s│ %(AE10_shift)s %(AE10_shift_option)s│ %(AE11_shift)s %(AE11_shift_option)s│ %(AE12_shift)s %(AE12_shift_option)s║         ║
  │ %(TLDE)s %(TLDE_option)s│ %(AE01)s %(AE01_option)s│ %(AE02)s %(AE02_option)s│ %(AE03)s %(AE03_option)s│ %(AE04)s %(AE04_option)s│ %(AE05)s %(AE05_option)s│ %(AE06)s %(AE06_option)s│ %(AE07)s %(AE07_option)s│ %(AE08)s %(AE08_option)s│ %(AE09)s %(AE09_option)s│ %(AE10)s %(AE10_option)s│ %(AE11)s %(AE11_option)s│ %(AE12)s %(AE12_option)s║ <--     ║
  ╔═══════╗─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─╚══╦══════╣
  ║  |<-  ║ %(AD01_shift)s %(AD01_shift_option)s│ %(AD02_shift)s %(AD02_shift_option)s│ %(AD03_shift)s %(AD03_shift_option)s│ %(AD04_shift)s %(AD04_shift_option)s│ %(AD05_shift)s %(AD05_shift_option)s│ %(AD06_shift)s %(AD06_shift_option)s│ %(AD07_shift)s %(AD07_shift_option)s│ %(AD08_shift)s %(AD08_shift_option)s│ %(AD09_shift)s %(AD09_shift_option)s│ %(AD10_shift)s %(AD10_shift_option)s│ %(AD11_shift)s %(AD11_shift_option)s│ %(AD12_shift)s %(AD12_shift_option)s║   |  ║
  ║  ->|  ║ %(AD01)s %(AD01_option)s│ %(AD02)s %(AD02_option)s│ %(AD03)s %(AD03_option)s│ %(AD04)s %(AD04_option)s│ %(AD05)s %(AD05_option)s│ %(AD06)s %(AD06_option)s│ %(AD07)s %(AD07_option)s│ %(AD08)s %(AD08_option)s│ %(AD09)s %(AD09_option)s│ %(AD10)s %(AD10_option)s│ %(AD11)s %(AD11_option)s│ %(AD12)s %(AD12_option)s║ <-'  ║
  ╠═══════╩╗───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───╚╗     ║
  ║        ║ %(AC01_shift)s %(AC01_shift_option)s│ %(AC02_shift)s %(AC02_shift_option)s│ %(AC03_shift)s %(AC03_shift_option)s│ %(AC04_shift)s %(AC04_shift_option)s│ %(AC05_shift)s %(AC05_shift_option)s│ %(AC06_shift)s %(AC06_shift_option)s│ %(AC07_shift)s %(AC07_shift_option)s│ %(AC08_shift)s %(AC08_shift_option)s│ %(AC09_shift)s %(AC09_shift_option)s│ %(AC10_shift)s %(AC10_shift_option)s│ %(AC11_shift)s %(AC11_shift_option)s│ %(BKSL_shift)s %(BKSL_shift_option)s║     ║
  ║  CAPS  ║ %(AC01)s %(AC01_option)s│ %(AC02)s %(AC02_option)s│ %(AC03)s %(AC03_option)s│ %(AC04)s %(AC04_option)s│ %(AC05)s %(AC05_option)s│ %(AC06)s %(AC06_option)s│ %(AC07)s %(AC07_option)s│ %(AC08)s %(AC08_option)s│ %(AC09)s %(AC09_option)s│ %(AC10)s %(AC10_option)s│ %(AC11)s %(AC11_option)s│ %(BKSL)s %(BKSL_option)s║     ║
  ╠══════╦═╝──┬─┴──┬─┴──┬─┴─══─┴──┬─┴──┬─┴─══─┴──┬─┴──┬─┴──┬─┴──╔══════╩═════╣
  ║   ^  ║ %(LSGT_shift)s %(LSGT_shift_option)s│ %(AB01_shift)s %(AB01_shift_option)s│ %(AB02_shift)s %(AB02_shift_option)s│ %(AB03_shift)s %(AB03_shift_option)s│ %(AB04_shift)s %(AB04_shift_option)s│ %(AB05_shift)s %(AB05_shift_option)s│ %(AB06_shift)s %(AB06_shift_option)s│ %(AB07_shift)s %(AB07_shift_option)s│ %(AB08_shift)s %(AB08_shift_option)s│ %(AB09_shift)s %(AB09_shift_option)s│ %(AB10_shift)s %(AB10_shift_option)s║     ^      ║
  ║   |  ║ %(LSGT)s %(LSGT_option)s│ %(AB01)s %(AB01_option)s│ %(AB02)s %(AB02_option)s│ %(AB03)s %(AB03_option)s│ %(AB04)s %(AB04_option)s│ %(AB05)s %(AB05_option)s│ %(AB06)s %(AB06_option)s│ %(AB07)s %(AB07_option)s│ %(AB08)s %(AB08_option)s│ %(AB09)s %(AB09_option)s│ %(AB10)s %(AB10_option)s║     |      ║
  ╠══════╩╦═══╧══╦═╧═══╦╧════╧════╧════╧════╧════╧═╦══╧══╦═╧════╬═════╦══════╣
  ║       ║      ║     ║ %(SPCE_shift)s            %(SPCE_shift_option)s            ║     ║      ║     ║      ║
  ║ Ctrl  ║ WinG ║ Alt ║ %(SPCE)s            %(SPCE_option)s            ║AltGr║ WinD ║WinM ║ Ctrl ║
  ╚═══════╩══════╩═════╩═══════════════════════════╩═════╩══════╩═════╩══════╝
"""

mainChars = u"$\"«»()_+-/*=%^,.'#1234567890@BÉPOÈ!VDLJZWAUIE?CTSRNMÇÊÀYH:K;QGXF—<>[]|&`¨€~\{}…ÆŒÙ°"

available = set()

out = codecs.open(sys.argv[2], "w", "utf8")
print >> out, u"* Complète"
fullMapValues = {}
for k, v in xkb.tmplValues.iteritems():
   v = terminators.get( v, v )
   if v == "":
     v = " "
   fullMapValues[k] = v
   available.add(v)
out.write( fullMapTmpl % fullMapValues )

print >> out 
print >> out 
print >> out, u"* Simplifiée"
fullMapValues = {}
for k, v in xkb.tmplValues.iteritems():
   v = terminators.get( v, v )
   if v == "":
     v = " "
   if ("_option" not in k and v in mainChars) or ("_option" in k and v in mainChars.lower()) or ("_shift" in k and k.count("_") == 1) or (k.count("_") == 0 and xkb.tmplValues[k+"_shift"] != v.upper()):
     fullMapValues[k] = v
   else:
     fullMapValues[k] = u" "
out.write( fullMapTmpl % fullMapValues )

print >> out 
print >> out 
print >> out, "* Capslock"
fullMapValues = {}
for k, v in xkb.tmplValues.iteritems():
   v = terminators.get( v, v )
   if v == "":
     v = " "
   if "_capslock" in k:
     k = k.replace("_capslock", "")
     fullMapValues[k] = v
     available.add(v)
out.write( fullMapTmpl % fullMapValues )

# find the dead keys used here
dks = set()
for v in xkb.tmplValues.itervalues():
  if terminators.has_key(v):
    dks.add(v)
    available.add(terminators[v])
    available.add(combiningTerminators[v])

for m in sorted(dks):
  deadName = "dead_" + m.replace("ringabove", "abovering")
  fullMapValues = {}
  for k in xkb.tmplValues.iterkeys():
    fullMapValues[k] = u' '
  print >> out
  print >> out
  print >> out, "* %s" % deadName
  for k, mods in sorted(dead_keys.dc):
    if mods == (m,) and dead_keys.dc.has_key((k, ())):
      k2 = dead_keys.dc[k, ()]
      v2 = dead_keys.dc[k, mods]
      for k3, v3 in xkb.tmplValues.iteritems():
        if v3 == k2:
          fullMapValues[k3] = v2      
          available.add(v2)
    elif m in mods:
      K = (k, tuple(a for a in mods if a != m))
      if dead_keys.dc.has_key(K):
        k2 = dead_keys.dc[K]
        v2 = dead_keys.dc[k, mods]
        for k3, v3 in xkb.tmplValues.iteritems():
          if v3 == k2:
            fullMapValues[k3] = v2      
            available.add(v2)
  for k, v in xkb.tmplValues.iteritems():
    if "_capslock" not in k and "_command" not in k:
      if v == u" ":
        fullMapValues[k] = spaceTerminators[m]
      elif v == m:
        fullMapValues[k] = terminators[m]
      elif v == u" ":
        fullMapValues[k] = combiningTerminators[m]
  out.write( fullMapTmpl % fullMapValues )

for i, m1 in enumerate(sorted(dks)):
  for m2 in sorted(dks)[i+1:]:
    fullMapValues = {}
    for k in xkb.tmplValues.iterkeys():
      fullMapValues[k] = u' '
    display = False
    for k, mods in sorted(dead_keys.dc):
      if mods == (m1, m2) and dead_keys.dc.has_key((k, ())):
        k2 = dead_keys.dc[k, ()]
        v2 = dead_keys.dc[k, mods]
        for k3, v3 in xkb.tmplValues.iteritems():
          if v3 == k2:
            fullMapValues[k3] = v2      
            available.add(v2)
            display = True
    if display:
      print >> out
      print >> out
      print >> out, "* %s" % " & ".join("dead_" + m.replace("ringabove", "abovering") for m in (m1, m2))
      out.write( fullMapTmpl % fullMapValues )

print >> out
print >> out
print >> out, u" * Caractères disponibles"
print >> out
print >> out, len(available), u"caractères."
print >> out
for c in sorted(available):
  print >> out, u"%s\t%s" % ( c, unicodedata.name(unicode(c), "pas dans unicode "+unicodedata.unidata_version) )
