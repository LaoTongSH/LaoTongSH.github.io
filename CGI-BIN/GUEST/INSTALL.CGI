#!/usr/bin/perl
#------------------------------------------------------#
#                                                      #
#              本程序为 中国CGI之家 提供	           #
#              Ajie的留言板多用户版V4.0                #
#------------------------------------------------------#
&mypath;
&myurl;
$cgiabs=$mypath;
######################
## 以下部分不需修改 ##
######################
if ($ENV{'REQUEST_METHOD'} eq "POST") {read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});}
else {$buffer = $ENV{'QUERY_STRING'};}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
($name, $value) = split(/=/, $pair);
$value=~tr/+/ /;
$value=~s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$value=~s/<!--(.|\n)*-->//g;
$value=~s/\t/--/g;
$value=~s/>/&gt;/g;
$value=~s/</&lt;/g;
$FORM{$name} = $value;
}
$menu=$FORM{'menu'};
###################################
$ajie='Ajie的留言本';
$home='中国CGI之家';
$homeurl="http://$ENV{'SERVER_NAME'}";
$images="$myurl/image";
$cgiurl=$myurl;
$cgiabs=$mypath;
$datapath="$cgiabs/data";
$infopath="$cgiabs/info";
$ipdir="$cgiabs/ipdata";
$userpath="$cgiabs/user";
$admin="Ajie";
$mailprog= &mailprogram;
################################
if($menu eq "ok"){&ok;exit;}
if($menu eq "register"){&register;exit;}
if($menu eq "adduser"){&adduser;exit;}
########## （第二步） ##########
print "Content-type: text/html\n\n";
print <<EOF;
<style>td {font-size:9pt}</style>
<title>Ajie的留言本安装向导</title>
<body bgcolor="#fafdfd" text="#000000">
<form method="post"><input type="hidden" value="ok" name="menu">
<div align="center">
<table cellSpacing="0" borderColorDark="#ffffff" cellPadding="3" width="646" bgColor="#83C6C0" borderColorLight="#008000" border="1">
<tbody><tr><td width="628"><center><p><b><font color="#ffffff">Ajie的留言本安装向导（第一步）</font></b></p></center></td></tr><tr><td width="628">
<table width=627 bgColor=ECF6F5><tbody><tr bgColor=ECF6F5><td align=right width=186>主页名称：</td><td width=466><input name=homename size=25 value=$home></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>主页地址：</td><td width=466><input name=homeurl size=25 value=$homeurl></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>站长信箱：</td><td width=466><input name=adminmail size=25 value="$adminmail"></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>超级用户名：</td><td width=466><input name=admname size=25 value=$admin></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>超级用户密码：</td><td width=466><input name=adpsd size=25></td></tr>
</tbody></table>
<table width=627 bgColor=ECF6F5><tbody>
<tr bgColor=ECF6F5><td align=right width=186>sendmail程序的绝对路径：</td><td width=466><input name=mailprog size=40 value=$mailprog></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>留言本目录的URL：</td><td width=466><input name=cgiurl size=40 value=$cgiurl></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>图片目录的URL：</td><td width=466><input name=images size=40 value=$images></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>留言本目录的绝对路径：</td><td width=466><input name=cgiabs size=40 value=$cgiabs></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>data目录的绝对路径：</td><td width=466><input name=datapath size=40 value=$datapath></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>user目录的绝对路径：</td><td width=466><input name=userpath size=40 value=$userpath></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>info目录的绝对路径：</td><td width=466><input name=infopath size=40 value=$infopath></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>ipdata目录的绝对路径：</td><td width=466><input name=ipdir size=40 value=$ipdir>
</td></tr>
</tbody></table>
</td></tr><tr><td width="628" align="center"><p><input type="submit" value="下一步"><font color="#ffffff"></font></td></tr>
<tr><td align="center" width="629"><font color="#ffffff">COPYRIGHT 2001 &copy; HOMECGI.COM
        ALL RIGHTS RESERVED 站长：Ajie QQ：5858314 Email：webmaster\@homecgi.com</font></td></tr></tbody></table></FORM></div>
