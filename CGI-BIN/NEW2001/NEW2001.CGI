#!/usr/bin/perl
########################################################
#            ������ΪYuzi������ ��֮�� �ṩ              #
#        Yuzi ����С��+վ��С�� 2001���û���v1.2         #
#                                                      #
#     �������Ȩ��Yuzi������ ��֮�� ���У��κ���          #
#     �Կ�����ʹ�ñ������ڷ���ҵ��;����ҵ��;��          #
#     �븶�������500Ԫ��                               #
#                                                      #
#                    лл��ʹ�ñ����򡡡���֮��          #
#                    E-mail: webmaster@popcgi.com      #
#                    http://www.yuzi.net	              #
#                                                      #
#     ������Ϊ��ѳ���������ʹ�ñ����򣬵�����          #
#     ����Yuzi������(http://www.yuzi.net)�����ӣ�       #
########################################################
require "setup.cgi";
############### ���������벻Ҫ����޸� ##################

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
$value =~ s/<!--(.|\n)*-->//g;
$value =~ s/>/&gt;/g;
$value =~ s/</&lt;/g;
$FORM{$name} = $value;
push (@DELETE, $value) if ($name eq "DEL");
}
####################################
$username=$FORM{'username'};
$userpass=$FORM{'userpass'};
$newid=$FORM{'newid'};
$ID=$FORM{'ID'};
$page_num=$FORM{'page_num'};
$Action=$FORM{'Action'};
if ($Action eq ""){&main;exit;}
if ($Action eq "login"){&login;exit;}
if ($Action eq "admin"){&admin;exit;}
if ($Action eq "show"){&show;exit;}
if ($Action eq "newpost"){&newpost;exit;}
if ($Action eq "donewpost"){&donewpost;exit;}
if ($Action eq "shownew"){&shownew;exit;}
if ($Action eq "editpost"){&editpost;exit;}
if ($Action eq "doeditpost"){&doeditpost;exit;}
if ($Action eq "delpost"){&delpost;exit;}
if ($Action eq "dodelpost"){&dodelpost;exit;}
if ($Action eq "makecode"){&makecode;exit;}
if ($Action eq "makejscode"){&makejscode;exit;}
if ($Action eq "js"){&js;exit;}
if ($Action eq "reg"){&reg;exit;}
if ($Action eq "doreg"){&doreg;exit;}
&main;
exit;

sub main {
print "Content-type: text/html\n\n";
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>��½ҳ��</title>

<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:$fontcolor}
-->
</style>
</head>
<body bgColor=$bgcolor>
<br>
<br>
<br>
<br>
<form action="$cgi_url" method="post">
<input type="hidden" name="Action" value="login">
<div align="center"><center><table
  cellSpacing="2" width="205" border="0">
    <tr bgColor="#ccccff" align="center">
      <td width="197" align="center" bgcolor="$TBcolor"><a href=$cgi_url?Action=reg>��Ҫ����</a><br><font size="2">�û���:</font> <input
      size="15" name="username"><br>
      <font size="2">��<font color="#ccccff">��</font>��:</font> <input type="password"
      size="15" value name="userpass"><br>
      <font size="2"><input type="submit" value=" �� �� " name="Submit"  style='background-color: rgb(255,255,255)'>��<input type="reset"
      value=" ȡ �� " name="Submit"  style='background-color: rgb(255,255,255)'></font></td>
    </tr>
  </table>
  </center></div>
</form>
<br>
<center>
<hr width=300 size=1>
<table width=90% align=center cellpadding=0 cellspacing=0 style='font-size: 9pt'>
<tr>
<td align=center valign=middle>
<font color=$fontcolor1>��ѷ�����
</font><font color=#ff6633><b><a href=$net_url>$net_name</a></b></font><font color=$fontcolor1>
�ṩ</font><br>
<font color=$fontcolor1>&copy;��Ȩ����:<a href=http://www.yuzi.net>YUZI������ ��֮��</a></font>
</td>
</tr>
</table>
</center>
</body></html>
EOF
exit;
}

sub errorview {
print "Content-type: text/html\n\n";
print "<meta http-equiv=Content-Type content=text/html; charset=gb2312>\n";
if ($_[1] ne ""){print "<META HTTP-EQUIV=Refresh CONTENT=2;URL=\"$_[1]\">\n";}
print "<html><head><title>����ҳ��</title>\n";
print "<style type=text/css>\n";
print "<!--\n";
print "A:link    {text-decoration:none;color:$linkcolor}\n";
print "A:active  {TEXT-DECORATION:none;color:$bgcolor}\n";
print "A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}\n";
print "A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}\n";
print "p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:$fontcolor}\n";
print "-->\n";
print "</style>\n";
print "</head><body bgColor=$bgcolor>\n";
if ($_[1] eq ""){print "<script>alert('$_[0]');history.back();</script>\n";}
if ($_[1] ne ""){print "<br><br><br><p align=center>$_[0]<br><br><input size=40 value=\"����ҳ�棡2����Զ����ص���½ҳ��\"></p>\n";}
print "</body></html>\n";
}

sub com124{ 
@com_list = @_;
foreach $list(@com_list){
$FORM{$list} =~ s/\|/&#124;/g;
}
}

