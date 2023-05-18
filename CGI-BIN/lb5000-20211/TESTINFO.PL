sub ipwhere {
    my $fromwhere = shift;
    (my $ip1,my $ip2,my $ip3,my $ip4)=split(/\./,$fromwhere);
    my $ips=$ip1*1000000000+$ip2*1000000+$ip3*1000+$ip4;
    $ip1=int($ip1);
    if (-f "${lbdir}data/$ip1.txt") {
        $datafile="${lbdir}data/".$ip1.".txt";
    }
    else {
        $datafile="${lbdir}data/other.txt";
    }
    open(IPF,"$datafile");
    my @ipdata=<IPF>;
    close(IPF);
    for ($i=0;$i<@ipdata;$i++){
        ($ip1,$ip2,$from1,$from2)=split(/__/,$ipdata[$i]);
        (my $ipa1,my $ipa2,my $ipa3,my $ipa4)=split(/\./,$ip1);
        (my $ipb1,my $ipb2,my $ipb3,my $ipb4)=split(/\./,$ip2);
        my $ipbegin =$ipa1*1000000000+$ipa2*1000000+$ipa3*1000+$ipa4;
        my $ipend =$ipb1*1000000000+$ipb2*1000000+$ipb3*1000+$ipb4;
        if (($ips<=$ipend)&&($ips>=$ipbegin)) {
            last;
        }
    }
    if ($from1 eq "") { $fromwhere="Î´ÖªµØÇø"; }
    else {$fromwhere="$from1$from2";}
    $fromwhere =~ s/[\n\r\)\(]//isg;
    return $fromwhere;
}
sub osinfo {
   local $os="",$Agent;
   $Agent = $ENV{'HTTP_USER_AGENT'};
   if (($Agent =~ /win/i)&&($Agent =~ /95/i)) {
      $os="Windows 95";
   }
   elsif (($Agent =~ /win 9x/i)&&($Agent =~ /4.90/i)) {
      $os="Windows ME";
   }
   elsif (($Agent =~ /win/i)&&($Agent =~ /98/i)) {
      $os="Windows 98";
   }
   elsif (($Agent =~ /win/i)&&($Agent =~ /nt 5\.0/i)) {
      $os="Windows 2000";
   }
   elsif (($Agent =~ /win/i)&&($Agent =~ /nt 5\.1/i)) {
      $os="Windows XP";
   }
   elsif (($Agent =~ /win/i)&&($Agent =~ /nt/i)) {
      $os="Windows NT";
   }
   elsif (($Agent =~ /win/i)&&($Agent =~ /32/i)) {
      $os="Windows 32";
   }
   elsif ($Agent =~ /linux/i) {
      $os="Linux";
   }
   elsif ($Agent =~ /unix/i) {
      $os="Unix";
   }
   elsif (($Agent =~ /sun/i)&&($Agent =~ /os/i)) {
      $os="SunOS";
   }
   elsif (($Agent =~ /ibm/isg)&&($Agent =~ /os/isg)) {
      $os="IBM OS/2";
   }
   elsif (($Agent =~ /Mac/i)&&($Agent =~ /PC/i)) {
      $os="Macintosh";
   }
   elsif ($Agent =~ /FreeBSD/i) {
      $os="FreeBSD";
   }
   elsif ($Agent =~ /PowerPC/i) {
      $os="PowerPC";
   }
   elsif ($Agent =~ /AIX/i) {
      $os="AIX";
   }
   elsif ($Agent =~ /HPUX/i) {
      $os="HPUX";
   }
   elsif ($Agent =~ /NetBSD/i) {
      $os="NetBSD";
   }
   elsif ($Agent =~ /BSD/i) {
      $os="BSD";
   }
   elsif ($Agent =~ /OSF1/i) {
      $os="OSF1";
   }
   elsif ($Agent =~ /IRIX/i) {
      $os="IRIX";
   }
  $os = "Unknown"  if ($os eq '');
  $os =~ s/[\n\r\)\(]//isg;
  return $os;
}
sub browseinfo {
   local $browser="",$browserver="",@Browsers = ("Lynx","MOSAIC","AOL","Opera","JAVA","MacWeb","WebExplorer","OmniWeb"),$Agent,$Part;
   $Agent = $ENV{'HTTP_USER_AGENT'};
   foreach (@Browsers) {
      if ($Agent =~/$_/i) {
         $browser = $_;
         $browserver ="";
      }
   }
   if (($Agent =~ "Mozilla")&&($Agent !~ "MSIE")) {
      $Part =(split(/\(/, $Agent))[0];
      $browserver = (split(/\//, $Part))[1];
      $browserver = (split(/ /,$browserver))[0];
      $browserver =~ s/([\d\.]+)/$1/isg;
      $browserver = " $browserver";
      $browser = "Netscape Navigator";
   }
   if (($Agent =~ "Mozilla")&&($Agent =~ "Opera")) {
      $Part =(split(/\(/, $Agent))[1];
      $browserver = (split(/\)/, $Part))[1];
      $browserver = (split(/ /,$browserver))[2];
      $browserver =~ s/([\d\.]+)/$1/isg;
      $browserver = " $browserver";
      $browser = "Opera";
   }
   if (($Agent =~ "Mozilla")&&($Agent =~ "MSIE")) {
      $Part = (split(/\(/, $Agent))[1];
      $Part = (split(/\;/,$Part))[1];
      $browserver = (split(/ /,$Part))[2];
      $browserver =~ s/([\d\.]+)/$1/isg;
      $browserver = " $browserver";
      $browser = "Internet Explorer";
   }
  if ($browser ne '') {
      $browserver =~ s/[^0-9\.b]//isg;
      $browserver = &lbhz($browserver,4) if (length($browserver) > 10);
      $browseinfo = "$browser $browserver";
  }
  else {
      $browseinfo = "Unknown";
  }
  $browseinfo =~ s/[\n\r\)\(]//isg;
  return $browseinfo;
}
1;