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
require "code.cgi";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "data/membertitles.cgi";
require "lb.lib.pl";
require "visitforum.lib.pl";

$adscript = &HTML("$adscript");
$adfoot = &HTML("$adfoot");
$|++;

#################--- Begin the program ---###################
$thisprog = "view.cgi";

$query = new LBCGI;

$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;

$inforum        = $query -> param('forum');
$inforum        = &stripMETA("$inforum");
$intopic        = $query -> param('topic');
$intopic        = &stripMETA("$intopic");
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));

############################
$filerequire = "$lbdir" . "data/style${inforum}.cgi"; 
if (-e $filerequire) { require $filerequire; } 
############################


$inmembername   = $query->cookie("amembernamecookie");
$inpassword     = $query->cookie("apasswordcookie");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

$nodispphoto  = $query->cookie("nodispphoto");

$banfresh1 = $query->cookie("banfresh");
$banfresh1 = 0 if ($banfresh1 eq "");
($backtopic, $banfresh) = split(/=/,$banfresh1);
$nowtime = time;
$banfreshcookie  = cookie(-name    =>   "banfresh",
                          -value   =>   "$intopic=$nowtime",
                          -path    =>   "$cookiepath/");

if ((($nowtime - $banfresh - 1) <= $banfreshtime)&&($backtopic eq $intopic)) {
   print header(-cookie=>[$banfreshcookie],-charset=>gb2312);
   print "服务器忙，请 3 秒后按刷新键继续。<BR><BR>";
   print "出错原因：你刷新页面过快，或者你打开了过多窗口来浏览本网站。";
   exit;
}

&ipbanned; #封杀一些 ip
&badwordfile;
&forumjump;
&getforum($inforum);
if ($jumpto) {
    print redirect(-location=>"$jumpto"); exit;
    }
if (!$inmembername) {
    $inmembername = "客人";
    }
    else {
        &getmember("$inmembername");
        $membercodetemp = $membercode;
        $tempaccess = "forumsallowed". "$inforum";
        $testentry = $query->cookie("$tempaccess");
        &moderator;
        if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
            else { $allowed  = "no"; }
#        &getmemberstime("$inmembername");
        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$inforum};
        $currenttime = time;
        &setlastvisit("$inforum,$currenttime");
        $inmembercode = $membercode;
        }

    print header(-cookie=>[$tempvisitcookie, $permvisitcookie, $banfreshcookie], -charset=>gb2312);

    if (($inmembername eq "客人")&&($regaccess eq "on")) {&error("进入会员论坛查看帖子内容&您是客人没有权限进入!");}
    if (("$privateforum" eq "yes" && "$allowed" ne "yes")) { &error("进入私有论坛&对不起，您没有权限进入该私有论坛！"); }

    my $dirtoopen2 = "$imagesdir" . "usr/$inforum";
    opendir (DIR2, "$dirtoopen2");
    my @dirdata2 = readdir(DIR2);
    closedir (DIR2);
    my @files11 = grep(/^$inforum\_$intopic\_/,@dirdata2);

    my $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
    my $filetoopens = &lockfilename($filetoopen);

    if (!(-e "$filetoopens.lck")) {
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allthreads = <FILE>;
        close(FILE);
        $totalthreadcount = @allthreads;
        $count = 0;
	@allthreadtemp = "";
        foreach $line (@allthreads) {
           ($tempno, $trash) = split(/\t/, $line);
           chomp $line;
           push (@numbercounter, $tempno);
            if ($intopic eq $tempno) {
                ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp) = split(/\t/,$line);
                $threadviews++; $keepcounter = $count;
                $linetokeep = "$topicid\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t";
                push (@allthreadtemp, $linetokeep);
            }
            else { push (@allthreadtemp, $line); }
        $count++;
        }
        open(FILE, ">$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach (@allthreadtemp) {
	    chomp $_;
            print FILE "$_\n" if ($_ ne "");
        }
        close(FILE);
        &winunlock($filetoopen);
        my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        open(MSG, ">$file");
        print MSG $linetokeep;
        close(MSG);
    }
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
      if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @threads = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
      }
      else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("打开主题&这个主题不存在！可能已经被删除！"); } 
        ($membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$threads[0]);     
        $topictitle =~ s/^＊＃！＆＊//;
        $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
        $postdate = &dateformat("$postdate");
        &getmember("$membername");
          	       
            if ($idmbcodestate eq 'on') {
            $post = &lbcode("$post");
            if ($post =~/<blockquote><font face=宋体>代码/isg){
             $post =~ s/\&amp\;/\&/ig ;
             $post =~ s/\&lt\;br\&gt\;/<br>/ig;
             }
            }
          
        if (($emoticons eq 'on') and ($showemoticons eq 'yes') and ($post =~ /:(.+?):/)) {
            $post = &doemoticons("$post");
            }
    
        if (($emoticons eq 'on') && ($showemoticons eq 'yes')) {
	    $post = &smilecode("$post");
            }                             
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $post =~ s/$bad/$good/isg;
                }
            }   
        $memberfilename = $membername;
        $memberfilename =~ y/ /_/;
	$memberfilename =~ tr/A-Z/a-z/;            
       $homepage =~ s/http\:\/\///sg;
       if ($homepage){ $homepage ="http://$homepage";}
