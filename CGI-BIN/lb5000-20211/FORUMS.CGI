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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/mpic.cgi";
require "data/styles.cgi";
require "lb.lib.pl";
require "visitforum.lib.pl";
$|++;                                     # Unbuffer the output

$thisprog = "forums.cgi";

$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/\/$//;

$query = new LBCGI;
&ipbanned; #封杀一些 ip

$inforum        = $query -> param('forum');
$action         = $query -> param('action');
$inshow         = $query -> param('show');
$inthreadages 	= $query -> param('threadages');
$jumpto         = $query -> param('jumpto');
$inorder 	= $query -> param('order');
$action         = &stripMETA("$action");
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

if (($forumimagead eq "1")||($useimageadforum eq "1")||($forumimagead1 eq "1")||($useimageadforum1 eq "1")) {
	require "${lbdir}imagead.cgi";
}

$inmembername  = $query -> param('membername');
$inpassword    = $query -> param('password');
$forumpassword = $query -> param('forumpassword');
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

$newmarktime = 24 if ($newmarktime eq "");

$screenmode = $query->cookie("screenmode");
$screenmode=7 if ($screenmode eq "");

$onlineview1 = $query->cookie("onlineview");
$onlineview  = $onlineview1 if ($onlineview1 ne "");
$onlineview  = 1 if ($onlineview eq "");

if ($action eq "onlineview") {
    if ($onlineview == 1){ $onlineview=0; } else { $onlineview=1; }
}

$onlineviewcookie     = cookie(-name    =>   "onlineview",
                         -value   =>   "$onlineview",
                         -path    =>   "$cookiepath/"
                         );

if ($onlineview==1){
    $onlinetitle="[<a href=$thisprog?action=onlineview&forum=$inforum ><font color=$titlefontcolor>关闭详细列表</font></a>]";
}
else {
    $onlinetitle="[<a href=$thisprog?action=onlineview&forum=$inforum ><font color=$titlefontcolor>显示详细列表</font></a>]";
}


if ((!$inmembername) or ($inmembername eq "客人")) {
    $inmembername = "客人";
}
else {
    &getmember("$inmembername");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    &getlastvisit;
    $forumlastvisit = $lastvisitinfo{$inforum};
    $currenttime = time;
    &setlastvisit("$inforum,$currenttime");
}
$cpudisp = 1 if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"));
&getforum("$inforum");
&badwordfile;

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
$addtimes = $timedifferencevalue*3600 + $timezone*3600;

if ($action eq "accessrequired") {
    if ((($userregistered ne "no")&&($allowedentry{$inforum} eq "yes"))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||(($userregistered ne "no") && ($forumpassword eq $forumpass))) {
	if ($inpassword ne $password){ &error("进入论坛&你不允许进入该论坛！"); }
	$allowcookiename  = "forumsallowed" . "$inforum";
	$allowforumcookie = cookie(-name => "$allowcookiename", -value => "$forumpass", -path => "$cookiepath/");
	print header(-cookie=>[$allowforumcookie], -charset=>gb2312);
	print qq ~<script>location.href="$boardurl/$thisprog?forum=$inforum";</script>~;
	exit;
    }
    &error("进入论坛&你不允许进入该论坛！");
}

if ($action eq "resetposts") {
    $currenttime = time;
    $currenttime = $currenttime+10;
    $mv=1;
    &setlastvisit("$inforum,$currenttime");
}
$currenttime = time;

$inthreadages     = $query->cookie("threadages") if (($query->cookie("threadages"))&&($inthreadages eq ""));
$defaulforumcshow = "orderlastpostd"  if ($defaulforumcshow eq "");
$inthreadages     = $defaulttopicshow if ($inthreadages eq "");
$inorder          = $defaulforumcshow if ($inorder eq "");
$inthreadages     = "all" if (($inorder ne "")&&($inorder ne "orderlastpostd"));

print header(-cookie=>[$allowforumcookie, $onlineviewcookie, $tempvisitcookie, $permvisitcookie], -charset=>gb2312);
#, -expires=>'now'

&forumjump;

	if ($jumpto) { print redirect(-location=>"$jumpto"); exit; }

        if (($privateforum eq "yes")||($xzbopen eq "no")||($startnewthreads eq "no")){
       	    $newthreadbutton3 = "";
        } else {
            $newthreadbutton3 = qq~<a href=$xzbprog?action=new&forum=$inforum><img src=$imagesurl/images/$newxzblogo border=0 alt=张贴一个小字报 width=99 height=25></a>　~;
        }

        if ($pollopen eq "no") {
            $newthreadbutton2 = "";
        }
        else {
            $newthreadbutton2 = qq~<a href=$pollprog?action=new&forum=$inforum><img src=$imagesurl/images/$newpolllogo border=0 alt=开启一个新投票 width=99 height=25></a>　~;
        }

        if ($postopen eq "no") {
            $newthreadbutton1 = "";
        }
        else {
            $newthreadbutton1 = qq~<a href=$postprog?action=new&forum=$inforum><img src=$imagesurl/images/$newthreadlogo border=0 alt=发表一个新主题 width=99 height=25></a>　~;
        }

        $newthreadbutton = "$newthreadbutton1$newthreadbutton2$newthreadbutton3";
        undef $newthreadbutton1; undef $newthreadbutton2; undef $newthreadbutton3;

        if ($forumgraphic) {
             $forumgraphic = qq~<a href=$forumsprog?forum=$inforum><img src=$imagesurl/images/$forumgraphic border=0></a>~;
        }
        else { $forumgraphic = qq~<a href=$forumsprog?forum=$inforum><img src=$imagesurl/images/$boardlogo border=0></a>~; }

        &moderator;
        &title;
	&threadage;
        if ($sortalltopic ne "no") { &orderpage; $orderdisplyed = qq~<td align=right width=140><p>$orderdisplyed</P></td>~; }

	$insidead    = "" if ($forumimagead  eq "0");
	$insidead1   = "" if ($forumimagead1 eq "0");

	$midiabsaddr = "$imagesdir" . "midi/$midiaddr";
	$output .= qq~<BGSOUND SRC=$imagesurl/midi/$midiaddr LOOP=-1>~ if ((-e "$midiabsaddr")&&($midiaddr ne ""));

$output .= qq~
<style>
TABLE {BORDER-TOP: 0px; BORDER-LEFT: 0px; BORDER-BOTTOM: 1px; }
TD {BORDER-RIGHT: 0px; BORDER-TOP: 0px; color: $fontcolormisc; }
.ha {color: $fonthighlight; font: bold;}
.hb {color: $menufontcolor; font: bold;}
.dp {padding: 4px 0px;}
</style>
<script language="javascript">
function O1(id) {window.open("topic.cgi?forum=$inforum&topic="+id);}
function O2(id) {window.open("view.cgi?forum=$inforum&topic="+id);}
function O3(id1,id2) {window.open("$threadprog?forum=$inforum&topic="+id1+"&start="+id2+"&replynum=last#end","_self");}
function O9(id) {window.open("$profileprog?action=show&member="+id);}
</script>
$insidead$insidead1
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
<tr><td width=30% rowspan=2 valign=top>$forumgraphic</td>
<td valign=top>
~;

