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
require "visitforum.lib.pl";
$|++;                                     # Unbuffer the output
$thisprog = "newposts.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$action                 = $query -> param('action');
$inmembername           = $query -> param("membername");
$inpassword             = $query -> param("password");
$inmembername           = &cleaninput($inmembername);
$inpassword             = &cleaninput($inpassword);
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
&badwordfile;

    print header(-charset=>gb2312);

    $output .= qq~
      <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
        <tr><td>
          <table cellpadding=3 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center colspan=3><font color=$fontcolormisc><b>�������ʱ���̳���������</b></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone align=center colspan=3><font color=$fontcolormisc>
            <br>ע�⣺ֻ�е����ɹ���½����ܹ����<br><br>
            </td>
            </tr>
    ~;

if ($action eq "viewposts") {
    &getmember("$inmembername");
    if    ($userregistered eq "no")  { &messangererror("һ��&��û��ע�ᣡ"); }
    elsif ($inpassword ne $password) { &messangererror("һ��&�����������"); }
    elsif ($inmembername eq "")      { &login("$thisprog?action=viewposts"); }

    $filetoopen = "$lbdir" . "data/allforums.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
    foreach $forum (@forums) { #start foreach @forums
        chomp $forum;
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);

        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$forumid};
        if ($forumlastvisit eq "0" || $forumlastvisit eq "") { next; }
        if ($forumlastvisit > $lastposttime) { next; }
        if (($privateforum eq "yes") && (($allowedentry{$forumid} ne "yes")&&($membercode ne "ad")&&($membercode ne 'smo'))) { next; }

        $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$forumid\t$forumlastvisit\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
        push (@rearrangedforums, $rearrange);

    }
    @finalsortedforums = sort numerically(@rearrangedforums);

    foreach (@finalsortedforums) {
	($categoryplace, $category, $forumname, $forumdescription,$forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $forumid, $forumlastvisit, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$_);

        $filetoopen = "$lbdir" . "boarddata/list$forumid.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen");
        @topics = <FILE>;
        close(FILE);

	foreach $topic (@topics) {
            chomp $topic;
            ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\t/,$topic);
            if ($forumlastvisit < $lastpostdate) {
        	$lastposter = $startedby if ($lastposter eq "");
                $found = ("$categoryplace\t$category\t$forumid\t$topicid\t$forumname\t$topictitle\t$lastposter\t$lastpostdate\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
                push (@founditems, $found);
            }
        }
    }

    $totals = @founditems;

    if ($totals eq 0) {
        $output .= qq~<tr><td bgcolor=$forumcolortwo colspan=3><font color=$forumfontcolor><b>�����һ�η��ʱ���̳��û��������</b>
        <br><br>ע�⣺������Ϊ�����ڷ���ĳ����̳��������ڷ�����̳���򱾳����ǲ��᷵�ؽ���ġ�</font></td></tr>\n~;
    }

    foreach (@founditems) {
       ($categoryplace, $categoryname, $forumid, $topicid, $forumname, $topictitle, $lastposter, $lastpostdate, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split (/\t/,$_);
        if ($categoryplace ne $lastcategoryplace) {
            $output .= qq~<tr><td bgcolor=$catback colspan=4><font color=$catfontcolor><b>$categoryname</b></font></td></tr>\n~;
        }
        if ($forumid ne $lastforumid) {
            $output .= qq~<tr><td bgcolor=$forumcolortwo colspan=4><font color=$forumfontcolor><b>-=> $forumname</b></font></td></tr>\n~;
        }
        $lastpostdate = $lastpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
        $longdate = &longdate("$lastpostdate");
        $shorttime = &shorttime("$lastpostdate");
        $topiclastpost = qq~<font color="$lastpostfontcolor">$longdate <font color="$lastpostfontcolor">$shorttime</font>~;

        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $topictitle=~ s/$bad/$good/isg;
            }
        }

        $output .= qq~
            <tr>
             <td bgcolor=$forumcolortwo><font color=$forumfontcolor><a href=$threadprog?forum=$forumid&topic=$topicid>$topictitle</a></td>
             <td bgcolor=$forumcolortwo><font color=$forumfontcolor colspan=3>�����ߣ�<a href=$profileprog?action=show&member=$lastposter target=_blank>$lastposter</a>��ʱ�䣺$topiclastpost</td>
            </tr>
        ~;

        $lastcategoryplace = $categoryplace;
        $lastforumid = $forumid;
    }
}
else {
    &login("$thisprog?action=viewposts");
}
    $output .= "</table></td></tr></table>\n";
    &printmessanger(
       -Title   => "$boardname - ������",
       -ToPrint => $output,
       -Version => $versionnumber
    );
sub login {
    local($url) = @_;
    ($postto, $therest) = split(/\?/,$url);
    @pairs = split(/\&/,$therest);

    foreach (@pairs) {
       ($name, $value)=split(/\=/,$_);
        $hiddenvars .= qq~<input type=hidden name="$name" value="$value">\n~;
    }

    $output .= qq~
        <tr>
        <td bgcolor=$miscbacktwo colspan=2 align=center>
        <form action="$postto" method="post">$hiddenvars
	<font color=$fontcolormisc><b>�����������û����������½</b></font></td></tr>
	<tr>
	  <td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td>
	  <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"></td></tr>
	<tr>
	  <td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td>
	  <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"></td></tr>
	<tr>
	  <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ½"></td></form></tr></table></td></tr></table>
    ~;
}
