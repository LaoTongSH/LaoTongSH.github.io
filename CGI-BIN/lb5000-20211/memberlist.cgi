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
use Benchmark;
$TT0  = new Benchmark;
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
require "data/boardstats.cgi";
require "data/progs.cgi";
require "data/styles.cgi";
require "data/membertitles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$backgroundcolor = "005984";
$topanzahl       = $hottopicmark;       #��ʾ����ǰ����������ʾ���¶��ٸ�������û���
$startseite      = "1";         	#Ĭ������:  1->������, 2->ǰN��, 3->�û���, 4->ע������
$memberproseite  = $maxthreads; 	#ÿҳ��ʾ�û���
if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie");   }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
   $inmembername = "����";
}

if ($infosopen == 2) {
    &getmember("$inmembername");
    &error("�鿴��Ա�б�&������Ȩ�鿴��Ա�б�") if ($inmembername eq "����");
    if ($userregistered eq "no") { &error("�鿴��Ա�б�&�㻹ûע���أ�"); }
    elsif ($inpassword ne $password) { &error("�鿴��Ա�б�&������������⣡"); }
    &error("�鿴��Ա�б�&��̳��Ա�б�ֻ��̳���Ͱ������Բ鿴��") if (($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne "mo"));
}
elsif ($infosopen == 1) {
    &getmember("$inmembername");
    &error("�鿴��Ա�б�&������Ȩ�鿴��Ա�б�") if ($inmembername eq "����");
    if ($userregistered eq "no") { &error("�鿴��Ա�б�&�㻹ûע���أ�"); }
    elsif ($inpassword ne $password) { &error("�鿴��Ա�б�&������������⣡"); }
}
else {
    &getmember("$inmembername");
}
$cpudisp = 1 if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"));
&badwordfile;
&title;
my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\t�û��б�\tnone\t�鿴�û��б�\t");
}
open (FILE, "$lbdir/data/lbmember.cgi");
@file = <FILE>;
close (FILE);
$totlemembertemp=@file;
foreach $line (@file) {
@tmpuserdetail = split (/\t/, $line);
chomp @tmpuserdetail;
if ($tmpuserdetail[1] eq banned) {push (@banned, "$tmpuserdetail[0]"); }
push (@cgi, "$tmpuserdetail[0]");
$postundmember {"$tmpuserdetail[0]"} = $tmpuserdetail[2];
$datumundmember {"$tmpuserdetail[0]"} = $tmpuserdetail[3];
}
@cgi=sort(@cgi);
@sortiert = reverse sort { $postundmember{$a} <=> $postundmember{$b} } keys(%postundmember);
@sortiert1 = sort { $datumundmember{$a} <=> $datumundmember{$b} } keys(%datumundmember);
@sortiert2 = reverse(@sortiert1);
$output .= qq~
           <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
           <tr>
           <td width=30% rowspan=2 valign=top><img src=$imagesurl/images/$boardlogo border=0></td>
           <td valign=middle align=left><font color=$fontcolormisc>
           ��<img src=$imagesurl/images/closedfold.gif border=0>��<a href=$forumsummaryprog>$boardname</a><br>
           ��<img src=$imagesurl/images/bar.gif border=0 width=15 height=15><img src=$imagesurl/images/openfold.gif border=0>���û��б�
           </td>
           <tr>
           <td valign=bottom align=right>&nbsp; $helpurl</td>
           </tr>
           </table><br>~;
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
$query = new LBCGI;
$a = $query -> param ("a");
if ($a eq '' && $buffer eq '')
{$buffer = "a=$startseite";}
else
{($buffer = "$buffer") || ($buffer = "a=$a");}
if ($buffer eq 'a=1') {&Postsortiert}
elsif ($buffer eq 'a=2') {&Topten}
elsif ($buffer eq 'a=3') {&Namensortiert}
elsif ($buffer eq 'a=4') {&datum}
elsif ($buffer eq 'a=5') {&redatum}
elsif ($buffer eq 'a=6') {&banned}

