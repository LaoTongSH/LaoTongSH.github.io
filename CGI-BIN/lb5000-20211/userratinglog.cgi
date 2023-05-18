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
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "userratinglog.cgi";

$query = new LBCGI;


$boardurltemp =$boardurl;

$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/$thisprog//sg;

$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {
        
        &getmember("$inmembername");
        
                if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
           $filetoopen = "$lbdir" . "data/userratinglog.cgi";
           unlink $filetoopen;
           print qq~
           <tr><td bgcolor=#333333"><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 删除用户威望操作日志</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center>
		<font color=#333333><b>文件删除操作日志</b>
		</td></tr>
		<tr><td align=center><br><br>用户威望操作日志已经删除!</td></tr>
           ~;
         
                }
        
        }
        
    else {
        
        &getmember("$inmembername");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "data/userratinglog.cgi";
                open (FILE, "$filetoopen");
                @baddel = <FILE>;
                close (FILE);
                
                print qq(
                <tr><td bgcolor=#333333" colspan=9><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 用户威望操作日志</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=9>
		<font color=#333333><b>用户威望操作日志</b>
		</td></tr>
		<tr><td>对象</td><td>威望值</td><td>操作者</td><td>相应贴子</td><td>IP 地址</td><td>代理 IP</td><td>操作时间</td></tr>
		);
		foreach (@baddel){
		(my $name1, my $name2,my $rate, my $oldtime,my $forum1,my $topic1, my $ip, my $proxy) = split(/\t/,$_);
    		$oldtime = $oldtime + ($timedifferencevalue*3600) + ($timezone*3600);
    		$oldtime = &dateformatshort($oldtime);
		print qq~
		<tr><td>$name1</td><td>$rate</td><td>$name2</td><td><a href=topic.cgi?forum=$forum1&topic=$topic1 target=_blank>进入</a></td><td>$ip</td><td>$proxy</td><td>$oldtime</td></tr>
		~;
		}
                print qq~
                <tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=9><br>
		<font color=#333333><b><a href=$thisprog?action=process>删除用户威望操作日志</a></b>
		</td></tr>
                ~;
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
