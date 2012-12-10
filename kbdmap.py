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

import xkb, dead_keys, codecs, compose
from terminators import terminators


header = u"""# bepo
#
# common keys first
#                                                         alt
# scan                       cntrl          alt    alt   cntrl lock
# code  base   shift  cntrl  shift  alt    shift  cntrl  shift state
# ------------------------------------------------------------------
  000   nop    nop    nop    nop    nop    nop    nop    nop     O
  001   esc    esc    esc    esc    esc    esc    debug  esc     O
  014   bs     bs     del    del    bs     bs     del    del     O
  015   ht     btab   nop    nop    ht     btab   nop    nop     O
  028   cr     cr     nl     nl     cr     cr     nl     nl      O
  029   lctrl  lctrl  lctrl  lctrl  lctrl  lctrl  lctrl  lctrl   O
  042   lshift lshift lshift lshift lshift lshift lshift lshift  O
  054   rshift rshift rshift rshift rshift rshift rshift rshift  O
  055   '*'    '*'    '*'    '*'    '*'    '*'    '*'    '*'     O
  056   lalt   lalt   lalt   lalt   lalt   lalt   lalt   lalt    O
  058   clock  clock  clock  clock  clock  clock  clock  clock   O
  059   fkey01 fkey13 fkey25 fkey37 scr01  scr11  scr01  scr11   O
  060   fkey02 fkey14 fkey26 fkey38 scr02  scr12  scr02  scr12   O
  061   fkey03 fkey15 fkey27 fkey39 scr03  scr13  scr03  scr13   O
  062   fkey04 fkey16 fkey28 fkey40 scr04  scr14  scr04  scr14   O
  063   fkey05 fkey17 fkey29 fkey41 scr05  scr15  scr05  scr15   O
  064   fkey06 fkey18 fkey30 fkey42 scr06  scr16  scr06  scr16   O
  065   fkey07 fkey19 fkey31 fkey43 scr07  scr07  scr07  scr07   O
  066   fkey08 fkey20 fkey32 fkey44 scr08  scr08  scr08  scr08   O
  067   fkey09 fkey21 fkey33 fkey45 scr09  scr09  scr09  scr09   O
  068   fkey10 fkey22 fkey34 fkey46 scr10  scr10  scr10  scr10   O
  069   nlock  nlock  nlock  nlock  nlock  nlock  nlock  nlock   O
  070   slock  slock  slock  slock  slock  slock  slock  slock   O
  071   fkey49 '7'    '7'    '7'    '7'    '7'    '7'    '7'     N
  072   fkey50 '8'    '8'    '8'    '8'    '8'    '8'    '8'     N
  073   fkey51 '9'    '9'    '9'    '9'    '9'    '9'    '9'     N
  074   fkey52 '-'    '-'    '-'    '-'    '-'    '-'    '-'     N
  075   fkey53 '4'    '4'    '4'    '4'    '4'    '4'    '4'     N
  076   fkey54 '5'    '5'    '5'    '5'    '5'    '5'    '5'     N
  077   fkey55 '6'    '6'    '6'    '6'    '6'    '6'    '6'     N
  078   fkey56 '+'    '+'    '+'    '+'    '+'    '+'    '+'     N
  079   fkey57 '1'    '1'    '1'    '1'    '1'    '1'    '1'     N
  080   fkey58 '2'    '2'    '2'    '2'    '2'    '2'    '2'     N
  081   fkey59 '3'    '3'    '3'    '3'    '3'    '3'    '3'     N
  082   fkey60 '0'    '0'    '0'    '0'    '0'    '0'    '0'     N
  083   del    '.'    '.'    '.'    '.'    '.'    boot   boot    N
  084   nop    nop    nop    nop    nop    nop    nop    nop     O
  085   nop    nop    nop    nop    nop    nop    nop    nop     O
  087   fkey11 fkey23 fkey35 fkey47 scr11  scr11  scr11  scr11   O
  088   fkey12 fkey24 fkey36 fkey48 scr12  scr12  scr12  scr12   O
  089   cr     cr     nl     nl     cr     cr     nl     nl      O
  090   rctrl  rctrl  rctrl  rctrl  rctrl  rctrl  rctrl  rctrl   O
  091   '/'    '/'    '/'    '/'    '/'    '/'    '/'    '/'     O
  092   nscr   pscr   debug  debug  nop    nop    nop    nop     O
  093   ralt   ralt   ralt   ralt   ralt   ralt   ralt   ralt    O
  094   fkey49 fkey49 fkey49 fkey49 fkey49 fkey49 fkey49 fkey49  O
  095   fkey50 fkey50 fkey50 fkey50 fkey50 fkey50 fkey50 fkey50  O
  096   fkey51 fkey51 fkey51 fkey51 fkey51 fkey51 fkey51 fkey51  O
  097   fkey53 fkey53 fkey53 fkey53 fkey53 fkey53 fkey53 fkey53  O
  098   fkey55 fkey55 fkey55 fkey55 fkey55 fkey55 fkey55 fkey55  O
  099   fkey57 fkey57 fkey57 fkey57 fkey57 fkey57 fkey57 fkey57  O
  100   fkey58 fkey58 fkey58 fkey58 fkey58 fkey58 fkey58 fkey58  O
  101   fkey59 fkey59 fkey59 fkey59 fkey59 fkey59 fkey59 fkey59  O
  102   fkey60 paste  fkey60 fkey60 fkey60 fkey60 fkey60 fkey60  O
  103   fkey61 fkey61 fkey61 fkey61 fkey61 fkey61 boot   fkey61  O
  104   slock  saver  slock  saver  susp   nop    susp   nop     O
  105   fkey62 fkey62 fkey62 fkey62 fkey62 fkey62 fkey62 fkey62  O
  106   fkey63 fkey63 fkey63 fkey63 fkey63 fkey63 fkey63 fkey63  O
  107   fkey64 fkey64 fkey64 fkey64 fkey64 fkey64 fkey64 fkey64  O
  108   nop    nop    nop    nop    nop    nop    nop    nop     O
#
# then bepo specific keys
#                                                         alt
# scan                       cntrl          alt    alt   cntrl lock
# code  base   shift  cntrl  shift  alt    shift  cntrl  shift state
# ------------------------------------------------------------------"""

