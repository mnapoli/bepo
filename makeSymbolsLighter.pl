#!/usr/bin/perl -w

use strict;

my $IN = "symbols.conf";

open(FILE, "< $IN") or die("open: $!");

LINE: while (<FILE>)
{
    chomp;
    my @array = split(/ +|\t/);

    if ($#array != 4)
    {
        print $_."\n";
    }
    else
    {
        my ($key, $unicode, $xkb, $xmodmap, $msklc) = @array;

        if (($unicode =~ /^[0-9A-Z]{4}$/) && ($key eq "U".$unicode) && ($xkb eq $key) && ($xmodmap eq $key) && ($msklc eq lc($unicode)))
        {
            print $key."\n";
        }
        else
        {
            print $_."\n";
        }
    }
}

close(FILE);

