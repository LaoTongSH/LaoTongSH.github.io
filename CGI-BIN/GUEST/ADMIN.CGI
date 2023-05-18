#!/usr/bin/perl
#------------------------------------------------------#
# laotong/asd168                                                     #
#              ±¾³ÌĞòÎª ÖĞ¹úCGIÖ®¼Ò Ìá¹©	           #
#              AjieµÄÁôÑÔ°å¶àÓÃ»§°æV3.01               #
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
print qq(<FONT COLOR=#ff0000><B>°²È«¾¯¸æ</B>£º<br>install.cgi ÎÄ¼şÈÔÈ»ÔÚÄúµÄ·şÎñÆ÷ÉÏ£¬ÇëÂíÉÏÀûÓÃ FTP ¹¤¾ß½«ÆäÉ¾³ı£¡£¡<br> µ±ÄãÉ¾³ıÖ®ºó£¬Ë¢ĞÂ±¾Ò³ÃæÖØĞÂ½øÈë¹ÜÀíÖĞĞÄ¡£</FONT>);exit;}
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
if ($testcookie) {$cookie_result = qq(Cookies ÊÇ·ñ¿ÉÓÃ? <font color=#336666>== [Í¨¹ı]</font>);}
else {$cookie_result = qq(Cookies ÊÇ·ñ¿ÉÓÃ? <font color=#336666>== [Ê§°Ü]</font>);}
print qq(
<tr><td bgcolor="#73BAB4"><font face=ËÎÌå color=#FFFFFF>
                <b>»¶Ó­À´µ½ÁôÑÔ±¾¹ÜÀíÖĞĞÄ</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center>
                <font face=ËÎÌå color=#336666><b>»¶Ó­ $admin</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>

                <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left>
                <font face=ËÎÌå color=#336666>
                <center><br>
                ·şÎñÆ÷Ê±¼ä£º<b>$current_time</b><br>
                </center>
                <hr color=#DCECEA>
                 <font color=#336666 face=ËÎÌå>
                  <p> <b>ÁôÑÔ±¾Êı¾İÕªÒª</b><br>
                    <br>
                    <br>
                    ×¢²áÁôÑÔ±¾Êı£º$totalrecode ¸ö <br>
                    <br><br><br>
                    Ö÷»úÓòÃû&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;£º<font color=red>$ENV{'HTTP_HOST'}</font><br>
                    Ö÷»úIPµØÖ·&nbsp;&nbsp;&nbsp;&nbsp;£º<font color=red>$ENV{'SERVER_ADDR'}</font><br>
                    Ä¿Â¼Â·¾¶&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;£º<font color=#FF0000>$cgiabs</font> == [ÕıÈ·] <br>
                    Perl&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;°æ±¾£º<font color=#FF0000>$]</font> == [Í¨¹ı] <br>
                    Cookie &nbsp;&nbsp;&nbsp;²âÊÔ£º<font color=#FF0000>$cookie_result</font><br>
                    ·şÎñÆ÷²Ù×÷ÏµÍ³£º<font color=red>$^O</font>
                    <br>
                    <br>
                  <hr color=#DCECEA>
                  <font color=#336666 face=ËÎÌå>³ÌĞòÖÆ×÷£º<a href="mailto:webmaster\@homecgi.com">Ajie</a><br>
                  °æÈ¨ËùÓĞ£º<a href="http://www.homecgi.com">ÖĞ¹úCGIÖ®¼Ò</a></font> </font>
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
<tr><td bgcolor="#73BAB4" colspan="8"><font face=ËÎÌå color=#FFFFFF>
                <b>»¶Ó­À´µ½ÁôÑÔ±¾¹ÜÀíÖĞĞÄ</b>
                </td></tr>
                <tr>
                <td bgcolor=#ECF6F5 align=center colspan="8">
                <font face=ËÎÌå color=#336666><b>×¢²áÁôÑÔ±¾¹ÜÀí</b></font>£¨ÏÖÓĞÉêÇëÓÃ»§<b><font face=ËÎÌå color=#ff0000>$totalrecode</font></b>¸ö£©
                </td></tr>
                <tr><td bgcolor=#ECF6F5 colspan="8">
                </td>
                </tr><tr>
<form method="POST" action="$cgiurl/admin.cgi">
<tr bgcolor="#DCECEA" align="center">
<td width="1%" height="1" align="center">
<input type=hidden name="action" value="deluser"></td>
<td width="15%" height="1" align="center">ÁôÑÔ±¾Ãû</td>
<td width="5%" height="1" align="center">ÓÃ»§</td>
<td width="5%" height="1" align="center">ÃÜÂë</td>
<td width="25%" height="1" align="center">ÍøÕ¾µØÖ·</td>
<td width="12%" height="1" align="center">ÉêÇëÊ±¼ä</td>
<td width="15%" height="1" align="center">Ê¹ÓÃIPµØÖ·</td>
<td width="10%" height="1" align="center">ÁôÑÔÊı</td>
</tr>
HTML
$inti=0;
foreach (@userno)
  {
   ($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/¡¬/,$USER{$_});
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
<tr bgcolor="#DCECEA" align="center"><td colspan="8"><input type="submit" value="É¾ ³ı" name="B1"></td></tr></form></table>
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
<tr><td bgcolor="#73BAB4" colspan="2"><font face=ËÎÌå color=#FFFFFF>
                <b>»¶Ó­À´µ½ÁôÑÔ±¾¹ÜÀíÖĞĞÄ</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=ËÎÌå color=#336666><b>×¢²áĞÂµÄÁôÑÔ±¾</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<form method="post" action="$cgiurl/admin.cgi">
<input type=hidden name="action" value="adduser">
<tr bgColor=ECF6F5><td align=right width=25%>ÓÃ »§ Ãû£º</td><td width=75%><input type="text" name="username" size="20" maxlength=8 value=$admin>* 1-8Î»£¨°æÖ÷ÓÃ»§Ãû£©</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>ÓÃ»§ÃÜÂë£º</td><td width=75%><input type="text" name="userpass" size=20 value="$password">* °æÖ÷ÃÜÂë</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>ÖØ¸´ÃÜÂë£º</td><td width=75%><input type="text" name="userpass1" size="20">* °æÖ÷ÃÜÂë</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>µç×ÓÓÊ¼ş£º</td><td width=75%><input type="text" name="emailaddress" size="20" value="$adminmail">* ÓÊ¼şµØÖ·£¨ÓÊ¼şÍ¨Öª£©</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>Ö÷Ò³µØÖ·£º</td><td width=75%><input type="text" name="homepage" value = "http://" size="20">* Ö÷Ò³µØÖ·</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>ÁôÑÔ±¾Ãû£º</td><td width=75%><input type="text" name="title" size="20" value="$homeÁôÑÔ±¾">* ÄãµÄÁôÑÔ±¾µÄÃû×Ö</td></tr>
<tr bgColor=ECF6F5><td align=right width=25%>Ã¿Ò³¼ÇÂ¼£º</td><td width=75%><input type="text" name="recode" size="20" value="$pagenum" maxlength="2">* Ä¬ÈÏÎª$pagenumÌõ</td></tr>
<tr><td width="100%" bgcolor=#DCECEA align="center" colspan="2">
<input type="submit" value="Ìá½»ÉêÇë" name=ok>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td></tr></FORM>
</table></td></tr></table>
);
exit;}
############################################
sub adduser {
if($FORM{'username'} eq ""){&errorview("ÓÃ»§Ãû²»ÄÜÃ»ÓĞÌîĞ´!");}
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
print qq(
<tr><td bgcolor="#73BAB4" colspan="2"><font face=ËÎÌå color=#FFFFFF>
                <b>»¶Ó­À´µ½ÁôÑÔ±¾¹ÜÀíÖĞĞÄ</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=ËÎÌå color=#336666><b>×¢²á³É¹¦</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<tr bgColor=ECF6F5>
<td align=center width=100%><br><br><a href=gbook.cgi?user=$name>½øÈëÄúµÄÁôÑÔ±¾</a><br></td></tr>
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

                   ($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/¡¬/,$USERLIST{$tempno});
                   delete $USERLIST{$tempno};
                   unlink (<"$datapath/$name.*">);
                  }
               }
            }
         }
       dbmclose(%USERLIST);
print qq(
<tr><td bgcolor="#73BAB4" colspan="8"><font face=ËÎÌå color=#FFFFFF>
                <b>»¶Ó­À´µ½ÁôÑÔ±¾¹ÜÀíÖĞĞÄ</b>
                </td></tr>
<tr bgcolor="#DCECEA" align="center"><td><br>É¾³ı³É¹¦¡­¡­</td></tr></table>
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
    <tr><td bgcolor="#73BAB4" colspan="2"><font face=ËÎÌå color=#FFFFFF>
                <b>»¶Ó­À´µ½ÁôÑÔ±¾¹ÜÀíÖĞĞÄ</b>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=ËÎÌå color=#336666><b>¡è ³ö ´í Ìá Ê¾</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5 colspan="2">
                </td>
                </tr>
<tr><td align=center>
<FONT size=7 face=Wingdings color=#ff0000>L</FONT><P><font size=2>$_[0]</font></P></td></tr>
<tr><td colSpan=2 width=100%><div align=center><center>
<table border=1 bgColor=cccccc cellspacing=0><tr><td width=100% align=center bordercolordark=#E6E6E6 bordercolorlight=#cccccc><A href=javascript:history.back()><font size=2 color=#000000>¡¡È· ¶¨&nbsp;&nbsp;</font></A>
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
