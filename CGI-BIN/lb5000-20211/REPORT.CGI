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
require "lbmail.lib.pl";
require "lb.lib.pl";
$|++;                        # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "report.cgi";

$query = new LBCGI;

&ipbanned; #��ɱһЩ ip

$inforum       = $query -> param('forum');
$intopic       = $query -> param('topic');

$action          = $query -> param('action');

$insubject       = $query -> param('subject');
$inemailmessage  = $query -> param('emailmessage');
$emailtopictitle = $query -> param('emailtopictitle');
$intouser        = $query -> param('touser');
$inmembername    = $query -> param('membername');
$inpassword      = $query -> param('password');
$inmsgtitle	 = $query -> param('subject');
$inmessage	 = $query -> param('emailmessage');
$inoriginalpost  = $query -> param('originalpost');
$inpost2 = "<BR><BR><b>����ԭʼλ�ã�</b> $boardurl/$threadprog?forum=$inforum&topic=$intopic<br>";

$insubject           = &cleaninput($insubject);
$inemailmessage      = &cleaninput($inemailmessage);
$emailtopictitle     = &cleaninput($emailtopictitle);
$inforum             = &cleaninput($inforum);
$inoriginalpost      = &cleaninput($inoriginalpost);

$inmembername        = &cleaninput($inmembername);
$inpassword          = &cleaninput($inpassword);
$inpostno      	     = $query -> param('postno');

$inmessage2 = $inemailmessage.$inoriginalpost.$inpost2;

# new
$add_user2	= $query -> param('touser1');
# -- new

print header(-charset=>gb2312);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie"); }
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

&title;


$output .= qq~
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
    <tr>
        <td width=30% rowspan=2><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td valign=middle align=left><font color=$fontcolormisc>
        ��<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">��$boardname</a><br>
        ��<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>�����������������
        </td>
    </tr>
</table>
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
        <td>
        <table cellpadding=6 cellspacing=1 border=0 width=100%>
        ~;

if ($action eq "send") {

}

else {


    $filetoopen = "$lbdir" . "data/allforums.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
    @forums = <FILE>;
    close(FILE);

    foreach $forumline (@forums) { #start foreach @forums
        ($tempno, $trash) = split(/\t/,$forumline);
        if ($inforum eq $tempno) {
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forumline);
            }
        }

    $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
    @allthreads = <FILE>;
    close(FILE);

    foreach $line (@allthreads) { #start foreach @threads
            ($tempno, $trash) = split(/\t/, $line);
            if ($intopic eq $tempno) {
                $linetokeep = $line;
            }
        } # end foreach


        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\t/,$linetokeep);
$topictitle =~ s/^����������//;
# Get the post to edit

$filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
    flock(FILE, 2);
    @threads = <FILE>;
    close(FILE);

    $posttoget = --$inpostno;
($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, @threads[$posttoget]);
$topictitle =~ s/^����������//;
    $post =~ s/\<p\>/\n\n/g;
    $post =~ s/\<br\>/\n/g;

    $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
    $postdate = &dateformat("$postdate");

 $rawpost = $post;

    $temppost = qq~ԭʼ������ $membername �� $postdate �������������£�\[br\]$rawpost~;


### print form
if ($forummoderator eq "") {
&error("���ͱ���&�����û�����ð�����"); }
else {
$recipient = $forummoderator }

@recipientname = split(",",$recipient);

