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
require "data/cityinfo.cgi";
require "lb.lib.pl";

$thisprog = "rateit.cgi";

$query = new LBCGI;

&ipbanned; #��ɱһЩ ip

print $query->header(-charset=>gb2312);

$access = qq(�Ƿ���������������);

$rate=$query->param("rateselect");
$inforum=$query->param("id");
$intopic=$query->param("forumname");
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$filerequire = "$lbdir" . "data/style${inforum}.cgi";
if (-e $filerequire) { require $filerequire; }

$inselectstyle   = $query->cookie("selectstyle");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
$stylequire = "$lbdir" . "data/skin/${inselectstyle}.cgi";
if ($inselectstyle ne ""){
    if (-e $stylequire){require $stylequire;}
}

$myip=$ENV{'REMOTE_HOST'};
$myip=$ENV{'REMOTE_ADDR'} if ($myip eq "");
if ($id =~ /[a-zA-Z\.]/) {print $access; exit;}
if ($threadname =~ /[a-zA-Z\.]/) {print $access; exit;}

if ($rate == 0 or $rate >= 6) { &error("ͶƱ����&��Ͷ����ʲôƱѽ������ô�����ģ�"); }

if (-e "$lbdir/forum$inforum/rateip$intopic.file.pl") {
	open(IP, "$lbdir/forum$inforum/rateip$intopic.file.pl");
	while(<IP>) {
	    $thisip=$_;
	    chomp($thisip);
	    if ($thisip eq $myip) { &error("ͶƱ����&�Բ���������Ѿ����������Ͷ��Ʊ�ˡ�"); }
	}
	close(IP);

	$filetomake = "$lbdir/forum$inforum/rateip$intopic.file.pl";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(IP, ">>$filetomake");
	flock(IP,2) if ($OS_USED eq "Unix");
	print IP "$myip\n";
	close(IP);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
}
else {
	$filetomake = "$lbdir/forum$inforum/rateip$intopic.file.pl";
	&winlock($filetomake) if ($OS_USED eq "Nt");
        open(IP, ">$filetomake");
        flock(IP,2) if ($OS_USED eq "Unix");
        print IP "$myip\n";
        close(IP);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
}

if (-e "$lbdir/forum$inforum/rate$intopic.file.pl") {
	require "$lbdir/forum$inforum/rate$intopic.file.pl";
	$votes = $votes +1;
	$rates = $rates + $rate;
	$average = int($rates / $votes);
	$filetomake = "$lbdir/forum$inforum/rate$intopic.file.pl";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(WRITE, ">$filetomake") || die ("���ܴ� $filetomake �ļ���<br> $!");
	flock(WRITE,2) if ($OS_USED eq "Unix");
	print WRITE "\$votes = $votes\;\n";
	print WRITE "\$rates = $rates\;";
	close(WRITE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	&ratings
}
else {
	$votes = 1;
	$rates = $rate;
	$average = $rate;
	$filetomake = "$lbdir/forum$inforum/rate$intopic.file.pl";
        &winlock($filetomake) if ($OS_USED eq "Nt");
	open(WRITE, ">$filetomake") || die ("���ܴ� $filetomake �ļ���<br> $!");
	flock(WRITE,2) if ($OS_USED eq "Unix");
	print WRITE "\$votes = $votes\;\n";
	print WRITE "\$rates = $rates\;";
	close(WRITE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	&ratings
}

sub ratings {
    $inmembername = cookie("amembernamecookie");
    $inpassword = cookie("apasswordcookie");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
    &title;
    $relocurl = "$threadprog?forum=$inforum&topic=$intopic";
    $output .= qq~
      <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
       <tr>
        <td width=30% rowspan=2 valign=top><img src=$imagesurl/images/$boardlogo border=0></td>
        <td valign=top align=left>
    ~;
    if ($indexforum ne "no"){
	$output .= qq~
        <font face=$font color=$fontcolormisc>
        ��<img src=$imagesurl/images/closedfold.gif border=0 width=15 height=11>��<a href="$forumsummaryprog">$boardname</a><br>
        ��<img src=$imagesurl/images/bar.gif border=0><img src="$imagesurl/images/openfold.gif" border=0 width=15 height=11>�� �������
	~;
    }else{
	$output .= qq~
        <font face=$font color=$fontcolormisc>
	<img src="$imagesurl/images/openfold.gif" border=0 width=15 height=11>�� �������
 	~;
    }
    $output .= qq~
        </td>
      </tr>
      </table>
	<p>
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font color=$fontcolormisc><b>�������</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>
            ��������û���Զ����أ������������ӣ�
            <ul>
            <li><a href=$threadprog?forum=$inforum&topic=$intopic>���ص�ǰ����</a>
            <li><a href=$forumsprog?forum=$inforum>���ص�ǰ��̳</a>
            <li><a href=$forumsummaryprog>������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
	<meta http-equiv="refresh" content="3; url=$relocurl">
    ~;

    &output(
        -Title   => $boardname,
        -ToPrint => $output,
        -Version => $versionnumber
    );
}
	