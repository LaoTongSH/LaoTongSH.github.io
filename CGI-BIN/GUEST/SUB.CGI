#------------------------------------------------------#
#                                                      #
#              ������Ϊ �й�CGI֮�� �ṩ	           #
#              Ajie�����԰���û���V4.0                #
#------------------------------------------------------#
##################################
sub gotopage{
$gotourl = $FORM{'gotourl'};
print <<EOF ;
<html>
<head>
<title>$title</title>
</head>
<body>
<meta HTTP-EQUIV="REFRESH" CONTENT="1;URL=$cgiurl/gbook.cgi?user=$user&page=$gotourl">
</body>
</html>
EOF
exit ;
}
########################################################
sub ipwhere {
    my $fromwhere = shift;
    my $datapath="$ipdir";
    (my $ip1,my $ip2,my $ip3,my $ip4)=split(/\./,$fromwhere);
    my $ips=$ip1*1000000000+$ip2*1000000+$ip3*1000+$ip4;
    $ip1=int($ip1);
    if (-f "$datapath/$ip1.txt") {
        $datafile=$datapath."/".$ip1.".txt";
    }
    else {
        $datafile=$datapath."/other.txt";
    }
    my $from1='';
    my $from2='';
    open(IPF,"$datafile");
    my @ipdata=<IPF>;
    close(IPF);
    for ($i=0;$i<@ipdata;$i++){
        ($ip1,$ip2,$from1,$from2)=split(/__/,$ipdata[$i]);
        (my $ipa1,my $ipa2,my $ipa3,my $ipa4)=split(/\./,$ip1);
        (my $ipb1,my $ipb2,my $ipb3,my $ipb4)=split(/\./,$ip2);
        my $ipbegin =$ipa1*1000000000+$ipa2*1000000+$ipa3*1000+$ipa4;
        my $ipend =$ipb1*1000000000+$ipb2*1000000+$ipb3*1000+$ipb4;
        if (($ips<=$ipend)&&($ips>=$ipbegin)) {
            last;
        }
    }
    if ($from1 eq "") { $fromwhere="δ֪����"; }
    else {$fromwhere="$from1$from2";}
    return $fromwhere;
}
#############
sub mailadmin
  {
   $texti       =~ s/&nbsp;/ /g;
   $textireturn =~ s/&nbsp;/ /g;
   if ($sendusermail eq "YES")
   {
    if ($email ne "����")
    {
   open (MAIL, "|$mailprog $email");
   print MAIL "Reply-to:\n";
   print MAIL "Cc: softwt\@21cn.com\n";
   print MAIL "From: $ajiegbmail\n";
   print MAIL "Subject: лл����$title������\n\n";
   print MAIL "�𾴵�$name����,�ǳ���л����$title�����ԡ� \n";
   print MAIL "------------------------------------------------------\n";
   print MAIL "������ҳ��ַ��: $url\n";
   print MAIL "����IP��ַ��  : $ipaddress\n";
   print MAIL "���ĵ�ַ��  : $fromwhere\n";
   print MAIL "�����Ե�ʱ����: $date_time\n";
   print MAIL "��������������:\n\n";
   print MAIL "    $texti\n\n";
   print MAIL "                                  ��ӭ�ٴι��ٱ���վ!!\n\n";
   print MAIL "                     $title    $ajiebookurl\n";
   print MAIL "                                  E-MAIL: $ajiegbmail\n";
   print MAIL "------------------------------------------------------\n";
   print OUTMAIL "������Ա������� $home($homeurl) �ṩ������֧��:�й�CGI֮��(http://www.homecgi.com)\n";
   close (MAIL);
     }
   }
  }
