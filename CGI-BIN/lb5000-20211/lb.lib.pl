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
$versionnumber = "LB5000II v20211";

$maxweiwang = 10 if (($maxweiwang < 5)||($maxweiwang eq ""));

opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
my @memdir = grep(/^members/i, @files2);
$memdir = $memdir[0];
my @msgdir = grep(/^messages/i, @files2);
$msgdir = $msgdir[0];

$ENV{'REMOTE_ADDR'} = $ENV{'HTTP_X_FORWARDED_FOR'} if (($ENV{'REMOTE_ADDR'} eq "127.0.0.1")&&($ENV{'HTTP_X_FORWARDED_FOR'} ne "")&&($ENV{'HTTP_X_FORWARDED_FOR'} ne "unknow"));

sub badwordfile {
  $filetoopen = "$lbdir" . "data/badwords.cgi";
  if (open (FILE, "$filetoopen")) {
#	flock (FILE, 1) if ($OS_USED eq "Unix");
	$badwords = <FILE>;
	close (FILE);
	$badwords=~ s/[\r\t\n\f]//ig;
	$badwords=~ s/\./\\\./ig;
	$badwords=~ s/\(/\\\(/ig;
	$badwords=~ s/\*/\\\*/ig;
	$badwords=~ s/\)/\\\)/ig;
  }
  else { $badwords = "";}
}

sub ipbanned {
  my $term_filetoopen ="$lbdir" . "data/ipbans.cgi";
  if (open(FILE,"$term_filetoopen")) {
#    flock (FILE, 1) if ($OS_USED eq "Unix");
    my @term_bannedmembers = <FILE>;
    close(FILE);
    my $term_bannedmembers = @term_bannedmembers;
    if ($term_bannedmembers > 0) {
	my $term_postipaddress = $ENV{'REMOTE_ADDR'};
	my $term_postipaddress1 = $ENV{'HTTP_X_FORWARDED_FOR'};
	$term_postipaddress = $term_postipaddress1 if (($term_postipaddress1 ne "")&&($term_postipaddress1 ne "unknown"));
	my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$term_postipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
	foreach $term_bannedip (@term_bannedmembers) {
            $term_bannedip =~ s/\r//ig;
	    chomp $term_bannedip;
	    next if ($term_bannedip eq "");
	    if ($term_postipaddress =~ /^$term_bannedip/) { &error(" IP 被禁止&由于你没遵守本站规定！你的 IP ($term_postipaddress) 被禁止！如有疑问，请联系管理员。"); }
	}
     }
   }

   my $term_idfiletoopen ="$lbdir" . "data/idbans.cgi";
   if (open(FILE,"$term_idfiletoopen")) {
#     flock (FILE, 1) if ($OS_USED eq "Unix");
     my @term_idbannedmembers = <FILE>;  
     close(FILE);
     my $term_idbannedmembers = @term_idbannedmembers;
     if ($term_idbannedmembers > 0) {
       my $inmembername = $query->cookie("amembernamecookie");
       if ($inmembername eq "") { $inmembername = "客人"; }
       foreach $term_bannedid (@term_idbannedmembers) {
            $term_bannedid =~ s/\r//ig;
	    chomp $term_bannedid;
	    next if ($term_bannedid eq "");
	    if ($inmembername eq $term_bannedid) { &error(" ID 被禁止&由于你没遵守本站规定！你的 ID ($inmembername) 被禁止！如有疑问，请联系管理员。"); }
       }
     }
   }
}

