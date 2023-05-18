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
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "lb.lib.pl";
require "rebuildlist.pl";
$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "merge.cgi";

$query = new LBCGI;


for ('action','oforum','dforum', 'delsource') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
    }

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
    &getmember("$inmembername");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
	if($action eq 'submit') {
		if($oforum == $dforum) {
			print qq~
			<tr><td bgcolor=#333333 colspan=2><font face=宋体 color=#FFFFFF>
		        <b>欢迎来到论坛管理中心 / 合并论坛</b>
		        </td></tr>
		        <tr>
		        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		        <font face=宋体 color=#990000><b>出错了\~\~\~一个论坛怎么合并呀？</td></tr>
        	        </table></td></tr></table>
        	        ~;
        	        print qq~</td></tr></table></body></html>~;
        	        exit;
        	}
        	$oforumpath = "${lbdir}forum$oforum";
        	$dforumpath = "${lbdir}forum$dforum";

        opendir (DIR, "$oforumpath");
        @dirdata = readdir(DIR);
        closedir (DIR);

        @olist = grep(/thd.cgi$/,@dirdata);

        $dirtoopen = "$lbdir" . "forum$dforum";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);
        @sorteddirdata = grep(/.thd.cgi$/,@dirdata);
        @newdirdata = sort numerically(@sorteddirdata);
        @neworderdirdata = reverse(@newdirdata);
        $highest = $neworderdirdata[0];
        $highest =~ s/.thd.cgi$//;
        $lastnum = $highest;

        	foreach(@olist) {
        		@fields = split(/\./);
        		$topicid = $fields[0];
        		$newid = ++$lastnum;
        		$topicids{$topicid} = $newid;
        		$fields[0] = $newid;
        		$_ = join("\t",@fields);
        	}

        	open(FILE,">$dforumpath/lastnum.cgi");
         	flock(FILE, 2) if ($OS_USED eq "Unix");
        	print FILE $newid;
        	close(FILE);

        $dirtoopen2 = "$imagesdir" . "usr/$oforum";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = grep(/^$oforum\_/,@dirdata2);

        	while(($oldid,$newid) = each %topicids) {
        		copy("$oforumpath/$oldid.pl","$dforumpath/$newid.pl");
        		copy("$oforumpath/$oldid.thd.cgi","$dforumpath/$newid.thd.cgi");
        		copy("$oforumpath/$oldid.mal.pl","$dforumpath/$newid.mal.pl") if (-e "$oforumpath/$oldid.mal.pl");
        		copy("$oforumpath/$oldid.poll.cgi","$dforumpath/$newid.poll.cgi") if (-e "$oforumpath/$oldid.poll.cgi");
        		copy("$oforumpath/rate$oldid.file.pl","$dforumpath/rate$newid.file.pl") if (-e "$oforumpath/rate$oldid.file.pl");
        		copy("$oforumpath/rateip$oldid.file.pl","$dforumpath/rateip$newid.file.pl") if (-e "$oforumpath/rateip$oldid.file.pl");

		        @files1 = grep(/^$oforum\_$oldid\./,@files);
		        $files1 = @files1;
			if ($files1 > 0) {
			    foreach (@files1) {
			    	(my $name,my $ext) = split(/\./,$_);
				copy("$dirtoopen2/$oforum\_$oldid\.$ext","$dirtoopen2/$dforum\_$newid\.$ext") if (-e "$dirtoopen2/$oforum\_$oldid\.$ext");
			    }
			}
        	}
        	$inforum = $oforum;
        	&deleteforum if ($delsource eq "yes");
        	$inforum = $dforum;

	         rebuildLIST(-Forum=>"$dforum");

		print qq~
	        <tr><td bgcolor=#333333 colspan=2><font face=宋体 color=#FFFFFF>
	        <b>欢迎来到论坛管理中心 / 合并论坛</b>
	        </td></tr>

	        ~;
		&recount;
	} else {
	open(FILE,"<${lbdir}data/allforums.cgi");
        flock(FILE, 1) if ($OS_USED eq "Unix");
	@forumlist = <FILE>;
	close(FILE);
	chomp @forumlist;
	$tempoutput = '';
	foreach(@forumlist) {
		($forumid,$no,$no,$forumname) = split(/\t/);
		$tempoutput .= "<option value=\"$forumid\">$forumname</option>\n";
	}

        print qq~
        <tr><td bgcolor=#333333 colspan=2><font face=宋体 color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 合并论坛</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=宋体 color=#990000><b>请注意:</b>此过程将耗费大量CPU时间和系统资源，不到万不得已，不要采用本功能！<br>
        合并前请务必先关闭整个论坛。
        </td></tr>
        <tr>
        <td bgcolor=#FFFFFF valign=middle colspan=2 align=center>
        <form action=$thisprog method=post>
        把论坛<select name="oforum">$tempoutput</select>合并到论坛<select name="dforum">$tempoutput</select><BR>
        <input type="checkbox" name="delsource" value='yes' checked> 合并后，删除原来论坛的一切数据？<BR><BR>
        <input type="submit" value="确定">
        <input type="hidden" name="action" value="submit"></form>
        </td></tr>
       </table></td></tr></table>
        ~;
	    }

   } else {
	&adminlogin;
    }