sub DSCode {
my $ThePost = shift;
$ThePost =~ s/(^|\s)(http:\/\/\S+)\b/ <A HREF="$2" TARGET=_blank>$2<\/A> /isg;
$ThePost =~ s/(^|\s)(www\.\S+)\b/ <A HREF="http:\/\/$2" TARGET=_blank>$2<\/A> /isg;
$ThePost =~ s/(\[URL\])(http|https|ftp)(:\/\/\S+?)(\[\/URL\])/ <A HREF="$2$3" TARGET=_blank>$2$3<\/A> /isg;
$ThePost =~ s/(\[URL\])(\S+?)(\[\/URL\])/ <A HREF="http:\/\/$2" TARGET=_blank>$2<\/A> /isg;
$ThePost =~ s/(\[URL=)(http|https|ftp)(:\/\/\S+?)(])(.+?)(\[\/URL\])/<A HREF="$2$3" TARGET=_blank>$5<\/A>/isg;
$ThePost =~ s/(\[URL=)(\S+?)(])(.+?)(\[\/URL\])/<A HREF="http:\/\/$2" TARGET=_blank>$4<\/A>/isg;
$ThePost =~ s/(\[EMAIL\])(\S+\@\S+?)(\[\/EMAIL\])/ <A HREF="mailto:$2">$2<\/A> /isg;
$ThePost =~ s/(\[IMG\])(\S+?)(\[\/IMG\])/ <IMG SRC="$2" border=0> /isg;
$ThePost =~ s/(\[JS\])(.+?)(\[\/JS\])/<script language=\"javascript1.2\" src=\"$2\"><\/script>/isg;
$ThePost =~ s/(\[br\])/<br>/isg;
$ThePost =~ s/(\[i\])(.+?)(\[\/i\])/<i>$2<\/i>/isg;
$ThePost =~ s/(\[b\])(.+?)(\[\/b\])/<b>$2<\/b>/isg;
$ThePost =~ s/(\[u\])(.+?)(\[\/u\])/<u>$2<\/u>/isg;
$ThePost =~ s/(\[color=red\])(\S+?)(\[\/color\])/<font color=red>$2<\/font>/isg;
$ThePost =~ s/(\[color=Black\])(\S+?)(\[\/color\])/<font color=Black>$2<\/font>/isg;
$ThePost =~ s/(\[color=Silver\])(\S+?)(\[\/color\])/<font color=Silver>$2<\/font>/isg;
$ThePost =~ s/(\[color=Gray\])(\S+?)(\[\/color\])/<font color=Gray>$2<\/font>/isg;
$ThePost =~ s/(\[color=pink\])(\S+?)(\[\/color\])/<font color=pink>$2<\/font>/isg;
$ThePost =~ s/(\[color=Maroon\])(\S+?)(\[\/color\])/<font color=Maroon>$2<\/font>/isg;
$ThePost =~ s/(\[color=Purple\])(\S+?)(\[\/color\])/<font color=Purple>$2<\/font>/isg;
$ThePost =~ s/(\[color=Fuchsia\])(\S+?)(\[\/color\])/<font color=Fuchsia>$2<\/font>/isg;
$ThePost =~ s/(\[color=Green\])(\S+?)(\[\/color\])/<font color=Green>$2<\/font>/isg;
$ThePost =~ s/(\[color=Lime\])(\S+?)(\[\/color\])/<font color=Lime>$2<\/font>/isg;
$ThePost =~ s/(\[color=Olive\])(\S+?)(\[\/color\])/<font color=Olive>$2<\/font>/isg;
$ThePost =~ s/(\[color=Yellow\])(\S+?)(\[\/color\])/<font color=Yellow>$2<\/font>/isg;
$ThePost =~ s/(\[color=Navy\])(\S+?)(\[\/color\])/<font color=Navy>$2<\/font>/isg;
$ThePost =~ s/(\[color=Blue\])(\S+?)(\[\/color\])/<font color=Blue>$2<\/font>/isg;
$ThePost =~ s/(\[color=Teal\])(\S+?)(\[\/color\])/<font color=Teal>$2<\/font>/isg;
$ThePost =~ s/(\[color=Aqua\])(\S+?)(\[\/color\])/<font color=Aqua>$2<\/font>/isg;
$ThePost =~ s/(\[color=orange\])(\S+?)(\[\/color\])/<font color=orange>$2<\/font>/isg;
$ThePost =~ s/(\[color=brown\])(\S+?)(\[\/color\])/<font color=brown>$2<\/font>/isg;
$ThePost =~ s/(\[color=navy\])(\S+?)(\[\/color\])/<font color=navy>$2<\/font>/isg;
return ($ThePost);
}

sub get_date {
($sec,$min,$hour,$day,$mon,$year) =localtime(time+(3600*$time_hour));
if ($sec < 10)  { $sec = "0$sec";   }
if ($min < 10)  { $min = "0$min";   }
if ($hour < 10) { $hour = "0$hour"; }
if ($day < 10) { $day = "0$day"; }
if ($mon < 10)  { $mon = "0$mon";  }
$month = ($mon + 1);
if ($month < 10)  { $month = "0$month";  }
if($year < 2000){
if($year >= 100){$year=($year-100)+2000;}
else{$year=2000+$year;}
}
}

sub read_session {
if ($ID eq ""){&errorview("��û����ȷ��SESSION��","$cgi_url?Action=main");exit;}
open(RFILE,"$session_dir/$ID.cgi");
@session_list=<RFILE>;
close(RFILE);
@session_data=split(/\|/,$session_list[0]);
}

sub check_time {
($sec,$min,$hour,$day,$mon,$year) =localtime(time+(3600*$time_hour));
$month=($mon + 1); 
if ($ID eq ""){&errorview("��û�е�½����ҳ��","$cgi_url?Action=main");exit;}
&read_session;
if ($session_data[4] ne "$year$mon$day"){&errorview("�Բ���SESSION�Ѿ�������,��ȷ���������!","$cgi_url?Action=main");exit;}
$mytime=$hour*3600+$min*60+$sec;
$session_data[5]=$session_data[5]+$time_out*60;
if ($session_data[5] < $mytime){&errorview("�Բ���ʱ���Ѿ������ˣ������µ�½,��ȷ���������!","$cgi_url?Action=main");exit;}
if ($session_data[6] ne $ENV{'REMOTE_ADDR'}){&errorview("�Բ������IP�����½ʱ��IP��ͬ,�����µ�½!","$cgi_url?Action=main");exit;}
}

sub login {
if ($username eq "" || $userpass eq ""){&errorview("�û���������û����д");exit;}
open(TEMP,"$filepath/user/userdata.cgi");
@USERDATA=<TEMP>;
close(TEMP);
$check=0;
foreach $USERDATA (@USERDATA) {
($T0,$T1,$T2,$T3,$T4,$T5,$T6,$T7,$T8,$T9,$T10,$T11,$T12,$T13,$T14,$T15,$T16,$T17,$T18)=split(/\|/,$USERDATA);
if ($username eq $T0){$check=1;if ($userpass ne $T1){&errorview("�������");exit;}}
}
if ($check==0){&errorview("���ݿ���û�и��û�����");exit;}
($sec,$min,$hour,$day,$mon,$year) =localtime(time+(3600*$time_hour));
$month=($mon + 1);
$login_date="$year$mon$day";
$login_time=$hour*3600+$min*60+$sec;
$login_ip=$ENV{'REMOTE_ADDR'};

open(WFILE,">$session_dir/$username.cgi");
print WFILE "|$username|$userpass|$username|$login_date|$login_time|$login_ip|||||\n";
close(WFILE);
chmod(0777,"$session_dir/$username.cgi");

print "Content-type: text/html\n\n";
print <<EOF;
<meta http-equiv=Content-Type content=text/html; charset=gb2312>
<META HTTP-EQUIV=Refresh CONTENT=2;URL="$cgi_url?Action=admin&ID=$username">
<html><head><title>��½�ɹ�</title>
<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:$fontcolor}
-->
</style>
</head><body bgColor=$bgcolor>
<br>
<br>
<br>
<br>
<p align="center"><input size="40" value="��½�ɹ���2����Զ����ص�����ҳ��"></p>
</body></html>
EOF
exit;
}

