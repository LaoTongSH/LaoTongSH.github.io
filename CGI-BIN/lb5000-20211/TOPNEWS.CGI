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
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$| = 1;
if ($ENV{'REQUEST_METHOD'} eq "POST") {read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});}
else {$buffer = $ENV{'QUERY_STRING'};}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {($name, $value) = split(/=/, $pair);
$value =~ tr/+/ /;
$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$value =~ s/<//g;
$value =~ s/>//g;
$value =~ s/\n//g;
$IN{$name} = $value;}
$cgipath="$lbdir";
#########设置部分#############
$hownews="50"; #小字报的字数限制
#########设置部分#############
print "Content-type: text/html\n\n";
if ($IN{do} eq "ok"){&dook;}
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>发表小字报</title>
</head>
<body>
<ul>发表小字报：<ul>
<form action="topnews.cgi" method="post"><input type="hidden" name="do" value="ok">
用户名：<input type="text" name="username"><br>
密 &nbsp;码：<input type="password" name="passwd">
<p>
醒目小字报: <input type="text" name="content" size="50"><p>
<input type="submit" value="发表">
</form>
<p style="font-size:9pt">说明: ~小字报限制在$hownews个字符内~
</body>
</html>
EOF
sub dook{
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday)= localtime(time+(3600*$time_hour));
$mon=$mon+1;
if($mon <10){$mon="0".$mon;}
if($mday<10){$mday="0".$mday;}
if($hour<10){$hour="0".$hour;}
if($min<10){$min="0".$min;}
if($sec<10){$sec="0".$sec;}
$year=$year+1900;
$thistime="$year$mon$mday$hour";
open (FILE, "${cgipath}data/topnews.txt");
@topnews=<FILE>;
close (FILE);
chomp($topnews[0]);
if ($topnews[0] eq $thistime){print "抱歉，一小时内只允许一个人发表小快报,欢迎您下个小时准时抢先来发表~！<p><a href=javascript:window.close()>关闭窗口</a>";exit;}
unless ($IN{content}){print "抱歉，您必须填写小字报的内容~！<p><a href=javascript:window.close()>关闭窗口</a>";exit;}
$content=$IN{content};
$stop=$hownews*2;
for ($i=0;$i< $stop;$i++){chop($IN{content});}
if ($IN{content}){print "抱歉，小字报的内容不能超过$hownews个字~！<p><a href=javascript:window.close()>关闭窗口</a>";exit;}
$IN{username}=~tr/\\n//;
$username=$IN{username};
$IN{username}=~tr/A-Z/a-z/;

&error("普通错误&老大，别乱黑我的程序呀！") if (($IN{username} =~  m/\//)||($IN{username} =~ m/\\/)||($IN{username} =~ m/\.\./));
$IN{username} =~ s/\///g;
$IN{username} =~ s/\.\.//g;
$IN{username} =~ s/\\//g;

open (FILE, "${cgipath}$memdir/$IN{username}.cgi")||((print "抱歉，此用户并不存在！")&&(exit));
$memberdaten=<FILE>;
close (FILE);
@memberdaten = split(/\t/,$memberdaten);
unless ($IN{passwd} eq $memberdaten[1]){print "抱歉，您的密码并不正确!<p><a href=javascript:window.close()>关闭窗口</a>";exit;}
open (FILE, ">${cgipath}data/topnews.txt");
print FILE "$thistime\n";
print FILE "$username\n";
print FILE "$content\n";
close (FILE);
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>发表小字报</title>
</head>
<body>
<ul>发表成功！<ul><p><a href=javascript:window.close()>关闭窗口</a>
</body>
</html>
EOF
exit;
}
