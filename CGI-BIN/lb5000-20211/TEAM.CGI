#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ����������)
#
#  ������  : ɽӥ�� (Shining Hu)
#            ����ȱ (Ifairy Han)
#           
#  ��ҳ��ַ: http://www.CGIer.com/      CGI �����֮��
#	     http://www.LeoBoard.com/   �װ���̳֧����ҳ
#	     http://www.leoBBS.com/     ����ֱ̳ͨ��
#            http://mail@17do.com/      ���һ����
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

# &ipbanned; #��ɱһЩ ip

$query = new LBCGI;
$inpage = $query -> param ("page");
if ($inpage eq "") { $inpage = 1; }
$inmembername = cookie ("amembernamecookie");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
   $inmembername = "����";
}
if ($infosopen == 2) {
    &getmember("$inmembername");
    print header(-charset=>gb2312);
    &error("�鿴�����Ŷ�&������Ȩ�鿴�����Ŷӣ�") if ($inmembername eq "����");
    if ($userregistered eq "no") { &error("�鿴�����Ŷ�&�㻹ûע���أ�"); }
    &error("�鿴�����Ŷ�&��̳�����Ŷ�ֻ��̳���Ͱ������Բ鿴��") if (($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne "mo"));
}
elsif ($infosopen == 1) {
    print header(-charset=>gb2312);
    &getmember("$inmembername");
    &error("�鿴�����Ŷ�&������Ȩ�鿴�����Ŷӣ�") if ($inmembername eq "����");
    if ($userregistered eq "no") { &error("�鿴�����Ŷ�&�㻹ûע���أ�"); }
}