else { $homepage ="$boardurl/leoboard.cgi";}

$addmefile =0;
my @files2 = grep(/^$inforum\_$intopic\./,@dirdata2);
my $file2 = @files2;
if ($file2 > 0) {
    my $files2s = $files2[0]; chomp $files2s;
    ($up_name, $up_ext) = split(/\./,$files2s);
    $up_ext =~ tr/A-Z/a-z/;
    $addmefile =1;
}

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
    }else{
       $addme = qq(<font color=$fonthighlight>相关附件</font>：<a href=$imagesurl/usr/$inforum/$up_name.$up_ext target=_blank><img src=$imagesurl/icons/$filetype.gif border=0 width=16 height=16 alt="该主题有一个“$filetype”类型附件，点击下载"></a> (共 $fileinfo[7] 字节)<br><br>);
    }
}
else { $addme = ""; }

        ##
 if ($posticon ne "") {
    if ($posticon =~/<br>/i){
	$posticon=~s/<br>/\t/ig;
	$maxpolllength = 0;
	
	($poll[1], $poll[2], $poll[3], $poll[4], $poll[5],$poll[6],$poll[7],$poll[8],$poll[9],$poll[10]) = split(/\t/, $posticon);
	$j=0;
	$pollinput ="";
    	for ($i=1;$i<=10;$i++){
    	    if ($poll[$i] ne "") {
    	        $j++;
    	        $pollinput .= qq~<input type=radio name=myChoice value='$i'> $poll[$i]<br>~;
    	        $maxpolllength = length($poll[$i]) if (length($poll[$i]) > $maxpolllength);
    	    }
	}
	$maxpolllength = $maxpolllength*7+10;
	$maxpolllength = 150 if ($maxpolllength < 150);
	$maxpolllength = 510 if ($maxpolllength > 510);
	
	$pollform =qq~
	    <form action="$pollprog" method=post>
	    <table cellpadding=1 cellspacing=0 border=0 width=$maxpolllength bgcolor=$tablebordercolor>
	    <tr><td>
	    <table width=100% cellpadding=4 cellspacing=0 bgcolor="#f2f2f2">
	    <tr><td>
	    $pollinput
	    <tr><td align=center nowrap>
	        <HR size=1 width=85%>
		<input type=hidden name=action value="poll">
		<input type=hidden name=id value="$inforum">
		<input type="hidden" name="threadname" value="$topicid">
		<input type=submit name=results value='参加投票'>
	    </td></form></tr></table></td></tr></table>
    	~;
	
	$showpoll = "";
	$pollnull = "";
	
	$poll =qq~ <table width=510 border=0 $maxpolllength>
	    <tr><td colspan=2><HR size=1 width=100%></td></tr>
	~;
	$filetomake = "$lbdir" . "forum$inforum/$topicid.poll.cgi";
	if (-e $filetomake) {
	    &winlock($filetomake) if ($OS_USED eq "Nt");
            open(FILE, "$filetomake");
            flock(FILE, 2) if ($OS_USED eq "Unix");
            @allpoll = <FILE>;
            close(FILE);
	    &winunlock($filetomake) if ($OS_USED eq "Nt");
            $size=@allpoll;

	    @thispoll=('0','0','0','0','0','0','0','0','0','0','0');
	    foreach (@allpoll){
		$_=~s/[\n\r]//isg;
		($tmpinmembername,$tmpmyChoice)=split(/\t/, $_);
		for ($i=1;$i<=$j;$i++){
		    $thispoll[$i]++ if ($i == $tmpmyChoice);
		}
	        $showpoll="true" if ($tmpinmembername eq $inmembername);
	    }
	    $poll .= qq~ <tr><td colspan=2>目前共有 <font color=$fonthighlight><B>$size</B></font> 人参加投票，结果如下：<HR size=1 width=100%><BR></td></tr>~;
    	    for ($i=1;$i<=$j;$i++){
    	    	if ($poll[$i] ne ""){
    		    $mypoll=int(($thispoll[$i]/$size)*100);
    		    $width=int(($mypoll/100)*160);
    		    $poll.=qq~<tr><td width=50%>$poll[$i] </td><td width=50%> <img src=$imagesurl/images/bar$i.gif width=$width height=10> <b>$thispoll[$i]</b> 票数 $mypoll%</td></tr>~;
    	    	}
	    }
	}
	else {
	    $poll .= qq~ <tr><td colspan=2>没有人参加此投票，选项列表如下：<HR size=1 width=100%><BR></td></tr>~;
    	    for ($i=1;$i<=$j;$i++){
		$poll .= qq~<tr><td colspan=2>$poll[$i] </td></tr>~;
	    }
	    $pollnull = "true";
	}
	$poll .= "</td></tr><tr><td colspan=2><HR size=1 width=100%></td></tr></table>";

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

    	$editgraphic="";
    	$posticon="";
    }
    else {
    	$posticon = qq~<img src=$imagesurl/posticons/$posticon width=13 height=13>~;
    }
}
if ($poll ne ""){
	$post=$post."<br>".$poll;
	$poll="";
    }
 ## 

       
