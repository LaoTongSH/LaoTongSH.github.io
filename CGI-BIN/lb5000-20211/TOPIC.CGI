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
use Benchmark;
$TT0  = new Benchmark;
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
require "data/cityinfo.cgi";
require "data/membertitles.cgi";
require "data/mpic.cgi";
require "data/styles.cgi";
require "lb.lib.pl";
require "visitforum.lib.pl";
require "testinfo.pl";
$|++;

#################--- Begin the program ---###################
$thisprog = "topic.cgi";
srand;

$query = new LBCGI;

$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;

$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$instart        = $query -> param('start');
$jumpto         = $query -> param('jumpto');
$inshow         = $query -> param('show');

&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

if ((($forumimagead eq "1")&&($useimageadtopic eq "1"))||(($forumimagead1 eq "1")&&($useimageadtopic1 eq "1"))) {
	require "${lbdir}imagead.cgi";
}

$inmembername   = $query->cookie("amembernamecookie");
$inpassword     = $query->cookie("apasswordcookie");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

$nodisp = $query->cookie("nodisp");
($nodispavatar, $nodispsign, $nodispphoto)  = split(/\|/,$nodisp);

$treeview   = $query->cookie("treeview");
$changemode = $query -> param('changemode');
$replynum   = $query -> param('replynum');
if ($changemode ne "") { $treeview=($treeview eq "yes")?"no":"yes"; }

$screenmode = $query->cookie("screenmode");
$screenmode = 7 if ($screenmode eq "");

#&ipbanned; #封杀一些 ip
$paraspace = "line-height: $paraspace%" if ($paraspace ne "130");
$wordspace = "letter-spacing: $wordspace" if ($wordspace ne "0");

&getforum($inforum);
if ($jumpto) { print redirect(-location=>"$jumpto"); exit; }
    
    if (!$inmembername) {
	$inmembername = "客人";
        &moderator;
    }
    else {
        &getmember("$inmembername");
        &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
        $membercodetemp = $membercode;
        $tempaccess = "forumsallowed". "$inforum";
        $testentry = $query->cookie("$tempaccess");
        &moderator;
        if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($inmembmod eq "yes")||($membercode eq 'smo')) { $allowed = "yes"; }
            else { $allowed  = "no"; }
        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$inforum};
        $currenttime = time;
        &setlastvisit("$inforum,$currenttime");
        $inmembercode = $membercode;
    }
$cpudisp = 1 if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"));
if (($privateforum eq "yes" && $allowed ne "yes")) { &error("进入私有论坛&对不起，您没有权限进入该私有论坛！"); }
&badwordfile;
&forumjump;
$treeviewcookie  = cookie(-name    =>   "treeview",
                          -value   =>   "$treeview",
                          -expires =>   "+30d",
                          -path    =>   "$cookiepath/");

print header(-cookie=>[$treeviewcookie, $tempvisitcookie, $permvisitcookie], -charset=>gb2312);

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");

    if ($forumgraphic) { $forumgraphic = qq~<a href=$forumsprog?forum=$inforum><img src=$imagesurl/images/$forumgraphic border=0></a>~; }
        else { $forumgraphic = qq~<a href=$forumsummaryprog><img src=$imagesurl/images/$boardlogo border=0></a>~; }

      $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
      &winlock($filetoopen) if ($OS_USED eq "Nt");
      if (open(FILE, "$filetoopen")) {
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @threads = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
      }
      else { &winunlock($filetoopen) if ($OS_USED eq "Nt"); &error("打开主题&这个主题不存在！可能已经被删除！"); }

    my $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
    my $filetoopens = &lockfilename($filetoopen);
    if (!(-e "$filetoopens.lck")) {#0
      &winlock($filetoopen);
      open(FILE, "$filetoopen");
      flock(FILE, 1) if ($OS_USED eq "Unix");
      @allthreads = <FILE>;
      close(FILE);
      &winunlock($filetoopen);

      $totalthreadcount = @allthreads;
      if ($totalthreadcount > 1) {
        my $count = 0;
	@allthreadtemp = "";
	$keepcounter = "";

        foreach $line (@allthreads) { #1
          ($tempno, $trash) = split(/\t/, $line);
          chomp $line;
          push (@numbercounter, $tempno);
          if (($intopic eq $tempno)&&($keepcounter eq "")) { #2
            ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp) = split(/\t/,$line);
            $threadviews++; $keepcounter = $count;

            if (($topictitle eq "")||($startedby eq "")||($startedpostdate eq "")||($threadposts eq "")) { #3
	      my @tmp = @threads; my $tmp = @tmp; $tmp --;
	      my $tmp1 = $tmp[-1]; my $tmp2 = $tmp[0];
	      ($membername0, $topictitle, my $no, $no, $no, $postdate, $no, $posticon) = split(/\t/,$tmp2);
  	      ($membername1, my $no, $no, $no, $no, $postdate1,$no, $posticon1) = split(/\t/,$tmp1);
	      chomp $posticon;
	      $posticon =~ s/\s//isg;
	      if ($posticon =~/<br>/i) { #4
      		$posticon=~s/<br>/\t/ig;
      		@temppoll = split(/\t/, $posticon);
      		$temppoll = @temppoll;
      		if ($temppoll >1) { $posticon = "<br>"; } else { $posticon = ""; }
	      } #4
	      $startedby       = $membername0 if ($startedby eq "");
	      $startedpostdate = $postdate;
	      $threadposts     = $tmp;
	      if ($tmp eq 0) { $lastpostdate = $postdate; $lastposter   = ""; } else { $lastpostdate = $postdate1; $lastposter   = $membername1; }
            } #3

            $threadstate = "poll" if (($posticon =~ m/<br>/i)&&($threadstate ne "poll")&&($threadstate ne "pollclosed"));
            if ($threadstate eq "") {$threadstate="open";}
            $threadviews = ($threadposts+1)*6 if ($threadviews < $threadposts);
   	    $threadviews = 9999 if ($threadviews > 9999);
            $posticon = "<br>" if ($posticon =~/<br>/i);
	    $topictitle =~ s/^＊＃！＆＊//;
            $linetokeep = "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t";
            push (@allthreadtemp, $linetokeep);
          } #2
          else { push (@allthreadtemp, $line); }
        $count++;
        } #1
	undef $count;
        if (!(-e "$filetoopens.lck")) {
          &winlock($filetoopen);
          if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            foreach (@allthreadtemp) {
	      chomp $_;
              print FILE "$_\n" if ($_ ne "");
            }
            close(FILE);
          }
          &winunlock($filetoopen);
          if (int(rand(5)) eq 2) {
            if (open(MSG, ">${lbdir}forum$inforum/$intopic.pl")) {
              print MSG $linetokeep;
              close(MSG);
            }
          }
        }
        undef @allthreadtemp;
        undef $linetokeep;
      }
    }#0

    $totalthreadcount--;

    if ($intopic eq $numbercounter[0]) { undef $nextlink; }
        else {
            $nexttopic = $keepcounter - 1;
            $threadnext = $numbercounter[$nexttopic];
            $nextlink = qq~　<a href=$threadprog?forum=$inforum&topic=$threadnext><img src=$imagesurl/images/nextthread.gif border=0 alt=浏览下一篇主题 width=52 height=12></a>~;
            }

    if ($intopic eq $numbercounter[$totalthreadcount]) { undef $backlink; }
        else {
            $backtopic = $keepcounter + 1;
            $threadback = $numbercounter[$backtopic];
            $backlink = qq~<a href=$threadprog?forum=$inforum&topic=$threadback><img src=$imagesurl/images/prethread.gif border=0 alt=浏览上一篇主题 width=52 height=12></a>~;
            }

    $nexttopiclinks = "";
    $nexttopiclinks .= "$backlink" if $backlink;
    if ($treeview eq "yes") { $viewstyle="&nbsp;<a href=$threadprog?forum=$inforum&topic=$intopic&changemode=1><img src=$imagesurl/images/flatview.gif width=40 height=12 border=0 alt=平板显示贴子></a>"; }
    else { $viewstyle="&nbsp;<a href=$threadprog?forum=$inforum&topic=$intopic&changemode=1><img src=$imagesurl/images/treeview.gif width=40 height=12 border=0 alt=树形显示贴子></a>"; }
    
    $nexttopiclinks .= qq~&nbsp;　<a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 alt=刷新本主题 width=40 height=12></a> $viewstyle~;
    $nexttopiclinks .= "$nextlink" if $nextlink;
    undef @numbercounter;
    &postings;
    &title;

    $maxthreads = $maxtopics;

