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
require "data/boardinfo.cgi";
require "code.cgi";
require "data/progs.cgi";
require "data/styles.cgi";
require "lbmail.lib.pl";
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "postjs.cgi";
$|++;                        # Unbuffer the output
$thisprog = "xzb.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip


for ('forum','membername','password','action','inpost','message','id') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inforum       = $forum;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
$inmembername  = $membername;
$inpassword    = $password;
$currenttime   = time;
$postipaddress = "$ENV{'REMOTE_ADDR'}=$ENV{'HTTP_X_FORWARDED_FOR'}";

$inselectstyle   = $query->cookie("selectstyle");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
    if ($inmembername eq "") {
        $inmembername = "����";
    }
    &getmember("$inmembername");

    if ($mainonoff == 1) { &InMaintenance; }
    print header(-charset=>gb2312);

    $helpurl = &helpfiles("�Ķ����");
    $helpurl = qq~$helpurl<img src=$imagesurl/images/help_b.gif border=0></a>~;

    my %Mode = (
    'new'	=>	\&newthread,
    'addnew'	=>	\&addnewthread,
    'view'	=>	\&view,
    'del'	=>	\&del,
    );

    if($Mode{$action}) {
        $Mode{$action}->();
    }
    else { &error("��ͨ&������ȷ�ķ�ʽ���ʱ�����"); }

    &output(
	-Title   => "$boardname - ��$forumname�ڷ�С�ֱ�",
	-ToPrint => $output,
	-Version => $versionnumber
    );

sub newthread {
#    &getmember("$inmembername");

    &getforum("$inforum");
    if (($privateforum eq "yes")||($xzbopen eq "no")||($startnewthreads eq "no")){
    	&error("����С�ֱ�&����̳����������С�ֱ�!");
    	}

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t$forumname\tnone\t����С�ֱ�\t") if ($privateforum ne "yes");
    &whosonline("$inmembername\t$forumname(��)\tnone\t�����µı���С�ֱ�\t") if ($privateforum eq "yes");
}

    &mischeader("����С�ֱ�");



            $startthreads = "�κ�ע���Ա(��̳���Ͱ���)������������";

    	$output .= qq~
                <form action="$thisprog" method=post name="FORM" >
                <input type=hidden name="action" value="addnew">
                <input type=hidden name="forum" value="$inforum">
        	<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            	<tr><td>
                <table cellpadding=3 cellspacing=1 border=0 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2><font color=$titlefontcolor><b>˭��������С�ֱ���</b> $startthreads</td>
                </tr>
                <tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>�û���</b></font></td>
                <td bgcolor=$miscbackone>��<input type=text name="membername" value="$inmembername">�� <font color=$fontcolormisc><a href="$registerprog">��û��ע�᣿</a></font></td>
                </tr><tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>�ܡ���</b></font></td>
                <td bgcolor=$miscbackone>��<input type=password name="password" value="$inpassword">�� <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">�������룿</a></font></td>
                </tr>
		<tr>
		<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>С�ֱ�����(��� 80 ��)</b></td>
		<td bgcolor=$miscbackone>
		��<input type="text" maxlength="80" name=inpost onkeydown=ctlent() value="$inpost" size=80><br>

		</td></tr>
		<tr>
		<td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>С�ֱ�����</b><p>
		 �ڴ���̳�У�<li>HTML ��ǩ: <b>������</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LB5000 ��ǩ</a>: <b>����</b>
		</td>
		<td bgcolor=$miscbacktwo valign=top>
		<b>����ÿСʱһ����һ�����������������48Сʱ</b><br>��
		<TEXTAREA cols=58 name=message rows=6 wrap=soft onkeydown=ctlent()>$message</TEXTAREA>
		</td>
		</tr>
		<tr>
                <td bgcolor=$miscbacktwo colspan=2 align=center>
                <input type=Submit value="�� ��" name=Submit"  onClick="return clckcntr();">������<input type="reset" name="Clear" value="�� ��">
                </td></form></tr>
            </table>
        </tr></td></table>
        ~;
}

