#!/usr/bin/perl
#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ���������)
#
#  ������  : ɽӥ�� (Shining Hu)
#            ����ȱ (Ifairy Han)
#           
#  ��ҳ��ַ: http://www.CGIer.com/      CGI �����֮��
#	     http://www.LeoBoard.com/   �װ���̳֧����ҳ
#	     http://www.leoBBS.com/     ����ֱ̳ͨ��
#            http://mail@17do.com/      ���һ����
#            
#############################################################
BEGIN {
    $LBPATH = '.';
    my $pgm = $0;
    $pgm =~s/\\/\//g;
    $pgm =~s/^.*\/([^\/]+)$/$1/g;
    unless (-e $LBPATH.'/'.$pgm) {
        foreach ($0, $ENV{'SCRIPT_FILENAME'}, $ENV{'PATH_TRANSLATED'}) {
            s!\\!/!g; s/^(.*)\/[^\/]+$/$1/g;
            if (-e $_ . '/' .$pgm) { $LBPATH = $_; last; }
        }
    }
    unshift (@INC, "$LBPATH");
}
use LBCGI;
$LBCGI::POST_MAX=1024*150;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/progs.cgi";
require "data/styles.cgi";
require "lb.lib.pl";
require "testinfo.pl";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$maxline = 1500;

if ($mainonoff == 1) { &InMaintenance; } 

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
   $inmembername = "����";
}
if ($recordviewstat eq "no") { &error("�鿴��̳ͳ��&��̳����ͳ�ƹ����Ѿ����رգ�"); }
if ($statsopen == 2) {
    &getmember("$inmembername");
    print header(-charset=>gb2312);
    &error("�鿴��̳ͳ��&������Ȩ�鿴��̳ͳ�����ϣ�") if ($inmembername eq "����");
    if ($userregistered eq "no") { &error("�鿴��̳ͳ��&�㻹ûע���أ�"); }
    elsif ($inpassword ne $password) { &error("�鿴��̳ͳ��&������������⣡"); }
    &error("�鿴��̳ͳ��&��̳ͳ������ֻ��̳���Ͱ������Բ鿴��") if (($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne "mo"));
}
elsif ($statsopen == 1) {
    print header(-charset=>gb2312);
    &getmember("$inmembername");
    &error("�鿴��̳ͳ��&������Ȩ�鿴��̳ͳ�����ϣ�") if ($inmembername eq "����");
    if ($userregistered eq "no") { &error("�鿴��̳ͳ��&�㻹ûע���أ�"); }
    elsif ($inpassword ne $password) { &error("�鿴��̳ͳ��&������������⣡"); }
}

$filetoopen = "$lbdir". "data/stats.cgi";
if (-e "$filetoopen") {
  &winlock($filetoopen);
  open(LOGFILE, "$filetoopen");
  flock (LOGFILE, 2) if ($OS_USED eq "Unix");
  @logdata = <LOGFILE>;
  close(LOGFILE);
  &winunlock($filetoopen);
  $logdata = @logdata;
}
else { undef @logdata; undef $logdata; }


foreach $log (@logdata) {
    ($timeinfo, $browser, $os, $location) = split(/\|/, $log);
    if (($timeinfo ne "")&&($browser ne "")&&($os ne "")&&($location ne "")) {
	push(@timeinfo, $timeinfo);
	push(@browser, $browser);
	push(@os, $os);
	push(@location, $location);
    }
}

$output .= qq~
    <a name= top></a>
    <br><br><center>
        [<a href="#newest">������������</a>]��[<a href="#browser">�����ͳ��</a>]��
        [<a href="#os">����ϵͳͳ��</a>]��[<a href="#time">����ʱ���ͳ��</a>]��[<a href="#location">������Դͳ��</a>]
    <br><br>
<table width=95% cellpadding=0 cellspacing=0 border=0 align=center bgcolor=#000000>
<tr><td>
    <table width=100% cellpadding=5 cellspacing=1 border=0>
<tr><td colspan=2 bgcolor=$forumcolorone><a name=newest></a><a href=#top>��</a> <B>��� $newrefers �����������</B></td></tr>
~;

