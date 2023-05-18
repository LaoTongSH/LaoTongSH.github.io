#!/usr/bin/perl
#############################################################
#  LeoBoard ver.5000 / LB5000 / 雷傲超级论坛 ver.5000
#
#  版权所有: 雷傲工作室(原蓝宝石软件工作室)
#
#  制作人  : 山鹰糊 (Shining Hu)
#            花无缺 (Ifairy Han)
#
#  主页地址: http://www.CGIer.com/      CGI 编程者之家
#	     http://www.LeoBoard.com/   雷傲论坛支持主页
#	     http://www.leoBBS.com/     本论坛直通车
#            http://mail@17do.com/      大家一起邮
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
&ipbanned; #封杀一些 ip

$action                 = $query -> param('action');
$inmembername           = $query -> param("membername");
$inpassword             = $query -> param("password");
$inmembername           = &cleaninput($inmembername);
$inpassword             = &cleaninput($inpassword);
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ($inmembername eq "") {
    $inmembername = "客人";
}
else {
&getmember("$inmembername");
&error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
&badwordfile;

    print header(-charset=>gb2312);

    $output .= qq~
      <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
        <tr><td>
          <table cellpadding=3 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center colspan=3><font color=$fontcolormisc><b>您最后访问本论坛后的新文章</b></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone align=center colspan=3><font color=$fontcolormisc>
            <br>注意：只有当您成功登陆后才能够检查<br><br>
            </td>
            </tr>
    ~;

if ($action eq "viewposts") {
    &getmember("$inmembername");
    if    ($userregistered eq "no")  { &messangererror("一般&您没有注册！"); }
    elsif ($inpassword ne $password) { &messangererror("一般&您的密码错误！"); }
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
        $output .= qq~<tr><td bgcolor=$forumcolortwo colspan=3><font color=$forumfontcolor><b>您最后一次访问本论坛后没有新文章</b>
        <br><br>注意：可能因为您还在访问某个论坛。如果您在访问论坛，则本程序是不会返回结果的。</font></td></tr>\n~;
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
             <td bgcolor=$forumcolortwo><font color=$forumfontcolor colspan=3>发言者：<a href=$profileprog?action=show&member=$lastposter target=_blank>$lastposter</a>　时间：$topiclastpost</td>
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
       -Title   => "$boardname - 新贴子",
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
	<font color=$fontcolormisc><b>请输入您的用户名、密码登陆</b></font></td></tr>
	<tr>
	  <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
	  <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"></td></tr>
	<tr>
	  <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
	  <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"></td></tr>
	<tr>
	  <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
    ~;
}

