#!/usr/bin/perl
#------------------------------------------------------#
#                 ������ΪYuzi�������ṩ               #
#              Yuzi��������2000���û���v1.20           #
#------------------------------------------------------#
require "setup.cgi";
######################
## ���²��ֲ����޸� ##
######################
$cgiurl  ="cjyh.cgi";
$perpage=20;
 if ($ENV{'REQUEST_METHOD'} eq "POST") {
  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
} else {
  $buffer = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
   ($name, $value) = split(/=/, $pair);
   $value =~ tr/+/ /;
   $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
   $value =~ s/<!--(.|\n)*-->//g;
   $value =~ s/\t//g;
   $FORM{$name} = $value;
}
$adm     = $FORM{'adm'};
$psd     = $FORM{'psd'};
$a_method= $FORM{'a_method'};
$selname = $FORM{'selname'};
$username= $FORM{'username'};
$page  = $FORM{'page'};
if(($admname ne $adm)||($delpsd ne $psd)){
&send_html;
print <<EOF;
<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style type="text/css">TD{FONT-SIZE:9pt}A{FONT-SIZE:9pt;TEXT-DECORATION:none}A:hover{FONT-SIZE:9pt;TEXT-DECORATION:underline}</style>
<style>input{font-size:9pt;color:#000080;background-color:#FFFFFF;padding-top:3px}<!--body,table a{text-decoration:none}a:hover{color:red;text-decoration:underline}--></style>
<title>�����û�����</title>
<script language="JavaScript">
function chksend(){
var send=false;
if(document.reg.adm.value){
if(document.reg.psd.value){
send=true;
}
}
if (send==false){
alert('վ�������ã�������룬лл��');
}
return send;
}

</script>
</head>
<body background=$imagurl/bg.jpg>

<br>
<h2 align="center">�����û�����</h2>
<div align="center"><center>
<form name="reg" action="$cgiurl" onsubmit="return chksend();">
  <table border="1" width="400">
    <tr>
      <td width="40%" align=center>�����û����֣�</td>
      <td width="60%"><input name="adm" type="text" size="30" maxlength="10"></td>
    </tr>
   <tr>
      <td width="40%" align=center>�����û����룺</td>
      <td width="60%"><input name="psd" type="password" size="30" maxlength="12"></td>
    </tr>
    <tr>
      <td><div align="center"><center><p><input type="reset" value="��   ��" name="B2"></td>
      <td align="center"><div align="center"><center><p><input type="submit" value="��   ��"
      name="B1"></td>
    </tr>
  </table>
</form>
<a href="reg.cgi">[�������]</a><a href="xiu.cgi">[���������޸�]</a>[�����û�����]<a href="list.cgi">[�û��б�]</a>
</a></center></div>
</body>
</html>
EOF
exit;
}

elsif($a_method eq "kills"){&kills;exit;}
elsif($a_method eq "ckbz"){&ckbz;exit;}
else{
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
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style type="text/css">
<!--
a:link {  font-family: "����", "serif"; font-size: 9pt; color: #004080; text-decoration: none}
a:hover {  color: #004080; text-decoration: underline; background-color: #CCCC99}
a:visited {  text-decoration: none}
body {  font-family: "����", "serif"; font-size: 9pt}
td {  font-family: "����", "serif"; font-size: 9pt}
input {  font-size: 9pt}
p {  font-size: 9pt}
br {  font-size: 9pt}
tr {  font-size: 9pt}
table {  font-size: 9pt}
-->
</style>
<body background=$imagurl/bg.jpg>
<title>�����û�����</title>
</head>
<br>
<center><h2>�����û�����</h2></center>
<center>
<form name="reg" action="$cgiurl">
�������������ƣ�<input type=text name="username" size=12>
<input type="hidden" name="adm" value="$adm">
<input type="hidden" name="psd" value="$psd">
<input name="a_method" type="hidden" value="ckbz">
<input type=submit value="ȷ��">
</form>
<br>������:<font color=#FF0000>$size</font>
<table border="1" width="80%" bordercolorlight="#008000" cellspacing="0" cellpadding="0" bordercolordark="#FFFFFF">
</tr>
<tr>
<td background=$imagurl/tablebg.gif width="45%" align="center"><font color=ffffff>$cginame����</font></td>
<td background=$imagurl/tablebg.gif width="10%" align="center"><font color=ffffff>������</font></td>
<td background=$imagurl/tablebg.gif width="10%" align="center"><font color=ffffff>����</font></td>
<td background=$imagurl/tablebg.gif width="20%" align="center"><font color=ffffff>����ʱ��</font></td>
<td background=$imagurl/tablebg.gif width="15%" align="center"><font color=ffffff>ɾ�����û�</font></td>
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
<td>��<a href=$yuzicgi?id=$rname target=_blank>$rtitle</a><br>$jianj</td>
<td align="center"><font color=#FF0000>$lys</font></td>
<td align="center"><a href="mailto:$rmail">$rname</a></td>
<td align="center">$zhtime</td>
<td align="center"><form action=$cgiurl METHOD=POST><input type=hidden name=selname value=$rname><input type=hidden name=adm value=$adm><input type=hidden name=psd value=$psd><input type=hidden name=a_method value=kills><input type=submit value=ɾ��></td>
</form>
</tr>
EOF
}
}
}
print <<EOF;
<tr>
<td align="center" width="100%" colspan="5" bgcolor="#FFF5E1">���$cginame������<font color=#cc0033>
</font><font color=#ff6633><b><font Helvetica, sans-serif><a href=$zyurl>$zynames</a></font></b></font><font color=#cc0033>
</font>�ṩ������������<b><a href="http://www.yuzi.net" target="_blank">Yuzi������</a></td></tr>
<tr>
<td colspan="5" align=center>
EOF
$j=$size;
while ($j>0) {
print "<a href=$cgiurl?adm=$adm&psd=$psd&page=$ii>" if ($page != $ii);
print "[$ii]";
print "</a>" if ($page != $ii);
$j=$j-$perpage;
$ii--;
}
print <<EOF;
</td>
</tr>
</table>




</center>
</body>
</html>
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
sub kills{
unlink("$filepath/list/$selname.cgi"); 
open(TITLES,"$list")|| die $!;
@hastitles=<TITLES>;
close(TITLES);
open(TITLES,">$list")|| die $!;
foreach $m (@hastitles){
$m=~ s/\n//g;
if($m ne ""){
($index)=split(/\t/,$m);
if($index ne $selname){
print TITLES $m."\n";
}
}
}
close(TITLES);
&send_html;
     print <<EOF;
<html><head>
</head>
<style type="text/css">TD{FONT-SIZE:9pt}A{FONT-SIZE:9pt;TEXT-DECORATION:none}A:hover{FONT-SIZE:9pt;TEXT-DECORATION:underline}</style>
<style>input{font-size:9pt;color:#000080;background-color:#FFFFFF;padding-top:3px}<!--body,table a{text-decoration:none}a:hover{color:red;text-decoration:underline}--></style>
<body background=$imagurl/bg.jpg>
<center>
<br><br>
<h2>�� �� �� �� ɾ �� ��</h2><br><br>
<p align=center><a href=$cgiurl?adm=$adm&psd=$psd>���ع����˵�</p></a>
</body></html>
EOF
exit;

}
##########
sub ckbz{
if ( -e "$filepath/list/$username.cgi"){
open(PSD,"$filepath/list/$username.cgi")||die $!;
@lines=<PSD>;
close(PSD);
foreach $line (@lines) {
$line=~ s/\n//g;
      ($rname,$rpass,$rmail,$rhome,$rtitle,$yhq,$rtime,$htmlt,$htmlw)=split(/\t/,$line);
}
&send_html;
   print "<HEAD>\n";
   print "<TITLE>�� �� �� �� $rname �� �� �� ��</TITLE>\n";
   print "</HEAD>\n";
   print "<style type=text/css>TD{FONT-SIZE:9pt}A{FONT-SIZE:9pt;TEXT-DECORATION:none}A:hover{FONT-SIZE:9pt;TEXT-DECORATION:underline}</style>\n";
   print "<body background=$imagurl/bg.jpg>\n";
   print "<br>\n";
   print "<p class=pt10 align=center><b>�� �� $rname �� �� �� ��</b><form action=$cgiurl METHOD=POST><input type=hidden name=selname value=$username><input type=hidden name=adm value=$adm><input type=hidden name=psd value=$psd><input type=hidden name=a_method value=kills><input type=submit value=ɾ��></form>\n";
   print "<p class=pt10 align=center>\n";
   print "<table cellspacing=4 cellpadding=3><tr><td class=pt9 bgcolor=#FFF5E1><b>$cginame���ƣ�</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000><a href=$yuzicgi?id=$rname target=_blank>$rtitle</font></tr>
<tr><td class=pt9 bgcolor=#FFF5E1><b>ע��������</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000>$rname</font></tr>
<tr><td class=pt9 bgcolor=#FFF5E1><b>���룺</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000>$rpass</font></tr>
<tr><td class=pt9 bgcolor=#FFF5E1><b>���䣺</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000><a href=mailto:$rmail>$rmail</a></font></tr>
<tr><td class=pt9 bgcolor=#FFF5E1><b>������ҳ��</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000><a href=$rhome target=_blank>$rhome</a></font>
<tr><td class=pt9 bgcolor=#FFF5E1><b>����ʱ�䣺</b><td class=pt9 align=left bgcolor=#FFF5E1><font color=#FF0000>$rtime.</font></table>\n";
   print "<br>[ <a href=javascript:history.back(-2)>������һҳ</a> ]<br><br>\n";
   print "<div align=center><center><table border=1 borderColorDark=#ffffff borderColorLight=#008000 cellPadding=0 cellSpacing=0 width=60%><tbody><tr><td align=middle width=100%>��ҳ�����CGI������£�������������<a href=http://www.yuzi.net target=_blank>Yuzi������</a>��</td></tr></tbody></table></center></div>\n";
   exit;
}else{
&errorview("�Բ��𣬴˰���û��ע�ᣡ");exit;
}
}
######################### END OF SCRIPT #########################