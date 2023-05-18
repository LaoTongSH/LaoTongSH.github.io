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
$thisprog = "setipbans.cgi";

$query = new LBCGI;

#$cookiepath = $query->url(-absolute=>1);
#$cookiepath =~ s/$thisprog//sg;

$boardurltemp =$boardurl;

$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/$thisprog//sg;

$wordarray     = $query -> param('wordarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {
        
        &getmember("$inmembername");
        
                if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 

        $wordarray =~ s/\s+/\n/ig;
        $wordarray =~ s/\n\n/\n/ig;

        $wordarray2display = $wordarray;
        $wordarray2display =~ s/\n/<br>/g;

        $filetomake = "$lbdir" . "data/ipbans.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / IP 禁止</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#333333><center><b>所有的信息已经保存</b></center><br><br>
		<b>你已经禁止了下列 IP</b><br><br>
		);
                    print qq(<b>$wordarray2display</b><br>);
                print qq(
                <br><br><br><center><a href="setipbans.cgi">再次增加一些禁止的 IP</a></center>);
                }
                else {
                    print qq(
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
			<b>欢迎来到 LB5000 论坛管理中心</b>
			</td></tr>
			<tr>
			<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
			<font color=#333333><b>所有的信息没有保存</b><br>有文件或目录为不可写，请设置属性 777 ！
                    	</td></tr></table></td></tr></table>
		     	);
                    }
                }
        }
        
    else {
        
        &getmember("$inmembername");
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "data/ipbans.cgi";
                open (FILE, "$filetoopen");
                @bannedips = <FILE>;
                close (FILE);
                
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / IP 禁止</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>IP 禁止列表</b>
		</td></tr>
		<form action="$thisprog" method="post">
		<input type=hidden name="action" value="process">
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#000000>
		<b>请注意:</b>如果你禁止了一个 IP 的话，那么这个 IP 将只能查看论坛的贴子而无法发言回复！<br>
		<br>
		<b>说明:</b><BR>
		             你如果要禁止一个 IP，可以直接输入 IP 地址在这里，比如： 202.100.200.100。<BR>
		             如果你要禁止一个 C 类网，那么你可以不输入 IP 的最后一位，比如：202.100.200. <BR>
		             如果你要禁止一个 B 类网，那么你可以不输入 IP 的最后两位，比如：202.100. <BR>
		             注意上面的写法，如果禁止的是一个 C 类或者 B 类网，请最后保留点号(.)，切记！<BR>
		             每行写一个 IP，注意最后回车！<BR>
	                </font></td>
		</tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
		<textarea cols=60 rows=6  name="wordarray">);
		                foreach (@bannedips) {
		                   $singleip = $_;
		                   chomp $_;
		                   next if ($_ eq "");
		                   #$singleip =~ s/\n\s/\n/g;
		                   print qq($singleip);
		                }
		                print qq(</textarea><BR>
		</td>
		</tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<input type=submit name=submit value=提交></td></form></tr></table></td></tr></table>
);
                
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