if ($indexforum ne "no"){
    $output .= qq~
<font color=$fontcolormisc>
　<img src=$imagesurl/images/closedfold.gif width=14 height=14>　<a href=$forumsummaryprog>$boardname</a><br>
　<img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=14 height=14>　$forumname
~;
}

$output .= qq~</td></tr>$uservisitdata</tr></table><br>~;

    if ($privateforum eq "yes"){
        $tempaccess = "forumsallowed". "$inforum";
        $testentry = cookie($tempaccess);
        if ((($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
	    if ($inpassword ne $password) {&error("进入论坛&你不允许进入该论坛！");}
        } else {&accessneeded; }
    }

$catbacks = "background=$imagesurl/images/$catbackpic";

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") { &whosonline("$inmembername\t$forumname\tnone\t查看论坛上的主题\t"); } else { &whosonline("$inmembername\t$forumname(密)\tnone\t查看保密论坛上的主题\t"); }
    &getonline("$forumname");

}
else {
    $memberoutput = "";
    $membertongji = " <B>由于服务器繁忙，所以本分论坛的在线数据暂时不提供显示。</B>";
    $onlinetitle = "";
}

if ($ratings ne "") { $ratings = qq~<td bgcolor=$titlecolor width=27 align=center $catbacks><font color=$titlefontcolor><b>评</b></td>~;}

if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")){
$mutdelete = qq~<td bgcolor=$titlecolor width=27 align=center $catbacks><font color=$titlefontcolor><b>删</b></td>~;
$mutdel=qq~<td><input type="button" name="chkall" value="全选" onclick="CheckAll(this.form)"><input type="button" name="clear2" value="反选" onclick="FanAll(this.form)"><input type="reset" name="Reset" value="重置"><input type="submit" name="delete" value="删除" ></td>~;
$mutdeletejs = qq~<script language="JavaScript">
function CheckAll(form){for (var i=0;i<form.elements.length;i++){var e = form.elements[i];e.checked = true;}}
function FanAll(form){for (var i=0;i<form.elements.length;i++){var e = form.elements[i];if (e.checked == true){ e.checked = false; }else { e.checked = true;}}}
</script>
~;
} else { $mutdelete=""; $mutdeletejs =""; $mutdel= "";}

    $modoutput = "<B>本论坛版主暂时空缺&nbsp;</B>" if (!$modoutput);
    if ($announcements eq 'yes') {
        $filetoopen = "$lbdir" . "data/news$inforum.cgi";
        if (open(FILE, "$filetoopen")) {
           @announcementdata = <FILE>;
           close(FILE);
           $totalannouncements = @announcementdata;
           if ($totalannouncements eq 0) { $dateposted = time; $title = "当前没有公告"; }
           else { ($title, $dateposted, $trash) = split(/\t/, $announcementdata[0]); }
	   undef @announcementdata;
        }
        else { $dateposted = time; $title = "当前没有公告"; }

        $dateposted = $dateposted + $addtimes;
        $dateposted = &longdate("$dateposted");
        if (($totalannouncements ne "")&&($totalannouncements ne 0)) { $announcetemp1=qq~<img src=$imagesurl/images/announce.gif alt="本分论坛的公告！共 $totalannouncements 条！" width=18 height=18>~; }
        else { $announcetemp1=qq~<img src=$imagesurl/images/announce.gif alt="本分论坛暂时无公告！" width=18 height=18>~; }

	if ($announcemove eq "on") {
	    $announcetemp2=qq~<marquee scrollamount=3><b><a href=$boardurl/$announceprog?forum=$inforum target=_blank>$title</a></b>　[$dateposted]</marquee>~;
	} else {
            $titletemp = &lbhz($title,25);
	    $announcetemp2=qq~<b><a href=$boardurl/$announceprog?forum=$inforum target=_blank title="$title">$titletemp</a></b>　[$dateposted]~;
	}
    }
    
