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
require "$mypath/"."codejs.cgi";

$adminame      = "$admin";
$admipass      = "$password";
$page          = 1;
$online =1;
$action        = "show";
($sec,$min,$hour,$mday,$mon,$year)=localtime(time);
$mon           = $mon+1;
$year          = $year+1900;
($reply_date,$reply_time)=&date;
&pagestyle;
&parseadminform;
if ($user eq "")
   {
    $finduser = "";
    $user = $FORM{'user'};
    dbmopen (%CONF,"$userpath/alluser.db",0666);
    foreach (%CONF)
       {
        if ($_ =~ "��$user��")
           {
            ($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/��/,$_);
            $ajiebookurl   = $url;
            $ajiegbmail  = $email;
            $adminame   = $name;
            $admipass   = $pass;
            $finduser = "YES";
           }
       }
    dbmclose(%CONF);
   }

print "Content-type: text/html\n\n";
if ($mainonoff eq "off") {
$line1 =~ s/\&lt;/</g;
$line1 =~ s/\&gt;/>/g;
$line1 =~ s/ \&nbsp;/��/g;
$line1 =~ s/\&amp;/\&/g;
print qq($line1);exit(0);}
if ($topgg ne "") {
$topgg =~ s/\&lt;/</g;
$topgg =~ s/\&gt;/>/g;
$topgg =~ s/ \&nbsp;/��/g;
$topgg =~ s/\&amp;/\&/g;
print qq(<center><TABLE border=0 cellSpacing=0 width=$tablewidth>
  <tr align=center>
    <td>$topgg</td></tr></table><br>);}
if ($FORM{'action'} ne ""){$action = $FORM{'action'};}
if ($FORM{'page'} ne ""){$page=$FORM{'page'};}
if ($action eq "search"){
$searchswitch  = "ON";
$searchcontent = $FORM{'search'};
&show;
exit(0)}
elsif ($action eq "add"){&add;exit;}
elsif ($action eq "show"){&show;exit;}
elsif ($action eq "del"){&del;exit;}
elsif ($action eq "delok"){&delok;exit;}
elsif ($action eq "write"){&write;exit;}
elsif ($action eq "replay"){&replay;exit;}
elsif ($action eq "gotopage"){&gotopage;exit;}
elsif ($action eq "replayok"){&replayok;exit;}
&show;
exit;
#############
sub date{
	my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
	$year+=1900;
	$mon++;
	my $date=sprintf("%4d-%02d-%02d",$year,$mon,$mday);
	my $htime=sprintf("%02d:%02d:%02d",$hour,$min,$sec);
	return ($date,$htime);
}
#############

