#!/usr/bin/perl
#------------------------------------------------------#
# laotong/asd168                                                     #
#              ������Ϊ �й�CGI֮�� �ṩ	           #
#              Ajie�����԰���û���V3.01               #
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
print qq(<FONT COLOR=#ff0000><B>��ȫ����</B>��<br>install.cgi �ļ���Ȼ�����ķ������ϣ����������� FTP ���߽���ɾ������<br> ����ɾ��֮��ˢ�±�ҳ�����½���������ġ�</FONT>);exit;}
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
if ($testcookie) {$cookie_result = qq(Cookies �Ƿ����? <font color=#336666>== [ͨ��]</font>);}
else {$cookie_result = qq(Cookies �Ƿ����? <font color=#336666>== [ʧ��]</font>);}
print qq(
<tr><td bgcolor="#73BAB4"><font face=���� color=#FFFFFF>
                <b>��ӭ�������Ա���������</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center>
                <font face=���� color=#336666><b>��ӭ $admin</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>

                <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left>
                <font face=���� color=#336666>
                <center><br>
                ������ʱ�䣺<b>$current_time</b><br>
                </center>
                <hr color=#DCECEA>
                 <font color=#336666 face=����>
                  <p> <b>���Ա�����ժҪ</b><br>
                    <br>
                    <br>
                    ע�����Ա�����$totalrecode �� <br>
                    <br><br><br>
                    ��������&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;��<font color=red>$ENV{'HTTP_HOST'}</font><br>
                    ����IP��ַ&nbsp;&nbsp;&nbsp;&nbsp;��<font color=red>$ENV{'SERVER_ADDR'}</font><br>
                    Ŀ¼·��&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;��<font color=#FF0000>$cgiabs</font> == [��ȷ] <br>
                    Perl&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;�汾��<font color=#FF0000>$]</font> == [ͨ��] <br>
                    Cookie &nbsp;&nbsp;&nbsp;���ԣ�<font color=#FF0000>$cookie_result</font><br>
                    ����������ϵͳ��<font color=red>$^O</font>
                    <br>
                    <br>
                  <hr color=#DCECEA>
                  <font color=#336666 face=����>����������<a href="mailto:webmaster\@homecgi.com">Ajie</a><br>
                  ��Ȩ���У�<a href="http://www.homecgi.com">�й�CGI֮��</a></font> </font>
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
<tr><td bgcolor="#73BAB4" colspan="8"><font face=���� color=#FFFFFF>
                <b>��ӭ�������Ա���������</b>
                </td></tr>
                <tr>
                <td bgcolor=#ECF6F5 align=center colspan="8">
                <font face=���� color=#336666><b>ע�����Ա�����</b></font>�����������û�<b><font face=���� color=#ff0000>$totalrecode</font></b>����
                </td></tr>
                <tr><td bgcolor=#ECF6F5 colspan="8">
                </td>
                </tr><tr>
<form method="POST" action="$cgiurl/admin.cgi">
<tr bgcolor="#DCECEA" align="center">
<td width="1%" height="1" align="center">
<input type=hidden name="action" value="deluser"></td>
<td width="15%" height="1" align="center">���Ա���</td>
<td width="5%" height="1" align="center">�û�</td>
<td width="5%" height="1" align="center">����</td>
<td width="25%" height="1" align="center">��վ��ַ</td>
<td width="12%" height="1" align="center">����ʱ��</td>
<td width="15%" height="1" align="center">ʹ��IP��ַ</td>
<td width="10%" height="1" align="center">������</td>
</tr>
HTML
$inti=0;
foreach (@userno)
  {
   ($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/��/,$USER{$_});
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
<tr bgcolor="#DCECEA" align="center"><td colspan="8"><input type="submit" value="ɾ ��" name="B1"></td></tr></form></table>
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
<tr><td bgcolor="#73BAB4" colspan="2"><font face=���� color=#FFFFFF>
                <b>��ӭ�������Ա���������</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=���� color=#336666><b>ע���µ����Ա�</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<form method="post" action="$cgiurl/admin.cgi">
<input type=hidden name="action" value="adduser">
<tr bgColor=ECF6F5><td align=right width=25%>�� �� ����</td><td width=75%><input type="text" name="username" size="20" maxlength=8 value=$admin>* 1-8λ�������û�����</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>�û����룺</td><td width=75%><input type="text" name="userpass" size=20 value="$password">* ��������</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>�ظ����룺</td><td width=75%><input type="text" name="userpass1" size="20">* ��������</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>�����ʼ���</td><td width=75%><input type="text" name="emailaddress" size="20" value="$adminmail">* �ʼ���ַ���ʼ�֪ͨ��</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>��ҳ��ַ��</td><td width=75%><input type="text" name="homepage" value = "http://" size="20">* ��ҳ��ַ</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>���Ա�����</td><td width=75%><input type="text" name="title" size="20" value="$home���Ա�">* ������Ա�������</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>ÿҳ��¼��</td><td width=75%><input type="text" name="recode" size="20" value="$pagenum" maxlength="2">* Ĭ��Ϊ$pagenum��</td></tr>
<tr><td width="100%" bgcolor=#DCECEA align="center" colspan="2">
<input type="submit" value="�ύ����" name=ok>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td></tr></FORM>
</table></td></tr></table>
);
exit;}
############################################
sub adduser {
if($FORM{'username'} eq ""){&errorview("�û�������û����д!");}
if($FORM{'username'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorview("�����в��ܺ��������ַ�!");}
if($FORM{'userpass'} eq ""){&errorview("�û����벻��û����д!");}
if($FORM{'userpass'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorview("�����в��ܺ��������ַ�!");}
if($FORM{'userpass'} ne "$FORM{'userpass1'}"){&errorview("������������벻��ͬ!");}
if (($FORM{'userpass'} eq "") || ($FORM{'userpass1'} eq ""))
{&errorview("�����ȷ�����벻��Ϊ��, ����������!!");}
if (!($FORM{'emailaddress'} =~ /.*\@.*\..*/)){&errorview("��������һ������ĵ����ʼ���ַ������");}
dbmopen(%USERFILE,"$userpath/alluser.db",0666);
foreach (%USERFILE)
{if ($_ =~ "��$FORM{'username'}��")
{&errorview("���û��ѱ�ע��!!������û���!!");}
if ($_ =~ "��$FORM{'homepage'}��"){&errorview("����ҳ�Ѿ�ע��������Ա�!!���������������!");}
if ($_ =~ "��$FORM{'emailaddress'}��"){&errorview("�������Ѿ�ע��������Ա�!!���������������!!");}}
($sec,$min,$hour,$mday,$mon,$year)=localtime(time);
$mon           = $mon+1;
$year          = $year+1900;
$date_time  = sprintf ("%04d/%02d/%02d",$year,$mon,$mday);
$name   = $FORM{'username'};
	    $name =~ s/\&nbsp\;//ig;
	    $name =~ s/��/ /g;
	    $name =~ s/��/ /g;
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
$USERFILE{$newuserno} = "start��$name��$pass��$email��$url��$title��$pagenum��$ipaddress��$date_time��end��\n";
dbmclose(%USERFILE);
print qq(
<tr><td bgcolor="#73BAB4" colspan="2"><font face=���� color=#FFFFFF>
                <b>��ӭ�������Ա���������</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=���� color=#336666><b>ע��ɹ�</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<tr bgColor=ECF6F5>
<td align=center width=100%><br><br><a href=gbook.cgi?user=$name>�����������Ա�</a><br></td></tr>
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

                   ($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/��/,$USERLIST{$tempno});
                   delete $USERLIST{$tempno};
                   unlink (<"$datapath/$name.*">);
                  }
               }
            }
         }
       dbmclose(%USERLIST);
print qq(
<tr><td bgcolor="#73BAB4" colspan="8"><font face=���� color=#FFFFFF>
                <b>��ӭ�������Ա���������</b>
                </td></tr>
<tr bgcolor="#DCECEA" align="center"><td><br>ɾ���ɹ�����</td></tr></table>
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
    <tr><td bgcolor="#73BAB4" colspan="2"><font face=���� color=#FFFFFF>
                <b>��ӭ�������Ա���������</b>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=���� color=#336666><b>�� �� �� �� ʾ</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5 colspan="2">
                </td>
                </tr>
<tr><td align=center>
<FONT size=7 face=Wingdings color=#ff0000>L</FONT><P><font size=2>$_[0]</font></P></td></tr>
<tr><td colSpan=2 width=100%><div align=center><center>
<table border=1 bgColor=cccccc cellspacing=0><tr><td width=100% align=center bordercolordark=#E6E6E6 bordercolorlight=#cccccc><A href=javascript:history.back()><font size=2 color=#000000>��ȷ ��&nbsp;&nbsp;</font></A>
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