if ($sticky eq "on") {
    @threads = reverse(@threads);
    $threadslast=pop(@threads);
    unshift(@threads,$threadslast);
    $threadscount=@threads;
}

    ($trash, $topictitle) = split(/\t/,$threads[0]);
    $topictitle =~ s/^＊＃！＆＊//;

    $numberofitems = @threads;
    $numberofpages = $numberofitems / $maxthreads;

    if ($numberofitems > $maxthreads) {
        $showmore = "yes";
        if ((!$instart) or ($instart < 0)) { $instart = 0; }
        if ($instart > 0) { $startarray = $instart; } else { $startarray = 0; }
        $endarray = $instart + $maxthreads - 1;
        if ($endarray < ($numberofitems - 1)) { $more = "yes"; }
        if (($endarray > ($maxthreads - 1)) and ($more ne "yes")) { $endarray = $numberofitems - 1; }
        }
        else {
             $showmore = "no";
             $startarray = 0;
             $pages = qq~<font color=$menufontcolor>该主题只有一页</font>~;
             $endarray = $numberofitems - 1;
             }

     if ($showmore eq "yes") {
     if ($maxthreads < $numberofitems) {
        ($integer,$decimal) = split(/\./,$numberofpages);
        if ($decimal > 0) { $numberofpages = $integer + 1; }
     #############
     $mypages=$numberofpages;
	    #分页
	    $intshow=$instart/(12*$maxthreads);
	    ($intshow,$mydecimal) = split(/\./,$intshow);
	    $intshow = $intshow + 1;
	    $preshow=($intshow-1)*12*$maxthreads-$maxthreads;
	    $nextshow=$intshow*12*$maxthreads;
	    $pages=qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$preshow&show=$inshow class=hb>←</a> ~ if ($intshow > 1);
	    if ($numberofpages > ($intshow*12)){
		$numberofpages=($intshow*12);
		$isnext=qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$nextshow&show=$inshow class=hb>→</a> ~;
	    }
	    $pagestart = ($intshow-1)*12*$maxthreads;
            $counter = ($intshow-1)*12;
            while ($numberofpages > $counter) {
		$counter++;
		if ($instart ne $pagestart) { $pages .= qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$pagestart&show=$inshow class=hb>$counter</a> ~; }
		else { $pages .= qq~<font color=$fonthighlight><b>$counter</b></font> ~; }
		$pagestart = $pagestart + $maxthreads;
	    }
	    $pages .=  $isnext;
	    #分页end
	}
	$pages = qq~<font color=$menufontcolor><b>本主题共有 <font color=$fonthighlight>$mypages</font> 页</b> [ $pages ]~;
        }

        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $topictitle =~ s/$bad/$good/isg;
                }
            }

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t$forumname\tnone\t浏览<a href=\"$threadprog?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t") if ($privateforum ne "yes");
    &whosonline("$inmembername\t$forumname(密)\tnone\t浏览保密贴子\t") if ($privateforum eq "yes");
}

    $printpageicon = qq~<a href=$printpageprog?forum=$inforum&topic=$intopic><img src=$imagesurl/images/printpage.gif border=0 width=16 height=16 alt=显示可打印的版本></a>&nbsp;~;
    $savefile = qq~<a href=# onclick="javascript:WebBrowser.ExecWB(4,1)"><img src=$imagesurl/images/saveas.gif border=0 width=16 height=16 alt="保存该页为文件" align=absmiddle></a>&nbsp;<object id="WebBrowser" width=0 height=0 classid="CLSID:8856F961-340A-11D0-A96B-00C04FD705A2"></object>~;
    $reporticon = qq~<a href=report.cgi?forum=$inforum&topic=$intopic><img src=$imagesurl/images/report.gif border=0 width=16 height=15 alt=本贴有问题，发送短消息报告给版主></a>&nbsp;~;
    $favicon = qq~<a href=fav.cgi?action=add&forum=$inforum&topic=$intopic><img src=$imagesurl/images/fav.gif border=0 width=13 height=15 alt=加入个人收藏&关注本贴></a>&nbsp;~;
    $pagpageicon = qq~<a href="javascript:openScript('pag.cgi?forum=$inforum&topic=$intopic',500,400)"><img src=$imagesurl/images/pag.gif border=0 width=16 height=16 alt=把本贴打包邮递></a>&nbsp;~;
    $topictitletemp = $topictitle;
    $topictitletemp =~s/\'/\`/isg;
    $bookmarkpage  = qq~<a href=#><span style="CURSOR: hand" onClick="window.external.AddFavorite('$boardurl/topic.cgi?forum=$inforum&topic=$intopic', ' $boardname - $topictitletemp')"><IMG SRC=$imagesurl/images/fav_add1.gif BORDER=0 width=15 height=15 alt=把本贴加入IE收藏夹></span></a>&nbsp;~;
    if ($privateforum ne "yes") { $sendtofriendicon = qq~<a href=$lbfriendprog?forum=$inforum&topic=$intopic><img src=$imagesurl/images/emailtofriend.gif border=0 width=16 height=16 alt=发送本页面给朋友></a>&nbsp;~;}

$topictitletemp =$topictitle;
$topictitletemp =~s/ \(无内容\)$//;
$topictitletemp1 = &lbhz($topictitletemp,34);

if ($ratings eq "") { $ratings2 = ""; $ratings3 = ""; }
else {
    if (-e "${lbdir}forum$inforum/rate$intopic.file.pl") {
	require "${lbdir}forum$inforum/rate$intopic.file.pl";
	$average = int($rates / $votes);
    }
    else { $average = "0"; }
    $ratings2 =  qq(<img src="$imagesurl/images/norate.gif" width=0 height=0 alt="无评分">);
    if ($average > 0) {$ratings2 =  qq(<img src=$imagesurl/images/1star.gif width=14 height=12 alt=太差了>);}
    if ($average > 1) {$ratings2 =  qq(<img src=$imagesurl/images/2star.gif width=14 height=12 alt=有点差>);}
    if ($average > 2) {$ratings2 =  qq(<img src=$imagesurl/images/3star.gif width=14 height=12 alt=一般性>);}
    if ($average > 3) {$ratings2 =  qq(<img src=$imagesurl/images/4star.gif width=14 height=12 alt=挺不错>);}
    if ($average > 4) {$ratings2 =  qq(<img src=$imagesurl/images/5star.gif width=14 height=12 alt=特别好>);}
    undef $average;
    $ratings3 = qq~
<form action="rateit.cgi" method="POST">
<input type="hidden" name="id" value="$inforum">
<input type="hidden" name="forumname" value="$intopic">
<select name="rateselect">
<option value="0">投票评分</option><option value="5">特别好</option><option value="4">挺不错</option><option value="3">一般性</option><option value="2">有点差</option><option value="1">太差了</option>
</select>
<input type="submit" value="评">
~;

}

$replynum=0 if ($replynum eq "");
if ($replynum > $numberofitems-1) {$replynum = $numberofitems - 1;}; 
if ($treeview eq "yes") {
     $replynum=$instart if (($instart ne "")&&($instart ne "0")&&($replynum ne "last"));
     $replynum=$numberofitems -1 if ($replynum eq "last");
     $startarray=$replynum;
     $endarray=$replynum;
}

        $output .= qq~
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
<tr><td width=30% rowspan=2 valign=top>$forumgraphic</td>
<td align=top>
~;
     if ($indexforum ne "no"){
	$output .= qq~
<font color=$fontcolormisc>
<img src=$imagesurl/images/closedfold.gif>　<a href=$forumsummaryprog>$boardname</a><br>
<img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/closedfold.gif width=14 height=14>　<a href=$forumsprog?forum=$inforum>$forumname</a>　[<a href=$boardurl/$forumsprog?show=$inshow&forum=$inforum>返回</a>]<br>
　 <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=14 height=14>　$topictitletemp1　$ratings2
	 ~;
    }
    else {
	$output .= qq~
<font color=$fontcolormisc>
<img src=$imagesurl/images/closedfold.gif>　<a href=$forumsprog?forum=$inforum>$forumname</a><br>
<img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=14 height=14>　$topictitletemp1　$ratings2
 	~;

    }

    $insidead  = "" if (($forumimagead ne "1")&&($useimageadtopic ne "1"));
    $insidead1 = "" if (($forumimagead1 ne "1")&&($useimageadtopic1 ne "1"));
    $threadviewstemp = "您是本帖第 <b>$threadviews</b> 个阅读者" if ($threadviews > 0);

    $output .= qq~$insidead$insidead1
