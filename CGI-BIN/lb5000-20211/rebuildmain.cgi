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
                print FILE "$existforum\t��̳���ඪʧ\t999\t��̳���ƶ�ʧ\t��̳������ʧ\t\toff\ton\tno\tyes\t\t\t0\t0\t\tno\t\t\tno\tyes\t\t\t";
	     }
	}
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        print qq(
            	<tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ���½�����̳������</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>���½��� Allforums.cgi �ļ����ָ��������Ѿ����!</b>
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
        <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
        <b>��ӭ������̳�������� / ���½�����̳������</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=���� color=#990000><b>�˹�����Ҫ�����޸��������з���̳��Ϣ��ʧ�����𻵣���ȫ���ܻ���</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <font face=���� color=#333333>�����ȷ������ô������������<p>
        >> <a href="$thisprog?action=delete&checkaction=yes">���½��� Allforums.cgi �ļ����ָ�������</a> <<
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