$output .= qq~
<SCRIPT FOR=forum EVENT=onclick>a();</SCRIPT>
<table cellpadding=1 cellspacing=0 width=$tablewidth align=center>
<tr><td align=center width=2></td><td align=center width=34>$announcetemp1</td><td width=* align=left>$announcetemp2</td><td align=right width=400><p>$daysold</p></td><td align=center width=4></td>
</tr></table>
<SCRIPT LANGUAGE="JavaScript">
function a(){el=event.srcElement;if (el.tagName=='A') el.target=(globalTarget.value);}
function setVMcookie(vtype){var expDays = 30;var exp = new Date();exp.setTime(exp.getTime() + (expDays*24*60*60*1000));SetCookie('viewMode',vtype,exp);}
function JM_setTarget(){globalTarget.value=(globalTarget.value=='_blank')?'':'_blank';globalTarget.children[0].src=(globalTarget.value=='')?'$imagesurl/images/$wlogo':'$imagesurl/images/$nwlogo';setVMcookie(globalTarget.value);}
function initViewMode(){viewMode=GetCookie('viewMode');globalTarget.value=(!viewMode)?'':'_blank';globalTarget.children[0].src=(!viewMode)?'$imagesurl/images/$wlogo':'$imagesurl/images/$nwlogo';}
initViewMode()
</script>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor width=92%><font color=$titlefontcolor>$membertongji　 $onlinetitle</td>
<td bgcolor=$titlecolor width=8% align=center><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 width=40 height=12></a></td>
</tr>
~;

    if ($onlineview == 1){
       	$output .= qq~<tr><td colspan=2 bgcolor=$forumcolorone background=$imagesurl/images/$otherbackpic>$memberoutput</td></tr>~;
    }
    $output .= qq~</table></td></tr></table><br>~;

    if (($privateforum ne "yes")&&($xzbopen ne "no")&&($startnewthreads ne "no")){
        my $dirtoopen = "$lbdir" . "boarddata";
	$xzb="";
	if (-e "$dirtoopen/xzb$inforum.cgi"){
	    open (DIR, "<$dirtoopen/xzb$inforum.cgi");
            my @xzbdata = <DIR>;
            close (DIR);
            chomp(@xzbdata);
            if (-e "$dirtoopen/xzbs$inforum.cgi"){
        	open(DIR,"<$dirtoopen/xzbs$inforum.cgi");
        	my $xzb1=<DIR>;
        	close(DIR);
            }
            if ($xzb1 eq '') {$xzb1="0"};
            if ($xzb1>=$#xzbdata) {$xzb1=0;} else {$xzb1++;}
            $xzbdata[$xzb1] =~ s/^＃—＃—·\t//isg;
            (my $title, my $postid, my $msg, my $posttime)=split(/\t/,$xzbdata[$xzb1]);
            open(DIR,">$dirtoopen/xzbs$inforum.cgi");
            print DIR $xzb1;
            close(DIR);
            if ($title ne ""){
        	my $vpostid = $postid;
        	$vpostid =~ s/ /\_/isg;
		$vpostid =~ tr/A-Z/a-z/;
        	my $titletemps = &lbhz($title,35);
        	$xzb = qq~&nbsp;小字报: <img src=$imagesurl/images/icon.gif width=14 height=12> <a href="javascript:openScript('$xzbprog?action=view&forum=$inforum&id=$xzb1',420,320)" title="$title"><font color=blue>$titletemps</font></a> -- <a href=javascript:O9('$vpostid')>$postid</a>~;
            }
        }
    }

if (($inmembername ne "")&&($inmembername ne "客人")){ $fav=qq~<img src=$imagesurl/images/icon.gif width=14 height=12> <a href=fav.cgi?action=show&member=$inmembername>个人收藏</a>&nbsp;~; }
if ($startnewthreads ne "no"){ $jinghua=qq~<img src=$imagesurl/images/icon.gif width=14 height=12> <a href=jinghua.cgi?action=list&forum=$inforum><font color=$fonthighlight>本版精华</font></a>　~; }
unless ($look eq "off"){ $lookstyles=qq~<img src=$imagesurl/images/icon.gif width=14 height=12> <a href=lookstyles.cgi?forum=$inforum>本版配色</a>&nbsp;~; }

if ($refreshforum eq "on") {
    my $autofreshtime = 300 if ($autofreshtime < 3);
    my $refreshnow = qq~<meta http-equiv="refresh" content="$autofreshtime;">~;
}

my $freshtime= $query->cookie("freshtime");
if ($freshtime ne "") {
    my $autofreshtime = $freshtime*60-1;
    $autofreshtime = 300 if ($autofreshtime < 3);
    my $refreshnow = qq~<meta http-equiv="refresh" content="$autofreshtime;">~;
}

$output .= qq~

$mutdeletejs
$refreshnow
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
<tr><td align=center width=2></td><td>$newthreadbutton</td><td align=right colspan=2>$modoutput&nbsp</td></form>
</tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center><tr><td>$xzb</td><td align=right width=*>$jinghua$fav$lookstyles</td>$orderdisplyed<td align=center width=4></td></tr></table>
<table cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<form action="$postingsprog" method=post>
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="action" value="delete">
<tr><td height=1></td></tr></table><center>
<table cellpadding=0 cellspacing=0 width=$tablewidth height=24 bordercolor=$tablebordercolor border=1>
<tr><td bgcolor=$titlecolor width=32 align=center $catbacks><font color=$titlefontcolor><b>状态</b></td>
<td bgcolor=$titlecolor width=* align=center $catbacks><font color=$titlefontcolor><b>主　题</b> (点心情符为新闻方式阅读)</td>
<td bgcolor=$titlecolor align=center width=80 $catbacks><font color=$titlefontcolor><b>作 者</b></td>
<td bgcolor=$titlecolor align=center width=32 $catbacks><font color=$titlefontcolor><b>回复</b></td>
<td bgcolor=$titlecolor align=center width=32 $catbacks><font color=$titlefontcolor><b>点击</b></td>
<td bgcolor=$titlecolor width=195 align=center $catbacks><font color=$titlefontcolor><b>　 最后更新 　 | 最后回复人</b></td>
$ratings$mutdelete</tr></table>
~;
###########################htc
    $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
    if (-e $filetoopen) {
    	&winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @topics = <FILE>;
        close(FILE);
        &winunlock($filetoopen);
    }
    else { &error("打开论坛&对不起，这个论坛不存在！如果确定分论坛号码没错，那么请进入管理区修复论坛一次！"); }

    $numberofitems = @topics;

      if (($inorder ne "")&&($inorder ne "orderlastpostd")) {
	if ($inorder eq "orderlastposta") {
	  @topics = reverse(@topics);
	}
	else {
	  undef @toptopic;
          foreach my $topic (@topics) {
	    chomp $topic;
            (my $topicid,my $topictitle,my $no, $no,my $threadposts,my $threadviews,my $startedby,my $startedpostdate, $no,my $lastpostdate, $no, $no) = split(/\t/,$topic);
 	    $topictitle =~ s/^＊＃！＆＊//;
	    next if (($topicid eq "")||($topicid !~ /^[0-9]+$/));
	    $threadviews = sprintf("%04d",$threadviews);
	    $threadposts = sprintf("%04d",$threadposts);
	    $ordername = $startedpostdate if (($inorder eq "orderthreadd")||($inorder eq "orderthreada"));
	    $ordername = $startedby if (($inorder eq "orderstartbyd")||($inorder eq "orderstartbya"));
	    $ordername = $threadviews if (($inorder eq "orderclickd")||($inorder eq "orderclicka"));
	    $ordername = $threadposts if (($inorder eq "orderreplyd")||($inorder eq "orderreplya"));
	    $ordername = $topictitle if (($inorder eq "ordertitled")||($inorder eq "ordertitlea"));
	    $additem = "$ordername|$topic";
            push (@toptopic, $additem);
	  }
	  if (($inorder eq "orderthreadd")||($inorder eq "orderthreada")) {
	  	@toptopic = sort({$a<=>$b}@toptopic);
	  }
	  else { @toptopic = sort(@toptopic); }

	  @toptopic = reverse(@toptopic) if ($inorder =~ m/d$/);
	  undef @topics;
          foreach my $topic (@toptopic) {
          	(my $no,my $additem) = split(/\|/,$topic);
                push (@topics, $additem);
	  }
	  undef @toptopic;
	}
      }

    if ($inthreadages && ($inthreadages ne "all")) {
	my $threadagelimit = $currenttime - ($inthreadages * 86400);

	my $forumtop = 0 ;
	my $forumbottom = $numberofitems - 1;

	while ($forumbottom > $forumtop +1) {
	    my $linenow = int(($forumbottom + $forumtop)/2);
	    my $topic = @topics[$linenow];
	    chomp $topic;
	    (my $no, $no, $no, $no, $no, $no, $no, $no, $no, $lastpostdate, $no, $no) = split(/\t/,$topic);
	    if ($lastpostdate > $threadagelimit) { $forumtop = $linenow; }
	    else { $forumbottom = $linenow; }
	}
        $numberofitems = $forumbottom+1;
    }

    $numberofpages = $numberofitems / $maxthreads;

    if ($numberofitems > $maxthreads) {
        $showmore = "yes";
        if ($inshow eq "" || $inshow < 0) { $inshow = 0; }
        if ($inshow > 0) { $startarray = $inshow; }
        else { $startarray = 0; }
        $endarray = $inshow + $maxthreads - 1;
        if ($endarray < ($numberofitems - 1)) { $more = "yes"; }
        elsif (($endarray > ($maxthreads - 1)) && ($more ne "yes")) { $endarray = $numberofitems -1; }
    }
    else {
        $showmore = "no";
        $startarray = 0;
        $topicpages = qq~<font color=$menufontcolor>本论坛只有一页</font>~;
        $endarray = $numberofitems -1;
    }
    if (($inthreadages)&&($inthreadages ne "all")) {
	$threadagesstart = "&threadages=$inthreadages";
    }
    else {undef $threadagesstart;}
    if (($inorder)&&($inorder ne "orderlastpostd")) {
	$orderstart = "&order=$inorder";
    }
    else {undef $orderstart;}
    if ($showmore eq "yes") {
	if ($maxthreads < $numberofitems) {
	    ($integer,$decimal) = split(/\./,$numberofpages);
	    if ($decimal > 0) { $numberofpages = $integer + 1; }
	    $mypages=$numberofpages;
	    #分页
	    $intshow=$inshow/(12*$maxthreads);
	    ($intshow,$mydecimal) = split(/\./,$intshow);
	    $intshow = $intshow + 1;
	    $preshow=($intshow-1)*12*$maxthreads-$maxthreads;
	    $nextshow=$intshow*12*$maxthreads;
	    $pages=qq~<a href=$thisprog?forum=$inforum&show=$preshow$threadagesstart$orderstart class=hb>←</a> ~ if ($intshow > 1);
	    if ($numberofpages > ($intshow*12)){
		$numberofpages=($intshow*12);
		$isnext=qq~<a href=$thisprog?forum=$inforum&show=$nextshow$threadagesstart$orderstart class=hb>→</a> ~;
	    }
	    $pagestart = ($intshow-1)*12*$maxthreads;
            $counter = ($intshow-1)*12;
            while ($numberofpages > $counter) {
		$counter++;
		if ($inshow ne $pagestart) { $pages .= qq~<a href=$thisprog?forum=$inforum&show=$pagestart$threadagesstart$orderstart class=hb>$counter</a> ~; }
		else { $pages .= qq~<font color=$fonthighlight><b>$counter</b></font> ~; }
		$pagestart = $pagestart + $maxthreads;
	    }
	    $pages .=  $isnext;
	    #分页end
	}
	$topicpages = qq~<font color=$menufontcolor><b>本论坛共有 <font color=$fonthighlight>$mypages</font> 页</b> [ $pages ]~;
    }
$icon_num = int(rand(10));
$topcount = 0;
    $filetoopen = "$lbdir" . "boarddata/ontop$inforum.cgi";
    if (-e $filetoopen) {
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @ontop = <FILE>;
        close(FILE);
    }
    else { undef @ontop; }
    $topcount = @ontop;

  if (($topcount > 0)&&($startarray eq 0)) {
    foreach $id (@ontop) {
      	chomp $id;
      	if ($id eq "") {
      	    $topcount --;
      	    next;
      	}
	my $file = "$lbdir" . "forum$inforum/$id.pl";
	open (TMP, "$file");
	(my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $lastpostdate, my $posticon1,my $inposttemp) = split (/\t/,<TMP>);
        $topictitle =~ s/^＊＃！＆＊//;
	close (TMP);


	if (($topictitle eq "")||($startedby eq "")||($startedpostdate eq "")||($threadposts eq "")){
	  my $file1 = "$lbdir" . "forum$inforum/$id.thd.cgi";
	  open (TMP1, "$file1");
	  my @tmp = <TMP1>;
	  close (TMP);


	  my $tmp = @tmp;
	  $tmp --;
	  my $tmp1 = $tmp[-1];
	  my $tmp2 = $tmp[0];
	  (my $membername, $topictitle, my $postipaddress, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/,$tmp2);
	  (my $membername1, my $topictitle1, my $postipaddress1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, $posticon1) = split(/\t/,$tmp1);
 	  $topictitle =~ s/^＊＃！＆＊//;
 	  $topictitle1 =~ s/^＊＃！＆＊//;
	  $membername1 = "" if ($tmp eq 0);
	  $threadviews = ($tmp+1) * 8;
	  $postdate1 = $lastpostdate if ($lastpostdate ne "");
	  $inposttemp = $post1;
	  $inposttemp =~ s/\[这个贴子最后由(.+?)编辑\]\n//isg;
	  $inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	  $inposttemp =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]//isg;
	  $inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2\n/isg;
	  $maxsmailtemp = $maxsmail;
	  $maxsmail     = 0;
	  $inposttemp = &doemoticons("$inposttemp");
 	  $maxsmail     = $maxsmailtemp;
	  $inposttemp =~ s/ \<img\s*(.*?)\s*\>//isg;
	  $inposttemp =~ s/\n//isg;
	  $inposttemp =~ s/( )+$//isg;
	  $inposttemp =~ s/^( )+//isg;
	  $inposttemp =~ s/<(.|\n)+?>//g;

	  $posticon1 = "<br>" if ($posticon =~/<br>/i);

          $inposttemp=&lbhz("$inposttemp",$maxsavepost);
	  $rr = ("$id\t$topictitle\t$topicdescription\t$threadstate\t$tmp\t$threadviews\t$membername\t$postdate\t$membername1\t$postdate1\t$posticon1\t$inposttemp\t\n");
        } else {
   	  $threadviews = ($tmp+1) * 8 if ($threadviews eq "");
 	  $threadviews = 9999 if ($threadviews >= 10000);
          $rr = ("$id\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon1\t$inposttemp\t\n");
	}
	if ($topictitle ne "") {push (@toptopic, $rr);} else {$topcount --;}
    }
  }
  else { undef @toptopic; }

            $dirtoopen2 = "$imagesdir" . "usr/$inforum";
            opendir (DIR, "$dirtoopen2");
            my @dirdata2 = readdir(DIR);
            closedir (DIR);

        foreach (@topics[$startarray ... $endarray]) {
            push (@toptopic, $_);
	}
	$topiccount = 0;
        foreach $topic (@toptopic) {
	    chomp $topic;
            ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp) = split(/\t/,$topic);

       	    $topcomp = 0;
       	    if (($topiccount >= $topcount)||($startarray ne 0)) {
              foreach $ontop (@ontop) {
            	chomp $ontop;
            	if ($topicid eq $ontop) {
            	    $topcomp = 1;
            	    last;
            	}
              }
	    }
            next if ($topcomp == 1);

	    next if (($topicid eq "")||($topicid !~ /^[0-9]+$/));

            if ($posticon ne "") {
            	$poll=0;
            	if ($posticon =~/<br>/i){
                    $posticon = int(rand(23));
    		    $posticon = "0$posticon" if ($posticon<10);
		    $posticon = qq~<img src=$imagesurl/posticons/$posticon.gif $defaultsmilewidth $defaultsmileheight border=0 align=absmiddle>~;
            	}
            	else{
            	    my $posticonfile = $imagesdir . "posticons/$posticon";
            	    if (!(-e $posticonfile)) {
                    	$posticon = int(rand(23));
    		    	$posticon = "0$posticon" if ($posticon<10);
    		    	$posticon = $posticon . ".gif";
		    }
            	    $posticon = qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight border=0 align=absmiddle>~;
            	}
            }
	    else {
    		$posticon = int(rand(23));
    		$posticon = "0$posticon" if ($posticon<10);
		$posticon = qq~<img src=$imagesurl/posticons/$posticon.gif $defaultsmilewidth $defaultsmileheight border=0 align=absmiddle>~;
	    }
	    if ($badwords) {
		@pairs = split(/\&/,$badwords);
		foreach (@pairs) {
		    ($bad, $good) = split(/=/,$_);
		    chomp $good;
		    $topictitle =~ s/$bad/$good/isg;
		}
	    }
	    $lastpostdatetemp=$lastpostdate;

	    $lastpostdate=$lastpostdatetemp;
            $numberofitems = $threadposts + 1;
            $numberofpages = $numberofitems / $maxtopics;
	    $counter = 0;
	    $hasshow=0;
            if ($numberofitems > $maxtopics) {
		if ($maxtopics < $numberofitems) {
		    ($integer,$decimal) = split(/\./,$numberofpages);
		    if ($decimal > 0) { $numberofpages = $integer + 1; }
		    $pagestart = 0;
		    while ($numberofpages > $counter) {
			$counter++;
	        	$gotoendpost = "$pagestart";
			if (($counter<5)||($counter>$numberofpages-4))
			{
				$threadpages .= qq~<a href=$threadprog?forum=$inforum&topic=$topicid&start=$pagestart&show=$inshow class=ha>$counter</a> ~;
			}else{
			$threadpages .="\. " if ($hasshow<3);
			$hasshow++;
			}
			$pagestart = $pagestart + $maxtopics;
		    }
		}
		$pagestoshow = qq~<font color=$forumfontcolor>　　[第 $threadpages 页]</font>~;
	    }
	    else {
	        $gotoendpost = "0";
	    }

            if ($inthreadages && ($inthreadages ne "all")&&(($topiccount >= $topcount)||($startarray ne 0))) {
		$threadagelimit = $currenttime - ($inthreadages * 86400);
		if ($lastpostdate < $threadagelimit) { last; }
	    }
	    if (!$forumlastvisit) { $forumlastvisit = "0"; }

            if ($startedpostdate > $currenttime - 3600 * $newmarktime) {
		$topnew = " <img src=$imagesurl/images/$new_blogo absmiddle>";$addonlength +=2;
 	    }
 	    else {$topnew = "";}

	    $topicicon = "<img src=$imagesurl/images/topicnonew.gif width=14 border=0>";

	    if (($threadposts >= $hottopicmark) && ($forumlastvisit < $lastpostdate) && ($inmembername ne "客人")) {
		$topicicon = "<img src=$imagesurl/images/topichot$icon_num.gif width=14 border=0>";
	    }
	    if (($threadposts >= $hottopicmark) && ($forumlastvisit > $lastpostdate) && ($inmembername ne "客人")) {
		$topicicon = "<img src=$imagesurl/images/topichotnonew.gif width=14 border=0>";
	    }
	    if (($threadposts < $hottopicmark) && ($forumlastvisit < $lastpostdate) && ($inmembername ne "客人")) {
		$topicicon = "<img src=$imagesurl/images/topicnew$icon_num.gif width=14 border=0>";
 	    }
	    if (($threadposts < $hottopicmark) && ($forumlastvisit > $lastpostdate) && ($inmembername ne "客人")) {
		$topicicon = "<img src=$imagesurl/images/topicnonew.gif width=14 border=0>";
	    }

	    $threadstate = "poll" if (($posticon =~/<br>/i)&&($threadstate eq ""));
	    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) {
		$filetomake = "$lbdir" . "forum$inforum/$topicid.poll.cgi";
		if (-e $filetomake) {
            	   open(FILE, "$filetomake");
            	   flock(FILE, 1) if ($OS_USED eq "Unix");
            	   my @allpoll = <FILE>;
            	   close(FILE);
	    	   $size = 0;
	    	   foreach (@allpoll) {
	    	   	chomp $_;
	    	   	$size ++ if ($_ ne "");
	    	   }
            	}
            	else {
            	    $size = 0;
            	}
	    }
	    if ($threadstate eq "closed") {
		$topicicon = "<img src=$imagesurl/images/topiclocked$icon_num.gif width=14 border=0>";
	    }
	    elsif ($threadstate eq "poll") {
	        if ($size >= $hotpollmark) {
		    $topicicon = "<img src=$imagesurl/images/closedbhot.gif width=13 border=0>";
	        }
		else {
		    $topicicon = "<img src=$imagesurl/images/closedb.gif width=13 border=0>";
		}
	    }
	    elsif ($threadstate eq "pollclosed") {
		$topicicon = "<img src=$imagesurl/images/closedb1.gif width=13 border=0>";
	    }

	    if ($lastpostdate ne "") {
		$lastpostdate = $lastpostdate + $addtimes;
		$longdate = &dateformatshort("$lastpostdate");
		$lastpostdate = qq~$longdate~;
	    }
	    else {
		$lastpostdate = qq~没有~;
		$lastpoststamp = "";
	    }
	    $startedpostdate = $startedpostdate + $addtimes;
	    $startedlongdate = &shortdate("$startedpostdate");
	    $startedshorttime = &shorttime("$startedpostdate");
	    $startedpostdate = qq~$startedlongdate $startedshorttime~;
	    if (($screenmode >=9)||($tablewidth > 770)) {
	    	$topictitlemax = 80;
	    }
	    else {$topictitlemax = 48;}

	    $posttemp = "(无内容)" if ($posttemp eq "");
	    $topictitletemp = &lbhz($topictitle,$topictitlemax);
	    $topictitle = qq~<a href=$threadprog?forum=$inforum&topic=$topicid&show=$inshow TITLE="最后回复摘要：\n\n$posttemp">$topictitletemp</a>~;
	    $startedbyfilename = $startedby;
	    $startedbyfilename =~ s/ /\_/isg;
	    $startedbyfilename =~ tr/A-Z/a-z/;

	    if ($lastposter) {
		$lastposterfilename = $lastposter;
		$lastposterfilename =~ s/ /\_/isg;
		if ($lastposter=~/\(客\)/) {
            	    $lastposter=~s/\(客\)//isg;
		    $lastposter = qq~<font color=$postfontcolorone title="此为未注册用户">$lastposter</font>~;
		}
		else {
		    $lastposter = qq~<a href=javascript:O9('$lastposterfilename')>$lastposter</a>~;
		}
	    }
	    else {$lastposter = qq~--------~;}

	    $topicdescriptiontemp = $topicdescription;

	    $topicdescriptiontemp =~s/\s*(.*?)\s*\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/$3/isg;
	    $topicdescriptiontemp =~s/\<\/a\>//isg;

	    if (length($topicdescriptiontemp) > ($topictitlemax-4)) {
		$topicdescriptiontemp=&lbhz("$topicdescriptiontemp",$topictitlemax);
		$topicdescription =~s/\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/\<a $1\>$topicdescriptiontemp\<\/a\>/isg;
	    }

	    if ($topicdescription) { $topicdescription = qq~<br>　　-=> $topicdescription~; }
	    if (-e "${lbdir}forum$inforum/rate$topicid.file.pl") {
		require "${lbdir}forum$inforum/rate$topicid.file.pl";
		$average = int($rates / $votes);
	        if ($average > 0) {$ratestar =  qq(<img src=$imagesurl/images/1star.gif width=14 alt=太差了>);}
	        if ($average > 1) {$ratestar =  qq(<img src=$imagesurl/images/2star.gif width=14 alt=有点差>);}
	        if ($average > 2) {$ratestar =  qq(<img src=$imagesurl/images/3star.gif width=14 alt=一般性>);}
	        if ($average > 3) {$ratestar =  qq(<img src=$imagesurl/images/4star.gif width=14 alt=挺不错>);}
	        if ($average > 4) {$ratestar =  qq(<img src=$imagesurl/images/5star.gif width=14 alt=特别好>);}
	    } else {
	        $ratestar =  qq(<img src=$imagesurl/images/norate.gif width=0 height=0 alt="没有投票评分记录">);
	    }

	    $addonlength=0;

	    if ($ratings eq "") { $ratings2 = ""; }
	    else  { $ratings2 = qq~<td bgcolor=$forumcolortwo align=center width=25>$ratestar</td>~; $addonlength += 2.5; }

	    if ($mutdelete eq "") { $mutdelete2 = ""; }
	    else  { $mutdelete2 = qq~<td bgcolor=$forumcolortwo align=center width=25><input type=checkbox name=topic value=$topicid></td>~; $addonlength += 2.5; }

            my @files = grep(/^$inforum\_$topicid\./,@dirdata2);
            my $files1 = @files;
	    if ($files1 > 0) {
              my $files1s = $files[0]; chomp $files1s;
              ($up_name, $up_ext) = split(/\./,$files1s);
              $up_ext =~ tr/A-Z/a-z/;
              $filetype = "unknow";
              $filetype = $up_ext if (-e "${imagesdir}icons/$up_ext.gif");
              if (($up_ext eq 'jpg')||($up_ext eq 'gif')||($up_ext eq 'bmp')||($up_ext eq 'png')) {$topictitle ="<a href=$imagesurl/usr/$inforum/$inforum\_$topicid.$up_ext target=_blank><img src=$imagesurl/icons/$filetype.gif width=16 height=16 alt=\"该主题有一张 $filetype 格式图片，点击观看\" border=0 align=absmiddle></a> ".$topictitle;}
              else {$topictitle ="<a href=$imagesurl/usr/$inforum/$inforum\_$topicid.$up_ext target=_blank><img src=$imagesurl/icons/$filetype.gif width=16 height=16 align=absmiddle alt=\"该主题有一个“$filetype”类型附件，点击下载\" border=0></a> ".$topictitle;}
              $addonlength += 4;
            }
            
            my @files = grep(/^$inforum\_$topicid\_/,@dirdata2);
            my $files1 = @files;
	    if ($files1 > 0) {
                 $topictitle=$topictitle." <img src=$imagesurl/icons/replyattachment.gif width=16 height=16 align=absmiddle alt=\"该主题内的回复中含有图形或附件\">";
                 $addonlength += 3;
	    }

	    if ($counter == 0) { $pagestoshowtemp1 = 0; }
	    if ($counter > 11)  { $counter = 11; }
	    else { $pagestoshowtemp1 =7;}
	    $totlelength = $counter*3.3 + $pagestoshowtemp1 + length($topictitletemp) + 3 + $addonlength; #标题栏的总长度
	    undef $pagestoshowtemp1;

	    if (($membercode eq "ad") || ($inmembmod eq "yes") || ($membercode eq 'smo')) {
		$admini = qq~<DIV ALIGN=Right><font color=$titlecolor>|<a href=jinghua.cgi?action=add&forum=$inforum&topic=$topicid><font color=$titlecolor>精</font></a>|<a href=$postingsprog?action=locktop&forum=$inforum&topic=$topicid><font color=$titlecolor>固</font></a>|<a href=$postingsprog?action=puttop&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>提</font></a>|<a href=$postingsprog?action=lock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>锁</font></a>|<a href=$postingsprog?action=unlock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|<a href=$postingsprog?action=delete&forum=$inforum&topic=$topicid><font color=$titlecolor>删</font></a>|<a href=$postingsprog?action=movetopic&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>移</font></a>|</font>&nbsp;</DIV>~;
            }
            elsif ((lc($inmembername) eq lc($startedby)) && ($inpassword eq $password)) {
	      if ($arrowuserdel eq "on") {
		$admini = qq~<DIV ALIGN=Right><font color=$titlecolor>| <a href=$postingsprog?action=lock&forum=$inforum&topic=$topicid><font color=$titlecolor>锁定此贴，不允许别人回复</font></a> | <a href=$postingsprog?action=delete&forum=$inforum&topic=$topicid><font color=$titlecolor>删除此贴</font></a> |</font>&nbsp;&nbsp;</DIV>~;
	      }
	      else { undef $admini; }
            }
            else { undef $admini; }

      	    if (($topiccount < $topcount)&&($startarray eq 0)) {
      	    	if (($membercode eq "ad") || ($inmembmod eq "yes") || ($membercode eq 'smo')) {
		    $admini = qq~<DIV ALIGN=Right><font color=$titlecolor>|<a href=$postingsprog?action=unlocktop&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>消</font></a>|<a href=$postingsprog?action=locktop&forum=$inforum&topic=$topicid><font color=$titlecolor>顶</font></a>|<a href=jinghua.cgi?action=add&forum=$inforum&topic=$topicid><font color=$titlecolor>精</font></a>|<a href=$postingsprog?action=lock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>锁</font></a>|<a href=$postingsprog?action=unlock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|<a href=$postingsprog?action=delete&forum=$inforum&topic=$topicid><font color=$titlecolor>删</font></a>|</font>&nbsp;</DIV>~;
      	    	}
                else { undef $admini; }
                $topicicon = "<img src=$imagesurl/images/locktop.gif width=15 border=0>";
	    }
	    $topictitle .= $topnew;
	    $topictitle=$topictitle."<BR>" if ($totlelength > $topictitlemax+5);

	    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) {
            	$outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=63 rowspan=2><ACRONYM TITLE="回复数：$threadposts， 点击数：$threadviews">共 $size 票</ACRONYM></font></td>~;
	    }
	    else {
            	$outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=30>$threadposts</font></td><td bgcolor=$forumcolortwo align=center width=30>$threadviews</a></font></td>~;
	    }
	    if ($startedby=~/\(客\)/) {
            	$startedby=~s/\(客\)//isg;
	        $startedby=qq~<font color=$postfontcolorone title="此为未注册用户">$startedby</font>~;
	    }
	    else {
	        $startedby=qq~<a href=javascript:O9('$startedbyfilename')>$startedby</a>~;
	    }
	    $output .=qq~<table cellspacing=0 width=$tablewidth bordercolor=$tablebordercolor border=1>
