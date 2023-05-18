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
use File::Copy;
$LBCGI::POST_MAX=1024*150;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "code.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "rebuildlist.pl";
$|++;                                     # Unbuffer the output
$thisprog = "jinghua.cgi";
$query = new LBCGI;
&ipbanned; #封杀一些 ip

$inshow         = $query -> param('show');
$inshow         = &stripMETA("$inshow");
for ('forum','topic','membername','password','action','checked','movetoid') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
    }
$inforum       = $forum;
$intopic       = $topic;
$inmembername  = $membername;
$inpassword    = $password;
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

print header(-charset=>gb2312);
if (($inforum)  && ($inforum  !~ /^[0-9]+$/)) { &error("普通错误&请不要修改生成的 URL！"); }
if (($intopic ) && ($intopic  !~ /^[0-9]+$/)) { &error("普通错误&请不要修改生成的 URL！"); }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
    if ($inmembername eq "") {
        $inmembername = "客人";
    }
    &getmember("$inmembername");
&badwordfile;

my %Mode = (
    'add'                 =>    \&add,
    'del'                 =>    \&del,
    );
if($Mode{$action}) {
        $Mode{$action}->();
        }
        elsif (($inforum ne "")&&($action eq "list")) { &list;   }
        else { &error("普通&请以正确的方式访问本程序"); }
    &output(
    -Title   => $boardname,
    -ToPrint => $output,
    -Version => $versionnumber
    );

