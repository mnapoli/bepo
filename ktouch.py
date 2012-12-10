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


fullMapTmpl = keyboardTemplate = u"""# -*- coding: utf-8; -*-
####################################################
#    KTouch
#    Fichier de définition de clavier
####################################################
# Disposition bépo
####################################################
#
#
#  Touches de repos: Cette catégorie recouvre les touches
#  sur lesquelles vos doigts reposent quand vous ne tapez pas.
#
#          Unicode      KeyText  x     y
# 3ème ligne de touches: Touches de repos
FingerKey	%(AC01_code)s	%(AC01)s	18	20
FingerKey	%(AC02_code)s	%(AC02)s	28	20
FingerKey	%(AC03_code)s	%(AC03)s	38	20
FingerKey	%(AC04_code)s	%(AC04)s	48	20
FingerKey	%(AC07_code)s	%(AC07)s	78	20
FingerKey	%(AC08_code)s	%(AC08)s	88	20
FingerKey	%(AC09_code)s	%(AC09)s	98	20
FingerKey	%(AC10_code)s	%(AC10)s	108	20
#
#
#
#  Touches modificatrices: Cette catégorie de touches
#  recouvre les touches dites "de contrôle". Ces touches 
#  seront utilisées plus bas notament pour les majuscules
#  
#               Unicode KeyText         x       y       Width  Height
#
ControlKey	260	Tab	0	10	15	10
ControlKey	13	Enter	138	10	12	20
ControlKey	258	Shift	123	30	27	10
ControlKey	264	AltGr	120	40	15	10
ControlKey	265	Ctrl	135	40	15	10
ControlKey	263	Alt	15	40	15	10
ControlKey	262	Ctrl	0	40	15	10
ControlKey	32	Space	30	40	90	10
ControlKey	257	Shift	0	30	13	10
ControlKey	259	CapsLock	0	20	18	10
ControlKey	8	BackSpace	130	0	20	10
#
#
#  Touches normales: Cette catégories recouvre toutes 
#  les touches por lesquelles vous n'avez pas besoin 
#  de taper autre chose qu'une touche pour écrire. 
#  A priori, ça correspond à toutes les minuscules et 
#  les chiffres (sur un qwerty). Pour cette catégorie, 
#  il faut indiquer avec quel doigt vous allez utiliser 
#  (en indiquant sa touche de repos).
#
#       Unicode KeyText         x       y       FingerKey
# 1ère ligne de touches
NormalKey	%(TLDE_code)s	%(TLDE)s	0	0	%(AC01_code)s
NormalKey	%(AE01_code)s	%(AE01)s	10	0	%(AC01_code)s
NormalKey	%(AE02_code)s	%(AE02)s	20	0	%(AC01_code)s
NormalKey	%(AE03_code)s	%(AE03)s	30	0	%(AC02_code)s
NormalKey	%(AE04_code)s	%(AE04)s	40	0	%(AC03_code)s
NormalKey	%(AE05_code)s	%(AE05)s	50	0	%(AC04_code)s
NormalKey	%(AE06_code)s	%(AE06)s	60	0	%(AC04_code)s
NormalKey	%(AE07_code)s	%(AE07)s	70	0	%(AC07_code)s
NormalKey	%(AE08_code)s	%(AE08)s	80	0	%(AC07_code)s
NormalKey	%(AE09_code)s	%(AE09)s	90	0	%(AC08_code)s
NormalKey	%(AE10_code)s	%(AE10)s	100	0	%(AC09_code)s
NormalKey	%(AE11_code)s	%(AE11)s	110	0	%(AC10_code)s
NormalKey	%(AE12_code)s	%(AE12)s	120	0	%(AC10_code)s
#
# 2ème ligne de touches
NormalKey	%(AD01_code)s	%(AD01)s	15	10	%(AC01_code)s
NormalKey	%(AD02_code)s	%(AD02)s	25	10	%(AC02_code)s
NormalKey	%(AD03_code)s	%(AD03)s	35	10	%(AC03_code)s
NormalKey	%(AD04_code)s	%(AD04)s	45	10	%(AC04_code)s
NormalKey	%(AD05_code)s	%(AD05)s	55	10	%(AC04_code)s
NormalKey	%(AD06_code)s	%(AD06)s	65	10	%(AC07_code)s
NormalKey	%(AD07_code)s	%(AD07)s	75	10	%(AC07_code)s
NormalKey	%(AD08_code)s	%(AD08)s	85	10	%(AC08_code)s
NormalKey	%(AD09_code)s	%(AD09)s	95	10	%(AC09_code)s
NormalKey	%(AD10_code)s	%(AD10)s	105	10	%(AC10_code)s
NormalKey	%(AD11_code)s	%(AD11)s	115	10	%(AC10_code)s
NormalKey	%(AD12_code)s	%(AD12)s	125	10	%(AC10_code)s
#
# 3ème ligne de touches: sauf touches de repos
NormalKey	%(AC05_code)s	%(AC05)s	58	20	%(AC04_code)s
NormalKey	%(AC06_code)s	%(AC06)s	68	20	%(AC07_code)s
NormalKey	%(AC11_code)s	%(AC11)s	118	20	%(AC10_code)s
NormalKey	%(BKSL_code)s	%(BKSL)s	128	20	%(AC10_code)s
#
# 4ème ligne de touches
NormalKey	%(LSGT_code)s	%(LSGT)s	13	30	%(AC01_code)s
NormalKey	%(AB01_code)s	%(AB01)s	23	30	%(AC01_code)s
NormalKey	%(AB02_code)s	%(AB02)s	33	30	%(AC02_code)s
NormalKey	%(AB03_code)s	%(AB03)s	43	30	%(AC03_code)s
NormalKey	%(AB04_code)s	%(AB04)s	53	30	%(AC04_code)s
NormalKey	%(AB05_code)s	%(AB05)s	63	30	%(AC04_code)s
NormalKey	%(AB06_code)s	%(AB06)s	73	30	%(AC07_code)s
NormalKey	%(AB07_code)s	%(AB07)s	83	30	%(AC07_code)s
NormalKey	%(AB08_code)s	%(AB08)s	93	30	%(AC08_code)s
NormalKey	%(AB09_code)s	%(AB09)s	103	30	%(AC09_code)s
NormalKey	%(AB10_code)s	%(AB10)s	113	30	%(AC10_code)s
#
#
#
#
#  Touches cachées: Ce sont les caractères inaccessibles
#  directement. Cela signifie que vous devez utiliser une
#  touche modificatrice pour les taper. A priori, ça 
#  concerne au moins les majuscules.
#
#      Unicode Target  Finger  Control
#Maj: 1ère ligne de touches
HiddenKey	%(TLDE_code)s	%(TLDE_shift_code)s	%(AC01_code)s	258	#%(TLDE_shift)s
HiddenKey	%(AE01_code)s	%(AE01_shift_code)s	%(AC01_code)s	258	#%(AE01_shift)s
HiddenKey	%(AE02_code)s	%(AE02_shift_code)s	%(AC01_code)s	258	#%(AE02_shift)s
HiddenKey	%(AE03_code)s	%(AE03_shift_code)s	%(AC02_code)s	258	#%(AE03_shift)s
HiddenKey	%(AE04_code)s	%(AE04_shift_code)s	%(AC03_code)s	258	#%(AE04_shift)s
HiddenKey	%(AE05_code)s	%(AE05_shift_code)s	%(AC04_code)s	258	#%(AE05_shift)s
HiddenKey	%(AE06_code)s	%(AE06_shift_code)s	%(AC04_code)s	258	#%(AE06_shift)s
HiddenKey	%(AE07_code)s	%(AE07_shift_code)s	%(AC07_code)s	257	#%(AE07_shift)s
HiddenKey	%(AE08_code)s	%(AE08_shift_code)s	%(AC07_code)s	257	#%(AE08_shift)s
HiddenKey	%(AE09_code)s	%(AE09_shift_code)s	%(AC08_code)s	257	#%(AE09_shift)s
HiddenKey	%(AE10_code)s	%(AE10_shift_code)s	%(AC09_code)s	257	#%(AE10_shift)s
HiddenKey	%(AE11_code)s	%(AE11_shift_code)s	%(AC10_code)s	257	#%(AE11_shift)s
HiddenKey	%(AE12_code)s	%(AE12_shift_code)s	%(AC10_code)s	257	#%(AE12_shift)s
#
#      Unicode Target  Finger  Control
#Maj: 2ème ligne de touches
HiddenKey	%(AD01_code)s	%(AD01_shift_code)s	%(AC01_code)s	258	#%(AD01_shift)s
HiddenKey	%(AD02_code)s	%(AD02_shift_code)s	%(AC02_code)s	258	#%(AD02_shift)s
HiddenKey	%(AD03_code)s	%(AD03_shift_code)s	%(AC03_code)s	258	#%(AD03_shift)s
HiddenKey	%(AD04_code)s	%(AD04_shift_code)s	%(AC04_code)s	258	#%(AD04_shift)s
HiddenKey	%(AD05_code)s	%(AD05_shift_code)s	%(AC04_code)s	258	#%(AD05_shift)s
HiddenKey	%(AD06_code)s	%(AD06_shift_code)s	%(AC07_code)s	257	#%(AD06_shift)s
HiddenKey	%(AD07_code)s	%(AD07_shift_code)s	%(AC07_code)s	257	#%(AD07_shift)s
HiddenKey	%(AD08_code)s	%(AD08_shift_code)s	%(AC08_code)s	257	#%(AD08_shift)s
HiddenKey	%(AD09_code)s	%(AD09_shift_code)s	%(AC09_code)s	257	#%(AD09_shift)s
HiddenKey	%(AD10_code)s	%(AD10_shift_code)s	%(AC10_code)s	257	#%(AD10_shift)s
HiddenKey	%(AD11_code)s	%(AD11_shift_code)s	%(AC10_code)s	257	#%(AD11_shift)s
HiddenKey	%(AD12_code)s	%(AD12_shift_code)s	%(AC10_code)s	257	#%(AD12_shift)s
#
#       Unicode   Target  Finger  Control
#Maj: 3ème ligne de touches
HiddenKey	%(AC01_code)s	%(AC01_shift_code)s	%(AC01_code)s	258	#%(AC01_shift)s
HiddenKey	%(AC02_code)s	%(AC02_shift_code)s	%(AC02_code)s	258	#%(AC02_shift)s
HiddenKey	%(AC03_code)s	%(AC03_shift_code)s	%(AC03_code)s	258	#%(AC03_shift)s
HiddenKey	%(AC04_code)s	%(AC04_shift_code)s	%(AC04_code)s	258	#%(AC04_shift)s
HiddenKey	%(AC05_code)s	%(AC05_shift_code)s	%(AC04_code)s	258	#%(AC05_shift)s
HiddenKey	%(AC06_code)s	%(AC06_shift_code)s	%(AC07_code)s	257	#%(AC06_shift)s
HiddenKey	%(AC07_code)s	%(AC07_shift_code)s	%(AC07_code)s	257	#%(AC07_shift)s
HiddenKey	%(AC08_code)s	%(AC08_shift_code)s	%(AC08_code)s	257	#%(AC08_shift)s
HiddenKey	%(AC09_code)s	%(AC09_shift_code)s	%(AC09_code)s	257	#%(AC09_shift)s
HiddenKey	%(AC10_code)s	%(AC10_shift_code)s	%(AC10_code)s	257	#%(AC10_shift)s
HiddenKey	%(AC11_code)s	%(AC11_shift_code)s	%(AC10_code)s	257	#%(AC11_shift)s
HiddenKey	%(BKSL_code)s	%(BKSL_shift_code)s	%(AC10_code)s	257	#%(BKSL_shift)s
#
#       Unicode   Target  Finger  Control
#Maj: 4ème ligne de touches
HiddenKey	%(LSGT_code)s	%(LSGT_shift_code)s	%(AC01_code)s	258	#%(LSGT_shift)s
HiddenKey	%(AB01_code)s	%(AB01_shift_code)s	%(AC01_code)s	258	#%(AB01_shift)s
HiddenKey	%(AB02_code)s	%(AB02_shift_code)s	%(AC02_code)s	258	#%(AB02_shift)s
HiddenKey	%(AB03_code)s	%(AB03_shift_code)s	%(AC03_code)s	258	#%(AB03_shift)s
HiddenKey	%(AB04_code)s	%(AB04_shift_code)s	%(AC04_code)s	258	#%(AB04_shift)s
HiddenKey	%(AB05_code)s	%(AB05_shift_code)s	%(AC04_code)s	258	#%(AB05_shift)s
HiddenKey	%(AB06_code)s	%(AB06_shift_code)s	%(AC07_code)s	257	#%(AB06_shift)s
HiddenKey	%(AB07_code)s	%(AB07_shift_code)s	%(AC07_code)s	257	#%(AB07_shift)s
HiddenKey	%(AB08_code)s	%(AB08_shift_code)s	%(AC08_code)s	257	#%(AB08_shift)s
HiddenKey	%(AB09_code)s	%(AB09_shift_code)s	%(AC09_code)s	257	#%(AB09_shift)s
HiddenKey	%(AB10_code)s	%(AB10_shift_code)s	%(AC10_code)s	257	#%(AB10_shift)s
#
#
#   Altgr
#
#      Unicode Target  Finger  Control
#Maj: 1ère ligne de touches
HiddenKey	%(TLDE_code)s	%(TLDE_option_code)s	%(AC01_code)s	264	#%(TLDE_option)s
HiddenKey	%(AE01_code)s	%(AE01_option_code)s	%(AC01_code)s	264	#%(AE01_option)s
HiddenKey	%(AE02_code)s	%(AE02_option_code)s	%(AC01_code)s	264	#%(AE02_option)s
HiddenKey	%(AE03_code)s	%(AE03_option_code)s	%(AC02_code)s	264	#%(AE03_option)s
HiddenKey	%(AE04_code)s	%(AE04_option_code)s	%(AC03_code)s	264	#%(AE04_option)s
HiddenKey	%(AE05_code)s	%(AE05_option_code)s	%(AC04_code)s	264	#%(AE05_option)s
HiddenKey	%(AE06_code)s	%(AE06_option_code)s	%(AC04_code)s	264	#%(AE06_option)s
HiddenKey	%(AE07_code)s	%(AE07_option_code)s	%(AC07_code)s	264	#%(AE07_option)s
HiddenKey	%(AE08_code)s	%(AE08_option_code)s	%(AC07_code)s	264	#%(AE08_option)s
HiddenKey	%(AE09_code)s	%(AE09_option_code)s	%(AC08_code)s	264	#%(AE09_option)s
HiddenKey	%(AE10_code)s	%(AE10_option_code)s	%(AC09_code)s	264	#%(AE10_option)s
HiddenKey	%(AE11_code)s	%(AE11_option_code)s	%(AC10_code)s	264	#%(AE11_option)s
HiddenKey	%(AE12_code)s	%(AE12_option_code)s	%(AC10_code)s	264	#%(AE12_option)s
#
#      Unicode Target  Finger  Control
#Maj: 2ème ligne de touches
HiddenKey	%(AD01_code)s	%(AD01_option_code)s	%(AC01_code)s	264	#%(AD01_option)s
HiddenKey	%(AD02_code)s	%(AD02_option_code)s	%(AC02_code)s	264	#%(AD02_option)s
HiddenKey	%(AD03_code)s	%(AD03_option_code)s	%(AC03_code)s	264	#%(AD03_option)s
HiddenKey	%(AD04_code)s	%(AD04_option_code)s	%(AC04_code)s	264	#%(AD04_option)s
HiddenKey	%(AD05_code)s	%(AD05_option_code)s	%(AC04_code)s	264	#%(AD05_option)s
HiddenKey	%(AD06_code)s	%(AD06_option_code)s	%(AC07_code)s	264	#%(AD06_option)s
HiddenKey	%(AD07_code)s	%(AD07_option_code)s	%(AC07_code)s	264	#%(AD07_option)s
HiddenKey	%(AD08_code)s	%(AD08_option_code)s	%(AC08_code)s	264	#%(AD08_option)s
HiddenKey	%(AD09_code)s	%(AD09_option_code)s	%(AC09_code)s	264	#%(AD09_option)s
HiddenKey	%(AD10_code)s	%(AD10_option_code)s	%(AC10_code)s	264	#%(AD10_option)s
HiddenKey	%(AD11_code)s	%(AD11_option_code)s	%(AC10_code)s	264	#%(AD11_option)s
HiddenKey	%(AD12_code)s	%(AD12_option_code)s	%(AC10_code)s	264	#%(AD12_option)s
#
#       Unicode   Target  Finger  Control
#Maj: 3ème ligne de touches
HiddenKey	%(AC01_code)s	%(AC01_option_code)s	%(AC01_code)s	264	#%(AC01_option)s
HiddenKey	%(AC02_code)s	%(AC02_option_code)s	%(AC02_code)s	264	#%(AC02_option)s
HiddenKey	%(AC03_code)s	%(AC03_option_code)s	%(AC03_code)s	264	#%(AC03_option)s
HiddenKey	%(AC04_code)s	%(AC04_option_code)s	%(AC04_code)s	264	#%(AC04_option)s
HiddenKey	%(AC05_code)s	%(AC05_option_code)s	%(AC04_code)s	264	#%(AC05_option)s
HiddenKey	%(AC06_code)s	%(AC06_option_code)s	%(AC07_code)s	264	#%(AC06_option)s
HiddenKey	%(AC07_code)s	%(AC07_option_code)s	%(AC07_code)s	264	#%(AC07_option)s
HiddenKey	%(AC08_code)s	%(AC08_option_code)s	%(AC08_code)s	264	#%(AC08_option)s
HiddenKey	%(AC09_code)s	%(AC09_option_code)s	%(AC09_code)s	264	#%(AC09_option)s
HiddenKey	%(AC10_code)s	%(AC10_option_code)s	%(AC10_code)s	264	#%(AC10_option)s
HiddenKey	%(AC11_code)s	%(AC11_option_code)s	%(AC10_code)s	264	#%(AC11_option)s
HiddenKey	%(BKSL_code)s	%(BKSL_option_code)s	%(AC10_code)s	264	#%(BKSL_option)s
#
#       Unicode   Target  Finger  Control
#Maj: 4ème ligne de touches
HiddenKey	%(LSGT_code)s	%(LSGT_option_code)s	%(AC01_code)s	264	#%(LSGT_option)s
HiddenKey	%(AB01_code)s	%(AB01_option_code)s	%(AC01_code)s	264	#%(AB01_option)s
HiddenKey	%(AB02_code)s	%(AB02_option_code)s	%(AC02_code)s	264	#%(AB02_option)s
HiddenKey	%(AB03_code)s	%(AB03_option_code)s	%(AC03_code)s	264	#%(AB03_option)s
HiddenKey	%(AB04_code)s	%(AB04_option_code)s	%(AC04_code)s	264	#%(AB04_option)s
HiddenKey	%(AB05_code)s	%(AB05_option_code)s	%(AC04_code)s	264	#%(AB05_option)s
HiddenKey	%(AB06_code)s	%(AB06_option_code)s	%(AC07_code)s	264	#%(AB06_option)s
HiddenKey	%(AB07_code)s	%(AB07_option_code)s	%(AC07_code)s	264	#%(AB07_option)s
HiddenKey	%(AB08_code)s	%(AB08_option_code)s	%(AC08_code)s	264	#%(AB08_option)s
HiddenKey	%(AB09_code)s	%(AB09_option_code)s	%(AC09_code)s	264	#%(AB09_option)s
HiddenKey	%(AB10_code)s	%(AB10_option_code)s	%(AC10_code)s	264	#%(AB10_option)s
"""

fullMapValues = {}
for k, v in xkb.tmplValues.iteritems():
   v = terminators.get( v, v )
   if v == "":
     v = " "
   fullMapValues[k] = v
   fullMapValues[k+"_code"] = str(ord(v))
out = codecs.open(sys.argv[2], "w", "utf8")
out.write( fullMapTmpl % fullMapValues )
