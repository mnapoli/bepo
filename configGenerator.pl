#!/usr/bin/env perl

###########################################################################
#   Copyright (C) 2008 by Nicolas Chartier                                #
#   chartier.nicolas@gmail.com                                            #
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 3 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#   This program is distributed in the hope that it will be useful,       #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#   GNU General Public License for more details.                          #
#                                                                         #
#   You should have received a copy of the GNU General Public License     #
#   along with this program; if not, write to the                         #
#   Free Software Foundation, Inc.,                                       #
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
###########################################################################

# TODO

# xkb :
# - gestion des level four alphabetic
# compose :
# - gestion de la surcharge
# msklc :
# - gestion du capslock pour msklc
# xmodmap :
# - générer via layout.conf les touches qui sont mises en dur dans le footer
# loadkeys :
# - tout

# source C :
# - tout

# Notes
# le format Mac OS X est généré à partir des fichiers xkb par le script de gaetan

use strict;
use warnings;
use locale;
use Data::Dumper;

binmode STDOUT, ":utf8";

die("Usage: $0 <version> <output format>\n")
    if (!defined($ARGV[1]));

my $VERSION            = $ARGV[0];
my $OUTPUT_FORMAT      = $ARGV[1];

my $LAYOUT_DESCRIPTION = "layout-$VERSION.conf";
my $DEAKEY_BEHAVIOUR   = "deads-$VERSION.conf";
my $VIRTUAL_KEYS       = "virtualKeys-$VERSION.conf";

my $KEYS_FILE         = "keys.conf";
my $SPECIAL_KEYS_FILE = "specialKeys.conf";
my $SYMBOLS_FILE      = "symbols.conf";

my $UNICODE_FILE = "UnicodeData-5.0.0.fr.txt";

my $SHORT_VERSION = $VERSION;
$SHORT_VERSION =~ tr/\.//d;

# Column 0: key/symbole code
# Column 1: scancode/unicode
my $x_xkb_column     = 2;
my $x_xmodmap_column = 3;
my $win_msklc_column = 4;

my $vk_azerty_column = 1;
my $vk_bepo_column   = 2;
my $vk_qwertz_column = 3;
my $vk_dvoraj_column = 4;

my %keys        = ();
my %specialKeys = ();
my %virtualKeys = ();
my %scanCodes   = ();

my %symbols  = ();
my %unicodes = ();

my @layoutKeys = ();
my %layoutSyms = ();

my @deadKeysA = ();
my %deadKeysH = ();

my %unicodesDescription = ();

my @levels = ('ONE', 'TWO', 'THREE', 'FOUR');

