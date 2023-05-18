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
require "data/styles.cgi";   # Require styles info
require "data/cityinfo.cgi";
require "lb.lib.pl";          # Require lbboard ()

$|++;                                      # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "vercheck.cgi";


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
	$server_port = ":$ENV{'SERVER_PORT'}" if ($ENV{'SERVER_PORT'} ne '80');
	$fullurl     = "http://$ENV{'SERVER_NAME'}$server_port$ENV{'SCRIPT_NAME'}";
	$myurl       = substr($fullurl,0,rindex($fullurl,"/"));
        $geturl="http://www.leoboard.com/cgi-bin/lbver.cgi?ver=$versionnumber&url=$myurl";
        
	$out=&lbagent($geturl);
        
        ($lastver,  $finish, $downtime, $nowver, $hasfunc, $gb, $big5, $download) = split(/§/,$out);
        (my $tmp,$lastver) = split(/\|/,$lastver);
             
        
       if ($lastver ne "") {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=宋体  color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 查看论坛版本更新</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2><br>
               ~;
                
                if ($versionnumber =~/LB5000/g){
                $myver=$versionnumber;
                $myver=~s /LB5000II v//isg;
                $myver=~s /LB5000 II v//isg;
                $newver=$nowver;
                $newver=~s /LB5000II v//isg;
                $newver=~s /LB5000 II v//isg;
                
                my $gengxin="";
                if ($myver >= $newver){
                print qq~
                <font face=宋体 color=#333333 ><center><b>您现在使用的是最新版本，感谢你使用我们的论坛 ！</b><br><br>
                ~;
                $gengxin="无需升级";
                }else{
               print qq~
                <font face=宋体 color=#333333 ><center><b>$myver >= $newver当前$nowver已经提供下载，如果你需要升级，请参看下面的连接 ！</b><br><br>
                ~;
                $gengxin="需要升级";
               }
               print qq~
               <table><tr><td>当前最新版本:$lastver  [ 你当前使用版本:$versionnumber <font color=red>$gengxin</font>]<br><hr>
               <br>
               <font color=blue>已完成功能:</font><br><br>
               $finish <br>
               估计提供下载时间:$downtime <br>
               <hr>
               </td></tr>
               <tr><td>当前可提供下载的最新版本:$nowver <br><hr>
               <br>
               <font color=red>功能列表:</font><br><br>
               $hasfunc <br>
               下载地址:<br>
                [GB版本]<a href=$gb>$gb</a> <br>
                [BIG5版本]<a href=$big5>$big5</a><br>
               <hr><br>
               <b>自2001年5月15日以来，至少<b><font color=blue>$download</font></b>人安装过本论坛！</b>
               <hr>
               </td></tr></table>
               ~;
               }else{
               print qq~
                <font face=宋体 color=#333333 ><center><b>你非法修改版本号，请及时改回连接和版本标示，谢谢合作！</b><br><br>
                ~;
               }
               

                print qq~
                </center>
                </td></tr></table></td></tr></table>
                ~;
                }

                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=宋体  color=#FFFFFF>
                    <b>欢迎来到 LB5000 论坛管理中心/查看论坛版本更新</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font color=#333333><b>没有版本信息</b><br>估计Socket模块不能正常使用，或者Leoboard服务器调整，请访问http://www.leoboard.com查看更新情况吧 ！
                    </td></tr></table></td></tr></table>
                    ~;
                    }
        
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                               print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=宋体  color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 论坛版本检查</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333 ><b>论坛版本检查</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                
                <font face=宋体 color=#990000 ><b><center>LB5000 论坛管理中心 / 论坛版本检查</center></b><br>
                <font face=宋体 color=#333333 >你可以查看当前Leoboard站点论坛的版本情况，<br>知道当前最新版本和是否增加了有用的功能，是否适合你升级！<br><br>
                本程序没有危害性，而且我们特意没有采用加密方式传送，<br>仅仅是为了让大家获得最新版本的情况，谢谢你采用雷傲论坛！
                
                </td>
                </tr>
                              
               <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="检查版本更新情况"></form></td></tr></table></td></tr></table>
               
               ~;

                            
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;

