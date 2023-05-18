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
&error("普通错误&老大，别乱黑我的程序呀！") if (($editmembername =~ m/\//)||($editmembername =~ m/\\/)||($editmembername =~ m/\.\./));
$editmembername =~ s/\///g;
$editmembername =~ s/\.\.//g;
$editmembername =~ s/\\//g;

$action         = $query -> param ("action");
$inforum        = $query -> param ("oldforum");
$intopic        = $query -> param ("oldtopic");
if (($inforum)  && ($inforum !~ /^[0-9]+$/))  { &error("普通&老大，别乱黑我的程序呀！"); }
if (($intopic)  && ($intopic !~ /^[0-9]+$/))  { &error("普通&老大，别乱黑我的程序呀！"); }

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

$inmembername   = cookie("amembernamecookie");
$inpassword     = cookie("apasswordcookie");
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
	        　<img src=$imagesurl/images/closedfold.gif width=15 height=11><a href=$forumsummaryprog>　$boardname</a><br>
                　<img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>　给用户投票
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
        <b>请首先登陆然后对 $editmembername 投票(仅对坛主和版主开放)</b></font></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc >清输入你的姓名</font></td>
        <td bgcolor=$miscbackone><input type=text name="inmembername" value="$inmembername" size=20></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc >清输入你的密码</font></td>
        <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword" size=20></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc >被投票用户名称</font></td>
        <td bgcolor=$miscbackone><input type=text name="membername" value="$editmembername" size=20></td></tr>
        <tr>
        <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登陆投票"></td></form></tr></table></td></tr></table>
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

	if ("$userregistered" eq "no")    { &error("用户投票&没有该注册用户");   }
	if ("$inpassword" ne "$password") { &error("用户投票&错误的管理员密码"); }
	if ($membercode eq "ad")          { $verify = "yes"; }
	if ($membercode eq 'smo')	  { $verify  = "yes"; }
	if ($membercode eq "mo")          { $verify = "yes"; }

	if ($verify ne "yes") { &error("用户投票&仅仅管理员才能投票"); }
	else {
	    &getmember("$editmembername");
	    if ("$userregistered" eq "no")    { &error("用户投票&没有该注册用户");   }
            if ($membercode eq "ad" || $membercode eq 'smo' || $membercode eq "mo") { &error("给用户投票&坛主和版主不能被投票"); }

	    if ($rating eq "") {
		$rating = 0;
	    }
	    $rating=$rating+0;
	    if ($rating < -6) { $rating = -6; }
	    if ($rating > $maxweiwang) { $rating = $maxweiwang; }

	    if ($rating == $maxweiwang) { $pwout = qq~<input type=radio name=pw value=warn CHECKED>警告用户~; }
	    elsif ($rating == -5) { $pwout = qq~<input type=radio name=pw value=praise CHECKED>赞扬用户　　<input type=radio name=pw value=warn>禁止用户</td>~; }
	    elsif ($rating == -6) { $pwout = qq~<input type=radio name=pw value=praise CHECKED>恢复用户~; }
	    else { $pwout = qq~<input type=radio name=pw value=praise CHECKED>赞扬用户　　<input type=radio name=pw value=warn>警告用户　　<input type=radio name=pw value=reset>清零　　<input type=radio name=pw value=worst>禁止发言</td>~; }

	    $output .= qq~
		<tr>
		<td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>$editmembername 的威望是: $rating</b></font></td>
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
		你的选择是: $pwout
		</tr>
		<tr>
		<td bgcolor=$miscbackone align=center><font color=$fontcolormisc>投票原因:<br><textarea size=20 name="reason" cols="40" rows="5"></textarea></td>
		</tr>
		<tr>
		<td bgcolor=$miscbackone align=center>
		通知用户: <input type=radio name=notify value=yes >是　　<input type=radio name=notify value=no CHECKED>否</td>
		<tr>
		<td bgcolor=$miscbacktwo align=center>
		<input type=submit value=确认 name=submit>
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

	if ("$userregistered" eq "no")    { &error("用户投票&没有该注册用户");   }
	if ("$inpassword" ne "$password") { &error("用户投票&错误的管理员密码"); }
	if ($membercode eq "ad")          { $verify = "yes"; }
	if ($membercode eq 'smo')	  { $verify  = "yes"; }
	if ($membercode eq "mo")          { $verify = "yes"; }

	if ($verify ne "yes") { &error("用户投票&仅仅管理员才能投票"); }

    	if (($notify eq "yes") && ($reason eq "")) {   &error("用户投票&假如你想通知用户，请给出个理由.");  }

        &getmember("$member");
        if ($membercode eq "ad" || $membercode eq 'smo' || $membercode eq "mo") { &error("给用户投票&坛主和版主不能被投票"); }

        if ($pw eq "praise") {
            $pwmail    = "赞扬";
            $pwmailing = "赞扬";
            $rating++;
        }
        elsif ($pw eq "warn") {
            $pwmail    = "警告";
            $pwmailing = "警告";
            $rating--;
        }
        elsif ($pw eq "reset") {
        	$pwmail = "恢复威望为０";
        	$pwmailing = "恢复";
        	$rating = 0;
        }
        else {
        	$pwmail = "减低威望到最低";
        	$pwmailing = "减低";
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

        if ($newmembercode eq "banned") { $membertitleout = "被禁止"; }
        else { $membertitleout = "普通会员"; }

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
	$subject = "$member 已经被 $sender $pwmail !";
	$message .= "\n";
	$message .= "$homename\n";
	$message .= "$boardurl/$forumsummaryprog\n";
	$message .= "$boardurl/$threadprog?forum=$inforum&topic=$intopic\n\n\n";
	$message .= "$member 已经被 $sender $pwmail !\n";
	$message .= "$member 的威望现在是: $rating\n";
	$message .= "$member 的状态现在是: $membertitleout\n\n\n";
	$message .= "被 $pwmailing $member 的原因是:\n";
	$message .= "$reason\n\n";
	$message .= "假如你认为不正确, 请跟 $sender 说说\n";
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
	<td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>$member 已经成功被$pwmail</b></font></td>
	</tr>
	<tr>
	<td bgcolor=$miscbackone>
	<font color=$fontcolormisc>具体情况:
	<br><ul>
	    <li><a href="$threadprog?forum=$inforum&topic=$intopic">返回当前主题 </a>$pages
            <li><a href="$forumsprog?forum=$inforum">返回当前论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
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
        $subject = "你已经被 $sender $pwmail !";
        $message .= "\n";
        $message .= "$homename\n";
        $message .= "$boardurl/$forumsummaryprog\n";
	$message .= "$boardurl/$threadprog?forum=$inforum&topic=$intopic\n\n\n";
        $message .= "你已经被 $sender $pwmail !\n\n\n";
        $message .= "你现在的威望是: $rating\n";
        $message .= "你现在的状态是: $membertitleout\n";
        $message .= "你被 $pwmailing 的原因是:\n";
        $message .= "$reason\n\n";
        $message .= "假如你认为有错, 请发信给\n";
        $message .= "坛主: $adminemail_in 解释原因！\n";
        &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
   }

print header(-charset=>gb2312);
&output(
       -Title   => "$boardname - 用户投票",
       -ToPrint => $output,
       -Version => $versionnumber
);