sub admin {
&check_time;
open(RFILE,"$data_dir/$ID.cgi");
@NEW_LIST=<RFILE>;
close(RFILE);
$LONG=@NEW_LIST;
print "Content-type: text/html\n\n";
print "<html>\n";
print "<head>\n";
print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=gb2312\">\n";
print "<title>����ҳ��</title>\n";
print "<style type=text/css>\n";
print "<!--\n";
print "A:link    {text-decoration:none;;color:$linkcolor}\n";
print "A:active  {TEXT-DECORATION:none;color:$bgcolor}\n";
print "A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}\n";
print "A:hover   {TEXT-DECORATION:underline overline ;color:$Hlinkcolor}\n";
print "p,br,body,td,select,input,form,textarea,option {font-size:9pt;font-family:����;}\n";
print ".toptable     {font-size:9pt;font-family:����;background-color:$fontcolor;color:$fontcolor;}\n";
print ".toptable1    {font-size:9pt;font-family:����;color:$fontcolor;}\n";
print ".n1           {background-color:$bgcolor;color:;}\n";
print "-->\n";
print "</style>\n";

print <<EOF;
<SCRIPT LANGUAGE="JavaScript">
function newin(width,height,url,name) {
msgWindow=window.open(url,name,'statusbar=no,scrollbars=yes,status=yes,resizable=yes,width='+width+',height='+height)
}
</SCRIPT>
EOF

print "</head>\n";
print "<body bgColor=$bgcolor>\n";
print "<table cellpadding=0 cellspacing=0 border=0 width=600 align=center>\n";
print "<tr>\n";
print "<td valign=middle><a href=$cgi_url?Action=newpost&ID=$ID><img src=$image_url/add.gif border=0>��Ӽ�¼</a></td>\n";
print "<td align=right valign=middle><a href=$cgi_url?Action=makecode&ID=$ID><img src=$image_url/code.gif border=0>����HTML</a> <a href=$cgi_url?Action=makejscode&ID=$ID><img src=$image_url/code.gif border=0>����JS����</a></td>\n";
print "</tr>\n";
print "</table>\n";
print "<form method='POST' action='$cgi_url'>\n";
print "<input type=hidden name='Action' value='dodelpost'>\n";
print "<input type=hidden name='ID' value='$ID'>\n";
print "<table cellpadding=0 cellspacing=0 border=0 width=600 bgcolor=$fontcolor align=center>\n";
print "<tr>\n";
print "<td height=1></td>\n";
print "</tr>\n";
print "</table>\n";
print "<table bgcolor=$TBcolor cellpadding=0 cellspacing=0 border=0 width=600 align=center>\n";
print "<tr class=toptable1>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=center width=30>ѡ��</td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=center width=250>����</td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=center width=40>�´���</td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=center width=120>����ʱ��</td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=center width=154>����</td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "</tr>\n";
print "</table>\n";
print "<table cellpadding=0 cellspacing=0 border=0 width=600 bgcolor=$fontcolor align=center>\n";
print "<tr>\n";
print "<td height=1></td>\n";
print "</tr>\n";
print "</table>\n";

if($page_num eq "" || $page_num==1){
$page_num==1;
$start_page=0;
$end_page=19;
}else{
$start_page=($page_num-1)*20;
$end_page=$page_num*20-1;
}

for ($i=0;$i<$LONG;$i++){
($TEMP0,$TEMP1,$TEMP2,$TEMP3,$TEMP4,$TEMP5,$TEMP6,$TEMP7,$TEMP8,$TEMP9,$TEMP10)=split(/\|/,$NEW_LIST[$i]);
if ($i>=$start_page && $i<=$end_page){
if (length($TEMP2) >40){$TEMP2=substr($TEMP2,0,38);$TEMP2="$TEMP2..";}
print "<table bgcolor=$TBcolor cellpadding=0 cellspacing=0 border=0 width=600 align=center>\n";
print "<tr class=n1>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=center width=30><input type=checkbox name=DEL value=$TEMP1></td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=left width=250><a href=$cgi_url?Action=shownew&ID=$ID&newid=$TEMP1>$TEMP2</a></td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=center width=40><a href=\"JavaScript:newin(320,240,'$cgi_url?Action=shownew&ID=$ID&newid=$TEMP1','NEW')\"><img src=$image_url/newwin.gif border=0></a></td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=center width=120><font color=$datecolor>$TEMP4</font> <font color=$timecolor>[$TEMP5]</font></td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "<td align=center width=154> <a href=$cgi_url?Action=editpost&ID=$ID&newid=$TEMP1><img src=$image_url/edit.gif border=0>�༭</a>&nbsp;&nbsp;<a href=$cgi_url?Action=delpost&ID=$ID&newid=$TEMP1><img src=$image_url/del.gif border=0>ɾ��</a></td>\n";
print "<td bgcolor=$fontcolor valign=middle width=1 height=24></td>\n";
print "</tr>\n";
print "</table>\n";
print "<table cellpadding=0 cellspacing=0 border=0 width=600 bgcolor=$fontcolor align=center>\n";
print "<tr>\n";
print "<td height=1></td>\n";
print "</tr>\n";
print "</table>\n";
}
}
print "<table cellpadding=0 cellspacing=0 border=0 width=600 align=center>\n";
print "<tr>\n";
print "<td height=16></td>\n";
print "</tr>\n";
print "</table>\n";

$total_page = int($LONG/20);
if($page_num<1 || $page_num eq ""){$page_num=1;}
if($page_num>$total_page){$page_num=$total_page;}
if (($total_page*20)<$LONG){$total_page++;}	
$page=$page_num;
$term = 10;
$mycel="Action=admin";
$ID=$ID;
print "<table cellpadding=0 cellspacing=0 border=0 width=600 align=center>\n";
print "<tr>\n";
print "<td align=center>\n";
&makepage;
print "</td>\n";
print "</tr>\n";
print "</table>\n";

print "<table cellpadding=0 cellspacing=0 border=0 width=600 align=center>\n";
print "<tr>\n";
print "<td align=right>\n";
print "<input type=submit value=' ɾ �� ' style='background-color: rgb(255,255,255)'>\n";
print "</td>\n";
print "</tr>\n";
print "</table></form>\n";

print <<EOF;
<br>
<center>
<hr width=300 size=1>
<table width=90% align=center cellpadding=0 cellspacing=0 style='font-size: 9pt'>
<tr>
<td align=center valign=middle>
<font color=$fontcolor1>��ѷ�����
</font><font color=#ff6633><b><a href=$net_url>$net_name</a></b></font><font color=$fontcolor1>
�ṩ</font><br>
<font color=$fontcolor1>&copy;��Ȩ����:<a href=http://www.yuzi.net>YUZI������ ��֮��</a></font>
</td>
</tr>
</table>
</center>
</body></html>
EOF
exit;
}

