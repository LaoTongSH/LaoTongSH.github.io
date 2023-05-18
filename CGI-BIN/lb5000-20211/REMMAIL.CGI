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
#            http://maildo.com/      大家一起邮
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
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                        # Unbuffer the output

########################## Program #####################################

$thisprog = "remmail.cgi";

$query = new LBCGI;

@params = $query->param;
foreach $param(@params) {
    $theparam = $query->param($param);
    $theparam = &unHTML("$theparam");
    ${$param} = $theparam;
}

$inmembername = $query->cookie("amembernamecookie");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if (lc($inmembername) eq lc($member)) {
 $filetoopen = "$lbdir" . "data/remmem.cgi";
 open (FILE,"$filetoopen");
 flock (FILE,2);
  @members = <FILE>;
 close (FILE);

foreach $removed (@members) {
 chomp($removed);
 if ($removed eq $member) {
  $output = qq~
   <tr bgcolor="#FFFFFF">
   <td align="center">
   你好，$member：你已经退出 LB5000 邮件列表了。
   </td>
   </tr>
  ~;
  &displayoutput;
 }
}


$filetoopen = "$lbdir" . "data/remmem.cgi";
open (FILE,">>$filetoopen");
 print FILE "$member\n";
close (FILE);

$output = qq~
 <tr bgcolor="#FFFFFF">
 <td align="center">
 你好，$member：你已经退出 LB5000 邮件列表了。
 <br>如果你想重新加入，请联系 <a href="mailto:$adminemail_out">坛主</a> 。
 </td>
 </tr>
~;
&displayoutput;

} else {

$output = qq~
 <tr bgcolor="#FFFFFF">
 <td align="center">
 对不起，你的 Cookie 不匹配。<br>如果你想退出此邮件列表，那么必须首先登陆论坛。
 <br><a href="$boardurl/$loginprog">按此登陆后重试</a>
 </td>
 </tr>
~;
&displayoutput;
}

sub displayoutput {

print qq~
 <html>
 <head>
 <title></title>
 </head>
 <body bgcolor="#FFFFFF">
 <table border="0" align="center" width="456">
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333 size=3><b>欢迎使用 LB5000 邮件列表</td>
 </tr>
 $output
 </table>
 </body>
 </html>~;
exit;
}