EOF
exit;
##############################################
sub ok{
    print "Set-Cookie: adminname=$FORM{'admname'}\n";
    print "Set-Cookie: adminpass=$FORM{'adpsd'}\n";
$cgiabs      =$FORM{'cgiabs'};
$datapath    =$FORM{'datapath'};
$userpath    =$FORM{'userpath'};
$infopath    =$FORM{'infopath'};
$ipdir       =$FORM{'ipdir'};
chmod(0777,"$cgiabs");
mkdir("$datapath",077);
mkdir("$userpath",077);
chmod(0777,"$cgiabs/data");
chmod(0777,"$cgiabs/user");
chmod(0777,"$cgiabs/info");
if($FORM{'admname'} eq ""){&errorview("超级用户名不能没有填写!");}
if($FORM{'admname'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorview("名字中不能含有特殊字符!");}
if($FORM{'adpsd'} eq ""){&errorview("超级用户名密码不能没有填写!");}
if($FORM{'adpsd'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorview("密码中不能含有特殊字符!");}
unless(-d "$datapath"){&errorview("  无法创建$datapath这个目录，请确定CGI程序文件的绝对路径是否设置正确,$cgiabs目录属性是否为777！ ");exit;}
unless(-d "$userpath"){&errorview("  无法创建$userpath这个目录，请确定CGI程序文件的绝对路径是否设置正确,$cgiabs目录属性是否为777！");exit;}
unless(-d "$ipdir"){&errorview("  ipdir目录$ipdir的绝对路径错误，该目录不存在! ");exit;}
$homename    =$FORM{'homename'};
$homeurl     =$FORM{'homeurl'};
$admail      =$FORM{'adminmail'};
$admail      =~ s/\@/\\\@/g;
$admin       =$FORM{'admname'};
$password    =$FORM{'adpsd'};
$mailprog    =$FORM{'mailprog'};
$cgiurl      =$FORM{'cgiurl'};
$images      =$FORM{'images'};
open(PSD,">$infopath/setup.cgi");
print PSD "\$home=\"$FORM{'homename'}\";\n";
print PSD "\$homeurl=\"$FORM{'homeurl'}\";\n";
print PSD "\$adminmail=\"$admail\";\n";
print PSD "\$admin=\"$FORM{'admname'}\";\n";
print PSD "\$password=\"$FORM{'adpsd'}\";\n";
print PSD "\$mailprog=\"$mailprog\";\n";
print PSD "\$cgiurl=\"$cgiurl\";\n";
print PSD "\$images=\"$images\";\n";
print PSD "\$cgiabs=\"$cgiabs\";\n";
print PSD "\$datapath=\"$datapath\";\n";
print PSD "\$infopath=\"$infopath\";\n";
print PSD "\$userpath=\"$userpath\";\n";
print PSD "\$ipdir=\"$ipdir\";\n";
print PSD "\$lymax=\"300\";\n";
print PSD "\$pagenum=\"10\";\n";
print PSD "\$sendusermail=\"yes\";\n";
print PSD "\$mailtoadmin=\"yes\";\n";
print PSD "\$shenqing=\"on\";\n";
print PSD "\$mainonoff=\"on\";\n";
print PSD "1\;\n";
close(PSD);
chmod(0777,"$cgiabs/ipdata");
chmod(0666,"$cgiabs/info/setup.cgi");
chmod(0755,"$cgiabs/gbook.cgi");
chmod(0755,"$cgiabs/admin.cgi");
chmod(0755,"$cgiabs/sub.cgi");
chmod(0666,"$cgiabs/ipdata/10.txt");
chmod(0666,"$cgiabs/ipdata/61.txt");
chmod(0666,"$cgiabs/ipdata/202.txt");
chmod(0666,"$cgiabs/ipdata/210.txt");
chmod(0666,"$cgiabs/ipdata/other.txt");
&okok;
}
########## （第二步） ##########
sub okok {
print "Content-type: text/html\n\n";
print <<EOF;
<style>td {font-size:9pt}</style>
<title>Ajie的留言本安装向导</title>
<body bgcolor="#fafdfd" text="#000000" link="#ffffff">
<br><form method="post"><input type="hidden" value="ok" name="menu">  <div align="center">
<table cellSpacing="0" borderColorDark="#ffffff" cellPadding="3" width="400" bgColor="#83C6C0" borderColorLight="#008000" border="1">
<tbody><tr><td width="98%"><center><p><b><font color="#ffffff">Ajie的留言本安装向导（第二步）</font></b></p></center></td></tr><tr><td width="100%">
<table width=100% bgColor=ECF6F5><tbody><tr bgColor=ECF6F5><td align=center width=100%><br>请检查这张图片是否能正常显示<br><br><img src=$FORM{'images'}/04.gif>
<br>
<p>如果正常的话，请进行下一步</td></tr></tbody></table>
</td></tr><tr><td width="100%"><font color="#ffffff">
①：如果图片显示不正确，请 <b><a href=javascript:history.back()>
<font color="#0000ff">返回</font></a></b> 重新填写图片路径。<br>
②：如果你的第一次安装留言本，点击  <a href=install.cgi?menu=register><b>
<font color="#0000ff">这里</font></b></a> 申请留言本。<br>
③：如果你是升级安装，请点击 <a href=admin.cgi><b>
<font color="#0000ff">这里</font></b></a> 直接进入管理中心。</font>
</td></tr></tbody></td></tr></tbody></table></FORM></div>
EOF
exit;
}
########## （第三步） ##########
sub register {
require "$mypath/"."info/setup.cgi";
print "Content-type: text/html\n\n";
print <<EOF;
<style>td {font-size:9pt}</style>
<title>Ajie的留言本安装向导</title>
<body bgcolor="#fafdfd" text="#000000" link=#ffffff>
<br><form method="post"><input type="hidden" value="adduser" name="menu"><div align="center">
<table cellSpacing="0" borderColorDark="#ffffff" cellPadding="3" width="400" bgColor="#83C6C0" borderColorLight="#008000" border="1">
<tbody><tr><td width="98%"><center><p><b><font color="#ffffff">Ajie的留言本安装向导（第三步）</font></b></p></center></td></tr>
<tr><td width="98%"><center><p><b><font color="#ffffff">申请您的留言本</font></b></p></center></td></tr>
<tr><td width="100%">
<table width=100% bgColor=ECF6F5><tbody>
<tr bgColor=ECF6F5><td align=right width=25%>用 户 名：</td><td width=75%><input type="text" name="username" size="20" maxlength=8 value=$admin>* 1-8位（版主用户名）</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>用户密码：</td><td width=75%><input type="text" name="userpass" size=20 maxlength=8 value="$password">* 版主密码</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>重复密码：</td><td width=75%><input type="text" name="userpass1" size="20" maxlength=8>* 版主密码</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>电子邮件：</td><td width=75%><input type="text" name="emailaddress" size="20" value="$adminmail">* 邮件地址（邮件通知）</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>主页地址：</td><td width=75%><input type="text" name="homepage" value = "http://" size="20">* 主页地址</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>留言本名：</td><td width=75%><input type="text" name="title" size="20" value="$home留言本">* 你的留言本的名字</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>每页记录：</td><td width=75%><input type="text" name="recode" size="20" value="$pagenum" maxlength="2">* 默认为$pagenum条</td></tr>
</tbody></table>
</td></tr><tr><td width="100%" align="center">
<input type=button name=back value="上一步" onclick=javascript:history.go(-1)>&nbsp;&nbsp;&nbsp;&nbsp;
<input type="submit" value="下一步" name=ok></td>
</tr><tr><td align="center" width="629"><font color="#ffffff">COPYRIGHT 2001 &copy; HOMECGI.COM
        ALL RIGHTS RESERVED <br>站长：Ajie QQ：5858314 技术支持：<a href=http://www.homecgi.com/lb5000/leoboard.cgi><font color=#FFFFFF>CGI技术论坛</font></a></font></td></tr></tbody></td></tr></tbody></table></FORM></div>
EOF
exit;
}
########## （第四步） ##########
sub adduser {
if($FORM{'username'} eq ""){&errorview("用户名不能没有填写!");}
if (length($FORM{'username'})>8) {&errorview("名字不能超过8个字符！");}
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
print "Content-type: text/html\n\n";
print <<EOF;
<style>td {font-size:9pt}</style>
<title>Ajie的留言本安装向导</title>
<body bgcolor="#fafdfd">
<br><form method="post"><input type="hidden" value="ok" name="menu">  <div align="center">
<table cellSpacing="0" borderColorDark="#ffffff" cellPadding="3" width="400" bgColor="#83C6C0" borderColorLight="#008000" border="1">
<tbody><tr><td width="98%"><center><p><b><font color="#ffffff">Ajie的留言本安装向导（完成）</font></b></p></center></td></tr><tr><td width="100%">
<table width=100% bgColor=ECF6F5><tbody><tr bgColor=ECF6F5>
<td align=center width=100%><br><a href=admin.cgi>进入管理中心</a><br><br><a href=gbook.cgi?user=$name><font color="#000000">进入您的留言本</font></a><br></td></tr></tbody></table>
</td></tr><tr><td align="center" width="100%"><font color="#ffffff">COPYRIGHT 2001 &copy; HOMECGI.COM
        ALL RIGHTS RESERVED <br>站长：Ajie QQ：5858314 技术支持：<a href=http://www.homecgi.com/lb5000/leoboard.cgi><font color=#FFFFFF>CGI技术论坛</font></a></font></td></tr></tbody></td></tr></tbody></table></FORM></div>
EOF
exit;
}
##############################################
sub mailprogram
{
    $mailprogram='/usr/sbin/sendmail';
    if (!(-e $mailprogram)) {$mailprogram='/usr/bin/sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='/bin/sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='/lib/sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='/usr/slib/sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='/usr/lib/sendmail';};
    if (!(-e $mailprogram)) {$mailprogram='perlmail';};
    if (!(-e $mailprogram)) {$mailprogram="没有找到Sendmail路径，可能你的主机不支持";};
    return $mailprogram;
}
##############################################
sub errorview {
&css;print "
<BODY background=$imagurl/bg.gif>
<TITLE>出错提示</TITLE>
<TABLE  width=100% border=0>
<TBODY><TR align=middle><TD height=413 valign=middle align=center>
<TABLE cellSpacing=0 borderColorDark=#ffffff bgColor=#336666 borderColorLight=#000000 border=1 width=275><TBODY><TR><TD width=350>
<TABLE cellSpacing=0 cellPadding=2 width=100% bgColor=#83C6C0 border=0>
<TBODY><TR><TD width=100%><FONT color=#336666>¤ 出错提示</FONT></TD><TD width=18>
<TABLE cellSpacing=0 borderColorDark=#ffffff cellPadding=0 bgColor=ECF6F5 borderColorLight=#666666 border=1><TBODY>
<TR><TD><B><font color=#336666>×</font></B></TD></TR></TBODY></TABLE></TD>
</TR></TBODY></TABLE>
<TABLE cellPadding=4 width=100% bgColor=#ECF6F5 border=0><TBODY>
<TR><TD vAlign=top align=center width=47><FONT size=7 face=Wingdings color=#ff0000>L</FONT></TD><TD width=210><P><font size=2>$_[0]</font></P></TD></TR>
<TR><TD vAlign=top align=center colSpan=2 width=100%><div align=center><center>
<table border=1 bgColor=cccccc cellspacing=0><tr><td width=100% align=center bordercolordark=#E6E6E6 bordercolorlight=#cccccc><A href=javascript:history.back()><font size=2 color=#000000>　确 定&nbsp;&nbsp;</font></A></td></tr></table></center></div></TD></TR></TBODY></TABLE></TD></TR></TBODY></TABLE></TD></TR></TBODY></TABLE></HTML>";exit;}
sub css {
print "Content-type: text/html\n\n";
print <<EOF;
<HTML><HEAD><meta http-equiv=Content-Type content=text/html; charset=gb2312><link REL="SHORTCUT ICON" href=$imagurl/gb.ico><style>td {font-size:9pt}</style></HEAD><body topmargin=0>
EOF
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
sub myurl{
local $server_port,$fullurl;
$server_port = ":$ENV{'SERVER_PORT'}"
if ($ENV{'SERVER_PORT'} ne '80');
$fullurl = "http://$ENV{'SERVER_NAME'}$server_port$ENV{'SCRIPT_NAME'}";
$myurl = substr($fullurl,0,rindex($fullurl,"/"));
return $myurl;
}