$filetoopen = "$lbdir". "data/refers.cgi";
if (-e "$filetoopen") {
  &winlock($filetoopen);
  open(LOGFILE, "$filetoopen");
  flock (LOGFILE, 2) if ($OS_USED eq "Unix");
  @refersdata = <LOGFILE>;
  close(LOGFILE);
  &winunlock($filetoopen);
  foreach (@refersdata) {
    ($refersurl, $ipalladdress, $timetemp) = split(/\|/, $_);
    ($ipaddresstemp, $trueipaddresstemp) = split(/\=/, $ipalladdress);
    ($ip1,$ip2,$ip3,$ip4) = split(/\./, $ipaddresstemp);
    ($ipt1,$ipt2,$ipt3,$ipt4) = split(/\./, $trueipaddresstemp);
    $ip1 = sprintf("%03d",$ip1);
    $ip2 = sprintf("%03d",$ip2);
    $ip3 = sprintf("%03d",$ip3);
    
    if ($refersurl ne "") {
        $refersurltemp = &lbhz($refersurl, 43);
        $refersurltemp = "<a href=$refersurl target=_blank title=\"$refersurl\">$refersurltemp</a>";
    }
    else { $refersurltemp = "δ֪"; }
    
    if ($ipaddresstemp eq $trueipaddresstemp) {
        $ipfromwhere = &ipwhere("$ipaddresstemp");
        $iptemp = "IP: $ip1.$ip2.$ip3.*��($ipfromwhere)";
    }
    else {
        $ipt1 = sprintf("%03d",$ipt1);
        $ipt2 = sprintf("%03d",$ipt2);
        $ipt3 = sprintf("%03d",$ipt3);
        $ipfromwhere  = &ipwhere("$ipaddresstemp");
        $ipfromwhere1 = &ipwhere("$trueipaddresstemp");
    	$iptemp = "IP1: $ip1.$ip2.$ip3.*��($ipfromwhere)<BR>IP2: $ipt1.$ipt2.$ipt3.*��($ipfromwhere1)";
    }
    $timetemp = $timetemp + ($timedifferencevalue*3600) + ($timezone*3600);
    $timetemp = &dateformat($timetemp);
    $statsout .= qq~<tr><td bgcolor=$forumcolortwo width=225><font color=$forumfontcolor>[$timetemp]<BR>$iptemp</font></td>
                <td bgcolor=$forumcolortwo><font color=$forumfontcolor>$refersurltemp</font></td></tr>~;

  }
}
else {
    $statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone>��ʱû��ͳ������ ...</td></tr>~;
}

$statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><a name=browser></a><a href=#top>��</a> <B>�����ʹ��ͳ��</B></td></tr>~;
$imgno = "1";
&datout("browser", @browser);

$statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><a name=os></a><a href=#top>��</a> <B>����ϵͳʹ��ͳ��</B></td></tr>~;
$imgno = "2";
&datout("os", @os);

$statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><a name=time></a><a href=#top>��</a> <B>����ʱ���ͳ��</B></td></tr>~;
$imgno = "4";
&timestats();

$statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><a name=location></a><a href=#top>��</a> <B>��������Դͳ��</B></td></tr>~;
$imgno = "3";
&datout("location", @location);

$statsout .= qq~</table></td></tr></table><BR><a href=#top>�����ˡ�</a><BR>~;
$output .= $statsout;		

if ($logdata >= $maxline) {
$filetoopen = "$lbdir". "data/stats.cgi";
open(FILE, ">$filetoopen");
close(FILE);
}

print $query->header(-charset=>gb2312);
$boardname = "$boardname";
&output(
-Title   => $boardname, 
-ToPrint => $output, 
-Version => $versionnumber 
);


sub sum {
    my ($aref) = @_;
    my ($total) = 0;
    foreach (@$aref) { $total += $_ }
    return $total;
}

