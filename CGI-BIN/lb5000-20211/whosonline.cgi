#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ���������)
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
require "data/boardinfo.cgi";
require "data/progs.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "whosonline.cgi";

$query = new LBCGI;

&ipbanned; #��ɱһЩ ip

$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/\/$//;

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
    $inmembername = "����";
}
else {
    &getmember("$inmembername");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
}
$membercodetemp = $membercode;

$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");
$current_time = time;
$current_time = &dateformatshort($current_time + ($timezone*3600) + ($timedifferencevalue*3600));

$helpurl = &helpfiles("�����û�");
$helpurl = qq~$helpurl<img src="$imagesurl/images/help_b.gif" border=0></a>~;

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\t�����û�\tnone\t�鿴�����û�״̬\t");
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
            &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0 width=15 height=15><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;��ǰ�����û� (������ʱ�䣺$current_time)
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
           <td bgcolor=$miscbacktwo valign=middle colspan=7 align=center><font face="$font" color=$fontcolormisc><b>�����û��б�</b> (�� $onlinedata ��)</font>
	   </td>
	</tr>
        <tr>
        <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc><b>ͷ��</b></font></td>
        <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc><b>�û���</b></font></td>
        <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc><b>��ǰλ��</b></font></td>
        <td bgcolor=$miscbackone align=center ><font face="$font" color=$fontcolormisc><b>�����</b></font></td>
        <td bgcolor=$miscbackone align=center ><font face="$font" color=$fontcolormisc><b>��½ʱ��</b></font></td>
        <td bgcolor=$miscbackone align=center ><font face="$font" color=$fontcolormisc><b>����ʱ��</b></font></td>
        </tr>
    ~;
                   
foreach $line (@onlinedata) {
    chomp $line;
    $line =~ s/����������//;
    ($savedusername, $savedcometime, $savedtime, $savedwhere, $saveipaddresstemp, $saveosinfo, $savebrowseinfo, $savedwhere2, $fromwhere) = split(/\t/, $line);
    $fromwhere     = "�����ñ���" if (($pvtip ne "on")&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes"));
    $savedcometime = &dateformatshort($savedcometime + ($timezone*3600) + ($timedifferencevalue*3600));
    $savedtime     = &dateformatshort($savedtime + ($timezone*3600) + ($timedifferencevalue*3600));
    ($lookfor, $no) = split(/\(/,$savedusername);
    if ($lookfor eq "����") { $savedusername = "����"; $useravatar = "û��"; }
    else {
    my $checkhidden=0;
    foreach (@hiddenmember){
    if ($_=~/^$lookfor/) {	   
         $checkhidden=1;       	
    	 $savedusername = "�����Ա"; $useravatar = "û��"; 
    	}
    }
     if ($checkhidden==0) {
        &getmember("$savedusername");
        if ($avatars eq "on") {
	    if (($personalavatar)&&($personalwidth)&&($personalheight)) { #�Զ���ͷ�����
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
            else {$useravatar="û��"; }
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
       if (($pvtip eq "on")&&($inmembername ne "����")) {
           $saveipaddress="$ip1.$ip2.*.*";
       }
       else { $saveipaddress="�����ñ���"; }
   }
   if ($savedusername eq "����") {
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
       -Title   => "$boardname - ��ǰ�����û�", 
       -ToPrint => $output, 
       -Version => $versionnumber 
);
