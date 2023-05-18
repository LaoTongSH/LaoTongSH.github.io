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
#            http://maildo.com/      大家一起邮
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
require "rebuildlist.pl";
$|++;                                     # Unbuffer the output
$thisprog = "forumoptions.cgi";
$query = new LBCGI;
&ipbanned; #封杀一些 ip

$checked        = $query -> param('checked');
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$action         = $query -> param('action');
$prunedays      = $query -> param('prunedays');
$inmembername   = $query -> param('membername');
$inpassword     = $query -> param('password');
$inforum        = &stripMETA("$inforum");
$intopic        = &stripMETA("$intopic");
$action         = &stripMETA("$action");
$prunedays      = &stripMETA("$prunedays");
$inmembername   = &stripMETA("$inmembername");
$inpassword     = &stripMETA("$inpassword");
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));
print header(-charset=>gb2312);
if (($inforum  !~ m|([0-9\G]+$)|g) or (!$inforum))  { &error("普通错误&请不要修改生成的 URL！"); }
if (($prunedays) && ($prunedays !~ /^[0-9]+$/)) { &error("普通错误&请不要修改生成的 URL！"); }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

&getmember("$inmembername");
&error("普通错误&此用户根本不存在！") if ($userregistered eq "no");

&moderator;
if ($action eq "prune") {
    $cleartoedit = "no";
    &mischeader("批量删除");
	if ($inpassword eq $password) {
		$pwok = "密码不显示";
	}
	else {
		$pwok = $inpassword;
	}
	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$trueipaddress = "no" if (($trueipaddress eq "")||($trueipaddress eq "unknown"));
	my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$trueipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
	my $thistime=time;
	$filetomake = "$lbdir" . "data/baddel.cgi";

    $maxdeloneday = 9 if (($maxdeloneday eq "")||($maxdeloneday <= 0));
    if ($membercode ne "ad"){ 
      &winlock($filetomake); 
      open(FILE,"$filetomake"); 
      flock (FILE, 2) if ($OS_USED eq "Unix"); 
      my @delfile = <FILE>; 
      close(FILE); 
      my $delcount=0; 
      my $delcou=0; 
      my $totime=$thistime-24*60*60; 
      foreach (@delfile){ 
	chomp($_); 
	(my $delname, my $no, my $noip, $no, $no ,my $notime) = split(/\t/,$_); 
	if (lc($delname) eq lc($inmembername)){ 
	  if ($notime <$totime){ 
	    $delcount++; 
	  } 
	} 
	if ($noip eq "$ENV{'REMOTE_ADDR'}"){ 
	  if ($notime <$totime){ 
	    $delcou++; 
	  }
	}
      }
      if ($delcount > $maxdeloneday){&error("删除主题&你今天删除帖子太多，请明天继续！");} 
      if ($delcou > $maxdeloneday)  {&error("删除主题&你今天删除帖子太多，请明天继续！");} 
      undef $delcount; 
      undef $delcou; 
    }
    if (open(FILE, ">>$filetomake")) {
    print FILE "$inmembername\t$pwok\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t批量删除$forumname $prunedays天前的贴子\t$thistime\t\n";
    close(FILE);
    }
    undef $thistime;
    &winunlock($filetomake); 

    if ((($membercode eq "ad") ||($membercode eq 'smo'))&& ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
        if ($cleartoedit eq "no" && $checked eq "yes") {&error("使用批量删除&您不是本论坛坛主、管理员或是您的密码输入错误！");  }
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        if ($prunedays < 20) {  &error("使用批量删除&指定删除的天数要大于 20 ！"); }

	&getforum($inforum);

      my $file = "$lbdir" . "boarddata/jinghua$inforum.cgi";
      if (-e $file) {
        open (ENT, $file);
        @jinghuatopic = <ENT>;
        close (ENT);
      }
      else { undef @jinghuatopic ;}

	$dirtoopen = "$lbdir" . "forum$inforum";
	opendir (DIR, "$dirtoopen");
	my @dirdata = readdir(DIR);
	closedir (DIR);
	@entry = grep(/\.thd\.cgi$/,@dirdata);
	foreach (@entry) {
	  (my $topicid, my $tr) = split(/\./,$_);
	  $jinghuatopicnow = 0 ;
	  foreach $jinghuatopic (@jinghuatopic) {
	      chomp $jinghuatopic;
	      if ($topicid eq $jinghuatopic) { $jinghuatopicnow = 1; }
	  }
	 if ($jinghuatopicnow eq 0) {
	  $file1 = "$lbdir" . "forum$inforum/$topicid.thd.cgi";
	  open (TMP1, "$file1");
          flock(TMP1, 1) if ($OS_USED eq "Unix");
	  my @tmp = <TMP1>;
	  close (TMP1);
	  $postcount = @tmp;
          $postcount--;
	  my $tmp1 = $tmp[-1];
	  (my $no, my $no, my $no, my $no, my $no, my $lastpostdate, my $no, $no) = split(/\t/,$tmp1);

            $currenttime = time;
            $threadagelimit = $currenttime - $prunedays * 86400;
            if ($lastpostdate < $threadagelimit) {
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.thd.cgi";
                unlink $filetotrash;
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.mal.pl";
                unlink $filetotrash;
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.poll.pl";
                unlink $filetotrash;
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.pl";
                unlink $filetotrash;
        	$filetounlink = "$lbdir" . "forum$inforum/rate$intopic.file.pl";
	        unlink $filetounlink;
        	$filetounlink = "$lbdir" . "forum$inforum/rateip$intopic.file.pl";
	        unlink $filetounlink;
		$dirtoopen2 = "$imagesdir" . "usr/$inforum";
        	opendir (DIR, "$dirtoopen2");
	        @dirdata2 = readdir(DIR);
        	closedir (DIR);
	        @dirdata2 = grep(/^$inforum\_$intopic/,@dirdata2);
	        @files = grep(/^$inforum\_$intopic\./,@dirdata2);
        	foreach $file (@files) {
	            $filetoremove = "$dirtoopen2/$file";
        	    unlink $filetoremove;
            	}
	        @files = grep(/^$inforum\_$intopic\_/,@dirdata2);
        	foreach $file (@files) {
	            $filetoremove = "$dirtoopen2/$file";
        	    unlink $filetoremove;
            	}
                $totaltopics_deleted++;
                $totalposts_deleted = $totalposts_deleted + $postcount;
	   }
	  }
	}

        rebuildLIST(-Forum=>"$inforum");

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen");
        @allforums = <FILE>;
        close(FILE);

        $filetomake = "$lbdir" . "data/allforums.cgi";
        $filetomake = &stripMETA($filetomake);
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) {
            chomp($forum);
            ($tempno, $trash) = split(/\t/,$forum);
            if ($inforum eq $tempno) {
               ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                $posts = $posts - $totalposts_deleted;
                $threads = $threads - $totaltopics_deleted;
                print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
            }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        require "$lbdir" . "data/boardstats.cgi";
        $filetomake   = "$lbdir" . "data/boardstats.cgi";
        $totalthreads = $totalthreads - $totaltopics_deleted;
        $totalposts   = $totalposts - $totalposts_deleted;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        if (! $totaltopics_deleted) { $totaltopics_deleted = "0"; }
        if (! $totalposts_deleted)  { $totalposts_deleted  = "0"; }
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>论坛文章已经被删除</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
            统计资料：
            <ul>
            <li>共删除主题：$totaltopics_deleted 篇
            <li>共删除回复：$totalposts_deleted 篇
            <li><a href="$forumsprog?forum=$inforum">返回论坛$savetopicid</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
	    ~;
	}
	else {
            &mischeader("批量删除");

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="prune">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <font face="$font" color=$fontcolormisc><b>请输入您的详细资料以便进入删除模式[批量删除]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc><b>一旦您删除了文章，将不能够恢复！</b><br>下面将删除发表时间超过一定天数外的所有文章。如果您确定这样做，请仔细检查您输入的信息。</font></td>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>删除多少天以外的文章<br>例如：输入'30'，将删除超过 30 天的所有文章。</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="prunedays"0></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="提 交"></td></tr></form></table></td></tr></table>
            </table></td></tr></table>
	    ~;
	}
}
else { &error("普通&未指定功能名！"); }
&output(
    -Title   => "$boardname - 批量删除",
    -ToPrint => $output,
    -Version => $versionnumber
);