sub Namensortiert {
    $query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") { $inpage = 1; }
	$a = 3;
	@memberarray = @cgi;
	&splitting;
	$Listenname = "���û�������";
	&Tabellenanfang;
	foreach $member (@cgi[$startmember ... $endmember]) {
	    $member =~s/ /_/g;
            $member =~ tr/A-Z/a-z/;
            $member =~s/_/\_/g;
	    if (-e "${lbdir}$memdir/$member.cgi") {
		$filetoopen = ("$lbdir" . "$memdir/$member.cgi");
		open(FILE, "$filetoopen" );
		$memberdaten = <FILE>;
		close(FILE);
		&Listing;
	    }
	}
	$output .= qq~</table>~;
}
sub banned {
    $query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") { $inpage = 1; }
	$a = 6;
	@memberarray = @banned;
	&splitting;
	$Listenname = "�����еķ���";
	&Tabellenanfang;
	foreach $member (@banned[$startmember ... $endmember]) {
	    $member =~s/ /_/g;
	    $member =~s/_/\_/g;
            $member =~ tr/A-Z/a-z/;
	    if (-e "${lbdir}$memdir/$member.cgi") {
		$filetoopen = ("$lbdir" . "$memdir/$member.cgi");
		open(FILE, "$filetoopen" );
		$memberdaten = <FILE>;
		close(FILE);
		&Listing;
	    }
	}
	$output .= qq~</table>~;
}
sub Postsortiert {
	$query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") { $inpage = 1; }
	$a = 1;
	@memberarray = @sortiert;
	&splitting;
	$Listenname = "�Է�����������";
	&Tabellenanfang;
	foreach $member (@sortiert[$startmember ... $endmember]) {
	    $member =~s/ /_/g;
	    $member =~s/_/\_/g;
            $member =~ tr/A-Z/a-z/;
	    if (-e "${lbdir}$memdir/$member.cgi") {
		$filetoopen = ("$lbdir" . "$memdir/$member.cgi");
		open(FILE, "$filetoopen" );
		$memberdaten = <FILE>;
		close(FILE);
		&Listing;
	    }
	}
	$output .= qq~</table>~;

}
sub Topten {
    $Listenname = "��������ǰ $topanzahl ��";
    &Tabellenanfang;
    @sortiert = splice(@sortiert,0,$topanzahl);
    foreach $member (@sortiert) {
        $member =~s/ /_/g;
        $member =~s/_/\_/g;
        $member =~ tr/A-Z/a-z/;
	if (-e "${lbdir}$memdir/$member.cgi") {
	$filetoopen = ("$lbdir" . "$memdir/$member.cgi");
        open(FILE, "$filetoopen" );
        $memberdaten = <FILE>;
        close(FILE);
        &Listing;
    }
    }
    $output .= qq~</table>~;
}
sub datum {
    $query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") {$inpage = 1;}
    $a = 4;
    $Listenname = "��ע��ʱ������";
    &Tabellenanfang;
    @memberarray = @sortiert1;
    &splitting;
    foreach $member (@sortiert1[$startmember ... $endmember]) {
        $member =~s/ /_/g;
        $member =~s/_/\_/g;
        $member =~ tr/A-Z/a-z/;
	if (-e "${lbdir}$memdir/$member.cgi") {
	$filetoopen = ("$lbdir" . "$memdir/$member.cgi");
            open(FILE, "$filetoopen" );
            $memberdaten = <FILE>;
            close(FILE);
            &Listing;
	}
    }
    $output .= qq~</table>~;
}
sub redatum {
    $Listenname = "���� $topanzahl ��ע���û�";
    &Tabellenanfang;
    @memberarray = @sortiert2;
    @sortiert2 = splice(@sortiert2,0,$topanzahl);
    foreach $member (@sortiert2) {
            $member =~s/ /_/g;
            $member =~s/_/\_/g;
            $member =~ tr/A-Z/a-z/;
	    if (-e "${lbdir}$memdir/$member.cgi") {
	    $filetoopen = ("$lbdir" . "$memdir/$member.cgi");
   	    open(FILE, "$filetoopen" );
            $memberdaten = <FILE>;
            close(FILE);
            &Listing;
	}
    }
    $output .= qq~</table>~;
}
sub Tabellenanfang {
    $totalpostandthreads = $totalposts + $totalthreads;
    $output .= qq~<center>
      <table width=$tablewidth bgcolor=$backgroundcolor cellspacing=0 border=0 bordercolor=$tablebordercolor>
    	<tr><td>
      	<table cellpadding=6 cellspacing=1 border=0 width=100%>
    	<tr bgcolor=$forumcolorone><td colspan=5 valign=top>&nbsp;>> <B>$Listenname</B> <<<BR><BR>
	&nbsp;��ע���û����� $totlemembertemp �� ������������ $totalpostandthreads ƪ</font></td>
	<td colspan=5 align=right><form method=get action=memberlist.cgi>
        <select name=a>
            <option value=2>��������ǰ $topanzahl ��</option>
            <option value=5>���� $topanzahl ��ע���û�</option>
            <option value=3>���û�������</option>
            <option value=1>�Է�����������</option>
            <option value=4>��ע��ʱ������</option>
            <option value=6>�����еķ���</option>
        </select>
	<input type=submit value="�� ��"><br>
	</td></form></tr>
	<tr bgcolor=$titlecolor><td align=center><b>�û���</b></td><td align=center><b>Email</b></td><td align=center><b>ICQ</b></td><td align=center><b>OICQ</b></td><td align=center><b>��ҳ</b></td><td align=center><b>����Ϣ</td><td align=center><b>�����</td><td align=center><b>ע��ʱ��</b></td><td align=center><b>�ȼ�״̬</b></td><td align=center><b>��������</b></td></font></tr>
    ~;
}