sub add {
#    &getmember("$inmembername");

    &moderator;
    $cleartoedit = "no";

    &mischeader("标记精华贴子");
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq "smo") && ($inpassword eq $password)) { $cleartoedit = "yes"; }

    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no" && $checked eq "yes") { &error("标记精华贴子&您不是本论坛坛主或版主，或者您的密码错误！"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    my $file = "$lbdir" . "boarddata/jinghua$inforum.cgi";
      if (-e $file) {
        open (ENT, $file);
        @toptopic = <ENT>;
        close (ENT);
        if (open (ENT, ">$file")) {
        print ENT "$intopic\n" if (-e "${lbdir}forum$inforum/$intopic.thd.cgi");
	foreach $topic (@toptopic) {
	    chomp $topic;
	    if ($topic ne $intopic) {
	    	print ENT "$topic\n" if ((-e "${lbdir}forum$inforum/$topic.thd.cgi")&&($topic ne ""));
	    }

	}
        close (ENT);
        }
      }
      else {
        if (open (ENT, ">$file")) {
        print ENT "$intopic\n";
        close (ENT);
        }
      }
       if ($movetoid ne ""){
       $dirtoopen = "$lbdir" . "forum$movetoid";
                opendir (DIR, "$dirtoopen");
                @numberdata = readdir(DIR);
                closedir (DIR);
                if ($movetoid == $inforum) { &error("拷贝主题&不允许在同个论坛上拷贝主题！"); }
                @sorteddirdata = grep(/.thd.cgi$/,@numberdata);
                @sorteddirdata = sort numerically(@sorteddirdata);
                @sorteddirdata = reverse(@sorteddirdata);
                $highestno = $sorteddirdata[0];
                $highestno =~ s/.thd.cgi$//;
                $newthreadnumber = $highestno + 1;
                $currenttime = time;
       my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 2) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
        &winunlock($file) if ($OS_USED eq "Nt");
        ($topicid, $topictitle, $topicdescription1, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon) = split(/\t/,$in);


        my $file = "$lbdir" . "forum$movetoid/$newthreadnumber.pl";
        $inforumwrite = "$newthreadnumber\t$topictitle\t\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t$lastinposticon\t";
        &winlock($file) if ($OS_USED eq "Nt");
        if (open(FILE, ">$file")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$inforumwrite";
        close(FILE);
        }
        &winunlock($file) if ($OS_USED eq "Nt");
        ### Pick up old forum messages

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        @oldforummessages = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        $oldthreadposts = @oldforummessages - 1;

        ### Print to new forum message file

        $filetomake = "$lbdir" . "forum$movetoid/$newthreadnumber.thd.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $message (@oldforummessages) {
            chomp $message;
            print FILE "$message\n";
            }

        close(FILE);
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");

   	copy("${lbdir}forum$inforum/$intopic.mal.pl","${lbdir}forum$movetoid/$newthreadnumber.mal.pl") if (-e "${lbdir}forum$inforum/$intopic.mal.pl");
   	copy("${lbdir}forum$inforum/$intopic.poll.cgi","${lbdir}forum$movetoid/$newthreadnumber.poll.cgi") if (-e "${lbdir}forum$inforum/$intopic.poll.cgi");
   	copy("${lbdir}forum$inforum/rate$intopic.file.pl","${lbdir}forum$movetoid/rate$newthreadnumber.file.pl") if (-e "${lbdir}forum$inforum/rate$intopic.file.pl");
   	copy("${lbdir}forum$inforum/rateip$intopic.file.pl","${lbdir}forum$movetoid/rateip$newthreadnumber.file.pl") if (-e "${lbdir}forum$inforum/rateip$intopic.file.pl");

        $dirtoopen2 = "$imagesdir" . "usr/$inforum";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = grep(/^$inforum\_/,@dirdata2);
        @files1 = grep(/^$inforum\_$intopic\./,@files);
        $files1 = @files1;
	if ($files1 > 0) {
	    foreach (@files1) {
	    	(my $name,my $ext) = split(/\./,$_);
		copy("$dirtoopen2/$inforum\_$intopic\.$ext","$dirtoopen2/$movetoid\_$newthreadnumber\.$ext") if (-e "$dirtoopen2/$inforum\_$intopic\.$ext");
	    }
	}

        ####
        $filetoopen = "$lbdir" . "data/allforums.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);

        $filetomake = "$lbdir" . "data/allforums.cgi";
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
        next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
                if ($movetoid eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter1 ,$lastposttime1, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                     $threads++;
                    $posts = $posts + $threadposts;
                    $lastposter=$startedby if ($lastposter eq "");
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$currenttime\%\%\%$newthreadnumber\%\%\%$topictitle\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                    }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");


            require "$lbdir" . "data/boardstats.cgi";
            $filetomake = "$lbdir" . "data/boardstats.cgi";

            $totalthreads++;
            $totalposts = $totalposts + $threadposts;

	    &winlock($filetomake) if ($OS_USED eq "Nt");
            if (open(FILE, ">$filetomake")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
            print FILE "\$totalmembers = \'$totalmembers\'\;\n";
            print FILE "\$totalthreads = \'$totalthreads\'\;\n";
            print FILE "\$totalposts = \'$totalposts\'\;\n";
            print FILE "\n1\;";
            close (FILE);
            }
            &winunlock($filetomake) if ($OS_USED eq "Nt");

        $file = "$lbdir" . "boarddata/list$movetoid.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
	$listall = @listall;

    if ($listall >= 200) {
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        print LIST "$inforumwrite\n";
        foreach (@listall) {
          (my $useid,my $no)=split(/\t/,$_);
	  $_ =~ s/[\n\r]//isg;
	  print LIST "$_\n" if (($useid ne $intopic)&&($useid ne "")&&($useid =~ /^[0-9]+$/));
        }
        close (LIST);
        }
        &winunlock($file);
    }
    else {
        &winunlock($file);
        rebuildLIST(-Forum=>"$movetoid");
    }

       }


            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>标记精华贴子成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="jinghua.cgi?action=list&forum=$inforum">返回精华区</a>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;

    } # end if clear to edit
    else {

            $inmembername =~ s/\_/ /g;
           $filetoopen = "$lbdir" . "data/allforums.cgi";
	$filetoopen = &stripMETA($filetoopen);
	open(FILE, "$filetoopen");
	my @forums = <FILE>;
	close(FILE);
            $jumphtml .= "<option value=\"\">选择一个论坛\n</option>";
            $jumphtml .= "<option value=\"\">不做任何拷贝\n</option>";
            foreach $forum (@forums) { #start foreach @forums
                chomp $forum;
	        next if ($forum eq "");
                ($movetoforumid, $category, $categoryplace, $forumname, $forumdescription, $noneed ,$noneed ,$noneed ,$noneed, $startnewthreads ,$noneed ,$noneed, $noneed, $noneed, $noneed, $ratings, $noneed,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$movetoforumid\t$forumgraphic\t$startnewthreads\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
                push (@rearrangedforums, $rearrange);
            } # end foreach (@forums)
            @finalsortedforums = sort numerically(@rearrangedforums);
            foreach $sortedforums (@finalsortedforums) { #start foreach
            ($categoryplace, $category, $forumname, $forumdescription, $movetoforumid, $forumgraphic, $startnewthreads,$ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$sortedforums);

            if ($startnewthreads eq "no"){
                $jumphtml .= "<option value=\"$movetoforumid\">$forumname\n</option>";
                }
        } # end foreach

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="add">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [标记精华贴子]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>拷贝一份至精华区：</b></font></td>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><select name="movetoid">$jumphtml</select></font></td>
            </tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end
sub del {
#    &getmember("$inmembername");

    &moderator;
    $cleartoedit = "no";

    &mischeader("取消精华贴子");
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no" && $checked eq "yes") { &error("取消精华贴子&您不是本论坛坛主或版主，或者您的密码错误！"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
      my $file = "$lbdir" . "boarddata/jinghua$inforum.cgi";
      if (-e $file) {
        open (ENT, $file);
        @toptopic = <ENT>;
        close (ENT);

        if (open (ENT, ">$file")) {
	foreach $topic (@toptopic) {
	    chomp $topic;
	    if ($topic ne $intopic) {
	    	print ENT "$topic\n" if ((-e "${lbdir}forum$inforum/$topic.thd.cgi")&&($topic ne ""));
	    }
	}
        close (ENT);
        }
      }

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>取消精华贴子成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="jinghua.cgi?action=list&forum=$inforum">返回精华区</a>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;

    } # end if clear to edit
    else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="del">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [取消精华贴子]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end

sub list
{
&getforum("$inforum");

&mischeader("本版精华贴子");

    if ("$privateforum" eq "yes"){
        $tempaccess = "forumsallowed". "$inforum";
        $testentry = cookie($tempaccess);
        if ((($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($inmembmod eq "yes")) {
        }  else {&accessneeded; }
       }


my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") {
    	&whosonline("$inmembername\t$forumname\tnone\t查看论坛上的精华贴子\t");
    }
    else {
	&whosonline("$inmembername\t$forumname(密)\tnone\t查看保密论坛上的精华贴子\t");
    }
}

    if ($ratings ne "") { $ratings = qq~<td bgcolor=$tablebordercolor width=1 height=24></td><td bgcolor=$titlecolor width=27 align=center><b>评</b></td>~;}
$output.=qq~
<style>
.drb { border: $tablebordercolor solid; border-width: 0px 1px 1px 0px}
</style>
<span id=forum>
<table cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
              <tr><td height=1></td></tr>
              </table>
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
              <tr>
                <td bgcolor=$tablebordercolor width=1 height=24></td>
              <td bgcolor=$titlecolor width=32 align=center><font color=$titlefontcolor><b>状态</b></td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor width=* align=center><font color=$titlefontcolor><b>主　题</b> (点心情符为新闻方式浏览)</td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor align=center width=80><font color=$titlefontcolor><b>作 者</b></td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor align=center width=32><font color=$titlefontcolor><b>回复</b></td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor align=center width=32><font color=$titlefontcolor><b>点击</b></td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor width=195 align=center><b>　 最后更新 　 | 最后回复人</b></td>
		$ratings
                <td bgcolor=$tablebordercolor width=1></td>
              </tr>
	      </table>
              <table cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
              <tr><td height=1></td></tr>
              </table>
	~;

    $icon_num = int(rand(10));
    $topcount = 0;
    $filetoopen = "$lbdir" . "boarddata/jinghua$inforum.cgi";
    $filetoopen = &stripMETA($filetoopen);
    if (-e $filetoopen) {
    	&winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        @ontop = <FILE>;
        close(FILE);
        &winunlock($filetoopen);
    }
    else { undef @ontop; }
    $topcount = @ontop;
    $numberofpages = $topcount / $maxthreads;


    if ($topcount > $maxthreads) {
        $showmore = "yes";
        if ($inshow eq "" || $inshow < 0) { $inshow = 0; }
        if ($inshow > 0) { $startarray = $inshow; }
        else { $startarray = 0; }
        $endarray = $inshow + $maxthreads - 1;
        if ($endarray < ($topcount - 1)) { $more = "yes"; }
        elsif (($endarray > ($maxthreads - 1)) && ($more ne "yes")) { $endarray = $topcount -1; }
    }
    else {
        $showmore = "no";
        $startarray = 0;
        $topicpages = qq~<font color=$menufontcolor>本精华区只有一页</font>~;
        $endarray = $topcount -1;
    }

        if ($showmore eq "yes") {
	if ($maxthreads < $topcount) {
	    ($integer,$decimal) = split(/\./,$numberofpages);
	    if ($decimal > 0) { $numberofpages = $integer + 1; }
	    $mypages=$numberofpages;
	    #分页
	    $intshow=$inshow/(12*$maxthreads);
	    ($intshow,$mydecimal) = split(/\./,$intshow);
	    $intshow = $intshow + 1;
	    $preshow=($intshow-1)*12*$maxthreads-$maxthreads;
	    $nextshow=$intshow*12*$maxthreads;
	    $pages=qq~<a href="$thisprog?action=list&forum=$inforum&show=$preshow"><font color=$menufontcolor><b>←</b></font></a> ~ if ($intshow > 1);
	    if ($numberofpages > ($intshow*12)){
		$numberofpages=($intshow*12);
		$isnext=qq~<a href="$thisprog?action=list&forum=$inforum&show=$nextshow"><font color=$menufontcolor><b>→</b></font></a> ~;
	    }
	    $pagestart = ($intshow-1)*12*$maxthreads;
            $counter = ($intshow-1)*12;
            while ($numberofpages > $counter) {
		$counter++;
		if ($inshow ne $pagestart) { $pages .= qq~<a href="$thisprog?action=list&forum=$inforum&show=$pagestart"><font color=$menufontcolor><b>$counter</b></font></a> ~; }
		else { $pages .= qq~<font color=$fonthighlight><b>$counter</b></font> ~; }
		$pagestart = $pagestart + $maxthreads;
	    }
	    $pages .=  $isnext;
	    #分页end
	}
	$topicpages = qq~<font color=$menufontcolor><b>本精华区共有 <font color=$fonthighlight>$mypages</font> 页</b> [ $pages ]~;
    }
    if ($topcount > 0) {

    for ($i=$startarray;$i<=$endarray;$i++) {
      	$id=$ontop[$i];
      	chop $id;
      	my $file = "$lbdir" . "forum$inforum/$id.pl";

	open (TMP, "$file");
	(my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $lastpostdate, my $posticon1, my $inposttemp) = split (/\t/,<TMP>);
	close (TMP);
 	$topictitle =~ s/^＊＃！＆＊//;

	my $file1 = "$lbdir" . "forum$inforum/$id.thd.cgi";
	if (($topictitle eq "")||($startedby eq "")||($startedpostdate eq "")||($threadposts eq "")){
	open (TMP1, "$file1");
	my @tmp = <TMP1>;
	close (TMP);
	my $tmp = @tmp;
	$tmp --;
	my $tmp1 = $tmp[-1];
        $tmp1 =~ s/[\n\r]//isg;
	my $tmp2 = $tmp[0];
        $tmp2 =~ s/[\n\r]//isg;
	(my $membername, $topictitle, my $postipaddress, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/,$tmp2);
	(my $membername1, my $topictitle1, my $postipaddress1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, $posticon1) = split(/\t/,$tmp1);
 	$topictitle =~ s/^＊＃！＆＊//;
	$membername1 = "" if ($tmp eq 0);
	$threadviews =$tmp * 8 if (($threadviews eq "")||($threadviews > 10000));
	$postdate1 = $lastpostdate if ($lastpostdate ne "");
	$inposttemp = $post1;
	$inposttemp =~ s/\[这个贴子最后由(.+?)编辑\]\n//isg;
	$inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	$inposttemp =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]//isg;
	$inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2\n/isg;
	$inposttemp = &doemoticons("$inposttemp");
	$inposttemp =~ s/ \<img\s*(.*?)\s*\>//isg;
	$inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)//isg;
	$inposttemp =~ s/( )+$//isg;
	$inposttemp =~ s/^( )+//isg;
	$inposttemp =~ s/<(.|\n)+?>//g;
	$inposttemp =~ s/[\a\f\n\e\0\r\t\n]//g;

	    $posticon =~ s/\s//isg;
	    if ($posticon =~/<br>/i) {
      		$posticon=~s/<br>/\t/ig;
      		@temppoll = split(/\t/, $posticon);
      		$temppoll = @temppoll;
      		if ($temppoll >1) {
      		    $posticon1 = "<br>";
      		}
      		else {
      		    $posticon1 = "";
      		}
	    }
	    $inposttemp = &lbhz($inposttemp,$maxsavepost);
            $posticon = "<br>" if ($posticon =~/<br>/i);

	$rr = ("$id\t$topictitle\t$topicdescription\t$threadstate\t$tmp\t$threadviews\t$membername\t$postdate\t$membername1\t$postdate1\t$posticon1\t$inposttemp\t\n");
        }else{
   	    $threadviews = ($tmp+1) * 8 if ($threadviews eq "");
   	    $threadviews = 9999 if ($threadviews > 9999);
            $posticon1 = "<br>" if ($posticon1 =~/<br>/i);
	    $topictitle =~ s/^＊＃！＆＊//;
            $rr = ("$id\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon1\t$inposttemp\t\n");
        }
	if ($topictitle ne "") {push (@toptopic, $rr);}
    }
  }
  else { undef @toptopic; }


$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

$topiccount = 0;
        foreach $topic (@toptopic) {
	    chomp $topic;
            ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp) = split(/\t/,$topic);
       	    next if ($topicid eq "");
            if ($posticon ne "") {
            	$poll=0;
            	if ($posticon =~/<br>/i){
                    $posticon = int(rand(23));
    		    $posticon = "0$posticon" if ($posticon<10);
		    $posticon = qq~<img src=$imagesurl/posticons/$posticon.gif $defaultsmilewidth $defaultsmileheight border=0 alt="新闻方式浏览">~;
            	}
            	else{
            	    $posticon = qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight border=0 alt="新闻方式浏览">~;
            	}
            }
	    else {
    		$posticon = int(rand(23));
    		$posticon = "0$posticon" if ($posticon<10);
		$posticon = qq~<img src=$imagesurl/posticons/$posticon.gif $defaultsmilewidth $defaultsmileheight border=0 alt="新闻方式浏览">~;
	    }
	    if ($badwords) {
		@pairs = split(/\&/,$badwords);
		foreach (@pairs) {
		    ($bad, $good) = split(/=/,$_);
		    chomp $good;
		    $topictitle =~ s/$bad/$good/isg;
		}
	    }
    	    $topictitle =~ s/^＊＃！＆＊//;
	    $lastpostdatetemp=$lastpostdate;

	    $lastpostdate=$lastpostdatetemp;
            $topcount = $threadposts + 1;
            $topcount = $topcount / $maxtopics;
	    $counter = 0;
            if ($topcount > $maxtopics) {
		if ($maxtopics < $topcount) {
		    ($integer,$decimal) = split(/\./,$topcount);
		    if ($decimal > 0) { $topcount = $integer + 1; }
		    $pagestart = 0;
		    while ($topcount > $counter) {
			$counter++;
			$threadpages .= qq~<a href=$threadprog?forum=$inforum&topic=$topicid&start=$pagestart><font color=$fonthighlight><b>$counter</b></font></a> ~;
			$pagestart = $pagestart + $maxtopics;
		    }
		}
		$pagestoshow = qq~<font color=$forumfontcolor>　　[第 $threadpages 页]</font>~;
	    }





	    if ($lastpostdate ne "") {
		$lastpostdate = $lastpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
		$longdate = &dateformatshort("$lastpostdate");
		$lastpostdate = qq~<font color=$fontcolormisc>$longdate</font>~;
	    }
	    else {
		$lastpostdate = qq~<font color=$fontcolormisc>没有~;
		$lastpoststamp = "";
	    }
	    $startedpostdate = $startedpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
	    $startedlongdate = &shortdate("$startedpostdate");
	    $startedshorttime = &shorttime("$startedpostdate");
	    $startedpostdate = qq~<font color=$fontcolormisc>$startedlongdate</font>~;
	    $screenmode   = $query->cookie("screenmode");
	    $topictitlemax = 54;
	    $topictitlemax = 84 if (($screenmode >=9)||($tablewidth > 770));

	    $posttemp = "(无内容)" if ($posttemp eq "");
	    if (length($topictitle)>$topictitlemax) { $topictitletemp = substr($topictitle,0,$topictitlemax-4)." ..."; }
	    else { $topictitletemp = $topictitle; }
	    $topictitle = qq~<ACRONYM TITLE="最后回复摘要：\n\n$posttemp"><a href=$threadprog?forum=$inforum&topic=$topicid target=_blank>$topictitletemp</a></ACRONYM>~;
	    $startedbyfilename = $startedby;
	    $startedbyfilename =~ s/ /\_/isg;
	    $startedbyfilename =~ tr/A-Z/a-z/;

	    if ($lastposter) {
		$lastposterfilename = $lastposter;
		$lastposterfilename =~ s/ /\_/isg;
		$lastposter = qq~<a href=$profileprog?action=show&member=$lastposterfilename>$lastposter</a>~;
	    }
	    else {$lastposter = qq~<font color=$fontcolormisc>--------</a>~;}

	    $topicdescriptiontemp = $topicdescription;

	    $topicdescriptiontemp =~s/\s*(.*?)\s*\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/$3/isg;
	    $topicdescriptiontemp =~s/\<\/a\>//isg;

	    if (length($topicdescriptiontemp) > ($topictitlemax-4)) {
		$topicdescriptiontemp = substr($topicdescriptiontemp,0, $topictitlemax-8) . " ...";
		$topicdescription =~s/\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/\<a $1\>$topicdescriptiontemp\<\/a\>/isg;
	    }

	    if ($topicdescription) { $topicdescription = qq~<br>　　-=> $topicdescription~; }
	    if (-e "$lbdir/forum$inforum/rate$topicid.file.pl") {
		require "$lbdir/forum$inforum/rate$topicid.file.pl";
		$average = int($rates / $votes);
	        if ($average > 0) {$ratestar =  qq(<img src=$imagesurl/images/1star.gif width=14 alt="太差了">);}
	        if ($average > 1) {$ratestar =  qq(<img src=$imagesurl/images/2star.gif width=14 alt="有点差">);}
	        if ($average > 2) {$ratestar =  qq(<img src=$imagesurl/images/3star.gif width=14 alt="一般性">);}
	        if ($average > 3) {$ratestar =  qq(<img src=$imagesurl/images/4star.gif width=14 alt="挺不错">);}
	        if ($average > 4) {$ratestar =  qq(<img src=$imagesurl/images/5star.gif width=14 alt="特别好">);}
	    } else {
	        $ratestar =  qq(<img src=$imagesurl/images/norate.gif width=0 height=0 alt="没有投票评分记录">);
	    }

	    if ($ratings eq "") { $ratings2 = ""; }
	    else  { $ratings2 = qq~<td bgcolor=$forumcolortwo align=center width=27 class=drb><font color=$forumfontcolor>$ratestar</font></td>~; }

	    if ($counter == 0) { $pagestoshowtemp1 = 0; }
	    else { $pagestoshowtemp1 =7;}
	    $totlelength = $counter*3.3 + $pagestoshowtemp1 + length($topictitletemp) + 4; #标题栏的总长度
	    undef $pagestoshowtemp1;



      	   if (($membercode eq "ad") || ($inmembmod eq "yes")) {
		    $admini = qq~
		        <tr><td align=right><font color=$titlecolor>|<a href=jinghua.cgi?action=del&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>除</font></a>|<a href=jinghua.cgi?action=add&forum=$inforum&topic=$topicid><font color=$titlecolor>提</font></a>|<a href=$postingsprog?action=lock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>锁</font></a>|<a href=$postingsprog?action=unlock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|</font>&nbsp;</td></tr>
		    ~;
      	   }else{
      	   $admini="";
      	   }
            $topicicon = "<img src=$imagesurl/images/jh.gif width=15 border=0>";

	    $topictitle=$topictitle."<BR>" if ($totlelength > $topictitlemax+5);
	    $output .=qq~
		<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
		<tr>
                <td bgcolor=$tablebordercolor width=1 height=24></td>
                  <td bgcolor=$forumcolorone align=center width=32 class=drb><font color=$forumfontcolor><a href=topic.cgi?forum=$inforum&topic=$topicid target=_blank>$topicicon</a></td>
                  <td bgcolor=$forumcolortwo width=* class=drb><font color=$forumfontcolor><img src="" width=0 height=4><BR>
                  <table cellpadding=0 cellspacing=0 width=100%><tr><td>&nbsp;<a href=view.cgi?forum=$inforum&topic=$topicid target=_blank>$posticon</a>&nbsp;$topictitle$pagestoshow$topicdescription</font></td></tr>$admini</table>
                  <img src="" width=0 height=4><BR></td>
                  <td bgcolor=$forumcolorone align=center width=80 class=drb><font color=$forumfontcolor><a href=$profileprog?action=show&member=$startedbyfilename>$startedby</a></font></td>
                  <td bgcolor=$forumcolortwo align=center width=32 class=drb><font color=$forumfontcolor>$threadposts</font></td>
                  <td bgcolor=$forumcolortwo align=center width=32 class=drb><font color=$forumfontcolor>$threadviews</a></font></td>
                  <td bgcolor=$forumcolorone width=195 class=drb><font color=$fonthighlight>&nbsp;$lastpostdate | $lastposter<br></td>
		  $ratings2
                </tr>
                </table>

	    ~;
	    $pagestoshow = undef;
	    $threadpages = undef;
	    $topiccount++;
	}
        $output .= qq~
        </tr></table></td>
        </tr></table></span>
        <table cellpadding=0 cellspacing=2 border=0 width=$tablewidth align=center>
	<tr height=4></tr>
        <tr>
        <td>$topicpages</td>
                   </tr></table>
            </tr>
            </table>
	    <br>
        ~;


}

