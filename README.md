bepo
====

Custom version of the french dvorak keyboard layout

## Changements

* Touche `2`: inversion de `«` et `<`
* Touche `3`: inversion de `»` et `>`
* Inversion des touches `^` et `w`
* Raccourcis clavier `Ctrl+X`, `Ctrl+C`, `Ctrl+V` et `Ctrl+Z` mappés comme en AZERTY.

## Installation

### Windows

Installation testée et OK. Utiliser l'exécutable dans le dossier result/...

Ça installera une disposition supplémentaire.

### OS X

Installation testée et OK.

- installer le bépo officiel
- télécharger le fichier `results/final/macosx/layout-matthieu.keylayout`
- ouvrir `/Library/Keyboard Layouts` et ouvrir le paquet dvorak-bepo -> `Contents/Resources/`
- ajouter le fichier .keylayout
- rouvrir la session et sélectionner `bépo-matthieu` dans le panneau de configuration

Installer KeyRemap4Macbook et cocher

- Command_L to Control_L (except Terminal, …)
- Control_L to Command_L (except Terminal, …)
- Use PC style Home/End #2

Créer un fichier `~/Library/KeyBindings/DefaultKeyBinding.dict` contenant :

```javascript
/* ~/Library/KeyBindings/DefaultKeyBinding.Dict

Here is a rough cheatsheet for syntax.
Key Modifiers
^ : Ctrl
$ : Shift
~ : Option (Alt)
@ : Command (Apple)
# : Numeric Keypad

Non-Printable Key Codes

Up Arrow:     \UF700        Backspace:    \U007F        F1:           \UF704
Down Arrow:   \UF701        Tab:          \U0009        F2:           \UF705
Left Arrow:   \UF702        Escape:       \U001B        F3:           \UF706
Right Arrow:  \UF703        Enter:        \U000A        ...
Insert:       \UF727        Page Up:      \UF72C
Delete:       \UF728        Page Down:    \UF72D
Home:         \UF729        Print Screen: \UF72E
End:          \UF72B        Scroll Lock:  \UF72F
Break:        \UF732        Pause:        \UF730
SysReq:       \UF731        Menu:         \UF735
Help:         \UF746

NOTE: typically the Windows 'Insert' key is mapped to what Macs call 'Help'.  
Regular Mac keyboards don't even have the Insert key, but provide 'Fn' instead, 
which is completely different.
*/

{

"\UF729"   = "moveToBeginningOfLine:";                       /* Home         */
"$\UF729"  = "moveToBeginningOfLineAndModifySelection:";     /* Shift + Home */
"\UF72B"   = "moveToEndOfLine:";                             /* End          */
"$\UF72B"  = "moveToEndOfLineAndModifySelection:";           /* Shift + End  */

"\UF72C"   = "pageUp:";                                      /* PageUp       */
"\UF72D"   = "pageDown:";                                    /* PageDown     */
"$\UF728"  = "cut:";                                         /* Shift + Del  */
"@\UF746"  = "copy:";                                        /* Cmd   + Help */
"$\UF746"  = "paste:";                                       /* Shift + Help */
"@\UF702"  = "moveWordBackward:";                            /* Cmd   + LeftArrow */
"@\UF703"  = "moveWordForward:";                             /* Cmd   + RightArrow */
"@$\UF702" = "moveWordBackwardAndModifySelection:";          /* Shift + Cmd + Leftarrow */
"@$\UF703" = "moveWordForwardAndModifySelection:";           /* Shift + Cmd + Rightarrow */
"@\U007F"  = "deleteWordBackward:";                          /* Cmd + Backspace */
"@\UF728"  = "deleteWordForward:";                           /* Cmd + Delete */

"~-" = ("insertText:", "->");                                /* Alt + - */
"~\\$" = ("insertText:", "$this->");                         /* Alt + $ */
"~," = ("moveToEndOfLine:", "insertText:", ";");             /* Alt + , */
"~y" = ("moveToEndOfLine:", "insertText:", " {", "insertNewline:"); /* Alt + y */
}
```

### Ubuntu

Modifier `/usr/share/X11/xkb/symbols/fr` (faire un backup) :

- copier-coller la définition du bépo (pas bépo latin9)
- modifier la nouvelle section (remplacer bepo par bepom, et le nom par Bépo Matthieu)
  - remplacer bepo par bepom
  - remplacer le nom par "Bepo Matthieu"
  - inverser "^" et "w"
  - inverser "«" et "<"
  - inverser "»" et ">"

Modifier `/usr/share/X11/xkb/rules/evdev.xml` et `/usr/share/X11/xkb/rules/base.xml` pour ajouter à la suite des déclarations bepo :

```xml
<variant>
  <configItem>
    <name>bepom</name>
    <description>French (Bepo Matthieu)</description>
  </configItem>
</variant>
```

En rouvrant le panneau de configuration, la nouvelle disposition "Bépo Matthieu" devrait apparaitre.

Pour les raccourcis clavier, utiliser AutoKey (par exemple créer une phrase `<ctrl>+v` et la binder à `Ctrl+.`).