sub datout {
  my ($filename, @datin) = @_;
  my @savedbrowser; my @savedbrowsers; my @savedcount;

  my $filetoopen = "$lbdir". "data/$filename.cgi";
  if (-e "$filetoopen") {
	open(FILE, "$filetoopen");
	@filedat = <FILE>;
	close(FILE);
	$i = 0;
	foreach (@filedat) {
	    chomp $_;
	    next if ($_ eq "");
	    ($count1, $browser1) = split(/\|/, $_);
	    $browser1 =~ s/\n//;
	    $browser1 =~ s/\)//;
	    $browser1 =~ s/\(//;
	    push (@savedbrowsers, $browser1);
	    $savedcount[$i] = $count1;
	    $i++;
	}
  }

  if (($logdata ne "")&&($logdata > 0)) {
    foreach $browser (@datin) {
	$grepbrow = $browser;
	$grepbrow =~ s/\n//;
	$grepbrow =~ s/\)//;
	$grepbrow =~ s/\(//;
	if (grep(/$grepbrow/, @savedbrowsers)) {
	   $arrsize = @savedbrowsers;
	   for ($i = 0; $i <= $arrsize; $i++) {
	   	if ($browser eq $savedbrowsers[$i]) {
	   	    $savedcount[$i]++;
		}
	   }
	} else {
	  push (@savedbrowsers, $browser);
	  $savedcount[$#savedbrowsers] = 1;
	}
    }

    for ($i = 0; $i <= $#savedbrowsers; $i++) {
      if ($savedbrowsers[$i] && $savedcount[$i]) {
	$itemtosave = "$savedcount[$i]|$savedbrowsers[$i]";
	push (@savedbrowser, $itemtosave);
      }
    }
  }
	
  @savedbrowser  = sort { $b <=> $a } @savedbrowser;
  $totalvisits = sum(\@savedcount);
  
  if ($totalvisits > 0) {
    foreach $browsers (@savedbrowser) {
	($count, $browser) = split(/\|/, $browsers);
	$percent = int(($count / $totalvisits) * 1000)/10;
	$picper  = int(sqrt($percent * 4)*10);
	$statsout .= qq~<tr><td bgcolor=$forumcolortwo><font color=$forumfontcolor>$browser</font></td>
	<td bgcolor=$forumcolortwo><font color=$forumfontcolor><img src=$imagesurl/images/bar$imgno.gif width=$picper height=10> <B>$count</B> ($percent%)</font></td></tr>
	~;
    }
  }
  else {
    $statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone>��ʱû��ͳ������ ...</td></tr>~;
  }
  
  if ($logdata >= $maxline) {
	$filetoopen = "$lbdir". "data/$filename.cgi";
	open(FILE, ">$filetoopen");
	flock (FILE, 2) if ($OS_USED eq "Unix");
	foreach $browser (@savedbrowser) {
	    next if ($browser eq "");
	    print FILE "$browser\n";
	}
	close(FILE);
  }
}


sub timestats {
  my $addtotle= 0;
  my $filetoopen = "$lbdir". "data/time.cgi";
  if (-e "$filetoopen") {
	open(FILE, "$filetoopen");
	@timedat = <FILE>;
	close(FILE);
	$i = 0;
        foreach (@timedat) {
            chomp $_;
	    next if ($_ eq "");
	    $outvar = "{$i}hour";
	    ${$outvar} = $_;
	    $addtotle += $_;
	    $i ++;
	}
  }

  if (($logdata ne "")&&($logdata > 0)) {
    $timeinfono = @timeinfo + 1;
    foreach $timeinfo (@timeinfo) {
      $timeinfo = $timeinfo + ($timedifferencevalue*3600) + ($timezone*3600);
      $timeinfo = &dateformat($timeinfo);
	for ($i = 0; $i <= 12; $i++) {
	    if ($timeinfo =~ /$i:\d\dam/) {
		$outvar = "{$i}hour";
		${$outvar}++;
	    } elsif ($timeinfo =~ /$i:\d\dpm/) {
		$td = $i;
		$td += 12 if ($i ne 12);
		$outvar = "{$td}hour";
		${$outvar}++;
	    }
	}
    }
  }
  else {$timeinfono = 0; }

  $addtotle = $timeinfono+$addtotle;
  
  if ($addtotle > 0 ) {
    for ($i = 0; $i < 24; $i++) {
	$outvar = "{$i}hour";
	if (! ${$outvar}) {
	   ${$outvar} = 0;
	}
	$percent = int((${$outvar} / $addtotle) * 1000)/10;
	$picper = int(sqrt($percent * 4)*10);
	$ii = $i;
	$ii = "0$ii" if ($ii <= 9);
	$statsout .= qq~
	<tr>
	<td bgcolor=$forumcolortwo><font color=$forumfontcolor>$ii:00 - $ii:59</font></td>
	<td bgcolor=$forumcolortwo><font color=$forumfontcolor><img src=$imagesurl/images/bar$imgno.gif width=$picper height=10> <B>${$outvar}</B> ($percent%)</font></td>
	</tr>
	~;
    }
  }
  else {
    $statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone>��ʱû��ͳ������ ...</td></tr>~;
  }

  
  if ($logdata >= $maxline) {
	$filetoopen = "$lbdir". "data/time.cgi";
	open(FILE, ">$filetoopen");
	flock (FILE, 2) if ($OS_USED eq "Unix");
	for ($i = 0; $i <= 24; $i++) {
	    $outvar = "{$i}hour";
	    if (! ${$outvar}) {
	        ${$outvar} = 0;
	    }
	    print FILE "${$outvar}\n";
	}
	close(FILE);
  }
}
