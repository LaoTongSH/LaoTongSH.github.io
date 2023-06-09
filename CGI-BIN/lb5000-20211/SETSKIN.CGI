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
require "lbadmin.lib.pl";     # Require Admin func()
require "data/progs.cgi";    # Require prog names
require "data/boardinfo.cgi";# Require board info
require "data/leoskin.cgi";
require "lb.lib.pl";          # Require lbboard ()

$|++;                                      # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "setskin.cgi";


$query = new LBCGI;



	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \"$theparam\"\;\n";
            }
	}


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");

print header(-charset=>gb2312);
&admintitle;

&getmember("$inmembername");
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
             
    if ($action eq "process") {


        $printme .= "1\;\n";

        $filetomake = "$lbdir" . "data/leoskin.cgi";

        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        close(FILE);
        
         
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=宋体  color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 论坛插件设定</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=宋体 color=#333333 ><center><b>所有的信息已经保存</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/1\;//g;
                print $printme;

                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }

                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=宋体  color=#FFFFFF>
                    <b>欢迎来到 LB5000 论坛管理中心</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font color=#333333><b>所有的信息没有保存</b><br>有文件或目录为不可写，请设置属性 777 ！
                    </td></tr></table></td></tr></table>
                    ~;
                    }
        
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                               print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=宋体  color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 论坛插件设定</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333 ><b>论坛插件设定</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
            
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000 ><b><center>LB5000 论坛管理中心论坛插件设定</center></b><br>
                <font face=宋体 color=#333333 >你可以增加和删除管理中心的论坛插件，方便论坛升级！
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 1 </a></b><br>论坛插件 1 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin1name" value="$skin1name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 1 URL</b><br>论坛插件1的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin1url" value="$skin1url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 2 </a></b><br>论坛插件 2 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin2name" value="$skin2name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 2 URL</b><br>论坛插件2的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin2url" value="$skin2url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 3 </a></b><br>论坛插件 3 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin3name" value="$skin3name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 3 URL</b><br>论坛插件3的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin3url" value="$skin3url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 4 </a></b><br>论坛插件 4 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin4name" value="$skin4name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 4 URL</b><br>论坛插件4的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin4url" value="$skin4url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 5 </a></b><br>论坛插件 5 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin5name" value="$skin5name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 5 URL</b><br>论坛插件5的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin5url" value="$skin5url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 6 </a></b><br>论坛插件 6 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin6name" value="$skin6name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 6 URL</b><br>论坛插件6的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin6url" value="$skin6url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 7 </a></b><br>论坛插件 7 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin7name" value="$skin7name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 7 URL</b><br>论坛插件7的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin7url" value="$skin7url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 8 </a></b><br>论坛插件 8 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin8name" value="$skin8name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 8 URL</b><br>论坛插件8的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin8url" value="$skin8url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 9 </a></b><br>论坛插件 9 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin9name" value="$skin9name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 9 URL</b><br>论坛插件9的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin9url" value="$skin9url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#AD0000 ><b>论坛插件 10 </a></b><br>论坛插件 10 的名称</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin10name" value="$skin10name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛插件 10 URL</b><br>论坛插件10的连接</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin10url" value="$skin10url"></td>
                </tr>      
                               
               <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="提交"></form></td></tr></table></td></tr></table>
               
               ~;

                            
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;

