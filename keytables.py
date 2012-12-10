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


header = r"""# bepo"""

charToCtrl = {
  "a": "^A",
  "b": "^B",
  "c": "^C",
  "d": "^D",
  "e": "^E",
  "f": "^F",
  "g": "^G",
  "h": r"'\b'",
  "i": r"'\t'",
  "j": r"'\n'",
  "k": r"'\v'",
  "l": "^L",
  "m": "^M",
  "n": "^N",
  "o": "^O",
  "p": "^P",
  "q": "^Q",
  "r": "^R",
  "s": "^S",
  "t": "^T",
  "u": "^U",
  "v": "^V",
  "w": "^W",
  "x": "^X",
  "y": "^Y",
  "z": "^Z",
  "\\": "^\\", 
  "]": "^]", 
  "^": "^^", 
  "_": "^_",
  "@": "^@",
}

deadNames = {
  "grave": "fa_grave",
  "acute": "fa_acute",
  "circumflex": "fa_cflex",
  "tilde": "fa_tilde",
  "diaeresis": "fa_umlaut",
  "cedilla": "fa_cedilla",
}

def chrRepr(s):
  if len(s) == 1:
    if ord(s) < 127:
      return "'%s'" % s
    else:
      return str(ord(s))
  return s

def escape(c):
  if c == "'":
    return "'\\''"
  if c == '"':
    return "'\"'"
  if c == " ":
    return "' '"
  return c

out = file(sys.argv[2], "w")

print >> out, header

f = file("keys.conf")
for l in f:
  if l.startswith("#") or len(l.strip()) == 0:
    continue
  k  = l.split("\t")[0]
  scanCode  = l.split("\t")[6]
  if not xkb.tmplValues.has_key(k):
    continue
  
#                                                         alt
# scan                       cntrl          alt    alt   cntrl lock
# code  base   shift  cntrl  shift  alt    shift  cntrl  shift state
  s = "key "+str(int(scanCode))+"\t "
  for m, prefix in [("", "base"), ("_shift", "shift"), ("_capslock", "caps"), (None, "ctrl"), ("_option", "altg")]:
    if m is not None:
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
          term = codecs.encode(terminators[v], "iso-8859-15")
        except:
          term = "nop"
      elif terminators.has_key(v):
        print "unsupported", "dead_"+v
        term = "nop"
        try:
          cl = codecs.encode(terminators[v], "iso-8859-15")
        except:
          cl = "nop"
      s += prefix+" "+escape(cl)+" "
    else:
      # this is the control modifier. We have to choose a single control char to send which correspond
      # to one of the 4 characters on the key.
      cc = "nop"
      for cm in ["_shift_option", "_option", "_shift", ""]:
        cv = xkb.tmplValues[k+cm]
        cv = terminators.get(cv, cv)
        if charToCtrl.has_key(cv):
          if cc != "nop" and cc != charToCtrl[cv]:
            print "ctrl already found for", k, cc, "- using", charToCtrl[cv], "instead."
          cc = charToCtrl[cv]
      s += prefix+" "+escape(cc)+" "
   
  print >> out, s