<tr><td align=center width=30 bgcolor=$forumcolorone><a href=javascript:O1($topicid)>$topicicon</a></td>
<td width=* class=dp bgColor=$forumcolortwo onmouseover="this.bgColor='$forumcolorone';" onmouseout="this.bgColor='$forumcolortwo';">&nbsp;<a href=javascript:O2($topicid)>$posticon</a>&nbsp;<span id=forum>$topictitle$pagestoshow$topicdescription$admini</span></td>
<td align=center width=78 bgcolor=$forumcolorone title="发布时间： $startedpostdate">$startedby</td>$outputtemp
<td width=193 bgcolor=$forumcolorone>&nbsp;<a href=javascript:O3($topicid,$gotoendpost)>$lastpostdate</a><font color=$fonthighlight> | </font>$lastposter</td>
$ratings2$mutdelete2</tr></table>
~;
	    $pagestoshow = undef;
	    $threadpages = undef;
	    $topiccount++;
	}
        $output .= qq~</tr></table></td></tr></table><table cellpadding=0 cellspacing=2 width=$tablewidth align=center><tr height=4></tr><tr><td>$topicpages　&nbsp;~;
        $output .= qq~<BR>~ unless (($screenmode >=9)||($tablewidth > 770));
        $output .= qq~[主题 <B>$threads</B> 篇，回复 <b>$posts</b> 篇]</td>$mutdel</form>~;