print qq~

<HTML><HEAD><TITLE>$topictitle</TITLE>
<META http-equiv=Content-Type content="text/html; charset=gb2312">
<script language="javaScript" type="text/javascript" SRC="$imagesurl/images/board.js"></SCRIPT>
<style>
BODY {
	FONT-SIZE: 9pt; FONT-FAMILY: "MS Shell Dlg";
}
P {
	FONT-SIZE: 9pt; FONT-FAMILY: "MS Shell Dlg"
}
SELECT {
	FONT-SIZE: 9pt; FONT-FAMILY: "MS Shell Dlg"
}
TD {
	FONT-SIZE: 12px; FONT-FAMILY: "MS Shell Dlg"
}
INPUT {
	FONT-SIZE: 9pt; FONT-FAMILY: 宋体; verdana: 
}
TEXTAREA {
	FONT-SIZE: 9pt; FONT-FAMILY: 宋体; verdana: 
}
TEXTAREA {
	FONT-SIZE: 9pt; FONT-FAMILY: 宋体; verdana: 
}
.input1 {
	BORDER-RIGHT: #085d3f 1px solid; BORDER-TOP: #085d3f 1px solid; BORDER-LEFT: #085d3f 1px solid; BORDER-BOTTOM: #085d3f 1px solid; BACKGROUND-COLOR: white
}
A {
	FONT-SIZE: 9pt; TEXT-TRANSFORM: none; COLOR: #000000; TEXT-DECORATION: none
}
A.lefta {
	FONT-SIZE: 9pt; TEXT-TRANSFORM: none; COLOR: #ffffff; TEXT-DECORATION: none
}
A.flink {
	FONT-SIZE: 9pt; TEXT-TRANSFORM: none; COLOR: #000000; TEXT-DECORATION: none
}
A.lefta:hover {
	COLOR: #c0c0c0; TEXT-DECORATION: none
}
A:hover {
	COLOR: red; TEXT-DECORATION: none
}
A:visited {
	TEXT-DECORATION: none
}
.smallsize {
	FONT-SIZE: 9px; COLOR: #d9d9d9; FONT-FAMILY: "verdana"
}
LI {
	FONT-SIZE: 9pt; LINE-HEIGHT: 15pt
}
.tt2 {
	FONT-SIZE: 9pt; LINE-HEIGHT: 16pt
}
.tt1 {
	FONT-SIZE: 14px
}
.tt3 {
	FONT-SIZE: 9pt; LINE-HEIGHT: 13pt
}
A.hb {
	FONT-SIZE: 9pt; COLOR: #000000; LINE-HEIGHT: 10pt
}
A.tt1 {
	COLOR: #000000; TEXT-DECORATION: none
}
</style>
<BODY background=$imagesurl/images/schedulebg.gif bgColor=#ffffff><a name="top"></a>
<table width=750 border="0" cellspacing="0" cellpadding="0" align="center">
  <tr> 
    <td height="40" width="176">
      <div align="center"><img src="$imagesurl/images/$boardlogo" border=0></div>
    </td>
    <td height="40" colspan="2"> 
      <div align="right">$adscript</div>
          </td>
  </tr>
  <tr align="right"> 
    <td colspan="3"> 
 <table border="1" cellspacing="1" bordercolorlight="#49ADE9" bordercolordark="#FFFFFF" cellpadding="1" width="100%">
        <tr bgcolor="#Caeaff"> 
          <td colspan="7">
          &nbsp;</td>
        </tr>
      </table>
    </td>
  </tr>
