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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/membertitles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                    # Unbuffer the output

#################--- Begin the program ---###################
$maxshowmembers = $maxtopics; ## Change how many team members per page are displayed

$teamscript = "team.cgi";

# &ipbanned; #封杀一些 ip

$query = new LBCGI;
$inpage = $query -> param ("page");
if ($inpage eq "") { $inpage = 1; }
$inmembername = cookie ("amembernamecookie");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
   $inmembername = "客人";
}
if ($infosopen == 2) {
    &getmember("$inmembername");
    print header(-charset=>gb2312);
    &error("查看管理团队&客人无权查看管理团队！") if ($inmembername eq "客人");
    if ($userregistered eq "no") { &error("查看管理团队&你还没注册呢！"); }
    &error("查看管理团队&论坛管理团队只有坛主和版主可以查看！") if (($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne "mo"));
}
elsif ($infosopen == 1) {
    print header(-charset=>gb2312);
    &getmember("$inmembername");
    &error("查看管理团队&客人无权查看管理团队！") if ($inmembername eq "客人");
    if ($userregistered eq "no") { &error("查看管理团队&你还没注册呢！"); }
}

$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\t管理团队\tnone\t查看管理人员名单\t");
}
&badwordfile;

## member files read in, Admins and Mods identify pushed into a list 

open (FILE, "$lbdir/data/lbmember.cgi");
@memberdata = <FILE>;
close (FILE);
foreach $line (@memberdata) {
@tmpuserdetail = split (/\t/, $line);    	
chomp @tmpuserdetail;
        if ($tmpuserdetail[1] eq ad) {
            push (@teamlist, "1\t$tmpuserdetail[0]"); }
        elsif ($tmpuserdetail[1] eq mo) {
            push (@teamlist, "3\t$tmpuserdetail[0]"); }
        elsif ($tmpuserdetail[1] eq "smo") {
            push (@teamlist, "2\t$tmpuserdetail[0]"); }
}            
            
    
## calculate the page's number
$totalpages = @teamlist / $maxshowmembers;
($pagenumbers, $decimal) = split (/\./, $totalpages);
if ($decimal > 0) {
    $pagenumbers++; }
$page = 1;
$pagedigit = 0;
$pagelinks = qq~Page: ~;
while ($pagenumbers > $pagedigit) { # start while
    $pagedigit++;
    if ($inpage ne $page) {
        $pagelinks .= qq~[<a href="$boardurl/$teamscript?page=$page">$pagedigit</a>] ~; }
    else {
        $pagelinks .= qq~[$pagedigit] ~; }
$page++; } # end while
if ($totalpages <= 1) {
    $pagelinks = qq~本列表只有一页~; }

## calculate the number of the start and final member, those to be displayed on this page 
$startmember = ($inpage - 1) * $maxshowmembers;
$endmember = $startmember + $maxshowmembers - 1;
if ($endmember > (@teamlist - 1)) {
    $endtopic = @teamlist - 1; }

