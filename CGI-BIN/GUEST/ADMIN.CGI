#!/usr/bin/perl
#------------------------------------------------------#
# laotong/asd168                                                     #
#              本程序为 中国CGI之家 提供	           #
#              Ajie的留言板多用户版V3.01               #
#------------------------------------------------------#
&mypath;
require "$mypath/"."info/setup.cgi";
require "$mypath/"."sub.cgi";
&parseadminform;
$action       = $FORM{'action'};
$inmembername = $FORM{'adminname'};
$inpassword   = $FORM{'adminpass'};
($sec,$min,$hour,$mday,$mon,$year)=localtime(time);
$mon           = $mon+1;
$year          = $year+1900;


if ($action eq "login") {
    print "Set-Cookie: adminname=$inmembername\n";
    print "Set-Cookie: adminpass=$inpassword\n";
}
else {
@cookies = split(/; /,$ENV{HTTP_COOKIE});
foreach (@cookies){
($name,$value) = split(/=/,$_);
$cookie{$name} = $value;}
$inmembername = $cookie{adminname};
$inpassword = $cookie{adminpass};
}
#############

$fileopen="$mypath/install.cgi";
unlink "$fileopen";
$fileopen="$mypath/install.cgi";
if(-e "$fileopen"){&header;
print qq(<FONT COLOR=#ff0000><B>安全警告</B>：<br>install.cgi 文件仍然在您的服务器上，请马上利用 FTP 工具将其删除！！<br> 当你删除之后，刷新本页面重新进入管理中心。</FONT>);exit;}
&header;
&admintitle;
if(($inmembername ne $admin)||($inpassword ne $password))
{  if(($inmembername ne "")||($inpassword ne ""))
     {&adminloginlogs;}
   &adminlogin;
}
elsif ($action eq "supervision"){&supervision;exit;}
elsif ($action eq "deluser"){&deluser;exit;}
elsif ($action eq "register"){&register;exit;}
elsif ($action eq "adduser"){&adduser;exit;}
else  {&loginok;}
#######################################
sub loginok{
$current_time = localtime;
dbmopen (%USER,"$userpath/alluser.db",0666);
@userno=keys %USER;
@userno=sort @userno;
$totalrecode = $#userno+1;
$testcookie = $ENV{HTTP_COOKIE};
if ($testcookie) {$cookie_result = qq(Cookies 是否可用? <font color=#336666>== [通过]</font>);}
else {$cookie_result = qq(Cookies 是否可用? <font color=#336666>== [失败]</font>);}
print qq(
<tr><td bgcolor="#73BAB4"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center>
                <font face=宋体 color=#336666><b>欢迎 $admin</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>

                <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left>
                <font face=宋体 color=#336666>
                <center><br>
                服务器时间：<b>$current_time</b><br>
                </center>
                <hr color=#DCECEA>
                 <font color=#336666 face=宋体>
                  <p> <b>留言本数据摘要</b><br>
                    <br>
                    <br>
                    注册留言本数：$totalrecode 个 <br>
                    <br><br><br>
                    主机域名&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;：<font color=red>$ENV{'HTTP_HOST'}</font><br>
                    主机IP地址&nbsp;&nbsp;&nbsp;&nbsp;：<font color=red>$ENV{'SERVER_ADDR'}</font><br>
                    目录路径&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;：<font color=#FF0000>$cgiabs</font> == [正确] <br>
                    Perl&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;版本：<font color=#FF0000>$]</font> == [通过] <br>
                    Cookie &nbsp;&nbsp;&nbsp;测试：<font color=#FF0000>$cookie_result</font><br>
                    服务器操作系统：<font color=red>$^O</font>
                    <br>
                    <br>
                  <hr color=#DCECEA>
                  <font color=#336666 face=宋体>程序制作：<a href="mailto:webmaster\@homecgi.com">Ajie</a><br>
                  版权所有：<a href="http://www.homecgi.com">中国CGI之家</a></font> </font>
                  </font>
                </td></tr></table></td></tr></table>
                );
}
#######################################
sub supervision
{
dbmopen (%USER,"$userpath/alluser.db",0666);
@userno=keys %USER;
@userno=sort @userno;
$totalrecode = $#userno+1;
print <<HTML;
<tr><td bgcolor="#73BAB4" colspan="8"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#ECF6F5 align=center colspan="8">
                <font face=宋体 color=#336666><b>注册留言本管理</b></font>（现有申请用户<b><font face=宋体 color=#ff0000>$totalrecode</font></b>个）
                </td></tr>
                <tr><td bgcolor=#ECF6F5 colspan="8">
                </td>
                </tr><tr>
<form method="POST" action="$cgiurl/admin.cgi">
<tr bgcolor="#DCECEA" align="center">
<td width="1%" height="1" align="center">
<input type=hidden name="action" value="deluser"></td>
<td width="15%" height="1" align="center">留言本名</td>
<td width="5%" height="1" align="center">用户</td>
<td width="5%" height="1" align="center">密码</td>
<td width="25%" height="1" align="center">网站地址</td>
<td width="12%" height="1" align="center">申请时间</td>
<td width="15%" height="1" align="center">使用IP地址</td>
<td width="10%" height="1" align="center">留言数</td>
</tr>
HTML
$inti=0;
foreach (@userno)
  {
   ($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/‖/,$USER{$_});
   $tmpurl=$url;
   if (length($tmpurl) > 25)
     {
      $tmpurl = substr($tmpurl,0,25);
      $tmpurl = "$tmpurl...";
     }
   &showuser;
   $inti++;
  }
dbmclose(%USER);
print <<HTML;
<tr bgcolor="#DCECEA" align="center"><td colspan="8"><input type="submit" value="删 除" name="B1"></td></tr></form></table>
HTML
exit;
}
#############
sub showuser
{
 dbmopen(%TEMP,"$datapath/$name.db",0666);
 @tempuserno=keys %TEMP;
 @tempuserno=sort @tempuserno;
 $temptotal=$#tempuserno+1;
 dbmclose(%TEMP);
 $temp=$inti+1;
 print <<HTML;
<tr align="center" bgcolor="#ECF6F5">
<td width="29" align="center" valign="middle">
<p align="center"><input type="checkbox" name="reco$temp"
value="$userno[$inti]"></p></td>
<td width="145" align="center" valign="middle">
<a href="$cgiurl/gbook.cgi?user=$name" target = _blank>$title</a></td>
<td width="52" align="center" valign="middle"><a href=mailto:$email>$name</a></td>
<td width="49" align="center" valign="middle">$pass</td>
<td width="172" align="center" valign="middle"><a
href="$url" target = _blank>$tmpurl</a></td>
<td width="79" align="center" valign="middle">$date_time</td>
<td width="87" align="center" valign="middle">$ipaddress</td>
<td width="77" align="center" valign="middle">$temptotal</td>
</tr>
HTML
}
#############
sub register{
print qq(
<tr><td bgcolor="#73BAB4" colspan="2"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=宋体 color=#336666><b>注册新的留言本</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<form method="post" action="$cgiurl/admin.cgi">
<input type=hidden name="action" value="adduser">
<tr bgColor=ECF6F5><td align=right width=25%>用 户 名：</td><td width=75%><input type="text" name="username" size="20" maxlength=8 value=$admin>* 1-8位（版主用户名）</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>用户密码：</td><td width=75%><input type="text" name="userpass" size=20 value="$password">* 版主密码</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>重复密码：</td><td width=75%><input type="text" name="userpass1" size="20">* 版主密码</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>电子邮件：</td><td width=75%><input type="text" name="emailaddress" size="20" value="$adminmail">* 邮件地址（邮件通知）</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>主页地址：</td><td width=75%><input type="text" name="homepage" value = "http://" size="20">* 主页地址</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>留言本名：</td><td width=75%><input type="text" name="title" size="20" value="$home留言本">* 你的留言本的名字</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>每页记录：</td><td width=75%><input type="text" name="recode" size="20" value="$pagenum" maxlength="2">* 默认为$pagenum条</td></tr>
<tr><td width="100%" bgcolor=#DCECEA align="center" colspan="2">
<input type="submit" value="提交申请" name=ok>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td></tr></FORM>
</table></td></tr></table>
);
exit;}
############################################
sub adduser {
if($FORM{'username'} eq ""){&errorview("用户名不能没有填写!");}
if($FORM{'username'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorview("名字中不能含有特殊字符!");}
if($FORM{'userpass'} eq ""){&errorview("用户密码不能没有填写!");}
if($FORM{'userpass'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorview("密码中不能含有特殊字符!");}
if($FORM{'userpass'} ne "$FORM{'userpass1'}"){&errorview("两次输入的密码不相同!");}
if (($FORM{'userpass'} eq "") || ($FORM{'userpass1'} eq ""))
{&errorview("密码或确认密码不能为空, 请重新输入!!");}
if (!($FORM{'emailaddress'} =~ /.*\@.*\..*/)){&errorview("你输入了一个错误的电子邮件地址！！！");}
dbmopen(%USERFILE,"$userpath/alluser.db",0666);
foreach (%USERFILE)
{if ($_ =~ "‖$FORM{'username'}‖")
{&errorview("此用户已被注册!!请更换用户名!!");}
if ($_ =~ "‖$FORM{'homepage'}‖"){&errorview("此主页已经注册过本留言本!!不能完成您的申请!");}
if ($_ =~ "‖$FORM{'emailaddress'}‖"){&errorview("此信箱已经注册过本留言本!!不能完成您的申请!!");}}
($sec,$min,$hour,$mday,$mon,$year)=localtime(time);
$mon           = $mon+1;
$year          = $year+1900;
$date_time  = sprintf ("%04d/%02d/%02d",$year,$mon,$mday);
$name   = $FORM{'username'};
	    $name =~ s/\&nbsp\;//ig;
	    $name =~ s/　/ /g;
	    $name =~ s// /g;
	    $name =~ s/[ ]+/ /g;
	    $name =~ s/\s*$//g;
	    $name =~ s/^\s*//g;
	    $name =~ s/ *$//g;
	    $name =~ s/^ *//g;
	    $name =~ s/[ ]+/ /;
	    $name =~ s/[ ]+/ /;
	    $name =~ s/�//isg;
	    $name =~ s///isg;
	    $name =~ s/()+//isg;
        $name =~ tr/A-Z/a-z/;
	    $name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\=\+\\\[\]\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$pass   = $FORM{'userpass'};
$email   = $FORM{'emailaddress'};
$url   = $FORM{'homepage'};
$title   = $FORM{'title'};
$pagenum   = $FORM{'recode'};
$newuserno  = sprintf ("%04d%02d%02d%02d%02d%02d",$year,$mon,$mday,$hour,$min,$sec);
$ipaddress  = $ENV{'REMOTE_ADDR'};
dbmopen(%USERFILE,"$userpath/alluser.db",0666);
$USERFILE{$newuserno} = "start‖$name‖$pass‖$email‖$url‖$title‖$pagenum‖$ipaddress‖$date_time‖end‖\n";
dbmclose(%USERFILE);
print qq(
<tr><td bgcolor="#73BAB4" colspan="2"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=宋体 color=#336666><b>注册成功</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<tr bgColor=ECF6F5>
<td align=center width=100%><br><br><a href=gbook.cgi?user=$name>进入您的留言本</a><br></td></tr>
</table></td></tr></table>
);
exit;
}
###############################
sub deluser
  {
       dbmopen(%USERLIST,"$userpath/alluser.db",0666);
       @userno=keys %USERLIST;
       @userno=sort @userno;
       $totalrecode = $#userno+1;

       for ($inti = $totalrecode-1;$inti >= 0;$inti--)
         {
          $tempint=$inti+1;
          $tempnum = "reco$tempint";
          $tempno=$FORM{$tempnum};
          if ($tempno ne "")
            {
             foreach (@userno)
               {
               	if ($tempno eq $_)
                  {

                   ($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/‖/,$USERLIST{$tempno});
                   delete $USERLIST{$tempno};
                   unlink (<"$datapath/$name.*">);
                  }
               }
            }
         }
       dbmclose(%USERLIST);
print qq(
<tr><td bgcolor="#73BAB4" colspan="8"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b>
                </td></tr>
<tr bgcolor="#DCECEA" align="center"><td><br>删除成功……</td></tr></table>
);
}
############################################################
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
sub errorview {
print qq(
    <tr><td bgcolor="#73BAB4" colspan="2"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=宋体 color=#336666><b>¤ 出 错 提 示</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5 colspan="2">
                </td>
                </tr>
<tr><td align=center>
<FONT size=7 face=Wingdings color=#ff0000>L</FONT><P><font size=2>$_[0]</font></P></td></tr>
<tr><td colSpan=2 width=100%><div align=center><center>
<table border=1 bgColor=cccccc cellspacing=0><tr><td width=100% align=center bordercolordark=#E6E6E6 bordercolorlight=#cccccc><A href=javascript:history.back()><font size=2 color=#000000>　确 定&nbsp;&nbsp;</font></A>
</td></tr></table></center></div></TD></TR></TBODY></TABLE>
</TD></TR></table></td></tr></table>);exit;}
sub adminloginlogs{
&getdate;
&gettime;
$ip=$ENV{'REMOTE_ADDR'};
$fileopen="$mypath" . "/info/log.cgi";
open(LOG,">>$fileopen");
print LOG "$inmembername\t$inpassword\t$ip\t$date $time\n";
close(LOG);
}
