#!/usr/local/bin/perl

my $n = 0;

while (<>) {
    my ($lhs, $rhs) = split /\|/;
    for (split ' ', $rhs) {
        $n++ if /\b(\w{2,4}|\w{7})\b/;
    }
}

print $n;
