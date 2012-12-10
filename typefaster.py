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


fullMapTmpl = keyboardTemplate = u"""<?xml version="1.0"?>
<layout version="1.0" horizgap="0.0714" vertgap="0.0714" ltr="true">
  <row scale="1.0">
    <key shape="square" type="normal" homekey="false" size="1" homeindex="29">
      <value when="rightshift" draw="true">%(TLDE_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(TLDE_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(TLDE)s</value>
      <value when="altgr" draw="true">%(TLDE_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="29">
      <value when="rightshift" draw="true">%(AE01_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE01_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE01)s</value>
      <value when="altgr" draw="true">%(AE01_option)s</value>
    </key>
    <key shape="square" type="squiggle" homekey="false" size="1" homeindex="30">
      <value when="rightshift" draw="true">%(AE02_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE02_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE02)s</value>
      <value when="altgr" draw="true">%(AE02_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="31">
      <value when="rightshift" draw="true">%(AE03_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE03_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE03)s</value>
      <value when="altgr" draw="true">%(AE03_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="31">
      <value when="rightshift" draw="true">%(AE04_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE04_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE04)s</value>
      <value when="altgr" draw="true">%(AE04_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="32">
      <value when="rightshift" draw="true">%(AE05_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE05_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE05)s</value>
      <value when="altgr" draw="true">%(AE05_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="32">
      <value when="leftshift" draw="true">%(AE06_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE06_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE06)s</value>
      <value when="altgr" draw="true">%(AE06_option)s</value>
    </key>
    <key shape="square" type="backwardaccent" homekey="false" size="1" homeindex="35">
      <value when="leftshift" draw="true">%(AE07_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE07_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE07)s</value>
      <value when="altgr" draw="true">%(AE07_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="35">
      <value when="leftshift" draw="true">%(AE08_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE08_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE08)s</value>
      <value when="altgr" draw="true">%(AE08_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="36">
      <value when="leftshift" draw="true">%(AE09_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE09_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE09)s</value>
      <value when="altgr" draw="true">%(AE09_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="37">
      <value when="leftshift" draw="true">%(AE10_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE10_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE10)s</value>
      <value when="altgr" draw="true">%(AE10_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="37">
      <value when="leftshift" draw="true">%(AE11_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE11_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE11)s</value>
      <value when="altgr" draw="true">%(AE11_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="38">
      <value when="leftshift" draw="true">%(AE12_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AE12_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AE12)s</value>
      <value when="altgr" draw="true">%(AE12_option)s</value>
    </key>
    <key shape="rect" type="backspace" homekey="false" size="2.0238;1">
    </key>
  </row>
  <row scale="1.0">
    <key shape="rect" type="tab" homekey="false" size="1.5238;1">
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="32">
      <value when="rightshift" draw="true">%(AD01_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AD01_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD01)s</value>
      <value when="altgr" draw="true">%(AD01_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="31">
      <value when="rightshift" draw="true">%(AD02_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AD02_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD02)s</value>
      <value when="altgr" draw="true">%(AD02_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="38">
      <value when="rightshift" draw="true">%(AD03_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AD03_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD03)s</value>
      <value when="altgr" draw="true">%(AD03_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="37">
      <value when="rightshift" draw="true">%(AD04_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AD04_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD04)s</value>
      <value when="altgr" draw="true">%(AD04_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="31">
      <value when="rightshift" draw="true">%(AD05_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AD05_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD05)s</value>
      <value when="altgr" draw="true">%(AD05_option)s</value>
    </key>
    <key shape="square" type="hat;doubledot" homekey="false" size="1" homeindex="38">
      <value when="leftshift" draw="true">%(AD06_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AD06_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD06)s</value>
      <value when="altgr" draw="true">%(AD06_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="32">
      <value when="leftshift" draw="true">%(AD07_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AD07_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD07)s</value>
      <value when="altgr" draw="true">%(AD07_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1"> <!--31-->
      <value when="leftshift" draw="true">%(AD08_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AD08_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD08)s</value>
      <value when="altgr" draw="true">%(AD08_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1"> <!--37-->
      <value when="leftshift" draw="true">%(AD09_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AD09_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD09)s</value>
      <value when="altgr" draw="true">%(AD09_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1"> <!--32-->
      <value when="leftshift" draw="true">%(AD10_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AD10_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD10)s</value>
      <value when="altgr" draw="true">%(AD10_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1"> <!--35-->
      <value when="leftshift" draw="true">%(AD11_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AD11_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD11)s</value>
      <value when="altgr" draw="true">%(AD11_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="30">
      <value when="leftshift" draw="true">%(AD12_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AD12_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AD12)s</value>
      <value when="altgr" draw="true">%(AD12_option)s</value>
    </key>
    <key shape="irregular" type="enter" homekey="false" size="1.5E;2.0714S;1.0952W;1.0714N;0.4048W;1N">
    </key>
  </row>
  <row scale="1.0">
    <key shape="rect" type="capslock" homekey="false" size="1.9286;1">
    </key>
    <key shape="square" type="normal" homekey="true" size="1" homeindex="29">
      <value when="rightshift" draw="true">%(AC01_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AC01_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC01)s</value>
      <value when="altgr" draw="true">%(AC01_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="true" size="1" homeindex="35">
      <value when="rightshift" draw="true">%(AC02_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AC02_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC02)s</value>
      <value when="altgr" draw="true">%(AC02_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="true" size="1" homeindex="36">
      <value when="rightshift" draw="true">%(AC03_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AC03_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC03)s</value>
      <value when="altgr" draw="true">%(AC03_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="true" size="1" homeindex="31">
      <value when="rightshift" draw="true">%(AC04_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AC04_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC04)s</value>
      <value when="altgr" draw="true">%(AC04_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="35">
      <value when="rightshift" draw="true">%(AC05_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AC05_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC05)s</value>
      <value when="altgr" draw="true">%(AC05_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="31">
      <value when="leftshift" draw="true">%(AC06_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AC06_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC06)s</value>
      <value when="altgr" draw="true">%(AC06_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="true" size="1" homeindex="32">
      <value when="leftshift" draw="true">%(AC07_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AC07_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC07)s</value>
      <value when="altgr" draw="true">%(AC07_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="true" size="1"> <!--30-->
      <value when="leftshift" draw="true">%(AC08_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AC08_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC08)s</value>
      <value when="altgr" draw="true">%(AC08_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="true" size="1" homeindex="35">
      <value when="leftshift" draw="true">%(AC09_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AC09_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC09)s</value>
      <value when="altgr" draw="true">%(AC09_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="true" size="1" homeindex="32">
      <value when="leftshift" draw="true">%(AC10_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AC10_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC10)s</value>
      <value when="altgr" draw="true">%(AC10_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1"> <!--38-->
      <value when="leftshift" draw="true">%(AC11_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AC11_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AC11)s</value>
      <value when="altgr" draw="true">%(AC11_option)s</value>
    </key>
        <key shape="square" type="normal" homekey="false" size="1" homeindex="31">
      <value when="leftshift" draw="true">%(BKSL_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(BKSL_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(BKSL)s</value>
      <value when="altgr" draw="true">%(BKSL_option)s</value>
    </key>
  </row>
  <row scale="1.0">
    <key shape="rect" type="leftshift" homekey="false" size="1.381;1">
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="35">
      <value when="rightshift" draw="true">%(LSGT_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(LSGT_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(LSGT)s</value>
      <value when="altgr" draw="true">%(LSGT_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="29">
      <value when="rightshift" draw="true">%(AB01_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AB01_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB01)s</value>
      <value when="altgr" draw="true">%(AB01_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="35">
      <value when="rightshift" draw="true">%(AB02_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AB02_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB02)s</value>
      <value when="altgr" draw="true">%(AB02_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="35">
      <value when="rightshift" draw="true">%(AB03_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AB03_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB03)s</value>
      <value when="altgr" draw="true">%(AB03_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="37">
      <value when="rightshift" draw="true">%(AB04_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AB04_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB04)s</value>
      <value when="altgr" draw="true">%(AB04_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1"> <!--36-->
      <value when="rightshift" draw="true">%(AB05_shift)s</value>
      <value when="rightshift;altgr" draw="true">%(AB05_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB05)s</value>
      <value when="altgr" draw="true">%(AB05_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="36">
      <value when="leftshift" draw="true">%(AB06_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AB06_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB06)s</value>
      <value when="altgr" draw="true">%(AB06_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1"> <!--29-->
      <value when="leftshift" draw="true">%(AB07_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AB07_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB07)s</value>
      <value when="altgr" draw="true">%(AB07_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="32">
      <value when="leftshift" draw="true">%(AB08_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AB08_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB08)s</value>
      <value when="altgr" draw="true">%(AB08_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="30">
      <value when="leftshift" draw="true">%(AB09_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AB09_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB09)s</value>
      <value when="altgr" draw="true">%(AB09_option)s</value>
    </key>
    <key shape="square" type="normal" homekey="false" size="1" homeindex="29">
      <value when="leftshift" draw="true">%(AB10_shift)s</value>
      <value when="leftshift;altgr" draw="true">%(AB10_shift_option)s</value>
      <value when="normal" draw="true" newline="true">%(AB10)s</value>
      <value when="altgr" draw="true">%(AB10_option)s</value>
    </key>
    <key shape="rect" type="rightshift" homekey="false" size="2.7143;1">
    </key>
  </row>
  <row scale="1.0">
    <key shape="rect" type="control" homekey="false" size="2.0714;1">
    </key>
    <key shape="rect" type="alt" homekey="false" size="2.0714;1">
    </key>
    <key shape="rect" type="normal" homekey="false" size="7.381;1">
      <value when="normal" draw="false"> </value>
    </key>
    <key shape="rect" type="altgr" homekey="false" size="2.0714;1">
    </key>  
    <key shape="rect" type="control" homekey="false" size="2.0714;1">
    </key>
  </row>
</layout>
"""

fullMapValues = {}
for k, v in xkb.tmplValues.iteritems():
   v = terminators.get( v, v )
   if v == u'"':
     v = u"&#x0022;"
   elif v == u'<':
     v = u"&#x003c;"
   elif v == u'&':
     v = u'&#x0026;'
   fullMapValues[k] = v
out = codecs.open(sys.argv[2], "w", "utf-16-le")
out.write(u"\uFEFF")
out.write( fullMapTmpl % fullMapValues )
