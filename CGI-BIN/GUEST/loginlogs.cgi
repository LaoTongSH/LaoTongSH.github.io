#!/usr/bin/perl
#------------------------------------------------------#
#                                                      #
#              本程序为 中国CGI之家 提供	           #
#              Ajie的留言板多用户版V4.0                #
#------------------------------------------------------#
&mypath;
require "$mypath/"."info/setup.cgi";
require "$mypath/"."info/style.cgi";
require "$mypath/"."sub.cgi";
&parseadminform;
@cookies = split(/; /,$ENV{HTTP_COOKIE});
foreach (@cookies){
($name,$value) = split(/=/,$_);
$cookie{$name} = $value;}
$inmembername = $cookie{adminname};
$inpassword = $cookie{adminpass};
$action=$FORM{'action'};
&header;
&admintitle;
if(($inmembername ne $admin)||($inpassword ne $password))
{
   &adminlogin;
}
elsif  ($action eq "dellogs") {&dellogs;exit;}
elsif  (-e "$mypath/info/log.cgi") {&dislogs;exit;}
else {
print qq(
<tr><td bgcolor="#73BAB4"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center>
                <font face=宋体 color=#336666><b>留言本安全操作日志</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<tr align="center"><td><br><br><br>暂时没有记录操作日志</td></tr></table>
);}
#####################################
sub dellogs{
$fileopen="$mypath/" . "info/log.cgi";
           unlink $fileopen;
print qq(
<tr><td bgcolor="#73BAB4"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center>
                <font face=宋体 color=#336666><b>文件删除操作日志</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<tr bgcolor="#DCECEA" align="center"><td>安全日志已经删除!</td></tr></table>
);exit;
}
sub dislogs{
$fileopen="$mypath/" . "info/log.cgi";
open (FILE, "$fileopen");
@baddel = <FILE>;
close (FILE);
print qq(
<tr><td bgcolor="#73BAB4" colspan="4"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="4">
                <font face=宋体 color=#336666><b>留言本安全操作日志</b></font>
                </td></tr>
                <tr bgcolor=#ECF6F5>
<tr><td>操作者</td><td>密码</td><td>IP 地址</td><td>操作时间</td></tr>);
		foreach (@baddel){
		(my $name, my $pass, my $ip,my $time) = split(/\t/,$_);
		print qq~
		<tr><td>$name</td><td>$pass</td><td>$ip</td><td>$time</td></tr>
		~;
                        }
print qq~<tr>
<td bgcolor="#DCECEA" align="center" colspan="4">
<b><a href=loginlogs.cgi?action=dellogs>删除安全日志</a></b></td></tr></table>
~;exit;
}
sub mypath{
local
$temp;
$temp=__FILE__;
$temp=~ s/\\/\//g if ($temp=~/\\/);
if ($temp) {$mypath=substr($temp,0,rindex($temp,"/"));}
else {
$mypath=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
$mypath=~ s/\\/\//g;
}
return
$mypath;
}