$toto = qq~<select name="touser">~;
foreach (@recipientname) {
    $toto .= qq~<option value="$_">$_</option>~;
}
$toto .= qq~</select>~;
&getforum("$inforum");

 &error("���ͱ���&����ǰ�������ʲô�ɻ���") if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"));

    $topictitle = &cleanarea("$topictitle");

    $output .= qq~
    <form action="$boardurl/$thisprog" method=post>
    <input type=hidden name="action" value="send">
    <input type=hidden name="forum" value="$inforum">
    <input type=hidden name="topic" value="$intopic">
	<tr>
    		<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
			<font color=$fontcolormisc><b>�����Ա���������������</b></font>
		</td>
	</tr>
  	<tr>
                <td bgcolor=$miscbackone valign=middle>
			<font color=$fontcolormisc><b>�û���</b></font>
		</td>
                <td bgcolor=$miscbackone valign=middle>
		<input type=text name="membername" value="$inmembername"> &nbsp; <font color=$fontcolormisc><a href="$registerprog">��û��ע�᣿</a></font>
		</td>
	</tr>
	<tr>
                <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>����</b></font>
		</td>
                <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">�������룿</a></font>
                <input type=hidden size=40 name="subject" value="��������������ӣ� $topictitle">
		</td>
	</tr>
	<tr>
                <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>���淢�͸��ĸ�����</b></font>
		</td>
                <td bgcolor=$miscbackone valign=middle>$toto
		</td>
	</tr>
	<tr>
    		<td bgcolor=$miscbackone>
		<font color=$fontcolormisc><b>����ԭ��</b><br>����������������Ƿ����ȡ�����<BR>�Ǳ�Ҫ����²�Ҫʹ������ܣ�
		</td>
    		<td bgcolor=$miscbackone><textarea name="emailmessage" cols="55" rows="6">
����Ա�����ã���������ԭ�������㱨��������������ӣ�



</textarea><input type=hidden name="originalpost" value="$temppost"></td>
	</tr>
	<tr>
    		<td colspan=2 bgcolor=$miscbackone align=center><input type=hidden name="emailtopictitle" value="$topictitle"><input type=submit value="���ͱ���" name="Submit"></form></table></td></tr></table>
    ~;


} # end routine.

if ($action eq "send") {


	&getmember("$inmembername");

	if ($userregistered eq "no") { &error("���ͱ���&�㻹ûע���أ�"); }
	elsif ($inpassword ne $password) { &error("���ͱ���&������������⣡"); }
	elsif ($inmembername eq "") { &login("$thisprog?action=reply&touser=$intouser"); }

	# Check for blanks

	if ($inmsgtitle eq "") { $blanks = "yes"; }
	if ($inmessage eq "")  { $blanks = "yes"; }
	if ($intouser eq "")   { $blanks = "yes"; }

	if ($blanks eq "yes") { &error("���ͱ���&��������д��������Ҫ��©��"); }

		    $memberfilename = $intouser;
		    $memberfilename =~ s/ /\_/g;
		    $memberfilename =~ tr/A-Z/a-z/;
		    $currenttime = time;

	            &getmember("$memberfilename");
        	    if ($userregistered eq "no") {&error("���ͱ���&������������⣬�����һ�����ͱ��棡");}


		    $filetoopen = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
		    open (FILE, "$filetoopen");
		    @inboxmessages = <FILE>;
		    close (FILE);

		    open (FILE, ">$filetoopen");
	    	    flock (FILE, 2) if ($OS_USED eq "Unix");
		    print FILE "$inmembername\tno\t$currenttime\t$inmsgtitle\t$inmessage2\t\n";
		    foreach $line (@inboxmessages) {
			chomp $line;
			print FILE "$line\n";
			}
		    close (FILE);

        if ($refreshurl == 1) {
	        $relocurl = "$threadprog?forum=$inforum&topic=$newthreadnumber";
	}
	else {
               	$relocurl = "$forumsprog?forum=$inforum";
        }

            $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>лл��$inmembername���Ѿ��ɹ������淢�͸�������</b></td>
            </tr>

            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ��������û���Զ����أ�������������ӣ�
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$intopic">��������</a>
            <li><a href="$forumsprog?forum=$inforum">������̳</a>
            <li><a href="$forumsummaryprog">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;


    } # end action




&output(
-Title   => $boardname,
-ToPrint => $output,
-Version => $versionnumber
);
