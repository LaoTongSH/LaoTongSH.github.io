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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/mpic.cgi";

$filerequire = "$lbdir" . "data/boardstats.cgi";
my @fileinfo = stat("$filerequire");
if ((!(-e $filerequire))||($fileinfo[7] < 50)) {
    $filetoopen = "$lbdir" . "data/allforums.cgi";
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
    $totle1 = 0; $totle2 = 0;
    foreach $forum (@forums) {
        chomp $forum;
	next if ($forum eq "");
        (my $tempno,my $no, $no, $no, $no, $no ,$no ,$no ,$no, $no ,$no ,$no, $threads, $posts, $no, $no, $no,$no,$no,$no) = split(/\t/,$forum);
   	next if ($tempno !~ /^[0-9]+$/);
	$totle1 += $threads; $totle2 += $posts;
    }
    opendir (DIRS, "$lbdir");
    my @files2 = readdir(DIRS);
    closedir (DIRS);
    my @memdir = grep(/^members/i, @files2);
    $memdir = $memdir[0];
    $dirtoopen = "$lbdir" . "$memdir";
    opendir (DIR, "$dirtoopen"); 
    my @filedata = readdir(DIR);
    closedir (DIR);
    my @countvar = grep(/\.cgi$/i,@filedata);
    $newtotalmembers = @countvar;
    $filetomake = "$lbdir" . "data/boardstats.cgi";
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'nodisplay\'\;\n";
        print FILE "\$totalmembers = \'$newtotalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totle1\'\;\n";
        print FILE "\$totalposts = \'$totle2\'\;\n";
        print FILE "\n1\;";
        close (FILE);
}
require "data/boardstats.cgi";
require "lb.lib.pl";
require "visitforum.lib.pl";

$|++;                                     # Unbuffer the output
$thisprog = "leoboard.cgi";

require "imagead.cgi" if (($useimagead eq "1")||($useimagead1 eq "1"));
$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/\/$//;
$query = new LBCGI;
&ipbanned; #封杀一些 ip

if ($showskin ne "off") {
    my $dirtoopen = "$lbdir" . "data/skin";
    opendir (DIR, "$dirtoopen");
    my @dirdata = readdir(DIR);
    closedir (DIR);
    $myskin="";
    my @thd = grep(/\.cgi$/,@dirdata);
    my $topiccount = @thd;
    @thd=sort @thd;
    for (my $i=0;$i<$topiccount;$i++){
	$thd[$i]=~s /\.cgi//isg;
	$myskin.=qq~<option value="$thd[$i]">[ $thd[$i] ]</option>~;
    }
}
$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$action = $query->param('action');
$catlog = $query->param('catlog');
$catlog2=$catlog;

$te="catlog".$catlog;
if ($catlog ne "") {
  $catlog1=$query->cookie("$te");
  if ($catlog1 ne "no") {
    $catlog1cookie     = cookie(-name    =>   "$te",
                         -value   =>   "no",
                         -expires =>   "+30d",
                         -path    =>   "$cookiepath/"
                         );
    }
  else {
    $catlog1cookie     = cookie(-name    =>   "$te",
                         -value   =>   "yes",
                         -expires =>   "+30d",
                         -path    =>   "$cookiepath/"
                         );
  }
}

$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ($action eq "delcookieall") {
	$namecookie = cookie(-name    =>"amembernamecookie",
                         -value   =>   "",
			 -path    =>   "$cookiepath/");
    	$passcookie = cookie(-name    =>"apasswordcookie",
                         -value   =>   "",
			 -path    =>   "$cookiepath/");
       $onlineviewcookie = cookie(-name    =>   "onlineview",
                         -value   =>   "",
                         -path    =>   "$cookiepath/");
	   $advpostcookie = cookie(-name    =>   "advpost",
                        -values   =>   "",
                        -path    =>   "$cookiepath/");
       $threadcookie = cookie(-name    =>   "threadages",
                        -value   =>   "",
                        -path    =>   "$cookiepath/");
       $viewcookie = cookie(-name    =>   "viewMode",
                         -value   =>   "",
                         -path    =>   "$cookiepath/");
       $nodisp     = cookie(-name    =>   "nodisp",
                         -value   =>   "",
                         -path    =>   "$cookiepath/");
       $freshtimecookie = cookie(-name    =>   "freshtime",
		    	 -value   =>   "",
                         -path    =>   "$cookiepath/");
       $selectstylecookie = cookie(-name    =>   "selectstyle",
		    	 -value   =>   "",
                         -path    =>   "$cookiepath/");
	$tanchumsgcookie = cookie(-name    =>   "tanchumsg",
		    	 -value   =>   "",
                         -path    =>   "$cookiepath/");

    $cookie     = cookie(-name    =>   "lastvisit",
                         -value   =>   "",
                         -path    =>   "$cookiepath/");
    $tempcookie = cookie(-name    =>   "templastvisit",
                         -value   =>   "",
                         -path    =>   "$cookiepath/");

$catlogcookie     = cookie(-name    =>   "catlog",
                         -value   =>   "",
                         -path    =>   "$cookiepath/"
                         );
$unioncookie     = cookie(-name    =>   "union",
                         -value   =>   "",
                         -path    =>   "$cookiepath/"
                         );
$banfreshcookie  = cookie(-name    =>   "banfresh",
                          -value   =>   "",
                          -path    =>   "$cookiepath/");
$treeviewcookie  = cookie(-name    =>   "treeview",
                          -value   =>   "",
                          -path    =>   "$cookiepath/");
$tecookie	 = cookie(-name    =>   "catlog",
                          -value   =>   "",
                          -path    =>   "$cookiepath/");

    	print header(-cookie=>[$tecookie, $cookie,$tempcookie, $catlogcookie,$unioncookie,$banfreshcookie, $treeviewcookie, $onlineviewcookie,$advpostcookie,$threadcookie,$viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie, $namecookie,$passcookie], -charset=>gb2312);
}

