#!/usr/bin/perl
#############################################################
#  LeoBoard ver.5000 / LB5000 / 雷傲超级论坛 ver.5000
#
#  版权所有: 雷傲工作室(原蓝宝石软件工作室)
#
#  制作人  : 山鹰糊 (Shining Hu)
#            花无缺 (Ifairy Han)
#           
#  主页地址: http://www.CGIer.com/      CGI 编程者之家
#	     http://www.LeoBoard.com/   雷傲论坛支持主页
#	     http://www.leoBBS.com/     本论坛直通车
#            http://mail@17do.com/      大家一起邮
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
&ipbanned; #封杀一些 ip

$maxline = 1500;

if ($mainonoff == 1) { &InMaintenance; } 

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
   $inmembername = "客人";
}
if ($recordviewstat eq "no") { &error("查看论坛统计&论坛访问统计功能已经被关闭！"); }
if ($statsopen == 2) {
    &getmember("$inmembername");
    print header(-charset=>gb2312);
    &error("查看论坛统计&客人无权查看论坛统计资料！") if ($inmembername eq "客人");
    if ($userregistered eq "no") { &error("查看论坛统计&你还没注册呢！"); }
    elsif ($inpassword ne $password) { &error("查看论坛统计&你的密码有问题！"); }
    &error("查看论坛统计&论坛统计资料只有坛主和版主可以查看！") if (($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne "mo"));
}
elsif ($statsopen == 1) {
    print header(-charset=>gb2312);
    &getmember("$inmembername");
    &error("查看论坛统计&客人无权查看论坛统计资料！") if ($inmembername eq "客人");
    if ($userregistered eq "no") { &error("查看论坛统计&你还没注册呢！"); }
    elsif ($inpassword ne $password) { &error("查看论坛统计&你的密码有问题！"); }
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
        [<a href="#newest">最近访问者情况</a>]　[<a href="#browser">浏览器统计</a>]　
        [<a href="#os">操作系统统计</a>]　[<a href="#time">访问时间段统计</a>]　[<a href="#location">访问来源统计</a>]
    <br><br>
<table width=95% cellpadding=0 cellspacing=0 border=0 align=center bgcolor=#000000>
<tr><td>
    <table width=100% cellpadding=5 cellspacing=1 border=0>
<tr><td colspan=2 bgcolor=$forumcolorone><a name=newest></a><a href=#top>↑</a> <B>最近 $newrefers 名访问者情况</B></td></tr>
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
    else { $refersurltemp = "未知"; }
    
    if ($ipaddresstemp eq $trueipaddresstemp) {
        $ipfromwhere = &ipwhere("$ipaddresstemp");
        $iptemp = "IP: $ip1.$ip2.$ip3.*　($ipfromwhere)";
    }
    else {
        $ipt1 = sprintf("%03d",$ipt1);
        $ipt2 = sprintf("%03d",$ipt2);
        $ipt3 = sprintf("%03d",$ipt3);
        $ipfromwhere  = &ipwhere("$ipaddresstemp");
        $ipfromwhere1 = &ipwhere("$trueipaddresstemp");
    	$iptemp = "IP1: $ip1.$ip2.$ip3.*　($ipfromwhere)<BR>IP2: $ipt1.$ipt2.$ipt3.*　($ipfromwhere1)";
    }
    $timetemp = $timetemp + ($timedifferencevalue*3600) + ($timezone*3600);
    $timetemp = &dateformat($timetemp);
    $statsout .= qq~<tr><td bgcolor=$forumcolortwo width=225><font color=$forumfontcolor>[$timetemp]<BR>$iptemp</font></td>
                <td bgcolor=$forumcolortwo><font color=$forumfontcolor>$refersurltemp</font></td></tr>~;

  }
}
else {
    $statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone>暂时没有统计数据 ...</td></tr>~;
}

$statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><a name=browser></a><a href=#top>↑</a> <B>浏览器使用统计</B></td></tr>~;
$imgno = "1";
&datout("browser", @browser);

$statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><a name=os></a><a href=#top>↑</a> <B>操作系统使用统计</B></td></tr>~;
$imgno = "2";
&datout("os", @os);

$statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><a name=time></a><a href=#top>↑</a> <B>访问时间段统计</B></td></tr>~;
$imgno = "4";
&timestats();

$statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><a name=location></a><a href=#top>↑</a> <B>访问者来源统计</B></td></tr>~;
$imgno = "3";
&datout("location", @location);

$statsout .= qq~</table></td></tr></table><BR><a href=#top>↑顶端↑</a><BR>~;
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
    $statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone>暂时没有统计数据 ...</td></tr>~;
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
    $statsout .= qq~<tr><td colspan=2 bgcolor=$forumcolorone>暂时没有统计数据 ...</td></tr>~;
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
