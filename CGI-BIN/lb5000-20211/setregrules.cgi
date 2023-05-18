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
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "lb.lib.pl";
$|++;

#################--- Begin the program ---###################

$thisprog = "setregrules.cgi";

$query = new LBCGI;


$rules        = $query -> param('therules');
$action       = $query -> param("action");
$action       = &cleaninput("$action");


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {
        
        $rules =~ s/\n\n/\n/ig;
        $rules =~ s/\s+/\n/ig;

        $filetomake = "$lbdir" . "data/register.dat";
        open (FILE, ">$filetomake");
        print FILE $rules;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font color=#333333><center><b>所有信息已经保存</b></center><br><br>
                <b>注册条款和声明已经保存.目前的注册条款和声明如下：</b><br><HR><ul>$rules</ul>
                <HR><br><br><br><center><a href="setregrules.cgi">修改注册条款和声明</a></center>);
                }
                else {
                    print qq(
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                    <font color=#333333><b>信息无法保存</b><br>文件或者目录不可写。
                    </td></tr></table></td></tr></table>
                    );
                    }
                }
        
    else {
        &getmember("$inmembername");
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "/data/register.dat";
                open (FILE, "$filetoopen") or $rules = "输入注册条款和声明";
                @rules = <FILE> if (!$rules);
                close (FILE);

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 注册条款和声明设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font color=#333333><b>输入注册条款和声明</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <br>
                <b>注意:</b>　可以使用 HTML ，但不能使用 LB5000 标签。<br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=70 rows=15 wrap="virtual" name="therules">);
		                foreach (@rules) {
		                   $rules = $_;
		                   #$rules =~ s/\n//isg;
		                   print qq($rules);
		                }
		                print qq(</textarea>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit name=submit value=提交></form></td></tr></table></td></tr></table>
                );
                
                }
                else {
                    &adminlogin;
                    }
        }

print qq~</td></tr></table></body></html>~;
exit;
