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
#            http://maildo.com/      ���һ����
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
require "visitforum.lib.pl";
$|++;                                     # Unbuffer the output
$thisprog = "help.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$inadmin                = $query -> param('admin');
$action                 = $query -> param('action');
$inhelpon               = $query -> param('helpon');
$inadminmodpass         = $query -> param("adminmodpass");
$inadminmodname         = $query -> param("adminmodname");
$inadminmodpass         = &cleaninput($inadminmodpass);
$inadminmodname         = &cleaninput($inadminmodname);
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inadminmodname =~ m/\//)||($inadminmodname =~ m/\\/)||($inadminmodname =~ m/\.\./));
$inadminmodname =~ s/\///g;
$inadminmodname =~ s/\.\.//g;
$inadminmodname =~ s/\\//g;

$inhelpon               = &cleaninput($inhelpon);
$inhelpon =~ s/\///g;
$inhelpon =~ s/\.cgi//ig;
$inhelpon =~ s/\.\.//g;
$inhelpon =~ s/\\//g;
$inadmin =~ s/\///g;
$inadmin =~ s/\.\.//g;
$inadmin =~ s/\\//g;
$cleanhelpname = $inhelpon;
$cleanhelpname =~ s/\_/ /g;
$cleanadminname = $inadmin;
$cleanadminname =~ s/\_/ /g;
if (($number) && ($number !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
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
print header(-charset=>gb2312);
    if ($inhelpon) {
        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
              <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 border=0 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>$boardname�İ����ļ�</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                       <br><center>$inmembername��ϣ������İ�����������</center><br><br>
                       <font face="$font" color=$fontcolormisc>
                       <b>����$cleanhelpname�İ�����</b><p>
	~;
        $filetoopen = "$lbdir" . "help/$inhelpon.dat";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen") or die "�޷���λ�����ļ���";
        @helpdata = <FILE>;
        close (FILE);

        foreach (@helpdata) {
            $output .= $_;
        }
    }
    elsif ($action eq "login") {

            &getmember("$inadminmodname");

            unless ($membercode eq "ad" ||($membercode eq 'smo')|| $membercode eq "mo") { &messangererror("�鿴����&��û��Ȩ�޲鿴���ļ���"); }
            if ($inadminmodpass ne $password) { &messangererror("�鿴����&�����������"); }

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
               <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 border=0 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>$boardname�İ����ļ�</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                      <br><center>$inadminmodname��ϣ������İ�����������</center><br><br>
                      <font face="$font" color=$fontcolormisc>
                      <b>����̳��/���������ļ�</b><p>
             ~;
            $dirtoopen = "$lbdir" . "help";
            opendir (DIR, "$dirtoopen") or die "���ܹ��ҵ������ļ�����Ŀ¼��$dirtoopen";
            @dirdata = readdir(DIR);
            closedir (DIR);
            @sorteddirdata = grep(/cgi$/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);

            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.cgi$//g;
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                $output .= qq~&nbsp;&nbsp;&nbsp;&nbsp;����<a href="$thisprog?admin=$filename" target="_self"><b>$cleanname</b></a>�İ���<p>~;
            }
	}
        elsif ($inadmin) {
	    &getmember("$inmembername");
            unless ($membercode eq "ad" || $membercode eq 'smo'|| $membercode eq "mo") { &messangererror("�鿴����&��û��Ȩ�޲鿴���ļ���"); }
            if ($inpassword ne $password) { &messangererror("�鿴����&�����������"); }
	    $output .= qq~
		<table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
                 <tr>
                  <td>
                  <table cellpadding=3 cellspacing=1 border=0 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>$boardname�İ����ļ�</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                      <br><center>$inmembername��ϣ������İ�����������</center><br><br>
                      <font face="$font" color=$fontcolormisc>
                      <b>����$cleanadminname�İ���</b><p>
            ~;

	    $filetoopen = "$lbdir" . "help/$inadmin.cgi";
            $filetoopen = &stripMETA($filetoopen);
            open (FILE, "$filetoopen") or die "�޷���λ�����ļ���";
            @helpdata = <FILE>;
            close (FILE);

	    foreach (@helpdata) {
                $output .= $_;
            }
        }
        else {
	    $output .= qq~
              <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
                <tr>
                <td>
                    <table cellpadding=3 cellspacing=1 border=0 width=100%>
                        <tr>
                            <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>$boardname�İ����ļ�</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                            <br><center>$inmembername��ϣ������İ�����������</center><br><br>
                            <font face="$font" color=$fontcolormisc>
                            <b>&nbsp;&nbsp;&nbsp;&nbsp;��������ļ�</b><p>
            ~;

            $dirtoopen = "$lbdir" . "help";
            opendir (DIR, "$dirtoopen") or die "���ܹ��ҵ������ļ�����Ŀ¼��$dirtoopen";
            @dirdata = readdir(DIR);
            closedir (DIR);
            @sorteddirdata = grep(/dat$/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);

            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.dat$//g;
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                $output .= qq~&nbsp;&nbsp;&nbsp;&nbsp;����<a href="$thisprog?helpon=$filename" target="_self"><b>$cleanname</b></a>�İ���<p>~;
            }
	}

    if ($passwordverification eq "yes") { $passwordverification = "�Ǳ����"; }
    else { $passwordverification = "���Ǳ����"; }

    if ($emailfunctions ne "on") { $emailfunctions = "�ر�"; }

    if ($emoticons eq "on") {
	$emoticons = "ʹ��";
        $emoticonslink = qq~| �鿴<a href=javascript:openwin('$miscprog?action=showsmilies',300,350)>����ת��</a>~;
    }
    else { $emoticons = "û��ʹ��"; }
    $output .= qq~<p><br><br>�鿴<a href=\"$thisprog\" target=\"_self\">���еİ����ļ�</a> $emoticonslink | �鿴 <a href=\"javascript:openwin('$miscprog?action=lbcode',300,350)\">LB5000 ��ǩ</a> | �鿴 <a href=\"javascript:openwin('lookemotes.cgi?action=style',300,350)\">EMOTE ��ǩ</a>~;

    $output .= qq~
    </td></tr>
    <tr>
    <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>��̳������Ϣ</b><br><br>
    �����Զ�ת����<b>$emoticons</b><br>�ʼ���ַȷ�ϣ�<b>$passwordverification</b><br>��̳�ʼ����ܣ�<b>$emailfunctions</b><br><br>
    </td>
    </tr>
    <tr>
    <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc><b>��½����̳��/�����İ���</b><br>

    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="login">
    <font face="$font" color=$fontcolormisc>
    �û�����&nbsp; <input type=text name="adminmodname" value="$inmembername"5> &nbsp;
    �ܡ��룺&nbsp; <input type=password name="adminmodpass" value="$inpassword"5> &nbsp; <input type=submit value="�� ½"></td></tr></form>
    </table></td></tr></table>
    ~;

    &printmessanger(
        -Title   => "$boardname - ����",
        -ToPrint => $output,
        -Version => $versionnumber
    );

sub messangererror {
    my $errorinfo = shift;
    (my $where,my $errormsg) = split(/\&/, $errorinfo);
    $output = qq~
      <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
	<tr>
        <td>
        <table cellpadding=6 cellspacing=1 border=0 width=100%>
        <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>����$where</b></font></td></tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
                <b>����$where�������ϸԭ��</b>
                <ul>
                <li><b>$errormsg</b>
                <li>���Ƿ���Ҫ�鿴<a href=>�����ļ�</a>?
                </ul>
                <b>����$where����Ŀ���ԭ�򣺣�</b>
                <ul>
                <li>�������<li>�û�������<li>������<a href=>ע��</a>�û�
                </ul>
                </tr>
                </td></tr>
                <tr>
                <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc> <a href="javascript:history.go(-1)"> << ������һҳ</a>
                </td></tr>
                </table></td></tr></table>
    ~;
    &printmessanger(
       -Title   => $boardname,
       -ToPrint => $output,
       -Version => $versionnumber
    );
}