sub newpost {
&check_time;
print "Content-type: text/html\n\n";
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>��Ӽ�¼</title>

<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:$fontcolor}
-->
</style>
</head>
<body bgColor=$bgcolor>
<form method="POST" action="$cgi_url" align="center">
<input type="hidden" name="Action" value="donewpost">
<input type="hidden" name="ID" value="$ID">
<table border="1" width="450" cellspacing="0" cellpadding="0" bgcolor="$TBcolor" align=center bordercolordark="$bgcolor"
bordercolorlight="$fontcolor" bordercolor="$bgcolor">
  <tr><td width="450" align="center" colspan="2"><b>��Ӽ�¼</b></td>
    </tr>
    <tr>
      <td width="110" align="center"><strong>��&nbsp; ��:</strong></td>
      <td width="340"><input type="text" name="T1" size="30" maxlength="30"><br>֧��[img][/img] [email][/email] [url][/url] [js][/js]����</td>
    </tr><tr>
      <td width="110" align="center"><strong>��&nbsp; ��:</strong></td>
      <td width="340"><textarea rows="8" name="T2" cols="50"></textarea></td>
    </tr><tr><td width="450" align="center" colspan="2"><input type="submit" value=" �� �� " style='background-color: rgb(255,255,255)'></td>
    </tr>
  </table>
</form>
<br>
<center>
<hr width=300 size=1>
<table width=90% align=center cellpadding=0 cellspacing=0 style='font-size: 9pt'>
<tr>
<td align=center valign=middle>
<font color=$fontcolor1>��ѷ�����
</font><font color=#ff6633><b><a href=$net_url>$net_name</a></b></font><font color=$fontcolor1>
�ṩ</font><br>
<font color=$fontcolor1>&copy;��Ȩ����:<a href=http://www.yuzi.net>YUZI������ ��֮��</a></font>
</td>
</tr>
</table>
</center>
</body></html>
EOF
exit;
}

sub donewpost {
&check_time;
if ($FORM{'T1'} eq "" || $FORM{'T2'} eq ""){&errorview("��������ݶ�����Ϊ��");exit;}

$FORM{'T1'}=~ s/&/&amp;/g;
$FORM{'T2'}=~ s/&/&amp;/g;
&com124('T1', 'T2');

$FORM{'T1'}=~ s/\r\n/\[br\]/g;
$FORM{'T1'}=~ s/</&lt;/g;
$FORM{'T1'}=~ s/>/&gt;/g;
$FORM{'T2'}=~ s/\r\n/\[br\]/g;
$FORM{'T2'}=~ s/</&lt;/g;
$FORM{'T2'}=~ s/>/&gt;/g;

&get_date;
$post_id="$year$month$day$hour$min$sec";

open(RFILE,"$data_dir/$ID.cgi");
@NEW_LIST=<RFILE>;
close(RFILE);

open(WFILE,">$data_dir/$ID.cgi");
print WFILE "|$post_id|$FORM{'T1'}|$FORM{'T2'}|$year-$month-$day|$hour:$min||||||\n";
print WFILE @NEW_LIST;
close(WFILE);
chmod(0777,"$data_dir/$ID.cgi");

print "Content-type: text/html\n\n";
print <<EOF;
<meta http-equiv=Content-Type content=text/html; charset=gb2312>
<META HTTP-EQUIV=Refresh CONTENT=2;URL="$cgi_url?Action=admin&ID=$ID">
<html><head><title>��Ӽ�¼�ɹ�</title>
</head><body bgColor=$bgcolor>
<br>
<br>
<br>
<br>
<p align="center"><input size="40" value="��Ӽ�¼�ɹ���2����Զ����ص�����ҳ��"></p>
</body></html>
EOF
exit;
}

sub show {
&get_date;
open(RFILE,"$data_dir/$ID.cgi");
@NEW_LIST=<RFILE>;
close(RFILE);
$LONG=@NEW_LIST;
print "Content-type: text/html\n\n";
print <<EOF;
<meta http-equiv=Content-Type content=text/html; charset=gb2312>
<html><head><title>��ʾ�б�</title>
<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color: rgb(255,128,192)}
-->
</style>

<SCRIPT LANGUAGE="JavaScript">
function newin(width,height,url,name) {
msgWindow=window.open(url,name,'statusbar=no,scrollbars=yes,status=yes,resizable=yes,width='+width+',height='+height)
}
</SCRIPT>

</head><body bgColor=$bgcolor>
EOF
if($page_num eq "" || $page_num==1){
$page_num==1;
$start_page=0;
$end_page=9;
}else{
$start_page=($page_num-1)*10;
$end_page=$page_num*10-1;
}
print "<table border=0 width=340 cellspacing=0 cellpadding=0 style=\"font-size: 9pt\" bgcolor=$bgcolor>\n";
print "<tr>\n";
print "<td width=340 align=center colspan=2 height=18 valign=middle>\n";
#print "<A HREF=http://www.yuzi.net target=_blank><ACRONYM TITLE='�������:�������\n��Ȩ����:YUZI������ ��֮��\n����֧��:http://www.yuzi.net'>YUZI NEW2001 V1.2</ACRONYM></A> &nbsp;&nbsp;<b><font color=#FF8000>����С�� <font color=red>+</font> վ��С��</font></b>\n";
print "document.write(\"<A HREF=http:// target=_blank style='TEXT-DECORATION:none;color:$Vlinkcolor'><ACRONYM TITLE='ɱ����ּ:����Ϊ����ӮǮ�����������ǳɹ���\\nɱ�ֿ챨����ʱ�����������顣\\n��ӭ����:mailto:dax2000@yeah.net'>ɱ������</ACRONYM></A> &nbsp;&nbsp;<b><font color=#FF8000>����С�� <font color=red>+</font> վ��С��</font></b>\");\n";
print "&nbsp;&nbsp;<a href=$cgi_url target=_blank><img src=\"$image_url/key.gif\" width=18 height=13 border=0>�������</a></td>\n";
print "</tr>\n";
$ii=10;
for ($i=0;$i<$LONG;$i++){
($TEMP0,$TEMP1,$TEMP2,$TEMP3,$TEMP4,$TEMP5,$TEMP6,$TEMP7,$TEMP8,$TEMP9,$TEMP10)=split(/\|/,$NEW_LIST[$i]);
if ($i>=$start_page && $i<=$end_page){
if(length($TEMP2) >30){$TEMP2=substr($TEMP2,0,28);$TEMP2="$TEMP2..";}
print "<tr onmouseover=\"this.style.backgroundColor='$DBcolor'\" onmouseout=\"this.style.backgroundColor='$bgcolor'\">\n";
print "<td width=230 height=16><a href=\"JavaScript:newin(320,240,'$cgi_url?Action=shownew&ID=$ID&newid=$TEMP1','NEW')\"><img src=\"$image_url/win.gif\" border=0 width=16 height=16> $TEMP2</a>\n";
($T0,$T1,$T2)=split(/\-/,$TEMP4);
if (($T0 eq $year)&&($T1 eq $month)&&($T2 eq $day)){
print "<img src=\"$image_url/today.gif\" border=0 width=16 height=16>\n";
}
print "</td>\n";
print "<td width=110 height=16><font color=$datecolor>$TEMP4</font> <font color=$timecolor>[$TEMP5]</font></td>\n";
print "</tr>\n";
$ii=$ii-1;
}
}
for (1..$ii){
print "<tr onmouseover=\"this.style.backgroundColor='$DBcolor'\" onmouseout=\"this.style.backgroundColor='$bgcolor'\">\n";
print "<td width=340 colspan=2 height=16><img src=\"$image_url/no.gif\" border=0 width=16 height=16> û������</td>\n";
print "</tr>\n";
}
$total_page = int($LONG/10);
if($page_num<1 || $page_num eq ""){$page_num=1;}
if($page_num>$total_page){$page_num=$total_page;}
if (($total_page*10)<$LONG){$total_page++;}	
$page=$page_num;
$term = 5;
$mycel="Action=show";
print "<tr>\n";
print "<td width=340 colspan=2 align=center  height=16>\n";
&makepage;
print "</td>\n";
print "</tr>\n";
print "</table>\n";
exit;
}

