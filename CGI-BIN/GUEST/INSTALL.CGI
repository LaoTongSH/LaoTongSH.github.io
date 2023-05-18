#!/usr/bin/perl
#------------------------------------------------------#
#                                                      #
#              ±¾³ÌĞòÎª ÖĞ¹úCGIÖ®¼Ò Ìá¹©	           #
#              AjieµÄÁôÑÔ°å¶àÓÃ»§°æV4.0                #
#------------------------------------------------------#
&mypath;
&myurl;
$cgiabs=$mypath;
######################
## ÒÔÏÂ²¿·Ö²»ĞèĞŞ¸Ä ##
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
$ajie='AjieµÄÁôÑÔ±¾';
$home='ÖĞ¹úCGIÖ®¼Ò';
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
########## £¨µÚ¶ş²½£© ##########
print "Content-type: text/html\n\n";
print <<EOF;
<style>td {font-size:9pt}</style>
<title>AjieµÄÁôÑÔ±¾°²×°Ïòµ¼</title>
<body bgcolor="#fafdfd" text="#000000">
<form method="post"><input type="hidden" value="ok" name="menu">
<div align="center">
<table cellSpacing="0" borderColorDark="#ffffff" cellPadding="3" width="646" bgColor="#83C6C0" borderColorLight="#008000" border="1">
<tbody><tr><td width="628"><center><p><b><font color="#ffffff">AjieµÄÁôÑÔ±¾°²×°Ïòµ¼£¨µÚÒ»²½£©</font></b></p></center></td></tr><tr><td width="628">
<table width=627 bgColor=ECF6F5><tbody><tr bgColor=ECF6F5><td align=right width=186>Ö÷Ò³Ãû³Æ£º</td><td width=466><input name=homename size=25 value=$home></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>Ö÷Ò³µØÖ·£º</td><td width=466><input name=homeurl size=25 value=$homeurl></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>Õ¾³¤ĞÅÏä£º</td><td width=466><input name=adminmail size=25 value="$adminmail"></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>³¬¼¶ÓÃ»§Ãû£º</td><td width=466><input name=admname size=25 value=$admin></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>³¬¼¶ÓÃ»§ÃÜÂë£º</td><td width=466><input name=adpsd size=25></td></tr>
</tbody></table>
<table width=627 bgColor=ECF6F5><tbody>
<tr bgColor=ECF6F5><td align=right width=186>sendmail³ÌĞòµÄ¾ø¶ÔÂ·¾¶£º</td><td width=466><input name=mailprog size=40 value=$mailprog></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>ÁôÑÔ±¾Ä¿Â¼µÄURL£º</td><td width=466><input name=cgiurl size=40 value=$cgiurl></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>Í¼Æ¬Ä¿Â¼µÄURL£º</td><td width=466><input name=images size=40 value=$images></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>ÁôÑÔ±¾Ä¿Â¼µÄ¾ø¶ÔÂ·¾¶£º</td><td width=466><input name=cgiabs size=40 value=$cgiabs></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>dataÄ¿Â¼µÄ¾ø¶ÔÂ·¾¶£º</td><td width=466><input name=datapath size=40 value=$datapath></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>userÄ¿Â¼µÄ¾ø¶ÔÂ·¾¶£º</td><td width=466><input name=userpath size=40 value=$userpath></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>infoÄ¿Â¼µÄ¾ø¶ÔÂ·¾¶£º</td><td width=466><input name=infopath size=40 value=$infopath></td></tr>
<tr bgColor=ECF6F5><td align=right width=186>ipdataÄ¿Â¼µÄ¾ø¶ÔÂ·¾¶£º</td><td width=466><input name=ipdir size=40 value=$ipdir>
</td></tr>
</tbody></table>
</td></tr><tr><td width="628" align="center"><p><input type="submit" value="ÏÂÒ»²½"><font color="#ffffff"></font></td></tr>
<tr><td align="center" width="629"><font color="#ffffff">COPYRIGHT 2001 &copy; HOMECGI.COM
        ALL RIGHTS RESERVED Õ¾³¤£ºAjie QQ£º5858314 Email£ºwebmaster\@homecgi.com</font></td></tr></tbody></table></FORM></div>
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
if($FORM{'admname'} eq ""){&errorview("³¬¼¶ÓÃ»§Ãû²»ÄÜÃ»ÓĞÌîĞ´!");}
if($FORM{'admname'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?ÿ-]/){&errorview("Ãû×ÖÖĞ²»ÄÜº¬ÓĞÌØÊâ×Ö·û!");}
if($FORM{'adpsd'} eq ""){&errorview("³¬¼¶ÓÃ»§ÃûÃÜÂë²»ÄÜÃ»ÓĞÌîĞ´!");}
if($FORM{'adpsd'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?ÿ-]/){&errorview("ÃÜÂëÖĞ²»ÄÜº¬ÓĞÌØÊâ×Ö·û!");}
unless(-d "$datapath"){&errorview("  ÎŞ·¨´´½¨$datapathÕâ¸öÄ¿Â¼£¬ÇëÈ·¶¨CGI³ÌĞòÎÄ¼şµÄ¾ø¶ÔÂ·¾¶ÊÇ·ñÉèÖÃÕıÈ·,$cgiabsÄ¿Â¼ÊôĞÔÊÇ·ñÎª777£¡ ");exit;}
unless(-d "$userpath"){&errorview("  ÎŞ·¨´´½¨$userpathÕâ¸öÄ¿Â¼£¬ÇëÈ·¶¨CGI³ÌĞòÎÄ¼şµÄ¾ø¶ÔÂ·¾¶ÊÇ·ñÉèÖÃÕıÈ·,$cgiabsÄ¿Â¼ÊôĞÔÊÇ·ñÎª777£¡");exit;}
unless(-d "$ipdir"){&errorview("  ipdirÄ¿Â¼$ipdirµÄ¾ø¶ÔÂ·¾¶´íÎó£¬¸ÃÄ¿Â¼²»´æÔÚ! ");exit;}
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
########## £¨µÚ¶ş²½£© ##########
sub okok {
print "Content-type: text/html\n\n";
print <<EOF;
<style>td {font-size:9pt}</style>
<title>AjieµÄÁôÑÔ±¾°²×°Ïòµ¼</title>
<body bgcolor="#fafdfd" text="#000000" link="#ffffff">
<br><form method="post"><input type="hidden" value="ok" name="menu">  <div align="center">
<table cellSpacing="0" borderColorDark="#ffffff" cellPadding="3" width="400" bgColor="#83C6C0" borderColorLight="#008000" border="1">
<tbody><tr><td width="98%"><center><p><b><font color="#ffffff">AjieµÄÁôÑÔ±¾°²×°Ïòµ¼£¨µÚ¶ş²½£©</font></b></p></center></td></tr><tr><td width="100%">
<table width=100% bgColor=ECF6F5><tbody><tr bgColor=ECF6F5><td align=center width=100%><br>Çë¼ì²éÕâÕÅÍ¼Æ¬ÊÇ·ñÄÜÕı³£ÏÔÊ¾<br><br><img src=$FORM{'images'}/04.gif>
<br>
<p>Èç¹ûÕı³£µÄ»°£¬Çë½øĞĞÏÂÒ»²½</td></tr></tbody></table>
</td></tr><tr><td width="100%"><font color="#ffffff">
¢Ù£ºÈç¹ûÍ¼Æ¬ÏÔÊ¾²»ÕıÈ·£¬Çë <b><a href=javascript:history.back()>
<font color="#0000ff">·µ»Ø</font></a></b> ÖØĞÂÌîĞ´Í¼Æ¬Â·¾¶¡£<br>
¢Ú£ºÈç¹ûÄãµÄµÚÒ»´Î°²×°ÁôÑÔ±¾£¬µã»÷  <a href=install.cgi?menu=register><b>
<font color="#0000ff">ÕâÀï</font></b></a> ÉêÇëÁôÑÔ±¾¡£<br>
¢Û£ºÈç¹ûÄãÊÇÉı¼¶°²×°£¬Çëµã»÷ <a href=admin.cgi><b>
<font color="#0000ff">ÕâÀï</font></b></a> Ö±½Ó½øÈë¹ÜÀíÖĞĞÄ¡£</font>
</td></tr></tbody></td></tr></tbody></table></FORM></div>
EOF
exit;
}
########## £¨µÚÈı²½£© ##########
sub register {
require "$mypath/"."info/setup.cgi";
print "Content-type: text/html\n\n";
print <<EOF;
<style>td {font-size:9pt}</style>
<title>AjieµÄÁôÑÔ±¾°²×°Ïòµ¼</title>
<body bgcolor="#fafdfd" text="#000000" link=#ffffff>
<br><form method="post"><input type="hidden" value="adduser" name="menu"><div align="center">
<table cellSpacing="0" borderColorDark="#ffffff" cellPadding="3" width="400" bgColor="#83C6C0" borderColorLight="#008000" border="1">
<tbody><tr><td width="98%"><center><p><b><font color="#ffffff">AjieµÄÁôÑÔ±¾°²×°Ïòµ¼£¨µÚÈı²½£©</font></b></p></center></td></tr>
<tr><td width="98%"><center><p><b><font color="#ffffff">ÉêÇëÄúµÄÁôÑÔ±¾</font></b></p></center></td></tr>
<tr><td width="100%">
<table width=100% bgColor=ECF6F5><tbody>
<tr bgColor=ECF6F5><td align=right width=25%>ÓÃ »§ Ãû£º</td><td width=75%><input type="text" name="username" size="20" maxlength=8 value=$admin>* 1-8Î»£¨°æÖ÷ÓÃ»§Ãû£©</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>ÓÃ»§ÃÜÂë£º</td><td width=75%><input type="text" name="userpass" size=20 maxlength=8 value="$password">* °æÖ÷ÃÜÂë</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>ÖØ¸´ÃÜÂë£º</td><td width=75%><input type="text" name="userpass1" size="20" maxlength=8>* °æÖ÷ÃÜÂë</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>µç×ÓÓÊ¼ş£º</td><td width=75%><input type="text" name="emailaddress" size="20" value="$adminmail">* ÓÊ¼şµØÖ·£¨ÓÊ¼şÍ¨Öª£©</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>Ö÷Ò³µØÖ·£º</td><td width=75%><input type="text" name="homepage" value = "http://" size="20">* Ö÷Ò³µØÖ·</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>ÁôÑÔ±¾Ãû£º</td><td width=75%><input type="text" name="title" size="20" value="$homeÁôÑÔ±¾">* ÄãµÄÁôÑÔ±¾µÄÃû×Ö</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>Ã¿Ò³¼ÇÂ¼£º</td><td width=75%><input type="text" name="recode" size="20" value="$pagenum" maxlength="2">* Ä¬ÈÏÎª$pagenumÌõ</td></tr>
</tbody></table>
</td></tr><tr><td width="100%" align="center">
<input type=button name=back value="ÉÏÒ»²½" onclick=javascript:history.go(-1)>&nbsp;&nbsp;&nbsp;&nbsp;
<input type="submit" value="ÏÂÒ»²½" name=ok></td>
</tr><tr><td align="center" width="629"><font color="#ffffff">COPYRIGHT 2001 &copy; HOMECGI.COM
        ALL RIGHTS RESERVED <br>Õ¾³¤£ºAjie QQ£º5858314 ¼¼ÊõÖ§³Ö£º<a href=http://www.homecgi.com/lb5000/leoboard.cgi><font color=#FFFFFF>CGI¼¼ÊõÂÛÌ³</font></a></font></td></tr></tbody></td></tr></tbody></table></FORM></div>
EOF
exit;
}
########## £¨µÚËÄ²½£© ##########
sub adduser {
if($FORM{'username'} eq ""){&errorview("ÓÃ»§Ãû²»ÄÜÃ»ÓĞÌîĞ´!");}
if (length($FORM{'username'})>8) {&errorview("Ãû×Ö²»ÄÜ³¬¹ı8¸ö×Ö·û£¡");}
if($FORM{'username'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?ÿ-]/){&errorview("Ãû×ÖÖĞ²»ÄÜº¬ÓĞÌØÊâ×Ö·û!");}
if($FORM{'userpass'} eq ""){&errorview("ÓÃ»§ÃÜÂë²»ÄÜÃ»ÓĞÌîĞ´!");}
if($FORM{'userpass'}=~m/[\#\&\*\=\+\\\:\"\/\<\>\?ÿ-]/){&errorview("ÃÜÂëÖĞ²»ÄÜº¬ÓĞÌØÊâ×Ö·û!");}
if($FORM{'userpass'} ne "$FORM{'userpass1'}"){&errorview("Á½´ÎÊäÈëµÄÃÜÂë²»ÏàÍ¬!");}
if (($FORM{'userpass'} eq "") || ($FORM{'userpass1'} eq ""))
{&errorview("ÃÜÂë»òÈ·ÈÏÃÜÂë²»ÄÜÎª¿Õ, ÇëÖØĞÂÊäÈë!!");}
if (!($FORM{'emailaddress'} =~ /.*\@.*\..*/)){&errorview("ÄãÊäÈëÁËÒ»¸ö´íÎóµÄµç×ÓÓÊ¼şµØÖ·£¡£¡£¡");}
dbmopen(%USERFILE,"$userpath/alluser.db",0666);
foreach (%USERFILE)
{if ($_ =~ "¡¬$FORM{'username'}¡¬")
{&errorview("´ËÓÃ»§ÒÑ±»×¢²á!!Çë¸ü»»ÓÃ»§Ãû!!");}
if ($_ =~ "¡¬$FORM{'homepage'}¡¬"){&errorview("´ËÖ÷Ò³ÒÑ¾­×¢²á¹ı±¾ÁôÑÔ±¾!!²»ÄÜÍê³ÉÄúµÄÉêÇë!");}
if ($_ =~ "¡¬$FORM{'emailaddress'}¡¬"){&errorview("´ËĞÅÏäÒÑ¾­×¢²á¹ı±¾ÁôÑÔ±¾!!²»ÄÜÍê³ÉÄúµÄÉêÇë!!");}}
($sec,$min,$hour,$mday,$mon,$year)=localtime(time);
$mon           = $mon+1;
$year          = $year+1900;
$date_time  = sprintf ("%04d/%02d/%02d",$year,$mon,$mday);
$name   = $FORM{'username'};
$name =~ s/\&nbsp\;//ig;
$name =~ s/¡¡/ /g;
$name =~ s/©¡/ /g;
$name =~ s/[ ]+/ /g;
$name =~ s/\s*$//g;
$name =~ s/^\s*//g;
$name =~ s/ *$//g;
$name =~ s/^ *//g;
$name =~ s/[ ]+/ /;
$name =~ s/[ ]+/ /;
$name =~ s/ÿ//isg;
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
$USERFILE{$newuserno} = "start¡¬$name¡¬$pass¡¬$email¡¬$url¡¬$title¡¬$pagenum¡¬$ipaddress¡¬$date_time¡¬end¡¬\n";
dbmclose(%USERFILE);
print "Content-type: text/html\n\n";
print <<EOF;
<style>td {font-size:9pt}</style>
<title>AjieµÄÁôÑÔ±¾°²×°Ïòµ¼</title>
<body bgcolor="#fafdfd">
<br><form method="post"><input type="hidden" value="ok" name="menu">  <div align="center">
<table cellSpacing="0" borderColorDark="#ffffff" cellPadding="3" width="400" bgColor="#83C6C0" borderColorLight="#008000" border="1">
<tbody><tr><td width="98%"><center><p><b><font color="#ffffff">AjieµÄÁôÑÔ±¾°²×°Ïòµ¼£¨Íê³É£©</font></b></p></center></td></tr><tr><td width="100%">
<table width=100% bgColor=ECF6F5><tbody><tr bgColor=ECF6F5>
<td align=center width=100%><br><a href=admin.cgi>½øÈë¹ÜÀíÖĞĞÄ</a><br><br><a href=gbook.cgi?user=$name><font color="#000000">½øÈëÄúµÄÁôÑÔ±¾</font></a><br></td></tr></tbody></table>
</td></tr><tr><td align="center" width="100%"><font color="#ffffff">COPYRIGHT 2001 &copy; HOMECGI.COM
        ALL RIGHTS RESERVED <br>Õ¾³¤£ºAjie QQ£º5858314 ¼¼ÊõÖ§³Ö£º<a href=http://www.homecgi.com/lb5000/leoboard.cgi><font color=#FFFFFF>CGI¼¼ÊõÂÛÌ³</font></a></font></td></tr></tbody></td></tr></tbody></table></FORM></div>
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
    if (!(-e $mailprogram)) {$mailprogram="Ã»ÓĞÕÒµ½SendmailÂ·¾¶£¬¿ÉÄÜÄãµÄÖ÷»ú²»Ö§³Ö";};
    return $mailprogram;
}
##############################################
sub errorview {
&css;print "
<BODY background=$imagurl/bg.gif>
<TITLE>³ö´íÌáÊ¾</TITLE>
<TABLE  width=100% border=0>
<TBODY><TR align=middle><TD height=413 valign=middle align=center>
<TABLE cellSpacing=0 borderColorDark=#ffffff bgColor=#336666 borderColorLight=#000000 border=1 width=275><TBODY><TR><TD width=350>
<TABLE cellSpacing=0 cellPadding=2 width=100% bgColor=#83C6C0 border=0>
<TBODY><TR><TD width=100%><FONT color=#336666>¡è ³ö´íÌáÊ¾</FONT></TD><TD width=18>
<TABLE cellSpacing=0 borderColorDark=#ffffff cellPadding=0 bgColor=ECF6F5 borderColorLight=#666666 border=1><TBODY>
<TR><TD><B><font color=#336666>¡Á</font></B></TD></TR></TBODY></TABLE></TD>
</TR></TBODY></TABLE>
<TABLE cellPadding=4 width=100% bgColor=#ECF6F5 border=0><TBODY>
<TR><TD vAlign=top align=center width=47><FONT size=7 face=Wingdings color=#ff0000>L</FONT></TD><TD width=210><P><font size=2>$_[0]</font></P></TD></TR>
<TR><TD vAlign=top align=center colSpan=2 width=100%><div align=center><center>
<table border=1 bgColor=cccccc cellspacing=0><tr><td width=100% align=center bordercolordark=#E6E6E6 bordercolorlight=#cccccc><A href=javascript:history.back()><font size=2 color=#000000>¡¡È· ¶¨&nbsp;&nbsp;</font></A></td></tr></table></center></div></TD></TR></TBODY></TABLE></TD></TR></TBODY></TABLE></TD></TR></TBODY></TABLE></HTML>";exit;}
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