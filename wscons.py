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

# keycode 2 = ampersand 1 
# keycode 3 = eacute 2 asciitilde
# keycode 4 = quotedbl 3 numbersign
# keycode 5 = apostrophe 4 braceleft
# keycode 6 = parenleft 5 bracketleft
# keycode 7 = minus 6 bar
# keycode 8 = egrave 7 grave
# keycode 9 = underscore 8 backslash
# keycode 10 = ccedilla 9 asciicircum
# keycode 11 = agrave 0 at
# keycode 12 = parenright degree bracketright
# keycode 13 = equal plus braceright
# keycode 16 = a  
# keycode 17 = z  
# keycode 18 = e  
# keycode 19 = r  
# keycode 20 = t  
# keycode 21 = y  
# keycode 22 = u  
# keycode 23 = i  
# keycode 24 = o  
# keycode 25 = p
# keycode 26 = dead_circumflex dead_diaeresis 
# keycode 27 = dollar sterling currency
# keycode 30 = q  
# keycode 31 = s  
# keycode 32 = d  
# keycode 33 = f  
# keycode 34 = g  
# keycode 35 = h  
# keycode 36 = j  
# keycode 37 = k  
# keycode 38 = l  
# keycode 39 = m  
# keycode 40 = ugrave percent 
# keycode 41 = twosuperior asciitilde 
# keycode 43 = asterisk mu 
# keycode 44 = semicolon bar adiaeresis Adiaeresis
# keycode 45 = x  
# keycode 46 = c  
# keycode 47 = v  
# keycode 48 = b  
# keycode 49 = n  
# keycode 50 = comma question 
# keycode 51 = semicolon period 
# keycode 52 = colon slash 
# keycode 53 = exclam section 
# keycode 57 = space  

header = u"""keycode 1 = Cmd_Debugger Escape 
keycode 14 = Cmd_ResetEmul Delete 
keycode 15 = Tab  
keycode 28 = Return  
keycode 29 = Cmd1 Control_L 
keycode 42 = Shift_L  
keycode 54 = Shift_R  
keycode 55 = KP_Multiply  
keycode 56 = Cmd2 Alt_L 
keycode 58 = Caps_Lock  
keycode 59 = Cmd_Screen0 f1 
keycode 60 = Cmd_Screen1 f2 
keycode 61 = Cmd_Screen2 f3 
keycode 62 = Cmd_Screen3 f4 
keycode 63 = Cmd_Screen4 f5 
keycode 64 = Cmd_Screen5 f6 
keycode 65 = Cmd_Screen6 f7 
keycode 66 = Cmd_Screen7 f8 
keycode 67 = Cmd_Screen8 f9 
keycode 68 = Cmd_Screen9 f10 
keycode 69 = Num_Lock  
keycode 70 = Hold_Screen  
keycode 71 = KP_Home KP_7
keycode 72 = KP_Up KP_8
keycode 73 = KP_Prior KP_9
keycode 74 = KP_Subtract
keycode 75 = KP_Left KP_4
keycode 76 = KP_Begin KP_5
keycode 77 = KP_Right KP_6
keycode 78 = KP_Add
keycode 79 = KP_End KP_1
keycode 80 = KP_Down KP_2
keycode 81 = KP_Next KP_3
keycode 82 = KP_Insert KP_0
keycode 83 = KP_Delete KP_Decimal
keycode 86 = less greater 
keycode 87 = f11  
keycode 88 = f12  
keycode 127 = Pause
keycode 156 = KP_Enter  
keycode 157 = Control_R  
keycode 170 = Print_Screen  
keycode 181 = KP_Divide  
keycode 183 = Print_Screen  
keycode 184 = Mode_switch Multi_key 
keycode 199 = Home  
keycode 200 = Up  
keycode 201 = Prior 
keycode 203 = Left  
keycode 205 = Right  
keycode 207 = End  
keycode 208 = Down  
keycode 209 = Next 
keycode 210 = Insert  
keycode 211 = Delete  
keycode 219 = Meta_L  
keycode 220 = Meta_R  
keycode 221 = Menu  
"""