</table>
<TABLE height="100%" cellSpacing=0 cellPadding=0 width=750 align=center 
border=0>
  <TBODY>
  <TR>
    <TD vAlign=top align=middle width=120>
      <TABLE height="100%" cellSpacing=0 cellPadding=0 width="100%" align=center 
      border=0>
        <TBODY>
        <TR>
          
          <TD vAlign=top width=1 bgColor=white></TD>
          <TD vAlign=top align=middle bgColor=#49ADE9>

            <TABLE cellSpacing=0 cellPadding=0 width=100 align=center 
              border=0>
              <TBODY> 
              <TR> 
                <TD height=6></TD>
              </TR>
              <TR> 
                <TD style="COLOR: white" align=middle bgColor=#ffa200 
                  height=18>
                  <div align="center"><B>本文章信息</B></div>
                </TD>
              </TR>
              <TR> 
                <TD height=6></TD>
              </TR>
              <TR> 
                <TD 
                onmouseover="this.style.background='#Caeaff';this.style.color='#000000'" 
                onmouseout="this.style.background='';this.style.color=''" 
                align=middle height=18><A class=LEFTA 
                  href="$profileprog?action=show&member=$memberfilename">作 者 资 料</A></TD>
              </TR>
              <TR> 
                <TD 
                onmouseover="this.style.background='#Caeaff';this.style.color='#000000'" 
                onmouseout="this.style.background='';this.style.color=''" 
                align=middle height=18><A class=LEFTA 
                  href="$homepage">作 者 主 页</A></TD>
              </TR>
              <TR> 
                <TD 
                onmouseover="this.style.background='#Caeaff';this.style.color='#000000'" 
                onmouseout="this.style.background='';this.style.color=''" 
                align=middle height=18><A class=LEFTA 
                  href="fav.cgi?action=add&forum=$inforum&topic=$intopic">我 
                  要 收 藏</A></TD>
              </TR>
              <TR> 
                <TD 
                onmouseover="this.style.background='#Caeaff';this.style.color='#000000'" 
                onmouseout="this.style.background='';this.style.color=''" 
                align=middle height=18><A class=LEFTA 
                  href="pag.cgi?forum=$inforum&topic=$intopic">打 包 下 载</A></TD>
              </TR>
              <TR> 
                <TD 
                onmouseover="this.style.background='#Caeaff';this.style.color='#000000'" 
                onmouseout="this.style.background='';this.style.color=''" 
                align=middle height=18><A class=LEFTA 
                  href="$postprog?action=new&forum=$inforum">发 表 主 题</A></TD>
              </TR>
              <TR> 
                <TD 
                onmouseover="this.style.background='#Caeaff';this.style.color='#000000'" 
                onmouseout="this.style.background='';this.style.color=''" 
                align=middle height=18><A class=LEFTA 
                  href="$lbfriendprog?forum=$inforum&topic=$intopic">转 
                  发 该 文</A></TD>
              </TR>
              <TR> 
                <TD height=6></TD>
              </TR>
              </TBODY> 
            </TABLE>
          </TD>
          <TD vAlign=top width=1 bgColor=white></TD>
          </TR></TBODY></TABLE></TD>
    <TD vAlign=top>