####################htc

if ($indexforum ne "no") { $output .= qq~<td align=right>$jumphtml</td></form>~; }

$output .= qq~</tr></table></tr></table><br>~;

if ($membercode eq "ad" || $inmembmod eq "yes" || $membercode eq 'smo') {
    $deltopicmore1 = qq~论坛选项~;
    $deltopicmore2 = qq~<img src=$imagesurl/images/adminlock.gif width=12 height=15> <a href=$forumoptionsprog?action=prune&forum=$inforum>批量删除文章</a>~;
    $deltopicmore3 = qq~<img src=$imagesurl/images/adminlock.gif width=12 height=15> <a href=$postingsprog?action=repireforum&forum=$inforum>修复这个论坛</a>~;
}
else { undef $deltopicmore1; undef $deltopicmore2; undef $deltopicmore3; }

if ($dispview eq "yes") {
    if ($inmembername ne "客人") {
        $output .= qq~
<table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellspacing=1 cellpadding=3 width=100%>
<tr><td width=80% bgcolor=$titlecolor><font color=$titlefontcolor><b>　-=> LB5000II 论坛图例</b></font></td>
<td noWrap bgcolor=$titlecolor width=20% align=right><font color=$titlefontcolor> 所有时间均为 - $basetimes &nbsp;</td></tr><tr><td colspan=3 bgcolor=$forumcolorone background=$imagesurl/images/$otherbackpic1>
<table cellspacing=4 cellpadding=0 width=94% align=center><tr>
<td width=20%><font color=$fonthighlight>打开的主题</font></td>
<td width=21%><font color=$fonthighlight>回复超 $hottopicmark 次的热门贴</font></td>
<td width=22%><font color=$fonthighlight>锁定贴子图标</font></td>
<td width=21%><font color=$fonthighlight>特殊贴子图标</font></td>
<td width=14%><font color=$fonthighlight>$deltopicmore1</font></td></tr><tr>
<td><img src=$imagesurl/images/topicnew$icon_num.gif width=14> 上次来之后发表</td>
<td><img src=$imagesurl/images/topichot$icon_num.gif width=14> <img src=$imagesurl/images/closedbhot.gif width=13> 上次来之后发表</td>
<td><img src=$imagesurl/images/topiclocked$icon_num.gif width=14> 关闭的主题，不接受回复</td>
<td><img src=$imagesurl/images/locktop.gif width=15> 固定顶端的主题</td>
<td>$deltopicmore2</td></tr><tr>
<td><img src=$imagesurl/images/topicnonew.gif width=14> 上次来之后无新回复</td>
<td><img src=$imagesurl/images/topichotnonew.gif width=14> 上次来之后无新回复</td>
<td><img src=$imagesurl/images/closedb1.gif width=13> 关闭的投票，不接受回复</td>
<td><img src=$imagesurl/images/closedb.gif width=13> 投票类别的主题</td>
<td>$deltopicmore3</td></tr></table></td></tr></table></td></tr></table><BR>
~;
    } else {
	$output .= qq~
<table cellspacing=0 cellpadding=0 width=$tablewidth align=center bgcolor=$tablebordercolor>
<tr><td><table cellspacing=1 cellpadding=3 width="100%"><tr>
<td width=80% bgcolor=$titlecolor><font color=$titlefontcolor><b>　-=> LB5000II 论坛图例</b></font></td>
<td noWrap bgcolor=$titlecolor width=20% align=right><font color=$titlefontcolor>所有时间均为 - $basetimes &nbsp;</td></tr><tr><td colspan=3 bgcolor=$forumcolorone background=$imagesurl/images/$otherbackpic1>
<table cellspacing=4 cellpadding=0 width=92% align=center><tr>
<td width=21%><img src=$imagesurl/images/topicnonew.gif width=14> 打开讨论的主题</td>
<td width=21%><img src=$imagesurl/images/closedb.gif width=13> 投票类别的主题</td>
<td width=28%><img src=$imagesurl/images/topiclocked$icon_num.gif width=14> <img src=$imagesurl/images/closedb1.gif width=13> 关闭了的主题，不接受回复</td>
<td width=21%><img src=$imagesurl/images/locktop.gif width=15> 固定顶端的主题</td>
</tr></table></td></tr></table></td></tr></table><BR>
~;
    }
}

