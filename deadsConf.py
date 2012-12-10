#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# produit le fichier dead.conf
#
# Copyright (C) 2008 Gaëtan Lehmann <gaetan.lehmann@jouy.inra.fr>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#


import dead_keys, compose, sys, defaults, re

defaults.xkbFile = sys.argv[1]

import xkb
from terminators import terminators, combiningTerminators, spaceTerminators

# find the dead keys used here
dks = set()
for v in xkb.tmplValues.itervalues():
  if terminators.has_key(v):
    dks.add(v)

composeDeadKeys = {}
# parse compose to find the chars not supported xkb with the dead keys

fCompose = file(defaults.composeFile)

for l in fCompose:
  if not l.startswith("XCOMM") and not l.startswith("##") and "<Multi_key>" not in l and len(l.strip()) != 0:# and "<KP_" not in l and "<underbar>" not in l and "<rightcaret>" not in l and "<leftshoe>" not in l and "<leftcaret>" not in l and "<rightshoe>" not in l and "<U223C>" not in l:
    seq = re.findall('<([^ ]+)>', l.split(":")[0])
    seq = [compose.upperUnicode(s) for s in seq]
    if compose.areSupportedChars(seq):
      c = l.split(":")[1].split()[1]
      k = tuple(compose.char(n) for n in seq)
      composeDeadKeys[k] = compose.char(c)
# print composeDeadKeys

f = file(sys.argv[2], "w")

for m in sorted([m for m in dead_keys.dmm if len(m) == 1]):
  if m[0] in dks:
    comm = u""
  else:
    comm = u"#"
  deadName = "dead_" + m[0].replace("ringabove", "abovering")
  print >> f, "# %s" % deadName
  print >> f
  for k, mods in sorted(dead_keys.dc):
    if mods == m and dead_keys.dc.has_key((k, ())):
      ck = (m[0], dead_keys.dc[k, ()])
      inCompose = composeDeadKeys.has_key(ck)
      if inCompose:
        tag = "L!"
        if composeDeadKeys[ck] != dead_keys.dc[k, mods]:
          print ck
      else:
        tag = ""
      print >> f, "%s%s%s\t%s\t%s" % (comm, tag, deadName, compose.name(dead_keys.dc[k, ()]), compose.name(dead_keys.dc[k, mods]))
    elif m[0] in mods:
      K = (k, tuple(a for a in mods if a != m[0]))
      if dead_keys.dc.has_key(K):
        ck = (m[0], dead_keys.dc[K])
        inCompose = composeDeadKeys.has_key(ck)
        if inCompose:
          tag = "L!"
          if composeDeadKeys[ck] != dead_keys.dc[k, mods]:
            print ck
        else:
          tag = ""
        print >> f, "%s%s%s\t%s\t%s" % (comm, tag, deadName, compose.name(dead_keys.dc[K]), compose.name(dead_keys.dc[k, mods]))
  
  # terminators
  if composeDeadKeys.has_key((m[0], m[0])):
    tag = "L!"
    if composeDeadKeys[(m[0], m[0])] != terminators[m[0]]:
      print m[0], m[0]
  else:
    tag = ""
  print >> f, "%s%s%s\t%s\t%s" % (comm, tag, deadName, deadName, compose.name(terminators[m[0]]))
  
  if composeDeadKeys.has_key((m[0], u" ")):
    tag = "L!"
    if composeDeadKeys[(m[0], u" ")] != terminators[m[0]]:
      print m[0], "nobreakspace"
  else:
    tag = ""
  print >> f, "%s%s%s\t%s\t%s" % (comm, tag, deadName, "nobreakspace", compose.name(combiningTerminators[m[0]]))
  
  if composeDeadKeys.has_key((m[0], u" ")):
    tag = "L!"
    if composeDeadKeys[(m[0], u" ")] != spaceTerminators[m[0]]:
      print "Warning:", m[0], "space is different in Compose:", composeDeadKeys[(m[0], u" ")], spaceTerminators[m[0]]
  else:
    tag = ""
  print >> f, "%s%s%s\t%s\t%s" % (comm, tag, deadName, "space", compose.name(spaceTerminators[m[0]]))
  
  print >> f

# double dead_keys
for m in sorted([m for m in dead_keys.dmm if len(m) == 2]):
  if m[0] in dks and m[1] in dks:
    comm = u""
  else:
    comm = u"#"
  deadNames = tuple("dead_" + m1.replace("ringabove", "abovering") for m1 in m)
  print >> f, "# %s" % " & ".join(deadNames)
  print >> f
  for k, mods in sorted(dead_keys.dc):
    if mods == m and dead_keys.dc.has_key((k, ())):
      # first couple
      ck = (m[0], m[1], dead_keys.dc[k, ()])
      inCompose = composeDeadKeys.has_key(ck)
      if inCompose:
        tag = "L!"
        if composeDeadKeys[ck] != dead_keys.dc[k, mods]:
          print ck
      else:
        tag = ""
      print >> f, "%s%s%s\t%s\t%s\t%s" % (comm, tag, deadNames[0], deadNames[1], compose.name(dead_keys.dc[k, ()]), compose.name(dead_keys.dc[k, mods]))

      # second couple
      ck = (m[1], m[0], dead_keys.dc[k, ()])
      inCompose = composeDeadKeys.has_key(ck)
      if inCompose:
        tag = "L!"
        if composeDeadKeys[ck] != dead_keys.dc[k, mods]:
          print ck
      else:
        tag = ""
      print >> f, "%s%s%s\t%s\t%s\t%s" % (comm, tag, deadNames[1], deadNames[0], compose.name(dead_keys.dc[k, ()]), compose.name(dead_keys.dc[k, mods]))
  
  print >> f