## Mitglieder-Details auslesen und die Mitglieder Seitenweise darstellen
@teamlist = sort alphabetically (@teamlist);
@teamlist = sort numerically (@teamlist);
foreach $teammember (@teamlist[$startmember ... $endmember]) {
    ($trash, $teammemberfile) = split (/\t/, $teammember);
    chomp $teammemberfile;
    $teammemberfile =~s/ /_/g;
    $teammemberfile =~ tr/A-Z/a-z/;
    open (FILE, "$lbdir/$memdir/$teammemberfile.cgi");
    $memberline = <FILE>;
    close (FILE);
    chomp $memberline;
         @userdetail = split (/\t/, $memberline);
         chomp @userdetail;
   	 $userdetail[0] =~ tr/A-Z/a-z/;
	next if (($userdetail[3] ne "ad")&&($userdetail[3] ne "smo")&&($userdetail[3] ne "mo"));
         ## Definiere die Hintergrund- und Textfarbe f黵 die Zeilen
         if ($lastcolor eq $postcolortwo) {
             $color = $postcolorone;
             $fontcolor = $postfontcolorone; }
         else {
             $color = $postcolortwo;
             $fontcolor = $postfontcolortwo; }

         ## Registrierdatum
         $userdetail[13] = $userdetail[13] + ($userdetail[16] * 3600) + ($timezone * 3600);
         $userdetail[13] = &longdate ($userdetail[13]);

         ## Setze Avatar-Grafiken
         if (($avatars eq "on") && ($userdetail[18]) && ($userdetail[18] ne "noavatar")) {
             $useravatar = qq~<br><img src="$imagesurl/avatars/$userdetail[18].gif" border=0 $defaultwidth $defaultheight>~; }
         else {
             $useravatar = ""; }
        ($iiii,$jjjj)= split(/\|/,$userdetail[4]);
        $numberofposts = $iiii +$jjjj;
        if ($numberofposts >= $mpostmarkmax)   { $mtitle =  $mtitlemax; $membergraphic = $mgraphicmax; }
        elsif ($numberofposts >= $mpostmark19) { $mtitle =  $mtitle19;  $membergraphic = $mgraphic19; }
        elsif ($numberofposts >= $mpostmark18) { $mtitle =  $mtitle18;  $membergraphic = $mgraphic18; }
        elsif ($numberofposts >= $mpostmark17) { $mtitle =  $mtitle17;  $membergraphic = $mgraphic17; }
        elsif ($numberofposts >= $mpostmark16) { $mtitle =  $mtitle16;  $membergraphic = $mgraphic16; }
        elsif ($numberofposts >= $mpostmark15) { $mtitle =  $mtitle15;  $membergraphic = $mgraphic15; }
        elsif ($numberofposts >= $mpostmark14) { $mtitle =  $mtitle14;  $membergraphic = $mgraphic14; }
        elsif ($numberofposts >= $mpostmark13) { $mtitle =  $mtitle13;  $membergraphic = $mgraphic13; }
        elsif ($numberofposts >= $mpostmark12) { $mtitle =  $mtitle12;  $membergraphic = $mgraphic12; }
        elsif ($numberofposts >= $mpostmark11) { $mtitle =  $mtitle11;  $membergraphic = $mgraphic11; }
        elsif ($numberofposts >= $mpostmark10) { $mtitle =  $mtitle10;  $membergraphic = $mgraphic10; }
        elsif ($numberofposts >= $mpostmark9)  { $mtitle =  $mtitle9;   $membergraphic = $mgraphic9; }
        elsif ($numberofposts >= $mpostmark8)  { $mtitle =  $mtitle8;   $membergraphic = $mgraphic8; }
        elsif ($numberofposts >= $mpostmark7)  { $mtitle =  $mtitle7;   $membergraphic = $mgraphic7; }
        elsif ($numberofposts >= $mpostmark6)  { $mtitle =  $mtitle6;   $membergraphic = $mgraphic6; }
        elsif ($numberofposts >= $mpostmark5)  { $mtitle =  $mtitle5;   $membergraphic = $mgraphic5; }
        elsif ($numberofposts >= $mpostmark4)  { $mtitle =  $mtitle4;   $membergraphic = $mgraphic4; }
        elsif ($numberofposts >= $mpostmark3)  { $mtitle =  $mtitle3;   $membergraphic = $mgraphic3; }
        elsif ($numberofposts >= $mpostmark2)  { $mtitle =  $mtitle2;   $membergraphic = $mgraphic2; }
        elsif ($numberofposts >= $mpostmark1)  { $mtitle =  $mtitle1;   $membergraphic = $mgraphic1; }
        else { $mtitle = $mtitle0; $membergraphic = ""; }  #显示默认等级
         if ($membergraphic) {
             $membergraphic = qq~<img src="$imagesurl/images/$membergraphic" border="0" width=100 height=16>~; }
        if ($avatars eq "on") {
	    if (($userdetail[22])&&($userdetail[23])&&($userdetail[24])) { #自定义头像存在
	        if (($userdetail[22] =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	            $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$userdetail[23] HEIGHT=$userdetail[24]><PARAM NAME=MOVIE VALUE=$userdetail[22]><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$userdetail[22] WIDTH=$userdetail[23] HEIGHT=$userdetail[24] PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
	        }
	        else {
	            $useravatar = qq(<br>&nbsp; <img src=$userdetail[22] border=0 width=$userdetail[23] height=$userdetail[24]>);
	        }
	    }
            elsif (($userdetail[18] ne "noavatar") && ($userdetail[18])) {
                $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$userdetail[18].gif" border=0 $defaultwidth $defaultheight>);
            }
            else { undef $useravatar; }
        }

        ## Setze Mitgliedsstatus 
        if ($userdetail[3] eq "ad") {
            $posterfontcolor = "$adminnamecolor";
            $membername = qq~$userdetail[0] <img src="$imagesurl/images/teamad.gif" border=0 alt=此人为坛主 width=16 height=16>~;
            $membergraphic = "<img src=\"$imagesurl/images/$admingraphic\" border=\"0\" width=100 height=16>" if ($admingraphic ne "");
            $mtitle = $adtitle if ($adtitle ne "");
            if (($userdetail[2] eq "member")||($userdetail[2] eq "Member")||($userdetail[2] eq "")) {
                $membertitle = qq~<font face="$font" color=$fontcolor>论坛坛主</font>~; }
            else {
                $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~; } }
        elsif ($userdetail[3] eq "mo") {
            $posterfontcolor = "$teamnamecolor";
            $membername = qq~$userdetail[0] <img src="$imagesurl/images/teammo.gif" border=0 alt=此人为版主 width=16 height=16>~;
            $membergraphic = "<img src=\"$imagesurl/images/$modgraphic\" border=\"0\" width=100 height=16>" if ($modgraphic ne "");
            $mtitle = $motitle if ($motitle ne "");
            if (($userdetail[2] eq "")||($userdetail[2] eq "Member")||($userdetail[2] eq "member")) {
                $membertitle = qq~<font face="$font" color=$fontcolor>论坛版主</font>~; }
            else {
                $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~; } }
	elsif ($userdetail[3] eq "smo") {
		$posterfontcolor = "$smonamecolor";
            $membername = qq~$userdetail[0] <img src="$imagesurl/images/teamsmo.gif" border=0 alt=此人为总版主 width=16 height=16>~;
            $membergraphic = "<img src=\"$imagesurl/images/$smodgraphic\" border=\"0\" width=100 height=16>" if ($smodgraphic ne "");
            $mtitle = $smotitle if ($smotitle ne "");
            if (($userdetail[2] eq "")||($userdetail[2] eq "Member")||($userdetail[2] eq "member")) {
                $membertitle = qq~<font face="$font" color=$fontcolor>总版主</font>~; }
            else {
                $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~; } }
	## Setze letzte Beitrags-Details
	($postdate, $posturl, $posttopic) = split(/\%%%/, $userdetail[14]);
	if ($postdate ne "没有发表过") {
	    $postdate = $postdate + ($userdetail[16] * 3600) + ($timezone * 3600);
            $lastpostdate = &longdate ("$postdate");
            $lastposttime = &shorttime ("$postdate");

        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chop $good;
                $posttopic=~ s/$bad/$good/isg;
                }
            }
	    $posttopic =~ s/^＊＃！＆＊//;

	    $lastpostdetails = qq~<a href="$posturl">$posttopic</a> ($lastpostdate $lastposttime)~; }
	else { $lastpostdetails = qq~从未发言过~; }
	if ($posturl eq "" && $posttopic eq "" && $postdate ne "没有发表过") {$lastpostdetails = qq~是发在保密论坛的哟，不给看~; }

        ## Ist das Mitglied ONLINE oder OFFLINE?
        foreach $onlineuser (@onlinedata) {
            @onlineuserdetail = split (/\t/, $onlineuser);
            chomp @onlineuserdetail;
            if ($onlineuserdetail[0] eq $userdetail[0]) {
                $online = qq~<IMG SRC="$imagesurl/images/online1.gif" width=15 height=15 border=0 alt="该用户目前在线">~; last; }
            else {
                $online = qq~<IMG SRC="$imagesurl/images/offline1.gif" width=15 height=15 alt="该用户目前不在线">~; } }

        ## Mehr Details
	if ($userdetail[6] eq "no") {$email = "保密"; }
	if ($userdetail[6] eq "msn") {$email = qq~<img src=$imagesurl/images/msn.gif border=0 width=16 height=16 align=absmiddle> <a href="mailto:$userdetail[5]">$userdetail[5]</a>~; }
        else {$email = qq~<a href="mailto:$userdetail[5]">$userdetail[5]</a>~; }

        if ($userdetail[8] eq "" || $userdetail[8] eq "http://") {
            $homepage = "没有"; }
        else {
            $homepage = qq~<a href="$userdetail[8]" target="_blank">$userdetail[8]</a>~; }
        if ($userdetail[9] eq "") {
            $aolname = "没有"; }
        else {
            $aolname = $userdetail[9]; }
        if ($userdetail[10] eq "") {
            $icqnumber = "没有"; }
        else {
            $icqnumber = $userdetail[10]; }
        if ($userdetail[39] eq "") {
            $jhmp = "无门无派"; }
        else {
            $jhmp = $userdetail[39]; }

        ## Erstelle Liste der moderierten Foren des Mitglieds
        $filetoopen = "$lbdir" . "data/allforums.cgi";
	$filetoopen = &stripMETA($filetoopen);
	open(FILE, "$filetoopen");
	@forumsdata = <FILE>;
	close(FILE);
	undef @moderatedforums;
        foreach $forum (@forumsdata) {
            @forumdetail = split (/\t/, $forum);
            chomp @forumdetail;
	    $forumdetail[5] =~ s/\, /\,/gi;
	    $forumdetail[5] =~ s/ \,/\,/gi;
	    $forumdetail[5] =~ tr/A-Z/a-z/;
	    @forummodnames = split(/\,/, $forumdetail[5]);
	    foreach $name (@forummodnames) {
    	        chomp $name;
                if ($name eq $userdetail[0]) {
                    push (@moderatedforums, "<a href=\"$boardurl/$forumsprog?forum=$forumdetail[0]\">$forumdetail[3]</a> ($forumdetail[1])<br>"); 
                }
            }
        }
        if (!@moderatedforums) {
           @moderatedforums = "$userdetail[0] 没有主持任何版块"; }
        @moderatedforums = sort alphabetically (@moderatedforums);

        ## Schreibe HTML in eine Variable
        $teamguts .= qq~
        <!--Begin Profile for $userdetail[0]-->
        <tr bgcolor=$color>
        <td valign=top>
	<table style="filter:glow(color=$titlecolor,strength=2)">$online　<font face="$posternamefont" color="$posterfontcolor"><b>$membername</b></font>
	</table>
        头衔：$membertitle
        <br>$useravatar
        <br>$membergraphic
        <br>级别：<a href="lookinfo.cgi?action=style" target="_blank">$mtitle</a><br>门派: $jhmp</td>
        <td valign=top><table cellspacing=0 cellpadding=0 border=0 width=100%>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>注册日期：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$userdetail[13]</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>最后发言：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$lastpostdetails</font></td>
        </tr>
        <tr><td colspan=2><font face="$font">&nbsp;</font></td></tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>电子邮件：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$email</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>主页：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$homepage</font></td>
        </tr>
        <tr><td colspan=2><font face="$font">&nbsp;</font></td></tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>OICQ 号码：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$aolname</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>ICQ 号码：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$icqnumber</font></td>
        </tr>
        <tr><td colspan=2><font face="$font">&nbsp;</font></td></tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>主持板块：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>@moderatedforums</font></td>
        </tr>
        </table></td>
        </tr>~;

        @moderatedforums = "";
        $lastcolor = $color;
        undef $membertitle;
        undef $icqnumber;
        undef $aolname;
        undef $homepage;
        undef $email;
        undef $lastpostdetails;
        undef $membername;
        undef $jhmp;
        undef $useravatar;
        undef $membergraphic;
        }


&title;

$output .= qq~
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
<tr>
<td width=30% rowspan=2>
<img src="$imagesurl/images/$boardlogo" border=0>
</td>
<td valign=top align=left>
<font face="$font" color=$fontcolormisc>
&nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0>&nbsp;&nbsp;<a href="$forumsummaryprog">$boardname</a>
<br>
&nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;管理团队
</td>
</tr>
</table>
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$titlecolor>
<td width=25% align=center><font face="$font" color=$titlefontcolor><b>管 理 人 员</b></td>
<td width=75% align=center><font face="$font" color=$titlefontcolor><b>详 细 信 息</b></td>
</tr>

$teamguts

</table></td></tr></table>
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr>
<td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$menubackground>
<td align=center><font face=宋体 color=$fontcolormisc>$pagelinks</font></td>
</tr>
</table></td>
</tr>
</table>
~;


print header(-charset=>gb2312);    
&output( -Title   => "$boardname - 管理团队", 
         -ToPrint => $output, 
         -Version => $versionnumber );
