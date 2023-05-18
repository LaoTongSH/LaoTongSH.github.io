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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$thisprog = "rateit.cgi";

$query = new LBCGI;

&ipbanned; #封杀一些 ip

print $query->header(-charset=>gb2312);

$access = qq(非法操作，不允许！);

$rate=$query->param("rateselect");
$inforum=$query->param("id");
$intopic=$query->param("forumname");
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$filerequire = "$lbdir" . "data/style${inforum}.cgi";
if (-e $filerequire) { require $filerequire; }

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
$stylequire = "$lbdir" . "data/skin/${inselectstyle}.cgi";
if ($inselectstyle ne ""){
    if (-e $stylequire){require $stylequire;}
}

$myip=$ENV{'REMOTE_HOST'};
$myip=$ENV{'REMOTE_ADDR'} if ($myip eq "");
if ($id =~ /[a-zA-Z\.]/) {print $access; exit;}
if ($threadname =~ /[a-zA-Z\.]/) {print $access; exit;}

if ($rate == 0 or $rate >= 6) { &error("投票评分&你投的是什么票呀？我怎么不懂的！"); }

if (-e "$lbdir/forum$inforum/rateip$intopic.file.pl") {
	open(IP, "$lbdir/forum$inforum/rateip$intopic.file.pl");
	while(<IP>) {
	    $thisip=$_;
	    chomp($thisip);
	    if ($thisip eq $myip) { &error("投票评分&对不起，你好像已经对这个主题投过票了。"); }
	}
	close(IP);

	$filetomake = "$lbdir/forum$inforum/rateip$intopic.file.pl";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(IP, ">>$filetomake");
	flock(IP,2) if ($OS_USED eq "Unix");
	print IP "$myip\n";
	close(IP);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
}
else {
	$filetomake = "$lbdir/forum$inforum/rateip$intopic.file.pl";
	&winlock($filetomake) if ($OS_USED eq "Nt");
        open(IP, ">$filetomake");
        flock(IP,2) if ($OS_USED eq "Unix");
        print IP "$myip\n";
        close(IP);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
}

if (-e "$lbdir/forum$inforum/rate$intopic.file.pl") {
	require "$lbdir/forum$inforum/rate$intopic.file.pl";
	$votes = $votes +1;
	$rates = $rates + $rate;
	$average = int($rates / $votes);
	$filetomake = "$lbdir/forum$inforum/rate$intopic.file.pl";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(WRITE, ">$filetomake") || die ("不能打开 $filetomake 文件！<br> $!");
	flock(WRITE,2) if ($OS_USED eq "Unix");
	print WRITE "\$votes = $votes\;\n";
	print WRITE "\$rates = $rates\;";
	close(WRITE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	&ratings
}
else {
	$votes = 1;
	$rates = $rate;
	$average = $rate;
	$filetomake = "$lbdir/forum$inforum/rate$intopic.file.pl";
        &winlock($filetomake) if ($OS_USED eq "Nt");
	open(WRITE, ">$filetomake") || die ("不能打开 $filetomake 文件！<br> $!");
	flock(WRITE,2) if ($OS_USED eq "Unix");
	print WRITE "\$votes = $votes\;\n";
	print WRITE "\$rates = $rates\;";
	close(WRITE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	&ratings
}

sub ratings {
    $inmembername = cookie("amembernamecookie");
    $inpassword = cookie("apasswordcookie");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
    &title;
    $relocurl = "$threadprog?forum=$inforum&topic=$intopic";
    $output .= qq~
      <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
       <tr>
        <td width=30% rowspan=2 valign=top><img src=$imagesurl/images/$boardlogo border=0></td>
        <td valign=top align=left>
    ~;
    if ($indexforum ne "no"){
	$output .= qq~
        <font face=$font color=$fontcolormisc>
        　<img src=$imagesurl/images/closedfold.gif border=0 width=15 height=11>　<a href="$forumsummaryprog">$boardname</a><br>
        　<img src=$imagesurl/images/bar.gif border=0><img src="$imagesurl/images/openfold.gif" border=0 width=15 height=11>　 评分完成
	~;
    }else{
	$output .= qq~
        <font face=$font color=$fontcolormisc>
	<img src="$imagesurl/images/openfold.gif" border=0 width=15 height=11>　 评分完成
 	~;
    }
    $output .= qq~
        </td>
      </tr>
      </table>
	<p>
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font color=$fontcolormisc><b>评分完成</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>
            如果浏览器没有自动返回，请点击下列链接！
            <ul>
            <li><a href=$threadprog?forum=$inforum&topic=$intopic>返回当前主题</a>
            <li><a href=$forumsprog?forum=$inforum>返回当前论坛</a>
            <li><a href=$forumsummaryprog>返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
	<meta http-equiv="refresh" content="3; url=$relocurl">
    ~;

    &output(
        -Title   => $boardname,
        -ToPrint => $output,
        -Version => $versionnumber
    );
}
	