sub show
  {
   dbmopen(%TEMP,"$datapath/$user.db",0666);
   %USERLIST = %TEMP;
   dbmclose(%TEMP);
   @userno=keys %USERLIST;
   @userno=sort @userno;
   $totalrecode = $#userno+1;
   print qq(

<BODY bgcolo=$gbbgcolor $gbbody>
$pagestyle
</head>
<center>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$tbcolor>
<tr><td>
<table width=100% cellspacing=0 cellpadding=4 border=0>
<tr><td bgcolor=$btbgcolor align=center>
<a href="$cgiurl/gbook.cgi?action=write&amp;user=$user"><font color=$btfont>[ǩд����] </font></a>&nbsp;
<a href="$homeurl"><font color=$btfont>[������ҳ]</font></a>&nbsp;
<a href="mailto:$ajiegbmail"><font color=$btfont>[��������]</font></a>&nbsp;
<a href=$cgiurl/register.cgi><font color=$btfont>[�������]</font></a>&nbsp;
<a href="$cgiurl/register.cgi?action=modify&amp;user=$user" target="_blank"><font color=$btfont>[�޸�����]</font></a>&nbsp;
<a href="$cgiurl/admin.cgi" target="_blank"><font color=$btfont>[��������]</font></a>&nbsp;
<a href="http://person.zj.cninfo.net/~laotong/guestbook/guestbook.html" target="_blank"><font color=$btfont>[�����Բ�]</font></a>
</td>
</tr></table>
</td></tr></table>
  <p align="center">
);
if ($searchswitch ne "ON")
   {
    $temp = $totalrecode-($page)*$pagenum;
   }
else
   {
    $temp = 0;
    $searchtotal = 0;
    foreach (%USERLIST)
     {
      if ($_ =~ /$searchcontent/)
         {
          $searchtotal++;
         }
     }
   }

   if ($temp < 0) {$temp = 0};
   for ($inti = ($totalrecode-($page-1)*$pagenum-1);$inti >= $temp;$inti--)
     {
      $tmp=$userno[$inti];
      ($mark,$name,$email,$place,$photo,$texti,$url,$fromwhere,$date_time,$oicq,$posticons,$markend,$last)=split(/��/,$USERLIST{$tmp});
      $recode = $inti+1;
      $photoimage = substr($photo,0,2);
      $photoname  = substr($photo,4,4);
      $photoimage = "$images/$photoimage.gif";
      $texti =~ s/&nbsp;/ /g;
      if ($searchswitch ne "ON")
         {
          &writegb;
         }
      else
         {
          if ($USERLIST{$tmp} =~ /$searchcontent/)
             {
              &writegb;
             }
         }
     }
   $tmp = $totalrecode / $pagenum;
   $tmp = int($tmp);
   $temp= $totalrecode % $pagenum;
   if ($temp != 0) {$tmp++;}
   if (($totalrecode == 0) || ($searchtotal == 0))
     {
      if ($searchswitch ne "ON")
         {
          if ($totalrecode == 0)
           {
            if ($finduser ne "YES")
              {
print qq(<center><table width=$tablewidth align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=0 cellpadding=4 border=0 height="100%"><tr>
          <td bgcolor=$guestbgcolor rowspan="4" width="25%" valign="top" align=center>
<table style="filter:glow(color=$guestnamegy,direction=135)">&nbsp;
<font color=$guestnamefont>Ajie</font><br></table><img src="$images/14.gif"><br><br>
            ��ҳ��<a href=http://www.homecgi.com target=_blank title=����Ajie����ҳ>�й�CGI֮��</a><br>
            ���䣺<a href=mailto:$myemail title=��Ajieд��>д�Ÿ���</a><br>
            OICQ��5858314</td>
          <td bgcolor=$lybgcolor align=center width="1" rowspan="4">
            <table width=1 height=100% cellpadding=0 cellspacing=0 bgcolor=#83c6c0>
              <tr>
                <td width=1></td>
              </tr>
            </table>
          </td>
          <td bgcolor=$lybgcolor width="75%">�ǳ���л��ʹ��Ajie�����Ա���
            <hr width=100% size=1 color=#336666>
          </td>
        </tr>
        <tr>
          <td bgcolor=$lybgcolor width="75%">
      ��.�����յ�һ��ʹ�ñ����Ա�����<a href=$cgiurl/gbook.cgi?action=register>��������������û�</a>��<br><br>
	  ��.���������ǳ���������棬����"��������"�е�"������������"�Ƿ�������ȷ��<br><br>
	  ��.�����������ʹ�ù������Ա�������������,��������û����Ƿ���ȷ���ʺű�����ɾ������<a href=$cgiurl/gbook.cgi?action=register>���������������</a>��<br></td>
        </tr>
        <tr>
          <td bgcolor=$lybgcolor width="75%">
            <hr width=100% size=1 color=$tbcolor="#336666";>
&nbsp;&nbsp;����㻹���κβ�����ĵط�������ʣ�
	  <a href=http://www.cgiubb.com target=_blank>[CGI������̳]</a>
</td></tr></table></td></tr></table>);
              }
            else
              {
               print qq(
<form method=POST action=$cgiurl/gbook.cgi?action=add&user=$user>
<table width=70% align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="3">
            <div align="center"><font color=$btfont>�� ϲ �� �� Ϊ �� һ �� �� �� �� ��</font></div>
          </td>
        </tr>
        <tr>
          <td bgcolor=$guestbgcolor width="50%">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="24%">���Ա��⣺</td>
                <td width="76%">&nbsp;
                  <input type="text" name="place" size="25" maxlength="50" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">�������֣�</td>
                <td width="76%">&nbsp;
                  <input type="text" name="name" size="25" maxlength="50" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">�����ʼ���</td>
                <td width="76%">&nbsp;
                  <input type="text" name="email" size="25" maxlength="30" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">OICQ���룺</td>
                <td width="76%">&nbsp;
                  <input type="text" name="oicq" size="25" maxlength="50" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">��ҳ��ַ�� </td>
                <td width="76%">&nbsp;
                  <input type="text" name="url" size="25" maxlength="50" value="http://" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">ѡ��ͷ��</td>
                <td width="76%">&nbsp;&nbsp;<select name="photo">
				<option value=01 selected>ͷ��01
				<option value=02>ͷ��02
				<option value=03>ͷ��03
				<option value=04>ͷ��04
				<option value=04>ͷ��05
				<option value=05>ͷ��06
				<option value=07>ͷ��07
				<option value=08>ͷ��08
				<option value=09>ͷ��09
				<option value=10>ͷ��10
				<option value=11>ͷ��11
				<option value=12>ͷ��12
				<option value=13>ͷ��13
				<option value=14>ͷ��14
				<option value=15>ͷ��15
				<option value=16>ͷ��16
				<option value=17>ͷ��17
				<option value=18>ͷ��18
				<option value=19>ͷ��19
				<option value=20>ͷ��20
				</select>
                  <a href=$cgiurl/avatarslist.cgi target=_blank>�鿴ͷ���б�</a></td>
              </tr>
            </table>
          </td>
          <td bgcolor=$guestbgcolor width="1">
            <table width=1 height=100% cellpadding=0 cellspacing=0 bgcolor=#83c6c0>
              <tr>
                <td width=1></td>
              </tr>
            </table>
          </td>
          <td bgcolor=$guestbgcolor width="50%">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td>
                  <div align="center">
				  <textarea rows="8" name="texti" cols="35" class="input3" wrap="PHYSICAL"></textarea>
				  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td bgcolor=$btbgcolor colspan="3">            <div align="center">
			<input type="submit" value="ǩд����" name="B1" class="input2">&nbsp;&nbsp;&nbsp;&nbsp;
             <input type="reset" value="��������" name="B2" class="input2"></div></td>
        </tr>
      </table>
    </td></tr></table>

</form>
);
              }
           }
         }
      else
         {
          print qq(
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor>
            <div align="center"><font color=$btfont>������Ϣ</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
                <td align="center">�Բ���û���ҵ����������ļ�¼!<br></td>
              </tr>
        <tr><td bgcolor=$btbgcolor><div align="center">
<input type=button name=ok class=input2 value=' �� �� ' onclick=javascript:history.go(-1)></div>
</td></tr></table>
</td></tr></table>
);
         }
     }
$pageup = $page-1;
$pagedown = $page+1;
if ($page == 1){$output = qq~
<font color=$btfont>�� $tmp ҳ&nbsp;��ǰҳ&nbsp;��һҳ&nbsp;ת��&nbsp;<input type="text" name="gotourl" size="2" class="input2" value=$page>&nbsp;ҳ&nbsp;&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$pagedown><font color=$btfont>��һҳ</font></a>&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$tmp><font color=$btfont>���ҳ</font></a></font>
~;
}
elsif ($page == $tmp){$output = qq~
<font color=$btfont>�� $tmp ҳ&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=1><font color=$btfont>��ǰҳ</font></a>&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$pageup><font color=$btfont>��һҳ</font></a>&nbsp;ת��&nbsp;<input type="text" name="gotourl" size="2" class="input2" value=$page>&nbsp;ҳ&nbsp;��һҳ&nbsp;���ҳ</font>
~;
}
else {$output = qq~
<font color=$btfont>�� $tmp ҳ&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=1><font color=$btfont>��ǰҳ</font></a>&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$pageup><font color=$btfont>��һҳ</font></a>&nbsp;ת��&nbsp;<input type="text" name="gotourl" size="2" class="input2" value=$page>&nbsp;ҳ&nbsp;&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$pagedown><font color=$btfont>��һҳ</font></a>&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$tmp><font color=$btfont>���ҳ</font></a></font>
~;}

print qq(
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$tbcolor>
<tr><td>
<table width=100% cellspacing=0 cellpadding=4 border=0>
<tr><form method="POST" action="$cgiurl/gbook.cgi?action=search&user=$user&page=&$inti">
<td bgcolor=$btbgcolor align=center>
<font color=$btfont>�ؼ��֣�</font><input name="search" size="20" class="input2">&nbsp;&nbsp;&nbsp;
<input name="B1" type="submit" value="����" class="input2">
</td></form><form method="post" action="$cgiurl/gbook.cgi?action=gotopage&user=$user">
<td bgcolor=$btbgcolor align=center>$output
</td></form>
</tr></table>
</td></tr></table>);
if ($downgg ne ""){
$downgg =~ s/\&lt;/</g;
$downgg =~ s/\&gt;/>/g;
$downgg =~ s/ \&nbsp;/��/g;
$downgg =~ s/\&amp;/\&/g;
print qq(
<TABLE border=0 cellSpacing=0 width=$tablewidth>
  <tr align=center>
    <td><br>$downgg</td></tr></table>);}
print qq(<TABLE border=0 cellSpacing=0 width=$tablewidth>
  <tr align=middle>
    <td><br>
    ������Է�����<a target="_blank" href="$homeurl"> <b>$home</b> </a>�ṩ ����֧�֣�<b>Ajie</b><br>
     <a target="_blank" href="http://www.homecgi.com">Ajie �����Ա� V4.0</a>  ��Ȩ����<script>
		var tc_user="homecgi";
		var tc_class="2";
		var tc_union="";
		var tc_type="1";
		_dw('<a href=http://www.textclick.com/viewmain.asp?name='+tc_user+' target=_blank><img WIDTH=0 EIGHT=0 src=http://ad.t2t2.com/scripts/stat.dll?default&user='+tc_user+'&refer='+escape(document.referrer)+'&cur=type2 border=0></a>');
		function _dw(string) {document.write(string);}
		</script>��<a href="http://www.homecgi.com" target="_blank"><b>�й�CGI֮��</b></a></p></td></tr></table>
);
}
#####################################################################
sub add
  {$writetoad=$FORM{'writetoad'};
   $qqtoad=$FORM{'qqtoad'};
   if (($qqtoad eq "on")&&($writetoad eq "on")){print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>����ͬʱѡ��[���Ļ�]��[���͸�����]���ܣ�</h2><br><input type=button name=ok class=input2 value=\"�� ��\" onclick=javascript:history.go(-1)></div>";exit;}
   $name       = &checknull($FORM{'name'}   ,"���ֲ���Ϊ��!!");
   if (length($name)>20) {print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>���ֲ��ܳ���10���֣�</h2><br><input type=button name=ok class=input2 value=\"�� ��\" onclick=javascript:history.go(-1)></div>";exit;}
   $email      = $FORM{'email'};
   if ($email eq ""){$email="��������";}
   $place      = &checknull($FORM{'place'}  ,"���ⲻ��Ϊ��!!");
if (length($place)>40) {print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>���ⳤ�Ȳ��ó��� 20 ������</h2><br><input type=button name=ok class=input2 value=\"�� ��\" onclick=javascript:history.go(-1)></div>";exit;}
   if ($place eq ""){$place="��������";}
   $oicq      = $FORM{'oicq'};
   $posticon  = $FORM{'posticon'};
   $posticons = "$images/posticons/$posticon";
   if ($oicq eq ""){$oicq="OICQ";}
   $url        = $FORM{'url'};
   if ($url   eq ""){$url  ="��������";}
   $texti = &checknull($FORM{'texti'}  ,"���Բ�˵�ǲ��е�!!һ��Ҫ˵����Ŷ��");
   $texti =~ s/ /&nbsp;/g;
   $texti =~ s/\<p\>/\n\n/ig;
   $texti =~ s/\<br\>/\n/ig;
   $texti = &code("$texti");
   if (length($oicq)>8) {print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>�����OICQ����!</h2><br><input type=button name=ok class=input2 value=\"�� ��\" onclick=javascript:history.go(-1)></div>";}
   if (length($texti)>$lymax) {print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>����������ݲ��ܳ���$lymax���ַ�Ŷ��<br>������볤ƪ���۵Ļ�������վ��̳ȥ�ɣ�</h2><br><input type=button name=ok class=input2 value=' �� �� '  onclick=javascript:history.go(-1)></div>";exit;}
   $photo      = $FORM{'photo'} ;
   $newuserno  = sprintf ("%04d%02d%02d%02d%02d%02d",$year,$mon,$mday,$hour,$min,$sec);
   $ipaddress  = $ENV{'REMOTE_ADDR'};
   $fromwhere = &ipwhere("$ipaddress");
   $date_time  = sprintf ("%04d/%02d/%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
   $message =  "������Ϣ���£� \n";
   $message.=  "------------------------------------------------------\n";
   $message.=  "���Ա���: $place\n";
   $message.=  "��    ��: $name\n";
   $message.=  "�����ʼ�: $email\n";
   $message.=  "OICQ����: $oicq\n";
   $message.=  "��ҳ��ַ: $url\n";
   $message.=  "I P ��ַ: $ipaddress\n";
   $message.=  "��    ��: $fromwhere\n";
   $message.=  "����ʱ��: $date_time\n";
   $message.=  "��������:\n\n";
   $message.=  "    $texti\n\n";
   $message.=  "\n\n";
   $message.=  "�ظ����ԣ�$cgiurl/gbook.cgi?action=replay&user=$user&recode1=$newuserno\n\n";
   $message.=  "------------------------------------------------------\n";
if ($qqtoad eq "on"){
   $user = $FORM{'user'};
   open (MAIL, "|$mailprog $ajiegbmail");
   print MAIL "Reply-to:$email\n";
   print MAIL "From: $ajiegbmail\n";
   print MAIL "Subject: $title�����Ѹ��㷢���Ļ���\n\n";
   print MAIL "$message";
   close (MAIL);
   $texti="������Ϊ���Ļ������������ѷ��͸���������";
}
if ($writetoad eq "on"){
   $user = $FORM{'user'};
   open (MAIL, "|$mailprog $ajiegbmail");
   print MAIL "Reply-to:$email\n";
   print MAIL "From: $ajiegbmail\n";
   print MAIL "Subject: $title�����Ѹ���������\n\n";
   print MAIL "$message";
   close (MAIL);
}
   dbmopen(%USERFILE,"$datapath/$user.db",0666);
   $USERFILE{$newuserno} = "start��$name��$email��$place��$photo��$texti��$url��$fromwhere��$date_time��$oicq��$posticons��end��\n";
   dbmclose(%USERFILE);
   &mailadmin;
   $linkurl      = "$cgiurl/gbook.cgi?user=$user";
print <<EOF;
<html>
<head>
<title>�������Ա�</title>
<meta HTTP-EQUIV="REFRESH" CONTENT="3;URL=$linkurl">
$pagestyle
</head>
<BODY bgcolo=$gbbgcolor $gbbody>
<ul>
<p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">
  <h2>
  ��ȴ� ϵͳ���ڴ������������Ϣ..... <br>
  ���Գɹ�,3������ǽ����㷵��������Ա�����ҳ.<br>
  ���ϵͳû�з�Ӧ�밴��������ӷ������Ա���<br>
  <a href=$cgiurl/gbook.cgi?user=$user>�����ҵ����Ա�</a>
  </h2>
</p>


  </font>


EOF
  }
#############
sub filterhtml
  {
   local($return)=$_[0];
   $return =~ s/<!--(.|\n)*-->//g;
   if ($allow_html == 0)
     {
      $return =~ s/<([^>]|\n)*>//g;
      $return =~ s/<//g;
     }
   return $return;
  }
#############
sub writegb
  {
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>$home</title></head>
<body bgcolor="$gbbgcolor" $gbbody>
EOF
print qq(<center><table width=$tablewidth align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=0 cellpadding=4 border=0 height="100%"><tr>
          <td bgcolor=$guestbgcolor rowspan="4" width="25%" valign="top" align=center>
<table style="filter:glow(color=$guestnamegy,direction=135)">&nbsp;
<font color=$guestnamefont>$name</font></table><img src="$photoimage"><br><br>
 �� $recode ������</td>
          <td bgcolor=$lybgcolor align=center width="1" rowspan="4">
            <table width=1 height=100% cellpadding=0 cellspacing=0 bgcolor=#83c6c0>
              <tr>
                <td width=1></td>
              </tr>
            </table>
          </td>
          <td bgcolor=$lybgcolor width="75%"><b>���⣺</b>$place);
if ($url eq "http://"){print qq~&nbsp;<img src="$images/homepage.gif" width="16" height="15" border=0>��ҳ~;}
else {print qq~&nbsp;&nbsp;<a href="$url" target="_blank" title="����$name����ҳ" target="_blank"><img src="$images/homepage.gif" width="16" height="15" alt="����$name����ҳ" border=0>��ҳ</a>~;}
if ($email eq "��������"){print qq~&nbsp;<img src="$images/email.gif" width="16" height="15" border=0>����</a>~;}
else {print qq~&nbsp;<a href="mailto:$email" title="��$name����" target="_blank"><img src="$images/email.gif" width="16" height="15" alt="��$name����" border=0>����</a>~;}
if ($oicq eq "OICQ"){print qq~&nbsp;&nbsp;<img src="$images/oicq.gif" width="16" height="15" alt="$name��QQ����:$oicq" border=0>$oicq~;}
else {print qq~&nbsp;&nbsp;<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$oicq target=_blank><img src="$images/oicq.gif" width="16" height="15" alt="$name��QQ����:$oicq" border=0>$oicq</a>~;}
print qq( <hr width=100% size=1 color=$tbcolor>
          </td>
        </tr>
        <tr>
          <td bgcolor=$lybgcolor width="75%"><TABLE border=0 cellPadding=3 cellSpacing=0 height="100%" width="100%"><TBODY><TR><TD vAlign=top width="100%"><img src=$posticons width=13 height=13 border=0>&nbsp;&nbsp;$texti</TD></TR></TBODY></TABLE></td>
        </tr>
        <tr>
          <td bgcolor=$lybgcolor width="75%">
            <hr width=100% size=1 color=$tbcolor>
<img src="$images/posttime.gif" width="16" height="15" alt="����ʱ��">��$date_time&nbsp;&nbsp;<img src="$images/ip.gif" width="16" height="15" alt="��������">��$fromwhere&nbsp;&nbsp;<a href="gbook.cgi?action=replay&user=$user&recode1=$tmp" target="_blank"><img src="$images/replynow.gif" width="16" height="15" alt="�ظ�����" border=0>�ظ�</a>&nbsp;
<a href="gbook.cgi?action=del&user=$user&recode1=$tmp" target="_blank"><img src="$images/del.gif" width="16" height="15" alt="ɾ������" border=0>ɾ��</a>
</td></tr></table></td></tr></table>);
   }
#############
sub del
  {
   dbmopen(%TEMP,"$datapath/$user.db",0666);
   %USERLIST = %TEMP;
   dbmclose(%TEMP);
   @userno=keys %USERLIST;
   @userno=sort @userno;
   $totalrecode = $#userno+1;
   $deleteyes = "del";
   print <<HTMLEOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>$gbname</title></head>
<center>
<form method="post" action="$cgiurl/gbook.cgi?action=delok&user=$user&recode1=$FORM{'recode1'}">

<table width=230 align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont>ɾ �� �� ��</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
                <td width="30%" align="center">�����˺ţ�</td>
                <td width="70%">&nbsp;<!--$admin-->
<input type=text name=adminame size=20 class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="30%" align="center">�������룺</td>
                <td width="70%"><!--$password-->&nbsp;
<input type=password name=admipass size=20 class="input2">
                </td>
              </tr>
        <tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
<input type="submit" value="ȷ��ɾ��" class="input2">
&nbsp;&nbsp;&nbsp;&nbsp;
<input type="reset" value="��������" class="input2"></div>
</td></tr></table>
</td></tr></table>
</form>
</body></html>
HTMLEOF
}
#############
sub replay
  {
   dbmopen(%TEMP,"$datapath/$user.db",0666);
   %USERLIST = %TEMP;
   dbmclose(%TEMP);
   @userno=keys %USERLIST;
   @userno=sort @userno;
   $totalrecode = $#userno+1;
   $deleteyes = "del";
   print <<HTMLEOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>$title</title></head><body><center>
<form method="post" action="$cgiurl/gbook.cgi?action=replayok&user=$user&recode1=$FORM{'recode1'}">
<table width=230 align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont>�� �� �� ��</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
                <td width="30%" align="center">�����˺ţ�</td>
                <td width="70%">&nbsp;<!--$admin-->
&nbsp;<input type=text name=adminame size=20 class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="30%" align="center">�������룺</td>
                <td width="70%"><!--$password-->&nbsp;
&nbsp;<input type=password name=admipass size=20 class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="30%" align="center" colspan="2">
<textarea rows="6" name="tempre" cols="30" class=input3></textarea></td>
              </tr>
        <tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
              <input type="submit" value="ȷ�ϻظ�" class="input2">
              &nbsp;&nbsp;&nbsp;&nbsp;
              <input type="reset" value="��������" name="B1" class="input2"></div>
</td></tr></table>
</td></tr></table>
</form>

</body></html>




HTMLEOF
}

#############
sub replayok
  {
   if ((($FORM{'adminame'} eq $adminame) && ($FORM{'admipass'} eq $admipass)) || (($FORM{'adminame'} eq $admin) && ($FORM{'admipass'} eq $password)))
      {
       dbmopen(%USERLIST,"$datapath/$user.db",0666);
       @userno=keys %USERLIST;
       @userno=sort @userno;
       $totalrecode = $#userno+1;
       for ($inti = $totalrecode-1;$inti >= 0;$inti--)
         {
          $tempint=$inti+1;
          $tempnum = "recode$tempint";
          $tempno=$FORM{$tempnum};
          $tempjob = "job$tempint";
          $tmpjob  = $FORM{$tempjob};
          $tempre  = "re$tempint";
          $tmpre   = $FORM{$tempre};
          if ($tempno ne "")
            {
             foreach (@userno)
               {
               	if ($tempno eq $_)
                  {
             ($mark,$name,$email,$place,$photo,$texti,$url,$fromwhere,$date_time,$oicq,$posticons,$markend,$last)=split(/��/,$USERLIST{$tempno});
             $textireturn=$texti;
             $tmpre =~ s/\n/<br>/g;
             $tmpre =~ s/ /&nbsp;/g;
             $texti="$texti<br>&nbsp;&nbsp;&nbsp;&nbsp;<font size=2 color=$adminfont>�������ظ�����</font><font size=2 color=$adminfontny>$FORM{'tempre'}</font>";
             $USERLIST{$tempno} = "start��$name��$email��$place��$photo��$texti��$url��$fromwhere��$date_time��$oicq��$posticons��end��\n";
             $tmpre =~ s/<br>/\n/g;
             $tmpre =~ s/&nbsp;/ /g;
             &mailadmin;
                  }
               }
            }
         }
dbmclose(%USERLIST);
print <<EOF;
<html>
<head>
<title></title>
<BODY bgcolo=$gbbgcolor $gbbody>
<meta HTTP-EQUIV="REFRESH" CONTENT="3;URL=$cgiurl/gbook.cgi?user=$user">
$pagestyle
</head>
<ul><center>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">
  <h2>
  ��ȴ� ϵͳ���ڴ������������Ϣ..... <br>
  �ظ��ɹ�,3������ǽ����㷵��������Ա�����ҳ.<br>
  ���ϵͳû�з�Ӧ�밴��������ӷ������Ա���<br>
  <a href=$cgiurl/gbook.cgi?user=$user>�����ҵ����Ա�</a>
  </h2>
</p>

  <p align="center">
</html>
EOF
}else{
print <<EOF;
<html>
<head>
<title></title>
<BODY bgcolo=$gbbgcolor $gbbody>
<meta HTTP-EQUIV="REFRESH" CONTENT="3;URL=$cgiurl/gbook.cgi?user=$user">
$pagestyle
</head>
<ul>
<p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">
  <h2>��&nbsp;&nbsp;&nbsp;&nbsp;��<br>
  ��ȴ� ϵͳ���ڴ������������Ϣ..... <br>
  �û������������,3������ǽ����㷵��������Ա�����ҳ.<br>
  ���ϵͳû�з�Ӧ�밴��������ӷ������Ա���<br>
  <a href=$cgiurl/gbook.cgi?user=$user>�����ҵ����Ա�</a>
  </h2>
</p>

</html>
EOF
     }
  }
#############
sub write
   {
print qq(
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>$home</title></head>
<body bgcolor="$gbbgcolor" $gbbody>
<form name=form method="POST" action="$cgiurl/gbook.cgi?action=add&user=$user">
<script>
function emoticon(theSmilie){
document.form.texti.value += theSmilie + ' ';
document.form.texti.focus();
}
</SCRIPT>
<SCRIPT src=$images/code.js></SCRIPT>
<table width=70% align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont><B>ǩ  д  ��  ��</b></font></div>
          </td>
        </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>���Ա��⣺</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="place" size="35" maxlength="40" class="input2">
                  * ���ó��� 20 ������
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>�������֣�</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="name" size="25" maxlength="50" class="input2"> *
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>�����ʼ���</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="email" size="25" maxlength="30" class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>OICQ���룺</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="oicq" size="25" maxlength="50" class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>��ҳ��ַ��</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="url" size="25" maxlength="50" value="http://" class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>��ǰ���飺</b><br>��ͼ�����������Ӧ������ͼ�꼴��</td>
                <td width="77%" valign=top>);

     open (FILE, "$cgiabs/info/post.cgi");
     my @posticondata = <FILE>;
     close (FILE);
     chomp @posticondata;

    $tempiconnum=1;
    $tempselect = "checked";
    foreach $picture (@posticondata) {
       if ($tempiconnum > 10) {
    	   $tempiconnum = 1;
    	   print qq~<BR>~;
                              }
       print qq(<input type=radio value="$picture" name="posticon" $tempselect><a href="javascript:emoticon('[img]$images/posticons/$picture\[/img]');"><img src=$images/posticons/$picture border=0></a>&nbsp;);
       $tempiconnum ++;
       $tempselect = "";
                                     }

     print qq(</td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>ѡ��ͷ��</b></td>
                <td width="77%">&nbsp;&nbsp;<select name="photo">
				<option value=01 selected>ͷ��01
				<option value=02>ͷ��02
				<option value=03>ͷ��03
				<option value=04>ͷ��04
				<option value=04>ͷ��05
				<option value=05>ͷ��06
				<option value=07>ͷ��07
				<option value=08>ͷ��08
				<option value=09>ͷ��09
				<option value=10>ͷ��10
				<option value=11>ͷ��11
				<option value=12>ͷ��12
				<option value=13>ͷ��13
				<option value=14>ͷ��14
				<option value=15>ͷ��15
				<option value=16>ͷ��16
				<option value=17>ͷ��17
				<option value=18>ͷ��18
				<option value=19>ͷ��19
				<option value=20>ͷ��20
				</select>
                  <a href=$cgiurl/avatarslist.cgi target=_blank>�鿴ͷ���б�</a></td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>�������ݣ�</b></td>
                <td width="77%" align=center>$insidejs<br>
<TEXTAREA rows=6 name=texti cols=64 class=input3 wrap=hard></TEXTAREA>
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>�������ܣ�</b></td>
                <td width="77%">
<input type=checkbox value=on name=qqtoad> ���Ļ�&nbsp;&nbsp;
<input type=checkbox value=on name=writetoad> �����Է��͸�����
                </td>
              </tr>
        <tr>
          <td bgcolor=$btbgcolor colspan="2"><div align="center">
<input type=submit value=ǩд���� class=input2 name=submit1>&nbsp;&nbsp;&nbsp;&nbsp;
<input type=button name=ok class=input2 value=�鿴���� onclick=javascript:history.go(-1)></div></td>
        </tr>
      </table>
    </td></tr></table>

</form>

<p align="center" class="newfont6">������Ա���
<a href=$homeurl target=_blank><b>$home</b></a></font>
<font color=#cc0033></font>�ṩ ����֧�֣�<a href=http://www.homecgi.com target=_blank><b>Ajie</b></a></p>
</body>
);
}
#############
sub mypath{
local
$temp;
$temp=__FILE__;
$temp=~ s/\\/\//g if ($temp=~/\\/);
if ($temp) {$mypath=substr($temp,0,rindex($temp,"/"));}
else{
$mypath=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
$mypath=~ s/\\/\//g;}
return
$mypath;
}
#############
sub delok
  {
   if ((($FORM{'adminame'} eq $adminame) && ($FORM{'admipass'} eq $admipass)) || (($FORM{'adminame'} eq $admin) && ($FORM{'admipass'} eq $password)))
      {

          $tempint=$inti+1;
          $tempnum = "recode$tempint";
          $tempno=$FORM{$tempnum};
          $tempjob = "job$tempint";
          $tempre  = "re$tempint";
          $tmpre   = $FORM{$tempre};
       dbmopen(%USERLIST,"$datapath/$user.db",0666);
       @userno=keys %USERLIST;
       @userno=sort @userno;
       $totalrecode = $#userno+1;
       delete $USERLIST{$tempno};
       dbmclose(%USERLIST);
print <<EOF;
<html>
<head>
<title>$home</title>
<BODY bgcolo=$gbbgcolor $gbbody>
<meta HTTP-EQUIV="REFRESH" CONTENT="3;URL=$cgiurl/gbook.cgi?user=$user">
$pagestyle
</head>
<ul><center>
<p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">
  <h2>
  ��ȴ� ϵͳ���ڴ������������Ϣ..... <br>
  ɾ���ɹ�,3������ǽ����㷵��������Ա�����ҳ.<br>
  ���ϵͳû�з�Ӧ�밴��������ӷ������Ա���<br><br>
  <a href=$cgiurl/gbook.cgi?user=$user>�������Ա�</a>
  </h2>
</p>


</html>
EOF
     }
   else
     {
print <<EOF;
<html>
<head>
<title>$home</title>
<BODY>
$pagestyle
</head>
<ul><center>
<p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">��</p>
  <p align="center">
  <h2>&nbsp;&nbsp;����:&nbsp;&nbsp;<br>
  ��ȴ� ϵͳ���ڴ������������Ϣ..... <br>
  �û������������.<br><br>
  <input type=button name=ok class=input2 value=' �� �� ' �� onclick=javascript:history.go(-1)>
  </h2>
</p>

</html>
EOF
     }
  }