sub makepage {
	$first = 1;
	$last = $term;
	while ($first <= $total_page) {
		if (($first <= $page) && ($page <= $last)) {
		$prevp = $first - 1;
			if ($prevp > 0) {
				print "[<a href=$cgi_url?$mycel&ID=$ID&page_num=$prevp>��ǰ��</a>].....";
			}
			else {
				print "[<font color=C0C0C0>��ǰ��</font>].....";
			}
		if ($last <= $total_page) {
			for ($pa = $first; $pa <= $last; $pa++) {
				if ($pa == $page) {
					print "[<a href=$cgi_url?$mycel&ID=$ID&page_num=$pa>$pa</a>] ";
				}
				else {
					print "[<a href=$cgi_url?$mycel&ID=$ID&page_num=$pa>$pa</a>] ";
				}
			}
		}
		else {
			for ($pa = $first; $pa <= $total_page; $pa++) {
				if ($pa == $page) {
					print "[<a href=$cgi_url?$mycel&ID=$ID&page_num=$pa>$pa</a>] ";
				}
				else {
					print "[<a href=$cgi_url?$mycel&ID=$ID&page_num=$pa>$pa</a>]  ";
				}
			}
		}
		$nextp = $last + 1;
		if ($nextp <= $total_page) {
			print ".....[<a href=$cgi_url?$mycel&ID=$ID&page_num=$nextp>���</a>]";
		}
		else {
			print ".....[<font color=C0C0C0>���</font>]";
		}
	}
	$first = $first + $term;
	$last = $last + $term;
	}
}

sub shownew {
open(RFILE,"$data_dir/$ID.cgi");
@NEW_LIST=<RFILE>;
close(RFILE);
$LONG=@NEW_LIST;
for ($i=0;$i<$LONG;$i++){
($TEMP0,$TEMP1,$TEMP2,$TEMP3,$TEMP4,$TEMP5,$TEMP6,$TEMP7,$TEMP8,$TEMP9,$TEMP10)=split(/\|/,$NEW_LIST[$i]);
if($newid eq $TEMP1){
($NTEMP0,$NTEMP1,$NTEMP2,$NTEMP3,$NTEMP4,$NTEMP5,$NTEMP6,$NTEMP7,$NTEMP8,$NTEMP9,$NTEMP10)=split(/\|/,$NEW_LIST[$i]);
}
}
$NTEMP3=&DSCode("$NTEMP3");
print "Content-type: text/html\n\n";
print <<EOF;
<meta http-equiv=Content-Type content=text/html; charset=gb2312>
<html><head><title>�� �� С ��</title>
<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:#555555}
-->
</style>
</head><body bgColor=$bgcolor>
<center>
<table width=280 align=center cellpadding=0 cellspacing=0>
<tr>
<td align=center valign=middle colspan=2><font size=5 color=#FF8040>�� �� С ��</font></td>
</tr>
<tr>
<td align=left valign=middle colspan=2>
<hr color=#0000FF width=280 size=1>
$NTEMP3
<hr color=#0000FF width=280 size=1>
</td>
</tr>
<tr>
<td align=LEFT valign=middle><font color=$timecolor>����ʱ��:</font><font color=$datecolor>$NTEMP4</font> <font color=$timecolor>[$NTEMP5]</font></td>
<td align=RIGHT valign=middle><a href='JavaScript:window.close();'><IMG SRC='$image_url/close.gif' border=0>�رմ���</a> </td>
</tr>
</table>
</center>
<br>
<center>
<hr width=200 size=1>
<table width=90% align=center cellpadding=0 cellspacing=0 style='font-size: 9pt'>
<tr>
<td align=center valign=middle>
<font color=$fontcolor1>��ѷ�����
</font><font color=#ff6633><b><a href=$net_url>$net_name</a></b></font><font color=$fontcolor1>
�ṩ</font><br>
<font color=$fontcolor1>&copy;��Ȩ����:<a href=http://www.yuzi.net>YUZI������ ��֮��</a></font>
</td>
</tr>
</table>
</center>
</body></html>
EOF
exit;
}

sub editpost {
&check_time;
if ($ID eq "" || $newid eq ""){&errorview("�ⲿ����");exit;}
open(RFILE,"$data_dir/$ID.cgi");
@NEW_LIST=<RFILE>;
close(RFILE);
$LONG=@NEW_LIST;
for ($i=0;$i<$LONG;$i++){
($TEMP0,$TEMP1,$TEMP2,$TEMP3,$TEMP4,$TEMP5,$TEMP6,$TEMP7,$TEMP8,$TEMP9,$TEMP10)=split(/\|/,$NEW_LIST[$i]);
if($newid eq $TEMP1){
($NTEMP0,$NTEMP1,$NTEMP2,$NTEMP3,$NTEMP4,$NTEMP5,$NTEMP6,$NTEMP7,$NTEMP8,$NTEMP9,$NTEMP10)=split(/\|/,$NEW_LIST[$i]);
}
}
$NTEMP3 =~ s/\[br\]/\r\t/g;
print "Content-type: text/html\n\n";
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>�޸ļ�¼</title>
<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:$fontcolor}
-->
</style>
</head>
<body bgColor=$bgcolor>
<form method="POST" action="$cgi_url" align="center">
<input type="hidden" name="Action" value="doeditpost">
<input type="hidden" name="newid" value="$NTEMP1">
<input type="hidden" name="ID" value="$ID">
<table border="1" width="450" cellspacing="0" cellpadding="0" bgcolor="$TBcolor" align=center bordercolordark="$bgcolor"
bordercolorlight="$fontcolor" bordercolor="$bgcolor">
   <tr><td width="450" align="center" colspan="2"><b>�޸ļ�¼</b></td>
    </tr>
    <tr>
      <td width="110" align="center"><strong>��&nbsp; ��:</strong></td>
      <td width="340"><input type="text" name="T1" size="30" maxlength="30" value=$NTEMP2></td>
    </tr><tr>
      <td width="110" align="center"><strong>��&nbsp; ��:</strong></td>
      <td width="340"><textarea rows="8" name="T2" cols="50">$NTEMP3</textarea></td>
    </tr><tr><td width="450" align="center" colspan="2"><input type="submit" value=" �� �� " style='background-color: rgb(255,255,255)'></td>
    </tr>
  </table>