sub title {
	my $newmail = "<p>";
        if ($mainonoff == 1) { &InMaintenance; }
	if ($inmembername eq "" || $inmembername eq "客人") {
	    $inmembername = "客人";
	    $loggedinas = qq~<b>客人</b>： <a href="$loginprog?forum=$inforum" title="从这里开始进入论坛">登陆</a> | <a href="$registerprog" title="注册了才能发表文章哦！">注册</a> | <a href="$lostpasswordprog" title="好惨啊，忘记密码登陆不了" style="cursor:help">忘记密码</a> | <a href="http://168.263xp.com/elove/index.asp" title="交友中心" target="_blank">交友中心</a> | <a href="$onlineprog" title="看看有谁在线……">在线</a> | <a href="$searchprog?forum=$inforum" title="按关键字、作者来搜寻">搜索</a> | <a href="javascript:openScript('$helpprog',500,400)" title="常见问题的解答">帮助</a>~;
	    if (($regaccess eq "on")&&($thisprog ne "loginout.cgi")&&($thisprog ne $registerprog)&&($thisprog ne $profileprog)&&($thisprog ne "viewavatars.cgi")) {
	    	print header(-cookie=>[$namecookie, $passcookie], -charset=>gb2312);
	    	print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	    	exit;
	    }
	}
	else {
	    my $memberfilename = $inmembername;
	    $memberfilename =~ s/ /\_/g;
	    $memberfilename =~ tr/A-Z/a-z/;
	    my $filetoopen = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
	    open (FILE, "$filetoopen");
	    @allmessages = <FILE>;
	    close (FILE);

	    $unread = 0;
	    foreach (@allmessages) {
		(my $trash, my $readstate) = split(/\t/,$_);
		$unread++ if ($readstate eq "no");
	    }
	    my $intanchumsg = $query->cookie("tanchumsg");
	    my $popnew = '<script language="JavaScript">JavaScript:PopWindow()</script>' if (($newmsgpop eq "on")&&($thisprog ne $threadprog)&&($intanchumsg eq ""));
	    $newmail = qq(<table width=$tablewidth cellpadding=2 cellspacing=0 align=center><tr><td align=right>
<bgsound src=$imagesurl/images/mail.wav border=0>$popnew<a href="javascript:openScript('$messangerprog?action=inbox',420,320)"><img src=$imagesurl/images/newmail.gif border=0><font color=$fonthighlight>你有短消息，请注意查收</font></a>
</td></tr></table>) if $unread;

	    $loggedinas = qq~$inmembername：<a href=$loginprog?forum=$inforum>重登陆</a> | <a href="javascript:openScript('$messangerprog?action=inbox',420,320)" title="悄悄话短讯息中心">消息</a> | <a href="javascript:openScript('friendlist.cgi',420,320)">好友</a> | <a href=$profileprog?action=modify title="编辑您的个人资料">资料</a> | <a href="javascript:openScript('$boardurl/$newpostsprog',500,400)">新贴</a> | <a href=$searchprog?forum=$inforum title="按关键字、作者来搜寻">搜索</a> | <a href="http://168.263xp.com/elove/index.asp" title="交友中心" target="_blank">交友中心</a> | <a href=$onlineprog title="看看有谁在线……">在线</a> | <a href="javascript:openScript('$helpprog',500,400)" title="常见问题的解答">帮助</a> | <a href=$loginprog?action=logout title="在公众的地方上网记得要按退出哦">退出</a>&nbsp;~;
        }
#	&getmember("$inmembername");

        $pluginadd = "";
	if ($inmembername ne "" && $inmembername ne "客人" && $thisprog eq $forumsummaryprog) {
	    my @fileinfo = stat("${lbdir}data/boardskin.cgi");
	    if ((-e "${lbdir}data/boardskin.cgi")&&($fileinfo[7] > 50)) {
		require "${lbdir}data/boardskin.cgi";
		require "${lbdir}addplugin.pl";
	    }
	}

	$loggedinas .= qq~| <a href=$adminprog target=_blank>管理中心</a>~ if (($membercode eq "ad")||($membercode eq "smo"));

	if (($thisprog eq $threadprog)||($thisprog eq $forumsprog)) {
	    $loggedinas .= qq~
<script>
var tc_user="cnleo";
var tc_class="2";
var tc_union="*";
var tc_type="1";
var tc_user;
if (tc_user==null) tc_user="";
_dw('<a href=http://www.textclick.com/viewmain.asp?name='+tc_user+' target=_blank><img WIDTH=0 HEIGHT=0 src=http://stat.t2t2.com/scripts/stat_01.dll?default&user='+tc_user+'&refer='+escape(document.referrer)+'&cur=type2 border=0></a>');
function _dw(string) {document.write(string);}
</script>
~;
	}

	$output = qq~$pluginadd
<table width=$tablewidth align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$titleborder><tr><td>
<table width=100% cellspacing=0 cellpadding=4 border=0>
<tr><td bgcolor=$menubackground background=$imagesurl/images/$menubackpic>
<font color=$menufontcolor>>> 欢迎您，$loggedinas </font></td>
<td bgcolor=$menubackground align=right background=$imagesurl/images/$menubackpic><a href=$homeurl target=_blank><img src=$imagesurl/images/gohome.gif width=48 height=16 border=0></a>&nbsp;
</td></tr></table></td></tr></table>
$newmail
~;
$output .= qq~<base onmouseover="window.status='$statusbar';return true">~ if ($statusbar ne "");
	if ($forumlastvisit) {
	    my $flv= $forumlastvisit + ($timedifferencevalue*3600) + ($timezone*3600);
	    my $flongdate = &longdate("$flv");
	    my $fshorttime = &shorttime("$flv");
	    $lastvisitdata = qq~ 最近访问论坛时间： $flongdate $fshorttime~;
	}
	else {
	    $lastvisitdata = qq~>> $forumname欢迎您的到来 <<~;
	}
	$uservisitdata = qq~
<tr><td valign=bottom align=right><font color=$menufontcolor>
<a href=$forumsprog?forum=$inforum&action=resetposts>标记论坛所有内容为已读</a>　 <a href="javascript:openScript('$helpprog?helpon=阅读标记',500,400)"><img src=$imagesurl/images/$help_blogo border=0></a>&nbsp;<br>$lastvisitdata&nbsp;</font>
</td></tr>
~;
}
sub mischeader {
	local($misctype) = @_;
	if ($#forums < 1) {
	  my $filetoopen = "$lbdir" . "data/allforums.cgi";
	  &winlock($filetoopen);
	  open(FILE, "$filetoopen");
	  flock (FILE, 1) if ($OS_USED eq "Unix");
	  @forums = <FILE>;
	  close(FILE);
	  &winunlock($filetoopen);
	  foreach my $forumline (@forums) {
	    chomp $forumline;
	    next if ($forumline eq "");
	    (my $tempno, my $trash) = split(/\t/,$forumline);
	    if ($inforum eq $tempno) {
		($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forumline);
	    }
	  }
	}
#	$filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
#	&winlock($filetoopen);
#	open(FILE, "$filetoopen");
#	flock (FILE, 1) if ($OS_USED eq "Unix");
#	my @allthreads = <FILE>;
#	close(FILE);
#	&winunlock($filetoopen);

#	foreach my $line (@allthreads) {
#	    ($tempno, $trash) = split(/\t/, $line);
#	    if ($intopic eq $tempno) {
#		($trash, my $topictitle, my $topicdescription, my $threadstate, $trash) = split(/\t/,$line);
#	    }
#	}

	if ($forumgraphic) {
	    $forumgraphic = qq~<a href=$forumsprog?forum=$inforum><img src=$imagesurl/images/$forumgraphic border=0></a>~;
        }
	else {
	    $forumgraphic = qq~<a href=$boardurl/$forumsummaryprog><img src=$imagesurl/images/$boardlogo border=0></a>~;
	}
	&title;
	$inmembername =~ s/\_/ /g;
        $output .= qq~
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
<tr><td width=30% rowspan=2 valign=top>
$forumgraphic
</td><td valign=top>
~;
        if ($indexforum ne "no"){
            $output .= qq~
<font color=$fontcolormisc>
　<img src=$imagesurl/images/closedfold.gif width=15 height=11>　<a href=$forumsummaryprog>$boardname</a><br>
　<img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/closedfold.gif width=15 height=11>　<a href=$forumsprog?forum=$inforum>$forumname</a><br>
　　 <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>　$misctype
~;
        }else{
	    $output .= qq~
<font color=$fontcolormisc>
<img src=$imagesurl/images/closedfold.gif width=15 height=11>　<a href=$forumsprog?forum=$inforum>$forumname</a><br>
<img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>　$misctype
~;
	}
        $output .= qq~
</td>
</tr></table><p>
~;

}

