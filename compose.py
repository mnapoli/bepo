#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Parser pour Compose
#
# Copyright (C) 2008 Gaëtan Lehmann <gaetan.lehmann@jouy.inra.fr>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#


import unicodedata, re, sys, defaults

def ishex(s):
  for c in s:
    if c not in "0123456789abcdefABCDEF":
      return False
  return True
  
fKeysymdef = file(defaults.keysymdefFile)

regexp = re.compile(r'#define XK_([^ ]+).*U\+([0-9A-Fa-f]+)')

composeNames = {}

for l in fKeysymdef:
  res = regexp.match(l)
  if res:
    name = res.group(1)
    c = res.group(2)
    try:
      C = unichr( int(c, 16) )
      composeNames[name] = C
    except:
      print l
      pass
      
# some missing chars
composeNames["combining_acute"] = u"́"
composeNames["combining_belowdot"] = u"̣"
composeNames["combining_grave"] = u"̀"
composeNames["combining_tilde"] = u"̃"
composeNames["NoSymbol"] = u""
composeNames["VoidSymbol"] = u""
# dead keys
composeNames["dead_abovedot"] = u"abovedot"
composeNames["dead_abovering"] = u"ringabove"
composeNames["dead_acute"] = u"acute"
composeNames["dead_belowdot"] = u"belowdot"
composeNames["dead_breve"] = u"breve"
composeNames["dead_caron"] = u"caron"
composeNames["dead_cedilla"] = u"cedilla"
composeNames["dead_circumflex"] = u"circumflex"
composeNames["dead_dasia"] = u"dasia"
composeNames["dead_diaeresis"] = u"diaeresis"
composeNames["dead_doubleacute"] = u"doubleacute"
composeNames["dead_grave"] = u"grave"
composeNames["dead_horn"] = u"horn"
composeNames["dead_macron"] = u"macron"
composeNames["dead_ogonek"] = u"ogonek"
composeNames["dead_psili"] = u"psili"
composeNames["dead_tilde"] = u"tilde"
composeNames["dead_stroke"] = u"stroke"
composeNames["UFDD0"] = u"stroke"
composeNames["dead_currency"] = u"currency"
composeNames["UFDD1"] = u"currency"
composeNames["Multi_key"] = u"Multi_key"
composeNames["dead_greek"] = u"greek"
composeNames["UFDD2"] = u"greek"
composeNames["dead_commabelow"] = u"commabelow"
composeNames["UFDD3"] = u"commabelow"
composeNames["dead_hook"] = u"hook"
composeNames["dead_horn"] = u"horn"
composeNames["dead_belowdot"] = u"belowdot"

composeChars = {}
for name, C in composeNames.iteritems():
  composeChars[C] = name
# force oslash name
composeChars[u"ø"] = "oslash"

from terminators import terminators


def char(k):
  if k == '':
    return u''
  if not composeNames.has_key(k) and k[0] == 'U' and len(k) == 5 and ishex(k[1:]):
    C = unichr(int(k[1:], 16))
    k = k.upper()
    if composeChars.has_key(C):
      return C
    composeNames[k] = C
    composeChars[C] = k
  return composeNames[k]

def name(c):
  if composeChars.has_key(c):
    return composeChars[c]
  k = u"U"+repr(c)[4:-1].rjust(4, '0').upper()
  composeNames[k] = c
  composeChars[c] = k
  return k

def isSupportedChar(k):
  if k[0] == 'U' and len(k) == 5 and ishex(k[1:]):
    return True
  return composeNames.has_key(k)
  
def areSupportedChars(ks):
  for k in ks:
    if not isSupportedChar(k):
      return False
  return True

def upperUnicode(k):
  if k[0] == 'U' and 5 <= len(k) <= 6 and ishex(k[1:]):
    return k.upper()
  return k
  
fCompose = file(defaults.composeFile)

states = set()
outputs = {}

for l in fCompose:
  if l.startswith("<Multi_key>") and "<KP_" not in l and "<underbar>" not in l and "<rightcaret>" not in l and "<leftshoe>" not in l and "<leftcaret>" not in l and "<rightshoe>" not in l and "<U223C>" not in l:
    seq = re.findall('<([^ ]+)>', l.split(":")[0])
    seq = [upperUnicode(s) for s in seq]
    if areSupportedChars(seq):
      for i in range(1, len(seq)):
        s = tuple(seq[:i])
        states.add(s)
      c = l.split(":")[1].split()[1]
      outputs[tuple(seq)] = char(c)
    
#    for k in seq:
#      if k[0] == 'U' and len(k) == 5 and ishex(k[1:]):
#        k = unichr(int(k[1:], 16))
#      keys.add(k)

statesByAction = {}
for S in states:
  a = S[-1]
  s = S[:-1]
  sset = statesByAction.get(a, set())
  sset.add(s)
  statesByAction[a] = sset


outputsByAction = {}
for S in outputs.keys():
  a = S[-1]
  s = S[:-1]
  sset = outputsByAction.get(a, set())
  sset.add((s, outputs[S]))
  outputsByAction[a] = sset

charActions = {}
for a in set(statesByAction.keys() + outputsByAction.keys()):
  if charActions.has_key(char(a)) :
    print (a, char(a), charActions[char(a)])
  charActions[char(a)] = a
# print charActions[u'(']
# sys.exit()

if __name__ == "__main__":
  for a in sorted(set(statesByAction.keys() + outputsByAction.keys()) ):
    C = char(a)
    if C:
      print u'    <action id="%s">' % C
      if statesByAction.has_key(a):
        for s in sorted(statesByAction[a]):
          print u'      <when state="%s" next="%s"/>' % ('_'.join(s), '_'.join(s+(a,)))
      if outputsByAction.has_key(a):
        for s, c in sorted(outputsByAction[a]):
          print u'      <when state="%s" output="%s"/>' % ('_'.join(s), c)
      print u'    </action>'

      
  print '''
    <action id="Multikey">
      <when state="none" next="Multikey"/>
    </action>
  '''

  print "  <terminators>"
  for ss in sorted(states):
    C = ''.join([terminators.get(char(s), char(s)) for s in ss])
    s = '_'.join(list(ss))
    print '    <when state="%s" output="%s"/>' % (s, C)
  print "  </terminators>"
  
  