sub accessneeded {
    $output .= qq~
        <form action="forums.cgi" method=post>
        <input type=hidden name="forum" value="$inforum">
        <input type=hidden name="action" value="accessrequired">
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
        <tr><td>
	<table cellpadding=3 cellspacing=1 border=0 width=100%>
        <tr><td bgcolor=$miscbacktwo colspan=2 align=center><font color=$fontcolormisc><b>请输入您的名称、密码登陆私有论坛</b></font></td></tr>
        <tr><td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc><br>每个浏览器只需要登陆一次，同时请确认你已经打开了浏览器的 Cookies 选项！<br>只有经过管理员许可的用户才可以访问该论坛，如果你不能登陆，请联系管理员！<br><br></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
        <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername">　 <a href=$registerprog><font color=$fontcolormisc>您没有注册？</font></a></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
        <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword">　 <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码 ?</a></font></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入论坛访问密码</font></td>
        <td bgcolor=$miscbackone><input type=password name="forumpassword" value="$forumpassword">　 <font color=$fontcolormisc>如果你已经授权允许进入，则不必输入密码.</font></td></tr>
        <tr height=28><td bgcolor=$miscbackone colspan=2 align=center><font color=$fontcolormisc>如果你确认输入了正确的密码，但还是无法登陆的话，请刷新此页面(或者再次按登陆键一次)。</td></tr>
        <tr>
        <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登  陆"></td></tr></table></td></tr></table>
       </form>
    ~;

    &output(
     -Title   => "$forumname",
     -ToPrint => $output,
     -Version => $versionnumber
    );
}