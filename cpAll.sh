#!/bin/sh

#VERSION=0.1.1
VERSION=1.0rc3


cp "results/layout-${VERSION}-user.xkb" ../xkb/bepo.xkb
cp "results/layout-${VERSION}-user-legacy.xkb" ../xkb/bepo-xorglegacy.xkb
cp "results/layout-${VERSION}.XCompose" ../xkb/XCompose

cp "results/bepo-${VERSION}A.klc" ../windows/bepo-azerty.klc
cp "results/bepo-${VERSION}B.klc" ../windows/bepo.klc
cp "results/bepo-${VERSION}C.klc" ../windows/bepo-qwertz.klc
cp "results/layout-${VERSION}.kbd" ../klavaro/bepo.kbd
cp "results/layout-${VERSION}.keyboard" ../ktouch/bepo.keyboard
cp "results/layout-${VERSION}.xml" ../typefaster/bepo.xml
cp "results/layout-${VERSION}.map" ../keymaps/bepo.map
cp "results/layout-${VERSION}.utf8.map" ../keymaps/bepo-utf8.map
cp "results/layout-${VERSION}.kbdmap" ../kbdmap/bepo.kbd
cp "results/layout-${VERSION}.wscons" ../wscons/bepo.map
cp "results/layout-${VERSION}.keylayout" ../macosx/bepo.bundle/Contents/Resources/bepo.keylayout
cp "results/layout-${VERSION}.keytables" ../keytables/bepo
