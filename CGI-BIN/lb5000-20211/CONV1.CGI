#!/usr/bin/perl
#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ����������)
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
use File::Copy;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output
print header(-charset=>gb2312);

        $dirtoopen2 = "$imagesdir" . "usr";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @dirdata2 = grep(/\_/,@dirdata2);
        unlink "${lbdir}data/banlist.cgi";

      $filetoopen = "$lbdir" . "data/allforums.cgi";
      if (-e "$filetoopen") {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE,"$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
      }
      else { undef @allforums; }
      $aaa= @allforums;
      mkdir ("${lbdir}boarddata", 0777);
      mkdir ("${lbdir}lock", 0777);
      mkdir ("${imagesdir}midi", 0777);
      mkdir ("${imagesdir}usr", 0777);
      mkdir ("${imagesdir}usravatars", 0777);
      mkdir ("${lbdir}backup", 0777);
      mkdir ("${lbdir}memfriend", 0777);
      mkdir ("${lbdir}memfav", 0777);

        foreach $forum (@allforums) {
            chomp($forum);
            (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription,my $no) = split(/\t/,$forum);
            next if ($forumid eq "");
    	    next if ($forumid !~ /^[0-9]+$/);
            next if ($category eq "");
 	    next if ($categoryplace eq "");
    	    next if ($categoryplace !~ /^[0-9]+$/);
            next if ($forumname eq "");
            next if ($forumdescription eq "");
            $dirtomake = "$imagesdir" . "usr/$forumid";
            mkdir ("$dirtomake", 0777) if (!(-e "$dirtomake"));
            @files = grep(/^$forumid\_/,@dirdata2);
            foreach (@files) {
	        copy("$dirtoopen2/$_","$dirtomake/$_");
		chmod(0666,"$dirtomake/$_");
	        unlink "$dirtoopen2/$_";
	    }
	    copy("${lbdir}forum$forumid/list.cgi","${lbdir}boarddata/list$forumid.cgi");
	    copy("${lbdir}forum$forumid/xzb.cgi","${lbdir}boarddata/xzb$forumid.cgi");
	    copy("${lbdir}forum$forumid/xzb1.cgi","${lbdir}boarddata/xzbs$forumid.cgi");
	    copy("${lbdir}forum$forumid/lastnum.cgi","${lbdir}boarddata/lastnum$forumid.cgi");
	    copy("${lbdir}forum$forumid/ontop.cgi","${lbdir}boarddata/ontop$forumid.cgi");
	    copy("${lbdir}forum$forumid/jinghua.cgi","${lbdir}boarddata/jinghua$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/list$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/xzb$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/xzbs$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/lastnum$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/ontop$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/jinghua$forumid.cgi");
	    unlink "${lbdir}forum$forumid/list.cgi";
	    unlink "${lbdir}forum$forumid/xzb.cgi";
	    unlink "${lbdir}forum$forumid/xzb1.cgi";
	    unlink "${lbdir}forum$forumid/lastnum.cgi";
	    unlink "${lbdir}forum$forumid/ontop.cgi";
	    unlink "${lbdir}forum$forumid/jinghua.cgi";
        }

print "�ܹ� $aaa ����̳������ת����ϣ�<BR><BR>\n\n";

opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
my @msgdir = grep(/^messages/i, @files2);
$msgdir = $msgdir[0];

        $dirtoopen2 = "${lbdir}$msgdir";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);

      mkdir ("${lbdir}$msgdir/in", 0777);
      mkdir ("${lbdir}$msgdir/out", 0777);
      mkdir ("${lbdir}$msgdir/main", 0777);
	
      @data1 = grep(/\_msg\.cgi/,@dirdata2);
      foreach (@data1) {
	copy("${lbdir}$msgdir/$_","${lbdir}$msgdir/in/$_");
	chmod(0666,"${lbdir}$msgdir/in/$_");
	unlink "${lbdir}$msgdir/$_";
      }
      @data2 = grep(/\_out\.cgi/,@dirdata2);
      foreach (@data2) {
	copy("${lbdir}$msgdir/$_","${lbdir}$msgdir/out/$_");
	chmod(0666,"${lbdir}$msgdir/out/$_");
	unlink "${lbdir}$msgdir/$_";
      }
      @data3 = grep(/\_main\.cgi/,@dirdata2);
      foreach (@data3) {
	copy("${lbdir}$msgdir/$_","${lbdir}$msgdir/main/$_");
	chmod(0666,"${lbdir}$msgdir/main/$_");
	unlink "${lbdir}$msgdir/$_";
      }
print "��̳����Ϣ����ת����ϣ�<BR><BR>ת��ȫ����ɣ�<BR><BR>\n";
print "������ƣ�<a href=\"mailto:webmaster\@cgier.com\">ɽӥ(��)</a><BR>";
print "��Ȩ���У�<a href=\"http://www.cgier.com/\">CGI �����֮��</a>";

exit;