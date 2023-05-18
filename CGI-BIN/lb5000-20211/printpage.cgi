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
require "lb.lib.pl";
require "visitforum.lib.pl";
$|++;                                     # Unbuffer the output
$thisprog = "printpage.cgi";
$query = new LBCGI;

&ipbanned; #封杀一些 ip

$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/$thisprog//sg;
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');

print header(-charset=>gb2312);
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ($inmembername eq "" || $inmembername eq "客人" ) {
    $inmembername = "客人";
	    if ($regaccess eq "on") {
	    	print header(-cookie=>[$namecookie, $passcookie], -charset=>gb2312);
	    	print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	    	exit;
	    }
}
else {
    &getmember("$inmembername");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    if (($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')) { $allowed = "yes"; } else { $allowed = "no"; }
#        &getmemberstime("$inmembername");
        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$inforum};
        $currenttime = time;
        &setlastvisit("$inforum,$currenttime");
    }
    $filetoopen = "$lbdir" . "data/allforums.cgi";
    open(FILE, "$filetoopen");
    @forums = <FILE>;
    close(FILE);
    foreach $forumline (@forums) {
        ($tempno, $trash) = split(/\t/,$forumline);
        if ($inforum eq $tempno) {
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forumline);
        }
    }
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @threads = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    ($trash, $topictitle, $trash) = split(/\t/, @threads[0]);
    $topictitle =~ s/^＊＃！＆＊//;
    $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));

    if (($privateforum eq "yes") && ($allowed ne "yes")) {
        &error("进入私密论坛&对不起，你无权访问这个论坛！");
    }
    else {
      my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
      $filetoopens = &lockfilename($filetoopens);
      if (!(-e "$filetoopens.lck")) {
        if ($privateforum ne "yes") {
            &whosonline("$inmembername\t$forumname\tnone\t浏览<a href=\"$threadprog?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>(文本方式)\t");
        }
        else {
            &whosonline("$inmembername\t$forumname(密)\tnone\t浏览保密贴子(文本方式)\t");
        }
      }
    }
&badwordfile;
    if ($badwords) {
        @pairs = split(/\&/,$badwords);
        foreach (@pairs) {
            ($bad, $good) = split(/=/,$_);
            chomp $good;
            $topictitle=~ s/$bad/$good/isg;
        }
     }
    $output .= qq~
    <html><head><title>$boardname</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}

	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}

		.t     {	LINE-HEIGHT: 1.4			}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
	</style>
    </head>
    <body topmargin=10 leftmargin=0 onload="window.print()">
    <table cellpadding=0 cellspacing=0 border=0 width=90% align=center>
        <tr>
            <td>
            <p><b>以文本方式查看主题</b><p>
            <b>- $boardname</b> ($boardurl/$forumsummaryprog)<br>
            <b>-- $forumname</b> ($boardurl/$forumsprog?forum=$inforum)<br>
            <b>--- $topictitle</b> ($boardurl/$forumsprog?forum=$inforum&topic=$intopic)
        </tr>
    </table>
    <p><p><p>
    <table cellpadding=0 cellspacing=0 border=0 width=90% align=center>
      <tr><td>
    ~;
    foreach $line (@threads) {
        ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\t/,$line);
        $post = &lbcode("$post");

        $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $post=~ s/$bad/$good/isg;
            }
        }
        $output .= qq~
        <p>
        <hr><p>
        -- 作者： $postermembername<BR>
        -- 发布时间： $postdate<p>
        $post
        <p><p>
        ~;
    }
    my $boardcopyright = qq(&copy\; $copyrightinfo) if $copyrightinfo;

   $boardcopyright =~ s/&lt;/</g; $boardcopyright =~ s/&gt;/>/g; $boardcopyright =~ s/&quot;/\"/g;

    $output .= qq~
        </td></tr></table><center><hr width=90%><font color=$fontcolormisc>
           $boardcopyright　 版本： <a href="http://www.leoboard.com/download.htm">$versionnumber</a>
           </font></center>
        </body></html>
    ~;
    print $output;
    exit;