</form>
<br>
<center>
<hr width=300 size=1>
<table width=90% align=center cellpadding=0 cellspacing=0 style='font-size: 9pt'>
<tr>
<td align=center valign=middle>
<font color=$fontcolor1>��ѷ�����
</font><font color=#ff6633><b><a href=$net_url>$net_name</a></b></font><font color=$fontcolor1>
�ṩ</font><br>
<font color=$fontcolor1>&copy;��Ȩ����:<a href=http://www.yuzi.net>YUZI������ ��֮��</a></font>
</td>
</tr>
</table>
</center>
</body></html>
EOF
exit;
}

sub doeditpost {
&check_time;
if ($FORM{'T1'} eq "" || $FORM{'T2'} eq ""){&errorview("��������ݶ�����Ϊ��");exit;}

$FORM{'T1'}=~ s/&/&amp;/g;
$FORM{'T2'}=~ s/&/&amp;/g;
&com124('T1', 'T2');

$FORM{'T1'}=~ s/\r\n/\[br\]/g;
$FORM{'T1'}=~ s/</&lt;/g;
$FORM{'T1'}=~ s/>/&gt;/g;
$FORM{'T2'}=~ s/\r\n/\[br\]/g;
$FORM{'T2'}=~ s/</&lt;/g;
$FORM{'T2'}=~ s/>/&gt;/g;

open(RFILE,"$data_dir/$ID.cgi");
@NEW_LIST=<RFILE>;
close(RFILE);
$LONG=@NEW_LIST;
open(WFILE,">$data_dir/$ID.cgi");
for ($i=0;$i<$LONG;$i++){
($TEMP0,$TEMP1,$TEMP2,$TEMP3,$TEMP4,$TEMP5,$TEMP6,$TEMP7,$TEMP8,$TEMP9,$TEMP10)=split(/\|/,$NEW_LIST[$i]);
if($newid eq $TEMP1){
($NTEMP0,$NTEMP1,$NTEMP2,$NTEMP3,$NTEMP4,$NTEMP5,$NTEMP6,$NTEMP7,$NTEMP8,$NTEMP9,$NTEMP10)=split(/\|/,$NEW_LIST[$i]);
print WFILE "$NTEMP0|$NTEMP1|$FORM{'T1'}|$FORM{'T2'}|$NTEMP4|$NTEMP5|$NTEMP6|$NTEMP7|$NTEMP8|$NTEMP9|$NTEMP10|\n";
}else{
print WFILE $NEW_LIST[$i];
}
}
close(WFILE);

print "Content-type: text/html\n\n";
print <<EOF;
<meta http-equiv=Content-Type content=text/html; charset=gb2312>
<META HTTP-EQUIV=Refresh CONTENT=2;URL="$cgi_url?Action=admin&ID=$ID">
<html><head><title>�޸ļ�¼�ɹ�</title>
<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:#555555}
-->
</style>
</head><body bgColor=$bgcolor>
<br>
<br>
<br>
<br>
<p align="center"><input size="40" value="�޸ļ�¼�ɹ���2����Զ����ص�����ҳ��"></p>
</body></html>
EOF
exit;
}

sub delpost {
&check_time;
open(RFILE,"$data_dir/$ID.cgi");
@NEW_LIST=<RFILE>;
close(RFILE);
$LONG=@NEW_LIST;
open(WFILE,">$data_dir/$ID.cgi");
for ($i=0;$i<$LONG;$i++){
($TEMP0,$TEMP1,$TEMP2,$TEMP3,$TEMP4,$TEMP5,$TEMP6,$TEMP7,$TEMP8,$TEMP9,$TEMP10)=split(/\|/,$NEW_LIST[$i]);
if($newid ne $TEMP1){
print WFILE $NEW_LIST[$i];
}
}
close(WFILE);
print "Content-type: text/html\n\n";
print <<EOF;
<meta http-equiv=Content-Type content=text/html; charset=gb2312>
<META HTTP-EQUIV=Refresh CONTENT=2;URL="$cgi_url?Action=admin&ID=$ID">
<html><head><title>ɾ�����</title>
<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:#555555}
-->
</style>
</head><body bgColor=$bgcolor>
<br>
<br>
<br>
<br>
<p align="center"><input size="40" value="ɾ����ɣ�2����Զ����ص�����ҳ��"></p>
</body></html>
EOF
exit;
}

sub dodelpost {
&check_time;
open(RFILE,"$data_dir/$ID.cgi");
@NEW_LIST=<RFILE>;
close(RFILE);
$LONG=@NEW_LIST;
$DLONG=@DELETE;
open(WFILE,">$data_dir/$ID.cgi");
for ($i=0;$i<$LONG;$i++){
$check=1;
($TEMP0,$TEMP1,$TEMP2,$TEMP3,$TEMP4,$TEMP5,$TEMP6,$TEMP7,$TEMP8,$TEMP9,$TEMP10)=split(/\|/,$NEW_LIST[$i]);
for ($ii=0;$ii<$LONG;$ii++){
if($DELETE[$ii] eq $TEMP1){$check=0;}
}
if ($check==1){print WFILE $NEW_LIST[$i];}
}
close(WFILE);
print "Content-type: text/html\n\n";
print <<EOF;
<meta http-equiv=Content-Type content=text/html; charset=gb2312>
<META HTTP-EQUIV=Refresh CONTENT=2;URL="$cgi_url?Action=admin&ID=$ID">
<html><head><title>ɾ�����</title>
<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:#555555}
-->
</style>
</head><body bgColor=$bgcolor>
<br>
<br>
<br>
<br>
<p align="center"><input size="40" value="ɾ����ɣ�2����Զ����ص�����ҳ��"></p>
</body></html>
EOF
exit;
}

sub makecode {
&check_time;
print "Content-type: text/html\n\n";
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>����HTML����</title>

<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:$fontcolor}
-->
</style>
</head>
<body bgColor=$bgcolor>
<p align="center">�뽫����HTML����ճ������ҳ��ȥ<br><textarea rows="8" name="S1" cols="60">&lt;IFRAME WIDTH=&quot;346&quot; HEIGHT=&quot;240&quot; MARGINWIDTH=&quot;1&quot; MARGINHEIGHT=&quot;1&quot; HSPACE=&quot;1&quot; VSPACE=&quot;1&quot; BORDER=&quot;0&quot; SCROLLING=&quot;no&quot; SRC=&quot;$cgi_url?Action=show&amp;amp;ID=$ID&quot;&gt;&lt;/IFRAME&gt;</textarea></p>
<br>
<center>
<hr width=300 size=1>
<table width=90% align=center cellpadding=0 cellspacing=0 style='font-size: 9pt'>
<tr>
<td align=center valign=middle>
<font color=$fontcolor1>��ѷ�����
</font><font color=#ff6633><b><a href=$net_url>$net_name</a></b></font><font color=$fontcolor1>
�ṩ</font><br>
<font color=$fontcolor1>&copy;��Ȩ����:<a href=http://www.yuzi.net>YUZI������ ��֮��</a></font>
</td>
</tr>
</table>
</center>
</body></html>
EOF
exit;
}

