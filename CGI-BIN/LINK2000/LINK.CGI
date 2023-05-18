#!/usr/bin/perl
#------------------------------------------------------#
#                 本程序为Yuzi工作室提供               #
#              Yuzi友情连接2000多用户版v1.20           #
#------------------------------------------------------#
require "setup.cgi";
######################
## 以下部分不需修改 ##
######################
($sec,$min,$hour,$mday,$mon,$year)= localtime(time+(3600*$time_hour));
$mon=$mon+1;
$year=$year+1900;
if($mon <10){$mon="0".$mon;}
if($mday<10){$mday="0".$mday;}
if($hour<10){$hour="0".$hour;}
if($min<10){$min="0".$min;}
if($sec<10){$sec="0".$sec;}
$thistime=$year."/".$mon."/".$mday;
&get_form;
&set_var;
open (PEOPLE, "$filepath/list/$id.cgi") || &open_error($userfile);
@lines = <PEOPLE>;
close (PEOPLE);
foreach $line (@lines){
$line=~ s/\n//g;
($rname,$rpassword,$rmail,$rhome,$rtitle,$urlname,$zhtime,$htmlt,$htmlw)=split(/\t/,$line);
if($rname eq $id){
$yuzibook ="$filepath/data/$id/$id.cgi";
$delpsd   = $rpassword;
}
}
mkdir("$filepath",0777);
mkdir("$filepath/list",0777);
mkdir("$filepath/data",0777);
unless(-f $yuzibook){
open(TMP,">$yuzibook")||die $!;
close(TMP);
chmod(0666,$yuzibook);
}
unless(-f $chklast){
open(TMP,">$chklast")||die $!;
close(TMP);
chmod(0666,$chklast);
}
if ($ENV{'REQUEST_METHOD'} eq "POST") {
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
} else {
$buffer = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
($name, $value) = split(/=/, $pair);
$FORM{$name} = $value;
}
$FORM{'comments'}=~s/\n/<br>/g;
$userip  =$ENV{'REMOTE_ADDR'};
$id=$FORM{'name'};
$logo    =$FORM{'logo'};
$userurl =$FORM{'URL'};
$ip      =$FORM{'ip'};
$page    =$FORM{'page'};
$retime  =$FORM{'retime'};
$username=$FORM{'username'};
$mail    =$FORM{'mail'};
$id      =$FORM{'id'};
$search  =$FORM{'search'};
$psd     =$FORM{'psd'};
$wzfl    =$FORM{'wzfl'};
$dj      =$FORM{'dj'};
$comments=$FORM{'comments'};
$search  =$FORM{'search'};
if($ip eq ""){$ip=$userip;}
$a_method=$FORM{'a_method'};
if($a_method eq "del"){&del;}
if($a_method eq "find"){&find;}
if($a_method eq "write"){&write;}
if($a_method eq "win"){&win;}
if($a_method eq "dj"){&dj;}
if($a_method eq "xiu"){&xiu;}
if($a_method eq "edit"){&edit;}
if($a_method eq "bzgl"){&bzgl;}
if($a_method eq ""){&show;}
##########
if($a_method eq "add"){
if($username eq ""){&errorview("您的网站名称不能没有填写哦！");exit;}
if($psd eq ""){&errorview("您的密码不能没有填写哦！");exit;}
if(!($mail=~ /.*\@.*\..*/)){&errorview("您的Email输入错误！");exit(0);}
if($userurl eq ""){&errorview("您的主页地址不能没有填写哦！");exit;}
if($comments eq ""){&errorview("您的主页简介不能没有填写哦！");exit;}
if(length($comments) > 400 ){&errorview("您的主页简介不能大于200个汉字！");exit;}
if ( -e "$filepath/data/$id/$username"){&errorview("您的网站资料已经加入友情连接！");exit;}
open (GUEST,"$yuzibook")||die $!;
@lines=<GUEST>;
close(GUEST);
$size=@lines;
$addsays=$username;
open (GUEST,">$yuzibook")||die $!;
print GUEST $addsays."\n";
for($i=0;$i<=$size;$i++){
$_=@lines[$i];
print GUEST $_;
}
close(GUEST);
$peo="$filepath/data/$id/$username";
unless(-f $peo){
open(TMP,">$peo");
close(TMP);
chmod(0666,$peo);
}
open(TMP,">$peo");
print TMP $username."\t".$psd."\t".$mail."\t".$userurl."\t".$comments."\t".$ip."\t".$thistime."\t".$wzfl."\t".$logo."\t".0;
close(TMP);
}
open (mail,"| $mailprg") || die "logo system error";
print mail "To: $mail\n";
print mail "Subject: 这是您在 $rtitle 登记的信息\n";
print mail "这是您在 $rtitle 登记的信息\n";
print mail "----------------------------------------------------------\n";
print mail "您的网站名称 : $username\n";
print mail "您的密码     : $psd\n";
print mail "您的邮件地址 : $mail\n";
print mail "您的主页地址 : $userurl\n";
print mail "您的图标地址 : $logo\n";
$comments =~ s/<br>/\n/g;
print mail "您的网站介绍 : $comments\n\n";
print mail "          您可以通过您的网站名称及密码, 修改您的站点资料了!\n";
print mail "          请将 $urlname($rhome) 加入到您的友情链接\n\n";
print mail "                                 $urlname: $rname\n";
print mail "                                 E-MAIL:   $rmail\n";
print mail "----------------------------------------------------------\n";
print mail "程序制作：Yuzi工作室(http://www.yuzi.net)\n";
print mail "免费$cginame服务由 $zynames($zyurl) 提供\n";
print mail "\n\n";
close(mail);
&win;
exit;
##########
sub get_form {
@querys = split(/&/, $ENV{'QUERY_STRING'});
foreach (@querys) {
($name,$value) = split(/=/, $_);
$value = &filterhtml($value);
&setvaluetoform($name, $value);
if ($name eq "userpassword") {&check_password;}
}
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $buffer);
foreach (@pairs) {
($name, $value) = split(/=/, $_);
$value =~ tr/+/ /;
$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$value = &filterhtml($value);
&setvaluetoform($name, $value);
if ($name eq "userpassword") {&check_password;}
}
}
##########
sub filterhtml {
local($return)=$_[0];
$return =~ s/<!--(.|\n)*-->//g;
if ($allow_html != 1) {
$return =~ s/<([^>]|\n)*>//g;
$return =~ s/<//g;
}
return $return;
}
##########
sub setvaluetoform {
if ($FORM{$_[0]}) {
$FORM{$_[0]}="$FORM{$_[0]}§$_[1]";
}
else {
$FORM{$_[0]}=$_[1];
}
}
##########
sub check_password {
$userid       =&get_var('userid'      ,'\n|"|<|>|\&|;| |\?|‖') if ($idasuserid==0);
$userid       =&get_var('id'    ,'\n|"|<|>|\&|;| |\?|‖') if ($idasuserid==1);
$userpassword =&get_var('userpassword','\n|"|<|>|\&|;| |\?|‖');
if ($super{$userid}) {
($chkuserpassword,$chkuserlevel)=split(/‖/,$super{$userid});
$userlevel=$chkuserlevel if ($chkuserpassword eq $userpassword);
$allow_html=1 if ($userlevel>=$level_html);
}
}
##########
sub set_var {
$job              =&get_var('job'            ,'\n|‖');
$id         =&get_var('id'       ,'\n|"|<|>|\&|;| |\?|‖');
&checkempty($id,"<a href=reg.cgi>请先注册$cginame</a>");
}
##########
sub get_var {
local($return)="";
$return="$FORM{$_[0]}" if ($FORM{$_[0]});
$return=~ s/$_[1]//g;
return $return;
}
##########
sub checkempty {
local($chkval)=$_[0];
$chkval =~ s/ |<br>|\n//g;
&error($_[1]) if ($chkval eq "");
}
##########
sub error {
&send_html;
print "<html><head><title>$roomtitle error</title>\n";
print "<META HTTP-EQUIV=REFRESH CONTENT='$_[1];URL=$_[2]'>\n" if (($_[1]) && ($_[2]));
print "</head><bodytext=$messageword>\n";
print "<center><h1>ERROR</h1><h2>$_[0]</h2></center>\n";
print "</body></html>\n";
exit 0;
}
##########
sub show {
if(($psd ne $rpassword)&&($psd ne "")){&errorview("您的密码错误！");exit;}
open(GUEST,"$yuzibook")||die $!;
@lines=<GUEST>;
close(GUEST);
$size=@lines;
&send_html;
$ii=0;
$j=$size;
while ($j>0) {
$j=$j-$perpage;
$ii++;
}
print <<EOF;
<html>
<head>
<style>
<!--
{font-size: 12px;}
p {font-size:12px;}
a { text-decoration: none; color: rgb(40,40,180) }
a:hover {color:#FF9900;text-decoration:none}
table {font-size:12px;}
td {font-size:12px;}
-->
</style>
<SCRIPT language=JavaScript>
<!-- Begin
function formHandler()
{
var URL = document.form.wzfl.options[document.form.wzfl.selectedIndex].value;
window.location.href = URL;
// End -->
}
</SCRIPT>
</head>
<title>$rtitle</title>
$htmlt
<table width=88% border=0 cellpadding=0 cellspacing=0 align=center>
<tr>
<td>
<div align=center><img src=$imagurl/title.gif></div>
</td>
</tr>
<tr>
<td>
<table width=100% border=0 cellspacing=0 cellpadding=0>
<tr>
<td align=center>
<a href=$yuzicgi?id=$id&a_method=write><img border=0 src=$imagurl/write.gif alt=友情登陆></a><a href=$yuzicgi?id=$id&a_method=xiu><img border=0 src=$imagurl/modi.gif alt=友情修改></a><a href=$yuzicgi?id=$id&a_method=bzgl><img src=$imagurl/admin.gif alt=版主管理 border=0></a><a href=$rhome><img src=$imagurl/home.gif alt=返回主页 border=0></a><a href=reg.cgi><img border=0 src=$imagurl/reg.gif alt=免费申请></a>
</td>
<td width=55% class=unnamed1 align=center>
<p><span class=unnamed1>$rtitle</span></p>
</td>
<td width=25% align=right>
<span class=unnamed1>共 <font color=#0099CC>$size</font> 个网站加入友情链接</span>
</td>
</tr>
</table>
</td>
</tr>
</table>
<tr valign=top>
<td height=12>
<table width=88% border=0 cellspacing=1 cellpadding=0 align=center background=$imagurl/pattn3.gif>
<tr>
<td height=25>
<div align=center class=unnamed1>
<FORM name=form>网站分类：<select name=wzfl onchange=formHandler() size=1>
<option selected value=$yuzicgi?id=$id>选择分类</option>
<option value=$yuzicgi?id=$id>所有类别</option>
<option value=$yuzicgi?id=$id&a_method=find&search=国家地区>国家地区</option>
<option value=$yuzicgi?id=$id&a_method=find&search=电脑网络>电脑网络</option>
<option value=$yuzicgi?id=$id&a_method=find&search=休闲娱乐>休闲娱乐</option>
<option value=$yuzicgi?id=$id&a_method=find&search=生活资讯>生活资讯</option>
<option value=$yuzicgi?id=$id&a_method=find&search=人文艺术>人文艺术</option>
<option value=$yuzicgi?id=$id&a_method=find&search=文化教育>文化教育</option>
<option value=$yuzicgi?id=$id&a_method=find&search=自然科学>自然科学</option>
<option value=$yuzicgi?id=$id&a_method=find&search=社会文化>社会文化</option>
<option value=$yuzicgi?id=$id&a_method=find&search=医药保健>医药保健</option>
<option value=$yuzicgi?id=$id&a_method=find&search=工商产业>工商产业</option>
<option value=$yuzicgi?id=$id&a_method=find&search=金融投资>金融投资</option>
<option value=$yuzicgi?id=$id&a_method=find&search=谈天说地>谈天说地</option>
<option value=$yuzicgi?id=$id&a_method=find&search=情感天地>情感天地</option>
<option value=$yuzicgi?id=$id&a_method=find&search=游戏世界>游戏世界</option>
<option value=$yuzicgi?id=$id&a_method=find&search=体育竞技>体育竞技</option>
<option value=$yuzicgi?id=$id&a_method=find&search=新闻时事>新闻时事</option>
<option value=$yuzicgi?id=$id&a_method=find&search=美眉天地>美眉天地</option>
<option value=$yuzicgi?id=$id&a_method=find&search=其他类别>其他类别</option>
</select>
　　现在有 <font color=#0080C0>$size</font> 个网站加入了<font color=#0099CC>所有类别</font>类
</div>
</td>
</tr> </form>
</table>
</td>
</tr>
<br>
EOF
if($page eq ""){$page=1;}
$pages=$page-1;
#foreach $line (@lines){
$pages=$page*$perpage-$perpage;
for($i=$pages; $i<$pages+$perpage; $i++) {
$line=@lines[$i];
$line =~ s/\n//g;
if ($line ne "") {
($index) = split(/\t/,$line);
unless(-f "$filepath/data/$id/$index"){
open(TMP,">$filepath/data/$id/$index")||die $!;
close(TMP);
chmod(0666,"$filepath/data/$id/$index");
}
open(PSD,"$filepath/data/$id/$index")|| die $!;
@lines1=<PSD>;
close(PSD);
foreach $line1 (@lines1) {
$line1=~ s/\n//g;
($rd_name,$rd_psd,$rd_mail,$rd_url,$rd_msg,$rd_ip,$rd_time,$wzfl,$rd_logo,$dj)=split(/\t/,$line1);
}
if(($rd_logo eq "")||($rd_logo eq "http://")){$rd_logo="$imagurl/nobanner.gif";}
print <<EOF;
<tr>
<td>
<table width=80% border=0 cellspacing=1 cellpadding=0 align=center>
<tr bgcolor=#0088aa class=unnamed1>
<td width=14%>
<div align=center>
<font color=#E1F0FF><b>网站名称:</b></font>
</div>
</td>
<td width=36%>
<div align=center>
<font color=#E1F0FF><b>$rd_name</b></font>
</div>
</td>
<td width=20% bgcolor=#0088aa>
<div align=center>
<font color=#E1F0FF><b>$wzfl</b></font>
</div>
</td>
<td width=15%>
<div align=center>
<font color=#E1F0FF><b>$rd_time</b></font>
</div>
</td>
<td width=15%>
<div align=center>
<font color=#E1F0FF><b>点击 <strong>$dj</strong> 次</b></font>
</div>
</td>
</tr>
<tr>
<td rowspan=2 width=14% class=unnamed1><a href=$yuzicgi?id=$id&a_method=dj&dj=$index target=_blank><img border=0 height=31 width=88 src=$rd_logo></a></td>
<td colspan=4 class=unnamed1><font color=#000000>网站地址:</font>
<a href=$yuzicgi?id=$id&a_method=dj&dj=$index target=_blank><font color=#004fff>$rd_url</font></a>
EOF
if ($psd eq $rpassword){
print "　　　<a href=$cgiurl?a_method=del&psd=$psd&id=$id&delindex=$index>◎　删 除　◎</a>";
}
print<<EOF;
</td>
</tr>
<tr>
<td colspan=4 class=unnamed1><font color=#0080ff>$rd_msg</font></td>
</tr>
</table>
</td>
</tr>
<tr>
<td>　</td>
</tr>
EOF
}
}
print "</table><center><tr><td><table width=88% border=0 cellspacing=0 cellpadding=0 background=$imagurl/pattn3.gif><tr><td height=25><div align=center><font color=#0088aa class=unnamed1>\n";
$j=$size;
while ($j>0) {
print "<a href=$yuzicgi?page=$ii&id=$id&psd=$psd>" if ($page != $ii);
print "[$ii]";
print "</a>" if ($page != $ii);
$j=$j-$perpage;
$ii--;
}
print <<EOF;
</font></div></td></tr></table></td></tr></table>
<form method=post action=$yuzicgi?id=$id>
<input type="hidden" name="psd" value=$psd>
<table width=210 cellspacing=1 bgcolor=#D8F3FE cellpadding=5>
<tr><td width=100% bgcolor=#ffffff align="center">
请输入您要搜索的字符<input type=hidden name=a_method value=find>
<input type=text name=search><input name=submit type=submit value=确定>
</td></tr>
</table>
</form>
EOF
print "$htmlw<br><td align=middle>免费$cginame服务由<font color=#cc0033></font><font color=#ff6633><b><font Helvetica, sans-serif> <a href=$zyurl>$zynames</a> </font></b></font><font color=#cc0033></font>提供　程序制作：<b><a href=http://www.yuzi.net target=_blank>Yuzi工作室</b></a></td></td>\n";
print "</body></html>\n";
exit;
}
##########
sub write{
&send_html;
print <<EOF;
<HTML><HEAD><TITLE>【登陆网站】</TITLE>
<META content=text/html; charset=gb2312 http-equiv=Content-Type>
<META content='Microsoft FrontPage 4.0' FrontPage 4.0 name=GENERATOR>
<STYLE>BODY {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; MARGIN-TOP: 0px
}
TABLE {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
INPUT {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
TEXTAREA {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
SELECT {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
A:link {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: none
}
A:visited {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: none
}
A:active {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: underline
}
A:hover {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: underline
}
.11f {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 10.5pt; LINE-HEIGHT: 12pt
}
</STYLE>
</HEAD>
<BODY link=#ffff00 text=#00ffff vLink=#ffff00>
<P align=center><FONT color=black><BR>登陆你的网站</FONT></P>
<form action=$yuzicgi?id=$id method=post>
<input type=hidden name=a_method value=add>
<DIV align=center>
<CENTER>
<TABLE border=1 borderColor=#ffffff borderColorDark=#ffffff
borderColorLight=#000000 cellSpacing=0 height=203 width=617>
<TBODY>
<TR align=middle>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=17 width=98><FONT
color=#000000>你的站点名称：</FONT></TD>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=17 width=203><INPUT maxLength=20
name=username size=20 tabIndex=1></TD>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=17 width=98><FONT
color=#000000>你的E-Mail地址：</FONT></TD>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=17 width=194><INPUT name=mail
size=20 tabIndex=5></TD></TR>
<TR align=middle>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=9 width=98><FONT
color=#000000>你的主页地址：</FONT></TD>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=9 width=203><INPUT name=URL size=20
tabIndex=6 value=http://></TD>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=9 width=96><FONT
color=#000000>你的图标地址：</FONT></TD>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=9 width=197><INPUT name=logo size=20
tabIndex=6 value=http://> <FONT color=#0080ff>88x31</FONT> </TD></TR>    
<TR align=middle>    
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff    
borderColorLight=#000000 height=8 width=98><FONT    
color=#000000>你的密码：</FONT></TD>    
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff    
borderColorLight=#000000 height=8 width=203><FONT color=#0080ff><INPUT    
maxLength=8 name=psd size=20 tabIndex=3> 长度1-8</FONT></TD>    
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff    
borderColorLight=#000000 height=8 width=96><FONT    
color=#000000>网站分类：</FONT></TD>    
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff    
borderColorLight=#000000 height=8 width=197>&nbsp;<select name=wzfl size=1 tabIndex=7>    
<option selected value=国家地区>国家地区</option>
<option value=电脑网络>电脑网络</option>
<option value=休闲娱乐>休闲娱乐</option>
<option value=生活资讯>生活资讯</option>
<option value=人文艺术>人文艺术</option>
<option value=文化教育>文化教育</option>
<option value=自然科学>自然科学</option>
<option value=社会文化>社会文化</option>
<option value=医药保健>医药保健</option>
<option value=工商产业>工商产业</option>
<option value=金融投资>金融投资</option>
<option value=谈天说地>谈天说地</option>
<option value=情感天地>情感天地</option>
<option value=游戏世界>游戏世界</option>
<option value=体育竞技>体育竞技</option>
<option value=新闻时事>新闻时事</option>
<option value=美眉天地>美眉天地</option>
<option value=其他类别>其他类别</option>
</select> </TD></TR>
<TR align=middle>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 vAlign=top width=97>　
<P><FONT color=#000000>网站介绍：</FONT></P></TD>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 colSpan=3 width=508><TEXTAREA cols=70 name=comments rows=5 200 tabIndex=9></TEXTAREA>
</TD></TR>
<TR align=middle>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 colSpan=4 height=42 width=605>
<DIV align=center>
<CENTER>
<P><input type=submit value=提交 name=B1><input type=reset value=重写 name=B2></P></CENTER></DIV></TD></TR></TBODY></TABLE></CENTER></DIV></FORM>
<P align=center>免费$cginame服务由<font color=#cc0033></font><font color=#ff6633><b> <a href=$zyurl>$zynames</a> </b></font><font color=#cc0033></font>提供　<FONT color=#000000>程序制作 </FONT><a href=http://www.yuzi.net target=_blank><b>Yuzi工作室</b></a>  
</P>  
</BODY></HTML>
EOF
exit;
}
##########
sub send_html {
if ($has_send ne "1") {
print "Content-type: text/html\n\n";
$has_send = "1";
}
}
##########
sub del {
if($psd ne $rpassword){&errorview("您的输入的密码错误，请重新输入！");exit;}
$delindex=$FORM{'delindex'};
open (GUEST,"$yuzibook") ||die $!;
@lines=<GUEST>;
close(GUEST);
open (GUEST,">$yuzibook") || die $!;
foreach $usersays (@lines) {
$usersays=~ s/\n//g;
if($usersays  ne ""){
($index)=split(/\t/,$usersays);
if($delindex ne $index){
print GUEST "$usersays\n";
}
}
}
close(GUEST);
unlink("$filepath/data/$id/$delindex"); 
&show;
}
##########
sub win{
&send_html;
print <<EOF;
<html>
<head>
<title>
发 送 成 功 !
</title>
<style>
<!--
{font-size: 12px;}
p {font-size:12px;}
a { text-decoration: none; color: rgb(40,40,180) }
a:hover {color:#FF9900;text-decoration:none}
table {font-size:12px;}
td {font-size:12px;}
-->
</style>
<meta HTTP-EQUIV="REFRESH" CONTENT=2;URL=link.cgi?id=$id>
</head>
<body>
<CENTER>
<br><br><br>
<table width=335 cellspacing=1 cellpadding=5>
<tr><td width=100% bgcolor=#ffffff align=center>
<span style="font-size: 10.5pt;line-height: 13pt">- 发 送 成 功 ! -</span><BR>
<tr><td align=center><a href="link.cgi?id=$id">[ 回 $rtitle ]</a>&nbsp;&nbsp;&nbsp;<a href="$rhome">[ 回 到 主 页 ]</a></td></tr>
</td></tr>
</table>
2秒钟后自动返回......
<br><br><br>
</body></html>
EOF
exit;
}
##########
sub errorview
{
print "Content-type: text/html\n\n";
print "<html><head></head><body><script>alert('$_[0]');history.back();</script></body></html>";
}
##########
sub dj{
open(PSD,"$filepath/data/$id/$dj")|| die $!;
@lines=<PSD>;
close(PSD);
open(PSD,">$filepath/data/$id/$dj")|| die $!;
foreach $line (@lines) {
if($line ne ""){
($rd_name,$rd_psd,$rd_mail,$rd_url,$rd_msg,$rd_ip,$rd_time,$wzfl,$rd_logo,$dj)=split(/\t/,$line);
$dj=$dj+1;
print PSD $rd_name."\t".$rd_psd."\t".$rd_mail."\t".$rd_url."\t".$rd_msg."\t".$rd_ip."\t".$rd_time."\t".$wzfl."\t".$rd_logo."\t".$dj;
}
}
close(PSD);
print "Location: $rd_url\n\n";
exit;
}
##########
sub find{
open(GUEST,"$yuzibook")||die $!;
@lines=<GUEST>;
close(GUEST);
$qbs=@lines;
$size=0;
foreach  $line (@lines){
if ($line ne "") {
($index) = split(/\t/,$line);
open(PSD,"$filepath/data/$id/$index")|| die $!;
@lines1=<PSD>;
close(PSD);
foreach $line1 (@lines1) {
$line1=~ s/\n//g;
($rd_name,$rd_psd,$rd_mail,$rd_url,$rd_msg,$rd_ip,$rd_time,$wzfl,$rd_logo,$dj)=split(/\t/,$line1);
}
if (($rd_name =~ /$search/gi)||($rd_msg =~ /$search/gi)||($wzfl =~ /$search/gi)){
$size=$size+1;
}
}
}
$ii=0;
$j=$size;
while ($j>0) {
$j=$j-$perpage;
$ii++;
}
if($page eq ""){$page=1;}
$pages=$page-1;
$pages=$page*$perpage-$perpage;
&send_html;
print <<EOF;
<html>
<head>
<style>
<!--
{font-size: 12px;}
p {font-size:12px;}
a { text-decoration: none; color: rgb(40,40,180) }
a:hover {color:#FF9900;text-decoration:none}
table {font-size:12px;}
td {font-size:12px;}
-->
</style>
<SCRIPT language=JavaScript>
<!-- Begin
function formHandler()
{
var URL = document.form.wzfl.options[document.form.wzfl.selectedIndex].value;
window.location.href = URL;
// End -->
}
</SCRIPT>
</head>
<title>$rtitle</title>
$htmlt
<table width=88% border=0 cellpadding=0 cellspacing=0 align=center>
<tr>
<td>
<div align=center><img src=$imagurl/title.gif></div>
</td>
</tr>
<tr>
<td>
<table width=100% border=0 cellspacing=0 cellpadding=0>
<tr>
<td align=center>
<a href=$yuzicgi?id=$id&a_method=write><img border=0 src=$imagurl/write.gif alt=友情登陆></a><a href=$yuzicgi?id=$id&a_method=xiu><img border=0 src=$imagurl/modi.gif alt=友情修改></a><img src=$imagurl/admin.gif alt=版主管理><a href=$rhome><img src=$imagurl/home.gif alt=返回主页 border=0></a><a href=reg.cgi><img border=0 src=$imagurl/reg.gif alt=免费申请></a>
</td>
<td width=55% class=unnamed1 align=center>
<p><span class=unnamed1>$rtitle</span></p>
</td>
<td width=25% align=right>
<span class=unnamed1>共 <font color=#0099CC>$qbs</font> 个网站加入友情链接</span>
</td>
</tr>
</table>
</td>
</tr>
</table>
<tr valign=top>
<td height=12>
<table width=88% border=0 cellspacing=1 cellpadding=0 align=center background=$imagurl/pattn3.gif>
<tr>
<td height=25>
<div align=center class=unnamed1>
<FORM name=form>网站分类：<select name=wzfl onchange=formHandler() size=1>
<option selected value=$yuzicgi?id=$id>选择分类</option>
<option value=$yuzicgi?id=$id>所有类别</option>
<option value=$yuzicgi?id=$id&a_method=find&search=国家地区>国家地区</option>
<option value=$yuzicgi?id=$id&a_method=find&search=电脑网络>电脑网络</option>
<option value=$yuzicgi?id=$id&a_method=find&search=休闲娱乐>休闲娱乐</option>
<option value=$yuzicgi?id=$id&a_method=find&search=生活资讯>生活资讯</option>
<option value=$yuzicgi?id=$id&a_method=find&search=人文艺术>人文艺术</option>
<option value=$yuzicgi?id=$id&a_method=find&search=文化教育>文化教育</option>
<option value=$yuzicgi?id=$id&a_method=find&search=自然科学>自然科学</option>
<option value=$yuzicgi?id=$id&a_method=find&search=社会文化>社会文化</option>
<option value=$yuzicgi?id=$id&a_method=find&search=医药保健>医药保健</option>
<option value=$yuzicgi?id=$id&a_method=find&search=工商产业>工商产业</option>
<option value=$yuzicgi?id=$id&a_method=find&search=金融投资>金融投资</option>
<option value=$yuzicgi?id=$id&a_method=find&search=谈天说地>谈天说地</option>
<option value=$yuzicgi?id=$id&a_method=find&search=情感天地>情感天地</option>
<option value=$yuzicgi?id=$id&a_method=find&search=游戏世界>游戏世界</option>
<option value=$yuzicgi?id=$id&a_method=find&search=体育竞技>体育竞技</option>
<option value=$yuzicgi?id=$id&a_method=find&search=新闻时事>新闻时事</option>
<option value=$yuzicgi?id=$id&a_method=find&search=美眉天地>美眉天地</option>
<option value=$yuzicgi?id=$id&a_method=find&search=其他类别>其他类别</option>
</select>
　　现在有 <font color=#0080C0>$size</font> 个网站加入了<font color=#0099CC>$search</font>类
</div>
</td>
</tr> </FORM>
</table>
</td>
</tr>
<br>
EOF
if($page eq ""){$page=1;}
$pages=$page-1;
#foreach $line (@lines){
$pages=$page*$perpage-$perpage;
for($i=$pages; $i<$pages+$perpage; $i++) {
$line=@lines[$i];
$line =~ s/\n//g;
if ($line ne "") {
($index) = split(/\t/,$line);
open(PSD,"$filepath/data/$id/$index")|| die $!;
@lines1=<PSD>;
close(PSD);
foreach $line1 (@lines1) {
$line1=~ s/\n//g;
($rd_name,$rd_psd,$rd_mail,$rd_url,$rd_msg,$rd_ip,$rd_time,$wzfl,$rd_logo,$dj)=split(/\t/,$line1);
}
if (($rd_name =~ /$search/gi)||($rd_msg =~ /$search/gi)||($wzfl =~ /$search/gi)){
if(($rd_logo eq "")||($rd_logo eq "http://")){$rd_logo="$imagurl/nobanner.gif";}
print <<EOF;
<tr>
<td>
<table width=80% border=0 cellspacing=1 cellpadding=0 align=center>
<tr bgcolor=#0088aa class=unnamed1>
<td width=14%>
<div align=center>
<font color=#E1F0FF><b>网站名称:</b></font>
</div>
</td>
<td width=36%>
<div align=center>
<font color=#E1F0FF><b>$rd_name</b></font>
</div>
</td>
<td width=20% bgcolor=#0088aa>
<div align=center>
<font color=#E1F0FF><b>$wzfl</b></font>
</div>
</td>
<td width=15%>
<div align=center>
<font color=#E1F0FF><b>$rd_time</b></font>
</div>
</td>
<td width=15%>
<div align=center>
<font color=#E1F0FF><b>点击 <strong>$dj</strong> 次</b></font>
</div>
</td>
</tr>
<tr>
<td rowspan=2 width=14% class=unnamed1><a href=$yuzicgi?id=$id&a_method=dj&dj=$index target=_blank><img border=0 height=31 width=88 src=$rd_logo></a></td>
<td colspan=4 class=unnamed1><font color=#000000>网站地址:</font>
<a href=$yuzicgi?id=$id&a_method=dj&dj=$index target=_blank><font color=#004fff>$rd_url</font></a>
EOF
if ($psd eq $rpassword){
print "　　　<a href=$cgiurl?a_method=del&delindex=$index&id=$id&psd=$psd>◎　删 除　◎</a>";
}
print<<EOF;
</td>
</tr>
<tr>
<td colspan=4 class=unnamed1><font color=#0080ff>$rd_msg</font></td>
</tr>
</table>
</td>
</tr>
<tr>
<td>　</td>
</tr>
EOF
}
}
}
print "</table><center><tr><td><table width=88% border=0 cellspacing=0 cellpadding=0 background=$imagurl/pattn3.gif><tr><td height=25><div align=center><font color=#0088aa class=unnamed1>\n";
$j=$size;
while ($j>0) {
print "<a href=$yuzicgi?a_method=find&page=$ii&id=$id&psd=$psd&search=$search>" if ($page != $ii);
print "[$ii]";
print "</a>" if ($page != $ii);
$j=$j-$perpage;
$ii--;
}
print <<EOF;
</font></div></td></tr></table></td></tr></table>
<form method=post action=$yuzicgi?id=$id>
<input type="hidden" name="psd" value=$psd>
<table width=210 cellspacing=1 bgcolor=#D8F3FE cellpadding=5>
<tr><td width=100% bgcolor=#ffffff align="center">
请输入您要搜索的字符<input type=hidden name=a_method value=find>
<input type=text name=search><input name=submit type=submit value=确定>
</td></tr>
</table>
</form>
EOF
print "$htmlw<br><td align=middle>免费$cginame服务由<font color=#cc0033></font><font color=#ff6633><b><font Helvetica, sans-serif> <a href=$zyurl>$zynames</a> </font></b></font><font color=#cc0033></font>提供　程序制作：<b><a href=http://www.yuzi.net target=_blank>Yuzi工作室</b></a></td></td>\n";
print "</body></html>\n";
exit;
}
##########
sub xiu{
&send_html;
if($username eq ""){
print <<EOF;

<HTML><HEAD><TITLE>【修改资料】</TITLE>
<META content=text/html; charset=gb2312 http-equiv=Content-Type>
<META content='Microsoft FrontPage 4.0' FrontPage 4.0 name=GENERATOR>
<STYLE>BODY {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; MARGIN-TOP: 0px
}
TABLE {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
INPUT {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
TEXTAREA {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
SELECT {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
A:link {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: none
}
A:visited {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: none
}
A:active {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: underline
}
A:hover {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: underline
}
.11f {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 10.5pt; LINE-HEIGHT: 12pt
}
</STYLE>
</HEAD>
<BODY link=#ffff00 text=#00ffff vLink=#ffff00>
<P align=center><FONT color=black><BR>修改网站资料</FONT></P>
<form action=$yuzicgi?id=$id method=post>
<input type=hidden name=a_method value=xiu>
<DIV align=center>
<CENTER>
<TABLE bgColor=#b2b2b2 border=1 borderColor=#ffffff borderColorDark=#ffffff 
borderColorLight=#000000 cellSpacing=0 width=617>
  <TBODY>
  <TR align=middle>
    <TD align=left bgColor=#FFEEEE borderColorDark=#ffffff 
    borderColorLight=#000000 width=98><FONT 
      color=#000000>你的网站名称：</FONT></TD>
    <TD align=left borderColorDark=#ffffff borderColorLight=#000000 
    width=205 bgColor="#FFEEEE"><INPUT maxLength=20 name=username size=20 tabIndex=2> 
      &nbsp;&nbsp;&nbsp; </TD>   
    <TD align=left bgColor=#FFEEEE borderColorDark=#ffffff    
    borderColorLight=#000000 width=91><FONT    
    color=#000000>你的密码：</FONT></TD>   
    <TD align=left borderColorDark=#ffffff borderColorLight=#000000    
    width=204 bgColor="#FFEEEE"><FONT color=#0080ff><INPUT maxLength=8 name=psd size=20    
      tabIndex=3 type=password></FONT></TD></TR>   
  <TR align=middle>   
    <TD align=left borderColorDark=#ffffff borderColorLight=#000000 colSpan=4 width=605 bgColor="#FFEEEE">   
      <P    
  align=center><INPUT tabIndex=10 type=submit value="   进入   "></P></TD></TR></TBODY></TABLE></DIV></CENTER></FORM> 
  <P align=center>免费$cginame服务由<font color=#cc0033></font><font color=#ff6633><b> <a href=$zyurl>$zynames</a> </b></font><font color=#cc0033></font>提供　<FONT color=#000000>程序制作 </FONT><a href=http://www.yuzi.net target=_blank><b>Yuzi工作室</b></a>   
</P>   
</BODY></HTML>
EOF
}else{
if ( -e "$filepath/data/$id/$username"){
open(PSD,"$filepath/data/$id/$username")|| die $!;
@lines=<PSD>;
close(PSD);
open(PSD,"$filepath/data/$id/$username")|| die $!;
foreach $line (@lines) {
if($line ne ""){
($rd_name,$rd_psd,$rd_mail,$rd_url,$rd_msg,$rd_ip,$rd_time,$wzfl,$rd_logo,$dj)=split(/\t/,$line);
}
}
close(PSD);
}else{&errorview("系统不存在此网站的资料！");exit;}
print <<EOF;
<HTML><HEAD><TITLE>【修改资料】</TITLE>
<META content=text/html; charset=gb2312 http-equiv=Content-Type>
<META content='Microsoft FrontPage 4.0' FrontPage 4.0 name=GENERATOR>
<STYLE>BODY {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; MARGIN-TOP: 0px
}
TABLE {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
INPUT {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
TEXTAREA {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
SELECT {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
A:link {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: none
}
A:visited {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: none
}
A:active {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: underline
}
A:hover {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: underline
}
.11f {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 10.5pt; LINE-HEIGHT: 12pt
}
</STYLE>
</HEAD>
<BODY link=#ffff00 text=#00ffff vLink=#ffff00>
<P align=center><FONT color=black><BR>修改网站资料</FONT></P>
<form action=$yuzicgi?id=$id method=post>
<input type=hidden name=a_method value=edit>
<input type="hidden" name="psd" value=$psd>
<input type="hidden" name="username" value=$username>
<DIV align=center>
<CENTER>
<TABLE bgColor=#c8c8c8 border=1 borderColor=#ffffff borderColorDark=#ffffff
borderColorLight=#000000 cellSpacing=0 width=617>
<TBODY>
<TR align=middle>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=9 width=98><FONT
color=#000000>你的图标地址：</FONT></TD>
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff
borderColorLight=#000000 height=9 width=203><INPUT name=logo size=25
tabIndex=6 value=$rd_logo> <FONT color=#0080ff>88x31</FONT> </TD>  
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff  
borderColorLight=#000000 height=9 width=96><FONT  
color=#000000>你的主页地址：</FONT></TD>  
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff  
borderColorLight=#000000 height=9 width=197><INPUT name=URL size=25  
tabIndex=6 value=$rd_url> </TD></TR>   
<TR align=middle>   
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff   
borderColorLight=#000000 vAlign=top width=97>　  
<P><FONT color=#000000>网站介绍：<BR></FONT></P></TD>  
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff  
borderColorLight=#000000 colSpan=3 width=508><TEXTAREA cols=70 name=comments rows=5 200 tabIndex=9>$rd_msg</TEXTAREA>  
</TD></TR>  
<TR align=middle>  
<TD align=left bgColor=#FFEEEE borderColorDark=#ffffff  
borderColorLight=#000000 colSpan=4 height=42 width=605>  
<DIV align=center>  
<CENTER>  
<P><input type=submit value=提交 name=B1><input type=reset value=重写 name=B2></P></CENTER></DIV></TD></TR></TBODY></TABLE></CENTER></DIV></FORM>  
 
  <P align=center>免费$cginame服务由<font color=#cc0033></font><font color=#ff6633><b> <a href=$zyurl>$zynames</a> </b></font><font color=#cc0033></font>提供　<FONT color=#000000>程序制作 </FONT><a href=http://www.yuzi.net target=_blank><b>Yuzi工作室</b></a>    
</P>    
</BODY></HTML>

EOF
}
exit;
}


##########
sub edit{
open(TITLES,"$filepath/data/$id/$username")|| die $!;
@hastitles=<TITLES>;
close(TITLES);
foreach $hastitles (@hastitles) {
$hastitles=~ s/\n//g;
($rd_name,$rd_psd,$rd_mail,$rd_url,$rd_msg,$rd_ip,$rd_time,$wzfl,$rd_logo,$dj)=split(/\t/,$hastitles);
}
if($psd ne $rd_psd){&errorview("您的输入的密码错误，请重新输入！");exit;}
open(TITLES,">$filepath/data/$id/$username")|| die $!;
@hastitles=<TITLES>;
print TITLES $rd_name."\t".$rd_psd."\t".$rd_mail."\t".$userurl."\t".$comments."\t".$rd_ip."\t".$rd_time."\t".$wzfl."\t".$logo."\t".$dj;
close(TITLES);
&win;
exit;
}
##########
sub bzgl{
&send_html;
print <<EOF;

<HTML><HEAD><TITLE>【版主管理】</TITLE>
<META content=text/html; charset=gb2312 http-equiv=Content-Type>
<META content='Microsoft FrontPage 4.0' FrontPage 4.0 name=GENERATOR>
<STYLE>BODY {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; MARGIN-TOP: 0px
}
TABLE {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
INPUT {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
TEXTAREA {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
SELECT {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt
}
A:link {
COLOR: black; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: none
}
A:visited {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: none
}
A:active {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: underline
}
A:hover {
COLOR: blue; FONT-FAMILY: 宋体, Arial; FONT-SIZE: 9pt; LINE-HEIGHT: 12pt; TEXT-DECORATION: underline
}
.11f {
FONT-FAMILY: 宋体, Arial; FONT-SIZE: 10.5pt; LINE-HEIGHT: 12pt
}
</STYLE>
</HEAD>
<BODY link=#ffff00 text=#00ffff vLink=#ffff00>
<P align=center><FONT color=black><BR></FONT><FONT   
    color=#000000>请输入版主的密码</FONT></P>
<form action=$yuzicgi?id=$id method=post>
<DIV align=center>
<CENTER>
<TABLE bgColor=#b2b2b2 border=1 borderColor=#ffffff borderColorDark=#ffffff 
borderColorLight=#000000 cellSpacing=0 width=617>
  <TBODY>
  <TR>
    <TD align=center bgColor=#FFEEEE width=611>
      <FONT color=#0080ff><INPUT maxLength=8 name=psd size=20   
      tabIndex=3 type=password></FONT></TD></TR>
  <TR align=middle>  
    <TD align=left borderColorDark=#ffffff borderColorLight=#000000 width=605 bgColor="#FFEEEE">  
      <P   
  align=center><INPUT tabIndex=10 type=submit value="   进入   "></P></TD></TR></TBODY></TABLE></DIV></CENTER></FORM><P align=center>免费$cginame服务由<font color=#cc0033></font><font color=#ff6633><b> <a href=$zyurl>$zynames</a> </b></font><font color=#cc0033></font>提供　<FONT color=#000000>程序制作 </FONT><a href=http://www.yuzi.net target=_blank><b>Yuzi工作室</b></a>  
</P>  
</BODY></HTML>
EOF
exit;
}
######################### END OF SCRIPT #########################
