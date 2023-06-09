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
require "lb.lib.pl";
$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "noregemail.cgi";

$query = new LBCGI;

$userarray     = $query -> param('userarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            
if ($action eq "process") {
    &getmember("$inmembername");
    if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

	$userarray .= "\n";
	$userarray =~ s/\t//isg;
	$userarray =~ s/\r\n/\n/ig;
	$userarray =~ s/\n+/\n/ig;
	$userarray =~ s/\n/\t/isg;

        @saveduserarray = split(/\t/,$userarray);
        
        $filetomake = "$lbdir" . "data/banemaillist.cgi";
        open (FILE, ">$filetomake");
        print FILE $userarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                
		print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><center><b>所有的信息已经保存</b></center><br><br>
                <b>你已经保留了下列 email，使用这些 Email 将不允许被申请。</b><br><br>
                );
                
                foreach $user(@saveduserarray) {
                    chomp $user;
                    print qq($user<br>);
                }
                print qq(<br><br><br><center><a href="noregemail.cgi">保留更多的特殊 Email</a></center>);
	}
        else {
		print qq(
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF align=center colspan=2>
                    <font color=#333333><b>所有的信息没有保存</b><br>有文件或目录为不可写，请设置属性 777 ！
                    </td></tr></table></td></tr></table>
                );
	}
    }
    else {
        &adminlogin;
    }

}
else {
        
        &getmember("$inmembername");
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
		$badusers = "";
                $filetoopen = "$lbdir" . "data/banemaillist.cgi";
                open (FILE, "$filetoopen");
                $badusers = <FILE>;
                close (FILE);
                
                $badusers =~ s/\t/\n/g;

                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 保留特殊 Email</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>保留一些特殊 Email</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#000000>
                <b>请注意：</b> 此功能是用来保留一些特殊的 email 不允许在注册时使用，这样可以阻止一些捣乱的人重复用一个 Email 来注册。<BR><BR>输入的时候，每行输入一个保留的 Email 即可。<BR><BR>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF align=center colspan=2>
                <textarea cols=60 rows=10 wrap="virtual" name="userarray">$badusers</textarea><BR><BR>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <input type=submit name=submit value="提 交"></td></form></tr></table></td></tr></table>
                );
                
	}
	else {
	    &adminlogin;
	}
}
print qq~</td></tr></table></body></html>~;
exit;
