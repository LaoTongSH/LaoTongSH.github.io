#!/usr/bin/perl


#############################################################
BEGIN {
    $LBPATH = '.';
    my $pgm = $0;
    $pgm =~s/\\/\//g;
    $pgm =~s/^.*\/([^\/]+)$/$1/g;
    unless (-e $LBPATH.'/'.$pgm) {
        foreach ($0, $ENV{'SCRIPT_FILENAME'}, $ENV{'PATH_TRANSLATED'}) {
            s!\\!/!g; s/^(.*)\/[^\/]+$/$1/g;
            if (-e $_ . '/' .$pgm) { $LBPATH = $_; last; }
        }
    }
    unshift (@INC, "$LBPATH");
}
use LBCGI;
$LBCGI::POST_MAX=1024*150;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                    # Unbuffer the output

#############################################################

my $q = new LBCGI;

my $action = $q->param('action');
my $deluser = $q->param('deluser');
my $adduser = $q->param('adduser');
my $inmembername = $q->param('membername');
my $inpassword = $q->param('password');

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie");   }

&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
    $inmembername = "客人";
    }

if ($inmembername eq "客人") {
	&loginbl;
} else {
	&action;
}



sub action {
if ($action eq "adduser") { &adduser($adduser); }
elsif ($action eq "deluser") { &deluser($deluser); }
else { &list; }
}

sub adduser {

&getmember($adduser);
if ($emailaddress) {

$memberfiletitle = $inmembername;
$memberfiletitle =~ s/ /_/g;
$memberfiletitle =~ tr/A-Z/a-z/;

$deluser =~ s/\+/ /;

$filetomake = "$lbdir" . "memfriend/${memberfiletitle}.cgi";
if (-e $filetomake) {
	open(FILE, "$filetomake");
	@currentlist = <FILE>;
	close (FILE);
}

unless (grep(/^$adduser$/, @currentlist)) {
push (@currentlist, $adduser);
}

if (open(FILE, ">$filetomake")) {
flock(FILE, 2) if ($OS_USED eq "Unix");
foreach $user (@currentlist) {
	chomp($user);
	print FILE "$user\n";
}
close(FILE);
}

&list;
} else {
errorbl("没有该注册用户！");
}
} ### end adduser

sub deluser {

$memberfiletitle = $inmembername;
$memberfiletitle =~ s/ /_/g;
$memberfiletitle =~ tr/A-Z/a-z/;

$deluser =~ s/\+/ /;

$filetomake = "$lbdir" . "memfriend/${memberfiletitle}.cgi";
if (-e $filetomake) {
	open(FILE, "$filetomake");
	@currentlist = <FILE>;
	close (FILE);
} else {
	errorbl("你的好友列表为空！");
}

if (open(FILE, ">$filetomake")) {
flock(FILE, 2) if ($OS_USED eq "Unix");
foreach $user (@currentlist) {
	chomp($user);
	unless ($user eq $deluser) {
	print FILE "$user\n";
	}
}
close(FILE);
}

&list;

} ### end deluser

sub list {
&getmember("$inmembername");

if ($userregistered eq "no") { &error("你没有注册！"); exit; }
elsif ($inpassword ne $password) { &error("你的密码错误."); exit; }
elsif ($inmembername eq "") { &loginbl; exit; }

$output .= qq~<html>
<head>
<script type="text/javascript">
function openScript(url, width, height) {
        var Win = window.open(url,"openwindow",'width=' + width + ',height=' + height + ',resizable=1,scrollbars=yes,menubar=yes,status=yes' );
}
</script>
<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline 	}
		A:link 	  {	text-decoration: none;}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}

</style>
<title>$inmembername - 好友列表</title>
</head>
<body bgcolor="#D1D9E2"  alink="#333333" vlink="#333333" link="#333333" >
<center>$inmembername 的好友列表</center><br>
<table width=97% align=center cellspacing=0 cellpadding=1  border=0 bgcolor=#333333>
		<tr><td>
<table width=100% cellspacing=0 cellpadding=4 border=0>
~;

$memberfiletitle = $inmembername;
$memberfiletitle =~ s/ /_/g;
$memberfiletitle =~ tr/A-Z/a-z/;

$filetomake = "$lbdir" . "memfriend/${memberfiletitle}.cgi";
if (-e $filetomake) {
	open(FILE, "$filetomake");
	@currentlist = <FILE>;
	close (FILE);
}



$colspant = "7";
$colspans = "5";

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t好友列表\tnone\t查看好友列表\t");
}

