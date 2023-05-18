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
&header;
######################################################
if ($FORM{'action'} eq "modify"){&modify;exit;}
if ($FORM{'action'} eq "adduser"||$FORM{'action'} eq "modifyuser"){&adduser;exit;}
if ($shenqing eq "off")
     {
      &errorinput("留言本暂停申请");
     }
&pagestyle;
print qq(
<html>
    <head>
    <title>申请留言本</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
    </head>
    <body bgcolor="$gbbgcolor" $gbbody>
);
print qq~
<form method=POST action=$cgiurl/register.cgi?action=adduser>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont>申 请 留 言 本</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">用 户 名：</td>
<td width="70%">&nbsp;
<input type="text" name="username" size="20" maxlength=8 class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 1-8位（版主用户名）
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">用户密码：</td>
<td width="70%">&nbsp;
<input type="password" name="userpass" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 版主密码
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">重复密码：</td>
<td width="70%">&nbsp;
<input type="password" name="userpass1" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 版主密码
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">电子邮件：</td>
<td width="70%">&nbsp;
<input type="text" name="emailaddress" size="20" class="input2" value="@">&nbsp;&nbsp;&nbsp; &nbsp;* 邮件地址(邮件通知）
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">主页地址：</td>
<td width="70%">&nbsp;
<input type="text" name="homepage" value = "http://" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 主页地址
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">留言本名：</td>
<td width="70%">&nbsp;
<input type="text" name="title" size="20" value="我的留言本" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 你的留言本的名字
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">每页记录：</td>
<td width="70%">&nbsp;
<input type="text" name="recode" size="20" value="$pagenum" maxlength="2" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 默认为$pagenum条
</td>
</tr>
        <tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
<input type="submit" value="提交申请" name="B1" class="input2">&nbsp;&nbsp;&nbsp;&nbsp;
			  <input type="reset"  value="重新来过" name="B2" class="input2"></div>
</td></tr></table>
</td></tr></table>
</form>
~;
sub modify{
$user=$FORM{'user'};
dbmopen (%USER,"$userpath/alluser.db",0666);
foreach (%USER){
if ($_ =~ "‖$user‖")
{
($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/‖/,$_);
dbmclose(%USER);
}}
&pagestyle;
print qq~
<html>
    <head>
    <title>修改留言本信息</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
    </head>
    <body bgcolor="$gbbgcolor" $gbbody>
<form method="POST" action="$cgiurl/register.cgi?action=modifyuser&user=$user">
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont>修改 <font color=red>$user</font> 留言本信息</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">用 户 名：</td>
<td width="70%">&nbsp;&nbsp;<font color=red>$user</font>
<input type="hidden" name="username" value="$user">
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">用户密码：</td>
<td width="70%">&nbsp;
<input type="password" name="userpass" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 版主密码
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">重复密码：</td>
<td width="70%">&nbsp;
<input type="password" name="userpass1" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 版主密码
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">电子邮件：</td>
<td width="70%">&nbsp;
<input type="text" name="emailaddress" size="20" class="input2" value="$email">&nbsp;&nbsp;&nbsp; &nbsp;* 邮件地址(邮件通知）
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">主页地址：</td>
<td width="70%">&nbsp;
<input type="text" name="homepage" value = "$url" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 主页地址
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">留言本名：</td>
<td width="70%">&nbsp;
<input type="text" name="title" size="20" value="$title" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 你的留言本的名字
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">每页记录：</td>
<td width="70%">&nbsp;
<input type="text" name="recode" size="20" value="$pagenum" maxlength="2" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 默认为$pagenum条
</td>
</tr>
        <tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
<input type="submit" value="提交申请" name="B1" class="input2">&nbsp;&nbsp;&nbsp;&nbsp;
			  <input type="reset"  value="重新来过" name="B2" class="input2"></div>
</td></tr></table>
</td></tr></table>
</form>
</table>
<table border="0" width=$tablewidth>
<tr align=middle>
<td width=100%><br>
<p align="center">免费留言本由<b><a href=$homeurl target=_blank> $home </a></b>
提供 技术支持：<b><a href=http://www.cgiubb.com target=_blank> CGI技术论坛</a></b></p>
</td>
</tr>
</table>
~;
}
print qq~
</table>
<table border="0" width=$tablewidth>
<tr align=middle>
<td width=100%><br>
<p align="center">免费留言本由<b><a href=$homeurl target=_blank> $home </a></b>
提供 技术支持：<b><a href=http://www.cgiubb.com target=_blank> CGI技术论坛</a></b></p>
</td>
</tr>
</table>
~;
#############
sub adduser
   {
    if ($FORM{show} eq "show")
       {
       	$linkurl = "$cgiurl/register.cgi";
        print "<META HTTP-EQUIV=REFRESH CONTENT=\"1;URL=$linkurl\">";
       }
    else
       {
       	if ($FORM{'action'} eq 'adduser')
       	   {
       	    $name       = &checknull($FORM{'username'}   ,"名字项不能为空!!");
            if (length($name)>8) {&errorinput("名字不能超过8个字符！");}
            if($name=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorinput("名字中不能含有特殊字符!");}
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
            if($FORM{'userpass'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorinput("密码中不能含有特殊字符!");}
       	    $email      = &checknull($FORM{'emailaddress'}  ,"电子邮件项不能为空!!");
            $title      = &checknull($FORM{'title'},"留言本名项不能为空!!");
            $url        = &checknull($FORM{'homepage'}    ,"主页地址不能为空!!");
            $pagenum    = &checknull($FORM{'recode'}  ,"每页记录数项不能为空!!");
            if (!($email =~ /.*\@.*\..*/))
              {
               &errorinput("你输入了一个错误的电子邮件地址！！！");
              }
            if (!($url   =~ /http:\/\/.*\..*/))
              {
               &errorinput("你输入了一个错误的主页地址！！！");
              }
       	    dbmopen(%USERFILE,"$userpath/alluser.db",0666);
            foreach (%USERFILE)
              {
               if ($_ =~ "‖$FORM{'username'}‖")
                  {
                   &errorinput("此用户已被注册!!请更换用户名!!");
                  }
               if ($_ =~ "‖$FORM{'homepage'}‖")
                  {
                   &errorinput("此主页已经注册过本留言本!!不能完成您的申请!!");
                  }
               if ($_ =~ "‖$FORM{'emailaddress'}‖")
                  {
                   &errorinput("此信箱已经注册过本留言本!!不能完成您的申请!!");
                  }
              }
            $date_time  = sprintf ("%04d/%02d/%02d",$year,$mon,$mday);
            if (($FORM{'userpass'} eq "") || ($FORM{'userpass1'} eq ""))
              {
               &errorinput("密码或确认密码不能为空, 请重新输入!!");
              }
            elsif ($FORM {'userpass'} ne $FORM {'userpass1'})
              {
               &errorinput("密码与确认密码不同, 请重新输入!!");
              }
            else
              {
               $pass   = $FORM{'userpass'};
              }
            $newuserno  = sprintf ("%04d%02d%02d%02d%02d%02d",$year,$mon,$mday,$hour,$min,$sec);
            $ipaddress  = $ENV{'REMOTE_ADDR'};
            dbmopen(%USERFILE,"$userpath/alluser.db",0666);
            $USERFILE{$newuserno} = "start‖$name‖$pass‖$email‖$url‖$title‖$pagenum‖$ipaddress‖$date_time‖end‖\n";
            dbmclose(%USERFILE);
           }
        else
           {
            dbmopen(%USERFILE,"$userpath/alluser.db",0666);
            @userno=keys %USERFILE;
            @userno=sort @userno;
            foreach (@userno)
              {
               ($mark,$name111,$pass111,$email111,$url111,$title111,$pagenum111,$ipaddress,$date_time,$markend,$last)=split(/‖/,$USERFILE{$_});
               if ($USERFILE{$_} =~ "$FORM{'username'}")
                 {
                  if (($name111 eq "$FORM{'username'}") && ($pass111 eq "$FORM{'userpass'}"))
                    {
                     $name       = &checknull($FORM{'username'}      ,"名字项不能为空!!");
                     $email      = &checknull($FORM{'emailaddress'}  ,"电子邮件项不能为空!!");
                     $title      = &checknull($FORM{'title'}         ,"留言本名项不能为空!!");
                     $url        = &checknull($FORM{'homepage'}      ,"主页地址不能为空!!");
                     $pagenum    = &checknull($FORM{'recode'}        ,"每页记录数项不能为空!!");
                     if ($FORM{'userpass1'} eq "")
                        {
                         $pass = $FORM{'userpass'};
                        }
                     else
                        {
                         $pass = $FORM{'userpass1'};
                        }
                     $USERFILE{$_} = "start‖$name‖$pass‖$email‖$url‖$title‖$pagenum‖$ipaddress‖$date_time‖end‖\n";
                    }
                 else
                    {
                     &errorinput("你的密码不对, 不能完成修改!!");
                    }
                }
              }
            dbmclose(%USERFILE);
           }
&pagestyle;
print <<PRINTHTML;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>申请成功</title></head>
<BODY bgcolor=$gbbgcolor $gbbody><center>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont>恭喜 <font color="#ff0000">$name</font> ，你已成功申请(修改)了您的留言板！</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">用 户 名：</td>
<td width="70%">&nbsp;$name</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">用户密码：</td>
<td width="70%">&nbsp;为了您的安全，不显示您的留言本密码！</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">留言本名：</td>
<td width="70%">&nbsp;$title</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">每页记录：</td>
<td width="70%">&nbsp;$pagenum</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">信箱地址：</td>
<td width="70%">&nbsp;$email</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">主页地址：</td>
<td width="70%">&nbsp;$url</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">查看留言：</td>
<td width="70%">&nbsp;<a href = $cgiurl/gbook.cgi?user=$name>$cgiurl/gbook.cgi?user=$name</a></td>
</tr>
<tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
<font color=$btfont>您的代码已经通过<a href = mailto:$email><font color="#ff0000"> $email </font></a>发到了你的信箱中。</font></div>
</td></tr></table>
</td></tr></table>

PRINTHTML
&sendmail()
       }
}
######################################################
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