sub moderator {
	if ($#forums < 1) {
	  my $filetoopen = "$lbdir" . "data/allforums.cgi";
	  &winlock($filetoopen);
	  open(FILE, "$filetoopen");
	  flock (FILE, 1) if ($OS_USED eq "Unix");
	  @forums = <FILE>;
	  close(FILE);
	  &winunlock($filetoopen);
	  foreach my $forumline (@forums) {
	    chomp $forumline;
	    next if ($forumline eq "");
	    (my $tempno, my $trash) = split(/\t/,$forumline);
	    if ($inforum eq $tempno) {
		($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forumline);
	    }
	  }
	}
	$forummoderator =~ s/\, /\,/gi;
	$forummoderator =~ s/ \,/\,/gi;
	my @forummodnames = split(/\,/, $forummoderator);
	my $nomods = @forummodnames;
	$inmembmod = "no";
    if ($nomods ne "0") {
$modoutput .= qq~
<SCRIPT LANGUAGE="JavaScript">
<!--
function menu1(){
var URL = document.modjump.jumpto1.options[document.modjump.jumpto1.selectedIndex].value;
window.open(URL);
}
// -->
</SCRIPT>
<form action="$profileprog" method="post" name="modjump"><img src=$imagesurl/images/team2.gif width=19 height=19 align=absmiddle>
<input type=hidden name="action" value="show">
<select name="jumpto1" onchange="menu1()">
<option value="#">本论坛版主：</option>
<option value="#">------------</option>
~;
	foreach my $name (@forummodnames) {
	  chomp $name;
	  my $cleanedmodname = $name;
	  $cleanedmodname =~ s/ /\_/g;
	  $cleanedmodname =~ tr/A-Z/a-z/;
	  $inmembmod = "yes" if (lc($inmembername) eq lc($name));
    	  $modoutput .= qq~<option value="$profileprog?action=show&member=$cleanedmodname">$name</option>~;
	}
	$modoutput .= qq~</select>\n~;
    }
    unless ($inmembmod eq "yes") { $inmembmod = "no"; }
}
sub getforum {
	my $inforum = shift;
	if ($#forums < 1) {
	  $filetoopen = "$lbdir" . "data/allforums.cgi";
	  &winlock($filetoopen);
	  open(FILE, "$filetoopen");
          flock(FILE, 1) if ($OS_USED eq "Unix");
	  @forums = <FILE>;
	  close(FILE);
	  &winunlock($filetoopen);
	  foreach my $forumline (@forums) {
	    chomp $forumline;
	    next if ($forumline eq "");
	    (my $tempno, my $trash) = split(/\t/,$forumline);
	    if ($inforum eq $tempno) {
		($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forumline);
	    }
	  }
	}
}

sub getmember {
	my $nametocheck = shift;
	$nametocheck =~ s/ /\_/g;
	$nametocheck =~ tr/A-Z/a-z/;
	$userregistered = "";
	undef $filedata;
	my $filetoopen = "$lbdir" . "$memdir/$nametocheck.cgi";
	$filetoopen = &stripMETA($filetoopen);
	if (-e $filetoopen) {
	    &winlock($filetoopen);
            open(FILE3,"$filetoopen");
            flock(FILE3, 1) if ($OS_USED eq "Unix");
            $filedata = <FILE3>;
            close(FILE3);
	    &winunlock($filetoopen);
	    chomp($filedata);
	    ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $aolname, $icqnumber ,$location ,$interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $addjy, $meili, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $useradd1, $useradd2, $jhmp, $useradd3,$useradd4,$useradd5,$useradd6,$useradd7,$useradd8) = split(/\t/,$filedata);
	    $timedifferencevalue=$timedifference;
	    ($numberofposts, $numberofreplys) = split(/\|/,$numberofposts);
            chomp $privateforums;
            if($privateforums) {
		@private = split(/&/,$privateforums);
		foreach $accessallowed (@private) {
		    chomp $accessallowed;
		    ($access, $value) = split(/=/,$accessallowed);
		    $allowedentry{$access} = $value;
		}
	    }
	}
	else { $userregistered = "no"; }
}

sub error {
	print header(-charset=>gb2312);
	my $errorinfo = shift;
	(my $where, my $errormsg) = split(/\&/, $errorinfo);
	$inmembername = cookie("amembernamecookie");
	$inpassword = cookie("apasswordcookie");
	$inmembername =~ s/\///g;
	$inmembername =~ s/\.\.//g;
	$inmembername =~ s/\\//g;

	&title;
	$output .= qq~
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
<tr><td width=30% rowspan=2 valign=top><img src="$imagesurl/images/$boardlogo"></td>
<td valign=top>
~;
	if ($indexforum ne "no"){
	    $output .= qq~
<font color=$fontcolormisc>
　<img src=$imagesurl/images/closedfold.gif width=15 height=11>　<a href="$forumsummaryprog">$boardname</a><br>
　<img src="$imagesurl/images/bar.gif" width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>　错误： $where
~;
	}else{
	    $output .= qq~<font color=$fontcolormisc><img src=$imagesurl/images/openfold.gif width=15 height=11>　错误： $where~;
	}
	$output .= qq~
	    </td></tr>
	   </table>
	   <p>
	   <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    	      <tr><td>
		<table cellpadding=6 cellspacing=1 border=0 width=100%>
		<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>错误： $where</b></font></td></tr>
		<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
                  <b>关于$where错误的详细原因：</b>
                  <ul>
                  <li><b>$errormsg</b>
                  <li>您是否需要查看<a href="javascript:openScript('$helpprog',500,400)">帮助文件</a>?
                  </ul>
                  <b>产生$where错误的可能原因：</b>
                  <ul>
                  <li>密码错误<li>用户名错误<li>您不是<a href="$registerprog" >注册</a>用户
                  </ul>
                  <br><br>
                  <center><font color=$fontcolormisc> << <a href="javascript:history.go(-1)">返回上一页</a></center>
                </tr></td>
                </table>
                </td></tr></table>
	~;
        &output(
          -Title   => $boardname,
          -ToPrint => $output,
          -Version => $versionnumber
        );
        exit;
}

