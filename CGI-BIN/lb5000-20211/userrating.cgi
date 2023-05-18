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
require "lbmail.lib.pl";
require "data/boardinfo.cgi";
require "data/boardstats.cgi";
require "data/progs.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "data/membertitles.cgi";
require "lb.lib.pl";
$|++;

#################--- Begin the program ---###################

$thisprog = "userrating.cgi";

$query = new LBCGI;


$editmembername = $query -> param ("membername");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($editmembername =~ m/\//)||($editmembername =~ m/\\/)||($editmembername =~ m/\.\./));
$editmembername =~ s/\///g;
$editmembername =~ s/\.\.//g;
$editmembername =~ s/\\//g;

$action         = $query -> param ("action");
$inforum        = $query -> param ("oldforum");
$intopic        = $query -> param ("oldtopic");
if (($inforum)  && ($inforum !~ /^[0-9]+$/))  { &error("��ͨ&�ϴ󣬱��Һ��ҵĳ���ѽ��"); }
if (($intopic)  && ($intopic !~ /^[0-9]+$/))  { &error("��ͨ&�ϴ󣬱��Һ��ҵĳ���ѽ��"); }

$inselectstyle   = $query->cookie("selectstyle");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

$inmembername   = cookie("amembernamecookie");
$inpassword     = cookie("apasswordcookie");
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

if ($action eq "") {
	$action = "login";
}

    print header(-charset=>gb2312);
&getforum($inforum);

    &title;
    if ($forumgraphic) { $forumgraphic = qq~<a href=$forumsprog?forum=$inforum><img src=$imagesurl/images/$forumgraphic border=0></a>~; }
        else { $forumgraphic = qq~<a href=$forumsummaryprog><img src=$imagesurl/images/$boardlogo border=0></a>~; }
    $output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
        <tr>
            <td width=30% rowspan=2>
            $forumgraphic
            </td>
            <td valign=top>
                <font color=$fontcolormisc>
	        ��<img src=$imagesurl/images/closedfold.gif width=15 height=11><a href=$forumsummaryprog>��$boardname</a><br>
                ��<img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>�����û�ͶƱ
            </td>
        </tr>
    </table>
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 border=0 width=100%>
    ~;

if ($action eq "login") {
	$inmembername =~ s/\_/ /g;
        $output .= qq~
        <tr>
        <td bgcolor=$miscbacktwo colspan=2 align=center><font color=$fontcolormisc>
        <form action="$thisprog" method="post">
        <input type=hidden name=action value="logmein">
        <input type=hidden name=oldforum value=$inforum>
        <input type=hidden name=oldtopic value=$intopic>
        <b>�����ȵ�½Ȼ��� $editmembername ͶƱ(����̳���Ͱ�������)</b></font></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc >�������������</font></td>
        <td bgcolor=$miscbackone><input type=text name="inmembername" value="$inmembername" size=20></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc >�������������</font></td>
        <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword" size=20></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc >��ͶƱ�û�����</font></td>
        <td bgcolor=$miscbackone><input type=text name="membername" value="$editmembername" size=20></td></tr>
        <tr>
        <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="��½ͶƱ"></td></form></tr></table></td></tr></table>
        ~;
    }
    elsif ($action eq "logmein") {

	$inmembername   = $query -> param ("inmembername");
	$inpassword     = $query -> param ("password");
	$editmembername = $query -> param ("membername");
	$inforum        = $query -> param ("oldforum");
	$intopic        = $query -> param ("oldtopic");

	$verify = "no";

	&getmember("$inmembername");

	if ("$userregistered" eq "no")    { &error("�û�ͶƱ&û�и�ע���û�");   }
	if ("$inpassword" ne "$password") { &error("�û�ͶƱ&����Ĺ���Ա����"); }
	if ($membercode eq "ad")          { $verify = "yes"; }
	if ($membercode eq 'smo')	  { $verify  = "yes"; }
	if ($membercode eq "mo")          { $verify = "yes"; }

	if ($verify ne "yes") { &error("�û�ͶƱ&��������Ա����ͶƱ"); }
	else {
	    &getmember("$editmembername");
	    if ("$userregistered" eq "no")    { &error("�û�ͶƱ&û�и�ע���û�");   }
            if ($membercode eq "ad" || $membercode eq 'smo' || $membercode eq "mo") { &error("���û�ͶƱ&̳���Ͱ������ܱ�ͶƱ"); }

	    if ($rating eq "") {
		$rating = 0;
	    }
	    $rating=$rating+0;
	    if ($rating < -6) { $rating = -6; }
	    if ($rating > $maxweiwang) { $rating = $maxweiwang; }

	    if ($rating == $maxweiwang) { $pwout = qq~<input type=radio name=pw value=warn CHECKED>�����û�~; }
	    elsif ($rating == -5) { $pwout = qq~<input type=radio name=pw value=praise CHECKED>�����û�����<input type=radio name=pw value=warn>��ֹ�û�</td>~; }
	    elsif ($rating == -6) { $pwout = qq~<input type=radio name=pw value=praise CHECKED>�ָ��û�~; }
	    else { $pwout = qq~<input type=radio name=pw value=praise CHECKED>�����û�����<input type=radio name=pw value=warn>�����û�����<input type=radio name=pw value=reset>���㡡��<input type=radio name=pw value=worst>��ֹ����</td>~; }

	    $output .= qq~
		<tr>
		<td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>$editmembername ��������: $rating</b></font></td>
		</tr>
		<tr>
		<td bgcolor=$miscbackone align=center>
		<form action="$thisprog" method="post">
		<input type=hidden name=action value=process>
		<input type=hidden name=sender value="$inmembername">
		<input type=hidden name=member value="$editmembername">
		<input type=hidden name=password value="$inpassword">
		<input type=hidden name=oldforum value=$inforum>
		<input type=hidden name=oldtopic value=$intopic>
		���ѡ����: $pwout
		</tr>
		<tr>
		<td bgcolor=$miscbackone align=center><font color=$fontcolormisc>ͶƱԭ��:<br><textarea size=20 name="reason" cols="40" rows="5"></textarea></td>
		</tr>
		<tr>
		<td bgcolor=$miscbackone align=center>
		֪ͨ�û�: <input type=radio name=notify value=yes >�ǡ���<input type=radio name=notify value=no CHECKED>��</td>
		<tr>
		<td bgcolor=$miscbacktwo align=center>
		<input type=submit value=ȷ�� name=submit>
		</td>
		</form>
		</tr>
		</table>
		</td>
		</tr>
		</table>
	   ~;
	}
    }
    elsif ($action eq "process") {

        print header(-charset=>gb2312);

	$inpassword     = $query -> param ("password");
	$sender   = $query -> param ("sender");
	$member   = $query -> param ("member");
	$pw       = $query -> param ("pw");
	$reason   = $query -> param ("reason");
	$notify   = $query -> param ("notify");
	$inforum  = $query -> param ("oldforum");
	$intopic  = $query -> param ("oldtopic");

	&getmember("$sender");

	if ("$userregistered" eq "no")    { &error("�û�ͶƱ&û�и�ע���û�");   }
	if ("$inpassword" ne "$password") { &error("�û�ͶƱ&����Ĺ���Ա����"); }
	if ($membercode eq "ad")          { $verify = "yes"; }
	if ($membercode eq 'smo')	  { $verify  = "yes"; }
	if ($membercode eq "mo")          { $verify = "yes"; }

	if ($verify ne "yes") { &error("�û�ͶƱ&��������Ա����ͶƱ"); }

    	if (($notify eq "yes") && ($reason eq "")) {   &error("�û�ͶƱ&��������֪ͨ�û��������������.");  }

        &getmember("$member");
        if ($membercode eq "ad" || $membercode eq 'smo' || $membercode eq "mo") { &error("���û�ͶƱ&̳���Ͱ������ܱ�ͶƱ"); }

        if ($pw eq "praise") {
            $pwmail    = "����";
            $pwmailing = "����";
            $rating++;
        }
        elsif ($pw eq "warn") {
            $pwmail    = "����";
            $pwmailing = "����";
            $rating--;
        }
        elsif ($pw eq "reset") {
        	$pwmail = "�ָ�����Ϊ��";
        	$pwmailing = "�ָ�";
        	$rating = 0;
        }
        else {
        	$pwmail = "�������������";
        	$pwmailing = "����";
        	$rating = -6;
        };

        if ($rating < -6)  { $rating = -6; }
        if ($rating > $maxweiwang)   { $rating = $maxweiwang ; }
        if ($rating eq "") { $rating = 0 ; }

        if ($rating == -6) {
            $newmembercode = "banned";

            $filetoopen = "$lbdir" . "data/banemaillist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$emailaddress\t";
            close(FILE);
            $filetoopen = "$lbdir" . "data/baniplist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$ipaddress\t";
            close(FILE);

        }
        else {
            $newmembercode = "me";
        }

        if ($newmembercode eq "banned") { $membertitleout = "����ֹ"; }
        else { $membertitleout = "��ͨ��Ա"; }

	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$trueipaddress = "no" if (($trueipaddress eq "")||($trueipaddress eq "unknown"));
	my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$trueipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
	my $thistime=time;
	$filetomake = "$lbdir" . "data/userratinglog.cgi";
   	if (open(FILE0, ">>$filetomake")) {
        flock(FILE0, 2) if ($OS_USED eq "Unix");
   	print FILE0 "$member\t$sender\t$rating\t$thistime\t$inforum\t$intopic\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t\n";
	close(FILE0);
	}

   if ($notify eq "yes") {
        &notifypw;
	$to = $adminemail_in;
	$from = $adminemail_out;
	$subject = "$member �Ѿ��� $sender $pwmail !";
	$message .= "\n";
	$message .= "$homename\n";
	$message .= "$boardurl/$forumsummaryprog\n";
	$message .= "$boardurl/$threadprog?forum=$inforum&topic=$intopic\n\n\n";
	$message .= "$member �Ѿ��� $sender $pwmail !\n";
	$message .= "$member ������������: $rating\n";
	$message .= "$member ��״̬������: $membertitleout\n\n\n";
	$message .= "�� $pwmailing $member ��ԭ����:\n";
	$message .= "$reason\n\n";
	$message .= "��������Ϊ����ȷ, ��� $sender ˵˵\n";
	&sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
   }

   $memberfiletitle = $member;
   $memberfiletitle =~ s/ /\_/isg;
   $memberfiletitle =~ tr/A-Z/a-z/;

if (($member ne "")&&($password ne "")) {
   $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
   &winlock($filetomake) if ($OS_USED eq "Nt");
   if (open(FILE0, ">$filetomake")) {
   flock(FILE0, 2) if ($OS_USED eq "Unix");
   print FILE0 "$member\t$password\t$membertitle\t$newmembercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t";
   close(FILE0);
   }
   &winunlock($filetomake) if ($OS_USED eq "Nt");
}
   $output .= qq~
      <tr>
	<td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>$member �Ѿ��ɹ���$pwmail</b></font></td>
	</tr>
	<tr>
	<td bgcolor=$miscbackone>
	<font color=$fontcolormisc>�������:
	<br><ul>
	    <li><a href="$threadprog?forum=$inforum&topic=$intopic">���ص�ǰ���� </a>$pages
            <li><a href="$forumsprog?forum=$inforum">���ص�ǰ��̳</a>
            <li><a href="$forumsummaryprog">������̳��ҳ</a>
        </ul>
	</td>
	</tr>
	</table>
	</td>
	</tr>
	</table>
    ~;
}
    sub notifypw {

   	$to = $emailaddress;
        $from = $adminemail_out;
        $subject = "���Ѿ��� $sender $pwmail !";
        $message .= "\n";
        $message .= "$homename\n";
        $message .= "$boardurl/$forumsummaryprog\n";
	$message .= "$boardurl/$threadprog?forum=$inforum&topic=$intopic\n\n\n";
        $message .= "���Ѿ��� $sender $pwmail !\n\n\n";
        $message .= "�����ڵ�������: $rating\n";
        $message .= "�����ڵ�״̬��: $membertitleout\n";
        $message .= "�㱻 $pwmailing ��ԭ����:\n";
        $message .= "$reason\n\n";
        $message .= "��������Ϊ�д�, �뷢�Ÿ�\n";
        $message .= "̳��: $adminemail_in ����ԭ��\n";
        &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
   }

print header(-charset=>gb2312);
&output(
       -Title   => "$boardname - �û�ͶƱ",
       -ToPrint => $output,
       -Version => $versionnumber
);