<a name="top"></a>
</td>$uservisitdata</tr></table><br>
<table cellpadding=1 cellspacing=0 width=$tablewidth align=center>
<tr><td align=center width=1></td>
<td width=330 valign=bottom>$newthreadbutton$newreplybutton$newpollbutton</td>
<td align=right valign=bottom width=* nowarp><font color=$forumfontcolor>$threadviewstemp　　$nexttopiclinks</td>
<td align=center width=2></td></tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
<tr><td bgcolor=$tablebordercolor width=1 height=24></td>
<td bgcolor=$titlecolor colspan=2>
<table cellpadding=0 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor><font color=$titlefontcolor>&nbsp;<b>* 贴子主题</B>： $topictitletemp　　</font>$replybutton</td>
<td bgcolor=$titlecolor align=right>$savefile $reporticon $favicon $printpageicon $pagpageicon $bookmarkpage $sendtofriendicon</td>
</tr></table></td><td bgcolor=$tablebordercolor width=1 height=24></td></tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table>
~;

    $editpostnumber = $startarray; $editpostnumber++; $postcountnumber = 0;
    $endarraytemp = $endarray + 1;
    $rn=$startarray;

    my $dirtoopen2 = "$imagesdir" . "usr/$inforum";
    opendir (DIR2, "$dirtoopen2");
    my @dirdata2 = readdir(DIR2);
    closedir (DIR2);
    @dirdata2 = grep(/^$inforum\_$intopic/,@dirdata2);
    my @files11 = grep(/^$inforum\_$intopic\_/,@dirdata2);
    $files11 = @files11;
    $addtimes = $timedifferencevalue*3600 + $timezone*3600;

    foreach (@threads[$startarray .. $endarray]) {
        $addmefile =0;
        if ($rn>0) {
          if ($files11 > 0) {
            if ($sticky eq "on") {$rrn=($#threads-$rn+1); } else {$rrn=$rn;}
            my @files1 = grep(/^$inforum\_$intopic\_$rrn\./,@files11);
            my $file1 = @files1;
            if ($file1 > 0) {
               my $files1s = $files1[0]; chomp $files1s;
               ($up_name, $up_ext) = split(/\./,$files1s);
                $up_ext =~ tr/A-Z/a-z/;
          	$addmefile =1;
          	$files11 --;
            }
          }
        }
        else {
            my @files2 = grep(/^$inforum\_$intopic\./,@dirdata2);
            my $file2 = @files2;
            if ($file2 > 0) {
               my $files2s = $files2[0]; chomp $files2s;
               ($up_name, $up_ext) = split(/\./,$files2s);
                $up_ext =~ tr/A-Z/a-z/;
          	$addmefile =1;
            }
        }

    $rn=$rn+1;

    if ($addmefile == 1) {
	@fileinfo = stat("${imagesdir}usr/$inforum/$up_name.$up_ext");
	$filetype = "unknow";
	$filetype = $up_ext if (-e "${imagesdir}icons/$up_ext.gif");
	if (($up_ext eq "gif")||($up_ext eq "jpg")||($up_ext eq "png")||($up_ext eq "bmp")){
          if ($nodispphoto eq 'yes'){
	    $addme=qq(<a href=$imagesurl/usr/$inforum/$up_name.$up_ext target=_blank><img src=$imagesurl/icons/$filetype.gif border=0 width=16 height=16></a> <a href=$imagesurl/usr/$inforum/$up_name.$up_ext target=_blank>点击显示此主题相关图片</a><br><br>);
	  }
	  else{
	    $addme = qq(<img src=$imagesurl/icons/$filetype.gif border=0 width=16 height=16> 此主题相关图片如下：<br><a href=$imagesurl/usr/$inforum/$up_name.$up_ext target=_blank><img src=$imagesurl/usr/$inforum/$up_name.$up_ext border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>screen.width-333)this.width=screen.width-333"></a><br><br>);
	  }
	}
	elsif ($up_ext eq "swf") {
	    $addme = qq(<img src=$imagesurl/icons/$filetype.gif border=0 width=16 height=16> 该主题有一个 $up_ext 格式 Flash 动画 (共 $fileinfo[7] 字节)<br><br><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$imagesurl/usr/$inforum/$up_name.$up_ext quality=high width=400 height=300 pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed><br>&nbsp;<img src=$imagesurl/images/fav.gif width=16 height=16> <a href=$imagesurl/usr/$inforum/$up_name.$up_ext target=_blank>全屏观看</a> (按右键下载)<br><br>)
	}
	else{
	    $addme = qq(<font color=$fonthighlight>相关附件</font>：<a href=$imagesurl/usr/$inforum/$up_name.$up_ext target=_blank><img src=$imagesurl/icons/$filetype.gif border=0 width=16 height=16 alt="该主题有一个“$filetype”类型附件，点击下载"></a> (共 $fileinfo[7] 字节)<br><br>);
	}
    }
    else { $addme = ""; }

####################################################################3
#	$nowtopicnotemp = $_;
        ($membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$_);
	$topictitle =~ s/^＊＃！＆＊//;

	($postipaddress,$truepostipaddress) = split(/\=/,$postipaddresstemp);
        $proxyip = 0;
	if ($truepostipaddress eq "") {
	    $truepostipaddress = $postipaddress;
	    $proxyip = 1;
	}
       
       $online = qq~<IMG SRC=$imagesurl/images/offline1.gif width=15 height=15 alt=该用户目前不在线>~;
       foreach $user (@onlinedata) {
           @userdetail = split (/\t/, $user);
           if ($userdetail[0] eq $membername) {$online = qq~<IMG SRC=$imagesurl/images/online1.gif width=15 height=15 alt=该用户目前在线>~; last; }
       }
        $postdate = $postdate + $addtimes;
        $postdate = &dateformat("$postdate");

        &getmember("$membername");

        if ($joineddate) {
            $joineddate = $joineddate + $addtimes;
            $joineddate = &joineddate("$joineddate");
        }
        else { $joineddate = "未知"; }

	$numberofposts += $numberofreplys;

        if (!$numberofposts) { $numberofposts = "0"; }

        if ((($post =~ /#Moderation Mode/i) and ($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo'))||($htmlstate eq 'on')) {
            $post =~ s/#Moderation Mode/***** 版主模式 *****\<BR\>/g;
            $post =~ s/&lt;/</g; $post =~ s/&gt;/>/g; $post =~ s/&quot;/\"/g;
        }

        if ($idmbcodestate eq 'on') {
            $post = &lbcode("$post");
            if ($post =~/<blockquote><font face=$font>代码/isg){
               $post =~ s/\&amp\;/\&/ig ;
               $post =~ s/\&lt\;br\&gt\;/<br>/ig;
            }
        }

        if ($count eq 1) { $postbackcolor = "$postcolorone"; $postfontcolor = "$postfontcolorone"; $count++; }
        else { $postbackcolor = "$postcolortwo"; $postfontcolor = "$postfontcolortwo"; $count = 1; }

        if (($emoticons eq 'on') and ($showemoticons eq 'yes') and ($post =~ /:(.+?):/)) {
            $post = &doemoticons("$post");
        }

        if (($emoticons eq 'on') && ($showemoticons eq 'yes')) {
	    $post = &smilecode("$post");
        }

	if ($membercode eq "masked") {
	    $signature ="";
            $post = qq(<br>------------------------<br><font color=$posternamecolor>此用户的发言已经被屏蔽！<br>如有疑问，请联系坛主！</font><br>------------------------);
        }

        if (($signature) and ($showsignature eq 'yes') and ($nodispsign ne "yes") and ($posticon !~/<br>/i) and ($userregistered ne "no")) {
	    $signature = &signlbcode($signature) if ($idmbcodestate eq 'on');
            $post = qq($post<table width=100% cellpadding=0 cellspacing=0><tr><td><br><br>--------------------------------------------------------------------------------<br>$signature</td></tr></table>);
        }
        $glowing = $memglow;
        if ($numberofposts >= $mpostmarkmax) { $mtitle =  $mtitlemax;  $membergraphic = $mgraphicmax; }
        elsif ($numberofposts >= $mpostmark19) { $mtitle =  $mtitle19;  $membergraphic = $mgraphic19; }
        elsif ($numberofposts >= $mpostmark18) { $mtitle =  $mtitle18;  $membergraphic = $mgraphic18; }
        elsif ($numberofposts >= $mpostmark17) { $mtitle =  $mtitle17;  $membergraphic = $mgraphic17; }
        elsif ($numberofposts >= $mpostmark16) { $mtitle =  $mtitle16;  $membergraphic = $mgraphic16; }
        elsif ($numberofposts >= $mpostmark15) { $mtitle =  $mtitle15;  $membergraphic = $mgraphic15; }
        elsif ($numberofposts >= $mpostmark14) { $mtitle =  $mtitle14;  $membergraphic = $mgraphic14; }
        elsif ($numberofposts >= $mpostmark13) { $mtitle =  $mtitle13;  $membergraphic = $mgraphic13; }
        elsif ($numberofposts >= $mpostmark12) { $mtitle =  $mtitle12;  $membergraphic = $mgraphic12; }
        elsif ($numberofposts >= $mpostmark11) { $mtitle =  $mtitle11;  $membergraphic = $mgraphic11; }
        elsif ($numberofposts >= $mpostmark10) { $mtitle =  $mtitle10;  $membergraphic = $mgraphic10; }
        elsif ($numberofposts >= $mpostmark9)  { $mtitle =  $mtitle9;   $membergraphic = $mgraphic9; }
        elsif ($numberofposts >= $mpostmark8)  { $mtitle =  $mtitle8;   $membergraphic = $mgraphic8; }
        elsif ($numberofposts >= $mpostmark7)  { $mtitle =  $mtitle7;   $membergraphic = $mgraphic7; }
        elsif ($numberofposts >= $mpostmark6)  { $mtitle =  $mtitle6;   $membergraphic = $mgraphic6; }
        elsif ($numberofposts >= $mpostmark5)  { $mtitle =  $mtitle5;   $membergraphic = $mgraphic5; }
        elsif ($numberofposts >= $mpostmark4)  { $mtitle =  $mtitle4;   $membergraphic = $mgraphic4; }
        elsif ($numberofposts >= $mpostmark3)  { $mtitle =  $mtitle3;   $membergraphic = $mgraphic3; }
        elsif ($numberofposts >= $mpostmark2)  { $mtitle =  $mtitle2;   $membergraphic = $mgraphic2; }
        elsif ($numberofposts >= $mpostmark1)  { $mtitle =  $mtitle1;   $membergraphic = $mgraphic1; }
        else { $mtitle = $mtitle0; $membergraphic = ""; }  #显示默认等级

        if ($membergraphic) { $membergraphic = "<img src=$imagesurl/images/$membergraphic width=100 height=16>"; }

        if ($avatars eq "on") {
	    if (($personalavatar)&&($personalwidth)&&($personalheight)) { #自定义头像存在
	        if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	            $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
	        }
	        else {
	            $useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>);
	        }
	    }
            elsif (($useravatar ne "noavatar") && ($useravatar)) {
                $useravatar = qq(<br>&nbsp; <img src=$imagesurl/avatars/$useravatar.gif $defaultwidth $defaultheight>);
            }
            else { undef $useravatar; }
        }

        $memberfilename = $membername;
        $memberfilename =~ y/ /_/;
	$memberfilename =~ tr/A-Z/a-z/;


        if (($threadstate ne "closed")&&($threadstate ne "pollclosed")&&($postopen ne "no")) {
            $replygraphic = qq~<a href=$postprog?action=replyquote&forum=$inforum&topic=$intopic&postno=$editpostnumber title=引用回复这个贴子><img src=$imagesurl/images/reply.gif border=0 width=16 height=16 align=absmiddle>引用</a>　~;
        }
        else { undef $replygraphic;}
        
        $copygfx = qq~<a href=$postprog?action=copy1&forum=$inforum&topic=$intopic&postno=$editpostnumber title=复制这个贴子><img src=$imagesurl/images/copy.gif border=0 width=16 height=16 align=absmiddle>复制</a>　~;
        $privatemessagegraphic = qq~<a href="javascript:openScript('$messangerprog?action=new&touser=$memberfilename',420,320)" title="给$membername发送一个短消息"><img src=$imagesurl/images/message.gif border=0 width=16 height=16 align=absmiddle>消息</a>　~;
        $searchgraphic  = qq~<a href="search.cgi?action=startsearch&TYPE_OF_SEARCH=username_search&NAME_SEARCH=topictitle_search&FORUMS_TO_SEARCH=$inforum&SEARCH_STRING=$memberfilename" target=_blank title="搜索$membername在本分论坛的全部贴子"><img src=$imagesurl/images/find.gif border=0 width=16 height=16 align=absmiddle>搜索</a>　~;
        $profilegraphic = qq~<a href=$profileprog?action=show&member=$memberfilename title="查看$membername的个人资料"><img src=$imagesurl/images/profile.gif border=0 width=16 height=16 align=absmiddle>查看</a>　~;
        $friendgraphic  = qq~<a href="javascript:openScript('friendlist.cgi?action=adduser&adduser=$memberfilename',420,320)" title="加$membername为我的好友"><img src=$imagesurl/images/friend.gif border=0 width=16 height=16 align=absmiddle>好友</a>　~;
        $editgraphic    = qq~<a href=$postingsprog?action=edit&forum=$inforum&topic=$intopic&postno=$editpostnumber title=编辑这个贴子><img src=$imagesurl/images/edit.gif border=0 width=16 height=15 align=absmiddle>编辑</a>~;
        $delgraphic    ="";
        $delgraphic    = qq~<a href=$postingsprog?action=directdel&forum=$inforum&topic=$intopic&postno=$editpostnumber title=删除这个回复><img src=$imagesurl/images/del.gif border=0 width=16 height=16>删除</a>~ if (($inmembercode eq "ad")||($inmembercode eq 'smo')||($inmembmod eq "yes"));
        $partition      = qq~|~;

	if($showemail eq "yes" || $showemail eq "msn") {
        	$emailgraphic = "<a href=mailto:$emailaddress title=电子邮件地址><img src=$imagesurl/images/email.gif border=0 width=16 height=16 align=absmiddle>邮件</a>　" if($showemail eq "yes");
        	$emailgraphic = "<a href=mailto:$emailaddress title=\"MSN 地址\"><img src=$imagesurl/images/msn.gif border=0 width=16 height=16 align=absmiddle>MSN</a>　" if($showemail eq "msn");
	}
        else { undef $emailgraphic; }

        $homepage =~ s/http\:\/\///sg;
        if ($homepage) { $homepagegraphic = qq~<a href=http://$homepage target=_blank title="访问 $membername 的主页"><img src=$imagesurl/images/homepage.gif border=0 width=16 height=16 align=absmiddle>主页</a>　~; }
            else { undef $homepagegraphic; }

        if (($aolname) && ($aolname =~ /[0-9]/)) {
        	my $oicqimg=&getoicq($aolname);
        	$aolgraphic = qq~<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$aolname target=_blank title="查看 QQ:$aolname的资料"><img src=$oicqimg border=0 width=16 height=16 align=absmiddle>QQ</a>　~;
        }
        else { undef $aolgraphic; }

        if (($icqnumber) && ($icqnumber =~ /[0-9]/)) { $icqgraphic = qq~<a href="javascript:openScript('$miscprog?action=icq&UIN=$icqnumber',450,300)" title="给 ICQ:$icqnumber 发个消息"><img src=http://wwp.icq.com/scripts/online.dll?icq=$icqnumber&img=5 border=0 width=16 height=16 align=absmiddle>ICQ</a>　~; }
            else { undef $icqgraphic; }

    if ($userregistered ne "no") {
        if ($membercode eq "ad") {
            $posterfontcolor = "$adminnamecolor";
            $glowing = $adminglow;
            $membernameimg = "<img src=$imagesurl/images/teamad.gif alt=此人为坛主 width=16>";
            $membergraphic = "<img src=$imagesurl/images/$admingraphic width=100 height=16>" if ($admingraphic ne "");
            $mtitle = $adtitle if ($adtitle ne "");
            if (($membertitle eq "Member")||($membertitle eq "member")) { $membertitle = "论坛坛主"; }
        }
        elsif ($membercode eq "mo") {
            $posterfontcolor = "$teamnamecolor";
            $glowing = $teamglow;
            $membernameimg = "<img src=$imagesurl/images/teammo.gif alt=此人为版主 width=16>";
            $membergraphic = "<img src=$imagesurl/images/$modgraphic width=100 height=16>" if ($modgraphic ne "");
	    $mtitle = $motitle if ($motitle ne "");
            if (($membertitle eq "Member")||($membertitle eq "member")) { $membertitle = "论坛版主"; }
        }
        elsif ($membercode eq "smo") {
            $posterfontcolor = "$smonamecolor";
            $glowing = $smoglow;
            $membernameimg = "<img src=$imagesurl/images/teamsmo.gif alt=此人为总版主 width=16>";
            $membergraphic = "<img src=$imagesurl/images/$smodgraphic width=100 height=16>" if ($smodgraphic ne "");
	    $mtitle = $smotitle if ($smotitle ne "");
            if (($membertitle eq "Member")||($membertitle eq "member")) { $membertitle = "总版主"; }
        }
        elsif ($membercode eq "banned") {
            $posterfontcolor = "$posternamecolor";
            $glowing = $banglow;
            $membergraphic = "";
            $membertitle = "&nbsp;　<b>已被禁止发言</b>";
            $membernameimg ="";
        }
        elsif ($membercode eq "masked") {
            $posterfontcolor = "$posternamecolor";
            $glowing = $banglow;
            $membergraphic = "";
            $membertitle = "&nbsp;　<b>发言已被屏蔽</b>";
            $membernameimg ="";
        }
        else { $posterfontcolor = "$posternamecolor"; $membernameimg =""; }
    }
    else {$membernameimg ="";}

    if (($inmembercode eq "ad")||($inmembercode eq "mo")||($inmembercode eq 'smo')) { $rateuser = qq~　<a href="userrating.cgi?membername=$membername&oldforum=$inforum&oldtopic=$intopic" title=给此用户投票><img src=$imagesurl/images/poll1.gif border=0 width=16 height=16>投票</a>~; }
    else {undef $rateuser; }

    if ($membertitle eq "member" || $membertitle eq "Member" || $membertitle eq "") { undef $membertitle; }
    else {$membertitle="头衔: $membertitle" if (($membercode ne "banned")&&($membercode ne "masked"));}

    $membertitle =~ s/&lt;/</g; $membertitle =~ s/&gt;/>/g; $membertitle =~ s/&quot;/"/g;

    $post =~ s/\[这个贴子最后由(.+?)编辑\]/\<font color=$posternamecolor>\[这个贴子最后由$1编辑\]\<\/font\>/isg;
    $location = "保密" if($location eq "");


if ($addme eq "") { $addmeshow =""; }
else{ $addmeshow=$addme; $addme=""; }

$posticon =~ s/\s//isg;
if ($posticon ne "") {
    if ($posticon =~/<br>/i){
	if ($showsignature eq 'yes') { $polltype = "checkbox"; } else { $polltype = "radio"; }

	$maxpollitem = 5 if ($maxpollitem < 5);
	$maxpollitem = 50 if ($maxpollitem > 50);

      $posticon=~s/<br><br>/<BR>/isg;
      $posticon=~s/<br>/\t/ig;
      @temppoll = split(/\t/, $posticon);
      $temppoll = @temppoll;
      if ($temppoll >1) {
	$maxpolllength = 0;

	($poll[1], $poll[2], $poll[3], $poll[4], $poll[5],$poll[6],$poll[7],$poll[8],$poll[9],$poll[10],$poll[11],$poll[12],$poll[13],$poll[14],$poll[15],$poll[16],$poll[17],$poll[18],$poll[19],$poll[20],$poll[21],$poll[22],$poll[23],$poll[24],$poll[25],$poll[26],$poll[27],$poll[28],$poll[29],$poll[30],$poll[31],$poll[32],$poll[33],$poll[34],$poll[35],$poll[36],$poll[37],$poll[38],$poll[39],$poll[40],$poll[41],$poll[42],$poll[43],$poll[44],$poll[45],$poll[46],$poll[47],$poll[48],$poll[49],$poll[50]) = split(/\t/, $posticon);
	$j=0;
	$pollinput ="";
    	for ($i=1;$i<=$maxpollitem;$i++){
    	    if ($poll[$i] ne "") {
    	        $j++;
    	        $pollinput .= qq~<input type="$polltype" name="myChoice" value='$i'> $poll[$i]<br>~;
    	        $maxpolllength = length($poll[$i]) if (length($poll[$i]) > $maxpolllength);
    	    }
	}
	$maxpolllength = $maxpolllength*7+10;
	$maxpolllength = 150 if ($maxpolllength < 150);
	$maxpolllength = 510 if ($maxpolllength > 510);

	$pollform =qq~
<form action="$pollprog" method=post>
<input type=hidden name=action value="poll">
<input type=hidden name=id value="$inforum">
<input type=hidden name=threadname value="$intopic">
<table cellpadding=1 cellspacing=0 width=$maxpolllength bgcolor=$tablebordercolor>
<tr><td nowrap><table width=100% cellpadding=4 cellspacing=0 bgcolor="$postbackcolor">
<tr><td nowrap>$pollinput<tr><td align=center nowrap><HR size=1 width=85%>
<input type=submit name=results value='参加投票'>
</td></form></tr></table></td></tr></table>
~;

	$showpoll = "";
	$pollnull = "";
  	if (($inmembercode eq "ad")||($inmembercode eq 'smo')||($inmembmod eq "yes")) { $adminview = 1; $maxpolllength = "550"; $adminviewcolspan = "3"; }
    	else { $adminview = 0; $maxpolllength = "510"; $adminviewcolspan = "2"; }

	$poll =qq~ <table width=$maxpolllength>

	~;
	
	
	$filetomake = "$lbdir" . "forum$inforum/$intopic.poll.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, "$filetomake")) {
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @allpoll = <FILE>;
            close(FILE);
            $size=@allpoll;
            &winunlock($filetomake) if ($OS_USED eq "Nt");
        }
	else { &winunlock($filetomake) if ($OS_USED eq "Nt"); $size=0; @allpoll=(); }
        if ( $size > 0 ) {
            $size= 0;
	    @thispoll=('0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0');
	    @pollname=('','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');

	    foreach (@allpoll){
		$_=~s/[\n\r]//isg;
		next if ($_ eq "");
		($tmpinmembername,$tmpmyChoice)=split(/\t/, $_);
		for ($i=1;$i<=$j;$i++){
		    if ($i == $tmpmyChoice) {
		    	$thispoll[$i]++;
		    	$pollname[$i] = "$pollname[$i]$tmpinmembername\t";
		    	$size ++;
		    }
		}
	        $showpoll="true" if ($tmpinmembername eq $inmembername);
	    }
	}
        if ( $size > 0 ) {
	    if ($showsignature eq 'yes') {
	        $poll .= qq~ <tr><td colspan=$adminviewcolspan><HR size=1 width=100%></td></tr><tr><td colspan=$adminviewcolspan>目前总共有 <font color=$fonthighlight><B>$size</B></font> 张投票，结果如下：<HR size=1 width=100%><BR></td></tr>~;
	    }
	    else {
	        $poll .= qq~ <tr><td colspan=$adminviewcolspan><HR size=1 width=100%></td></tr><tr><td colspan=$adminviewcolspan>目前共有 <font color=$fonthighlight><B>$size</B></font> 人参加投票，结果如下：<HR size=1 width=100%><BR></td></tr>~;
	    }
    	    for ($i=1;$i<=$j;$i++){
    	    	if ($poll[$i] ne ""){
    		    $mypoll=int(($thispoll[$i]/$size)*1000)/10;
    		    $width=int(($mypoll/100)*160);
    		    if ($adminview == 1) {
    		    	undef @pollmanname;
    		    	$adminviewpoll = qq~</td><td nowarp><select><option>投票人名单　</option><option>----------</option>~;
    		        @pollmanname = split(/\t/, $pollname[$i]);
    		        $pollmanname = @pollmanname;
    		        foreach (@pollmanname) {
    		            $adminviewpoll .= qq~<option value="$_">$_ </option>~;
    		        }
    		    	$adminviewpoll .= qq~</select>~;
	    		$adminviewpoll = "</td><td nowarp>[没有人投票]" if ($pollmanname eq 0);

    		    }
    		    else { undef $adminviewpoll; }
    		    $ii = $i;
    		    $ii = $ii - 40 if ($ii > 40);
    		    $ii = $ii - 30 if ($ii > 30);
    		    $ii = $ii - 20 if ($ii > 20);
    		    $ii = $ii - 10 if ($ii > 10);
    		    $poll.=qq~<tr><td nowarp>$poll[$i]　　　&nbsp;　　　</td><td nowarp> <img src=$imagesurl/images/bar$ii.gif width=$width height=10> <b>$thispoll[$i]</b> 票数 $mypoll%　$adminviewpoll</td></tr>\n~;
    	    	}
	    }
	}
	else {
	    $poll .= qq~ <tr><td colspan=2><HR size=1 width=100%></td></tr><tr><td colspan=2>没有人参加此投票，选项列表如下：<HR size=1 width=100%><BR></td></tr>~;
    	    for ($i=1;$i<=$j;$i++){
		$poll .= qq~<tr><td colspan=2>$poll[$i] </td></tr>~;
	    }
	    $pollnull = "true";
	}
	$poll .= "</td></tr><tr><td colspan=$adminviewcolspan><HR size=1 width=100%></td></tr></table>";

	if (($threadstate eq "pollclosed")||($showpoll eq "true")||($inmembername eq "客人")) {
	    $poll1 = "<font color=$fonthighlight>客人不能投票，请注册！</font>" if ($inmembername eq "客人");
	    $poll1 = "<font color=$fonthighlight>谢谢，你已经投过票了！</font>" if ($showpoll eq "true");
	    $poll1 = "<font color=$fonthighlight>对不起，此投票已经关闭！</font>" if ($threadstate eq "pollclosed");
	    $poll = "$poll$poll1";
	}
	else {
	    if ($pollnull eq "true") {
	        $poll = "$pollform<BR><font color=$fonthighlight>目前暂时没有人投票！</font>";
	    }
	    else {
	        $poll = "$pollform$poll";
	    }
	}

    	$editgraphic ="";
    	$delgraphic  ="";
    	$posticon    ="";
    	$posticon    ="";
      }
    }
    else {
        if ($posticon eq "") {
            $posticon = int(rand(23));
    	    $posticon = "0$posticon" if ($posticon<10);
    	    $posticon = $posticon . ".gif";
	}
    	$posticon = qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight>~;
    }
}
else {
    $posticon = int(rand(23));
    $posticon = "0$posticon" if ($posticon<10);
    $posticon = qq~<img src=$imagesurl/posticons/$posticon.gif $defaultsmilewidth $defaultsmileheight>~;
}

    if (($pvtip eq "on")||($membercodetemp eq "ad")||(($membercodetemp eq 'smo')&&($smocanseeip eq "no"))) {
        $fromwhere = &ipwhere("$truepostipaddress");
    }
    else { $fromwhere = "已设置保密"; }

   ($ip1,$ip2,$ip3,$ip4) = split(/\./,$postipaddress);

   if ($membercodetemp eq "ad") {
        $postipaddress="$postipaddress";
   }
   elsif ($membercodetemp eq "smo") {
   	if ($smocanseeip eq "no") { $postipaddress="$postipaddress"; }
       	else {
       	    if ($pvtip eq "on") { $postipaddress="$postipaddress"; }
       	    else { $postipaddress="已设置保密"; }
	}
   }
   elsif ($inmembmod eq "yes") {
       if ($pvtip eq "on") { $postipaddress="$ip1.$ip2.$ip3.*"; }
       else { $postipaddress="已设置保密"; }
   }
   else {
       if (($pvtip eq "on")&&($inmembername ne "客人")) {
           $postipaddress="$ip1.$ip2.*.*";
       }
       else { $postipaddress="已设置保密"; }
   }

    if ($badwords) {
        @pairs = split(/\&/,$badwords);
        foreach (@pairs) {
            ($bad, $good) = split(/=/,$_);
            chomp $good;
            $location =~ s/$bad/$good/isg;
            $post =~ s/$bad/$good/isg;
            $jhmp =~ s/$bad/$good/isg;
            $membertitle =~ s/$bad/$good/isg;
            $topictitle =~ s/$bad/$good/isg;
        }
    }

if ($proxyip ne 1) {
    if ($membercodetemp eq "ad") { $fromproxy ="真实 IP： $truepostipaddress"; } else { $fromproxy = "此 IP 为代理服务器"; }
}
else { undef $fromproxy; }

    if ($poll ne ""){
	$post=$post."<br>".$poll;
	$poll="";
    }
    if ($rating !~ /^[0-9\-]+$/) {$rating = 0;}
    if ($rating eq "") {$rating =0;}
    if ($rating > 0 ) {$rating = "+$rating"; }

    if ($jhmp eq "无门无派" || $jhmp eq "") { undef $jhmp; }
    else {$jhmp="门派: $jhmp<br>";}

    $jingyan = $addjy;
if ($usertype eq "0") {
    if (($membercode eq "rz")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo")) {
    	$mymoney = ($numberofposts-$numberofreplys) * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney;
    	$meili   = ($numberofposts-$numberofreplys) * $addml + $numberofreplys * $replyml + $visitno * $loginml + $meili - $postdel * $delml;
    	$jingyan = ($numberofposts-$numberofreplys) * $ttojy + $numberofreplys * $rtojy + $visitno * $ltojy + $jingyan - $postdel * $deljingyan;
    }
}
else {
    	$mymoney = ($numberofposts-$numberofreplys) * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney;
    	$meili   = ($numberofposts-$numberofreplys) * $addml + $numberofreplys * $replyml + $visitno * $loginml + $meili - $postdel * $delml;
    	$jingyan = ($numberofposts-$numberofreplys) * $ttojy + $numberofreplys * $rtojy + $visitno * $ltojy + $jingyan - $postdel * $deljingyan;
}

    $mymoney = "<font title=$mymoney>>9999999999999</font>" if ($mymoney > 9999999999999 );

    $meili1= $meili;
    $meili = 0 if ($meili < 0);
    $mlwidth = int(sqrt($meili)*10)/30;
    $mlwidth = 120 if ($mlwidth > 120);
    $mlgraphic = qq~<img src=$imagesurl/images/bar4.gif width=$mlwidth height=8 alt="$meili1">~;

    $jingyan1= $jingyan;
    $jingyan = 0 if ($jingyan < 0);
    $jywidth = int(sqrt($jingyan)*10)/60;
    $jywidth = 120 if ($jywidth > 120);
    $jygraphic = qq~<img src=$imagesurl/images/bar5.gif width=$jywidth height=8 alt="$jingyan1">~;
    $userflag = "blank" if ($userflag eq "");
    $userflag = qq~　<img src=$imagesurl/flags/$userflag.gif width=21 height=14 align=absmiddle>~;

if ($userxz eq "z1")     {$showxz = "<IMG height=13 src=$imagesurl/star/z1.gif  width=13 alt=白羊座 align=absmiddle>";}
elsif ($userxz eq "z2")  {$showxz = "<IMG height=13 src=$imagesurl/star/z2.gif  width=13 alt=金牛座 align=absmiddle>";}
elsif ($userxz eq "z3")  {$showxz = "<IMG height=13 src=$imagesurl/star/z3.gif  width=13 alt=双子座 align=absmiddle>";}
elsif ($userxz eq "z4")  {$showxz = "<IMG height=13 src=$imagesurl/star/z4.gif  width=13 alt=巨蟹座 align=absmiddle>";}
elsif ($userxz eq "z5")  {$showxz = "<IMG height=13 src=$imagesurl/star/z5.gif  width=13 alt=狮子座 align=absmiddle>";}
elsif ($userxz eq "z6")  {$showxz = "<IMG height=13 src=$imagesurl/star/z6.gif  width=13 alt=处女座 align=absmiddle>";}
elsif ($userxz eq "z7")  {$showxz = "<IMG height=13 src=$imagesurl/star/z7.gif  width=13 alt=天秤座 align=absmiddle>";}
elsif ($userxz eq "z8")  {$showxz = "<IMG height=13 src=$imagesurl/star/z8.gif  width=13 alt=天蝎座 align=absmiddle>";}
elsif ($userxz eq "z9")  {$showxz = "<IMG height=13 src=$imagesurl/star/z9.gif  width=13 alt=射手座 align=absmiddle>";}
elsif ($userxz eq "z10") {$showxz = "<IMG height=13 src=$imagesurl/star/z10.gif width=13 alt=魔羯座 align=absmiddle>";}
elsif ($userxz eq "z11") {$showxz = "<IMG height=13 src=$imagesurl/star/z11.gif width=13 alt=水瓶座 align=absmiddle>";}
elsif ($userxz eq "z12") {$showxz = "<IMG height=13 src=$imagesurl/star/z12.gif width=13 alt=双鱼座 align=absmiddle>";}
else {$showxz = "";}

    if ($userregistered eq "no") {
    	$membername=~s/\(客\)/ \(客人\)/isg;
    	$membertitle="　　 -* 未注册 *-";
    	$rating = "未知";
    	$membergraphic = "";
    	$useravatar = "<BR>";
    	$posterfontcolor = "$posternamecolor";
    	$mtitle = "未知";
    	$joineddate = "未知";
    	$location = "未知";
    	$numberofposts = 0;
    	$sex = "";
    	$jhmp= "";
    	$mymoney = 0;
    	$mlgraphic="未知";
    	$jygraphic="未知";
    	undef $rateuser;
    	undef $userflag;
    	undef $privatemessagegraphic;
    	undef $profilegraphic;
    	undef $friendgraphic;
    	undef $emailgraphic;
    	undef $homepagegraphic;
    	undef $aolgraphic;
    	undef $icqgraphic;
    	undef $searchgraphic;
    	undef $showxz;
    }
    if ($sex eq "m") { $seximages = "<img src=$imagesurl/images/mal.gif width=20 height=14 alt=哦，帅哥哟>"; }
    elsif ($sex eq "f") { $seximages = "<img src=$imagesurl/images/fem.gif width=20 height=14 alt=哇，美女耶>";}
    else { $seximages = ""; }

    $useravatar = "" if ($nodispavatar eq "yes");
    $delgraphic = "" if ($editpostnumber == 1);

    $output .= qq~<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
<tr><td bgcolor=$tablebordercolor width=1 height=24></td><td bgcolor="$postbackcolor">
~;

    $output .= qq~<a name="end">~ if ($editpostnumber eq $endarraytemp);
    $moneyname ="雷傲元" if ($moneyname eq "");

    $output .= qq~<table width=100% cellpadding=4 cellspacing=5 bgcolor=$postbackcolor>
<tr><td bgcolor=$postbackcolor valign=top width=168 rowspan=2>
<table cellpadding=0 cellspacing=0><tr><td width=30>$online</td><td><table style="filter:glow(color=$glowing,direction=135)">&nbsp;<font color=$posterfontcolor><b>$membername&nbsp;</b></font></table></td><td>　$seximages $membernameimg</td></tr></table>
<font color=$postfontcolortwo>$membertitle</font> $showxz<BR>
<font color=$postfontcolorone>$jhmp</font>
$useravatar
<br>$membergraphic
<br><font color=$postfontcolortwo>威望: $rating$rateuser</font>
<br><font color=$postfontcolorone>级别: <a href=lookinfo.cgi?action=style target=_blank>$mtitle</a></font>
<br><font color=$postfontcolortwo>魅力: $mlgraphic</font>
<br><font color=$postfontcolorone>经验: $jygraphic</font>
<br><font color=$postfontcolortwo>金钱: $mymoney $moneyname</font>
<br><font color=$postfontcolorone>来自: $location$userflag</font>
<br><font color=$postfontcolortwo>鉴定: $fromwhere</font>
<br><font color=$postfontcolorone>总发贴数: <b>$numberofposts</b> 篇</font>
<br><font color=$postfontcolortwo>注册日期: $joineddate</font><BR>
</td>
<td bgcolor=$postbackcolor width=1 height=100% rowspan=2>
<table width=1 height=100% cellpadding=0 cellspacing=0 bgcolor=$titlecolor><tr><td width=1></td></tr></table>
</td><td bgcolor=$postbackcolor valign=top width=* height=100%>
$privatemessagegraphic$profilegraphic$searchgraphic$friendgraphic$emailgraphic$homepagegraphic$aolgraphic$icqgraphic$copygfx$replygraphic$replynow<BR><hr width=100% size=1 color=$tablebordercolor>
<table cellpadding=0 cellspacing=0 width=100% style="TABLE-LAYOUT: fixed">
<tr><td width=32 valign=top>$posticon&nbsp;</td>
<td style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word; $paraspace; $wordspace\pt">$addmeshow<font color=$postfontcolor><font color=$postfontcolor>$post<BR></td>
<td width=16></td></tr></table></td></tr>
<tr><td class=bottomline bgcolor=$postbackcolor valign=bottom><hr width=100% size=1 color=$tablebordercolor>
<table width=100% cellpadding=0 cellspacing=0>
<tr><td valign=bottom><font color=$postfontcolor>$editgraphic　$delgraphic　<img src=$imagesurl/images/posttime.gif width=16 height=15 alt=发贴时间 align=absmiddle>$postdate　<img src=$imagesurl/images/ip.gif width=13 height=15 alt="$fromproxy" align=absmiddle>IP: $postipaddress</td>
<td align=right nowarp valign=bottom width=110>$ratings3</td></form>
<td align=right valign=bottom width=4></td></tr></table>
</td></tr></table></td><td bgcolor=$tablebordercolor width=1 height=24></td></tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table>
~;
    $ratings3 = "";
    $editpostnumber++; $postcountnumber++;
    }

##################3
if ($treeview eq "yes") {
    @treelist=();
    $pages = qq~<font color=$menufontcolor><b>本主题共有一页</b>~;
    @tmptopic = @threads;
    chomp(@tmptopic);

    foreach(@tmptopic) {
      ($membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$_);
	$topictitle =~ s/^＊＃！＆＊//;
        $postdate = &shortdate($postdate + ($timezone*3600) + ($timedifferencevalues*3600));
	$post =~ s/\[这个贴子最后由(.+?)编辑\]//isg;
	$post =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	$post =~ s/\[quote\](.*)\[\/quote\]//isg;
	$post =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/isg;
	$post =~ s/\<img\s*(.*?)\s*\>//isg;
	$post =~ s/\<BR\>/ /isg;
	$post =~ s/\<P\>/ /isg;
	$post =~ s/( )+$/ /isg;
	$post =~ s/^( )+/ /isg;
	$post =~ s/<(.|\n)+?>//g;
	$post =~ s/\[.+?\]//g;

      $topictitlemax = 50;
      $topictitlemax = 96 if (($screenmode >=9)||($tablewidth > 770));

      if (length($post)>=$topictitlemax) {
        $post=&lbhz($post,$topictitlemax);
      }
      if ($post eq "") {$post="无内容";}
      push(@treelist,"$post\t$membername\t$postdate\t$posticon");
    }
    chomp(@treelist);
    $output .= qq~<p><table cellpadding=4 cellspacing=1 width=$tablewidth align=center><tr><td colspan=3 bgcolor=$titlecolor><font color=$titlefontcolor><B>&nbsp;* 树形目录</B></font></td></tr>~;
    for($i=0;$i<=$#treelist;$i++) {
      ($post,$membername,$postdate,$posticon)=split(/\t/,$treelist[$i]);
        if ($posticon eq "") {
            $posticon = int(rand(23));
    	    $posticon = "0$posticon" if ($posticon<10);
    	    $posticon = $posticon . ".gif";
	}
    	$posticon = qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight>~;
      $memberfilename = $membername;
      $memberfilename =~ y/ /_/;
      $memberfilename =~ tr/A-Z/a-z/;
      if ($membername=~/\(客\)/) {
          $membername=~s/\(客\)//isg;
	  $h4 = qq~<font color=$postfontcolorone title="此为未注册用户">$membername</font>~;
      }
      else {
	  $h4 = qq~<a href=$profileprog?action=show&member=$memberfilename title=\"查看$membername的个人资料\">$membername</a>~;
      }
      $treefontcolor=$postfontcolorone;
      $h1="<a href=$boardurl/${thisprog}?forum=${inforum}&topic=${intopic}&replynum=$i&show=$show>";
      $h2="</a>";
      $h3="　　回复：";
      if ($i==0) {$h3="　主题：";}
      if ($treebackcolor ne $postcolorone) {$treebackcolor=$postcolorone;} else {$treebackcolor=$postcolortwo;}
      if ($i==$replynum) {
           $treefontcolor="$fonthighlight";
           $h1=""; $h2="";
      }
      $output .=qq~<tr bgcolor="$treebackcolor"><td><font color=$treefontcolor> $h3 $posticon $h1 $post $h2</td><td width=130> &nbsp 作者：$h4</td><td width=70 align=right> $postdate&nbsp;</font></td></tr>~;
    }
    $output .= qq~</table><img src="" height=3 width=0><BR>~;
}
########3

if (($threadstate ne "closed")&&($threadstate ne "pollclosed")&&($postopen ne "no")&&($dispquickreply ne "no")) {

    if ($emoticons eq "on") { $emoticonslink = qq~<input CHECKED name=inshowemoticons type=checkbox value=yes>使用表情字符转换？~; }
    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = qq~<input name=notify type=checkbox value=yes checked>有回复时使用邮件通知您？<br>~; }
	    else { $requestnotify = qq~<input name=notify type=checkbox value=yes>有回复时使用邮件通知您？<br>~;}
    }
}

 $output .= qq~
<table cellpadding=0 cellspacing=2 width=$tablewidth align=center>
<tr bgcolor=$menubackground height=4></tr><tr><td>
<font color=$menufontcolor>&nbsp;$pages</td>
~;
if ($indexforum ne "no"){
	 $output .= qq~<td align=right nowrap>$jumphtml</td></form>~;
}
$output .= qq~</tr></table><br>~;

if (($threadstate ne "closed")&&($threadstate ne "pollclosed")&&($postopen ne "no")&&($dispquickreply ne "no")) {
$output .= qq~
<form action="$postprog?action=reply&forum=$inforum&topic=$intopic" method=post name="FORM">
<input type=hidden name="action" value="addreply">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<table cellPadding=5 cellSpacing=1 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td bgcolor=$titlecolor width=178><font color=$fontcolormisc><b>快速回复主题:</b></font></td><td bgcolor=$titlecolor colspan="2" width=*> <font color=$fontcolormisc>$topictitle</font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>输入用户名和密码:</b></font></td><td bgcolor=$miscbackone> <font color=$fontcolormisc><b>用户名</b>: <input type=text name="membername" value="$inmembername"> <a href="$registerprog">没有注册？</a>　 <b>密码:</b> <input type=password name="password" value="$inpassword"> <a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo valign=top width=178><font color=$fontcolormisc><BR>
<input CHECKED name=inshowsignature type=checkbox value=yes>显示您的签名？<br>
$requestnotify
$emoticonslink<BR>
&nbsp;预览？<input name=previewfirst type=radio value=yes>是&nbsp;<input CHECKED name=previewfirst type=radio value=no>否</font></td>
<td bgcolor=$miscbacktwo colspan="2" width=*> <textarea cols=80 name=inpost onKeyDown=ctlent() rows=5></textarea><br>
 <INPUT name=Submit onclick="return clckcntr();" type=submit value="发 表">　<INPUT name=Clear type=reset value="清 除">
</td></tr></table>
</form>
~;
}
$output .= qq~
<table cellspacing=0 cellpadding=0 width=$tablewidth align=center>
<tr><td>&nbsp;<a href=#top><img src=$imagesurl/images/gotop.gif height=15 width=15 border=0 align=absmiddle>顶端</a></td><td nowrap align=right><font color=$menufontcolor><b>主题管理</B>：
<a href=jinghua.cgi?action=add&forum=$inforum&topic=$intopic>精华</a> |
<a href=$postingsprog?action=locktop&forum=$inforum&topic=$intopic>固顶</a> |
<a href=$postingsprog?action=unlocktop&forum=$inforum&topic=$intopic>取消固顶</a> |
<a href=$postingsprog?action=puttop&forum=$inforum&topic=$intopic>提升</a> |
<a href=$postingsprog?action=lock&forum=$inforum&topic=$intopic>锁定</a> |
<a href=$postingsprog?action=unlock&forum=$inforum&topic=$intopic>解锁</a> |
<a href=$postingsprog?action=delete&forum=$inforum&topic=$intopic>删除</a> |
<a href=$postingsprog?action=movetopic&forum=$inforum&topic=$intopic>移动</a>&nbsp;
</td></tr></table><p><p>
~;

    &output(
        -Title   => "$forumname - $topictitle",
        -ToPrint => $output,
        -Version => $versionnumber
        );


sub postings {
if ($postopen eq "no") { $newthreadbutton = ""; }
else { $newthreadbutton = qq~<a href=$postprog?action=new&forum=$inforum><img src=$imagesurl/images/$newthreadlogo border=0 alt=发表一个新主题 width=99 height=25></a>　~; }

if ($pollopen eq "no") { $newpollbutton = ""; }
else { $newpollbutton = qq~<a href=$pollprog?action=new&forum=$inforum><img src=$imagesurl/images/$newpolllogo border=0 alt=开启一个新投票 width=99 height=25></a>~; }

if (($threadstate ne "closed")&&($threadstate ne "pollclosed")&&($postopen ne "no")) {
        $newreplybutton = qq~<a href=$postprog?action=reply&forum=$inforum&topic=$intopic><img src=$imagesurl/images/$newreplylogo border=0 alt=回复贴子 width=99 height=25></a>　~;
        $replybutton = qq~<a href=$postprog?action=reply&forum=$inforum&topic=$intopic><img src=$imagesurl/images/replytothread.gif border=0 alt=回复贴子 height=13 align=absmiddle></a>~;
        $replynow = qq~<a href=$postprog?action=reply&forum=$inforum&topic=$intopic><img src=$imagesurl/images/replynow.gif border=0 alt=回复贴子 width=16 height=16>回复</a>　~;
    }
    else {
        $replybutton = qq~<img src=$imagesurl/images/closed.gif alt=贴子被锁定，不能回复 height=13>~;
        undef $replynow;
        undef $newreplybutton;
    }
}

END {
  if ($cpudisp eq "1") {
    $TT1 = new Benchmark;
    $td  = Benchmark::timediff($TT1,  $TT0);
    $td  = Benchmark::timestr($td);
    $td  =~ /(\d+)\s*wallclock secs \(\s*?(\d*?\.\d*?)\s*usr\s*\+\s*(\d*?\.\d*?)\s*sys/i;
    print "<center><font color=$cpudispcolor>程序占用 CPU 时间：$2 usr + $3 sys";
  }
}