$union   = $query->cookie("union");
$screenmode   = $query->cookie("screenmode");
$screenmode=7 if ($screenmode eq "");
$onlineview=1 if ($onlineview eq "");
$union=1 if ($union eq "");
if ($catlog eq ""){$catlog   = $query->cookie("catlog");}
if ($inmembername eq "") {    $inmembername = "客人";}else {    &getmember("$inmembername");  &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");  &getlastvisit;}
$cpudisp = 1 if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"));
$onlineview1   = $query->cookie("onlineview");
$onlineview = $onlineview1 if ($onlineview1 ne "");
$onlineview=1 if ($onlineview eq "");
if ($action eq "onlineview") {if ($onlineview == 1){	$onlineview=0; }else{	$onlineview=1;  }}
$treecat1   = $query->cookie("treeview");
$treeview   = 0 if (($treecat1 ne "")||($catlog ne ""));
$treeview   = 1 if ($treeview eq "");
if ($action eq "union") {if ($union == 1){ $union=0; }else{ $union=1;  }}
elsif ($action eq "expand") {$catlog="expand";}
elsif ($action eq "depand") {$catlog="depand";}
elsif ($action eq "resetall") {
    $filetoopen = "$lbdir" . "data/allforums.cgi";
    &winlock($filetoopen);
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
    &winunlock($filetoopen);
    $currenttime = time;
    foreach (@forums) {
    	($tempno, $trash) = split(/\t/,$_);
    	$lvisit .= "$tempno-$currenttime--";
    }
    $cookie     = cookie(-name    =>   "lastvisit",
                         -value   =>   "$lvisit",
                         -path    =>   "$cookiepath/",
                         -expires =>   "+30d");
    $tempcookie = cookie(-name    =>   "templastvisit",
                         -value   =>   "$lvisit",
                         -path    =>   "$cookiepath/",
                         -expires =>   "+30d");
}

$onlineviewcookie     = cookie(-name    =>   "onlineview",
                         -value   =>   "$onlineview",
                         -path    =>   "$cookiepath/"
                         );

$catlogcookie     = cookie(-name    =>   "catlog",
                         -value   =>   "$catlog",
                         -expires =>   "+30d",
                         -path    =>   "$cookiepath/"
                         );


if ($onlineview==1){
    $onlinetitle="<a href=$thisprog?action=onlineview><font color=$fontcolormisc>关闭详细列表</font></a>";
}else{
    $onlinetitle="<a href=$thisprog?action=onlineview><font color=$fontcolormisc>显示详细列表</font></a>";
}
$treecatlog="<a href=$thisprog?action=expand><font color=$fontcolormisc>展开所有</a>] [<a href=$thisprog?action=depand>收缩所有</font></a>";

if (open(FILE2,"${lbdir}data/shareforums.cgi")) {
#    flock(FILE2, 1) if ($OS_USED eq "Unix");
    @lmforums = <FILE2>;
    close(FILE2);
    $lmforums = @lmforums;
 }

$unioncookie     = cookie(-name    =>   "union",
                         -value   =>   "$union",
                         -expires =>   "+30d",
                         -path    =>   "$cookiepath/"
                         );
$uniontitle="<font color=$fontcolormisc>（共有 $lmforums 个联盟论坛）</font>";
if ($union==0){ $unionview="显示联盟列表"; }else{$unionview="关闭联盟列表";}

    &title;

    &birthday if ($dispborn ne "no");

    print header(-cookie  =>[$onlineviewcookie, $cookie, $tempcookie ,$unioncookie,$catlogcookie, $catlog1cookie], -charset=>gb2312) if ($action ne "delcookieall");
#, -expires=>'now'

    $cleanlastregistered = $lastregisteredmember;
    $cleanlastregistered =~ y/ /_/;
    $cleanlastregistered =~ tr/A-Z/a-z/;
    $cleanlastregistered = qq~<a href="javascript:O9('$cleanlastregistered')">$lastregisteredmember</a>~;
    if ($inmembername eq "客人") {
	$inboxstatus = qq~<font color=$forumfontcolor align=center>你必须<a href="$registerprog">注册</a>并<a href="$loginprog">登陆</a>后才能查看你的短消息信箱信息。</font>~;
	$inboximg = qq~<img src=$imagesurl/images/inboxnologin.gif width=16>~;
    }

    if ($inmembername ne "客人") {
        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
	$memberfilename =~ tr/A-Z/a-z/;
        $totalmessages = @allmessages;
        $filetoopen = "$lbdir". "$msgdir/out/$memberfilename" . "_out.cgi";
        open (FILE, "$filetoopen");
    	flock(FILE, 1) if ($OS_USED eq "Unix");
        @allmessages = <FILE>;
        close (FILE);
        $totalmessagesout = @allmessages;
        if ($unread eq "0") {
        	$inboximg = qq~<img src=$imagesurl/images/inboxnonew.gif width=16>~;
        	$inboxstatus = qq~　<font color=$forumfontcolor>目前您没有新的短消息。 [<a href=$boardurl/messanger.cgi?action=inbox target=_blank>短消息收件箱</a>]中共有 <b>$totalmessages</b> 条信息，[<a href=$boardurl/messanger.cgi?action=outbox target=_blank>短消息发件箱</a>]中共有 <b>$totalmessagesout</b> 条信息。</font>~; }
	else {
		$inboximg = qq~<img src=$imagesurl/images/inboxnew.gif width=16>~;
		$inboxstatus = qq~　<font color=$forumfontcolor>目前您有 <a href=$boardurl/messanger.cgi?action=inbox target=_blank><b><font color=$fonthighlight>$unread</font></a></b> 条新的短消息</a>。 [<a href=$boardurl/messanger.cgi?action=inbox target=_blank>短消息收件箱</a>]中共有 <b>$totalmessages</b> 条信息，[<a href=$boardurl/messanger.cgi?action=outbox target=_blank>短消息发件箱</a>]中共有 <b>$totalmessagesout</b> 条信息。</font>~;
        }
        $inboxstatus = qq~$inboxstatus <font color=$fonthighlight><br>　注　意：请及时删除已阅读的短消息，以免给系统带来负担，谢谢合作！</font>~ if (($totalmessages + $totalmessagesout) >= 15);
}
    $adscript = &HTML("$adscript");
    $adfoot = &HTML("$adfoot");
    $insidead  = "" if ($useimagead ne "1");
    $insidead1 = "" if ($useimagead1 ne "1");
    $output .= qq~$insidead$insidead1~;

$output .= qq~<BGSOUND SRC=$imagesurl/midi/$midiaddr2 LOOP=-1>~ if ($midiaddr2 ne "");

$output .= qq~
<script language="javascript">
function O3(id) {window.open("$forumsprog?forum="+id);}
function O9(id) {window.open("$profileprog?action=show&member="+id);}
</script>
<TABLE cellSpacing=0 cellPadding=0 width=$tablewidth align=center>
<tr><TD width=30% rowSpan=3><img src=$imagesurl/images/$boardlogo></TD>
<TD vAlign=bottom align=right><div align="right">$adscript</div></TD></TR>
<TR><td valign=bottom align=right><br><font color=$fontcolormisc>
热烈欢迎新会员 "$cleanlastregistered" 的加入。 [<a href="memberlist.cgi?a=5" target=_blank>新进会员</a>]&nbsp;<br>共有 <a href="memberlist.cgi?a=3" target=_blank><b>$totalmembers</b></a> 名注册会员、<b>$totalthreads</b> 篇主题， <b>$totalposts</b> 篇回复&nbsp;<br>
</td></TR></TABLE><br>
~;
    &whosonline("$inmembername\t论坛首页\tboth\t查看论坛信息\t");
if ($announcements eq 'yes') {
	if (open(FILE, "${lbdir}data/news.cgi")) {
    	    flock(FILE, 1) if ($OS_USED eq "Unix");
            my @announcementdata = <FILE>;
            close(FILE);
            $totalannouncements = @announcementdata;
            if ($totalannouncements eq 0) {
            	$dateposted = time; $title = "当前没有公告";
            }
            else {
               ($title, $dateposted, $trash) = split(/\t/, $announcementdata[0]);
            }
        }
        else { $dateposted = time; $title = "当前没有公告"; }
        $dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
        $dateposted = &longdate("$dateposted");
        if (($totalannouncements ne 0)&&($totalannouncements ne "")) {
            $announcetemp1=qq~<img src=$imagesurl/images/announce.gif border=0 alt="总论坛公告！共 $totalannouncements 条！" width=18 height=18>~;
        }
        else {$announcetemp1=qq~<img src=$imagesurl/images/announce.gif border=0 alt="总论坛暂时无公告！" width=18 height=18>~;}

	if ($announcemove eq "on") {
	    $announcetemp2=qq~<marquee scrollamount=3><b><a href=$boardurl/$announceprog target=_blank>$title</a></b>　[$dateposted]</marquee>~;
	}
	else {
            $titletemp = &lbhz($title,25);
	    $announcetemp2=qq~<b><a href=$boardurl/$announceprog target=_blank title="$title">$titletemp</a></b>　[$dateposted]~;
	}


        undef $titletemp; undef $title;
}
my $recodeview = "";
$recodeview = qq~<img src=$imagesurl/images/poll.gif border=0 width=16 height=16 alt="显示访问统计" align=absmiddle><font color=$forumfontcolor><a href="javascript:openScript('viewstats.cgi',550,400)">访问统计</a>~ if ($recordviewstat eq "yes");
$output .= qq~
<table cellpadding=1 cellspacing=0 width=$tablewidth align=center>
<tr><td align=center width=2></td>
<td align=center width=34>$announcetemp1</td>
<td width=* align=left><font color=$forumfontcolor>$announcetemp2</td><td width=140>&nbsp;</td>
<td width=90 align=right>$recodeview</td>
<td width=90 align=right><img src=$imagesurl/images/team.gif border=0 width=16 height=16 alt="显示管理团队" align=absmiddle><font color=$forumfontcolor><a href=team.cgi target=_blank>管理团队</a></td>
<td width=90 align=right><img src=$imagesurl/images/userlist.gif border=0 width=16 height=16 alt="显示用户列表" align=absmiddle><font color=$forumfontcolor><a href=memberlist.cgi?a=4 target=_blank>用户列表</a></td>
<td width=90 align=right><img src=$imagesurl/images/top.gif border=0 width=16 height=16 alt="显示发贴量排名" align=absmiddle><font color=$forumfontcolor><a href=memberlist.cgi?a=1 target=_blank>发贴排名</a></td>
</tr></table>
~;
$filetoopen = "$lbdir" . "data/allforums.cgi";
if (!(-e "$filetoopen")) { $filetoopen = "$lbdir" . "data/allforums.cgi.cgi"; }
$forumsize=0;
if (-e "$filetoopen"){
&winlock($filetoopen);
open(FILE, "$filetoopen");
flock (FILE, 1) if ($OS_USED eq "Unix");
@forums = <FILE>;
close(FILE);
&winunlock($filetoopen);
$forumsize=@forums;
}
else {
   &error("论坛&请先在管理区建立分论坛！");
}
$filetoopen = "$lbdir" . "data/allforums.cgi";
	$output .= qq~
<style>
TABLE {BORDER-TOP: 0px; BORDER-LEFT: 0px; BORDER-BOTTOM: 1px; }
TD {BORDER-RIGHT: 0px; BORDER-TOP: 0px; color: $fontcolormisc; }
</style>
<table cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table>
<table cellpadding=6 cellspacing=0 width=$tablewidth height=28 align=center  bordercolor=$tablebordercolor border=1>
~;
    if (($inmembername eq "客人")&&(($showfastlogin eq "top")||($showfastlogin eq "")||($showfastlogin eq "all"))) {
    $output .= qq~<tr><td bgcolor=$titlecolor colspan=7><font color=$titlefontcolor>
<B>-=> 快速登录入口</B>　 [<a href=register.cgi>注册用户</a>]　[<a href=profile.cgi?action=lostpass style=cursor:help>忘记密码</a>]<BR>
</td></tr>
<FORM name=login method=post action=loginout.cgi>
<tr><td bgcolor=$forumcolorone align=center width=26>
<img src=$imagesurl/images/userlist.gif></td>
<td bgcolor=$forumcolortwo colspan=6 width=*>
<input type=hidden name="action" value="login">
&nbsp;用户名：<input type=text name="inmembername" size=12 maxlength=16>　　密码：<input type=password name="inpassword" size=12 maxlength=20>　　~;
$output .= qq~<select name=CookieDate><option selected value=-1d>不保存</option><option value=+1d>保存一天</option><option value=+30d>保存一月</option><option value=+20y>永久保存</option></select>　~;
if ($showskin ne "off") {$output .= qq~<select name="selectstyle"><option value="">默认风格$myskin</option></select>~;}
$output .= qq~　<select name=forum><option selected value=>论坛首页</option>~;
foreach my $forum (@forums) {
    chomp $forum;
    next if ($forum eq "");
    (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription, my $tmp , $tmp , $tmp , $tmp,  $tmp , $tmp , $tmp,  $tmp,  $tmp,  $tmp, $tmp, $tmp, $tmp,my $hiddenforum,$tmp) = split(/\t/,$forum);
    next if ($forumid !~ /^[0-9]+$/);
$output .= qq~<option value="$forumid">$forumname</option>~;
}
$output .= qq~</select>　　<input type=submit name="submit" value="登 陆"></td></tr></form></td></tr></table>~;
}

	$output .= qq~
<table cellpadding=6 cellspacing=0 width=$tablewidth height=28 align=center  bordercolor=$tablebordercolor border=1>
<tr><td bgcolor=$titlecolor width=26 align=center><font color=$titlefontcolor><b>状态</b></font></td>
<td bgcolor=$titlecolor width=* align=center><font color=$titlefontcolor><b>论坛名称</b></font>　<font color=$fontcolormisc>[$treecatlog]</font></td>
<td bgcolor=$titlecolor width=80 align=center><font color=$titlefontcolor><b>版主</b></font></td>
<td bgcolor=$titlecolor width=38 align=center><font color=$titlefontcolor><b>主题</b></font></td>
<td bgcolor=$titlecolor width=42 align=center><font color=$titlefontcolor><b>回复</b></font></td>
<td bgcolor=$titlecolor width=168 align=center><font color=$titlefontcolor><b>最后更新</b></font></td>
<td bgcolor=$titlecolor width=26 align=center><font color=$titlefontcolor><b><a title="将“$boardname”添加到收藏夹" href="javascript:window.external.addFavorite('$boardurl/$thisprog', '$boardname')">收藏</a></b></font></td>
</tr></table>
~;
###自动备份，自动恢复
my $filetoopens = &lockfilename($filetoopen);
if (!(-e "$filetoopens.lck")) {
  if ($forumsize == 0){
    open(FILE, "$filetoopen.cgi");
    flock (FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
    open(FILE, ">$filetoopen");
    flock (FILE, 2) if ($OS_USED eq "Unix");
    foreach (@forums) {
    	print FILE $_;
    }
    close(FILE);
  }else{
    if (!(-e "$filetoopen.cgi")){
    	open(FILE, ">$filetoopen.cgi");
    	foreach (@forums) {
    	    print FILE $_;
    	}
    	close(FILE);
    }
  }
}
undef $forumsize;
###自动备份，自动恢复

foreach $forum (@forums) {
    chomp $forum;
    next if ($forum eq "");
    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic,$tmp,$tmp,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
    next if ($forumid !~ /^[0-9]+$/);

    $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$forumid\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
    push (@rearrangedforums, $rearrange);
}
@finalsortedforums = sort(@rearrangedforums);

foreach $sortedforums (@finalsortedforums) {
    ($categoryplace, $category, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp,$tmp,$hiddenforum,$tmp,$tmp) = split(/\t/,$sortedforums);
    if (($categoryplace ne $lastcategoryplace)&&($hiddenforum ne "yes")) {

    $has=0;
          foreach (@hascat){
          $has=1 if ($_ eq $categoryplace);
          }
           if ($has ==0){
         $output .= qq~<table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center bordercolor=$tablebordercolor border=1>~;
#<tr><td bgcolor=$catback background=$imagesurl/images/$catbackpic colspan=7><a href=$thisprog?catlog=$categoryplace><img src=$imagesurl/images/cat.gif border=0 width=9 height=9> <font color=$catfontcolor><b>$category</b></font></a></td></tr></table>~;

      $te="catlog".$categoryplace;
      
      if (((($query->cookie("$te") ne "no")&&($catlog2 ne $categoryplace))||(($query->cookie("$te") eq "no")&&($catlog2 eq $categoryplace))||($catlog eq "expand"))&&!($catlog eq "depand"))
      {
      $output .= qq~<tr><td bgcolor=$catback background=$imagesurl/images/$catbackdpic colspan=7 height=24 align=left><a href=$thisprog?catlog=$categoryplace><img src=$imagesurl/images/cat1.gif border=0 width=9 height=9> <font color=$catfontcolor><b>$category</b></font></a></td></tr></table>~;   
      } 
      else 
      {
      $output .= qq~<tr><td bgcolor=$catback background=$imagesurl/images/$catbackpic colspan=7 height=24 align=left><a href=$thisprog?catlog=$categoryplace><img src=$imagesurl/images/cat.gif border=0 width=9 height=9> <font color=$catfontcolor><b>$category</b></font></a></td></tr></table>~;   
      }
      
     foreach my $myforums (@rearrangedforums) {
     ($mycategoryplace, $category, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime1, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$forumid,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$myforums);
     if (($categoryplace eq $mycategoryplace)&&($hiddenforum ne "yes")){
       $tm = 0;
       $modout="";
       if ($forummoderator) {
            $forummoderator =~ s/\, /\,/g;
            my @mods = split(/\,/,$forummoderator);
            $tm = @mods; my $mc = 1;
            foreach (@mods) {
                my $cmodn = $_; $cmodn =~ y/ /_/;
                $cmodn =~ tr/A-Z/a-z/;
  	        last if ($mc > 3 );
                if ($mc != $tm) {
                    $modout .= qq~<a href="javascript:O9('$cmodn')">$_</a><BR>~;
                    }
                    else { $modout .= qq~<a href="javascript:O9('$cmodn')">$_</a>~;
                }
                $mc++;
             }
        }
    $modout .= qq~<font color=$posternamecolor>More...</font>~ if ($tm > 3 );
    $modout="暂时空缺" if ($modout eq "");
    if ($catlog eq "expand"){$output .= qq~ <script>document.cookie="$te=yes;expires=+30d;path=$cookiepath/";</script>~;}
    if ($catlog eq "depand"){$output .= qq~ <script>document.cookie="$te=no;expires=+30d;path=$cookiepath/";</script>~;} 
    if (((($query->cookie("$te") ne "no")&&($catlog2 ne $categoryplace))||(($query->cookie("$te") eq "no")&&($catlog2 eq $categoryplace))||($catlog eq "expand"))&&!($catlog eq "depand")) {
    if ($dispboardonline ne "no") {
     &getonlineno("$forumname");
     if ($guests1 ne 0) {
    	$guestadd = qq~（其中 $guests1 个客人）~;
     }
     else { undef $guestadd; }
     $titleinfos = qq~TITLE="目前共有 $totleonline 人在此论坛上$guestadd！$output2"~;
    }
    else {
      $titleinfos = "";
    }
    $forumnameadd = $forumname;
    my $fm = $forumname;
    $forumname = qq~<a href=$forumsprog?forum=$forumid $titleinfos><font color=$posternamecolor>$forumname</font></a>~;

    $forumlastvisit = $lastvisitinfo{$forumid};
    $folderpicture = qq(　);

    ($lastposttime,$threadnumber,$topictitle)=split(/\%\%\%/,$lastposttime1);

    if (($lastposttime > $forumlastvisit)&&($inmembername ne "客人")) {
	if (($forumpass)||($privateforum eq "yes")){
	    $folderpicture = qq~<a href=javascript:O3($forumid)><img src=$imagesurl/images/$bm_havenew width=13 height=16 border=0></a>~;
	}
	elsif ($startnewthreads eq "follow") {
	    $folderpicture = qq~<a href=javascript:O3($forumid)><img src=$imagesurl/images/$pl_havenew width=13 height=16 border=0></a>~;
	}
	elsif ($startnewthreads eq "yes") {
	    $folderpicture = qq~<a href=javascript:O3($forumid)><img src=$imagesurl/images/$zg_havenew width=13 height=16 border=0></a>~;
	}
	elsif ($startnewthreads eq "all") {
	    $folderpicture = qq~<a href=javascript:O3($forumid)><img src=$imagesurl/images/$kf_havenew width=13 height=16 border=0></a>~;
	}
        $posts         = qq~<font color=$fonthighlight><b>$posts</b></font>~;
        $threads       = qq~<font color=$fonthighlight><b>$threads</b></font>~;
    }
    else {
        if (($forumpass)||($privateforum eq "yes")){
            $folderpicture = qq~<a href=javascript:O3($forumid)><img src=$imagesurl/images/$bm_nonew width=13 height=16 border=0></a>~;
	}
	elsif ($startnewthreads eq "follow") {
	    $folderpicture = qq~<a href=javascript:O3($forumid)><img src=$imagesurl/images/$pl_nonew width=13 height=16 border=0></a>~;
	}
	elsif ($startnewthreads eq "yes") {
	    $folderpicture = qq~<a href=javascript:O3($forumid)><img src=$imagesurl/images/$zg_nonew width=13 height=16 border=0></a>~;
	}
	elsif ($startnewthreads eq "all") {
	    $folderpicture = qq~<a href=javascript:O3($forumid)><img src=$imagesurl/images/$kf_nonew width=13 height=16 border=0></a>~;
	}
    }

 if ($startnewthreads eq "no") {
     $folderpicture = qq~<a href=javascript:O3($forumid)><img src=$imagesurl/images/$jh_pic width=13 height=16 border=0></a>~;
 }

        if ($inmembername eq "客人") { $loginmessage = "（您必须登陆才能查看详情，否则只显示该论坛的无新贴图例）"; }
        $lastposterfilename = $lastposter;
        $lastposterfilename =~ y/ /_/;
        $lastposterfilename =~ tr/A-Z/a-z/;

        $forumlastvisit = $forumlastvisit + ($timedifferencevalue*3600) + ($timezone*3600);
        $lastdate = &longdate("$forumlastvisit");
        $lasttime = &shorttime("$forumlastvisit");
        if ($lastposttime) {
            $lastposttime = $lastposttime + ($timedifferencevalue*3600) + ($timezone*3600);
            $longdate = &longdate("$lastposttime");
            $shorttime = &shorttime("$lastposttime");
            $forumlastpost = qq~<BR><font color=$lastpostfontcolor>&nbsp;$longdate $shorttime</font><BR>~;
            if ($lastposter=~/\(客\)/) {
            	$lastposter=~s/\(客\)//isg;
                $lastposterby  = qq~<font color=$posternamecolor title="此为未注册用户">&nbsp;最后发表： $lastposter</font>　<img src="$imagesurl/images/lastpost.gif" width=11 height=10>~;
            }
            else {
                $lastposterby  = qq~<font color=$posternamecolor>&nbsp;最后发表： </font><a href="javascript:O9('$lastposterfilename')">$lastposter</a>　<img src="$imagesurl/images/lastpost.gif" width=11 height=10>~;
            }
        }
        else { $forumlastpost = qq~<font color=$lastpostfontcolor>&nbsp;没有贴子</font>~;
               $lastposterby  = "";
        }
        $lastpost = "";
	$topictitle =~ s/\&lt;/</g;
	$topictitle =~ s/\&gt;/>/g;
	$topictitle =~ s/ \&nbsp;/　/g;
        $topictitle =~ s/\&amp;/\&/g;
        $topictitle =~ s/^＊＃！＆＊//;

	if (($privateforum ne "yes")&&($topictitle)) {
            $topictitletemp = &lbhz($topictitle,18);
            $topictitletemp =~ s/\&/\&amp;/g;
	    $topictitletemp =~ s/</\&lt;/g;
	    $topictitletemp =~ s/>/\&gt;/g;
            $topictitle =~ s/\&/\&amp;/g;
	    $topictitle =~ s/</\&lt;/g;
	    $topictitle =~ s/>/\&gt;/g;
            $lastpost = qq~<font color=$posternamecolor>&nbsp;主题： </font><a href=$threadprog?forum=$forumid&topic=$threadnumber&replynum=last TITLE="$topictitle">$topictitletemp</a><BR>~;
        }
    $forumbookmark = qq~<span style="CURSOR: hand" onClick="window.external.AddFavorite('$boardurl/$forumsprog?forum=$forumid', '$boardname - $forumnameadd')"><IMG SRC="$imagesurl/images/fav_add.gif" BORDER="0" width=15 height=15 ALT="将$forumnameadd添加到收藏夹"></span>~;

   if ($teamlogo eq ""){
    	$team="";
        }
    if ((($teamurl eq "")||($teamurl eq "http://")) && ($teamlogo ne "")){
    	$team=qq~<img src=$imagesurl/images/$teamlogo>~;
        }
    if ((($teamurl ne "")&&($teamurl ne "http://")) && ($teamlogo ne "")){
    	$team=qq~<a href=$teamurl><img src=$imagesurl/images/$teamlogo border=0></a>~;
    	}

    $output .= qq~
<table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center bordercolor=$tablebordercolor border=1>
<tr><td bgcolor=$forumcolorone align=center width=26>$folderpicture</td>
<td bgcolor=$forumcolortwo valign=top width=*>
<table><tr><td>$team</td><td>$forumname<font color=$forumfontcolor><br>$forumdescription</td></tr></table>
</td>
<td bgcolor=$forumcolorone align=center width=80><font color=$forumfontcolor>$modout</td>
<td bgcolor=$forumcolortwo align=center width=38><font color=$forumfontcolor>$threads</td>
<td bgcolor=$forumcolortwo align=center width=42><font color=$forumfontcolor>$posts</td>
<td bgcolor=$forumcolorone width=168><font color=$lastpostfontcolor>$lastpost$lastposterby$forumlastpost</td>
<td bgcolor=$forumcolortwo align=center width=26>$forumbookmark</td>
</tr></table>
~;
}
}
    }
    }
    $lastcategoryplace = $categoryplace;
    push (@hascat, $categoryplace);
    undef $forumlastvisit; undef $forummoderator; undef $modout; undef $forumbookmark;
  }
}
    if (($inmembername eq "客人")&&(($showfastlogin eq "bottom")||($showfastlogin eq "all"))) {
    $output .= qq~
<table cellpadding=6 cellspacing=0 width=$tablewidth height=28 align=center  bordercolor=$tablebordercolor border=1>
<tr><td bgcolor=$titlecolor colspan=7><font color=$titlefontcolor>
<B>-=> 快速登录入口</B>　 [<a href=register.cgi>注册用户</a>]　[<a href=profile.cgi?action=lostpass style=cursor:help>忘记密码</a>]<BR>
</td></tr>
<FORM name=login method=post action=loginout.cgi>
<tr><td bgcolor=$forumcolorone align=center width=26>
<img src=$imagesurl/images/userlist.gif></td>
<td bgcolor=$forumcolortwo colspan=6 width=*>
<input type=hidden name="action" value="login">
&nbsp;用户名：<input type=text name="inmembername" size=12 maxlength=16>　　密码：<input type=password name="inpassword" size=12 maxlength=20>　　~;
$output .= qq~<select name=CookieDate><option selected value=-1d>不保存</option><option value=+1d>保存一天</option><option value=+30d>保存一月</option><option value=+20y>永久保存</option></select>　~;
if ($showskin ne "off") {$output .= qq~<select name="selectstyle"><option value="">默认风格$myskin</option></select>~;}
$output .= qq~　<select name=forum><option selected value=>论坛首页</option>~;
foreach my $forum (@forums) {
    chomp $forum;
    next if ($forum eq "");
    (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription, my $tmp , $tmp , $tmp , $tmp,  $tmp , $tmp , $tmp,  $tmp,  $tmp,  $tmp, $tmp, $tmp, $tmp,my $hiddenforum,$tmp) = split(/\t/,$forum);
    next if ($forumid !~ /^[0-9]+$/);
$output .= qq~<option value="$forumid">$forumname</option>~;
}
$output .= qq~</select>　　<input type=submit name="submit" value="登 陆"></td></tr></form></td></tr></table>~;
}

undef @hascat;
  $output .= qq~
    <img src="" width=9 height=5><br>
    <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 width=100%>
  ~;


    if (($lmforums ne "")&&($lmforums > 0)) {
	$output .= qq~
	  <tr>
	  <td bgcolor=$titlecolor colspan=2>
	 <font color=$titlefontcolor><b>-=> 联盟论坛 $uniontitle</b>　 [<a href=$thisprog?action=union><font color=$fontcolormisc>$unionview</font></a>]　 [<a href="javascript:openScript('lmcode.cgi',480,240)">论坛联盟代码</a>]</font>
	  </td>
	  </tr>
	~;
	if ($union==1){
	  $lmtexts = "";
	  $lmlogos = "";
	  foreach $lmforum (@lmforums) {
	    chomp $lmforum;
            next if ($lmforum eq "");
            ($lmforumname,$lmforumurl,$lmforuminfo,$lmforumorder,$lmweblogo) = split(/\t/,$lmforum);
            if (($lmweblogo ne "")&&($lmweblogo ne "http:\/\/")) {
            	$lmlogos .= qq~<a href=$lmforumurl target=_blank><img src=$lmweblogo width=88 height=31 border=0 title="$lmforumname\n\n$lmforuminfo"></a> ~;
            	
            }
            else {
            	$lmtexts .= qq~<a href=$lmforumurl target=_blank title="$lmforuminfo">$lmforumname</a>　~;
            }
	  }
	  $output .= qq~<tr><td bgcolor=$forumcolorone width=26 align=center><img src=$imagesurl/images/$lm_pic width=16 height=16></td><td bgcolor=$forumcolortwo width=*><table width=100% cellpadding=0 cellspacing=0><tr><td width=100%><img src="" width=500 height=1><BR>$lmlogos</td></tr></table></td></tr>~ if ($lmlogos ne "");
	  $output .= qq~<tr><td bgcolor=$forumcolorone width=26 align=center><img src=$imagesurl/images/$lm_pic width=16 height=16></td><td bgcolor=$forumcolortwo width=*><table width=100% cellpadding=0 cellspacing=0><tr><td width=100%><img src="" width=500 height=1><BR>$lmtexts</td></tr></table></td></tr>~ if ($lmtexts ne "");
     }
   }
   undef @lmforums;

    $onlinemaxtime = &dateformatshort($onlinemaxtime);
    my $total_users = $guests + $members;
    $output .= qq~
</table></td></tr></table><img src="" width=10 height=5><br>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=7><font color=$titlefontcolor><b>-=> 您的个人状态</b></font></td></tr>
<tr><td bgcolor=$forumcolorone align=center width=26>$inboximg</td>
<td bgcolor=$forumcolortwo colspan=6 width=*>$inboxstatus<BR>
　您的 IP 是：<font color=$posternamecolor>$ENV{'REMOTE_ADDR'}</font>，来自：<font color=$posternamecolor>$fromwhere1</font> 。
　操作系统：<font color=$posternamecolor>$osinfo</font>，浏览器：<font color=$posternamecolor>$browseinfo</font>。
</td></tr>
~;
if ($dispborn ne "no") {
    $birthdayuser = "今天没有人过生日" if ($birthdayuser eq "");
    $output .= qq~
<tr><td bgcolor=$titlecolor colspan=7><font color=$titlefontcolor>
<B>-=> 今天过生日的注册用户 （共 $borncount 人）<BR>
</td></tr>
<tr><td bgcolor=$forumcolorone align=center width=26><img src=$imagesurl/images/born.gif alt="今天过生日人员名单" width=16 height=16></td>
<td bgcolor=$forumcolortwo colspan=6 width=*><font color=$titlefontcolor>
　<font color=$forumfontcolor>$birthdayuser</font>
~;
}
    $output .= qq~
</table></td></tr></table><img src="" width=10 height=5><br>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=7><font color=$titlefontcolor>
<B>-=> 论坛在线统计 （同时在线峰值：$onlinemax 人，发生时刻：$onlinemaxtime）</B>　 [$onlinetitle]<BR>
</td></tr>
<tr><td bgcolor=$forumcolorone align=center width=26><img src=$imagesurl/images/online.gif alt="论坛在线人数" width=16 height=16></td>
<td bgcolor=$forumcolortwo colspan=6 width=* background=$imagesurl/images/$otherbackpic><font color=$titlefontcolor>
　<font color=$forumfontcolor>目前论坛总共有 <a href=$onlineprog><B>$total_users</B></a> 人在线。其中注册用户 <B>$members</B> 人，访客 <B>$guests</B> 人。 论坛总共被访问 <b>$count1</b> 次，共被点击 <b>$count2</b> 次。<BR></font>
~;
    if ($onlineview == 1) {
            $output .= qq~　<font color=$forumfontcolor>在线名单图例：　<img src=$imagesurl/images/$onlineadmin width=11 height=12> 论坛坛主， 　<img src=$imagesurl/images/$onlinesmod width=12 height=11> 论坛总版主， 　<img src=$imagesurl/images/$onlinemod width=12 height=11> 论坛版主， 　<img src=$imagesurl/images/$onlinemember width=12 height=11> 普通会员， 　<img src=$imagesurl/images/$onlineguest width=12 height=11> 客人或隐身会员<br><hr size=1 width=98%><img src="" width=1 height=4><BR><font color=$forumfontcolor>$memberoutput</font>~;
    }

  if ($dispview eq "yes") {
    $leofilename = "$imagesdir"."images/leo728.gif";
    if (-e "$leofilename"){
       $leomemory = "<a href=http://www.cgier.com target=_blank><img src=$imagesurl/images/leo728.gif TITLE=雷傲论坛纪念版本专用标志 width=88 border=0 height=45></a>";
    }
    else { $leomemory = qq~<a href=http://www.cgier.com target=_blank title="------------------------    ☆    ------------------------\n 雷傲论坛(LeoBoard)由 CGI 编程者之家制作\n 正版标示： Powered By CGIer.com \n 感谢您采用我们的论坛，让我们做的更好！\n------------------------    ☆    ------------------------"><img src=$imagesurl/images/powered.gif width=88 height=31 border=0></a>~; }
    $output .= qq~</td></tr></table></td></tr></table>~;
    $output .= qq~<img src="" width=9 height=5><br>
<table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellspacing=1 cellpadding=3 width=100%>
<tr><td width=75% bgcolor=$titlecolor><b>　-=> LB5000II 论坛图例</b></td>
<td align=right noWrap bgcolor=$titlecolor width=25%>所有时间均为 - $basetimes &nbsp;</td></tr>
<tr><td bgcolor=$forumcolortwo colspan=3 background=$imagesurl/images/$otherbackpic1>
<table cellspacing=4 cellpadding=0 width=92% align=center>
<tr><td colspan=5>论坛图例仅当你登陆并且上次访问后才显示&nbsp;$loginmessage</font></div></td></tr>
<tr><td><font color=$fonthighlight TITLE="允许注册会员发言和回复">正规论坛</font></td>
<td><font color=$fonthighlight TITLE="允许任何人发言和回复">开放论坛</font></td>
<td><font color=$fonthighlight TITLE="允许坛主和版主发言，其他注册用户只能回复">评论论坛</font></td>
<td><font color=$fonthighlight TITLE="允许拥有访问密码或已经经过认证的注册会员发言">保密论坛</font></td>
<td colspan=2><font color=$fonthighlight>特殊论坛</font></td></tr>
<tr><td><img src=$imagesurl/images/$zg_havenew width=13 height=16> 有新的贴子</td>
<td><img src=$imagesurl/images/$kf_havenew width=13 height=16> 有新的贴子</td>
<td><img src=$imagesurl/images/$pl_havenew width=13 height=16> 有新的贴子</td>
<td><img src=$imagesurl/images/$bm_havenew width=13 height=16> 有新的贴子</td>
<td><img src=$imagesurl/images/$jh_pic width=13 height=16 TITLE="只允许坛主和版主发言和操作"> 只读精华区</td>
<td align=right valign=top rowspan=2>$leomemory</td></tr>
<tr><td><img src=$imagesurl/images/$zg_nonew width=13 height=16> 没有新贴子</td>
<td><img src=$imagesurl/images/$kf_nonew width=13 height=16> 没有新贴子</td>
<td><img src=$imagesurl/images/$pl_nonew width=13 height=16> 没有新贴子</td>
<td><img src=$imagesurl/images/$bm_nonew width=13 height=16> 没有新贴子</td>
<td><img src=$imagesurl/images/$lm_pic width=16 height=16 TITLE="和本论坛友情链接的联盟论坛"> 联盟论坛区</td></tr>
</table>
~;
  }

my $timenow = time ;
$timenow = $timenow + ($timedifferencevalue*3600) + ($timezone*3600);
my $timenow1 = &longdate("$timenow");
my $timenow2 = &shorttime("$timenow");

$output .= qq~</td></tr></table></td></tr></table>~;
    $output .= qq~<img src="" width=9 height=5><br>
<table cellspacing=0 cellpadding=0 width=$tablewidth align=center>
<tr><td>&nbsp;&nbsp;现在时间是 $timenow1 $timenow2 ($basetimes)</td>
<td align=right noWrap>[ <a href=leoboard.cgi?action=delcookieall>删除论坛所设 cookie</a> ] :: [ <a href=leoboard.cgi?action=resetall>标记所有论坛为已读</a> ]&nbsp;</td></tr>
</table><center><br>$adfoot</center>~;

print header(-charset=>gb2312);
&output(
-Title   => $boardname,
-ToPrint => $output,
-Version => $versionnumber
);


sub getonlineno {
	my $where=shift;
	$guests1=0;
	$members1 = 0;
	$output2 = "";
	foreach my $line (@onlinedata) {
	    chomp $line;
	    (my $savedusername, my $no, $no, my $savedwhere, $no, $no, $no, $no, $no) = split(/\t/, $line);
	    (my $lookfor, $no) = split(/\(/,$savedusername);
    	    next if ($lookfor =~ m/\(/);
    	    next if ($lookfor =~ m/\)/);
    	    next if ($lookfor =~ m/\*/);
	    my $wherebaomi=$where."(密)";
	    if (($savedwhere eq $where)||($savedwhere eq $wherebaomi)){
        	my $checkhidden=0;
                foreach (@hiddenmember){
                if ($_=~/^$lookfor/) {
		    $checkhidden=1;
        	    $guests1++;
        	 }
        	}
                if ($checkhidden==0) {
                   $members1++;
                   if ($members1 eq 1) { $output2 .= qq~$savedusername~; }
                   else { $output2 .= qq~，$savedusername~; }
                }
	    }
	}
	$totleonline = $members1 + $guests1;
    	$output2 ="\n\n --= 会员列表（共 $members1 人） =--\n$output2\n" if ($output2 ne "");
}

sub birthday {
    $birthdayuser = "";
    $borncount = 0;
    $nowtime = time;
    $nowtime = &shortdate($nowtime + ($timezone*3600) + ($timedifferencevalue*3600));
    (my $nowy, my $nowm, my $nowd) = split(/\//, $nowtime);
    $filetomakeopen = "${lbdir}data/lbmember3.cgi";
    open (MEMFILE, "$filetomakeopen");
    flock (MEMFILE, 1) if ($OS_USED eq "Unix");
    @memberdata = <MEMFILE>;
    close (MEMFILE);
    foreach (@memberdata) {
	chomp $_;
	(my $users, my $borns) = split(/\t/,$_);
	(my $unowy, my $unowm, my $unowd) = split(/\//, $borns);
	if (($nowm eq $unowm)&&($nowd eq $unowd)) {
            my $usersfilename = $users;
            $usersfilename =~ s/ /\_/g;
	    $usersfilename =~ tr/A-Z/a-z/;
	    $unowy = $nowy - $unowy;
	    $birthdayuser .= qq~<a href="javascript:O9('$usersfilename')" title=祝$unowy岁生日快乐！>$users</a>, ~;
	    $borncount ++;
	}
    }
    chop $birthdayuser;
    chop $birthdayuser;
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
