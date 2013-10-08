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

### Ubuntu

Modifier `/usr/share/X11/xkb/symbols/fr` (faire un backup) :

- copier-coller la définition du bépo (pas bépo latin9)
- modifier la nouvelle section (remplacer bepo par bepom, et le nom par Bépo Matthieu)

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
