#!/usr/bin/perl
#------------------------------------------------------#
#                 ������ΪYuzi�������ṩ               #
#              Yuzi��������2000���û���v1.20           #
#------------------------------------------------------#
require "setup.cgi";
######################
## ���²��ֲ����޸� ##
######################
$cgiurl    = "xiu.cgi";
$from    = $ENV{'REMOTE_ADDR'};
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday)= localtime(time+(3600*$time_hour));
$mon=$mon+1;
if($mon <10){$mon="0".$mon;}
if($mday<10){$mday="0".$mday;}
if($hour<10){$hour="0".$hour;}
if($min<10){$min="0".$min;}
if($sec<10){$sec="0".$sec;}
$year=$year+1900;
$thistime=$year."-".$mon."-".$mday.".".$hour.":".$min.":".$sec;
$lasttime=$year."-".$mon."-".$mday;
##########
if ($ENV{'REQUEST_METHOD'} eq "POST") {
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}
else {
$buffer = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
($name, $value) = split(/=/, $pair);
$value =~ tr/+/ /;
$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$FORM{$name} = $value;
$FORM{'htmlt'}=~s/\n//g;
$FORM{'htmlw'}=~s/\n//g;
$FORM{'jj'}=~s/\n//g;
}
##########
$username = $FORM{'username'};
$newpsd   = $FORM{'newpsd'};
$userpsd  = $FORM{'userpsd'};
$titles   = $FORM{'titles'};
$comment  = $FORM{'comment'};
$urlname = $FORM{'urlname'};
$mail     = $FORM{'mail'};
$home     = $FORM{'home'};
$htmlt     = $FORM{'htmlt'};
$htmlw     = $FORM{'htmlw'};
$title    = $FORM{'title'};
$a_method = $FORM{'a_method'};
$newpsd   = $FORM{'newpsd'};
$jj   = $FORM{'jj'};
$regd=0;
$regda=0;
$regdb=0;
if($a_method eq "reguser"){&reguser; exit;}
if($a_method eq "reg"){&reg;exit;}
if($username eq ""){&bzgl;exit;}
&reg;
exit;
##########
sub send_html {
if ($has_send ne "1") {
print "Content-type: text/html\n\n";
$has_send = "1";
}
}
##########
sub reg{
if ( -e "$filepath/list/$username.cgi"){
open(PSD,"$filepath/list/$username.cgi")||die $!;
@lines=<PSD>;
close(PSD);
foreach $line (@lines) {
$line=~ s/\n//g;
($rname,$rpass,$rmail,$rhome,$rtitle,$urlname,$rtime,$htmlt,$htmlw,$jj)=split(/\t/,$line);
&send_html;
print <<EOF;
<HTML><HEAD><TITLE>���������޸�</TITLE>
<STYLE type=text/css>TD {
FONT-FAMILY: Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 20px
}
.pt9 {
FONT-FAMILY: "����", "Arial", "Times New Roman"; FONT-SIZE: 9pt; LINE-HEIGHT: 13pt
}
.pt9w {
COLOR: #ffffff; FONT-FAMILY: "����", "Arial", "Times New Roman"; FONT-SIZE: 9pt; LINE-HEIGHT: 13pt
}
.pt9b {
FONT-FAMILY: "����", "Arial", "Times New Roman"; FONT-SIZE: 9pt; FONT-WEIGHT: bold; LINE-HEIGHT: 13pt
}
.pt10 {
FONT-FAMILY: ����, "Arial", "Times New Roman"; FONT-SIZE: 16px; LINE-HEIGHT: 21px
}
A:link {
COLOR: rgb(152,78,50); CURSOR: hand; FONT-STYLE: normal; TEXT-DECORATION: none
}
A:visited {
COLOR: #666666; FONT-STYLE: normal; TEXT-DECORATION: none
}
A:active {
COLOR: rgb(198,198,198); FONT-STYLE: normal; TEXT-DECORATION: none
}
A:hover {
COLOR: rgb(72,105,191); TEXT-DECORATION: none
}
</STYLE>

<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style><!--  .ourfont{font-size: 12px;line-height: 17px;}
A:link {text-decoration: none; color: #ffffff}       A:visited {text-decoration: none; color:#8080FF }      A:active {text-decoration: none}      A:hover {text-decoration: none; color: #FF0000}   --></style>
</HEAD>
<BODY bgColor=#ffffff textcolor="000000">
<form method="post" action="$cgiurl">
<input type="hidden" name="a_method" value="reguser">
<div align="center">
<table border="1" cellpadding="3" cellspacing="0" width="310" bgcolor="#FFCC66" bordercolorlight="#008000" bordercolordark="#FFFFFF">
<tr>
<TD><center><p><b>���������޸�</b></p></TD>
</tr>
<tr>
<TD>
<P class=pt9>��
������ɺ������ɻ���Լ���$cginame($ym/$yuzicgi?id=����Ա����) <BR>��
��<FONT color=red>*</FONT>Ϊ���� </P></TD>
</tr>
<tr>
<TD>
<TABLE bgColor=#bbbbbb width="627">
<TBODY>
<TR>
<TD align=right class=pt9 width="186"><FONT color=red>*</FONT>  ���趨$cginame�����ƣ�</TD>
<TD class=pt9 width="466"><INPUT maxLength=80 name=title size=65  value=$rtitle></TD></TR>
<TR>
<TD align=right class=pt9 width="186"><FONT color=red>*</FONT>
����Ա���ƣ�</TD>
<TD class=pt9 width="466"><INPUT maxLength=20 name=username value=$rname> </TD></TR>
<TR>
<TD align=right class=pt9 width="186"><FONT color=red>*</FONT>
����Ա���룺</TD>
<TD class=pt9 width="466"><INPUT name=userpsd type=password value=$userpsd></TD></TR>
<TR>
<TD align=right class=pt9 width="186">����Ա�������룺</TD>
<TD class=pt9 width="466"><input size=20 maxlength=12 name="newpsd" value=><FONT color=red>�������������������룬�˴������գ�</TD></TR>
<TR>
<TD align=right class=pt9 width="186"><FONT color=red>*</FONT>  ����Email��ַ��</TD>
<TD class=pt9 width="466"><INPUT maxLength=80 name=mail size=50 value=$rmail></TD></TR>
<TR>
<TD align=right class=pt9 width="186">������ҳ���ƣ�</TD>
<TD class=pt9 width="466"><INPUT name=urlname value=$urlname><TR></TD></TR>
<TR>
<TD align=right class=pt9 width="186">������ҳ��URL��</TD>
<TD class=pt9 width="466"><INPUT maxLength=80 name=home size=65 value=$rhome><TR></TD></TR>
<TR>
<TD align=right class=pt9 width="186">$cginame��飺</TD>
<TD class=pt9 width="466"><textarea cols=63 name=jj rows=5>$jj</textarea></TD></TR>
<TR>
<TD align=right class=pt9 width="186">$cginameͷ����ʾ��Ϣ��<br><FONT color=red>��֧�� html��</FONT></TD>
<TD class=pt9 width="466"><textarea cols=63 name=htmlt rows=5>$htmlt</textarea></TD></TR>
<TR>
<TD align=right class=pt9 width="186">$cginameβ����ʾ��Ϣ��<br><FONT color=red>��֧�� html��</FONT></TD>
<TD class=pt9 width="466"><textarea cols=63 name=htmlw rows=5>$htmlw</textarea></TD></TR>
</TBODY></TABLE></TD>
</tr>
<tr>
<TD class=pt9>
<P><input type="submit" value="����ˣ�������"><P align=center
class=pt9>������ʹ�ñ�$cginameϵͳ���û������Ի��<BR><B>$ym/$yuzicgi?id=�û���</B><BR>������ָ����$cginameϵͳ��<BR>
<P align=right class=pt9><a href="reg.cgi">[�������]</a>[���������޸�]<a href="cjyh.cgi">[�����û�����]</a><a href="list.cgi">[�û��б�]</a>
<P>
<DIV
class=pt9>ע�����<BR>1������ʹ�ñ�$cginameϵͳ�����κΰ���ɫ�顢�Ƿ����Լ�Σ�����Ұ�ȫ�����ݵ�$cginame;<BR>2�������ڱ�ϵͳ�û���ӵ�е�$cginame�ڷ����κ�ɫ�顢�Ƿ�������Σ�����Ұ�ȫ��$cginame;<BR>3�����Ϲ���Υ�������Ը�����վ��Ȩɾ�������û��������ݣ���׷���䷨�����Ρ�<BR></DIV></TD>
</tr>
<td align="middle">���$cginame������<font color=#cc0033>
</font><font color=#ff6633><b><font Helvetica, sans-serif><a href=$zyurl>$zynames</a></font></b></font><font color=#cc0033>
</font>�ṩ������������<b><a href="http://www.yuzi.net" target="_blank">Yuzi������</b></a></td>
��</td>
</tr>
</table>
</form>
</BODY></HTML>
EOF
exit;
}
}else{
&errorview("�Բ��𣬴�����û���ڱ�$cginameע���!");exit;
}
}
##########
sub reguser{
if(($userpsd eq "")||($username eq "")||($mail eq "")||($title eq "")){&errorview("��ʾ���⡡���֡����롡���䡡��˳Ҫ��д�ģ����������룡");exit;}
if(!($mail=~ /.*\@.*\..*/)){&errorview("����Email�������");exit(0);}
if(length($jj) > 400 ){&errorview("����$cginame��鲻�ܴ���200�����֣�");exit;}
if ( -e "$filepath/list/$username.cgi"){
$regd=1;
open(PSD,"$filepath/list/$username.cgi")|| die $!;
@lines=<PSD>;
close(PSD);
foreach $line (@lines) {
$line=~ s/\n//g;
($rdname,$rdpassword,$rdtitle,$rdmail,$rdhome,$rlast)=split(/\t/,$line);
if($username eq $rdname){
$regda=1;
if($userpsd eq $rdpassword){
$regdb=1;
}
}
}
if($regdb eq "1"){
if($newpsd ne ""){$userpsd = $newpsd}
open(PSD,">$filepath/list/$username.cgi")|| die $!;
foreach $line (@lines) {
$line=~ s/\n//g;
($rdname,$rdpassword,$rdtitle,$rdimg,$rdmail,$rdhome,$rdlasttime)=split(/\t/,$line);
if($newpsd ne ""){$userpsd = $newpsd}
if($username eq $rdname){
print PSD $username."\t".$userpsd."\t".$mail."\t".$home."\t".$title."\t".$urlname."\t".$lasttime."\t".$htmlt."\t".$htmlw."\t".$jj;
print PSD "\n";
}else{
print PSD $line."\n";
}
}
close(PSD);
}
if(($regda eq "1")&&($regdb ne "1")){&errorview("�������������������������룡");exit;}
if(($regd eq "1")&&($regda ne "1")){
unless(-f "$filepath/list/$username.cgi"){
open(PSD,">>$filepath/list/$username.cgi")||die $!;
print PSD $username."\t".$userpsd."\t".$mail."\t".$home."\t".$title."\t".$urlname."\t".$lasttime."\t".$htmlt."\t".$htmlw."\t".$jj;
print PSD "\n";
close(PSD);
chmod(0666,"$filepath/list/$username.cgi");
}
}
}else{
&errorview("�Բ��𣬴��û���û���ڱ�$cginameע���!");exit;
}
&send_html;
print "<HEAD>\n";
print "<TITLE>ף �� �� �� �� �� �� �� �� �� �� ��</TITLE>\n";
print "</HEAD>\n";
print "<style type=text/css>TD{FONT-SIZE:9pt}A{FONT-SIZE:9pt;TEXT-DECORATION:none}A:hover{FONT-SIZE:9pt;TEXT-DECORATION:underline}</style>\n";
print "<body background=$imagurl/bg.jpg>\n";
print "<br>\n";
print "<p class=pt10 align=center><b>ף �� �� �� �� �� �� �� �� �� �� ��</b>\n";
print "<p class=pt10 align=center><b><a href=$yuzicgi?id=$username target=_blank>����Ϊ������$cginame����ṩ��һ���������Լ���������<br>$ym/$yuzicgi?id=$username<br>���ס����</a></b>\n";
print "<p class=pt10 align=center><b><a href=$yuzicgi?id=$username target=_blank>���ڴ����ϵ���������Ҽ���<br>�������������������ǩ�����ղؼ���</a></b>\n";
print "<p class=pt10 align=center>\n";
print "<table cellspacing=4 cellpadding=3><tr><td class=pt9 align=right bgcolor=#FFF5E1><b>��ʾ���⣺</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000>$FORM{title}</font><td class=pt9 bgcolor=#FFF5E1><b>������ҳ��</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000>$FORM{home}</font><tr><td class=pt9 align=right bgcolor=#FFF5E1><b>ע��������</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000>$FORM{username}</font><td class=pt9 bgcolor=#FFF5E1><b>�������룺</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000>$userpsd</font><tr><td class=pt9 align=right bgcolor=#FFF5E1><b>�������䣺</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000>$FORM{mail}</font><td class=pt9 bgcolor=#FFF5E1><b>ע��ʱ�䣺</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000>$lasttime.</font></table>\n";
print "</table>\n";
print "<br>\n";
print "<div align=center><center><table border=1 borderColorDark=#ffffff borderColorLight=#008000 cellPadding=0 cellSpacing=0 width=60%><tbody><tr><td align=middle width=100%>��ҳ�����CGI������£�������������<a href=http://www.yuzi.net target=_blank>YUZI������</a>��</td></tr></tbody></table></center></div>\n";
exit;
}
########
sub bzgl{
&send_html;
print <<EOF;
<HTML>
<head>
<META HTTP-EQUIV=Content-Type CONTENT=text/html; charset=gb2312>
<TITLE>���������޸�</TITLE>
<style type=text/css>
<!--
.ourfont {font-size: 9pt ; line-height:13pt; }
A{text-transform: none; text-decoration: none;}
a:hover {text-decoration:underline}
-->
</style>
</head>
<BODY BGCOLOR=white text=000000 link=blue vlink=blue>
<br>
<center><table border=1 bgcolor=ffffdd><tr><td align=center>
<p><b><font face="����" size="5">���������޸�</font></b>
<form method="post" action="$cgiurl">
<table border=0>
<tr><td class=ourfont>��������:</td><td class=ourfont><input type="text" name="username" size="9"></td></tr>
<tr><td class=ourfont>��������:</td><td class=ourfont><input type="password" name="userpsd" size="9"></td></tr>
<tr><td class=ourfont colspan=2><input name="submit" type="submit" value="����"></td></tr>
</table>
</form>
<div class=ourfont>
<a href="reg.cgi">[�������]</a>[���������޸�]<a href="cjyh.cgi">[�����û�����]</a><a href="list.cgi">[�û��б�]</a><br>
<hr size=1 width=450>
���$cginame������ <a href=$zyurl>$zynames</a> �ṩ����������<a href=http://www.yuzi.net targe=_blank> Yuzi������ </a>
</div>
</html>
EOF
exit;
}
######################### END OF SCRIPT #########################