#!/usr/bin/perl
#------------------------------------------------------#
#                 本程序为Yuzi工作室提供               #
#              Yuzi友情连接2000多用户版v1.20           #
#------------------------------------------------------#
require "setup.cgi";
######################
## 以下部分不需修改 ##
######################
$perpage=20;
if ($ENV{'REQUEST_METHOD'} eq "POST") {
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}
else {
$buffer = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
($name, $value) = split(/=/, $pair);
$FORM{$name} = $value;
}
$page  =$FORM{'page'};
##########
open(PSD,"$filepath/data/list")|| die $!;
@lines=<PSD>;
close(PSD);
$size=@lines;
$ii=0;
$j=$size;
while ($j>0) {
$j=$j-$perpage;
$ii++;
}
&send_html;
print <<EOF;
<html>
<head>
<TITLE>用户列表</TITLE>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<body background="$imagurl/bg.jpg">
<style type="text/css">
<!--
a:link {  font-family: "宋体", "serif"; font-size: 9pt; color: #004080; text-decoration: none}
a:hover {  color: #004080; text-decoration: underline; background-color: #CCCC99}
a:visited {  text-decoration: none}
body {  font-family: "宋体", "serif"; font-size: 9pt}
td {  font-family: "宋体", "serif"; font-size: 9pt}
input {  font-size: 9pt}
p {  font-size: 9pt}
br {  font-size: 9pt}
tr {  font-size: 9pt}
table {  font-size: 9pt}
-->
</style>
</head>
<br>
<div align="center"><center>
<font color=#FF0000>>></font><a href=reg.cgi>免费申请</a><font color=#FF0000>>></font><a href=xiu.cgi>版主资料修改</a><font color=#FF0000>>></font><a href="cjyh.cgi">超级用户管理</a><font color=#FF0000>>></font>用户列表
<br>居民数:<font color=#FF0000>$size</font>
<table border="1" width="80%" bordercolorlight="#008000" cellspacing="0" cellpadding="0" bordercolordark="#FFFFFF">
</tr>
<tr>
<td background=$imagurl/tablebg.gif width="55%" align="center"><font color=ffffff>$cginame名称</font></td>
<td background=$imagurl/tablebg.gif width="10%" align="center"><font color=ffffff>连接数</font></td>
<td background=$imagurl/tablebg.gif width="15%" align="center"><font color=ffffff>版主</font></td>
<td background=$imagurl/tablebg.gif width="20%" align="center"><font color=ffffff>申请时间</font></td>

</tr>
EOF
if($page eq ""){$page=$ii;}
$pages=$page-1;
$pages=$page*$perpage-$perpage;
for($i=$pages; $i<$pages+$perpage; $i++) {
$line=@lines[$i];
$line=~ s/\n//g;
if ($line ne "") {
($username)=split(/\t/,$line);
unless(-f "$filepath/list/$username.cgi"){
open(TMP,">$filepath/list/$username.cgi");
close(TMP);
chmod(0666,"$filepath/list/$username.cgi");
}
open(PSD1,"$filepath/list/$username.cgi")|| die $!;
@lines1=<PSD1>;
close(PSD1);
foreach $line1 (@lines1) {
$line1=~ s/\n//g;
($rname,$rpassword,$rmail,$rhome,$rtitle,$jhq,$zhtime,$htmlt,$htmlw,$jianj)=split(/\t/,$line1);
unless(-f "$filepath/data/$username/$username.cgi"){
open(TMP,">$filepath/data/$username/$username.cgi");
close(TMP);
chmod(0666,"$filepath/data/$username/$username.cgi");
}
open(PSD2,"$filepath/data/$username/$username.cgi")|| die $!;
@lines2=<PSD2>;
close(PSD2);
$lys=@lines2;
print <<EOF;
<tr>
<td>　<a href=$yuzicgi?id=$rname target=_blank>$rtitle</a><br>$jianj</td>
<td align="center"><font color=#FF0000>$lys</font></td>
<td align="center"><a href="mailto:$rmail">$rname</a></td>
<td align="center">$zhtime</td>
</tr>
EOF
}
}
}
print <<EOF;
<tr>
<td align="center" width="100%" colspan="5" bgcolor="#FFF5E1">免费$cginame服务由<font color=#cc0033>
</font><font color=#ff6633><b><font Helvetica, sans-serif><a href=$zyurl>$zynames</a></font></b></font><font color=#cc0033>
</font>提供　程序制作：<b><a href="http://www.yuzi.net" target="_blank">Yuzi工作室</a></td></tr>
<tr>
<td colspan="5" align=center>
EOF
$j=$size;
while ($j>0) {
print "<a href=$cgiurl?page=$ii>" if ($page != $ii);
print "[$ii]";
print "</a>" if ($page != $ii);
$j=$j-$perpage;
$ii--;
}
print <<EOF;
</td>
</tr>
</table>
</center></div>
</body>
</html>
EOF
exit;
##########
sub send_html {
if ($has_send ne "1") {
print "Content-type: text/html\n\n";
$has_send = "1";
}
}
######################### END OF SCRIPT #########################
