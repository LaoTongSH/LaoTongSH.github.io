#!/usr/bin/perl
#------------------------------------------------------#
#                                                      #
#              ������Ϊ �й�CGI֮�� �ṩ	           #
#              Ajie�����԰���û���V4.0                #
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
      &errorinput("���Ա���ͣ����");
     }
&pagestyle;
print qq(
<html>
    <head>
    <title>�������Ա�</title>
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
            <div align="center"><font color=$btfont>�� �� �� �� ��</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�� �� ����</td>
<td width="70%">&nbsp;
<input type="text" name="username" size="20" maxlength=8 class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * 1-8λ�������û�����
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�û����룺</td>
<td width="70%">&nbsp;
<input type="password" name="userpass" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * ��������
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�ظ����룺</td>
<td width="70%">&nbsp;
<input type="password" name="userpass1" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * ��������
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�����ʼ���</td>
<td width="70%">&nbsp;
<input type="text" name="emailaddress" size="20" class="input2" value="@">&nbsp;&nbsp;&nbsp; &nbsp;* �ʼ���ַ(�ʼ�֪ͨ��
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">��ҳ��ַ��</td>
<td width="70%">&nbsp;
<input type="text" name="homepage" value = "http://" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * ��ҳ��ַ
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">���Ա�����</td>
<td width="70%">&nbsp;
<input type="text" name="title" size="20" value="�ҵ����Ա�" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * ������Ա�������
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">ÿҳ��¼��</td>
<td width="70%">&nbsp;
<input type="text" name="recode" size="20" value="$pagenum" maxlength="2" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * Ĭ��Ϊ$pagenum��
</td>
</tr>
        <tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
<input type="submit" value="�ύ����" name="B1" class="input2">&nbsp;&nbsp;&nbsp;&nbsp;
			  <input type="reset"  value="��������" name="B2" class="input2"></div>
</td></tr></table>
</td></tr></table>
</form>
~;
sub modify{
$user=$FORM{'user'};
dbmopen (%USER,"$userpath/alluser.db",0666);
foreach (%USER){
if ($_ =~ "��$user��")
{
($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/��/,$_);
dbmclose(%USER);
}}
&pagestyle;
print qq~
<html>
    <head>
    <title>�޸����Ա���Ϣ</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
    </head>
    <body bgcolor="$gbbgcolor" $gbbody>
<form method="POST" action="$cgiurl/register.cgi?action=modifyuser&user=$user">
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont>�޸� <font color=red>$user</font> ���Ա���Ϣ</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�� �� ����</td>
<td width="70%">&nbsp;&nbsp;<font color=red>$user</font>
<input type="hidden" name="username" value="$user">
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�û����룺</td>
<td width="70%">&nbsp;
<input type="password" name="userpass" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * ��������
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�ظ����룺</td>
<td width="70%">&nbsp;
<input type="password" name="userpass1" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * ��������
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�����ʼ���</td>
<td width="70%">&nbsp;
<input type="text" name="emailaddress" size="20" class="input2" value="$email">&nbsp;&nbsp;&nbsp; &nbsp;* �ʼ���ַ(�ʼ�֪ͨ��
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">��ҳ��ַ��</td>
<td width="70%">&nbsp;
<input type="text" name="homepage" value = "$url" size="20" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * ��ҳ��ַ
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">���Ա�����</td>
<td width="70%">&nbsp;
<input type="text" name="title" size="20" value="$title" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * ������Ա�������
</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">ÿҳ��¼��</td>
<td width="70%">&nbsp;
<input type="text" name="recode" size="20" value="$pagenum" maxlength="2" class="input2">&nbsp;&nbsp;&nbsp;&nbsp; * Ĭ��Ϊ$pagenum��
</td>
</tr>
        <tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
<input type="submit" value="�ύ����" name="B1" class="input2">&nbsp;&nbsp;&nbsp;&nbsp;
			  <input type="reset"  value="��������" name="B2" class="input2"></div>
</td></tr></table>
</td></tr></table>
</form>
</table>
<table border="0" width=$tablewidth>
<tr align=middle>
<td width=100%><br>
<p align="center">������Ա���<b><a href=$homeurl target=_blank> $home </a></b>
�ṩ ����֧�֣�<b><a href=http://www.cgiubb.com target=_blank> CGI������̳</a></b></p>
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
<p align="center">������Ա���<b><a href=$homeurl target=_blank> $home </a></b>
�ṩ ����֧�֣�<b><a href=http://www.cgiubb.com target=_blank> CGI������̳</a></b></p>
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
       	    $name       = &checknull($FORM{'username'}   ,"�������Ϊ��!!");
            if (length($name)>8) {&errorinput("���ֲ��ܳ���8���ַ���");}
            if($name=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorinput("�����в��ܺ��������ַ�!");}
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
            if($FORM{'userpass'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?�-]/){&errorinput("�����в��ܺ��������ַ�!");}
       	    $email      = &checknull($FORM{'emailaddress'}  ,"�����ʼ����Ϊ��!!");
            $title      = &checknull($FORM{'title'},"���Ա������Ϊ��!!");
            $url        = &checknull($FORM{'homepage'}    ,"��ҳ��ַ����Ϊ��!!");
            $pagenum    = &checknull($FORM{'recode'}  ,"ÿҳ��¼�����Ϊ��!!");
            if (!($email =~ /.*\@.*\..*/))
              {
               &errorinput("��������һ������ĵ����ʼ���ַ������");
              }
            if (!($url   =~ /http:\/\/.*\..*/))
              {
               &errorinput("��������һ���������ҳ��ַ������");
              }
       	    dbmopen(%USERFILE,"$userpath/alluser.db",0666);
            foreach (%USERFILE)
              {
               if ($_ =~ "��$FORM{'username'}��")
                  {
                   &errorinput("���û��ѱ�ע��!!������û���!!");
                  }
               if ($_ =~ "��$FORM{'homepage'}��")
                  {
                   &errorinput("����ҳ�Ѿ�ע��������Ա�!!���������������!!");
                  }
               if ($_ =~ "��$FORM{'emailaddress'}��")
                  {
                   &errorinput("�������Ѿ�ע��������Ա�!!���������������!!");
                  }
              }
            $date_time  = sprintf ("%04d/%02d/%02d",$year,$mon,$mday);
            if (($FORM{'userpass'} eq "") || ($FORM{'userpass1'} eq ""))
              {
               &errorinput("�����ȷ�����벻��Ϊ��, ����������!!");
              }
            elsif ($FORM {'userpass'} ne $FORM {'userpass1'})
              {
               &errorinput("������ȷ�����벻ͬ, ����������!!");
              }
            else
              {
               $pass   = $FORM{'userpass'};
              }
            $newuserno  = sprintf ("%04d%02d%02d%02d%02d%02d",$year,$mon,$mday,$hour,$min,$sec);
            $ipaddress  = $ENV{'REMOTE_ADDR'};
            dbmopen(%USERFILE,"$userpath/alluser.db",0666);
            $USERFILE{$newuserno} = "start��$name��$pass��$email��$url��$title��$pagenum��$ipaddress��$date_time��end��\n";
            dbmclose(%USERFILE);
           }
        else
           {
            dbmopen(%USERFILE,"$userpath/alluser.db",0666);
            @userno=keys %USERFILE;
            @userno=sort @userno;
            foreach (@userno)
              {
               ($mark,$name111,$pass111,$email111,$url111,$title111,$pagenum111,$ipaddress,$date_time,$markend,$last)=split(/��/,$USERFILE{$_});
               if ($USERFILE{$_} =~ "$FORM{'username'}")
                 {
                  if (($name111 eq "$FORM{'username'}") && ($pass111 eq "$FORM{'userpass'}"))
                    {
                     $name       = &checknull($FORM{'username'}      ,"�������Ϊ��!!");
                     $email      = &checknull($FORM{'emailaddress'}  ,"�����ʼ����Ϊ��!!");
                     $title      = &checknull($FORM{'title'}         ,"���Ա������Ϊ��!!");
                     $url        = &checknull($FORM{'homepage'}      ,"��ҳ��ַ����Ϊ��!!");
                     $pagenum    = &checknull($FORM{'recode'}        ,"ÿҳ��¼�����Ϊ��!!");
                     if ($FORM{'userpass1'} eq "")
                        {
                         $pass = $FORM{'userpass'};
                        }
                     else
                        {
                         $pass = $FORM{'userpass1'};
                        }
                     $USERFILE{$_} = "start��$name��$pass��$email��$url��$title��$pagenum��$ipaddress��$date_time��end��\n";
                    }
                 else
                    {
                     &errorinput("������벻��, ��������޸�!!");
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
<title>����ɹ�</title></head>
<BODY bgcolor=$gbbgcolor $gbbody><center>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont>��ϲ <font color="#ff0000">$name</font> �����ѳɹ�����(�޸�)���������԰壡</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�� �� ����</td>
<td width="70%">&nbsp;$name</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�û����룺</td>
<td width="70%">&nbsp;Ϊ�����İ�ȫ������ʾ�������Ա����룡</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">���Ա�����</td>
<td width="70%">&nbsp;$title</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">ÿҳ��¼��</td>
<td width="70%">&nbsp;$pagenum</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�����ַ��</td>
<td width="70%">&nbsp;$email</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">��ҳ��ַ��</td>
<td width="70%">&nbsp;$url</td>
</tr>
<tr bgcolor=$lybgcolor>
<td width="30%" align="center">�鿴���ԣ�</td>
<td width="70%">&nbsp;<a href = $cgiurl/gbook.cgi?user=$name>$cgiurl/gbook.cgi?user=$name</a></td>
</tr>
<tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
<font color=$btfont>���Ĵ����Ѿ�ͨ��<a href = mailto:$email><font color="#ff0000"> $email </font></a>��������������С�</font></div>
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