sub uplogintime {
        my($nametocheck,$visit) = @_;
	my $nametochecktemp = $nametocheck;
	$nametocheck =~ s/ /\_/g;
	$nametocheck =~ tr/A-Z/a-z/;
	$userregistered = "";
	my $filetoopen = "$lbdir" . "$memdir/$nametocheck.cgi";
	$filetoopen = &stripMETA($filetoopen);
	if (-e $filetoopen) {
	    &winlock($filetoopen);
	    open(FILE6,"$filetoopen");
	    flock (FILE6, 1) if ($OS_USED eq "Unix");
            my $filedata = <FILE6>;
            close(FILE6);
	    chomp($filedata);
	    (my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $aolname, my $icqnumber ,my $location ,my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $userflag,my  $userxz, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno,my  $addjy,my  $meili, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $useradd1,my  $useradd2, my $jhmp,my $useradd3,my $useradd4,my $useradd5,my $useradd6, my $useradd7, my $useradd8) = split(/\t/,$filedata);

    	    $visitno++ if ($visit eq "T");
	    if (($membername ne "")&&($password ne "")) {
	      if (open(FILE6,">$filetoopen")) {
	      flock (FILE6, 2) if ($OS_USED eq "Unix");
	      $lastgone=time;
	      print FILE6 "$nametochecktemp\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t\n";
	      close(FILE6);
	      }
	    }
	    &winunlock($filetoopen);
	}
}
sub numerically { $a <=> $b }
sub alphabetically { lc($a) cmp lc($b) }
sub whosonline {
	local($instruct) = @_;
	(my $tempusername, my $where, my $method, my $where2) = split(/\t/, $instruct);
	my $ipaddress  = $ENV{'REMOTE_ADDR'};
	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$trueipaddress = $ipaddress if (($trueipaddress eq "")||($trueipaddress eq "unknown"));
	my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$trueipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
	my $ipall      = "$ipaddress=$trueipaddress";
	my $tempusername1=$tempusername;
	if ($tempusername eq "客人") {
	    $tempusername = "客人($ipaddress)";
	}
	$guests = 0;
	$members = 0;

	undef @onlinedata;
	undef @onlinedata1;
	$currenttime = time;
	$membergone = 30 if ($membergone< 5);
	my $userexpire = $currenttime - ($membergone * 60);
	my $memberprinted = "no";
	$screenmode=7 if ($screenmode eq "");

     my $filetoopen = "$lbdir" . "data/onlinedata.cgi";
     my @fileinfo = stat("$filetoopen");
     my $filelength1 = $fileinfo[7];
        @fileinfo = stat("$filetoopen.cgi");
     my $filelength2 = $fileinfo[7];
     if ((($filelength1 <60)&&($filelength2 > 60)&&($currenttime-$fileinfo[9] <= 300))||(($currenttime-$fileinfo[9] <= 300)&&($filelength2-$filelength1>1200)&&($filelength2<3000))||(($currenttime-$fileinfo[9] <= 300)&&($filelength2 > $filelength1*2)&&($filelength2>3000)&&($filelength2<50000))||(($currenttime-$fileinfo[9] <= 300)&&($filelength2*2 > $filelength1*3)&&($filelength2>50000))) {
	if (open(FILE5,"$filetoopen.cgi")) {
	  @onlinedata1 = <FILE5>;
	  close(FILE5);
	  $onlinedatanumber=@onlinedata1;
	}
     }
     else {
        &winlock($filetoopen);
        if (open(FILE5,"$filetoopen")) {
	  flock (FILE5, 1) if ($OS_USED eq "Unix");
	  @onlinedata1 = <FILE5>;
	  close(FILE5);
	  $onlinedatanumber=@onlinedata1;
	}
        &winunlock($filetoopen);
     }
     
        foreach my $line (@onlinedata1) {
                chomp $line;
                (my $savedusername, my $savedcometime, my $savedtime, my $savedwhere, my $savedipaddress, my $saveosinfo, my $savebrowseinfo, my $savedwhere2, my $fromwhere, my $savemembercode, $savehidden) = split(/\t/, $line);
 		(my $lookfor, my $no) = split(/\(/,$savedusername);
                next if ((length($savedusername)>12)&&($lookfor ne "客人"));
                $fromwhere = &lbhz("$fromwhere", 30) if (length($fromwhere) > 30);
                $saveosinfo = &lbhz("$saveosinfo", 15) if (length($saveosinfo) > 15);
                $savebrowseinfo = &lbhz("$savebrowseinfo", 28) if (length($savebrowseinfo) > 28);
    		$lookfor =~ s/[\*\)\(]//isg;

                $savedusername =~ s/\_/ /g;
                $tempusername =~ s/\_/ /g;

		if ($userexpire <= $savedtime) {
                    if ((lc($savedusername) eq lc($tempusername))||(($savedusername eq "客人($ipaddress)")&&($ipall eq $savedipaddress))) {
                         if ((($currenttime - $savedtime) <= $banfreshtime - 1)&&($savedwhere eq $where)&&($savedwhere2 eq $where2)&&(($thisprog eq $postprog)||($thisprog eq $forumsummaryprog)||($thisprog eq $forumsprog)||($thisprog eq $threadprog))) {
                             print header(-charset=>gb2312);
                             print "<BR>服务器忙，请 $banfreshtime 秒后按刷新键继续。<BR><BR>出错原因：你刷新页面过快，或者你打开了过多窗口来浏览本网站。";
                             exit;
                         }
                         if ($memberprinted eq "no") {
                             $savehidden = $hidden if ($hidden ne "");
                             $tempdata = "$tempusername\t$savedcometime\t$currenttime\t$where\t$ipall\t$saveosinfo\t$savebrowseinfo\t$where2\t$fromwhere\t$membercode\t$savehidden\t" ;
			     $osinfo=$saveosinfo;
	   		     $browseinfo=$savebrowseinfo;
                             $tempdata =~ s/[\n\r]//isg;
                             $fromwhere1 = $fromwhere;
                             push(@onlinedata,$tempdata);
                             $memberprinted = "yes";
                         }
                    }
                    else {
                         $line =~ s/[\n\r]//isg;
                         push(@onlinedata,$line);
                    }
                }
                else {
                	&uplogintime("$savedusername","") if (($savedusername !~ /^客人/)&&(($thisprog eq $forumsprog)||($thisprog eq $forumsummaryprog)));
                }
        }

        if ($memberprinted eq "no") {
	   if (($onlinedatanumber >= $arrowonlinemax)&&($arrowonlinemax > 0)&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "mo")) {
       	      print header(-charset=>gb2312);
              print "<BR>服务器忙，已经超出论坛允许的最大在线人数。<BR><BR>目前论坛在线 $onlinedatanumber 人，最大允许同时在线 $arrowonlinemax 人。";
              exit;
           }
	   require "${lbdir}testinfo.pl";
	   $osinfo=&osinfo();
	   $browseinfo=&browseinfo();
           my $fromwhere = &ipwhere("$trueipaddress");
           my $tempdata = "$tempusername\t$currenttime\t$currenttime\t$where\t$ipall\t$osinfo\t$browseinfo\t$where2\t$fromwhere\t$membercode\t$hidden\t" ;
	   if ((($thisprog eq $forumsprog)||($thisprog eq $forumsummaryprog))&&($recordviewstat eq "yes")) {
	     $filetomake = "$lbdir" . "data/stats.cgi";
             my $filetoopens = &lockfilename($filetomake);
  	     if (!(-e "$filetoopens.lck")) {
	        if (open(LOGFILE, ">>$filetomake")) {
	        print LOGFILE "$currenttime|$browseinfo|$osinfo|$fromwhere|\n";
	        close(LOGFILE);
	        }
             }

	     $filetomake = "$lbdir" . "data/refers.cgi";
             $filetoopens = &lockfilename($filetomake);
	     $laiyuan = $ENV{'HTTP_REFERER'};
	     if ($noself eq "on") {
	     	$recoder=1;
	     }
	     else {
	        if ($laiyuan =~ m/$homeurl/isg) {
	            $recoder=0;
	        }
	        else {
	            $recoder=1;
	        }
	     }
  	     if ((!(-e "$filetoopens.lck"))&&($laiyuan ne "")&&($laiyuan !~ m/unknow /i)&&($laiyuan !~ m/$boardurl/isg)&&($recoder==1)) {
		if (-e "$filetomake") {
	          &winlock($filetomake) if ($OS_USED eq "Nt");
	          open(LOGFILE, "$filetomake");
                  flock(LOGFILE, 1) if ($OS_USED eq "Unix");
	          my @refersall= <LOGFILE>;
	          close(LOGFILE);
		  my $refersall = @refersall;
      		  if ($refersall<$newrefers) {  $newrefers=$refersall; }  else {  $newrefers--; }
	          if (open(LOGFILE, ">$filetomake")) {
                  flock(LOGFILE, 2) if ($OS_USED eq "Unix");
                  unless (($noself eq "off")&&($laiyuan =~ m/$homeurl/isg)) {
	              print LOGFILE "$laiyuan|$ipall|$currenttime|\n";
	          }
		  for ($i=0;$i<$newrefers;$i++) {
         	    print LOGFILE $refersall[$i];
      		  }
	          close(LOGFILE);
	          }
	          &winunlock($filetomake) if ($OS_USED eq "Nt");
	        }
	        else {
	           if (open(LOGFILE, ">>$filetomake")) {
	           print LOGFILE "$laiyuan|$ipall|$currenttime|\n";
	           close(LOGFILE);
	           }
	        }
             }
           }
           $fromwhere1 = $fromwhere;
           &uplogintime("$tempusername","T") if ($tempusername !~ /^客人/);
           $tempdata =~ s/[\n\r]//isg;
           push(@onlinedata,$tempdata);
        }

        my $filetoopen = "$lbdir" . "data/onlinedata.cgi";
        $filetoopens = &lockfilename($filetoopen);
  	if (!(-e "$filetoopens.lck")) {
	    &winlock($filetoopen);
            if (open(FILE4,">$filetoopen")) {
              flock(FILE4, 2) if ($OS_USED eq "Unix");
              foreach $line (@onlinedata) {
                chomp $line;
                print FILE4 "$line\n" if ($line ne "");
	      }
              close(FILE4);
            }
            if ($currenttime-$fileinfo[9] >= 120) {
             if (open(FILE4,">$filetoopen.cgi")) {
              flock(FILE4, 2) if ($OS_USED eq "Unix");
              foreach $line (@onlinedata) {
                chomp $line;
                print FILE4 "$line\n" if ($line ne "");
	      }
              close(FILE4);
             }
            }
            &winunlock($filetoopen);
        }
	if (($thisprog eq $forumsummaryprog)||($thisprog eq $forumsprog)||($thisprog eq "index.cgi")) {
	    $filetomake = "$lbdir" . "data/counter.cgi";

	    my $countfiles=1 if (-e "$filetomake");

	    $onlinemax = @onlinedata;

	    &winlock($filetomake);
	    open(FILE,"$filetomake");
	    flock (FILE, 1) if ($OS_USED eq "Unix");
	    my $count = <FILE>;
	    close(FILE);
	    &winunlock($filetomake);

	    ($count1,$count2,$onlinemax1,$onlinemaxtime1) = split(/\t/, $count);
	    $onlinemaxtime1 = $currenttime if ($onlinemaxtime1 eq "");
	    $count2++;
	    $count1++ if ($memberprinted eq "no");
	    $count1=0 if ($count1 eq "");
	    if ($onlinemax < $onlinemax1) {
	        $onlinemax = $onlinemax1;
	        $onlinemaxtime = $onlinemaxtime1;
	    }
	    else {
	        $onlinemaxtime = $currenttime;
	    }
	    unless (($count2 eq 1)&&($countfiles eq 1)) {
              $filetoopens = &lockfilename($filetomake);
	      if (!(-e "$filetoopens.lck")) {
	      	if (($count1 > 0)&&($count2 > 0)&&($onlinemax > 0)&&($onlinemax <= 3000)) {
	            &winlock($filetomake);
	            if (open(FILE, ">$filetomake")) {
	                flock (FILE, 2) if ($OS_USED eq "Unix");
	                print FILE "$count1\t$count2\t$onlinemax\t$onlinemaxtime\t\n";
	                close(FILE);
	            }
	            &winunlock($filetomake);
	        }
	      }
	    }
	}
        undef @onlinedata1;
        if ($method eq "both") {
            $memberoutput ="　";
            $memberoutput1 ="　";
            my $lengthmark= 0;

            foreach my $line (@onlinedata) {
                chomp $line;
		$line =~ s/＊＃！＆＊//;
                (my $savedusername, my $savedcometime, my $savedtime, my $savedwhere, my $postipaddresstemp, my $saveosinfo, my $savebrowseinfo, my $savedwhere2, my $fromwhere, my $memcod, my $hiddened) = split(/\t/, $line);
		if ($memcod eq "ad") {$mspic=$onlineadmin;}
		    elsif ($memcod eq "smo") {$mspic=$onlinesmod;}
		    elsif ($memcod eq "mo")  {$mspic=$onlinemod;}
		    else  {$mspic=$onlinemember;}

 		(my $lookfor, my $no) = split(/\(/,$savedusername);
		($savedipaddress,$truepostipaddress) = split(/\=/,$postipaddresstemp);

		$fromwhere = "已设置保密" unless (($pvtip eq "on")||($membercode eq "ad")||(($membercode eq 'smo')&&($smocanseeip eq "no")));

		(my $ip1, my $ip2, my $ip3, my $ip4) = split(/\./,$savedipaddress);
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
		    $savedcometime = &dateformatshort($savedcometime + ($timezone*3600) + ($timedifferencevalue*3600));
		    $savedtime = &dateformatshort($savedtime + ($timezone*3600) + ($timedifferencevalue*3600));

		    $savedwhere2 =~s/\<a \s*(.*?)\s*\>\s*(.*)/“$2”/isg;
		    $savedwhere2 =~s/\<\/a\>//isg;
		    $savedwhere2 =~s/\<b\>//isg;
		    $savedwhere2 =~s/\<\/b\>//isg;
		    $savedwhere2 =~s/\"/\\\"/;

                my $guestmode=$screenmode*2-1;
                if (((($hiddened eq 1)&&($membercode ne "ad"))||($savedusername =~ /^客人/))&&(lc($savedusername) ne lc($inmembername))) {
                   $guests++;
		    $XA = $XB =  '';
		   if ((lc($savedusername) eq lc($inmembername))||($savedusername eq "客人($trueipaddress)")) {
		    	$XA = "<font color=$onlineselfcolor>";
		    	$XB = '</font>';
		    	$online_self = $onlineguest;
		   }
                   if ($savedusername !~ /^客人/) {
		     $memberoutput1 .= qq~<img src=$imagesurl/images/$onlineguest width=12 height=11 alt=请勿打扰！><a href=# nowarp TITLE=\"来访时间：$savedcometime\n活动时间：$savedtime\nＩＰ地址：$savedipaddress\n来源鉴定：$fromwhere\">$XA隐身$XB</a>　~;
                     $memberoutput1 .= qq~<br>　~ if ($guests == int($guests/$guestmode)*$guestmode);
		    }
		    else {
		     $memberoutput1 .= qq~<img src=$imagesurl/images/$onlineguest width=12 height=11 alt=快注册呀！><a href=# nowarp TITLE=\"目前位置：$savedwhere\n目前动作：$savedwhere2\n来访时间：$savedcometime\n活动时间：$savedtime\n操作系统：$saveosinfo\n浏 览 器：$savebrowseinfo\nＩＰ地址：$savedipaddress\n来源鉴定：$fromwhere\">$XA客人$XB</a>　~;
                     $memberoutput1 .= qq~<br>　~ if ($guests == int($guests/$guestmode)*$guestmode);
		    }
                }
                else {
                    $members++;
                    my $spaces = "";
                    my $cleanmember = $savedusername;
                    $cleanmember =~ s/ /\_/g;
		    $cleanmember =~ tr/A-Z/a-z/;
                    my $spacetemp= 12 - length($cleanmember);
		    my $spacetemp1 = int($spacetemp/2);
		    $spaces .= " " if ($spacetemp ne $spacetemp1*2);
		    for (my $i=1;$i<=$spacetemp1;$i++) { $spaces .= "　"; }
		    $lengthmark =$lengthmark+4+length($cleanmember);
	     	    $XA = $XB =  '';
		    if (lc($savedusername) eq lc($inmembername)) {
		    	$XA = "<font color=$onlineselfcolor>";
		    	$XB = '</font>';
		    	$online_self = $mspic;
		    }
		    $hiddeninfo = "";
		    $hiddeninfo = "\n-=> 目前处于隐身状态 <=-" if ($hiddened eq 1);
                    $memberoutput .= qq~<a href="javascript:openScript('messanger.cgi?action=new&touser=$cleanmember',420,320)"><img src=$imagesurl/images/$mspic border=0 width=12 height=11 alt="给$savedusername发送一个短消息"></a><a href="javascript:O9('$cleanmember')" nowarp TITLE=\"目前位置：$savedwhere\n目前动作：$savedwhere2\n来访时间：$savedcometime\n活动时间：$savedtime\n操作系统：$saveosinfo\n浏 览 器：$savebrowseinfo\nＩＰ地址：$savedipaddress\n来源鉴定：$fromwhere$hiddeninfo\">$XA$savedusername$XB</a>$spaces　~;

		    if ($members == int($members/$screenmode)*$screenmode) {
                        $memberoutput .= qq~<br>　~;
 		    }
                }
            }
    	    $memberoutput1 = "" if (($members > 50)&&($guests > 20));
	    $memberoutput1 = "" if ($memberoutput1 eq "　");
	    $memberoutput = "" if ($memberoutput eq "　");

    	    $memberoutput = "$memberoutput<BR>" if (($memberoutput ne "")&&($memberoutput1 ne ""));
            $memberoutput = "$memberoutput$memberoutput1";
        }
}

sub lbhz{
my($str,$maxlen) = @_;
if (length($str) <= $maxlen){    return $str;    }
if (substr($str,0,$maxlen-4) =~ /^([\000-\177]|[\200-\377][\200-\377])*([\000-\177]|[\200-\377][\200-\377])$/ ){
return substr($str,0,$maxlen-4)." ...";
}else{
return substr($str,0,$maxlen-5)."　...";
}
}

sub cleaninput {
    my $text = shift;
    $text =~ s/\&nbsp;/ /g;
    $text =~ s/\@ARGV/\&\#64\;ARGV/isg;
    $text =~ s/\;/\&\#59\;/isg;
    $text =~ s/\&/\&amp;/g;
    $text =~ s/\&amp;\#/\&\#/isg;
    $text =~ s/<script>/\&lt;script\&gt;/ig;
    $text =~ s/"/\&quot;/g;
    $text =~ s/  / \&nbsp;/g;
    $text =~ s/</\&lt;/g;
    $text =~ s/>/\&gt;/g;
    $text =~ s/[\t\r]//g;
    $text =~ s/  / /g;
    $text =~ s/\n\n/<p>/g;
    $text =~ s/\n/<br>/g;
    return $text;
}
sub unclean {
    my $text = shift;
    $text =~ s/\&amp;/\&/g;
    $text =~ s/\&quot;/"/g;
    $text =~ s/ \&nbsp;/　/g;
    return $text;
}
sub unHTML {
    my $text = shift;
    $text =~ s/<!--(.|\n)*-->//g;
    $text =~ s/\&/\&amp;/g;
    $text =~ s/<script>/\&lt;script\&gt;/ig;
    $text =~ s/"/\&quot;/g;
    $text =~ s/  / \&nbsp;/g;
    $text =~ s/</\&lt;/g;
    $text =~ s/>/\&gt;/g;
    return $text;
}
sub HTML {
    my $text = shift;
    $text =~ s/\&amp;/\&/g;
    $text =~ s/\&quot;/"/g;
    $text =~ s/ \&nbsp;/　/g;
    $text =~ s/\&lt;/</g;
    $text =~ s/\&gt;/>/g;
    return $text;
}
sub cleanarea {
    my $text = shift;
    $text =~ s/<!--(.|\n)*-->//g;
    $text =~ s/\&/\&amp;/g;
    $text =~ s/<script>/\&lt;script\&gt;/ig;
    $text =~ s/"/\&quot;/g;
    $text =~ s/  / \&nbsp;/g;
    $text =~ s/</\&lt;/g;
    $text =~ s/>/\&gt;/g;
    $text =~ s/[\t\r]//g;
    $text =~ s/  / /g;
    $text =~ s/\n\n/<p>/g;
    $text =~ s/\n/<br>/g;
    return $text;
}
sub stripMETA {
    my $file = shift;
    $file =~ s/[<>\^\(\)\{\}\$\n\r"\`\&\;\|\*\?]//g;
    return $file;
}
sub dateformat {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    my @months = ('01','02','03','04','05','06','07','08','09','10','11','12');
    $mon = $months[$mon];
    my $ampm = "am";
    if ($hour > 11) {  $ampm = "pm"; }
    if ($hour > 12) { $hour = $hour - 12; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min = "0$min"; }
    if ($sec < 10) { $sec = "0$sec"; }
    if ($mday < 10) { $mday = "0$mday"; }
    $year = $year + 1900;
    return "$year/$mon/$mday $hour:$min$ampm";
}
sub longdate {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    my @months = ('01','02','03','04','05','06','07','08','09','10','11','12');
    $year = $year + 1900;
    if ($mday < 10) { $mday = "0$mday"; }
    return "$year年$months[$mon]月$mday日";
}
sub shortdate {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    $mon++;
    if ($mon < 10) { $mon = "0$mon"; }
    if ($mday < 10) { $mday = "0$mday"; }
    $year = $year + 1900;
    return "$year/$mon/$mday";
}
sub shorttime {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    $mon++;
    my $ampm = "am";
    if ($hour > 11) {  $ampm = "pm"; }
    if ($hour > 12) { $hour = $hour - 12; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min = "0$min"; }
    if ($sec < 10) { $sec = "0$sec"; }
    return "$hour:$min$ampm";
}
sub dateformatshort {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    my @months = ('01','02','03','04','05','06','07','08','09','10','11','12');
    $mon = $months[$mon];
    if ($hour < 10) { $hour = "0$hour"; }
    if ($mday < 10) { $mday = "0$mday"; }
    if ($min < 10) { $min = "0$min"; }
    if ($sec < 10) { $sec = "0$sec"; }
    $year = $year + 1900;
    return "$year/$mon/$mday $hour:$min";
}
sub joineddate {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    my @months = ('01','02','03','04','05','06','07','08','09','10','11','12');
    $year = $year + 1900;
    if ($mday < 10) { $mday = "0$mday"; }
    return " $year/$months[$mon]/$mday";
}
sub output {
        my %args = (
        -Title        => "",
        -ToPrint      => "",
        -Version      => "",
        @_,
        );
        my $title         = $args{-Title};
        my $output        = $args{-ToPrint};
        my $versionnumber = $args{-Version};
        my $filetoopen = "$lbdir" . "data/template.cgi";
        open(FILE,"$filetoopen");
        my @templatedata = <FILE>;
        close(FILE);
        my $boardcopyright = qq(&copy\; $copyrightinfo) if $copyrightinfo;

        $boardcopyright =~ s/&lt;/</g; $boardcopyright =~ s/&gt;/>/g; $boardcopyright =~ s/&quot;/\"/g;
        my $copyright = qq~<center>~;
        if ($thisprog eq $threadprog) {
	    $adfoot = &HTML("$adfoot");
	    $copyright .= $adfoot;
	}
	$copyright .= qq~<hr width=380 size=1><table width=80% align=center cellpadding=0 cellspacing=0><tr><td align=center>~;

	if ($thisprog eq $threadprog) {
	    $copyright .= qq~
<script>
var tc_user="cnleo";
var tc_class="2";
var tc_union="*";
var tc_type="1";
var tc_user;
if (tc_user==null) tc_user="";
_dw('<a href=http://www.textclick.com/viewmain.asp?name='+tc_user+' target=_blank><img WIDTH=0 HEIGHT=0 src=http://stat.t2t2.com/scripts/stat_01.dll?default&user='+tc_user+'&refer='+escape(document.referrer)+'&cur=type2 border=0></a>');
function _dw(string) {document.write(string);}
</script>
~;
	}
	$boardlastinfo =qq~<BR>本论坛言论纯属发表者个人意见，与<font color=$fonthighlight><b> $boardname </b></font>立场无关<br>~ if ($dispboardsm ne "no");
        $copyright .= qq~<font color=$fontcolormisc>$boardcopyright　 版本： <a href="http://www.leoboard.com/download.htm">$versionnumber</a>$boardlastinfo</font></td></tr></table></center>~;

if ($coolwin eq "1") {
$coolwinn = qq~<script language="javaScript" type="text/javascript" SRC="$imagesurl/images/pz_chromeless_2.1.js"></SCRIPT>
<script>
function openScript(theURL, W, H) {
var bIsIE5 = navigator.userAgent.indexOf('IE 5.5')  > -1;
if (bIsIE5) {
wname ="Leoboard5000" 
windowCERRARa = "$imagesurl/close_a.gif"  
windowCERRARd = "$imagesurl/close_d.gif"
windowCERRARo = "$imagesurl/close_o.gif"
windowNONEgrf = "$imagesurl/none.gif" 
windowCLOCK = "$imagesurl/clock.gif" 
windowREALtit = "------| Leoboard Windows V2.1 |" 
windowTIT = "<font style=font-size:12px;font-family:Verdana>------| 雷傲论坛　http://www.LeoBoard.com/ |</font>" 
windowBORDERCOLOR = "#000000" 
windowBORDERCOLORsel = "#111111" 
windowTITBGCOLOR = "#D7DCD9" 
windowTITBGCOLORsel = "#FFFFFF" 
winBGCOLOR = "#D7DCD9"
openchromeless(theURL, wname, W, H, windowCERRARa, windowCERRARd, windowCERRARo, windowNONEgrf, windowCLOCK, windowTIT, windowREALtit , windowBORDERCOLOR, windowBORDERCOLORsel, windowTITBGCOLOR, windowTITBGCOLORsel)
}
}
</script>
~;
}
else {$coolwinn = "";}
$coolmeta = qq~<META http-equiv="Page-Enter" content="revealTrans(Transition=$cinoption,Duration=$timetoshow)">
<META http-equiv="Page-Exit" content="revealTrans(Transition=$cinoption,Duration=$timetoshow)">
~ if ($pagechange eq "yes");
        foreach my $line (@templatedata) {
            $line =~ s/\$lbbody/$lbbody/sg;
            $line =~ s/\$page_title/$title/sg;
            $line =~ s/\$imagesurl/$imagesurl\/images/sg;
            $line =~ s/\$lbboard_main/$output\n\n$copyright\n/sg;
            $line =~ s/\$coolwin/$coolwinn/isg;
            $line =~ s/\$coolmeta/$coolmeta/isg;
            print $line;
        }
        exit;
}
sub helpfiles {
    my $helptype = shift;
    my $helpurl = qq~<a href="javascript:openScript('help.cgi?helpon=$helptype',500,400)">~;
    return $helpurl;
}
sub doemoticons {
	my $post = shift;
	if ($#emoticondata < 1) {
          open (FILE, "${lbdir}data/lbemot.cgi");
#    	  flock (FILE, 1) if ($OS_USED eq "Unix");
          @emoticondata = <FILE>;
	  close (FILE);
	}
	chomp @emoticondata;

        foreach $picture (@emoticondata) {
            $smileyname = $picture;
            $smileyname =~ s/\.gif$//g;
            for (my $i=1;$i<=$maxsmail;$i++) {
                $post =~ s/\:$smileyname\:/\<img src=$imagesurl\/emot\/$picture>/is;
            }
            $post =~ s/ \:$smileyname\://isg;
            $post =~ s/\:$smileyname\://isg;
            $post =~ s/\&nbsp;\:$smileyname\://isg;
      }
        return $post;
}

sub lockfilename{
    my ($lockfilename) = shift;
    $lockfilename =~ s/\\/\//isg;
    $lockfilename =~ s/\://isg;
    $lockfilename =~ s/\//\_/isg;
    $lockfilename = "$lbdir" . "lock/$lockfilename";
}

sub winlock{
    my ($lockfile) = shift;
    my $i = 0;
    $lockfile =~ s/\\/\//isg;
    $lockfile =~ s/\://isg;
    $lockfile =~ s/\//\_/isg;
    $lockfile = "$lbdir" . "lock/$lockfile";
    while (-e "$lockfile.lck") {
	last if ($i >= 177);
	select(undef,undef,undef,0.1);
	$i++;
    }
    open (LOCKFILE, ">$lockfile.lck");
    close (LOCKFILE);
}
sub winunlock{
    my ($lockfile) = shift;
    $lockfile =~ s/\\/\//isg;
    $lockfile =~ s/\://isg;
    $lockfile =~ s/\//\_/isg;
    $lockfile = "$lbdir" . "lock/$lockfile";
#    chmod(0777,"$lockfile.lck");
    unlink("$lockfile.lck");
}

sub InMaintenance {
    $title = "论坛暂时关闭！";
    $line1=&HTML($line1);
    $line1 =~ s/\n/<BR>/isg;
    $output .= qq~
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
<tr><td width=30% rowspan=2><img src="$imagesurl/images/$boardlogo" border=0></td>
<td valign=middle align=left><font face="$font" color=$fontcolormisc size=2>
　<img src="$imagesurl/images/closedfold.gif" border=0>$boardname　--　论坛维护中
</td><div align="center">
<center><br>
<table border="0" cellpadding="0" cellspacing="0" width="80%" bgcolor="#fdfdfd">
<tr><td width="100%">
<p align="center"><b><font  color="#FF0000" size="4"><br>论坛暂时关闭<br><br>现在正在维护，请稍后访问！<br><br><br>
</font><font face="宋体" color="#FF0000">$line1<br>
</tr></table></center></div>
<tr><td valign=bottom align=right>&nbsp; $helpurl</td></tr></table><br>
~;

print header(-charset=>gb2312);
&output(
       -Title   => "$boardname",
       -ToPrint => $output,
       -Version => $versionnumber
       );
exit;
}

sub lbagent {
    my $out="";
    my $url=shift;
    $url =~ m@http://(.*?)/(.*)@;
    my ($host,$path) = ($1,$2);
    my $port = 80;
    if ($host =~ /(.*):(\d+)/) {
	$host = $1;
	$port = $2;
    }
    my $file;
    if ($path =~ m@.*/(.*)@) {
	$file = $1;
    } else {
	$file = $path;
    }
    my ($name,$aliases,$addrtype,$len,@addrs) = gethostbyname($host);
    my ($a,$b,$c,$d) = unpack("C4",$addrs[0]);
    my $that = pack('S n C4 x8',2,$port,$a,$b,$c,$d);
    select (sock);
    $|=1;
    select (STDOUT);
    socket(sock,2,1,0);
    my $result = connect(sock,$that);
    if ($result != 1) {
	$out="连接远程服务器错误,请检查网络!";
    } else {
	print sock "GET /$path HTTP/1.1\r\n";
	print sock "Host: $host\r\n";
	print sock "Accept: */*\r\n";
	print sock "User-Agent: Leoboard Agent 1.0 By hanwei\r\n";
	print sock "Pragma: no-cache\r\n";
	print sock "Cache-Control: no-cache\r\n";
	print sock "Connection: close\r\n";
	print sock "\r\n";
	recv(sock,$out,4096,0);
	recv(sock,$out1,4096,0);
	recv(sock,$out2,4096,0);
	recv(sock,$out3,4096,0);
	$out=$out.$out1.$out2.$out3;
	close(sock);
    }
    return $out;
}

sub getoicq {
    my $oicq=shift;
    if ($oicqshow == 0){
	return "$imagesurl/images/oicq.gif";
    }else{
	my $geturl="http://search.tencent.com/cgi-bin/friend/oicq_find?oicq_no=$oicq";
	my $out=&lbagent($geturl);
	if ($out eq "连接远程服务器错误,请检查网络!"){
	    return "$imagesurl/images/oicq.gif";
	}else{
	    @str_ary = split(/ShowResult/,$out);
	    @str_ary =split(/<\/script>/,$str_ary[2]);
	    @str_ary = split(/\"\,\"/,$str_ary[0]);
	    if ($str_ary[1] !~ /\.gif$/isg){
		return "$imagesurl/images/oicq.gif";
	    }else{
		return "$str_ary[1]";
	    }
	}
    }
}

1;