charToCtrl = {
  "a": "soh",
  "b": "stx",
  "c": "etx",
  "d": "eot",
  "e": "enq",
  "f": "ack",
  "g": "bel",
  "h": "bs",
  "i": "ht",
  "j": "nl",
  "k": "vt",
  "l": "np",
  "m": "cr",
  "n": "so",
  "o": "si",
  "p": "dle",
  "q": "dc1",
  "r": "dc2",
  "s": "dc3",
  "t": "dc4",
  "u": "nak",
  "v": "syn",
  "w": "etb",
  "x": "can",
  "y": "em",
  "z": "sub",
  # 27 esc
  "\\": "fs", 
  "]": "gs", 
  "^": "rs", 
  "_": "us",
  # 32 sp 
  # 127 de
}

defaultDeads = ["grave", "acute", "circumflex", "tilde", "diaeresis", "cedilla", "ogonek", "caron", "breve", "doubleacute"]

deadNames = {
  "grave": "dgra",
  "acute": "dacu",
  "circumflex": "dcir",
  "tilde": "dtil",
  "macron": "dmac",
  "breve": "dbre",
  "abovedot": "ddot",
  "diaeresis": "ddia",
  "ringabove": "drin",
  "cedilla": "dced",
  "doubleacute": "ddac",
  "ogonek": "dogo",
  "caron": "dcar",
  "currency": "dapo",
  "stroke": "dsla",
  #"duml",
}

def chrRepr(s):
  if len(s) == 1:
    if ord(s) < 127:
      return "'%s'" % s
    else:
      return str(ord(s))
  return s


