#!/usr/bin/perl
###################################################
# LB5000 首页显示用户排名 ver 1.00
# 程序编制： 任逍遥  xoyoren@inhe.net
# 版权所有： CGI 编程者之家  http://www.CGIer.com
###################################################
# 使用办法： showmem.cgi?show=显示数量
# 例： 在你主页的适当位置加入以下语句
#      <script src="showmem.cgi?show=20"></script>
#      这样就可以在相应位置显示论坛的用户前20名
#
#   如果不需要显示这么详细，请自己看这个程序最后的
#   输出部分，删除掉不要显示的列，就可以了。
###################################################
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
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "lb.lib.pl";

&ReadParse;
$show = $in{'show'} or 20;

$|++;
$thisprog = "showmem.cgi";
print "Content-type: text/html; charset=gb2312\n\n";

$filetoopen = "$lbdir" . "data/onlinedata.cgi";
&winlock($filetoopen);
open(FILE,"<$filetoopen");
flock (FILE, 1) if ($OS_USED eq "Unix");
@onlinedata1 = <FILE>;
close(FILE);
&winunlock($filetoopen);

foreach(@onlinedata1) {
	($name,$no,$gone) = split(/\t/);
	if((time - $gone) > ($membergone * 60)) {
		$_ = '';
	} else {
		$_ = $name;
	}
	
}
@onlinedata1 = grep(/.+/,@onlinedata1);
$filetoopen = "${lbdir}data/lbmember.cgi";
&winlock($filetoopen);
open(FILE,"<$filetoopen");
flock (FILE, 1) if ($OS_USED eq "Unix");
@members = <FILE>;
close(FILE);
&winunlock($filetoopen);
@memberstats = ();
foreach(@members) {
	($membername,$title,$post,$regtime,$email) = split(/\t/);
	if(grep(/^$membername$/i,@onlinedata1)) {
		$memberstat = "<font color=#FF0000>在线</font>";
	} else {
		$memberstat = "不在线";
	}
	push(@memberstats,"$membername\t$post\t$memberstat");
}
@memberstats = sort bypost @memberstats;

$str = "";
$str.= "<table cellspacing=0 cellpadding=0 border=0 width=100%>";
$str.= "<tr><td align=center><b>名字</b></td><td align=center><b>发贴量</b></td><td align=center><b>状态</b></td></tr>";
$i = 0;
while(($i < $show) and ($this = $memberstats[$i])) {
	($name,$post,$status) = split(/\t/,$this);
	$str .= "<tr><td align=center><a href=$boardurl/profile.cgi?action=show&member=$name>$name</a></td><td align=center>$post</td><td align=center>$status</td></tr>";
	$i++;
}
$str .= "</table>";
print "document.write('$str')\n";
exit;

sub ReadParse {
if ($ENV{'REQUEST_METHOD'} eq "POST") {
  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
} 
else {
  $buffer = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
   ($name, $value) = split(/=/, $pair);
   $value =~ tr/+/ /;
   $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
   $value =~ s/<!--(.|\n)*-->//g;
   $value =~ s/__/--/g;
   $value =~ s/>/&gt;/g;
   $value =~ s/</&lt;/g;
   $value =~ s/\t//g;
   $in{$name} = $value;
}
}
sub bypost {
	($no,$posta,$no) = split(/\t/,$a);
	($no,$postb,$no) = split(/\t/,$b);
	$postb <=> $posta;
}
