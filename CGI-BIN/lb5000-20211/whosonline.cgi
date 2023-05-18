#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / 雷傲超级论坛 ver.5000
#
#  版权所有: 雷傲工作室(原蓝宝石软件工作室)
#
#  制作人  : 山鹰糊 (Shining Hu)
#            花无缺 (Ifairy Han)
#           
#  主页地址: http://www.CGIer.com/      CGI 编程者之家
#	     http://www.LeoBoard.com/   雷傲论坛支持主页
#	     http://www.leoBBS.com/     本论坛直通车
#            http://mail@17do.com/      大家一起邮
#            
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
require "data/boardinfo.cgi";
require "data/progs.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "whosonline.cgi";

$query = new LBCGI;

&ipbanned; #封杀一些 ip

$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/\/$//;

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
    $inmembername = "客人";
}
else {
    &getmember("$inmembername");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
$membercodetemp = $membercode;

$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");
$current_time = time;
$current_time = &dateformatshort($current_time + ($timezone*3600) + ($timedifferencevalue*3600));

$helpurl = &helpfiles("在线用户");
$helpurl = qq~$helpurl<img src="$imagesurl/images/help_b.gif" border=0></a>~;

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\t在线用户\tnone\t查看在线用户状态\t");
}
$freshtime= $query->cookie("freshtime");
if ($freshtime ne "") {
    $autofreshtime = $freshtime*60-1;
    $refreshnow = qq~<meta http-equiv="refresh" content="$autofreshtime;">~;}
&title;
$output .= qq~
$refreshnow
  <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
    <tr>
        <td width=30% rowspan=2 valign=top><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td valign=middle align=left><font face="$font" color=$fontcolormisc>
            &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0>&nbsp;&nbsp;<a href="$forumsummaryprog">$boardname</a>
	        <br>
            &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0 width=15 height=15><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;当前在线用户 (最后更新时间：$current_time)
        </td>
        <tr>
        <td valign=bottom align=right>
&nbsp; $helpurl</td>
    </tr>
  </table>
  <p>
~;

    $onlinedata = @onlinedata;
    $output .= qq~
	<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center >
    	<tr>
	   <td>
           <table cellpadding=6 cellspacing=1 border=0 width=100%>
	   <tr>
           <td bgcolor=$miscbacktwo valign=middle colspan=7 align=center><font face="$font" color=$fontcolormisc><b>在线用户列表</b> (共 $onlinedata 人)</font>
	   </td>
	</tr>
        <tr>
        <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc><b>头像</b></font></td>
        <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc><b>用户名</b></font></td>
        <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc><b>当前位置</b></font></td>
        <td bgcolor=$miscbackone align=center ><font face="$font" color=$fontcolormisc><b>最后动作</b></font></td>
        <td bgcolor=$miscbackone align=center ><font face="$font" color=$fontcolormisc><b>登陆时间</b></font></td>
        <td bgcolor=$miscbackone align=center ><font face="$font" color=$fontcolormisc><b>最近活动时间</b></font></td>
        </tr>
    ~;
                   
foreach $line (@onlinedata) {
    chomp $line;
    $line =~ s/＊＃！＆＊//;
    ($savedusername, $savedcometime, $savedtime, $savedwhere, $saveipaddresstemp, $saveosinfo, $savebrowseinfo, $savedwhere2, $fromwhere) = split(/\t/, $line);
    $fromwhere     = "已设置保密" if (($pvtip ne "on")&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes"));
    $savedcometime = &dateformatshort($savedcometime + ($timezone*3600) + ($timedifferencevalue*3600));
    $savedtime     = &dateformatshort($savedtime + ($timezone*3600) + ($timedifferencevalue*3600));
    ($lookfor, $no) = split(/\(/,$savedusername);
    if ($lookfor eq "客人") { $savedusername = "客人"; $useravatar = "没有"; }
    else {
    my $checkhidden=0;
    foreach (@hiddenmember){
    if ($_=~/^$lookfor/) {	   
         $checkhidden=1;       	
    	 $savedusername = "隐身会员"; $useravatar = "没有"; 
    	}
    }
     if ($checkhidden==0) {
        &getmember("$savedusername");
        if ($avatars eq "on") {
	    if (($personalavatar)&&($personalwidth)&&($personalheight)) { #自定义头像存在
	        if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	            $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
	        }
	        else {
	            $useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>);
	        }
	    }
            elsif (($useravatar ne "noavatar") && ($useravatar)) {
                $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$useravatar.gif" border=0 $defaultwidth $defaultheight>);
            }
            else {$useravatar="没有"; }
        }
    }
    }

  ($saveipaddress, $none) = split(/=/,$saveipaddresstemp);
  ($ip1,$ip2,$ip3,$ip4) = split(/\./,$saveipaddress);
   if (($membercodetemp eq "ad")||($membercodetemp eq "smo")) {
       $saveipaddress="$ip1.$ip2.$ip3.$ip4";
   }
   elsif ($membercodetemp eq "mo") {
       $saveipaddress="$ip1.$ip2.$ip3.*";
   }
   else {
       if (($pvtip eq "on")&&($inmembername ne "客人")) {
           $saveipaddress="$ip1.$ip2.*.*";
       }
       else { $saveipaddress="已设置保密"; }
   }
   if ($savedusername eq "客人") {
       $savedtime = "";
   }
   else {
       $savedtime = "\n$savedtime";
   }
   $output .=qq~
    <tr>
    <td bgcolor=$miscbackone nowrap align=center>$useravatar</td>
    <td bgcolor=$miscbackone nowrap align=center><a href="$profileprog?action=show&member=$savedusername" target=_blank><font face="$font" color=$fontcolormisc><b>$savedusername</b></font></a></td>
    <td bgcolor=$miscbackone nowrap><font face="$font" color=$fontcolormisc>$savedwhere</font></td>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc>$savedwhere2</font></td>
    <td bgcolor=$miscbackone nowrap align=center><font face="$font" color=$fontcolormisc>$savedcometime</font></td>
    <td bgcolor=$miscbackone nowrap align=center><font face="$font" color=$fontcolormisc>$savedtime</font></td>
    </tr>
   ~;
}
    
$output .= qq~</table></td></tr></table>~;

print header(-charset=>gb2312);
&output(
       -Title   => "$boardname - 当前在线用户", 
       -ToPrint => $output, 
       -Version => $versionnumber 
);
