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
require "data/cityinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setcity.cgi";

$query = new LBCGI;

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam =~ s/'//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \'$theparam\'\;\n";
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);
&admintitle;

&getmember("$inmembername");
        
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

    
    if ($action eq "process") {

        
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/cityinfo.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 变量结构</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>以下信息已经成功保存</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 变量设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=宋体 color=#333333><b>所有信息没有保存</b><br>文件或者目录不可写<br>请检测你的 data 目录和 cityinfo.cgi 文件的属性！
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                $moneyname ="雷傲元" if ($moneyname eq "");
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 社区设置</b>
                </td></tr>
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                我们添加社区货币的制度，现在还没有什么用处。但在以后向社区发展的过程中会用到。
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>社区货币设置</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>货币名称符号</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="moneyname" value="$moneyname" maxlength=6> 默认：雷傲元</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每推荐一个人增加的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjhb" value="$addtjhb"> 默认：100</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每推荐一个人增加的经验</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjjy" value="$addtjjy"> 默认：0</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每推荐一个人增加的魅力</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjml" value="$addtjml"> 默认：10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每发一个主题折算的经验数</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="ttojy" value="$ttojy"> 默认：6</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每发一个回复折算的经验数</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="rtojy" value="$rtojy"> 默认：6</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每登陆一次折算的经验数</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="ltojy" value="$ltojy"> 默认：2</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>被删除一个贴子减去的经验</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="deljingyan" value="$deljingyan"> 默认：10</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>新用户注册分配的经验</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinjingyan" value="$joinjingyan"> 默认：100</td>
                </tr>  
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次发帖增加的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addmoney" value="$addmoney"> 默认：10</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次回复增加的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="replymoney" value="$replymoney"> 默认：8</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次登陆增加的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="loginmoney" value="$loginmoney"> 默认：15</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次被删除贴子减去的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="delmoney" value="$delmoney"> 默认：20</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>新用户注册分配的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinmoney" value="$joinmoney"> 默认：1000</td>
                </tr> 
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次发帖增加的魅力</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addml" value="$addml"> 默认：8</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次回复增加的魅力</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="replyml" value="$replyml"> 默认：5</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次登陆增加的魅力</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="loginml" value="$loginml"> 默认：5</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次被删除贴子减去的魅力</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="delml" value="$delml"> 默认：10</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>新用户注册分配的魅力</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinml" value="$joinml"> 默认：100</td>
                </tr>  
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
                ~;
                
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;
