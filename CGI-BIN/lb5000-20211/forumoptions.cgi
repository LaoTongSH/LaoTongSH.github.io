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
#            http://maildo.com/      ���һ����
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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "rebuildlist.pl";
$|++;                                     # Unbuffer the output
$thisprog = "forumoptions.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$checked        = $query -> param('checked');
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$action         = $query -> param('action');
$prunedays      = $query -> param('prunedays');
$inmembername   = $query -> param('membername');
$inpassword     = $query -> param('password');
$inforum        = &stripMETA("$inforum");
$intopic        = &stripMETA("$intopic");
$action         = &stripMETA("$action");
$prunedays      = &stripMETA("$prunedays");
$inmembername   = &stripMETA("$inmembername");
$inpassword     = &stripMETA("$inpassword");
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
print header(-charset=>gb2312);
if (($inforum  !~ m|([0-9\G]+$)|g) or (!$inforum))  { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
if (($prunedays) && ($prunedays !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

&getmember("$inmembername");
&error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");

&moderator;
if ($action eq "prune") {
    $cleartoedit = "no";
    &mischeader("����ɾ��");
	if ($inpassword eq $password) {
		$pwok = "���벻��ʾ";
	}
	else {
		$pwok = $inpassword;
	}
	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$trueipaddress = "no" if (($trueipaddress eq "")||($trueipaddress eq "unknown"));
	my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$trueipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
	my $thistime=time;
	$filetomake = "$lbdir" . "data/baddel.cgi";

    $maxdeloneday = 9 if (($maxdeloneday eq "")||($maxdeloneday <= 0));
    if ($membercode ne "ad"){ 
      &winlock($filetomake); 
      open(FILE,"$filetomake"); 
      flock (FILE, 2) if ($OS_USED eq "Unix"); 
      my @delfile = <FILE>; 
      close(FILE); 
      my $delcount=0; 
      my $delcou=0; 
      my $totime=$thistime-24*60*60; 
      foreach (@delfile){ 
	chomp($_); 
	(my $delname, my $no, my $noip, $no, $no ,my $notime) = split(/\t/,$_); 
	if (lc($delname) eq lc($inmembername)){ 
	  if ($notime <$totime){ 
	    $delcount++; 
	  } 
	} 
	if ($noip eq "$ENV{'REMOTE_ADDR'}"){ 
	  if ($notime <$totime){ 
	    $delcou++; 
	  }
	}
      }
      if ($delcount > $maxdeloneday){&error("ɾ������&�����ɾ������̫�࣬�����������");} 
      if ($delcou > $maxdeloneday)  {&error("ɾ������&�����ɾ������̫�࣬�����������");} 
      undef $delcount; 
      undef $delcou; 
    }
    if (open(FILE, ">>$filetomake")) {
    print FILE "$inmembername\t$pwok\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t����ɾ��$forumname $prunedays��ǰ������\t$thistime\t\n";
    close(FILE);
    }
    undef $thistime;
    &winunlock($filetomake); 

    if ((($membercode eq "ad") ||($membercode eq 'smo'))&& ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
        if ($cleartoedit eq "no" && $checked eq "yes") {&error("ʹ������ɾ��&�����Ǳ���̳̳��������Ա�������������������");  }
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        if ($prunedays < 20) {  &error("ʹ������ɾ��&ָ��ɾ��������Ҫ���� 20 ��"); }

	&getforum($inforum);

      my $file = "$lbdir" . "boarddata/jinghua$inforum.cgi";
      if (-e $file) {
        open (ENT, $file);
        @jinghuatopic = <ENT>;
        close (ENT);
      }
      else { undef @jinghuatopic ;}

	$dirtoopen = "$lbdir" . "forum$inforum";
	opendir (DIR, "$dirtoopen");
	my @dirdata = readdir(DIR);
	closedir (DIR);
	@entry = grep(/\.thd\.cgi$/,@dirdata);
	foreach (@entry) {
	  (my $topicid, my $tr) = split(/\./,$_);
	  $jinghuatopicnow = 0 ;
	  foreach $jinghuatopic (@jinghuatopic) {
	      chomp $jinghuatopic;
	      if ($topicid eq $jinghuatopic) { $jinghuatopicnow = 1; }
	  }
	 if ($jinghuatopicnow eq 0) {
	  $file1 = "$lbdir" . "forum$inforum/$topicid.thd.cgi";
	  open (TMP1, "$file1");
          flock(TMP1, 1) if ($OS_USED eq "Unix");
	  my @tmp = <TMP1>;
	  close (TMP1);
	  $postcount = @tmp;
          $postcount--;
	  my $tmp1 = $tmp[-1];
	  (my $no, my $no, my $no, my $no, my $no, my $lastpostdate, my $no, $no) = split(/\t/,$tmp1);

            $currenttime = time;
            $threadagelimit = $currenttime - $prunedays * 86400;
            if ($lastpostdate < $threadagelimit) {
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.thd.cgi";
                unlink $filetotrash;
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.mal.pl";
                unlink $filetotrash;
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.poll.pl";
                unlink $filetotrash;
                $filetotrash = "$lbdir" . "forum$inforum/$topicid.pl";
                unlink $filetotrash;
        	$filetounlink = "$lbdir" . "forum$inforum/rate$intopic.file.pl";
	        unlink $filetounlink;
        	$filetounlink = "$lbdir" . "forum$inforum/rateip$intopic.file.pl";
	        unlink $filetounlink;
		$dirtoopen2 = "$imagesdir" . "usr/$inforum";
        	opendir (DIR, "$dirtoopen2");
	        @dirdata2 = readdir(DIR);
        	closedir (DIR);
	        @dirdata2 = grep(/^$inforum\_$intopic/,@dirdata2);
	        @files = grep(/^$inforum\_$intopic\./,@dirdata2);
        	foreach $file (@files) {
	            $filetoremove = "$dirtoopen2/$file";
        	    unlink $filetoremove;
            	}
	        @files = grep(/^$inforum\_$intopic\_/,@dirdata2);
        	foreach $file (@files) {
	            $filetoremove = "$dirtoopen2/$file";
        	    unlink $filetoremove;
            	}
                $totaltopics_deleted++;
                $totalposts_deleted = $totalposts_deleted + $postcount;
	   }
	  }
	}

        rebuildLIST(-Forum=>"$inforum");

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen");
        @allforums = <FILE>;
        close(FILE);

        $filetomake = "$lbdir" . "data/allforums.cgi";
        $filetomake = &stripMETA($filetomake);
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) {
            chomp($forum);
            ($tempno, $trash) = split(/\t/,$forum);
            if ($inforum eq $tempno) {
               ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                $posts = $posts - $totalposts_deleted;
                $threads = $threads - $totaltopics_deleted;
                print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
            }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        require "$lbdir" . "data/boardstats.cgi";
        $filetomake   = "$lbdir" . "data/boardstats.cgi";
        $totalthreads = $totalthreads - $totaltopics_deleted;
        $totalposts   = $totalposts - $totalposts_deleted;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        if (! $totaltopics_deleted) { $totaltopics_deleted = "0"; }
        if (! $totalposts_deleted)  { $totalposts_deleted  = "0"; }
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>��̳�����Ѿ���ɾ��</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
            ͳ�����ϣ�
            <ul>
            <li>��ɾ�����⣺$totaltopics_deleted ƪ
            <li>��ɾ���ظ���$totalposts_deleted ƪ
            <li><a href="$forumsprog?forum=$inforum">������̳$savetopicid</a>
            <li><a href="$forumsummaryprog">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
	    ~;
	}
	else {
            &mischeader("����ɾ��");

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="prune">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <font face="$font" color=$fontcolormisc><b>������������ϸ�����Ա����ɾ��ģʽ[����ɾ��]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc><b>һ����ɾ�������£������ܹ��ָ���</b><br>���潫ɾ������ʱ�䳬��һ����������������¡������ȷ��������������ϸ������������Ϣ��</font></td>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>�����������û���</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>��������������</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>ɾ�����������������<br>���磺����'30'����ɾ������ 30 ����������¡�</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="prunedays"0></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="�� ��"></td></tr></form></table></td></tr></table>
            </table></td></tr></table>
	    ~;
	}
}
else { &error("��ͨ&δָ����������"); }
&output(
    -Title   => "$boardname - ����ɾ��",
    -ToPrint => $output,
    -Version => $versionnumber
);
