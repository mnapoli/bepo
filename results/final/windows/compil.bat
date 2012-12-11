REM Batch à lancer dans ...\msklc\bin\i386\ avec les 6 fichiers .klc
REM Il génère les fichiers dlls avec kbdutool.exe
REM Penser à modificer le numéro de version (set ver=...)
REM Le nom de la dll est en dos 8.3 donc le nom de version est abrégé en rc2x
REM Il faut ensuite faire les fichiers d'installation avec msklc
REM (Attention a bien garder le même nom de dll.)
@echo off
set ver=m
md bepo%ver%
cd bepo%ver%
md amd64
md i386
md ia64
md sources
md wow64
cd..
kbdutool.exe -u -x bepo%ver%.klc
move /y bepo%ver%.dll bepo%ver%/i386/
kbdutool.exe -u -i bepo%ver%.klc
move /y bepo%ver%.dll bepo%ver%/ia64/
kbdutool.exe -u -m bepo%ver%.klc
move /y bepo%ver%.dll bepo%ver%/amd64/
kbdutool.exe -u -o bepo%ver%.klc
move /y bepo%ver%.dll bepo%ver%/wow64/