<TABLE cellSpacing=0 cellPadding=0 width="100%" border=0  style="TABLE-LAYOUT: fixed">
        <TBODY>
        <TR>
          <TD width=22></TD>
          <TD vAlign=top>
            <TABLE cellSpacing=0 cellPadding=0 width="100%" border=0>
              <TBODY>
              <TR>
                <TD width="100%" bgColor=#49ADE9 height=17><FONT 
                  color=#ffffff>&nbsp;&gt;&gt; <A 
                  href="$forumsummaryprog"><FONT 
                  color=#ffffff>$boardname</FONT></A>／<A 
                  href="$forumsprog?forum=$inforum"><FONT 
                  color=#ffffff>$forumname</FONT></A>／<A 
                  href="$threadprog?forum=$inforum&topic=$intopic"><FONT 
                  color=#ffffff>$topictitle</FONT></A></FONT></TD></TR></TBODY></TABLE>
<SPAN style="FONT-SIZE: 14px"><BR>
            <CENTER><B>$topictitle</B></CENTER><BR>
            <SPAN 
            style="FONT-SIZE: 9pt">(这条文章已经被阅读了 <FONT color=red>$threadviews </FONT>次) 时间：$postdate
            　来源：$membername</SPAN><br><br>$addme
            <br>$post
           <br>
            </SPAN><BR><BR>
            <TABLE cellSpacing=0 cellPadding=0 width="100%" border=0>
              <TBODY> 
              <TR> 
                <TD width="100%" bgColor=#ffa200 height=18>
                  <div align="center">［<A  href="pag.cgi?forum=$inforum&topic=$intopic">打包下载</A>］　　　［<A href="post.cgi?action=copy1&forum=$inforum&topic=$intopic&postno=1">引用该文</A>］　　　［<A 
                  href="post.cgi?action=reply&forum=$inforum&topic=$intopic">发表评论</A>］　　　［<A 
                  href="lbfriend.cgi?forum=$inforum&topic=$intopic">转寄该文</A>］　　　［<A 
                  href="javascript:window.close();">关闭窗口</A>］</div>
                </TD>
              </TR>
              <TR> 
                <TD width="100%" height=18>此文章相关评论: </TD>
              </TR>
