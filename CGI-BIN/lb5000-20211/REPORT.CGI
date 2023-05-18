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
require "lbmail.lib.pl";
require "lb.lib.pl";
$|++;                        # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "report.cgi";

$query = new LBCGI;

&ipbanned; #封杀一些 ip

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
$inpost2 = "<BR><BR><b>贴子原始位置：</b> $boardurl/$threadprog?forum=$inforum&topic=$intopic<br>";

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
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie"); }
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

&title;


$output .= qq~
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
    <tr>
        <td width=30% rowspan=2><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td valign=middle align=left><font color=$fontcolormisc>
        　<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">　$boardname</a><br>
        　<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>　报告有问题的贴子
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
$topictitle =~ s/^＊＃！＆＊//;
# Get the post to edit

$filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
    flock(FILE, 2);
    @threads = <FILE>;
    close(FILE);

    $posttoget = --$inpostno;
($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, @threads[$posttoget]);
$topictitle =~ s/^＊＃！＆＊//;
    $post =~ s/\<p\>/\n\n/g;
    $post =~ s/\<br\>/\n/g;

    $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
    $postdate = &dateformat("$postdate");

 $rawpost = $post;

    $temppost = qq~原始贴子由 $membername 在 $postdate 发布，内容如下：\[br\]$rawpost~;


### print form
if ($forummoderator eq "") {
&error("发送报告&本版块没有设置版主！"); }
else {
$recipient = $forummoderator }

@recipientname = split(",",$recipient);

$toto = qq~<select name="touser">~;
foreach (@recipientname) {
    $toto .= qq~<option value="$_">$_</option>~;
}
$toto .= qq~</select>~;
&getforum("$inforum");

 &error("发送报告&你就是版主，搞什么飞机？") if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"));

    $topictitle = &cleanarea("$topictitle");

    $output .= qq~
    <form action="$boardurl/$thisprog" method=post>
    <input type=hidden name="action" value="send">
    <input type=hidden name="forum" value="$inforum">
    <input type=hidden name="topic" value="$intopic">
	<tr>
    		<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
			<font color=$fontcolormisc><b>向管理员报告有问题的贴子</b></font>
		</td>
	</tr>
  	<tr>
                <td bgcolor=$miscbackone valign=middle>
			<font color=$fontcolormisc><b>用户名</b></font>
		</td>
                <td bgcolor=$miscbackone valign=middle>
		<input type=text name="membername" value="$inmembername"> &nbsp; <font color=$fontcolormisc><a href="$registerprog">您没有注册？</a></font>
		</td>
	</tr>
	<tr>
                <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>密码</b></font>
		</td>
                <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font>
                <input type=hidden size=40 name="subject" value="报告有问题的贴子： $topictitle">
		</td>
	</tr>
	<tr>
                <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>报告发送给哪个版主</b></font>
		</td>
                <td bgcolor=$miscbackone valign=middle>$toto
		</td>
	</tr>
	<tr>
    		<td bgcolor=$miscbackone>
		<font color=$fontcolormisc><b>报告原因：</b><br>垃圾贴、广告贴、非法贴等。。。<BR>非必要情况下不要使用这项功能！
		</td>
    		<td bgcolor=$miscbackone><textarea name="emailmessage" cols="55" rows="6">
管理员，您好，由于如下原因，我向你报告这有问题的贴子：



</textarea><input type=hidden name="originalpost" value="$temppost"></td>
	</tr>
	<tr>
    		<td colspan=2 bgcolor=$miscbackone align=center><input type=hidden name="emailtopictitle" value="$topictitle"><input type=submit value="发送报告" name="Submit"></form></table></td></tr></table>
    ~;


} # end routine.

if ($action eq "send") {


	&getmember("$inmembername");

	if ($userregistered eq "no") { &error("发送报告&你还没注册呢！"); }
	elsif ($inpassword ne $password) { &error("发送报告&你的密码有问题！"); }
	elsif ($inmembername eq "") { &login("$thisprog?action=reply&touser=$intouser"); }

	# Check for blanks

	if ($inmsgtitle eq "") { $blanks = "yes"; }
	if ($inmessage eq "")  { $blanks = "yes"; }
	if ($intouser eq "")   { $blanks = "yes"; }

	if ($blanks eq "yes") { &error("发送报告&请完整填写表单，不要遗漏！"); }

		    $memberfilename = $intouser;
		    $memberfilename =~ s/ /\_/g;
		    $memberfilename =~ tr/A-Z/a-z/;
		    $currenttime = time;

	            &getmember("$memberfilename");
        	    if ($userregistered eq "no") {&error("发送报告&这个版主有问题，请更换一个发送报告！");}


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
                <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>谢谢，$inmembername！已经成功将报告发送给版主了</b></td>
            </tr>

            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            如果浏览器没有自动返回，请点击下面的链接！
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$intopic">返回主题</a>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
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