sub addnewthread {

#    &getmember("$inmembername");


    if    ($userregistered eq "no")     { &error("����С�ֱ�&��û��ע�ᣡ"); }
    elsif ($inpassword ne $password)    { &error("����С�ֱ�&�����������"); }
    elsif ($membercode eq "banned")     { &error("����С�ֱ�&������ֹ���ԣ�"); }
    elsif ($inpost eq "")               { &error("����С�ֱ�&����������⣡"); }
    elsif (length($inpost) > 82)        { &error("������ͶƱ&���������"); }
    else  {
        &getforum("$inforum");
if (($privateforum eq "yes")||($xzbopen eq "no")||($startnewthreads eq "no")){
    	&error("����С�ֱ�&����̳����������С�ֱ�!");
    	}

        $dirtoopen = "$lbdir" . "boarddata";
        open (DIR, "<$dirtoopen/xzb$inforum.cgi");
        @xzbdata = <DIR>;
        close (DIR);
        chomp(@xzbdata);
        $sizexzb=@xzbdata;
        $currenttime = time;
        if (($membercode eq "ad") ||($membercode eq 'smo')|| ($inmembmod eq "yes")) {
           &error("����С�ֱ�&�����̳�����ò���,лл������");
        }

	($tmp, $tmp,$tmp,$tmp,$lastpost)=split(/\t/,$xzbdata[0]);
	$lastpost = ($lastpost + 3600);

	if ($lastpost > $currenttime)  {
           &error("����С�ֱ�&���Сʱ�Ѿ����˷�����һ��С�ֱ��ˣ����һ��Сʱ������");
	}

        $inpost=~s/</&lt;/sg;
        $inpost=~s/>/&gt;/sg;
        $sizexzb=48 if ($sizexzb >48);
        $write="����������\t$inpost\t$inmembername\t$message\t$currenttime\t";
        @newxzb=($write,@xzbdata);
        open(DIR,">$dirtoopen/xzb$inforum.cgi");
        for ($i=0;$i<=$sizexzb;$i++){
             	print DIR "$newxzb[$i]\n";
        }

        &mischeader("��С�ֱ������ɹ�");

            	$relocurl = "$forumsprog?forum=$inforum";

        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>лл��������С�ֱ��Ѿ������ɹ���</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ��������û���Զ����أ�������������ӣ�
            <ul>
            <li><a href="$forumsprog?forum=$inforum">������̳</a>
            <li><a href="$forumsummaryprog">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;

    }
}



sub view {
&error("�ϴ������ҵĳ���!") if (($id eq "")||($inforum eq ""));
	$dirtoopen = "$lbdir" . "boarddata";
	open (DIR, "<$dirtoopen/xzb$inforum.cgi");
        @xzbdata = <DIR>;
        close (DIR);
        chomp(@xzbdata);
        &getforum("$inforum");
        $xzbdata[$id] =~ s/^����������\t//isg;
        ($title,$postid,$msg,$posttime)=split(/\t/,$xzbdata[$id]);

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t$forumname\tnone\t�Ķ�С�ֱ�\t") if ($privateforum ne "yes");
        &whosonline("$inmembername\t$forumname(��)\tnone\t�Ķ�����С�ֱ�\t") if ($privateforum eq "yes");
}

#       &getmember("$inmembername");
	$dateposted = $posttime + ($timedifferencevalue*3600) + ($timezone*3600);
        $dateposted = &dateformat("$dateposted");
        $msg = &lbcode("$msg");
       $admindelete=qq~
       <a href=xzb.cgi?action=del&forum=$inforum&id=$id>ɾ��</a>
       ~;
	$output=qq~
	<html><body><head>
	<title>�Ķ�С�ֱ�</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline 	}
		A:link 	  {	text-decoration: none;}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT	{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT	{	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}

</style>
	</head>
	<table cellpadding=0 cellspacing=0 border=0 width=97% bgcolor=#000000 align=center>
	                <tr>
	                    <td>
	                    <table cellpadding=3 cellspacing=1 border=0 width=100% style="TABLE-LAYOUT: fixed">
	~;




	$output .= qq~
	                  <tr>
	                  <td bgcolor=$titlecolor align=center valign=top><font face="$font" color=$titlefontcolor><b>>> $title <<</b></td></tr>
		    ~;
		    if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||($postid eq "$inmembername")) {
			  $output .= qq~
	                      	<tr>
	                      	    <td bgcolor=$postcolortwo align=right>$admindelete</td>
	                       	</tr>
			  ~;
		    }

       $output .= qq~
	                 <tr>
	                    <td bgcolor="$postcolortwo" valign=top style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word"><font face="$font" color=$postfontcolortwo>
	                        $msg
	                    </td>
	                 </tr>
	                 <tr>
	                    <td bgcolor="$postcolortwo" valign=middle>
	                     <table width=100% border="0" cellpadding="0" cellspacing="0">
	                        <tr><td align=left>&nbsp;&nbsp;&nbsp;<font face="$font" color=$postfontcolortwo><b>������</b>�� $postid</font>
	                        </td><td align=right><font face="$font" color=$postfontcolortwo><b>����ʱ��</b>�� $dateposted</font>&nbsp;&nbsp;&nbsp;
	                        </tr>
	                        </table>
	                        </td>
	                        </font>
	                        </tr></table></td></tr></table></body></html>

	              ~;
	             print header(-charset=>gb2312);
	             print $output;

exit;
}

sub del {
	&error("�ϴ������ҵĳ���!") if (($id eq "")||($inforum eq ""));
	$dirtoopen = "$lbdir" . "boarddata";
	open (DIR, "<$dirtoopen/xzb$inforum.cgi");
        @xzbdata = <DIR>;
        $sizexzb=@xzbdata;
        close (DIR);
        chomp(@xzbdata);
#        &getmember("$inmembername");
        ($nouse, $title,$postid,$msg,$posttime)=split(/\t/,$xzbdata[$id]);
         if (($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes")&&($postid ne "$inmembername")) {
        &error("ɾ��С�ֱ�&��ûȨ��ɾ��!");
}

        open (DIR, ">$dirtoopen/xzb$inforum.cgi");
        for ($i=0;$i<$sizexzb;$i++){
        	if ($i ne $id){
             	print DIR "$xzbdata[$i]\n";

             	}
        }
        close (DIR);

	$output=qq~
	<script>top.window.close();</script>
	~;
	             print header(-charset=>gb2312);
	             print $output;

exit;
}