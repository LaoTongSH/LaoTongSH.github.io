#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ����������)
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
#########���ò���#############
$hownews="50"; #С�ֱ�����������
#########���ò���#############
print "Content-type: text/html\n\n";
if ($IN{do} eq "ok"){&dook;}
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>����С�ֱ�</title>
</head>
<body>
<ul>����С�ֱ���<ul>
<form action="topnews.cgi" method="post"><input type="hidden" name="do" value="ok">
�û�����<input type="text" name="username"><br>
�� &nbsp;�룺<input type="password" name="passwd">
<p>
��ĿС�ֱ�: <input type="text" name="content" size="50"><p>
<input type="submit" value="����">
</form>
<p style="font-size:9pt">˵��: ~С�ֱ�������$hownews���ַ���~
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
if ($topnews[0] eq $thistime){print "��Ǹ��һСʱ��ֻ����һ���˷���С�챨,��ӭ���¸�Сʱ׼ʱ����������~��<p><a href=javascript:window.close()>�رմ���</a>";exit;}
unless ($IN{content}){print "��Ǹ����������дС�ֱ�������~��<p><a href=javascript:window.close()>�رմ���</a>";exit;}
$content=$IN{content};
$stop=$hownews*2;
for ($i=0;$i< $stop;$i++){chop($IN{content});}
if ($IN{content}){print "��Ǹ��С�ֱ������ݲ��ܳ���$hownews����~��<p><a href=javascript:window.close()>�رմ���</a>";exit;}
$IN{username}=~tr/\\n//;
$username=$IN{username};
$IN{username}=~tr/A-Z/a-z/;

&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($IN{username} =~  m/\//)||($IN{username} =~ m/\\/)||($IN{username} =~ m/\.\./));
$IN{username} =~ s/\///g;
$IN{username} =~ s/\.\.//g;
$IN{username} =~ s/\\//g;

open (FILE, "${cgipath}$memdir/$IN{username}.cgi")||((print "��Ǹ�����û��������ڣ�")&&(exit));
$memberdaten=<FILE>;
close (FILE);
@memberdaten = split(/\t/,$memberdaten);
unless ($IN{passwd} eq $memberdaten[1]){print "��Ǹ���������벢����ȷ!<p><a href=javascript:window.close()>�رմ���</a>";exit;}
open (FILE, ">${cgipath}data/topnews.txt");
print FILE "$thistime\n";
print FILE "$username\n";
print FILE "$content\n";
close (FILE);
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>����С�ֱ�</title>
</head>
<body>
<ul>�����ɹ���<ul><p><a href=javascript:window.close()>�رմ���</a>
</body>
</html>
EOF
exit;
}