$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\t�����Ŷ�\tnone\t�鿴������Ա����\t");
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
    $pagelinks = qq~���б�ֻ��һҳ~; }

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
         ## Definiere die Hintergrund- und Textfarbe f�r die Zeilen
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
        else { $mtitle = $mtitle0; $membergraphic = ""; }  #��ʾĬ�ϵȼ�
         if ($membergraphic) {
             $membergraphic = qq~<img src="$imagesurl/images/$membergraphic" border="0" width=100 height=16>~; }
        if ($avatars eq "on") {
	    if (($userdetail[22])&&($userdetail[23])&&($userdetail[24])) { #�Զ���ͷ�����
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
            $membername = qq~$userdetail[0] <img src="$imagesurl/images/teamad.gif" border=0 alt=����Ϊ̳�� width=16 height=16>~;
            $membergraphic = "<img src=\"$imagesurl/images/$admingraphic\" border=\"0\" width=100 height=16>" if ($admingraphic ne "");
            $mtitle = $adtitle if ($adtitle ne "");
            if (($userdetail[2] eq "member")||($userdetail[2] eq "Member")||($userdetail[2] eq "")) {
                $membertitle = qq~<font face="$font" color=$fontcolor>��̳̳��</font>~; }
            else {
                $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~; } }
        elsif ($userdetail[3] eq "mo") {
            $posterfontcolor = "$teamnamecolor";
            $membername = qq~$userdetail[0] <img src="$imagesurl/images/teammo.gif" border=0 alt=����Ϊ���� width=16 height=16>~;
            $membergraphic = "<img src=\"$imagesurl/images/$modgraphic\" border=\"0\" width=100 height=16>" if ($modgraphic ne "");
            $mtitle = $motitle if ($motitle ne "");
            if (($userdetail[2] eq "")||($userdetail[2] eq "Member")||($userdetail[2] eq "member")) {
                $membertitle = qq~<font face="$font" color=$fontcolor>��̳����</font>~; }
            else {
                $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~; } }
	elsif ($userdetail[3] eq "smo") {
		$posterfontcolor = "$smonamecolor";
            $membername = qq~$userdetail[0] <img src="$imagesurl/images/teamsmo.gif" border=0 alt=����Ϊ�ܰ��� width=16 height=16>~;
            $membergraphic = "<img src=\"$imagesurl/images/$smodgraphic\" border=\"0\" width=100 height=16>" if ($smodgraphic ne "");
            $mtitle = $smotitle if ($smotitle ne "");
            if (($userdetail[2] eq "")||($userdetail[2] eq "Member")||($userdetail[2] eq "member")) {
                $membertitle = qq~<font face="$font" color=$fontcolor>�ܰ���</font>~; }
            else {
                $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~; } }
	## Setze letzte Beitrags-Details
	($postdate, $posturl, $posttopic) = split(/\%%%/, $userdetail[14]);
	if ($postdate ne "û�з�����") {
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
	    $posttopic =~ s/^����������//;

	    $lastpostdetails = qq~<a href="$posturl">$posttopic</a> ($lastpostdate $lastposttime)~; }
	else { $lastpostdetails = qq~��δ���Թ�~; }
	if ($posturl eq "" && $posttopic eq "" && $postdate ne "û�з�����") {$lastpostdetails = qq~�Ƿ��ڱ�����̳��Ӵ��������~; }

        ## Ist das Mitglied ONLINE oder OFFLINE?
        foreach $onlineuser (@onlinedata) {
            @onlineuserdetail = split (/\t/, $onlineuser);
            chomp @onlineuserdetail;
            if ($onlineuserdetail[0] eq $userdetail[0]) {
                $online = qq~<IMG SRC="$imagesurl/images/online1.gif" width=15 height=15 border=0 alt="���û�Ŀǰ����">~; last; }
            else {
                $online = qq~<IMG SRC="$imagesurl/images/offline1.gif" width=15 height=15 alt="���û�Ŀǰ������">~; } }

        ## Mehr Details
	if ($userdetail[6] eq "no") {$email = "����"; }
	if ($userdetail[6] eq "msn") {$email = qq~<img src=$imagesurl/images/msn.gif border=0 width=16 height=16 align=absmiddle> <a href="mailto:$userdetail[5]">$userdetail[5]</a>~; }
        else {$email = qq~<a href="mailto:$userdetail[5]">$userdetail[5]</a>~; }

        if ($userdetail[8] eq "" || $userdetail[8] eq "http://") {
            $homepage = "û��"; }
        else {
            $homepage = qq~<a href="$userdetail[8]" target="_blank">$userdetail[8]</a>~; }
        if ($userdetail[9] eq "") {
            $aolname = "û��"; }
        else {
            $aolname = $userdetail[9]; }
        if ($userdetail[10] eq "") {
            $icqnumber = "û��"; }
        else {
            $icqnumber = $userdetail[10]; }
        if ($userdetail[39] eq "") {
            $jhmp = "��������"; }
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
           @moderatedforums = "$userdetail[0] û�������κΰ��"; }
        @moderatedforums = sort alphabetically (@moderatedforums);

        ## Schreibe HTML in eine Variable
        $teamguts .= qq~
        <!--Begin Profile for $userdetail[0]-->
        <tr bgcolor=$color>
        <td valign=top>
	<table style="filter:glow(color=$titlecolor,strength=2)">$online��<font face="$posternamefont" color="$posterfontcolor"><b>$membername</b></font>
	</table>
        ͷ�Σ�$membertitle
        <br>$useravatar
        <br>$membergraphic
        <br>����<a href="lookinfo.cgi?action=style" target="_blank">$mtitle</a><br>����: $jhmp</td>
        <td valign=top><table cellspacing=0 cellpadding=0 border=0 width=100%>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>ע�����ڣ�</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$userdetail[13]</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>����ԣ�</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$lastpostdetails</font></td>
        </tr>
        <tr><td colspan=2><font face="$font">&nbsp;</font></td></tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>�����ʼ���</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$email</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>��ҳ��</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$homepage</font></td>
        </tr>
        <tr><td colspan=2><font face="$font">&nbsp;</font></td></tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>OICQ ���룺</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$aolname</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>ICQ ���룺</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$icqnumber</font></td>
        </tr>
        <tr><td colspan=2><font face="$font">&nbsp;</font></td></tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>���ְ�飺</font></td>
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
&nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;�����Ŷ�
</td>
</tr>
</table>
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$titlecolor>
<td width=25% align=center><font face="$font" color=$titlefontcolor><b>�� �� �� Ա</b></td>
<td width=75% align=center><font face="$font" color=$titlefontcolor><b>�� ϸ �� Ϣ</b></td>
</tr>

$teamguts

</table></td></tr></table>
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr>
<td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$menubackground>
<td align=center><font face=���� color=$fontcolormisc>$pagelinks</font></td>
</tr>
</table></td>
</tr>
</table>
~;


print header(-charset=>gb2312);    
&output( -Title   => "$boardname - �����Ŷ�", 
         -ToPrint => $output, 
         -Version => $versionnumber );