print qq~</td></tr></table></body></html>~;
exit;
sub byupdate {
	(my $no,$no,$no,$no,$no,$no,$no,$no,$no,my $lastpostdatea, $no, $no) = split(/\t/,$a);
	(my $no,$no,$no,$no,$no,$no,$no,$no,$no,my $lastpostdateb, $no, $no) = split(/\t/,$b);
	$lastpostdateb <=> $lastpostdatea;
}



sub recount { #start


        $dirtoopen = "$lbdir" . "forum$inforum";

        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);

        @thd = grep(/thd.cgi$/,@dirdata);
        $topiccount = @thd;


        foreach $topic (@thd) {

            $filetoopen = "$lbdir" . "forum$inforum/$topic";

            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open (FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @threads = <FILE>;
            close (FILE);
            &winunlock($filetoopen) if ($OS_USED eq "Nt");

            $newthreads = @threads;
            $newthreads--;
            $threadcount = $threadcount + $newthreads;
         }

         $threadcount = "0" if (!$threadcount);
         $topiccount  = "0" if (!$topiccount);


         $filetoopen = "$lbdir" . "data/allforums.cgi";
         &winlock($filetoopen);
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         @allforums = <FILE>;
         close(FILE);

         $filetomake = "$lbdir" . "data/allforums.cgi";
         open(FILE, ">$filetomake");
         flock(FILE, 2) if ($OS_USED eq "Unix");
         foreach $forum (@allforums) { #start foreach @forums
         chomp($forum);
 	 next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    $posts = $threadcount;
                    $threads = $topiccount;
	            $dirtomake = "$lbdir" . "forum$forumid";
	            $filetomake1 = "$dirtomake/foruminfo.cgi";
          	    open(FILE1,">$filetomake1");
                    print FILE1 "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t";
                    close(FILE1);
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
         }
         close(FILE);
         &winunlock($filetomake);

         rebuildLIST(-Forum=>"$inforum");

         print qq~
         <tr>
         <td bgcolor=#FFFFFF colspan=2>
         <font color=#990000>
         <center><b>论坛合并成功</b></center><p>
         主题数： $topiccount<p>
         回复数： $threadcount
         </td></tr></table></td></tr></table>
         ~;


} # routine ends
sub deleteforum { #start

        $dirtoopen = "$lbdir" . "forum$inforum";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);

        foreach $file (@dirdata) {
            $filetoremove = "$dirtoopen/$file";
            unlink $filetoremove;
        }

        $dirtoopen2 = "$imagesdir" . "usr/$inforum";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = @dirdata2;

        foreach $file (@files) {
            $filetoremove = "$dirtoopen2/$file";
            unlink $filetoremove;
        }

         $dirtoremove = "$lbdir" . "forum$inforum";
         rmdir $dirtoremove;
         $dirtoremove = "$imagesdir" . "usr/$inforum";
         rmdir $dirtoremove;

        $filetoremove = "$lbdir" . "boarddata/list$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/xzb$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/xzbs$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/lastnum$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/ontop$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "data/news$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "data/style$inforum.cgi";
        unlink $filetoremove;

         $filetoopen = "$lbdir" . "data/allforums.cgi";
         &winlock($filetoopen);
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         @forums = <FILE>;
         close(FILE);

         open(FILE,">$filetoopen");
         flock(FILE,2) if ($OS_USED eq "Unix");
         foreach $forum (@forums) {
         chomp $forum;
	 next if ($forum eq "");
            ($forumid,$category,$notneeded,$notneeded) = split(/\t/,$forum);
    	    next if ($forumid !~ /^[0-9]+$/);
                unless ($forumid eq "$inforum") {
                    print FILE "$forum\n";
                    }
                }
         close(FILE);
         &winunlock($filetoopen);


} # routine ends