sub Listing {
    @memberdaten = split(/\t/,$memberdaten);
    $name        = $memberdaten[0];
    $status      = $memberdaten[2];
    $anzahl      = $memberdaten[4];
    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
    $anzahl = $anzahl1 + $anzahl2;
    $email       = $memberdaten[5];
    $home        = $memberdaten[8];
    $aolname     = $memberdaten[9];
    $icq         = $memberdaten[10];
    $date        = $memberdaten[13] + ($memberdaten[16] * 3600) + ($timezone * 3600);
    $rang        = $memberdaten[3];
    $emailstatus = $memberdaten[6];
    next if ($name eq "");
    ($postdate, $posturl, $posttopic) = split(/\%%%/, $memberdaten[14]);
    if (($postdate ne "û�з����")&&($postdate ne "")) {
        $postdate = $postdate + ($userdetail[16] * 3600) + ($timezone * 3600);
        $lastpostdate = &longdate ("$postdate");
        $lastposttime = &longdate ("$postdate");
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $posttopic=~ s/$bad/$good/isg;
            }
	}
        $posttopic =~ s/^����������//;
	$lastpostdetails = qq~<a href=$posturl><img border=0 src=$imagesurl/images/openfold.gif alt=$posttopic></a>~;
    }
    else{$lastpostdetails = "û��";}
    $date = &longdate($date + ($memberdaten[16]*3600) + ($timezone*3600));
    $postundmember {"$name"} = $anzahl;
    if (($icq) && ($icq =~ /[0-9]/)){
	$icqgraphic = qq~<a href="javascript:openScript('$miscprog?action=icq&UIN=$icq',450,300)"><img src=http://wwp.icq.com/scripts/online.dll?icq=$icq&img=5 border=0 width=16 height=16></a>~;
    }
    else{$icqgraphic = "û��";}

    if (($home eq "http://") || ($home eq "")) { $home = "û��"; }
    else{
	$home = "<a href=$home target=_blank><img border=0 src=$imagesurl/images/homepage.gif></a>"
    }

    if ($aolname) {my $oicqimg=&getoicq($aolname); $aolgraphic = qq~<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$aolname target=_blank><img src=$oicqimg alt="�鿴 OICQ:$aolname ������" border=0 width=16 height=16></a>~; }
    else{$aolgraphic = "û��";}
    if ($email eq "" || $emailstatus eq "no" || $emailstatus eq "msn"){
	$email = "û��" if ($email eq "");
	$email = "����" if ($emailstatus eq "no");
	$email = "<a href=mailto:$email><img border=0 src=$imagesurl/images/msn.gif></a>" if ($emailstatus eq "msn");
    }
    else {$email = "<a href=mailto:$email><img border=0 src=$imagesurl/images/email.gif></a>" }
        if ($anzahl >= $mpostmarkmax)   { $mtitle = $mtitlemax; $membergraphic = $mgraphicmax; }
        elsif ($anzahl >= $mpostmark19) { $mtitle = $mtitle19;  $membergraphic = $mgraphic19; }
        elsif ($anzahl >= $mpostmark18) { $mtitle = $mtitle18;  $membergraphic = $mgraphic18; }
        elsif ($anzahl >= $mpostmark17) { $mtitle = $mtitle17;  $membergraphic = $mgraphic17; }
        elsif ($anzahl >= $mpostmark16) { $mtitle = $mtitle16;  $membergraphic = $mgraphic16; }
        elsif ($anzahl >= $mpostmark15) { $mtitle = $mtitle15;  $membergraphic = $mgraphic15; }
        elsif ($anzahl >= $mpostmark14) { $mtitle = $mtitle14;  $membergraphic = $mgraphic14; }
        elsif ($anzahl >= $mpostmark13) { $mtitle = $mtitle13;  $membergraphic = $mgraphic13; }
        elsif ($anzahl >= $mpostmark12) { $mtitle = $mtitle12;  $membergraphic = $mgraphic12; }
        elsif ($anzahl >= $mpostmark11) { $mtitle = $mtitle11;  $membergraphic = $mgraphic11; }
        elsif ($anzahl >= $mpostmark10) { $mtitle = $mtitle10;  $membergraphic = $mgraphic10; }
        elsif ($anzahl >= $mpostmark9)  { $mtitle = $mtitle9;   $membergraphic = $mgraphic9; }
        elsif ($anzahl >= $mpostmark8)  { $mtitle = $mtitle8;   $membergraphic = $mgraphic8; }
        elsif ($anzahl >= $mpostmark7)  { $mtitle = $mtitle7;   $membergraphic = $mgraphic7; }
        elsif ($anzahl >= $mpostmark6)  { $mtitle = $mtitle6;   $membergraphic = $mgraphic6; }
        elsif ($anzahl >= $mpostmark5)  { $mtitle = $mtitle5;   $membergraphic = $mgraphic5; }
        elsif ($anzahl >= $mpostmark4)  { $mtitle = $mtitle4;   $membergraphic = $mgraphic4; }
        elsif ($anzahl >= $mpostmark3)  { $mtitle = $mtitle3;   $membergraphic = $mgraphic3; }
        elsif ($anzahl >= $mpostmark2)  { $mtitle = $mtitle2;   $membergraphic = $mgraphic2; }
        elsif ($anzahl >= $mpostmark1)  { $mtitle = $mtitle1;   $membergraphic = $mgraphic1; }
        else { $mtitle = $mtitle0; $membergraphic = ""; }
        if($rang eq "ad") {
        	$mtitle = $adtitle if ($adtitle ne "");
        	$membergraphic = "$admingraphic" if ($admingraphic ne "");
        }
        elsif ($rang eq "mo") {
        	$mtitle = $motitle if ($motitle ne "");
        	$membergraphic = "$modgraphic" if ($modgraphic ne "");
        }
        elsif ($rang eq "smo") {
        	$mtitle = $smotitle if ($smotitle ne "");
        	$membergraphic = "$smodgraphic" if ($smodgraphic ne "");
        }
        elsif ($rang eq "banned") {
        	$mtitle = "�ѱ���ֹ����";
        	$membergraphic = "";
        }
        elsif ($rang eq "masked") {
        	$mtitle = "�����ѱ�����";
        	$membergraphic = "";
        }

        if ($membergraphic) { $membergraphic = "<img src=$imagesurl/images/$membergraphic border=0>"; }
	$memberfilename = $name;
	$memberfilename =~ y/ /_/;
	$memberfilename =~ tr/A-Z/a-z/;
	$message = "<a href=javascript:openScript('messanger.cgi?action=new&touser=$memberfilename',600,400)><img src=$imagesurl/images/message.gif border=0></a>";
	$output .= qq~<tr bgcolor=$forumcolortwo><td>&nbsp;<a href=$profileprog?action=show&member=$memberfilename>$name</a></td><td align=center>$email</td><td align=center>$icqgraphic</td><td align=center>$aolgraphic</td><td align=center>$home</td><td align=center>$message</td><td align=center>$lastpostdetails</td><td align=center>$date</td><td align=center>$mtitle<br>$membergraphic</td><td align=center>$anzahl</td></tr>~;

}
sub splitting {
    $totalpages = @memberarray / $memberproseite;
    ($pagenumbers, $decimal) = split (/\./, $totalpages);
    if ($decimal > 0) {$pagenumbers++;}

    $pagedigit = 0;
    $mypage=$inpage-1;
    $pagelinks =qq~���������� $pagenumbers ҳ ~;
    if ($inpage>1){$pagelinks .= qq~[<a href=$boardurl/memberlist.cgi?a=$a&page=$mypage>��һҳ</a>] ~;}
    for ($page=$inpage;$page<$inpage+12;$page++){
    if ($page<=$pagenumbers){
    if ($inpage ne $page) {$pagelinks .= qq~[<a href=$boardurl/memberlist.cgi?a=$a&page=$page>��$pageҳ</a>] ~; }
	else{$pagelinks .= qq~[<B>��$pageҳ</B>] ~;}
    }
    }
    $nextpage=$inpage+12;
    if ($pagenumbers>$inpage+12){$pagelinks .= qq~[<a href=$boardurl/memberlist.cgi?a=$a&page=$nextpage>��һҳ</a>] ~;}
    if ($totalpages <= 1) {$pagelinks = qq~~;}

    $startmember = ($inpage - 1) * $memberproseite;
    $endmember = $startmember + $memberproseite - 1;
    if ($endmember > (@memberarray-1)) {$endtopic = @memberarray - 1;}

}
$output .= qq~</td></tr></table><p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr>
<td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$menubackground>
<td align=center><font face=���� color=$fontcolormisc>$pagelinks</font></td>
</tr>
</table></td>
</tr>
</table></center>~;
print header(-charset=>gb2312);
&output(
  -Title   => "$boardname - �û��б�",
  -ToPrint => $output,
  -Version => $versionnumber
);

END {
  if ($cpudisp eq "1") {
    $TT1 = new Benchmark;
    $td  = Benchmark::timediff($TT1,  $TT0);
    $td  = Benchmark::timestr($td);
    $td  =~ /(\d+)\s*wallclock secs \(\s*?(\d*?\.\d*?)\s*usr\s*\+\s*(\d*?\.\d*?)\s*sys/i;
    print "<center><font color=$cpudispcolor>����ռ�� CPU ʱ�䣺$2 usr + $3 sys";
  }
}