namesData = {
  0x0000: "nul",
  0x0001: "Control_a",
  0x0002: "Control_b",
  0x0003: "Control_c",
  0x0004: "Control_d",
  0x0005: "Control_e",
  0x0006: "Control_f",
  0x0007: "Control_g",
  0x0008: "BackSpace",
  0x0009: "Tab",
  0x000a: "Linefeed",
  0x000b: "Control_k",
  0x000c: "Control_l",
  0x000d: "Control_m",
  0x000e: "Control_n",
  0x000f: "Control_o",
  0x0010: "Control_p",
  0x0011: "Control_q",
  0x0012: "Control_r",
  0x0013: "Control_s",
  0x0014: "Control_t",
  0x0015: "Control_u",
  0x0016: "Control_v",
  0x0017: "Control_w",
  0x0018: "Control_x",
  0x0019: "Control_y",
  0x001a: "Control_z",
  0x001b: "Escape",
  0x001c: "Control_backslash",
  0x001d: "Control_bracketrig",
  0x001e: "Control_asciicircu",
  0x001f: "Control_underscore",
  0x0020: "space",
  0x0021: "exclam",
  0x0022: "quotedbl",
  0x0023: "numbersign",
  0x0024: "dollar",
  0x0025: "percent",
  0x0026: "ampersand",
  0x0027: "apostrophe",
  0x0028: "parenleft",
  0x0029: "parenright",
  0x002a: "asterisk",
  0x002b: "plus",
  0x002c: "comma",
  0x002d: "minus",
  0x002e: "period",
  0x002f: "slash",
  0x0030: "0",
  0x0031: "1",
  0x0032: "2",
  0x0033: "3",
  0x0034: "4",
  0x0035: "5",
  0x0036: "6",
  0x0037: "7",
  0x0038: "8",
  0x0039: "9",
  0x003a: "colon",
  0x003b: "semicolon",
  0x003c: "less",
  0x003d: "equal",
  0x003e: "greater",
  0x003f: "question",
  0x0040: "at",
  0x0041: "A",
  0x0042: "B",
  0x0043: "C",
  0x0044: "D",
  0x0045: "E",
  0x0046: "F",
  0x0047: "G",
  0x0048: "H",
  0x0049: "I",
  0x004a: "J",
  0x004b: "K",
  0x004c: "L",
  0x004d: "M",
  0x004e: "N",
  0x004f: "O",
  0x0050: "P",
  0x0051: "Q",
  0x0052: "R",
  0x0053: "S",
  0x0054: "T",
  0x0055: "U",
  0x0056: "V",
  0x0057: "W",
  0x0058: "X",
  0x0059: "Y",
  0x005a: "Z",
  0x005b: "bracketleft",
  0x005c: "backslash",
  0x005d: "bracketright",
  0x005e: "asciicircum",
  0x005f: "underscore",
  0x0060: "grave",
  0x0061: "a",
  0x0062: "b",
  0x0063: "c",
  0x0064: "d",
  0x0065: "e",
  0x0066: "f",
  0x0067: "g",
  0x0068: "h",
  0x0069: "i",
  0x006a: "j",
  0x006b: "k",
  0x006c: "l",
  0x006d: "m",
  0x006e: "n",
  0x006f: "o",
  0x0070: "p",
  0x0071: "q",
  0x0072: "r",
  0x0073: "s",
  0x0074: "t",
  0x0075: "u",
  0x0076: "v",
  0x0077: "w",
  0x0078: "x",
  0x0079: "y",
  0x007a: "z",
  0x007b: "braceleft",
  0x007c: "bar",
  0x007d: "braceright",
  0x007e: "asciitilde",
  0x007f: "Delete",
  0x00a0: "nobreakspace",
  0x00a1: "exclamdown",
  0x00a2: "cent",
  0x00a3: "sterling",
  0x00a5: "yen",
  0x00a7: "section",
  0x00a9: "copyright",
  0x00aa: "ordfeminine",
  0x00ab: "guillemotleft",
  0x00ac: "notsign",
  0x00ad: "hyphen",
  0x00ae: "registered",
  0x00af: "macron",
  0x00b0: "degree",
  0x00b1: "plusminus",
  0x00b2: "twosuperior",
  0x00b3: "threesuperior",
  0x00b5: "mu",
  0x00b6: "paragraph",
  0x00b7: "periodcentered",
  0x00b9: "onesuperior",
  0x00ba: "masculine",
  0x00bb: "guillemotright",
  0x00bf: "questiondown",
  0x00c0: "Agrave",
  0x00c1: "Aacute",
  0x00c2: "Acircumflex",
  0x00c3: "Atilde",
  0x00c4: "Adiaeresis",
  0x00c5: "Aring",
  0x00c6: "AE",
  0x00c7: "Ccedilla",
  0x00c8: "Egrave",
  0x00c9: "Eacute",
  0x00ca: "Ecircumflex",
  0x00cb: "Ediaeresis",
  0x00cc: "Igrave",
  0x00cd: "Iacute",
  0x00ce: "Icircumflex",
  0x00cf: "Idiaeresis",
  0x00d0: "ETH",
  0x00d1: "Ntilde",
  0x00d2: "Ograve",
  0x00d3: "Oacute",
  0x00d4: "Ocircumflex",
  0x00d5: "Otilde",
  0x00d6: "Odiaeresis",
  0x00d7: "multiply",
  0x00d8: "Ooblique",
  0x00d9: "Ugrave",
  0x00da: "Uacute",
  0x00db: "Ucircumflex",
  0x00dc: "Udiaeresis",
  0x00dd: "Yacute",
  0x00de: "THORN",
  0x00df: "ssharp",
  0x00e0: "agrave",
  0x00e1: "aacute",
  0x00e2: "acircumflex",
  0x00e3: "atilde",
  0x00e4: "adiaeresis",
  0x00e5: "aring",
  0x00e6: "ae",
  0x00e7: "ccedilla",
  0x00e8: "egrave",
  0x00e9: "eacute",
  0x00ea: "ecircumflex",
  0x00eb: "ediaeresis",
  0x00ec: "igrave",
  0x00ed: "iacute",
  0x00ee: "icircumflex",
  0x00ef: "idiaeresis",
  0x00f0: "eth",
  0x00f1: "ntilde",
  0x00f2: "ograve",
  0x00f3: "oacute",
  0x00f4: "ocircumflex",
  0x00f5: "otilde",
  0x00f6: "odiaeresis",
  0x00f7: "division",
  0x00f8: "oslash",
  0x00f9: "ugrave",
  0x00fa: "uacute",
  0x00fb: "ucircumflex",
  0x00fc: "udiaeresis",
  0x00fd: "yacute",
  0x00fe: "thorn",
  0x00ff: "ydiaeresis",
  0x00a4: "currency",
  0x00bd: "onehalf",
  0x00bc: "onequarter",
}

defaultDeads = ["grave", "acute", "circumflex", "tilde", "diaeresis", "ringabove", "cedilla"]

for i in range(256):
  if not namesData.has_key(i):
    namesData[i] = hex(i)
#  print i, namesData[i]

names = {}
for c, n in namesData.iteritems():
  names[chr(c)] = n
#print names

out = file(sys.argv[2], "w")

print >> out, header,

f = file("keys.conf")
for l in f:
  if l.startswith("#") or len(l.strip()) == 0:
    continue
  k, scanCode  = l.split("\t")[:2]
  if not xkb.tmplValues.has_key(k):
    continue

  s = "keycode %s =" % str(int(scanCode, 16))
  for m in ["", "_shift", "_option", "_shift_option"]:
      v = xkb.tmplValues[k+m]
    #  v = terminators.get( v, v )
      try:
       cl = codecs.encode(v, "iso-8859-15")
       name = names[cl]
      except:
    #    if terminators.has_key(v):
        if v in defaultDeads:
          name = "dead_" + v.replace("ringabove", "abovering")
        else:
          name = "voidSymbol"
      s += " "+name
      
  print >> out, s