sub loadKeys($)
{
    my $column = shift;

    open(FILE, "< $KEYS_FILE") or die("open: $!");

    LINE: while (<FILE>)
    {
        next LINE if (/^#/);
        next LINE if (/^\s*$/);

        chomp;
        s/#.*$//g;
        my @array = split(/ +|\t/);
        $scanCodes{$array[0]} = $array[1];
        $keys{$array[0]} = $array[$column];
    }

    close(FILE);

#print Dumper(\%keys);
}

sub loadSpecialKeys()
{
    open(FILE, "< $SPECIAL_KEYS_FILE") or die("open: $!");

    LINE: while (<FILE>)
    {
        next LINE if (/^#/);
        next LINE if (/^\s*$/);

        chomp;
        s/#.*$//g;
        my @array = split(/\t/);
        $specialKeys{$array[0]} = \@array;
    }

    close(FILE);

#print Dumper(\%specialKeys);
}

sub loadVirtualKeys($)
{
    my $column = shift;

    open(FILE, "< $VIRTUAL_KEYS") or die("open: $!");

    LINE: while (<FILE>)
    {
        next LINE if (/^#/);
        next LINE if (/^\s*$/);

        chomp;
        s/#.*$//g;
        my @array = split(/ +|\t/);
        $virtualKeys{$array[0]} = $array[$column];
    }

    close(FILE);

#print Dumper(\%virtualKeys);
}

sub loadSymbols($)
{
    my $column = shift;

    open(FILE, "< $SYMBOLS_FILE") or die("open: $!");

    LINE: while (<FILE>)
    {
        next LINE if (/^#/);
        next LINE if (/^\s*$/);

        chomp;
        s/#.*$//g;
        my @array = ();

        if (/^U([0-9A-Z]{4})$/)
        {
            my $unicode = $1;
            @array = ("U".$unicode, $unicode, "U".$unicode, "U".$unicode, lc($unicode));
        }
        else
        {
            @array = split(/ +|\t/);
        }

        if (defined($unicodes{$array[0]}))
        {
            print STDERR "Duplicate unicode: ".$array[0]."\n";
            next LINE;
        }
        if (defined($symbols{$array[0]}))
        {
            print STDERR "Duplicate symbol: ".$array[0]."\n";
            next LINE;
        }

        $unicodes{$array[0]} = $array[1];
        $symbols{$array[0]} = $array[$column];
    }

    close(FILE);

#print Dumper(\%symbols);
}

sub loadLayout()
{
    open(FILE, "< $LAYOUT_DESCRIPTION") or die("open: $!");

    LINE: while (<FILE>)
    {
        next LINE if (/^#/);

        if (/^\s*$/)
        {
            push(@layoutKeys, "");
            next LINE;
        }

        chomp;
        s/#.*$//g;
        my @array = split(/ +|\t/);
        my $key = $array[0];
        my %symbols = ();
        $symbols{'direct'}      = $array[1];
        $symbols{'shift'}       = $array[2];
        $symbols{'altgr'}       = $array[3];
        $symbols{'altgr+shift'} = $array[4];
        $symbols{'translation'} = $array[5];

        if ($key =~ /(.+)!(.+)/)
        {
            my $special = $1;
            $key = $2;

            $symbols{'windowsOnly'} = ($special =~ /w/);
            $symbols{'caps0'}       = ($special =~ /0/);
            $symbols{'caps1'}       = ($special =~ /1/);
            $symbols{'caps2'}       = ($special =~ /2/);
        }

        push(@layoutKeys, $key);
        $layoutSyms{$key} = \%symbols;
    }

    close(FILE);

#print Dumper(\@layoutKeys);
#print Dumper(\%layoutSyms);
}

sub loadDeadKeys()
{
    open(FILE, "< $DEAKEY_BEHAVIOUR") or die("open: $!");

    LINE: while (<FILE>)
    {
        next LINE if (/^#/);

        if (/^\s*$/)
        {
            push(@deadKeysA, "");
            next LINE;
        }

        chomp;
        s/#.*$//g;
        my @array = split(/ +|\t/);
        my %infos = ();
        $infos{'symbol'} = pop(@array);

        if ($array[0] =~ /(.+)!(.+)/)
        {
            my $special = $1;
            $array[0] = $2;

            $infos{'notLinux'}    = ($special =~ /L/);
            $infos{'windowsOnly'} = ($special =~ /w/);
        }

        push(@deadKeysA, \@array);
        $deadKeysH{\@array} = \%infos;
    }

    close(FILE);

#print Dumper(\@deadKeysA);
#print Dumper(\%deadKeysH);
}

sub loadUnicode()
{
    open(FILE, "< $UNICODE_FILE") or die("open: $!");

    LINE: while (<FILE>)
    {
        next LINE
            if (/^#/ || /^\s*$/);

        chomp;
        s/#.*$//g;
        my @array = split(/;/);
        my $code = shift(@array);
        my $desc = shift(@array);

        $unicodesDescription{$code} = $desc;
    }

    close(FILE);

#print Dumper(\%unicodesDescription);
}

sub unicode2utf8($)
{
    my $unicode = shift;

    return ""
        if ($unicode eq "NA");

    return chr(hex(lc($unicode)));
}

sub gen_x_xkb_header()
{
    my $header = "partial alphanumeric_keys\nxkb_symbols \"dvorak\" {\n\n".
                 "\tname[Group1]= \"France - Bepo, ergonomic, Dvorak way (v$VERSION)\";\n";

    return $header;
}

sub gen_x_xkb_user_header()
{
    my $header = "xkb_keymap        {\n".
                 "\n".
                 "xkb_keycodes      { include \"xfree86+aliases(azerty)\" };\n".
                 "\n".
                 "xkb_types         { include \"complete\" };\n".
                 "\n".
                 "xkb_compatibility { include \"complete\" };\n".
                 "\n";

    return $header;
}

sub gen_x_xmodmap_header()
{
    my $header = "clear    shift\n".
                 "clear    lock\n".
                 "clear    control\n".
                 "clear    mod1\n".
                 "clear    mod2\n".
                 "clear    mod3\n".
                 "clear    mod4\n".
                 "clear    mod5\n";

    return $header;
}

sub gen_x_compose_header()
{
    my $header = "include \"%L\"\n";

    return $header;
}

sub gen_win_msklc_header($$)
{
    my ($localeName, $localeId) = @_;

    my $header = "KBD\tbepo".$SHORT_VERSION."\t\"Bépo v".$VERSION."\"\r\n".
                 "\r\n".
                 "COPYRIGHT\t\"CC-SA-BY\"\r\n".
                 "\r\n".
                 "COMPANY\t\"Disposition bépo — http://bepo.fr\"\r\n".
                 "\r\n".
                 "LOCALENAME\t\"".$localeName."\"\r\n".
                 "\r\n".
                 "LOCALEID\t\"".$localeId."\"\r\n".
                 "\r\n".
                 "VERSION\t".$VERSION."\r\n".
                 "\r\n".
                 "SHIFTSTATE\r\n".
                 "\r\n".
                 "0\t//Column 4\r\n".
                 "1\t//Column 5 : Shft\r\n".
                 "2\t//Column 6 :       Ctrl\r\n".
                 "6\t//Column 7 :       Ctrl Alt\r\n".
                 "7\t//Column 8 : Shft  Ctrl Alt\r\n\r\n".
                 "LAYOUT\t\t;an extra '\@' at the end is a dead key\r\n".
                 "\r\n".
                 "//SC\tVK_\t\tCap\t0\t1\t2\t6\t7\r\n".
                 "//--\t----\t\t----\t----\t----\t----\t----\t----\r\n";

    return $header;
}

sub gen_x_xkb_body()
{
    my $body = "";

    for my $key (@layoutKeys)
    {
        if ($key eq "")
        {
            $body .= "\n";
            next;
        }

        if (!defined($keys{$key}))
        {
            print STDERR "Unknown key: ".$key."\n";
            next;
        }

        my %keySymbols = %{$layoutSyms{$key}};
        my $lineEnd = " ] };";
        my $comment = "\n";
        my $nextSymbolExists = 0;
        my $voidSymbol = "VoidSymbol";

        my $symbolNumber = 0;

        next
            if (defined($keySymbols{'windowsOnly'}) && $keySymbols{'windowsOnly'} == 1);

        # AltGr + Shift
        if (defined($keySymbols{'altgr+shift'}) && $keySymbols{'altgr+shift'} ne "")
        {
            if (!defined($symbols{$keySymbols{'altgr+shift'}}))
            {
                print STDERR "Unknown symbol: ".$key."{'altgr+shift'}: ".$keySymbols{'altgr+shift'}."\n";
                next;
            }
            $lineEnd = ", ".$symbols{$keySymbols{'altgr+shift'}}.$lineEnd;
            $comment = " ".&unicode2utf8($unicodes{$keySymbols{'altgr+shift'}}).$comment;
            $nextSymbolExists = 1;

            $symbolNumber = 4
                if ($symbolNumber == 0);
        }

        # AltGr
        if (defined($keySymbols{'altgr'}) && $keySymbols{'altgr'} ne "")
        {
            if (!defined($symbols{$keySymbols{'altgr'}}))
            {
                print STDERR "Unknown symbol: ".$key."{'altgr'}: ".$keySymbols{'altgr'}."\n";
                next;
            }
            $lineEnd = ", ".$symbols{$keySymbols{'altgr'}}.$lineEnd;
            $comment = " ".&unicode2utf8($unicodes{$keySymbols{'altgr'}}).$comment;
            $nextSymbolExists = 1;

            $symbolNumber = 3
                if ($symbolNumber == 0);
        }
        elsif ($nextSymbolExists == 1)
        {
            $lineEnd = ", ".$voidSymbol.$lineEnd;
            $comment = "  ".$comment;
        }

        # Shift
        if (defined($keySymbols{'shift'}) && $keySymbols{'shift'} ne "")
        {
            if (!defined($symbols{$keySymbols{'shift'}}))
            {
                print STDERR "Unknown symbol: ".$key."{'shift'}: ".$keySymbols{'shift'}."\n";
                next;
            }
            $lineEnd = ", ".$symbols{$keySymbols{'shift'}}.$lineEnd;
            $comment = " ".&unicode2utf8($unicodes{$keySymbols{'shift'}}).$comment;
            $nextSymbolExists = 1;

            $symbolNumber = 2
                if ($symbolNumber == 0);
        }
        elsif ($nextSymbolExists == 1)
        {
            $lineEnd = ", ".$voidSymbol.$lineEnd;
            $comment = "  ".$comment;
        }

        # Direct
        if (!defined($keySymbols{'direct'}) || $keySymbols{'direct'} eq "")
        {
            print STDERR "Unknown symbol: ".$key."{'direct'}\n";
            next;
        }
        if (!defined($symbols{$keySymbols{'direct'}}))
        {
            print STDERR "Unknown symbol: ".$key."{'direct'}: ".$keySymbols{'direct'}."\n";
            next;
        }

        $symbolNumber = 1
            if ($symbolNumber == 0);

        # Caps level
        my $level = "";

        $level = "type[group1] = \"".$levels[$symbolNumber-1]."_LEVEL\", "
            if (defined($keySymbols{'caps0'}) && $keySymbols{'caps0'} == 1);

        $level = "type[group1] = \"FOUR_LEVEL_SEMIALPHABETIC\", "
            if (defined($keySymbols{'caps1'}) && $keySymbols{'caps1'} == 1);

        $level = "type[group1] = \"FOUR_LEVEL_ALPHABETIC\", "
            if (defined($keySymbols{'caps2'}) && $keySymbols{'caps2'} == 1);

        $lineEnd = "[ ".$symbols{$keySymbols{'direct'}}.$lineEnd;
        $comment = " ".&unicode2utf8($unicodes{$keySymbols{'direct'}}).$comment;

        $body .= "\tkey <".$keys{$key}."> { ".$level.$lineEnd." //".$comment;
    }

    return $body;
}

sub gen_x_xkb_user_body()
{
    my $body = "\n".
               "\tinclude \"pc(pc105)\"\n";

    return $body;
}

sub gen_x_compose_body()
{
    my $body = "";
    my $previousDeadKey = "";

    for my $combo (@deadKeysA)
    {
        next
            if ($combo eq "");

        my @keyCombo = @{$combo};
        my %infos = %{$deadKeysH{$combo}};

        next
            if ((defined($infos{'notLinux'})    && $infos{'notLinux'}    == 1) ||
                (defined($infos{'windowsOnly'}) && $infos{'windowsOnly'} == 1));

        my $result = $infos{'symbol'};

        my $failed = 0;
        my $line = "";
        for my $key (@keyCombo)
        {
            if (!defined($symbols{$key}))
            {
                print STDERR "Unknown symbol: ".$key."\n";
                $failed = 1;
            }
            else
            {
                $line .= "<".$symbols{$key}."> ";
            }
        }

        if (!defined($symbols{$result}))
        {
            print STDERR "Unknown symbol: ".$result."\n";
            $failed = 1;
        }

        if (!defined($unicodes{$result}))
        {
            print STDERR "No unicode for symbol: ".$result."\n";
            $failed = 1;
        }

        next
            if ($failed == 1);

        $body .= $line.": $symbols{$result}\n";
    }

    return $body;
}

sub gen_x_xmodmap_body()
{
    my $body = "";

    for my $key (@layoutKeys)
    {
        if ($key eq "")
        {
            $body .= "\n";
            next;
        }

        if (!defined($keys{$key}))
        {
            print STDERR "Unknown key: ".$key."\n";
            next;
        }

        my %keySymbols = %{$layoutSyms{$key}};
        my $lineEnd = "\n";
        my $nextSymbolExists = 0;
        my $voidSymbol = "VoidSymbol";

        next
            if (defined($keySymbols{'windowsOnly'}) && $keySymbols{'windowsOnly'} == 1);

        # AltGr + Shift
        if (defined($keySymbols{'altgr+shift'}) && $keySymbols{'altgr+shift'} ne "")
        {
            if (!defined($symbols{$keySymbols{'altgr+shift'}}))
            {
                print STDERR "Unknown symbol: ".$key."{'altgr+shift'}: ".$keySymbols{'altgr+shift'}."\n";
                next;
            }
            $lineEnd = " ".$symbols{$keySymbols{'altgr+shift'}}.$lineEnd;
            $nextSymbolExists = 1;
        }

        # AltGr
        if (defined($keySymbols{'altgr'}) && $keySymbols{'altgr'} ne "")
        {
            if (!defined($symbols{$keySymbols{'altgr'}}))
            {
                print STDERR "Unknown symbol: ".$key."{'altgr'}: ".$keySymbols{'altgr'}."\n";
                next;
            }
            $lineEnd = " ".$symbols{$keySymbols{'altgr'}}.$lineEnd;
            $nextSymbolExists = 1;
        }
        else
        {
            $lineEnd = " ".$voidSymbol.$lineEnd
                if ($nextSymbolExists == 1);
        }

        # Shift
        if (defined($keySymbols{'shift'}) && $keySymbols{'shift'} ne "")
        {
            if (!defined($symbols{$keySymbols{'shift'}}))
            {
                print STDERR "Unknown symbol: ".$key."{'shift'}: ".$keySymbols{'shift'}."\n";
                next;
            }
            $lineEnd = " ".$symbols{$keySymbols{'shift'}}.$lineEnd;
            $nextSymbolExists = 1;
        }
        else
        {
            $lineEnd = " ".$voidSymbol.$lineEnd
                if ($nextSymbolExists == 1);
        }

        # Direct
        if (!defined($keySymbols{'direct'}) || $keySymbols{'direct'} eq "")
        {
            print STDERR "Unknown symbol: ".$key."{'direct'}\n";
            next;
        }
        if (!defined($symbols{$keySymbols{'direct'}}))
        {
            print STDERR "Unknown symbol: ".$key."{'direct'}: ".$keySymbols{'direct'}."\n";
            next;
        }

        $body .= "keycode ".$keys{$key}." = ".$symbols{$keySymbols{'direct'}}.$lineEnd;
    }

    return $body;
}

sub gen_win_msklc_bodyKeys()
{
    my $body = "";

    for my $key (@layoutKeys)
    {
        if ($key eq "")
        {
            $body .= "\r\n";
            next;
        }

        if (!defined($keys{$key}))
        {
            print STDERR "Unknown key: ".$key."\n";
            next;
        }

        if (!defined($virtualKeys{$key}))
        {
            print STDERR "Unknown virtual key: ".$key."\n";
            next;
        }

        my %keySymbols = %{$layoutSyms{$key}};

        # Caps level
        my $level = "";

        $level = "0"
            if (defined($keySymbols{'caps0'}) && $keySymbols{'caps0'} == 1);

        $level = "1"
            if (defined($keySymbols{'caps1'}) && $keySymbols{'caps1'} == 1);

        $level = "5"
            if (defined($keySymbols{'caps2'}) && $keySymbols{'caps2'} == 1);
        
        my $line = $scanCodes{$key}."\t".$virtualKeys{$key}."\t\t".$level."\t";
        my $comment = "\t//";
        my $voidSymbol = "-1";

        # Direct
        if (!defined($keySymbols{'direct'}) || $keySymbols{'direct'} eq "")
        {
            print STDERR "Unknown symbol: ".$key."{'direct'}\n";
            next;
        }
        if (!defined($symbols{$keySymbols{'direct'}}))
        {
            print STDERR "Unknown symbol: ".$key."{'direct'}: ".$keySymbols{'direct'}."\n";
            next;
        }

        $line .= $symbols{$keySymbols{'direct'}}."\t";
        $comment .= " ".&unicode2utf8($unicodes{$keySymbols{'direct'}});

        # Shift
        if (defined($keySymbols{'shift'}) && $keySymbols{'shift'} ne "")
        {
            if (!defined($symbols{$keySymbols{'shift'}}))
            {
                print STDERR "Unknown symbol: ".$key."{'shift'}: ".$keySymbols{'shift'}."\n";
                next;
            }
            $line .= $symbols{$keySymbols{'shift'}}."\t";
            $comment .= " ".&unicode2utf8($unicodes{$keySymbols{'shift'}});
        }
        else
        {
            $line .= $voidSymbol."\t";
            $comment .= "  ";
        }

        # Ctrl
        $line .= $voidSymbol."\t";

        # AltGr
        if (defined($keySymbols{'altgr'}) && $keySymbols{'altgr'} ne "")
        {
            if (!defined($symbols{$keySymbols{'altgr'}}))
            {
                print STDERR "Unknown symbol: ".$key."{'altgr'}: ".$keySymbols{'altgr'}."\n";
                next;
            }
            $line .= $symbols{$keySymbols{'altgr'}}."\t";
            $comment .= " ".&unicode2utf8($unicodes{$keySymbols{'altgr'}});
        }
        else
        {
            $line .= $voidSymbol."\t";
            $comment .= "  ";
        }

        # AltGr + Shift
        if (defined($keySymbols{'altgr+shift'}) && $keySymbols{'altgr+shift'} ne "")
        {
            if (!defined($symbols{$keySymbols{'altgr+shift'}}))
            {
                print STDERR "Unknown symbol: ".$key."{'altgr+shift'}: ".$keySymbols{'altgr+shift'}."\n";
                next;
            }
            $line .= $symbols{$keySymbols{'altgr+shift'}};
            $comment .= " ".&unicode2utf8($unicodes{$keySymbols{'altgr+shift'}});
        }
        else
        {
            $line .= $voidSymbol;
        }

        $body .= $line.$comment."\r\n";
    }

    return $body;
}

sub gen_win_msklc_bodyDeadKeys()
{
    my $body = "";
    my $previousDeadKey = "";

    for my $combo (@deadKeysA)
    {
        if ($combo eq "")
        {
            $body .= "\r\n";
            next;
        }

        my @keyCombo = @{$combo};
        my %infos = %{$deadKeysH{$combo}};

        next
            if (defined($infos{'notWindows'}) && $infos{'notWindows'} == 1);

        my $result = $infos{'symbol'};

        my $comboSize = $#keyCombo + 1;
        next
            if ($comboSize > 2); # Not supported by MSKLC

        my $deadKey = $keyCombo[0];
        my $key     = $keyCombo[1];

        if (!defined($deadKey) || $deadKey eq "")
        {
            print STDERR "Unknown deadkey\n";
            next;
        }

        if (!defined($symbols{$deadKey}) || $symbols{$deadKey} eq "")
        {
            print STDERR "Unknown deadkey: ".$deadKey."\n";
            next;
        }

        if (!defined($key) || $key eq "")
        {
            print STDERR "Unknown key\n";
            next;
        }

        if (!defined($symbols{$key}) || $symbols{$key} eq "")
        {
            print STDERR "Unknown key: ".$key."\n";
            next;
        }

        if (!defined($result) || $result eq "")
        {
            print STDERR "Unknown result symbol\n";
            next;
        }

        if (!defined($symbols{$result}) || $symbols{$result} eq "")
        {
            print STDERR "Unknown result symbol: ".$result."\n";
            next;
        }

        if ($deadKey ne $previousDeadKey)
        {
            $body .= "DEADKEY\t".lc($unicodes{$deadKey})."\r\n".
                     "\r\n";
            $previousDeadKey = $deadKey;
        }

        $body .= lc($unicodes{$key})."\t".lc($unicodes{$result})."\t// ".&unicode2utf8($unicodes{$key})." -> ".&unicode2utf8($unicodes{$result})."\r\n";
    }

    return $body;
}

sub gen_x_xkb_footer()
{
    my $footer = "\tinclude \"level3(ralt_switch)\"\n".
                 "};\n";

    return $footer;
}

sub gen_x_xkb_user_footer()
{
    my $footer = "\n".
                 "xkb_geometry { include \"pc(pc105)\" };\n".
                 "\n".
                 "};\n";

    return $footer;
}

sub gen_x_xmodmap_footer()
{
    my $footer = "keycode 0x32 = Shift_L\n".
                 "keycode 0x3E = Shift_R\n".
                 "\n".
                 "keycode 0x25 = Control_L\n".
                 "keycode 0x73 = Super_L\n".
                 "keycode 0x40 = Alt_L           Meta_L\n".
#                 "keycode 0x41 = space           nobreakspace\n".
                 "keycode 0x71 = Mode_switch     Meta_R\n".
                 "keycode 0x74 = Super_R\n".
#                 "keycode 0x75 = Menu\n".
                 "keycode 0x75 = Super_R\n".
                 "keycode 0x6D = Control_R\n".
                 "\n".
                 "add  shift   = Shift_L          Shift_R\n".
                 "add  lock    = Caps_Lock\n".
                 "add  control = Control_L        Control_R\n".
                 "add  mod1    = Alt_L\n".
                 "add  mod2    = Num_Lock\n".
                 "add  mod4    = Super_L          Super_R\n".
                 "add  mod5    = ISO_Level3_Shift\n";

    return $footer;
}

sub gen_win_msklc_footer()
{
    my $keyNames = "KEYNAME\r\n".
                   "\r\n";

    my $keyNamesExt = "KEYNAME_EXT\r\n".
                      "\r\n";

    for my $scanCode (sort keys %specialKeys)
    {
        my @array = @{$specialKeys{$scanCode}};

        $keyNames .= $scanCode."\t".$array[1]."\r\n"
            if ($#array >= 1 && $array[1] ne "");

        $keyNamesExt .= $scanCode."\t".$array[2]."\r\n"
            if ($#array == 2);
    }

    my $footer = $keyNames.
                 "\r\n".
                 $keyNamesExt.
                 "\r\n".
                 "KEYNAME_DEAD\r\n".
                 "\r\n".
                 "00b4\t\"ACUTE ACCENT\"\r\n".
                 "02dd\t\"DOUBLE ACUTE ACCENT\"\r\n".
                 "0060\t\"GRAVE ACCENT\"\r\n".
                 "005e\t\"CIRCUMFLEX ACCENT\"\r\n".
                 "02c7\t\"CARON\"\r\n".
                 "002c\t\"COMMA BELOW\"\r\n".
                 "002f\t\"STROKE\"\r\n".
                 "02d8\t\"BREVE\"\r\n".
                 "00a8\t\"DIAERESIS\"\r\n".
                 "02d9\t\"DOT ABOVE\"\r\n".
                 "00a4\t\"CURRENCY\"\r\n".
                 "00af\t\"MACRON\"\r\n".
                 "00b8\t\"CEDILLA\"\r\n".
                 "007e\t\"TILDE\"\r\n".
                 "02da\t\"RING ABOVE\"\r\n".
                 "00b5\t\"GREEK\"\r\n".
                 "02db\t\"OGONEK\"\r\n".
                 "0309\t\"HOOK ABOVE\"\r\n".
                 "031b\t\"HORN\"\r\n".
                 "0323\t\"DOT BELOW\"\r\n".
                 "\r\n".
                 "\r\n".
                 "DESCRIPTIONS\r\n".
                 "\r\n".
                 "0409\tFrench (bépo v$VERSION)\r\n".
                 "040C\tFrançais (bépo v$VERSION)\r\n".
                 "\r\n".
                 "LANGUAGENAMES\r\n".
                 "\r\n".
                 "0409\tFrench (France)\r\n".
                 "040C\tFrançais (France)\r\n".
                 "\r\n".
                 "ENDKBD\r\n";

    return $footer;
}

sub gen_x_xkb_root()
{
    &loadKeys   ($x_xkb_column);
    &loadSymbols($x_xkb_column);
    &loadLayout();

    my $header = &gen_x_xkb_header();
    my $body   = &gen_x_xkb_body();
    my $footer = &gen_x_xkb_footer();

    print $header.$body.$footer;
}

sub gen_x_xkb_user()
{
    &loadKeys   ($x_xkb_column);
    &loadSymbols($x_xkb_column);
    &loadLayout();

    my $header = &gen_x_xkb_header();
    my $body   = &gen_x_xkb_body();
    my $footer = &gen_x_xkb_footer();

    my $headerUser = &gen_x_xkb_user_header();
    my $bodyUser   = &gen_x_xkb_user_body();
    my $footerUser = &gen_x_xkb_user_footer();

    print $headerUser.$header.$bodyUser.$body.$footer.$footerUser;
}

sub gen_x_xmodmap()
{
    &loadKeys   ($x_xmodmap_column);
    &loadSymbols($x_xmodmap_column);
    &loadLayout();

    my $header = &gen_x_xmodmap_header();
    my $body   = &gen_x_xmodmap_body();
    my $footer = &gen_x_xmodmap_footer();

    print $header.$body.$footer;
}

sub gen_x_compose()
{
    &loadSymbols($x_xkb_column);
    &loadDeadKeys();

    my $header = &gen_x_compose_header();
    my $body   = &gen_x_compose_body();

    print $header.$body;
}

sub gen_win_msklc($$$)
{
    my ($vkType, $localeName, $localeId) = @_;

    &loadKeys       ($win_msklc_column);
    &loadVirtualKeys($vkType);
    &loadSymbols    ($win_msklc_column);
    &loadLayout();
    &loadDeadKeys();
    &loadSpecialKeys();

    my $header       = &gen_win_msklc_header($localeName, $localeId);
    my $bodyKeys     = &gen_win_msklc_bodyKeys();
    my $bodyDeadKeys = &gen_win_msklc_bodyDeadKeys();
    my $footer       = &gen_win_msklc_footer();

    print $header.$bodyKeys.$bodyDeadKeys.$footer;
}

sub gen_win_msklc_azerty()
{
    gen_win_msklc($vk_azerty_column, "fr-FR", "0000040c");
}

sub gen_win_msklc_bepo()
{
    gen_win_msklc($vk_bepo_column, "fr-FR", "0000040c");
}

sub gen_win_msklc_qwertz()
{
    gen_win_msklc($vk_qwertz_column, "fr-CH", "0000100c");
}

sub gen_win_msklc_dvoraj()
{
    gen_win_msklc($vk_dvoraj_column, "fr-FR", "0000040c");
}

sub gen_description_header()
{
    return "<table>\n"
        ."<tr><th>Accès direct</th><th>Shift</th><th>AltGr</th><th>AltGr + Shift</th></th>\n";
}

sub gen_description_body()
{
    my $body = "";

    for my $key (@layoutKeys)
    {
        if ($key eq "")
        {
            $body .= "\n";
            next;
        }

        if (!defined($keys{$key}))
        {
            print STDERR "Unknown key: ".$key."\n";
            next;
        }

        my %keySymbols = %{$layoutSyms{$key}};

        next
            if (defined($keySymbols{'windowsOnly'}) && $keySymbols{'windowsOnly'} == 1);

        my $line = "<tr>";

        # Direct
        if (!defined($keySymbols{'direct'}) || $keySymbols{'direct'} eq "")
        {
            print STDERR "Unknown symbol: ".$key."{'direct'}\n";
            $line .= "<td />";
        }
        elsif (!defined($symbols{$keySymbols{'direct'}}))
        {
            print STDERR "Unknown symbol: ".$key."{'direct'}: ".$keySymbols{'direct'}."\n";
            $line .= "<td />";
        }
        elsif (!defined($unicodesDescription{$unicodes{$keySymbols{'direct'}}}))
        {
            if ($unicodes{$keySymbols{'altgr'}} ne "NA")
            {
                print STDERR "No unicode description for: ".$key."{'direct'}: ".$keySymbols{'direct'}."\n";
                $line .= "<td>UNKNOWN</td>";
            }
            else
            {
                $line .= "<td />";
            }
        }
        else
        {
            $line .= "<td>".$unicodesDescription{$unicodes{$keySymbols{'direct'}}}."</td>";
        }

        # Shift
        if (!defined($keySymbols{'shift'}) || $keySymbols{'shift'} eq "")
        {
            $line .= "<td />";
        }
        elsif (!defined($symbols{$keySymbols{'shift'}}))
        {
            print STDERR "Unknown symbol: ".$key."{'shift'}: ".$keySymbols{'shift'}."\n";
            $line .= "<td />";
        }
        elsif (!defined($unicodesDescription{$unicodes{$keySymbols{'shift'}}}))
        {
            if ($unicodes{$keySymbols{'altgr'}} ne "NA")
            {
                print STDERR "No unicode description for: ".$key."{'shift'}: ".$keySymbols{'shift'}."\n";
                $line .= "<td>UNKNOWN</td>";
            }
            else
            {
                $line .= "<td />";
            }
        }
        else
        {
            $line .= "<td>".$unicodesDescription{$unicodes{$keySymbols{'shift'}}}."</td>";
        }

        # AltGr
        if (!defined($keySymbols{'altgr'}) || $keySymbols{'altgr'} eq "")
        {
            $line .= "<td />";
        }
        elsif (!defined($symbols{$keySymbols{'altgr'}}))
        {
            print STDERR "Unknown symbol: ".$key."{'altgr'}: ".$keySymbols{'altgr'}."\n";
            $line .= "<td />";
        }
        elsif (!defined($unicodesDescription{$unicodes{$keySymbols{'altgr'}}}))
        {
            if ($unicodes{$keySymbols{'altgr'}} ne "NA")
            {
                print STDERR "No unicode description for: ".$key."{'altgr'}: ".$keySymbols{'altgr'}."\n";
                $line .= "<td>UNKNOWN</td>";
            }
            else
            {
                $line .= "<td />";
            }
        }
        else
        {
            $line .= "<td>".$unicodesDescription{$unicodes{$keySymbols{'altgr'}}}."</td>";
        }

        # AltGr + Shift
        if (!defined($keySymbols{'altgr+shift'}) || $keySymbols{'altgr+shift'} eq "")
        {
            $line .= "<td />";
        }
        elsif (!defined($symbols{$keySymbols{'altgr+shift'}}))
        {
            print STDERR "Unknown symbol: ".$key."{'altgr+shift'}: ".$keySymbols{'altgr+shift'}."\n";
            $line .= "<td />";
        }
        elsif (!defined($unicodesDescription{$unicodes{$keySymbols{'altgr+shift'}}}))
        {
            if ($unicodes{$keySymbols{'altgr'}} ne "NA")
            {
                print STDERR "No unicode description for: ".$key."{'altgr+shift'}: ".$keySymbols{'altgr+shift'}."\n";
                $line .= "<td>UNKNOWN</td>";
            }
            else
            {
                $line .= "<td />";
            }
        }
        else
        {
            $line .= "<td>".$unicodesDescription{$unicodes{$keySymbols{'altgr+shift'}}}."</td>";
        }

        $body .= $line."</tr>\n";
    }

    return lc($body);
}

sub gen_description_footer()
{
    return "</table>";
}

sub gen_description()
{
    &loadKeys   ($x_xkb_column);
    &loadSymbols($x_xkb_column);
    &loadLayout();
    &loadUnicode();

    my $header = &gen_description_header();
    my $body   = &gen_description_body();
    my $footer = &gen_description_footer();

    binmode STDOUT, ":bytes";
    print $header.$body.$footer;
}


SWITCH: for ($OUTPUT_FORMAT)
{
    /x_xkb_root/i       && do { &gen_x_xkb_root();       last; };
    /x_xkb_user/i       && do { &gen_x_xkb_user();       last; };
    /x_xmodmap/i        && do { &gen_x_xmodmap();        last; };
    /x_compose/i        && do { &gen_x_compose();        last; };
    /win_msklc_azerty/i && do { &gen_win_msklc_azerty(); last; };
    /win_msklc_bepo/i   && do { &gen_win_msklc_bepo();   last; };
    /win_msklc_qwertz/i && do { &gen_win_msklc_qwertz(); last; };
    /win_msklc_dvoraj/i && do { &gen_win_msklc_dvoraj(); last; };
    /description/i      && do { &gen_description();      last; };

    die("output format must be one of the following: x_xkb_root, x_xkb_user, x_xmodmap, x_compose, win_msklc_azerty, win_msklc_bepo, win_msklc_qwertz, win_msklc_dvoraj\n");
}