~;
#############
$size=@threads;
$hasadd=$size-1;
if ($hasadd == 0){
print qq~
	     <TR> 
                <TD width="100%" height=18>该文章还没有相关评论！(<a href=$threadprog?forum=$inforum&topic=$intopic><font Color=#ffa200>点这儿论坛方式查看</font></a>) </TD>
              </TR></TBODY>
            </TABLE>
~;
}else{
print qq~
              <TR> 
                <TD width="100%" height=18>该文章有<font color=red>$hasadd</font>个相关评论如下：(<a href=$threadprog?forum=$inforum&topic=$intopic><font Color=#ffa200>点这儿论坛方式查看</font></a>)<br><HR size=1 width=100%></TD>
              </TR></TBODY>
            </TABLE>

~;
}

for ($i=1;$i<$size;$i++){
($membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$threads[$i]);     
        $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
        $postdate = &dateformat("$postdate");

############################################################
        $addmefile =0;
        $rrn=$i;
          my @files1 = grep(/^$inforum\_$intopic\_$rrn\./,@files11);
            my $file1 = @files1;
            if ($file1 > 0) {
               my $files1s = $files1[0]; chomp $files1s;
               ($up_name, $up_ext) = split(/\./,$files1s);
                $up_ext =~ tr/A-Z/a-z/;
          	$addmefile =1;
            }

    
    if ($addmefile == 1) {
    @fileinfo = stat("${imagesdir}usr/$inforum/$up_name.$up_ext");
    $filetype = "unknow";
    $filetype = $up_ext if (-e "${imagesdir}icons/$up_ext.gif");
    if (($up_ext eq "gif")||($up_ext eq "jpg")||($up_ext eq "png")||($up_ext eq "bmp")){
       $addme = qq(<img src=$imagesurl/icons/$filetype.gif border=0 width=16 height=16> 相关图片如下：<br><a href=$imagesurl/usr/$inforum/$up_name.$up_ext target=_blank><img src=$imagesurl/usr/$inforum/$up_name.$up_ext border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>screen.width-333)this.width=screen.width-333"></a><br><br>);	
    }else{
       $addme = qq(<font color=$fonthighlight>相关附件</font>：<a href=$imagesurl/usr/$inforum/$up_name.$up_ext target=_blank><img src=$imagesurl/icons/$filetype.gif border=0 width=16 height=16 alt="该主题有一个“$filetype”类型附件，点击下载"></a> (共 $fileinfo[7] 字节)<br><br>);
    }
    }

     else { $addme = ""; }




############################################################          	       
            if ($idmbcodestate eq 'on') {
            $post = &lbcode("$post");
            if ($post =~/<blockquote><font face=宋体>代码/isg){
             $post =~ s/\&amp\;/\&/ig ;
             $post =~ s/\&lt\;br\&gt\;/<br>/ig;
             }
            }
          
        if (($emoticons eq 'on') and ($showemoticons eq 'yes') and ($post =~ /:(.+?):/)) {
            $post = &doemoticons("$post");
            }
    
        if (($emoticons eq 'on') && ($showemoticons eq 'yes')) {
        	    $post = &smilecode("$post");
            }                             
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $post =~ s/$bad/$good/isg;
                }
            }   
        $memberfilename = $membername;
        $memberfilename =~ y/ /_/;
	$memberfilename =~ tr/A-Z/a-z/; 
	if ($post =~/<blockquote>/isg){
	$post=~ s/(<blockquote>)(.*?)(<hr noshade><\/blockquote>)//isg;
	}
	#if ($i/2==int($i/2)) {$color="#ffffff";}
	#else {$color="#ffffff";}
print qq~
	<table style="TABLE-LAYOUT: fixed" cellpadding=8 cellspacing=1 border=0 width=100%>
        <tr>
            <td bgcolor="#FFFFFF" rowspan=2 valign="top" width=20%><font color=#000000>
            <b><a href=$profileprog?action=show&member=$memberfilename target=_blank>$memberfilename</a></b></font></td>
            <td bgcolor="#FFFFFF" ><font color=#000000><b>发表于： $postdate</b><br>$addme</td>
        </tr>
        <tr>    
         <td bgcolor="#FFFFFF" style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word">$post
</td>
        </tr>
        <tr>
            <td colspan=2 bgcolor="#EEEEEE" align=right>&nbsp;<a href=#top><img src=$imagesurl/images/gotop.gif border=0 weight=15 height=15 align=absmiddle>顶部</a></td>
        </tr>
        </table>
	
~;	 
}	
#############
print qq~              
              
          </TD>
          </TR></TBODY></TABLE></TD></TR></TBODY></TABLE>

    </td>
  </tr>
</table>
<div align="center"> 
  <table height=22 cellspacing=0 cellpadding=0 width="721" 
                  border=0>
    <tbody> 
    <tr > 
      <td colspan="2" width="987" height="20"> 
        <div align="center"><font class="chinese_text13" color="#000000"> 
          <script language=JavaScript1.2>
<!--
var correctwidth=800
var correctheight=600
if (screen.width!=correctwidth||screen.height!=correctheight)
document.write("建议使用"+correctwidth+"×"+correctheight+"以上分辨率. 您当前的分辨率是:"+screen.width+"×"+screen.height+"。")
//-->
</script>
          </font></div>
      </td>
    </tr>
    <tr > 
      <td colspan="2" width="987" height="20"> 
        </div>
      </td>
    </tr></tbody></table></div>
<br>
</BODY></HTML>
<center>$adfoot</center>
~;
exit;        