$output .= qq~
<tr>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>姓名</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>短消息</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>Email</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>ICQ</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>OICQ</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>主页</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>删除?</b></center></font></td>
</tr>
~;
$pmnamenumber = 0;
foreach $user (@currentlist) {
    chomp $user;
    &getmember($user);
    $memname = $membername;
    $memname =~ s/ /+/;
    $pmname = $membername;
    $pmname =~ s/ /_/;
    $duser = $user;
    $duser =~ s/ /+/;
$pmnamenumber++;
    if ($userregistered ne "no") {

	$homepage =~ s/http\:\/\///sg;

	if ($homepage) { $homepage = qq~<a href="http://$homepage" target="_blank"><img src="$imagesurl/images/homepage.gif" border=0></a>~; } else { $homepage = "N/A"; }
	if ($showemail eq "no"||$emailstatus eq "no"||$emailaddress eq ""||$showemail eq "msn"){
	    $emailaddress = "未输入" if ($$emailaddress eq "");
	    $emailaddress = "保密" if ($emailstatus eq "no");
	    $emailaddress = "保密" if ($showemail eq "no");
	    $emailaddress = "<a href=mailto:$emailaddress><img border=0 src=$imagesurl/images/msn.gif></a>" if ($showemail eq "msn");
	}
	else {$emailaddress = "<a href=mailto:$emailaddress><img border=0 src=$imagesurl/images/email.gif></a>" }

	if ($icqnumber) { $icqnumber = qq~<a href="javascript:openScript('$miscprog?action=icq&UIN=$icqnumber',450,300)"><img src="http://wwp.icq.com/scripts/online.dll?icq=$icqnumber&img=5" border=0></a>~; } else { $icqnumber = "N/A"; }
	if ($aolname) { $aolname = qq~<a href="javascript:openScript('http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$aolname',450,200)"><img src="$imagesurl/images/oicq.gif" border=0></a>~; } else { $aolname = "N/A"; }

	foreach $user (@onlinedata) {
           @userdetail = split (/\t/, $user);
           chomp @userdetail;
           if ($userdetail[0] eq $membername) {$online = qq~<IMG SRC=$imagesurl/images/online1.gif width=15 height=15 alt="该用户目前在线">~; last; }
           else { $online = qq~<IMG SRC=$imagesurl/images/offline1.gif width=15 height=15 alt="该用户目前不在线">~; }
       }

	$output .=qq~
	<tr>
	<td bgcolor=$miscbackone>$online <a href="$profileprog?action=show&member=$pmname">$user</a></td>
	<td bgcolor=$miscbackone><center><a href="javascript:openScript('$boardurl/messanger.cgi?action=new&touser=$pmname',600,400)"><img src="$imagesurl/images/message.gif" border=0></a></center></td>
	<td bgcolor=$miscbackone><center>$emailaddress</center></td>
	<td bgcolor=$miscbackone><center>$icqnumber</center></td>
	<td bgcolor=$miscbackone><center>$aolname</center></td>
	<td bgcolor=$miscbackone><center>$homepage</center></td>
	<td bgcolor=$miscbackone><center><form action=$boardurl/friendlist.cgi method=post name=pm$pmnamenumber><input type=hidden name=action value=deluser><input type=hidden name=deluser value=$duser><a href="javascript:document.pm$pmnamenumber.submit()">删除</a></center></td></form></tr>
	~;
    }
    else {
	$output .=qq~
	<tr>
	<td bgcolor=$miscbackone>$user (未注册)</td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone><center><form action=$boardurl/friendlist.cgi method=post name=pm$pmnamenumber><input type=hidden name=action value=deluser><input type=hidden name=deluser value=$duser><a href="javascript:document.pm$pmnamenumber.submit()">删除</a></center></td></form></tr>
	~;

    }
}

$output .= qq~
<tr>
<form action=$boardurl/friendlist.cgi method=post name=adduser><input type=hidden name=action value=adduser><td bgcolor=$miscbackone><font  color=black >好友姓名:</td><td colspan=$colspans bgcolor=$miscbackone><input type=text size=20 name=adduser></td><td bgcolor=$miscbackone><center><a href="javascript:document.adduser.submit()">增加</a></center></td></form>
<tr><td bgcolor=$miscbackone colspan=$colspant><center><font  color=black >输入你要想增加的好友姓名，点击增加确认操作！<br><br><a href=javascript:top.close();>[关闭窗口]</a></center></td></tr>
</table></td></tr>
	    </table>
</body>
</html>
~;

print header(-charset=>gb2312);
print "$output";
} ### end of list

sub errorbl {
$errormsg = shift;
$output = qq~
<html>
<head>
<title>$inmembername - 好友列表 >> 错误</title>
<meta http-equiv="refresh" content="30;URL=$boardurl/friendlist.cgi">
<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline 	}
		A:link 	  {	text-decoration: none;}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}

</style>
</head>
<body bgcolor="#D1D9E2"  alink="#333333" vlink="#333333" link="#333333">
<br>
<center>好友列表错误</center><br><br>
<font color=red>
<center>
<b>$errormsg</b>
</center>
</font>
<br><br>
<center><font color=$fontcolormisc> << <a href="javascript:history.go(-1)">返回上一页</a></center>

</body>
</html>
~;
print header(-charset=>gb2312);
print "$output";
}

sub loginbl {
$output .= qq~
<head>
<title>好友列表登陆</title>
<center>好友列表登陆</center><br>
<meta http-equiv="refresh" content="30">
<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline 	}
		A:link 	  {	text-decoration: none;}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}

</style>
</head>
<body bgcolor="#D1D9E2"  alink="#333333" vlink="#333333" link="#333333">
<font color=$titlefont>
<center>
你必须登陆才能察看你的好友列表<br><a href=loginout.cgi target=_blank>点这儿登陆</a>
</center>
</font>
</body>
</html>
~;
print header(-charset=>gb2312);
print "$output";
}