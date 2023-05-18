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
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "lb.lib.pl";
$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "rebuildmain.cgi";

$query = new LBCGI;

$checkaction   = $query -> param("checkaction");
$checkaction   = &cleaninput("$checkaction");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
if ($checkaction eq "yes") {
    &getmember("$inmembername");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

        $dirtoopen = "$lbdir";
        opendir (DIR, "$dirtoopen"); 
        @dirdata = readdir(DIR);
        closedir (DIR);
        @existforum = grep(/^forum[0-9]+$/,@dirdata);
        $existforumcount = @existforum;

        $filetoopen = "$lbdir" . "data/allforums.cgi";
      if (-e "$filetoopen") {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE,"$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);
      }
      else { undef @allforums; }
      undef @allforums1;
        foreach $forum (@allforums) {
            chomp($forum);
            (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription,my $no, $no, $no, $no, $no, $no, $no, my $threads, my $posts) = split(/\t/,$forum);
            next if ($forumid eq "");
    	    next if ($forumid !~ /^[0-9]+$/);
            next if ($category eq "");
 	    next if ($categoryplace eq "");
    	    next if ($categoryplace !~ /^[0-9]+$/);
            next if ($forumname eq "");
            next if ($forumdescription eq "");
            next if ($threads eq "");
            next if ($posts eq "");
            $dirtoopen = "$lbdir" . "forum$forumid";
 	    next if (!(-e $dirtoopen));
       	    push(@allforums1, $forum);

	        $dirtomake = "$lbdir" . "forum$forumid";
	        $filetomake1 = "$dirtomake/foruminfo.cgi";
		open(FILE1,">$filetomake1");
                print FILE1 $forum;
                close(FILE1);

 	    undef @existforum1;
            foreach $existforum (@existforum) {
        	next if ($existforum eq "forum$forumid");
        	push(@existforum1, $existforum);
 	    }
 	    @existforum = @existforum1;
        }
        $filetomake = "$lbdir" . "data/allforums.cgi";
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums1) {
            print FILE "$forum\n";
	}
        foreach $existforum (@existforum) {
             $dirtomake = "$lbdir" . "$existforum";
             $filetoopen1 = "$dirtomake/foruminfo.cgi";
             if (-e $filetoopen1){
		open(FILE1,"$filetoopen1");
		$existforuminfo = <FILE1>;
		close(FILE1);
	     	$existforum =~ s/forum//isg;
		chomp $existforuminfo;
		(my $forumid, my $category, my $categoryplace,my $forumname, my $forumdescription, my $forummoderator, my $htmlstate, my $idmbcodestate, my $privateforum, my $startnewthreads, my $lastposter, my $lastposttime, my $threads, my $posts, my $forumgraphic, my $ratings, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $miscadd1,my $miscadd2,my $miscadd3,my $miscadd4,my $miscad5) = split(/\t/,$existforuminfo);
		print FILE "$existforum\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
	     }
	     else {
	     	$existforum =~ s/forum//isg;
                print FILE "$existforum\t论坛分类丢失\t999\t论坛名称丢失\t论坛描述丢失\t\toff\ton\tno\tyes\t\t\t0\t0\t\tno\t\t\tno\tyes\t\t\t";
	     }
	}
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        print qq(
            	<tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 重新建立论坛主界面</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>重新建立 Allforums.cgi 文件，恢复主界面已经完成!</b>
		</td></tr>
	);

    }
    else {
	&adminlogin;
    }
}
else {
    &getmember("$inmembername");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
        print qq~
        <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 重新建立论坛主界面</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=宋体 color=#990000><b>此功能主要用于修复主界面中分论坛信息丢失或者损坏，完全智能化。</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <font face=宋体 color=#333333>如果您确定，那么请点击下面链接<p>
        >> <a href="$thisprog?action=delete&checkaction=yes">重新建立 Allforums.cgi 文件，恢复主界面</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
    }
    else {
	&adminlogin;
    }
}
print qq~</td></tr></table></body></html>~;
exit;