sub makejscode {
&check_time;
print "Content-type: text/html\n\n";
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>����JS����</title>

<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:$fontcolor}
-->
</style>
</head>
<body bgColor=$bgcolor>
<p align="center">�뽫����JS����ճ������ҳ��ȥ<br><textarea rows="8" name="S1" cols="60">&lt;script src=&quot;$cgi_url?Action=js&amp;ID=$ID&quot;&gt;&lt;/script&gt;</textarea></p>
<br>
<center>
<hr width=300 size=1>
<table width=90% align=center cellpadding=0 cellspacing=0 style='font-size: 9pt'>
<tr>
<td align=center valign=middle>
<font color=$fontcolor1>��ѷ�����
</font><font color=#ff6633><b><a href=$net_url>$net_name</a></b></font><font color=$fontcolor1>
�ṩ</font><br>
<font color=$fontcolor1>&copy;��Ȩ����:<a href=http://www.yuzi.net>YUZI������ ��֮��</a></font>
</td>
</tr>
</table>
</center>
</body></html>
EOF
exit;
}

sub js {
&get_date;
if ($ID eq ""){
print "Content-type: text/html\n\n";
print "document.write(\"�����ID\");\n";
exit;
}
open(RFILE,"$data_dir/$ID.cgi");
@NEW_LIST=<RFILE>;
close(RFILE);
$LONG=@NEW_LIST;
print "Content-type: text/html\n\n";
print "function newin(width,height,url,name) {\n";
print "msgWindow=window.open(url,name,'statusbar=no,scrollbars=yes,status=yes,resizable=yes,width='+width+',height='+height)\n";
print "}\n";
if($page_num eq "" || $page_num==1){
$page_num==1;
$start_page=0;
$end_page=9;
}else{
$start_page=($page_num-1)*10;
$end_page=$page_num*10-1;
}
print "document.write(\"<table border=0 width=340 cellspacing=0 cellpadding=0 style='font-size: 9pt' bgcolor=$bgcolor>\");\n";
print "document.write(\"<tr>\");\n";
print "document.write(\"<td width=340 align=center colspan=2 height=18 valign=middle>\");\n";
#print "document.write(\"<A HREF=http://www.yuzi.net target=_blank style='TEXT-DECORATION:none;color:$Vlinkcolor'><ACRONYM TITLE='�������:�������\\n��Ȩ����:YUZI������ ��֮��\\n����֧��:http://www.yuzi.net'>YUZI NEW2001 V1.2</ACRONYM></A> &nbsp;&nbsp;<b><font color=#FF8000>����С�� <font color=red>+</font> վ��С��</font></b>\");\n";
print "document.write(\"<A HREF=http:// target=_blank style='TEXT-DECORATION:none;color:$Vlinkcolor'><ACRONYM TITLE='ɱ����ּ:����Ϊ����ӮǮ�����������ǳɹ���\\nɱ�ֿ챨����ʱ�����������顣\\n��ӭ����:mailto:dax2000@yeah.net'>ɱ������</ACRONYM></A> &nbsp;&nbsp;<b><font color=#FF8000>����С�� <font color=red>+</font> վ��С��</font></b>\");\n";
print "document.write(\"&nbsp;&nbsp;<a href=$cgi_url target=_blank style='TEXT-DECORATION:none;color:$Vlinkcolor'><img src='$image_url/key.gif' width=18 height=13 border=0>�������</a></td>\");\n";
print "document.write(\"</tr>\");\n";
$ii=10;
for ($i=0;$i<$LONG;$i++){
($TEMP0,$TEMP1,$TEMP2,$TEMP3,$TEMP4,$TEMP5,$TEMP6,$TEMP7,$TEMP8,$TEMP9,$TEMP10)=split(/\|/,$NEW_LIST[$i]);
if ($i>=$start_page && $i<=$end_page){
if(length($TEMP2) >30){$TEMP2=substr($TEMP2,0,28);$TEMP2="$TEMP2..";}
print "document.write(\"<tr onmouseover=this.style.backgroundColor='$DBcolor' onmouseout=this.style.backgroundColor='$bgcolor'>\");\n";
print "document.write(\"<td width=230 height=16><a href=JavaScript:newin(320,240,'$cgi_url?Action=shownew&ID=$ID&newid=$TEMP1','NEW') style='TEXT-DECORATION:none;color:$linkcolor'><img src='$image_url/win.gif' border=0 width=16 height=16> $TEMP2</a>\");\n";
($T0,$T1,$T2)=split(/\-/,$TEMP4);
if (($T0 eq $year)&&($T1 eq $month)&&($T2 eq $day)){
print "document.write(\"<img src='$image_url/today.gif' border=0 width=16 height=16>\");\n";
}
print "document.write(\"</td>\");\n";
print "document.write(\"<td width=110 height=16><font color=$datecolor>$TEMP4</font> <font color=$timecolor>[$TEMP5]</font></td>\");\n";
print "document.write(\"</tr>\");\n";
$ii=$ii-1;
}
}
for (1..$ii){
print "document.write(\"<tr onmouseover=this.style.backgroundColor='$DBcolor' onmouseout=this.style.backgroundColor='$bgcolor'>\");\n";
print "document.write(\"<td width=340 colspan=2 height=16 style=color:$NOmessagecolor><img src='$image_url/no.gif' border=0 width=16 height=16> û������</td>\");\n";
print "document.write(\"</tr>\");\n";
}
$total_page = int($LONG/10);
if($page_num<1 || $page_num eq ""){$page_num=1;}
if($page_num>$total_page){$page_num=$total_page;}
if (($total_page*10)<$LONG){$total_page++;}	
$page=$page_num;
$term = 5;
$mycel="Action=show";
print "document.write(\"<tr>\");\n";
print "document.write(\"<td width=340 colspan=2 align=center  height=16 style=color:$NOmessagecolor>\");\n";
&makepagejs;
print "document.write(\"</td>\");\n";
print "document.write(\"</tr>\");\n";
print "document.write(\"</table>\");\n";
exit;
}