$output =~ s/option value=\"$inthreadages\"/option value=\"$inthreadages\" selected/;
$output =~ s/option value=\"$inorder\"/option value=\"$inorder\" selected/;
&output( -Title   => "$forumname", -ToPrint => $output, -Version => $versionnumber );
exit;

sub accessneeded {
    $output .= qq~
<form action="$thisprog" method=post>
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="action" value="accessrequired">
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=3 cellspacing=1 width=100%>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><font color=$fontcolormisc><b>请输入您的名称、密码登陆私有论坛</b></font></td></tr>
<tr><td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc><br>每个浏览器只需要登陆一次，同时请确认你已经打开了浏览器的 Cookies 选项！<br>只有经过管理员许可的用户才可以访问该论坛，如果你不能登陆，请联系管理员！<br><br></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
<td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername">　 <a href=$registerprog><font color=$fontcolormisc>您没有注册？</font></a></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
<td bgcolor=$miscbackone><input type=password name="password" value="$inpassword">　 <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码 ?</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入论坛访问密码</font></td>
<td bgcolor=$miscbackone><input type=password name="forumpassword" value="$forumpassword">　 <font color=$fontcolormisc>如果你已经授权允许进入，则不必输入密码.</font></td></tr>
<tr height=28><td bgcolor=$miscbackone colspan=2 align=center><font color=$fontcolormisc>如果你确认输入了正确的密码，但还是无法登陆的话，请刷新此页面(或者再次按登陆键一次)。</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登  陆"></td></tr></table></td></tr></table></form>
~;
    &output( -Title   => "$forumname", -ToPrint => $output, -Version => $versionnumber );
}

