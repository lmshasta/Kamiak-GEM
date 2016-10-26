#!/usr/bin/env perl

use strict;
use warnings;
use File::Find;

my %GEM;
my %transcripts;

find (\&process_fpkm_file,  "./");

sub process_fpkm_file {
  my $cwd = $File::Find::dir;
  my $file = $_;
  my $path = $File::Find::name;

  return if ($cwd eq '.');
  return if ($cwd eq './logs');
  return if ($cwd eq './reference');
  return if ($file !~ m/\.fpkm$/);

  my $sample = $file;
  $sample =~ s/^(.*)_vs_.*$/$1/;

  open (FPKM, $file) or die $!;
  while (my $line = <FPKM>) {
   chomp($line);
   my @cols = split(/\t/, $line);
   $transcripts{$cols[0]} = 1;
   if ($cols[1] > 0) {
     $GEM{$sample}{$cols[0]} = $cols[1];
   }
   else {
     $GEM{$sample}{$cols[0]} = 'NA';
   }
  }
  close(FPKM);
}

# Add the header
my $header = '';
foreach my $sample (sort keys %GEM) {
  $header .= $sample . "\t";
}
chop($header);
print $header . "\n";

foreach my $transcript (sort keys %transcripts) {
  print "$transcript";  
  foreach my $sample (sort keys %GEM) {
    print "\t" . $GEM{$sample}{$transcript};
  }
  print "\n";
}
