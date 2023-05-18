#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ���������)
#
#  ������  : ɽӥ�� (Shining Hu)
#            ����ȱ (Ifairy Han)
#           
#  ��ҳ��ַ: http://www.CGIer.com/      CGI �����֮��
#	     http://www.LeoBoard.com/   �װ���̳֧����ҳ
#	     http://www.leoBBS.com/     ����ֱ̳ͨ��
#            http://mail@17do.com/      ���һ����
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
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "rebuildlist.pl";
$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "rebuildall.cgi";

$query = new LBCGI;

$nextforum     = $query -> param('nextforum');
$action        = $query -> param("action");
$action        = &cleaninput("$action");
$nextforum=0 if ($nextforum eq "");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {#1
    &getmember("$inmembername");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { #2
        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
        @forums = <FILE>;
        my $size=@forums;
        close(FILE);

        @checkforums = @forums;
        @checkforums = reverse(@checkforums);
        ($inforum, $trash) = split(/\t/,$checkforums[$nextforum]);
        ############################
        $dirtoopen = "$lbdir" . "forum$inforum";
        if (-e $dirtoopen){#3
          opendir (DIR, "$dirtoopen"); 
          @dirdata = readdir(DIR);
          closedir (DIR);
          @thd = grep(/thd.cgi$/,@dirdata);
          $topiccount = @thd;
          foreach $topic (@thd) {#4
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
          }#4
       
          $threadcount = "0" if (!$threadcount);
          $topiccount  = "0" if (!$topiccount);
        
          $filetoopen = "$lbdir" . "data/allforums.cgi";
          &winlock($filetoopen) if ($OS_USED eq "Nt");
          open(FILE,"$filetoopen");
          flock(FILE, 1) if ($OS_USED eq "Unix");
          @allforums = <FILE>;
          close(FILE);

          $filetomake = "$lbdir" . "data/allforums.cgi";
          open(FILE, ">$filetomake");
          flock(FILE, 2) if ($OS_USED eq "Unix");
          foreach $forum (@allforums) { #5
            chomp($forum);
 	    next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
            if ($inforum eq $tempno) { #6
               ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                $posts = $threadcount;
                $threads = $topiccount;
	        $dirtomake = "$lbdir" . "forum$forumid";
	        $filetomake1 = "$dirtomake/foruminfo.cgi";
		open(FILE1,">$filetomake1");
                print FILE1 "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t";
                close(FILE1);
                print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
            }#6
            else { print FILE "$forum\n"; }
          }#5
          close(FILE);
          &winunlock($filetomake) if ($OS_USED eq "Nt");
          rebuildLIST(-Forum=>"$inforum");
        }#3

	############################
	$nextforum++;
	if ($nextforum > $size){
            print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / �ָ�-���¼���������̳</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>�ָ�-���¼���������̳�Ѿ����!</b>
		</td></tr>);
	}else{
	    print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / �ָ�-���¼���������̳</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>�ָ�-���¼���������̳</b>
		</td></tr>
		<td bgcolor=#ffffff valign=middle align=left colspan=2>
		<font color=black><b><br><br><br>������..
		<br>�ظ���:$threadcount<br>
		������:$topiccount</b></td></tr>
		
		<meta http-equiv="refresh" content="2; url=$thisprog?action=process&nextforum=$nextforum">
	    );
	}
      }#2
      else {
         &adminlogin;
      }
}#1   
else {
        &getmember("$inmembername");
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / �ָ�-���¼���������̳</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>�ָ�-���¼���������̳</b>
		</td></tr>
		<form action="$thisprog" method="post">
		<input type=hidden name="action" value="process">
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#000000>
		<b>��ע��:</b><br>�˹��̽��ķѴ���CPUʱ���ϵͳ��Դ�������򲻵��ѣ���Ҫ���ñ����ܣ�
		</td>
		</tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<input type=submit name=submit value=�ύ></td></form></tr></table></td></tr></table>
		);
	}
        else {
		&adminlogin;
	}
}
print qq~</td></tr></table></body></html>~;
exit;