sub threadage {
    $daysold = qq~
<SCRIPT LANGUAGE="JavaScript">
function threadmenu(){var URL = document.jump1.threadages.options[document.jump1.threadages.selectedIndex].value;top.location.href = "$forumsprog?forum=$inforum&order=orderlastpostd&threadages=" + URL; target = '_self';}
</SCRIPT>
<form action="$forumsprog" method=post name="jump1">
<A href=javascript:JM_setTarget() value='' id=globalTarget><img src=$imagesurl/images/$wlogo width=74 height=21 border=0 alt="查看帖子使用的模式？" align=absmiddle></a>　
<select name="threadages" onchange="threadmenu()">
<option value="all">查看所有的主题</option><option value="1">查看一天内的主题</option><option value="2">查看两天内的主题</option><option value="7">查看一星期内的主题</option><option value="15">查看半个月内的主题</option><option value="30">查看一个月内的主题</option><option value="61">查看两个月内的主题</option><option value="182">查看半年内的主题</option><option value="365">查看一年内的主题</option>
</select></form>
~;
}

sub orderpage {
    $orderdisplyed = qq~
<SCRIPT LANGUAGE="JavaScript">
function ordermenu(){var URL = document.jump2.order.options[document.jump2.order.selectedIndex].value;top.location.href = "$forumsprog?forum=$inforum&threadages=all&order=" + URL; target = '_self';}
</SCRIPT>
<form action="$forumsprog" method=post name="jump2">
<select name="order" onchange="ordermenu()">
<option value="orderlastpostd">按最后回复时间降序</option><option value="orderlastposta">按最后回复时间升序</option><option value="orderthreadd">按主题发布时间降序</option><option value="orderthreada">按主题发布时间升序</option><option value="orderstartbyd">按主题发布人降序</option><option value="orderstartbya">按主题发布人升序</option><option value="orderclickd">按主题点击数降序</option><option value="orderclicka">按主题点击数升序</option><option value="orderreplyd">按主题回复数降序</option><option value="orderreplya">按主题回复数升序</option><option value="ordertitled">按主题标题降序</option><option value="ordertitlea">按主题标题升序</option>
</select></form>
~;
}

