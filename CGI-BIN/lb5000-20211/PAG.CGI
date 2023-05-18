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
require "code.cgi";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "lbmail.lib.pl";
require "visitforum.lib.pl";
$|++;
$thisprog = "pag.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/$thisprog//sg;
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$email        = $query -> param('email');

print header(-charset=>gb2312);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
	    if ($regaccess eq "on") {
	    	print header(-cookie=>[$namecookie, $passcookie], -charset=>gb2312);
	    	print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	    	exit;
	    }
}
else {
    &getmember("$inmembername");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
    if (($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')) { $allowed = "yes"; } else { $allowed = "no"; }
#        &getmemberstime("$inmembername");
        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$inforum};
        $currenttime = time;
        &setlastvisit("$inforum,$currenttime");
    }

    $filetoopen = "$lbdir" . "data/allforums.cgi";
    open(FILE, "$filetoopen");
    @forums = <FILE>;
    close(FILE);
    foreach $forumline (@forums) {
        ($tempno, $trash) = split(/\t/,$forumline);
        if ($inforum eq $tempno) {
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forumline);
        }
    }
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @threads = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    ($trash, $topictitle, $trash) = split(/\t/, @threads[0]);
    $topictitle =~ s/^����������//;
    $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));

    if (($privateforum eq "yes") && ($allowed ne "yes")) {
        &error("����˽����̳&�Բ�������Ȩ���������̳��");
    }
    else {
      my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
      $filetoopens = &lockfilename($filetoopens);
      if (!(-e "$filetoopens.lck")) {
        if ($privateforum ne "yes") {
            &whosonline("$inmembername\t$forumname\tnone\t����ʵ�����<a href=\"$threadprog?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
        }
        else {
            &whosonline("$inmembername\t$forumname(��)\tnone\t����ʵ����ӱ�������\t");
        }
      }
    }
&badwordfile;
if ($emailfunctions eq "off") { &error("����ʵ�&�ǳ���Ǹ����̳�ķ����ʼ������Ѿ��رգ�");  }

    if ($badwords) {
        @pairs = split(/\&/,$badwords);
        foreach (@pairs) {
            ($bad, $good) = split(/=/,$_);
            chomp $good;
            $topictitle=~ s/$bad/$good/isg;
        }
    }

    if ($email){
        if ($email !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) { &error("����ʵ�&������ʼ���ַ��"); }
        $email =~ s/[\a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
        $output .= qq~
        <html><head><title>$boardname</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}

	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
	</style>
    </head>
    <body topmargin=10 leftmargin=0>
    <table cellpadding=0 cellspacing=0 border=0 width=90% align=center>
        <tr>
            <td>
            <p><b>��$boardname���������</b><p>
            <b>�� ̳ ��- $boardname</b> ($boardurl/$forumsummaryprog)<br>
            <b>��������-- $forumname</b> ($boardurl/$forumsprog?forum=$inforum)<br>
            <b>���ӱ���--- $topictitle</b> ($boardurl/$forumsprog?forum=$inforum&topic=$intopic)
        </tr>
    </table>
    <p><p><p>
    <table cellpadding=0 cellspacing=0 border=0 width=90% align=center>
        <tr>
            <td>

    ~;
    foreach $line (@threads) {
        ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\t/,$line);
        $post = &lbcode("$post");
        $post =~ s/&lt\;/\</g;
        $post =~ s/&gt\;/\>/g;
        $post =~ s/&quot\;/\"/g;
        $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $post=~ s/$bad/$good/isg;
            }
        }
        $output .= qq~
        <p>
        <hr><p>
        -- �����ˣ� $postermembername<BR>
        -- ����ʱ�䣺 $postdate<p>
        $post
        <p><p>
        ~;
    }
    $output .= qq~
        </td></tr></table><center><hr><p>$boardname<br>&copy; 2000 cgier.com</center>
        </body></html>
    ~;
    $filetoopen = "$lbdir" . "forum$inforum/mail${intopic}.htm";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE $output;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    $from = $adminemail_out;
    $subject = "��$boardname����ʵݹ���������";
    if (($SMTP_SERVER ne "")&&($emailtype eq "smtp_mail")){
	require "${lbdir}SendMail.pm.pl";
	eval("use MIME::Base64;");
	eval("use MIME::QuotedPrint;");
	$obj = new SendMail($SMTP_SERVER, $SMTP_PORT);
	$obj->setDebug($obj->OFF);
	$obj->From($from);
	$obj->Subject($subject);
	$obj->To($email);
	$header= "X-Mailer";
	$headervalue= "Perl SendMail Module 2.03";
	$mailbodydata= qq~<html>
	   <STYLE type=text/css>
		A:link    {	COLOR: #7547B5;	TEXT-DECORATION: none	}
		A:visited {	COLOR: #6547B5; TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	COLOR: #555555;	TEXT-DECORATION: underline overline	}
		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;		}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt; color:#000000;	}
		DIV    {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
	</STYLE>
	<body bgcolor="#c8c8c8">
	<p align="center"><br>
  ������ϸ�л��ʹ�� LeoBoard 5000 ������<br>
  Thanks for use LeoBoard 5000 board!!!</p>
<table width="63%" border="0" align="center">
  <tr>
    <td><font color=black>�������Ǵ� $boardname ����ʵݹ���������</font><br>
    ��̳��������:<br>
        <script src="http://www.leoboard.com/cgi-bin/news.cgi?forum=2&max=20" language="">
</script>
<hr>
      <p>CGIer.com CEO ɽӥ(��)<br>
        CGIer.com CTO ����ȱ<br>
        <a href=http://www.cgier.com/>http://www.cgier.com/</a><br>
        <a href=http://leoboard.com/>http://leoboard.com/</a> </p>
</td>
  </tr>
</table>
<div align="center"><br>
  <a href="http://www.leobbs.com">���� LB5000 ������̳ </a></div>
</body></html>~;
    $obj->setMailHeader($header, $headervalue);
    $obj->setMailBody($mailbodydata);
    $obj->Inline($filetoopen);
    if ($obj->sendMail() != 0) {
    print $obj->{'error'}."\n";
	}
    $obj->reset();
}
else {
   $output.= "\nLB5000 ��̳������֧�֣�http://www.leoBBS.com/\n";
   $output.= "���İ�Ȩ��CGI �����֮��  http://www.CGIer.com/\n";
    if ($SEND_MAIL ne "") {
	    open (MAIL,"| $SEND_MAIL -t");
	    print MAIL "To: $email\n";
	    print MAIL "From: $from\n";
	    print MAIL "Subject: $subject\n";
	    print MAIL "Content-Type: text/html;charset=gb2312\n";
 	    print MAIL "$output\n";
	    print MAIL "\n.";
	    close(MAIL);
    }
    else{
       if ($emailtype eq "blat_mail") {
	open(MAIL,"|blat $filetoopen -t \"$email\" -b \"$bccinfo\" -i \"$from\" -f \"$from\" -s \"$subject\"");
        close(MAIL);
       }
       else {
       	   $smtp = $SMTP_SERVER;
	   &smtpmail($email, $from, $subject, $output, $smtp);
       }
    }
}
    unlink $filetoopen;
    print "<center><br><b>�ʵ��������!</b><br><br>�Զ��رմ���<script>top.window.close()</script></center>";
    exit;
}
else {
    $output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=460 align=center>
    <tr>
        <td width=30% rowspan=2 valign=top><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td align=left><font color=$fontcolormisc>
        ��<img src=$imagesurl/images/closedfold.gif border=0>��<a href=$forumsummaryprog>$boardname</a><br>
        ��<img src=$imagesurl/images/bar.gif border=0><img src=$imagesurl/images/openfold.gif border=0>������ʵ�
        </td>
    </tr>
    </table>
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=460 bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 border=0 width=100%>
    <form action="$boardurl/$thisprog" method=post>
    <tr>
    <td bgcolor=$miscbacktwo colspan=2 align=center>
    <input type=hidden name="forum" value="$inforum">
    <input type=hidden name="topic" value="$intopic">
    <font color=$fontcolormisc><b>����ʵ�</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc>
    <b>�ѱ��� <a href=$threadprog?forum=$inforum&topic=$intopic>$topictitle</a> ����ʵݡ�</b><br>����ȷ������Ҫ�ʵݵ��ʼ���ַ��
    </td></tr><tr>
    <td bgcolor=$miscbacktwo><font color=$fontcolormisc><b>�ʵݵ� Email ��ַ��</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="email"></td>
    </tr><tr>
    <td colspan=2 bgcolor=$miscbacktwo align=center><input type=submit value="�� ��" name="Submit"></table></td></form></tr></table>
    ~;
    &output(
	-Title   => $boardname,
	-ToPrint => $output,
	-Version => $versionnumber
    );
}