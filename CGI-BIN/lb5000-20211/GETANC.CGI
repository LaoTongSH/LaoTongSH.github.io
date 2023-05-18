#!/usr/bin/perl
###################################################################################
# LB5000 公告显示 ver 1.5
# 版权所有： CGI 编程者之家  http://www.CGIer.com
###################################################################################
# 使用办法： getanc.cgi?max=显示公告长度
# 例： 在你主页的适当位置加入以下语句
#      <script src="getanc.cgi?max=500"></script>
#      这样就可以在相应位置显示论坛的最新公告的前 500 字符。
#      如果想不限制显示字符数，可以设置 max 参数的值为 99999999，比如：
#      <script src="getanc.cgi?max=99999999"></script>
#
#      所有参数均可以省略，默认显示公告的前面 500 字符。
###################################################################################
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
require "code.cgi";
require "data/boardinfo.cgi";
require "lb.lib.pl";

$|++;
$query = new LBCGI;
$max	= $query -> param('max');
$max    = &stripMETA("$max");
$max	= 500 if ($max eq "");        # 默认显示公告的前 500 字符

print header(-charset=>gb2312);

    $filetoopen = "$lbdir" . "data/news.cgi";
    if (-e "$filetoopen") {
    	open(FILE, "$filetoopen");
    	flock (FILE, 1) if ($OS_USED eq "Unix");
        @announcements = <FILE>;
        close(FILE);
        ($title, $dateposted, $post, $nameposted) = split(/\t/, $announcements[0]);
                
      if ($post ne "") {
        $dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
	$dateposted = &dateformat("$dateposted");
	        
	$post = &lbcode("$post");
	$post = &doemoticons("$post");
	$post = &smilecode("$post");
	$title =~ s/\'/\`/;
	$title =~ s/\&amp;/\&/g;
	$title =~ s/\&quot;/\"/g;
	$title =~ s/\&lt;/</g;
	$title =~ s/\&gt;/>/g;
	$title =~ s/ \&nbsp;/　/g;
	$title =~ s/  /　/g;
	$post =~ s/\'/\`/;
	$post =~ s/\&amp;/\&/g;
	$post =~ s/\&quot;/\"/g;
	$post =~ s/\&lt;/</g;
	$post =~ s/\&gt;/>/g;
	$post =~ s/ \&nbsp;/　/g;
	$post =~ s/  /　/g;
	if (length($post)>$max) {
	    $post = &lbhz("$post",$max) . "<p align=right><a href=$boardurl/announcements.cgi target=_blank>More>>></a>&nbsp;</p>";
	}
	$str=qq~ 
	<table width=95% border=0 cellspacing=0 cellpadding=0>
	<tr valign=top><td height=158> 
	<b>$title</b><br>$post
	</td></tr>
	<tr valign=top><td height=18 align=right>
	<br>$nameposted　　$dateposted&nbsp;
	</td></tr>
	</table>~;
      }
      else {
	$str = "当前没有公告！";
      }
    }
    else {
	$str = "当前没有公告！";
    }
$str=~s /\n//isg;
print "document.write('$str')\n";
exit;