#############
sub checknull
  {
   if ($_[0] eq "")
     {
      &errorinput($_[1]);
     }
   else
     {
      if ($allow_html ==0)
        {
         $return=&filterhtml($_[0]);
        }
      else
        {
         $return=$_[0];
        }
     }
   return $return;
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
sub sendmail
{
open (MAIL, "|$mailprog $email");
if ($mailtoadmin eq "YES")
 {
  print MAIL "Reply-to: $adminmail\n";
 }
else
 {
  print MAIL "Reply-to:\n";
 }
print MAIL "From: $adminmail\n";
print MAIL "Subject: ���Ա���֪ͨͨ��\n\n";
print MAIL "�𾴵�$name����,�ǳ���л��������$home($homeurl)�����Ա�����\n";
print MAIL "------------------------------------------------------\n";
print MAIL "�����û�����    :$name\n";
print MAIL "���Ĺ���������  :$pass\n";
print MAIL "������İ�����  :$title\n";
print MAIL "ÿҳ��¼��      :$pagenum\n";
print MAIL "��EMAIL��ַ     :$email\n";
print MAIL "������ҳ��ַ    :$url\n";
print MAIL "���������鿴���Ա�Ӧ�����HTMLԴ����:\n\n";
print MAIL "$cgiurl/gbook.cgi?user=$name\n";
print MAIL "�����Ǹ�������ҳ��Ӧ�����HTMLԴ����:\n\n";
print MAIL "$cgiurl/gbook.cgi?action=write&user=$name\n";
print MAIL "������ͨ�������˺��޸��������Ա�, ��ӭ�ٴι��ٱ���վ!!\n";
print MAIL "�뽫��վ���뵽����������, �������������ӻ�����ҳ����!!\n\n";
print MAIL "           ��ʲô������E-MAIL����: $adminmail\n";
print MAIL "------------------------------------------------------\n";
print MAIL "������Ա������� $home($homeurl) �ṩ������֧��:�й�CGI֮��(http://www.homecgi.com)\n";
close (MAIL);
}
##############################################
sub header{print "Content-type: text/html\n\n";}
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
    if (!(-e $mailprogram)) {$mailprogram="û���ҵ� Sendmail ·�����������������֧��";};
    return $mailprogram;
}
##############################################
sub admintitle {
     print qq(
    <html>
    <head>
    <title>���Ա���������</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
    <style type="text/css">
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}

	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
    </style>
    <script language="javascript">
    function save_changes() {
    document.the_form.process.value="true";
    }
    function preview_template() {
    document.the_form.target="_blank";
    document.the_form.process.value="preview template";
    }
    </script>
    </head>
    <body bgcolor="#83C6C0" text="#336666" link="#336666" vlink="#333333" topmargin=5 leftmargin=15>
    <table width=100% cellpadding=0 cellspacing=1 border=0 height="300" bgcolor="#336666">
        <tr><td width=22% valign=top bgcolor=#ECF6F5>
            <table width=100% cellpadding=6 cellspacing=0 border=0>
              <tr>
                <td bgcolor="#73BAB4"><font face=���� color=#FFFFFF> <b>�����˵�</b>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5><font face=���� color=#336666> >> <a href="$cgiurl/admin.cgi">����������ҳ</a> << <br>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#DCECEA"><font face=���� color=#336666><b>���Ա�����</b>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#ECF6F5"><font face=���� color=#336666> >> <a href="$cgiurl/admin.cgi?action=register">�������Ա�</a><br> >> <a href="$cgiurl/admin.cgi?action=supervision">ע�����Ա�����</a>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#DCECEA"><font face=���� color=#336666><b>�������ݹ���</b>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#ECF6F5"><font face=���� color=#336666>
                  >> ɾ������<br>
                  >> �������<br>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#DCECEA"><font face=���� color=#336666><b>���ù���</b> </font></td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5><font face=���� color=#336666>>> <a href="./setvar.cgi">������������</a><br>
                  >> <a href="./setstyle.cgi">���Ա��������</a><br>
                  >> <a href="./settemplate.cgi">�༭���Ա�ģ��</a>
                  </font></td>
              </tr>
              <tr><td bgcolor="#DCECEA"><font face=���� color=#336666><b>��������</b> </font></td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5><font face=���� color=#336666>
                  >> <a href="./loginlogs.cgi">��������ȫ��־</a><br>
                  >> ���Ա��汾/����<br>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#DCECEA"><font face=���� color=#336666><b>���Ա� ��Ϣ</b>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5 align=left> <span class="large">�汾��</span><span class="body">Ajie�����Ա�
                  V4.0 </span>
                  <p> <font face=���� color="#336666"> ���İ�Ȩ���У� <a href="http://www.homecgi.com/" target=_blank>�й�CGI֮��</a><br>
                    ����֧����̳�� <a href="http://www.homecgi.com/lb5000/leoboard.cgi" target="_blank">CGI������̳</a>
                    </font>
                </td>
              </tr>
            </table>
</td><td width=75% valign=top bgcolor=#ECF6F5>
    <table width=100% cellpadding=6 cellspacing=0 border=0>
);
}
##############################################
sub adminlogin {
    $current_time = localtime;
    print qq(
    <tr><td bgcolor="#73BAB4" colspan="2"><font face=���� color=#FFFFFF>
                <b>��ӭ�������Ա���������</b>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=���� color=#336666><b>�� �� Ա �� ½</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5 colspan="2">
                </td>
                </tr>

                <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left colspan=2>
                <font face=���� color=#336666>
                <center><br>
                ������ʱ�䣺<b>$current_time</b><br>
                </center>
                <hr color=#DCECEA></tr>
             <form method="POST" action="$cgiurl/admin.cgi">
             <input type=hidden name="action" value="login">
              <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left width="39%">
                  <div align="right">�����˺ţ�</div>
                </td>
                <td bgcolor=#ECF6F5 valign=middle align=left width="61%">&nbsp;
                  <input type=text name=adminname size=20>
                </td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left width="39%">
                  <div align="right">�������룺</div>
                </td>
                <td bgcolor=#ECF6F5 valign=middle align=left width="61%">&nbsp;
                  <input type=password name=adminpass size=20>
                </td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left colspan="2">
                  <div align="center"><font face=���� color=#336666>
                    <input type="submit" value="������½">
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <input type="reset" value="��������" name="B1">
                    </font></div>
                </td>
              </tr>
              </form><tr>
                <td bgcolor=#ECF6F5 valign=middle align=left colspan="2">
                  <p><font face=���� color=#336666><font color=#336666 face=����>��ע��<br>
                    ֻ����̳��̳�����ܵ�½��̳�������ġ�<br>
                    δ������Ȩ�ĳ��Ե�½��Ϊ���ᱻ��¼�ڰ���</font></font></p>
                  <p>�ڽ�����̳��������ǰ����ȷ�������������� Cookie ѡ�<br>
                    Cookie ֻ������ڵ�ǰ������������С�Ϊ�˰�ȫ���������ر����������Cookie ��ʧЧ�����Զ�ɾ����<br>
                  </p>
                  <p><font face=���� color=#336666>����������<a href="mailto:webmaster\@homecgi.com">Ajie</a><br>
                    ��Ȩ���У�<a href="http://www.homecgi.com">�й�CGI֮��</a></font>
                  </p>
               </td></tr></table></td></tr></table>
);
exit;}
##############################################
sub parseadminform {
if ($ENV{'REQUEST_METHOD'} eq "POST")
{read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'});}
else{$buffer=$ENV{'QUERY_STRING'};}
@pairs = split(/&/, $buffer);
   foreach $pair (@pairs) {
   ($name, $value) = split(/=/, $pair);
   $value =~ tr/+/ /;
   $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
   $value=~s/\t/--/g;
   $value=~s/\n/\<br\>/g;
   $value =~ s/<!--(.|\n)*-->//g;
   $value =~ s/<([^>]|\n)*>//g;
   $FORM{$name} = $value;
}
@querys = split(/&/, $ENV{'QUERY_STRING'});
foreach $query (@querys) {
($name, $value) = split(/=/, $query);
$FORM{$name} = $value;   }
}
#############
sub errorinput
  {&pagestyle;
print qq(
<html>
    <head>
    <title>������Ϣ</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
    </head>
    <body bgcolor="$gbbgcolor" $gbbody>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor>
            <div align="center"><font color=$btfont>������Ϣ</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
                <td width="30%" align="center">$_[0]<br></td>
              </tr>
        <tr><td bgcolor=$btbgcolor><div align="center">
<input type=button name=ok class=input2 value=' �� �� ' onclick=javascript:history.go(-1)></div>
</td></tr></table>
</td></tr></table>
);
   exit;
  }
############################################
sub pagestyle{
   $templatefile = "$mypath/info/template.cgi";
   open (TEMPLATE, "$templatefile");
   local $/ = undef;
   $template_data = <TEMPLATE>;
   close (TEMPLATE);
$template_data =~ s/\&lt;/</g;
$template_data =~ s/\&gt;/>/g;
$template_data =~ s/ \&nbsp;/��/g;
$template_data =~ s/\&amp;/\&/g;
$pagestyle = qq($template_data);
return $pagestyle;
}
sub getdate{
($no,$no,$no,$day,$month,$year)= localtime(time);
$month++;
if($month <10){$month="0".$month;}
if($day<10){$day="0".$day;}
$year=$year+1900;
$date=$year."-".$month."-".$day;
}
sub gettime{
($sec,$min,$hour,$no,$no,$no)= localtime(time);
if($sec<10){$sec="0".$sec;}
if($min<10){$min="0".$min;}
if($hour<10){$hour="0".$hour;}
$time=$hour.":".$min.":".$sec;
}
######################################################
sub code {
    my $signature = shift;

	$signature =~ s/\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<img src=$1:\/\/$2 border=0>/isg;
    $signature =~ s/\<p>/<br><br>/isg;
    $signature =~ s|\[\[|\{\{|g;
    $signature =~ s|\]\]|\}\}|g;
    $signature =~ s|\n\[|\[|g;
    $signature =~ s|\]\n|\]|g;
    $signature =~ s|<br>| <br>|g;
    $signature =~ s|\[hr\]\n| |g;
    $signature =~ s|\[hr\]| |g;
    $signature =~ s/\[br\]/<br>/isg;
    $signature =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]/$1$2<br>$3<br>/isg;
    $signature =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]/$1/isg;
    $signature =~ s/\[url\](\[\S+\])(\S+?)(\[\S+\])\[\/url\]/<a href=$2 target=_blank>$1$2$3<\/a>/isg;
    $signature =~ s/\[url=(http|https|ftp):\/\/(\S+?)\]/<a href=$1:\/\/$2 target=_blank>/isg;
    $signature =~ s/\[url=(\S+?)\]/<a href=http:\/\/$1 target=_blank>/isg;
    $signature =~ s/\[url=\s*(.*?)\s*\]\s*(.*?)\s*\[\/url\]/<a href=$1 target=_blank>$2<\/a>/isg;
    $signature =~ s/\[url\]\s*(http|https|ftp):\/\/(.*?)\s*\[\/url\]/<a href=$1:\/\/$2 target=_blank>$1:\/\/$2<\/a>/isg;
    $signature =~ s/\[url\]\s*(.*?)\s*\[\/url\]/<a href=http:\/\/$1 target=_blank>$1<\/a>/isg;
    $signature =~ s/\[\/url\]/<\/a>/isg;
    $signature =~ s/(\[email\])(\S+\@\S+?)(\[\/email\])/<A HREF="mailto:$2">$2<\/A>/isg;
    $signature =~ s/\ (http|https|ftp):\/\/(\S+?)\ / <a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
    $signature =~ s/<br>(http|https|ftp):\/\/(\S+?)\ /<br><a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
    $signature =~ s/^(http|https|ftp|rtsp):\/\/(\S+?)\ /<a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
    $signature =~ s/\ www\.(\S+?)\ / <a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
    $signature =~ s/<br>www\.(\S+?)\ /<br><a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
    $signature =~ s/^www\.(\S+?)\ /<a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
    $signature =~ s/\[b\]/<b>/isg;
    $signature =~ s/\[\/b\]/<\/b>/isg;
    $signature =~ s/\[i\]/<i>/isg;
    $signature =~ s/\[\/i\]/<\/i>/isg;
    $signature =~ s/\[font=\s*(.*?)\s*\]\s*(.*?)\s*\[\/font\]/<font face=$1>$2<\/font>/isg;
    $signature =~ s/\[u\]/<u>/isg;
    $signature =~ s/\[\/u\]/<\/u>/isg;
    $signature =~ s/\[color=(\S+?)\]/<font color=$1>/isg;
    $signature =~ s/\[\/color\]/<\/font>/isg;
    $signature =~ s/\\(http|https|ftp):\/\/(\S+)/<a href=$1:\/\/$2 target=_blank>$1:\/\/$2<\/a>/isg;
    $signature =~ s/\[code\](.+?)\[\/code\]/$1/isg;
    $signature =~ s/\\(\S+?)\@(\S+)/<a href=mailto:$1\@$2\>$1\@$2<\/a>/ig;
    $signature =~ s/\[email=(\S+?)\]/<a href=mailto:$1>/isg;
    $signature =~ s/\[\/email\]/<\/a>/isg;
    $signature=~ s/<br>(\w+\@\w+\.\w+)/<br><A HREF=mailto:$1>$1<\/A>/isg;
    $signature =~ s/^(\w+\@\w+\.\w+)/<A HREF=mailto:$1>$1<\/A>/isg;
    $signature =~ s/\\(\w+\@\w+\.\w+)/<A HREF=mailto:$1>$1<\/A>/isg;
    $signature =~ s/(\[fly\])(.+?)(\[\/fly\])/<marquee width=90% behavior=alternate scrollamount=3>$2<\/marquee>/isg;
    $signature =~ s/(\[s\])(.+?)(\[\/s\])/<s>$2<\/s>/isg;
    $signature =~ s/(\[sup\])(.+?)(\[\/sup\])/<sup>$2<\/sup>/isg;
    $signature =~ s/(\[sub\])(.+?)(\[\/sub\])/<sub>$2<\/sub>/isg;
    $signature =~ s/(\[align=)(left|center|right)(\])(.+?)(\[\/align\])/<DIV Align=$2>$4<\/DIV>/isg;
    $signature =~ s/(\[SHADOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/SHADOW\])/<table width=$2 style="filter:shadow\(color=$4\, direction=$6)">$8<\/table>/isg;
    $signature =~ s/(\[GLOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/GLOW\])/<table width=$2 style="filter:glow\(color=$4\, strength=$6)">$8<\/table>/isg;
    $signature =~ s/(\[BLUR=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/BLUR\])/<table width=$2 style="filter:blur\(Add=0, direction=$4\, strength=$6)">$8<\/table>/isg;
    $signature =~ s/(\[FLIPH\])(.+?)(\[\/FLIPH\])/<table style="filter:flipH">$2<\/table>/isg;
    $signature =~ s/(\[FLIPV\])(.+?)(\[\/FLIPV\])/<table style="filter:flipV">$2<\/table>/isg;
    $signature =~ s/(\[INVERT\])(.+?)(\[\/INVERT\])/<table style="filter:invert">$2<\/table>/isg;
    $signature =~ s/(\[xray\])(.+?)(\[\/xray\])/<table style="filter:xray">$2<\/table>/isg;
    $signature =~ s/(\[MOVE\])(.+?)(\[\/Move\])/<MARQUEE>$2<\/MARQUEE>/isg;

    $signature =~ s|\{\{|\[|g;
    $signature =~ s|\}\}|\]|g;
    $signature =~ s/\&amp;/\&/ig;
    $signature =~ s/&quot\;/\"/ig;
    $signature =~ s/ \&nbsp;/��/ig;
    $signature =~ s/apasswordcookie/apassword cookies/isg;
    $signature =~ s/adminpass/admin password/isg;
    $signature =~ s/document.cookie/documents .cookie/isg;
    $signature =~ s/file:\/\//�ļ�\:\/\//isg;
    $signature =~ s/javascript/java script/isg;
    return $signature;
}
1;