sub makepagejs {
	$first = 1;
	$last = $term;
	while ($first <= $total_page) {
		if (($first <= $page) && ($page <= $last)) {
		$prevp = $first - 1;
			if ($prevp > 0) {
				print "document.write(\"[<a href=JavaScript:newin(400,280,'$cgi_url?$mycel&ID=$ID&page_num=$prevp','NEW') style='TEXT-DECORATION:none;color:$Vlinkcolor'>��ǰ��</a>].....\");";
			}
			else {
				print "document.write(\"[<font color=$Vlinkcolor>��ǰ��</font>].....\");";
			}
		if ($last <= $total_page) {
			for ($pa = $first; $pa <= $last; $pa++) {
				if ($pa == $page) {
					print "document.write(\"[<a href=JavaScript:newin(400,280,'$cgi_url?$mycel&ID=$ID&page_num=$pa','NEW') style='TEXT-DECORATION:none;color:$Vlinkcolor'>$pa</a>] \");";
				}
				else {
					print "document.write(\"[<a href=JavaScript:newin(400,280,'$cgi_url?$mycel&ID=$ID&page_num=$pa','NEW') style='TEXT-DECORATION:none;color:$Vlinkcolor'>$pa</a>] \");";
				}
			}
		}
		else {
			for ($pa = $first; $pa <= $total_page; $pa++) {
				if ($pa == $page) {
					print "document.write(\"[<a href=JavaScript:newin(400,280,'$cgi_url?$mycel&ID=$ID&page_num=$pa','NEW') style='TEXT-DECORATION:none overline;color:$Vlinkcolor'>$pa</a>] \");";
				}
				else {
					print "document.write(\"[<a href=JavaScript:newin(400,280,'$cgi_url?$mycel&ID=$ID&page_num=$pa','NEW') style='TEXT-DECORATION:none;color:$Vlinkcolor'>$pa</a>] \");";
				}
			}
		}
		$nextp = $last + 1;
		if ($nextp <= $total_page) {
			print "document.write(\".....[<a href=JavaScript:newin(400,280,'$cgi_url?$mycel&ID=$ID&page_num=$nextp','NEW') style='TEXT-DECORATION:none;color:$Vlinkcolor'>���</a>]\");";
		}
		else {
			print "document.write(\".....[<font color=$Vlinkcolor>���</font>]\");";
		}
	}
	$first = $first + $term;
	$last = $last + $term;
	}
}

sub reg {
print "Content-type: text/html\n\n";
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>�����û���</title>

<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:$fontcolor}
-->
</style>
</head>
<body bgColor=$bgcolor>
<br>
<br>
<form action="$cgi_url" method="post">
<input type="hidden" name="Action" value="doreg">
<center><div align="center"><table
  cellSpacing="2" width="205" border="0">
    <tr bgColor="#ccccff" align="center">
      <td width="197" align="center" bgcolor="$TBcolor"><font size="2">�û���:</font> <input
      size="15" name="username"><br>
      <font size="2">��<font color="#ccccff">��</font>��:</font> <input type="password"
      size="15" name="userpass"><br>
      <font size="2">��<font color="#ccccff">��</font>��:</font> <input type="text"
      size="15" value name="email"><br>
      <font size="2">��<font color="#ccccff">��</font>ҳ:</font> <input type="text"
      size="15" name="homeurl" value="http://"><br>
      <font size="2">վ<font color="#ccccff">��</font>��:</font> <input type="text"
      size="15" name="homename"><br>
      <font size="2"><input type="submit" value=" �� �� " name="Submit"  style='background-color: rgb(255,255,255)'>��<input type="reset"
      value=" ȡ �� " name="Submit"  style='background-color: rgb(255,255,255)'></font></td>
    </tr>
  </table>
  </center></div>
</form>
<br>
<center>
<hr width=300 size=1>
<table width=90% align=center cellpadding=0 cellspacing=0 style='font-size: 9pt'>
<tr>
<td align=center valign=middle>
<font color=$fontcolor1>��ѷ�����
</font><font color=#ff6633><b><a href=$net_url>$net_name</a></b></font><font color=$fontcolor1>
�ṩ</font><br>
<font color=$fontcolor1>&copy;��Ȩ����:<a href=http://www.yuzi.net>YUZI������ ��֮��</a></font>
</td>
</tr>
</table>
</center>
</body></html>
EOF
exit;
}

sub doreg {
if ($FORM{'username'} eq ""||$FORM{'userpass'} eq ""||$FORM{'email'} eq ""||$FORM{'homeurl'} eq ""||$FORM{'homename'} eq ""){&errorview("�û��������룬���ʵ����ϱ�����ʵ��д��");exit;}
if (!($FORM{'email'}=~ /.*\@.*\..*/)){&errorview("����Email�������");exit;}

open(TEMP,"$filepath/user/userdata.cgi");
@USERDATA=<TEMP>;
close(TEMP);
$check=0;
foreach $USERDATA (@USERDATA) {
($T0,$T1,$T2,$T3,$T4,$T5,$T6,$T7,$T8,$T9,$T10,$T11,$T12,$T13,$T14,$T15,$T16,$T17,$T18)=split(/\|/,$USERDATA);
if ($username eq $T0){&errorview("�û���Ϊ$username���Ѿ����ڣ��뻻���û������룡");exit;}
}

$FORM{'username'}=~ s/&/&amp;/g;
$FORM{'userpass'}=~ s/&/&amp;/g;
$FORM{'email'}=~ s/&/&amp;/g;
$FORM{'homename'}=~ s/&/&amp;/g;
$FORM{'homeurl'}=~ s/&/&amp;/g;
&com124('username', 'userpass', 'email', 'homename', 'homeurl');

open(TMP,">$filepath/user/userdata.cgi");
print TMP "@USERDATA";
print TMP "$FORM{'username'}|$FORM{'userpass'}|$FORM{'email'}|$FORM{'homename'}|$FORM{'homeurl'}|||||||||||\n";
close(TMP);

print "Content-type: text/html\n\n";
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>����ɹ�</title>

<style type=text/css>
<!--
A:link    {text-decoration:none;color:$linkcolor}
A:active  {TEXT-DECORATION:none;color:$bgcolor}
A:visited {TEXT-DECORATION:none;color:$Vlinkcolor}
A:hover   {TEXT-DECORATION:underline overline;color:$Hlinkcolor}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:$fontcolor}
-->
</style>
</head>
<body bgColor=$bgcolor>
<p align="center"><a href=new2001.cgi>��½</a></p>
<br>
<center>
<hr width=300 size=1>
<table width=90% align=center cellpadding=0 cellspacing=0 style='font-size: 9pt'>
<tr>
<td align=center valign=middle>
<font color=$fontcolor1>��ѷ�����
</font><font color=#ff6633><b><a href=$net_url>$net_name</a></b></font><font color=$fontcolor1>
�ṩ</font><br>
<font color=$fontcolor1>&copy;��Ȩ����:<a href=http://www.yuzi.net>YUZI������ ��֮��</a></font>
</td>
</tr>
</table>
</center>
</body></html>
EOF
exit;
}