sub getonline {
	my $where=shift;
	my $guests=0;
	my $members = 0;
	my $memberoutput1 ="　";
	my $memberoutput2 ="　";
	my $ipaddress  = $ENV{'REMOTE_ADDR'};
	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$trueipaddress = $ipaddress if (($trueipaddress eq "")||($trueipaddress eq "unknown"));
	my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$trueipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
	$screenmode=$screenmode+1;
        my $guestmode=$screenmode*2-1;
        my $totleonlineall = 0;
	foreach my $line (@onlinedata) {
	    chomp $line;
	    $line =~ s/＊＃！＆＊//;
	    (my $savedusername, my $savedcometime, my $savedtime, my $savedwhere, my $postipaddresstemp, my $saveosinfo, my $savebrowseinfo, my $savedwhere2, my $fromwhere, my $memcod, my $hiddened) = split(/\t/, $line);
		if ($memcod eq "ad") {$mspic=$onlineadmin;}
		    elsif ($memcod eq "smo") {$mspic=$onlinesmod;}
		    elsif ($memcod eq "mo")  {$mspic=$onlinemod;}
		    else  {$mspic=$onlinemember;}

	    (my $lookfor, my $no) = split(/\(/,$savedusername);
    	    next if ($lookfor =~ m/\(/);
    	    next if ($lookfor =~ m/\)/);
    	    next if ($lookfor =~ m/\*/);
   	    $totleonlineall ++;

	    unless (($pvtip eq "on")||($membercode eq "ad")||(($membercode eq 'smo')&&($smocanseeip eq "no"))) { $fromwhere = "已设置保密"; }

	    (my $savedipaddress, my $truepostipaddress) = split(/\=/,$postipaddresstemp);
            (my $ip1,my $ip2,my $ip3,my $ip4) = split(/\./,$savedipaddress);
            $pmipaddress  = $savedipaddress;
		   if ($membercode eq "ad") {
		       $savedipaddress="$ip1.$ip2.$ip3.$ip4";
		   }
		   elsif ($membercode eq "smo") {
			if ($smocanseeip eq "no") { $savedipaddress="$ip1.$ip2.$ip3.$ip4"; }
			else {
			    if ($pvtip eq "on") { $savedipaddress="$ip1.$ip2.$ip3.$ip4"; }
			    else { $savedipaddress="已设置保密"; }
			}
		   }
		   elsif ($membercode eq "mo") {
			if ($pvtip eq "on") { $savedipaddress="$ip1.$ip2.$ip3.*"; }
       			else { $savedipaddress="已设置保密"; }
		   }
		   else {
		       if (($pvtip eq "on")&&($inmembername ne "客人")) {
			 $savedipaddress="$ip1.$ip2.*.*";
		       }
       		       else { $savedipaddress="已设置保密"; }
		   }
	    $savedcometime = &dateformatshort($savedcometime + $addtimes);
	    $savedtime = &dateformatshort($savedtime + $addtimes);
	    $savedwhere2 =~s/\<a \s*(.*?)\s*\>\s*(.*)/“$2”/isg;
	    $savedwhere2 =~s/\<\/a\>//isg;
	    $savedwhere2 =~s/\<b\>//isg;
	    $savedwhere2 =~s/\<\/b\>//isg;
	    $savedwhere2 =~s/\"/\\\"/;

	    my $wherebaomi=$where."(密)";
	    if (($savedwhere eq $where)||($savedwhere eq $wherebaomi)){
                if (((($hiddened eq 1)&&($membercode ne "ad"))||($savedusername =~ /^客人/))&&(lc($savedusername) ne lc($inmembername))) {
		    $guests++;
		    $XA = $XB =  '';
		   if ((lc($savedusername) eq lc($inmembername))||($savedusername eq "客人($trueipaddress)")) {
		    	$XA = "<font color=$onlineselfcolor>";
		    	$XB = '</font>';
		    	$online_self = $onlineguest;
		    }

                   if ($savedusername !~ /^客人/) {
		      $memberoutput1 .= qq~<img src=$imagesurl/images/$onlineguest border=0 width=12 alt=请勿打扰！><a href=# nowarp TITLE="来访时间：$savedcometime\n活动时间：$savedtime\nＩＰ地址：$savedipaddress\n来源鉴定：$fromwhere">$XA隐身$XB</a>　~;
		      $memberoutput1 .= qq~<br>　~ if ($guests == int($guests/$guestmode)*$guestmode);
		    }
		    else {
		      $memberoutput1 .= qq~<img src=$imagesurl/images/$onlineguest border=0 width=12 alt=快注册呀！><a href=# nowarp TITLE="目前动作：$savedwhere2\n来访时间：$savedcometime\n活动时间：$savedtime\nＩＰ地址：$savedipaddress\n来源鉴定：$fromwhere">$XA客人$XB</a>　~;
		      $memberoutput1 .= qq~<br>　~ if ($guests == int($guests/$guestmode)*$guestmode);
		    }
		}
	        else {
		    my $spaces = "";
		    $members++;
		    my $cleanmember = $savedusername;
		    $cleanmember =~ s/ /\_/g;
		    $cleanmember =~ tr/A-Z/a-z/;
		    my $spacetemp= 12 - length($cleanmember);
		    my $spacetemp1 = int($spacetemp/2);
		    $spaces .= " " if ($spacetemp ne $spacetemp1*2);
		    for (my $i=1;$i<=$spacetemp1;$i++) { $spaces .= "　"; }
	     	    $XA = $XB =  '';
		    if ($savedusername eq $inmembername) {
		    	$XA = "<font color=$onlineselfcolor>";
		    	$XB = '</font>';
		    	$online_self = $mspic;
		    }
		    $hiddeninfo = "";
		    $hiddeninfo = "\n-=> 目前处于隐身状态 <=-" if ($hiddened eq 1);
		    $memberoutput2 .= qq~<a href="javascript:openScript('messanger.cgi?action=new&touser=$cleanmember',420,320)"><img src=$imagesurl/images/$mspic border=0 width=12 height=11 alt="给$savedusername发送一个短消息"></a><a href=javascript:O9('$cleanmember') TITLE="目前动作：$savedwhere2\n来访时间：$savedcometime\n活动时间：$savedtime\n操作系统：$saveosinfo\n浏 览 器：$savebrowseinfo\nＩＰ地址：$savedipaddress\n来源鉴定：$fromwhere$hiddeninfo">$XA$savedusername$XB</a>$spaces&nbsp;~;
		    $memberoutput2 .= qq~<br>　~ if ($members == int($members/$screenmode)*$screenmode);
	  }
	    }
    	}
    	$memberoutput1 = "" if (($members > 50)&&($guests > 20));
	$memberoutput1 = "" if ($memberoutput1 eq "　");
	$memberoutput2 = "" if ($memberoutput2 eq "　");

    	$memberoutput2 = "$memberoutput2<BR>" if (($memberoutput2 ne "")&&($memberoutput1 ne ""));
        $memberoutput = "$memberoutput2$memberoutput1";
    	undef $memberoutput1; undef $memberoutput2;
        my $totleonline=$members+$guests;
        $membertongji = " 目前论坛总在线 <b>$totleonlineall</b> 人，本分论坛共有 <b>$totleonline</b> 人在线。其中注册用户 <b>$members</b> 人，访客 <b>$guests</b> 人。";
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
