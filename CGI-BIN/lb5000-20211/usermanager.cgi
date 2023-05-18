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
require "lbmail.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                                   # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "usermanager.cgi";
$query = new LBCGI;

$action          = $query -> param('action');
$usertype        = $query -> param('usertype');
$action          = &unHTML("$action");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);       
&admintitle;
        
&getmember("$inmembername");
        
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 用户分类管理</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'search' =>    \&searchusers,
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &searchoptions; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        
sub searchoptions {

    print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
	由于 <font color=red>一般用户</font> 数目较多，请到 <a href="$setmembersprog">用户管理/排名(*)</a> 搜索。<br><br>
        <form method=get action="usermanager.cgi">
        <input type=hidden name="action" value="search">
        <div align=center>请选择需要查询的用户类型
	<select name="usertype">
	<option value="rz" selected>认证用户</option>
	<option value="mo">分论坛版主</option>
        <option value="smo">论坛总版主</option>
	<option value="ad">坛主</option>
        <option value="banned">禁止用户发言</option>
        <option value="masked">屏蔽此用户帖子</option>
	</select> 
        <p><input type="submit" value='确定'></p></div></form>
	</td></tr>
        ~;
        }

sub searchusers {
	unless ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
        }

        if ($usertype eq ""){
	print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>没有选择需要搜索的用户类别</font>
                    
        </td></tr>
         ~;
         }
         else {
	print qq~
        <tr>
        <td bgcolor=#FFFFFF colspan=2><br>
         ~;

	$filetoopen = "$lbdir" . "data/lbmember.cgi";
        open(FILE,"$filetoopen");
        flock (FILE, 1) if ($OS_USED eq "Unix");
        @memberfiles = <FILE>;
        close(FILE);
	$i=0;
        foreach $memtypedata (@memberfiles) {
	chomp $memtypedata;
        ($username, $membertype) = split(/\t/,$memtypedata);

       if ($membertype eq $usertype) {
       print qq~
       <a href="setmembers.cgi?action=edit&member=$username">$username</a><br><br>~;
       $i++;
       }
    }
       print qq~
       <br><br>
       <b>共找到 $i 位用户</b><br>
       </td></tr>
       ~;
       }
     }

print qq~</td></tr></table></body></html>~;
exit;