out = file(sys.argv[2], "w")

print >> out, header

f = file("keys.conf")
for l in f:
  if l.startswith("#") or len(l.strip()) == 0:
    continue
  k, scanCode  = l.split("\t")[:2]
  if not xkb.tmplValues.has_key(k):
    continue
  
#                                                         alt
# scan                       cntrl          alt    alt   cntrl lock
# code  base   shift  cntrl  shift  alt    shift  cntrl  shift state
  s = "  "+str(int(scanCode, 16)).rjust(3, "0")+"   "
  for m, ctrl in [("", False), ("_shift", False), ("", True), ("_shift", True), ("_option", False), ("_shift_option", False), ("_option", True), ("_shift_option", True)]:
      v = xkb.tmplValues[k+m]
    #  v = terminators.get( v, v )
      if v == "":
        v = "nop"
      try:
       term = "nop"
       cl = codecs.encode(v, "iso-8859-15")
      except:
        cl = "nop"
      
    #    if terminators.has_key(v):
      if deadNames.has_key(v):
        cl = deadNames[v]
        try:
          term = names[codecs.encode(terminators[v], "iso-8859-15")]
        except:
          term = "nop"
      elif terminators.has_key(v):
        print "unsupported", "dead_"+v
        term = "nop"
        try:
          cl = names[codecs.encode(terminators[v], "iso-8859-15")]
        except:
          cl = "nop"
        
          
      if ctrl:
        if charToCtrl.has_key(cl):
          cl = charToCtrl[cl]
        elif charToCtrl.has_key(cl.lower()):
          cl = charToCtrl[cl.lower()]
        elif charToCtrl.has_key(term):
          cl = charToCtrl[term]
        else:
          cl = "nop"
        
      s += chrRepr(cl).ljust(7)
    
  s += " "
  if "ALPHABETIC" in xkb.options[k]:
    s += "C"
  else:
    s += "O"

  print >> out, s


print >> out, """#
# finally, the dead keys
# ex:
#  041   dgra   172	 nop	nop    '|'    '|'    nop    nop     O
#  dgra  '`'  ( 'a' 224 ) ( 'A' 192 ) ( 'e' 232 ) ( 'E' 200 )
#             ( 'i' 236 ) ( 'I' 204 ) ( 'o' 242 ) ( 'O' 210 )
#             ( 'u' 249 ) ( 'U' 217 )"""
			
# find the dead keys used here
dks = set()
for v in xkb.tmplValues.itervalues():
  if terminators.has_key(v):
    dks.add(v)

for m in sorted([m for m in dead_keys.dmm if len(m) == 1]):
  if m[0] not in dks or not deadNames.has_key(m[0]) :
    continue
  
  count = 0
  s = "  %s %s " % (deadNames[m[0]], chrRepr(codecs.encode(terminators[m[0]], "iso-8859-15", 'replace')))
  for k, mods in sorted(dead_keys.dc):
    if mods == m and dead_keys.dc.has_key((k, ())):
      try:
        i = chrRepr(codecs.encode(dead_keys.dc[k, ()], "iso-8859-15"))
        o = chrRepr(codecs.encode(dead_keys.dc[k, mods], "iso-8859-15"))
        if count != 0 and count % 4 == 0:
          s += "\n           "
        s += "( %s %s ) " % (i, o)
        count += 1
      except:
        pass
    elif m[0] in mods:
      K = (k, tuple(a for a in mods if a != m[0]))
      if dead_keys.dc.has_key(K):
        try:
          i = chrRepr(codecs.encode(dead_keys.dc[K], "iso-8859-15"))
          o = chrRepr(codecs.encode(dead_keys.dc[k, mods], "iso-8859-15"))
          if count != 0 and count % 4 == 0:
            s += "\n           "
          s += "( %s %s ) " % (i, o)
          count += 1
        except:
          pass

  print >> out, s
#  if count > 0:
#    print >> out, s
