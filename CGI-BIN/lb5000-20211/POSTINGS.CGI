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
use File::Copy;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "postjs.cgi";
require "rebuildlist.pl";

$|++;                                     # Unbuffer the output
$thisprog = "postings.cgi";
$query = new LBCGI;

&ipbanned; #封杀一些 ip

$addme=$query->param('addme');
if ($arrowavaupload ne "on") { undef $addme; }
for ('forum','topic','membername','password','action','postno',
     'notify','deletepost','previewfirst','intopictitle','intopicdescription',
     'inpost','inshowemoticons','inshowsignature','checked','movetoid','leavemessage','posticon','newtopictitle') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
    }
$inforum       = $forum;
$intopic       = $topic;
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9 ]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9 ]+$/));
$inmembername  = $membername;
$inpassword    = $password;
$inpostno      = $postno;
$innotify      = $notify;
$indeletepost  = $deletepost;
$inleavemessage= $leavemessage;
$currenttime   = time;
$inposticon	= $posticon;

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

$maxupload = 300 if ($maxupload eq "");
$LBCGI::POST_MAX=1024 * $maxupload;

if ($inshowemoticons ne "yes") { $inshowemoticons eq "no"; }
if ($innotify ne "yes")        { $innotify eq "no"; }
        print header(-charset=>gb2312);
if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("普通错误&请不要修改生成的 URL！"); }
if (($movetoid) && ($movetoid !~ /^[0-9]+$/)) { &error("普通错误&请不要修改生成的 URL！"); }

if ($useemote eq "yes") {
    $filetoopen = "$lbdir" . "data/emote.cgi";
    open (FILE, "$filetoopen");
    flock (FILE, 1) if ($OS_USED eq "Unix");
    $emote = <FILE>;
    close (FILE);
}
else { undef $emote; }

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

	$addtypedisp = $addtype;
	$addtypedisp =~ s/\, /\,/gi;
	$addtypedisp =~ s/ \,/\,/gi;
	$addtypedisp =~ tr/A-Z/a-z/;
	my @addtypedisp = split(/\,/, $addtypedisp);
	$addtypedisp = "<select><option value=#>支持类型：</option><option value=#>----------</option>";
	foreach my $name (@addtypedisp) {
	  chomp $name;
    	  $addtypedisp .= qq~<option>$name</option>~;

	}
   	$addtypedisp .= qq~</select>~;

    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
    &error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
    $inmembername =~ s/\///g;
    $inmembername =~ s/\.\.//g;
    $inmembername =~ s/\\//g;
    if ($inmembername eq "") {
        $inmembername = "客人";
    }
&getmember("$inmembername");
$cpudisp = 1 if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"));
&getforum("$inforum");
my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t$forumname\tnone\t查看论坛上的主题\t") if ($privateforum ne "yes");
    &whosonline("$inmembername\t$forumname(密)\tnone\查看论坛上的主题\t") if ($privateforum eq "yes");
}
&badwordfile;

    if ($arrawpostpic eq "on") { $postpicstates = "允许";} else {$postpicstates = "禁止";}
    if ($arrawpostfontsize eq "on") { $postfontsizestates = "允许";} else {$postfontsizestates = "禁止";}
    if ($arrawpostsound eq "on") { $postsoundstates = "允许";} else {$postsoundstates = "禁止";}
    my %Mode = (
    'edit'                 =>    \&editform,
    'lock'                 =>    \&lockthread,
    'unlock'               =>    \&unlockthread,
    'delete'               =>    \&deletethread,
    'movetopic'            =>    \&movetopic,
    'puttop'               =>    \&puttop,
    'repireforum'          =>    \&repireforum,
    'locktop'		   =>	 \&locktop,
    'unlocktop'		   =>	 \&unlocktop
    );
    if($Mode{$action}) {
        $Mode{$action}->();
        }
        elsif ($action eq "processedit" && $indeletepost eq "yes") { &deletepost;   }
        elsif ($action eq "directdel") {&deletepost}
        elsif ($action eq "processedit" && $previewfirst eq "no")  { &processedit;  }
        elsif ($action eq "processedit" && $previewfirst eq "yes") { &editform;     }
        else { &error("普通&请以正确的方式访问本程序"); }
    &output(
    -Title   => $boardname,
    -ToPrint => $output,
    -Version => $versionnumber
    );
sub movetopic {

#    &getmember("$inmembername");
    &moderator;
    $cleartomove = "no";

    &mischeader("移动主题");

    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartomove = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartomove = 'yes'; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartomove = "yes"; }
    unless ($cleartomove eq "yes") { $cleartomove = "no"; }

        if ($cleartomove eq "no" && $checked eq "yes") { &error("移动主题&您不是坛主或版主，或者您的密码错误！"); }

        if (($cleartomove eq "yes") && ($checked eq "yes") && ($movetoid)) {
                if ($movetoid == $inforum) { &error("移动主题&不允许在同个论坛上移动主题！"); }

                ### Get a new thread number.
                $currenttime = time;

     undef $newthreadnumber;
     $filetoopen = "$lbdir" . "boarddata/lastnum$movetoid.cgi";
     if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $newthreadnumber = <FILE>;
        close(FILE);
        chomp $newthreadnumber;
	$newthreadnumber ++;
     }
      $filetoopen1 = "$lbdir" . "forum$movetoid/$newthreadnumber.pl";
      if ((!(-e $filetoopen1))&&($newthreadnumber =~ /^[0-9]+$/)) {
        if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE $newthreadnumber;
        close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
       }
       else {
        $dirtoopen = "$lbdir" . "forum$movetoid";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);
        @sorteddirdata = grep(/.thd.cgi$/,@dirdata);
        @newdirdata = sort numerically(@sorteddirdata);
        @neworderdirdata = reverse(@newdirdata);
        $highest = $neworderdirdata[0];
        $highest =~ s/.thd.cgi$//;
        $newthreadnumber = $highest + 1;

        if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE $newthreadnumber;
        close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
       }

                ### Get the old forum name

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                &winlock($filetoopen);
                open(FILE, "$filetoopen");
                flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);
                &winunlock($filetoopen);
                foreach $forumline (@forums) { #start foreach @forums
                    ($tempno, $trash) = split(/\t/,$forumline);
                        if ($inforum eq $tempno) {
                            ($trash, $trash, $trash, $oldforumname, $trash) = split(/\t/,$forumline);
                            last;
                        }
                    }

                ### Get the new forum name

                foreach $forumline (@forums) { #start foreach @forums
                    ($tempno, $trash) = split(/\t/,$forumline);
                        if ($movetoid eq $tempno) {
                            ($trash, $trash, $trash, $newforumname, $trash) = split(/\t/,$forumline);
                            last;
                        }
                    }

                    $inpostaddon = "<p>" if ($inpost ne "");
                    if ($movetopicname eq "on") {
                        $myinpost=qq~***** 版主模式 *****<p>$inpost$inpostaddon该贴子是管理员从<a href=$forumsprog?forum=$inforum>$oldforumname</a>转移过来的！~;
                    }
                    else { undef $myinpost; }
                    $myinpost="$inmembername\t$topictitle\t$ENV{'REMOTE_ADDR'}\tyes\tyes\t$currenttime\t$myinpost\t$inposticon\t\n";
                    $inpost = qq~***** 版主模式 *****<p>$inpost$inpostaddon<a href=$threadprog?forum=$movetoid&topic=$newthreadnumber>该贴子已被管理员转移，请点击这里查看</a>~;
                unless ($inleavemessage eq "no") {
                    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
		    if (-e $filetoopen) {
                        &winlock($filetoopen) if ($OS_USED eq "Nt");
                        open(FILE, "$filetoopen");
                        flock(FILE, 1) if ($OS_USED eq "Unix");
                        @allmessages = <FILE>;
                        close(FILE);
                        &winunlock($filetoopen) if ($OS_USED eq "Nt");
                    }
	  	    else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("移动主题&这个主题不存在！可能已经被删除！"); }

                    $linetokeep = $allmessages[0];
                    chomp $linetokeep;
                    ($trash, $topictitle, $trash) = split(/\t/,$linetokeep);

        	    $inforumtemp = $inforum;
                    $filetomake = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
		    &winlock($filetomake) if ($OS_USED eq "Nt");
                    if (open(FILE, ">$filetomake")) {
                    flock(FILE, 2) if ($OS_USED eq "Unix");
                        foreach $messages (@allmessages) {
                            chomp $messages;
                            print FILE "$messages\n";
                            }
                    print FILE "$inmembername\t$topictitle\t$ENV{'REMOTE_ADDR'}\tyes\tyes\t$currenttime\t$inpost\t$inposticon\t\n";
                    close(FILE);
                    }
	            &winunlock($filetomake) if ($OS_USED eq "Nt");

                    $threadposts = @allmessages;

                    my $file = "$lbdir" . "forum$inforum/$intopic.pl";
                    &winlock($file) if ($OS_USED eq "Nt");
                    open (ENT, $file);
                    flock(ENT, 2) if ($OS_USED eq "Unix");
                    $in = <ENT>;
                    close (ENT);
                    ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon,$inposttemp) = split(/\t/,$in);
		    $oldthreadstate = $threadstate;
		    if (($threadstate eq "poll")||($threadstate eq "pollclosed")) {
	                $threadstate = "pollclosed";
        	    }
	            else {
        	        $threadstate = "closed";
        	    }

                    if (open(FILE, ">$file")) {
                    flock(FILE, 2) if ($OS_USED eq "Unix");
                    $threadposts++;
                    $topicdescription2 = $topicdescription;
                    if ($movetopicname eq "on") {
                        $moveinfo = qq~此贴已被管理员$inmembername转移至： <a href=\"$forumsprog?forum=$movetoid\" target=\"_self\">$newforumname</a>~;
                    }
                    else { $moveinfo = ""; }
                    $inforumwrite = "$intopic\t$topictitle\t$moveinfo\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$inmembername\t$currenttime\t$lastinposticon\t$inposttemp\t";
                    print FILE $inforumwrite;
                    close(FILE);
                    }
		    &winunlock($file) if ($OS_USED eq "Nt");

            } # end if inleavemessage eq yes
            else { $myinpost = ""; }
        my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 1) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
        &winunlock($file) if ($OS_USED eq "Nt");
        ($topicid, $topictitle, $topicdescription1, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon,$inposttemp) = split(/\t/,$in);
        if ($inleavemessage eq "no") { #删除原贴
            $threadviews ++;
	    $threadposts ++;
        }

        if ($movetopicname eq "on") {
              $moveinfo = qq~此贴转移自： <a href=\"$boardurl/$forumsprog?forum=$inforum\" target=\"_self\">$oldforumname</a>~;
        }
        else { $moveinfo = ""; }
        my $file = "$lbdir" . "forum$movetoid/$newthreadnumber.pl";
        if (open(FILE, ">$file")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        $moveforumwrite = "$newthreadnumber\t$topictitle\t$moveinfo\t$oldthreadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$inmembername\t$currenttime\t$lastinposticon\t$inposttemp\t";
        print FILE $moveforumwrite;
        close(FILE);
        }
        ### Pick up old forum messages

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @oldforummessages = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        $oldthreadposts = @oldforummessages - 1;

        ### Print to new forum message file
        if ($inleavemessage ne "no") { #不删除原贴
            $oldthreadposts -- ;
        }
        $filetomake = "$lbdir" . "forum$movetoid/$newthreadnumber.thd.cgi";
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
       for ($i=0;$i<=$oldthreadposts;$i++){
            chomp $oldforummessages[$i];
            print FILE "$oldforummessages[$i]\n" if ($oldforummessages[$i] ne "");
            }
        if ($myinpost ne ""){
        print FILE "$myinpost";
        }
        close(FILE);
	}
   	
   	copy("${lbdir}forum$inforum/$intopic.mal.pl","${lbdir}forum$movetoid/$newthreadnumber.mal.pl") if (-e "${lbdir}forum$inforum/$intopic.mal.pl");
   	copy("${lbdir}forum$inforum/$intopic.poll.cgi","${lbdir}forum$movetoid/$newthreadnumber.poll.cgi") if (-e "${lbdir}forum$inforum/$intopic.poll.cgi");
   	copy("${lbdir}forum$inforum/rate$intopic.file.pl","${lbdir}forum$movetoid/rate$newthreadnumber.file.pl") if (-e "${lbdir}forum$inforum/rate$intopic.file.pl");
   	copy("${lbdir}forum$inforum/rateip$intopic.file.pl","${lbdir}forum$movetoid/rateip$newthreadnumber.file.pl") if (-e "${lbdir}forum$inforum/rateip$intopic.file.pl");

      $threadposts1 = $threadposts;

        require "$lbdir" . "data/boardstats.cgi";
        if ($inleavemessage ne "no") { #不删除原贴
            $totalthreads++;
            $totalposts = $totalposts + $threadposts + 1;
        }
        else {
            $totalposts ++;
        }
          $filetomake = "$lbdir" . "data/boardstats.cgi";
          my $filetoopens = &lockfilename($filetomake);
	  if (!(-e "$filetoopens.lck")) {
	    &winlock($filetomake) if ($OS_USED eq "Nt");
            if (open(FILE, ">$filetomake")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
            print FILE "\$totalmembers = \'$totalmembers\'\;\n";
            print FILE "\$totalthreads = \'$totalthreads\'\;\n";
            print FILE "\$totalposts = \'$totalposts\'\;\n";
            print FILE "\n1\;";
            close (FILE);
            }
            &winunlock($filetomake) if ($OS_USED eq "Nt");
          }

        $dirtoopen2 = "$imagesdir" . "usr/$inforum";
        $dirtoopen3 = "$imagesdir" . "usr/$movetoid";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = grep(/^$inforum\_/,@dirdata2);
        @files1 = grep(/^$inforum\_$intopic\./,@files);
        $files1 = @files1;
	if ($files1 > 0) {
	    foreach (@files1) {
	    	(my $name,my $ext) = split(/\./,$_);
		copy("$dirtoopen2/$inforum\_$intopic\.$ext","$dirtoopen3/$movetoid\_$newthreadnumber\.$ext") if (-e "$dirtoopen2/$inforum\_$intopic\.$ext");
	    }
	}

        @files1 = grep(/^$inforum\_$intopic\_/,@files);
        $files1 = @files1;
	if ($files1 > 0) {
	    foreach (@files1) {
	    	(my $name,my $ext) = split(/\./,$_);
	    	(my $name1,my $name2,my $name3) = split(/\_/,$name);
		copy("$dirtoopen2/$inforum\_$intopic\_$name3\.$ext","$dirtoopen3/$movetoid\_$newthreadnumber\_$name3\.$ext") if (-e "$dirtoopen2/$inforum\_$intopic\_$name3\.$ext");
	    }
	}

        if ($inleavemessage ne "yes") {
          $filetounlink = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
          unlink $filetounlink;
          $filetounlink = "$lbdir" . "forum$inforum/$intopic.poll.cgi";
          unlink $filetounlink;
          $filetounlink = "$lbdir" . "forum$inforum/$intopic.mal.pl";
          unlink $filetounlink;
          $filetounlink = "$lbdir" . "forum$inforum/rate$intopic.file.pl";
          unlink $filetounlink;
          $filetounlink = "$lbdir" . "forum$inforum/rateip$intopic.file.pl";
          unlink $filetounlink;
          my $file = "$lbdir" . "forum$inforum/$intopic.pl";
          unlink $file;
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


	$filetomakeopen = "$lbdir" . "data/recentpost.cgi";
	&winlock($filetomakeopen) if ($OS_USED eq "Nt");
	open(FILE, "$filetomakeopen");
	flock (FILE, 1) if ($OS_USED eq "Unix");
	@recentposts=<FILE>;
	close(FILE);
	if (open (FILE, ">$filetomakeopen")) {
	flock (FILE, 2) if ($OS_USED eq "Unix");
	foreach (@recentposts) {
	    chomp $_;
	    ($tempno1, $tempno2, $tempno3, $tempno4, $tempno5) = split (/\t/,$_);
	    next if (($tempno1 !~ /^[0-9]+$/)||($tempno2 !~ /^[0-9]+$/));
	    my $checkme=0;
	    $checkme = 1 if ($intopic eq $tempno2);
	    unless (($tempno1 eq $inforum)&&($checkme eq 1)) {
		print FILE "$_\n"
	    }
	    else {
	    	print FILE "$movetoid\t$newthreadnumber\t$tempno3\t$tempno4\t$tempno5\t\n";
	    }
	}
	close(FILE);
	}
	&winunlock($filetomakeopen) if ($OS_USED eq "Nt");

	$filetoopen = "$lbdir" . "boarddata/ontop$inforum.cgi";
	if (-e $filetoopen) {
	    &winlock($filetoopen);
	    open(FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @ontop = <FILE>;
            close(FILE);

            if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
	    foreach (@ontop) {
		chomp $_;
		my $checkme=0;
	        print FILE "$_\n" if ($intopic ne $_);
	    }
            close(FILE);
            }
            &winunlock($filetoopen);
	}


        } # end unless statement

        $file = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
	$listall = @listall;

    if ($listall >= 200) {
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        print LIST "$inforumwrite\n" if ($inleavemessage ne "no");
        foreach (@listall) {
          (my $useid,my $no)=split(/\t/,$_);
	  $_ =~ s/[\n\r]//isg;
	  print LIST "$_\n" if (($useid ne $intopic)&&($useid ne "")&&($useid =~ /^[0-9]+$/));
        }
        close (LIST);
        }
        &winunlock($file);
    }
    else {
        &winunlock($file);
        rebuildLIST(-Forum=>"$inforum");
    }

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);
        &winunlock($filetoopen);

      $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
      $filetomake = "$lbdir" . "data/allforums.cgi";
      my $filetoopens1 = &lockfilename($filetoopen);
      my $filetoopens2 = &lockfilename($filetomake);

      if ((!(-e "$filetoopens1.lck"))||(!(-e "$filetoopens2.lck"))) {
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $linetokeep = <FILE>;
        close(FILE);
        &winunlock($filetoopen);

        chomp $linetokeep;
        ($topicid, $topictitle, $trash, $trash, $trash, $trash, $lastforumposter1, $trash, $lastforumposter, $lastforumpostdate) = split(/\t/,$linetokeep);

        &winlock($filetomake);
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
        next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    if ($inleavemessage eq "no") { #删除原贴
                    	$threads--;
                        $posts = $posts - $threadposts1;
                    }
                    else { $posts++; }
                    $currenttime = time;
                    $lastforumposter = $lastforumposter1 if ($lastforumposter eq "");
                    $lastforumpostdate = "$currenttime\%\%\%$topicid\%\%\%$topictitle";
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastforumposter\t$lastforumpostdate\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        open(FILE, "$filetomake");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        $file = "$lbdir" . "boarddata/list$movetoid.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
	$listall = @listall;

	if ($listall >= 200) {
            if (open (LIST, ">$file")) {
            flock (LIST, 2) if ($OS_USED eq "Unix");
            print LIST "$moveforumwrite\n";
            foreach (@listall) {
		(my $useid,my $no)=split(/\t/,$_);
		$_ =~ s/[\n\r]//isg;
		print LIST "$_\n" if (($useid ne "")&&($useid =~ /^[0-9]+$/));
            }
            close (LIST);
            }
            &winunlock($file);
	}
	else {
            &winunlock($file);
            rebuildLIST(-Forum=>"$movetoid");
	}
      }

      $filetoopen = "$lbdir" . "boarddata/list$movetoid.cgi";
      $filetomake = "$lbdir" . "data/allforums.cgi";
      my $filetoopens1 = &lockfilename($filetoopen);
      my $filetoopens2 = &lockfilename($filetomake);
      if ((!(-e "$filetoopens1.lck"))||(!(-e "$filetoopens2.lck"))) {
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $linetokeep = <FILE>;
        close(FILE);
        &winunlock($filetoopen);

        chomp $linetokeep;
        ($topicid, $topictitle, $trash, $trash, $trash, $trash, $lastforumposter1, $trash, $lastforumposter, $lastforumpostdate) = split(/\t/,$linetokeep);

        &winlock($filetomake);
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
        next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($movetoid eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    $currenttime = time;
                    $threads++;
                    $posts = $posts + $threadposts1;
                    $lastforumposter = $lastforumposter1 if ($lastforumposter eq "");
                    $lastforumpostdate = "$currenttime\%\%\%$topicid\%\%\%$topictitle";
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastforumposter\t$lastforumpostdate\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetomake);
      }

        $relocurl = "$forumsprog?forum=$inforum";

        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>主题已经移动</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回原论坛</a>
            <li><a href="$forumsprog?forum=$movetoid">返回新论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
            $checked = "no";

        } # end clear to move if

        else {

            $filetoopen = "$lbdir" . "data/allforums.cgi";
            &winlock($filetoopen);
            open(FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @forums = <FILE>;
            close(FILE);
            &winunlock($filetoopen);
            $jumphtml .= "<option value=\"\">选择一个论坛\n</option>";

            foreach $forum (@forums) { #start foreach @forums
                chomp $forum;
	        next if ($forum eq "");
                ($movetoforumid, $category, $categoryplace, $forumname, $forumdescription, $noneed ,$noneed ,$noneed ,$noneed, $noneed ,$noneed ,$noneed, $noneed, $noneed, $noneed, $ratings, $noneed,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
    	    	next if ($movetoforumid !~ /^[0-9]+$/);
    	    	next if ($categoryplace !~ /^[0-9]+$/);
                $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$movetoforumid\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
                push (@rearrangedforums, $rearrange);
            } # end foreach (@forums)
            @finalsortedforums = sort numerically(@rearrangedforums);
            foreach $sortedforums (@finalsortedforums) { #start foreach
            ($categoryplace, $category, $forumname, $forumdescription, $movetoforumid, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$sortedforums);

            if ($categoryplace ne $lastcategoryplace) { #start if $categoryplace
                $jumphtml .= "<option value=\"\"> >>>&nbsp;$category <<<\n</option>";
                $jumphtml .= "<option value=\"$movetoforumid\">$forumname\n</option>";
                }
                else {
                    $jumphtml .= "<option value=\"$movetoforumid\">$forumname\n</option>";
                    }
                $lastcategoryplace = $categoryplace;
                } # end foreach

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
                <tr>
                    <td>
                    <table cellpadding=6 cellspacing=1 border=0 width=100%>
                        <tr>
                        <td bgcolor=$miscbacktwo align=center colspan=2>
                        <form action="$thisprog" method="post">
                        <input type=hidden name="action" value="movetopic">
                        <input type=hidden name="checked" value="yes">
                        <input type=hidden name="forum" value="$inforum">
                        <input type=hidden name="topic" value="$intopic">
                        <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [移动主题]</b></font></td></tr>
                                <tr>
                                <td bgcolor=$miscbackone width=40%><font color=$fontcolormisc><b>请输入您的用户名</b></font></td>
                                <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0</td></tr>
                                    <tr>
                                    <td bgcolor=$miscbackone><font color=$fontcolormisc><b>请输入您的密码</b></font></td>
                                    <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
                                    <tr>
                                    <td bgcolor=$miscbackone><font color=$fontcolormisc>
                                    <b>移动选项</td>
                                    <td bgcolor=$miscbackone><font color=$fontcolormisc>
                                    <input name="leavemessage" type="radio" value="yes" checked> 移动并保留一个已经锁定的主题在原论坛<br><input name="leavemessage" type="radio" value="no"> 移动并将此主题从原论坛中删除</font>
                                    </td>
                                    </tr>
<tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>当前心情</b><br><li>将放在贴子的前面<BR></font></td>
<td bgcolor=$miscbackone valign=top>
~;

    open (FILE, "${lbdir}data/lbpost.cgi");
     my @posticondata = <FILE>;
     close (FILE);
     chomp @posticondata;

    $tempiconnum=1;
#    $tempselect = "checked";
    foreach $picture (@posticondata) {
       $posticonname = $picture;
       $posticonname =~ s/\.gif$//g;
       if ($tempiconnum > 12) {
    	   $tempiconnum = 1;
    	   $output .= qq~<BR>~;
       }
       if ($picture eq $posticon) {$tempselect = "checked";} else {$tempselect = "";}
       $output .= qq~<input type=radio value="$picture" name="posticon" $tempselect><img src="$imagesurl/posticons/$picture" $defaultsmilewidth $defaultsmileheight border=0>&nbsp;~;
       $tempiconnum ++;
       $tempselect = "";
    } #endforeach
$output .= qq~
</td>
</tr>
                                <tr>
                                <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>信息：</b><p>
                                这个是可选的，可以填入一些说明信息。<p> 移动后的目标地址会自动输入在主题中。
                                </font></td>
                                <td bgcolor=$miscbackone><textarea cols=80 rows=9 wrap="soft" name="inpost"></textarea></td>
                                </tr>
                            <tr>
                        <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>转移至：</b></font></td>
                        <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><select name="movetoid">$jumphtml</select></font></td>
                        </tr>
                    <tr>
                <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="提 交"></td></tr></form></table></td></tr></table>
            </table>
            </td></tr>
            </table>
            ~;

             } # end else
} # end movetopic
sub deletethread {
    &mischeader("删除主题");
#    &getmember("$inmembername");
    &moderator;
    $cleartoedit = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    $alldeltopic = 0;

    if ($checked eq "yes"){ #1
        @intopic=split(/ /,$intopic);
        $alldeltopic=@intopic;
        foreach $intopic (@intopic){#2
            $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
            if (-e $filetoopen) {#3
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, "$filetoopen");
		flock(FILE, 1) if ($OS_USED eq "Unix");
		@threads = <FILE>;
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");

	    	$linetemp=$threads[0];
	    	($startedby, my $no, $no, $no, $no ,$no, $no, $no, $no, $no) = split(/\t/,$linetemp);

        	if ($arrowuserdel eq "on") {
            	    if ((lc($inmembername) eq lc($startedby)) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
        	}

		unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

        	if ($cleartoedit eq "no") { &error("删除主题&您不是本论坛坛主或版主，也不是本主题的发布者，或者您的密码错误！"); }
        	if ($cleartoedit eq "yes") {#4
    		  if ((($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"))&&($inmembername ne $startedby)) {#5
	  	    $nametocheck = $startedby;
	  	    $nametocheck =~ s/ /\_/g;
	  	    $nametocheck =~ tr/A-Z/a-z/;
	  	    my $filetoopen = "$lbdir" . "$memdir/$nametocheck.cgi";
	  	    $filetoopen = &stripMETA($filetoopen);
	  	    if (-e $filetoopen) {#6
	    		&winlock($filetoopen);
	    		open(FILE,"$filetoopen");
	    		flock (FILE, 1) if ($OS_USED eq "Unix");
            		my $filedata = <FILE>;
            		close(FILE);
	    		chomp($filedata);
	    		(my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $aolname, my $icqnumber ,my $location ,my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $misc1,my  $userxz, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno,my  $addjy,my  $meili, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $useradd1, my $useradd2, my $jhmp,my $useradd3, my $useradd4, my $useradd5, my $useradd6, my $useradd7, my $useradd8 ) = split(/\t/,$filedata);
	  		if (($membername ne "")&&($password ne "")) {#7
	    		    open(FILE,">$filetoopen");
	    		    flock (FILE, 2) if ($OS_USED eq "Unix");
	    		    $lastgone=time;
	    		    $postdel ++;
	    		    print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t\n";
	    		    close(FILE);
	  		}#7
	    		&winunlock($filetoopen);
	  	    }#6
		  }#5

		  $postcount = @threads;
        	  $postcount--;
		  $alldelpost=$postcount+$alldelpost;
		  $filetotrash = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        	  unlink "$filetotrash";
        	  $filetotrash = "$lbdir" . "forum$inforum/$intopic.mal.pl";
        	  unlink "$filetotrash";
        	  $filetotrash = "$lbdir" . "forum$inforum/$intopic.poll.pl";
        	  unlink "$filetotrash";
        	  $filetounlink = "$lbdir" . "forum$inforum/rate$intopic.file.pl";
        	  unlink $filetounlink;
        	  $filetounlink = "$lbdir" . "forum$inforum/rateip$intopic.file.pl";
        	  unlink $filetounlink;
        	  $dirtoopen2 = "$imagesdir" . "usr/$inforum";
        	  opendir (DIR, "$dirtoopen2");
        	  @dirdata2 = readdir(DIR);
        	  closedir (DIR);
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

            	  my $file = "$lbdir" . "forum$inforum/$intopic.pl";
            	  unlink $file;
	        }#4
	    }#3
    	    else { $alldeltopic -- ; }
	}#2

    if ($alldeltopic > $logdelmax){
	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$trueipaddress = "no" if (($trueipaddress eq "")||($trueipaddress eq "unknown"));
	my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$trueipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
	my $thistime=time;
#	&getforum($inforum);
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
      if ($delcount > $maxdeloneday){&error("删除主题&你今天删除帖子太多，请明天继续！");} 
      if ($delcou > $maxdeloneday)  {&error("删除主题&你今天删除帖子太多，请明天继续！");} 
      undef $delcount; 
      undef $delcou; 
    }
    if (open(FILE, ">>$filetomake")) {
    print FILE "$inmembername\t密码不显示\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t删除$forumname $alldeltopic 个贴子\t$thistime\t\n";
    close(FILE);
    }
    undef $thistime;
    &winunlock($filetomake); 
    }

    if ($cleartoedit eq "no")  { &error("删除主题&您不是本论坛坛主或版主，也不是本主题的发布者，或者您的密码错误！"); }
    if ($cleartoedit eq "yes") {
       	undef @sortdat;
	$file = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
        &winunlock($file);
	$listall = @listall;

        if ($listall >= 200) {
            &winlock($file);
            if (open (LIST, ">$file")) {
            flock (LIST, 2) if ($OS_USED eq "Unix");
            foreach (@listall) {
		($listone, $noneed) = split(/\t/,$_);
		next if ($listone !~ /^[0-9]+$/);
		my $checkme=0;
		foreach $intopic (@intopic){
		    if ($listone eq $intopic) {
			$checkme=1;
		    }
		}
		print LIST "$_" if ($checkme ==0);
		push(@sortdat, $_) if ($checkme ==0);
	    }
	    close (LIST);
	    }
	    &winunlock($file);
	}
	else {
	    rebuildLIST(-Forum=>"$inforum");
	}

	$filetomakeopen = "$lbdir" . "data/recentpost.cgi";
	&winlock($filetomakeopen) if ($OS_USED eq "Nt");
	open(FILE, "$filetomakeopen");
	flock (FILE, 1) if ($OS_USED eq "Unix");
	@recentposts=<FILE>;
	close(FILE);
	if (open (FILE, ">$filetomakeopen")) {
	flock (FILE, 2) if ($OS_USED eq "Unix");
	foreach (@recentposts) {
	    chomp $_;
	    ($tempno1, $tempno2, $no) = split (/\t/,$_);
	    next if (($tempno1 !~ /^[0-9]+$/)||($tempno2 !~ /^[0-9]+$/));
	    my $checkme=0;
	    $checkme = 1 if ($intopic eq $tempno2);
	    foreach $intopic (@intopic){
		if ($tempno2 eq $intopic) {
		    $checkme=1;
		}
	    }
	    unless (($tempno1 eq $inforum)&&($checkme eq 1)) {
		print FILE "$_\n"
	    }
	}
	close(FILE);
	}
	&winunlock($filetomakeopen) if ($OS_USED eq "Nt");

	$filetoopen = "$lbdir" . "boarddata/ontop$inforum.cgi";
	if (-e $filetoopen) {
	    &winlock($filetoopen);
	    open(FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @ontop = <FILE>;
            close(FILE);

            if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
	    foreach (@ontop) {
		chomp $_;
		my $checkme=0;
	        $checkme = 1 if ($intopic eq $_);
          	foreach $intopic (@intopic){
	    	    if ($_ eq $intopic) {
	      	        $checkme=1;
	            }
	        }
	        print FILE "$_\n" if ($checkme ==0);
	    }
            close(FILE);
            }
            &winunlock($filetoopen);
	}

      $filetoopen = "$lbdir" . "data/allforums.cgi";
      $filetoopen1 = "$lbdir" . "boarddata/list$inforum.cgi";
      my $filetoopens1 = &lockfilename($filetoopen);
      my $filetoopens2 = &lockfilename($filetoopen1);
      if ((!(-e "$filetoopens1.lck"))&&(!(-e "$filetoopens2.lck"))) {
        $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $linetokeep = <FILE>;
        close(FILE);
        &winunlock($filetoopen);

        chomp $linetokeep;
        ($topicid, $topictitle, $trash, $trash, $trash, $trash, $lastforumposter1, $trash, $lastforumposter, $lastforumpostdate) = split(/\t/,$linetokeep);

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);

        $filetomake = "$lbdir" . "data/allforums.cgi";
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
        next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    $posts = $posts - $alldelpost;
                    $threads=$threads-$alldeltopic;
                    $lastforumposter = $lastforumposter1 if ($lastforumposter eq "");
                    $lastforumpostdate = "$lastforumpostdate\%\%\%$topicid\%\%\%$topictitle";
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastforumposter\t$lastforumpostdate\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
      }
        require "$lbdir" . "data/boardstats.cgi";

      $filetomake = "$lbdir" . "data/boardstats.cgi";
      my $filetoopens = &lockfilename($filetomake);
      if (!(-e "$filetoopens.lck")) {
        $totalthreads=$totalthreads-$alldeltopic;
        $totalposts = $totalposts - $alldelpost;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        }
	&winunlock($filetomake) if ($OS_USED eq "Nt");
      }
    }#1

           $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>删除成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$forumsprog?forum=$inforum">
            ~;
            }

            else {
            @intopic = $query -> param('topic');
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post" enctype="multipart/form-data">
            <input type=hidden name="action" value="delete">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="@intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [删除主题]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc><b>该操作是不可逆的，请仔细考虑！</font></td>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></tr></form></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end deletethread
sub lockthread {
#    &getmember("$inmembername");

    &moderator;
    $cleartoedit = "no";

    &mischeader("主题锁定");
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        if (-e $filetoopen) {
           &winlock($filetoopen) if ($OS_USED eq "Nt");
           open(FILE, "$filetoopen");
           flock(FILE, 1) if ($OS_USED eq "Unix");
           @threads = <FILE>;
           close(FILE);
           &winunlock($filetoopen) if ($OS_USED eq "Nt");
        }
	else { &error("主题锁定&这个主题不存在！"); }

	$linetemp=$threads[0];
	($startedby, my $no, $no, $no, $no ,$no, $no, $no, $no, $no) = split(/\t/,$linetemp);

        if ($arrowuserdel eq "on") {
            if ((lc($inmembername) eq lc($startedby)) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
        }

        unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no" && $checked eq "yes") { &error("主题锁定&您不是本论坛坛主或版主，或者您的密码错误！"); }

        if (($cleartoedit eq "yes") && ($checked eq "yes")) {

        my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 1) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
        &winunlock($file) if ($OS_USED eq "Nt");
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $tmp,$inposttemp) = split(/\t/,$in);

        if (($threadstate eq "poll")||($threadstate eq "pollclosed")) {
             $threadstate = "pollclosed";
        }
        else {
            $threadstate = "closed";
        }

        &winlock($file) if ($OS_USED eq "Nt");
        if (open(FILE, ">$file")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t\t$inposttemp\t";
        close(FILE);
        }
        &winunlock($file) if ($OS_USED eq "Nt");
        my $file1 = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        open (TMP1, "$file1");
        @tmp = <TMP1>;
        close (TMP);
        $tmp1 = $tmp[-1];
        ($no, $no, $no, $no, $no ,$no, $post1, $no) = split(/\t/,$tmp1);
	$inposttemp = $post1;
	$inposttemp =~ s/\[这个贴子最后由(.+?)编辑\]\n//isg;
	$inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	$inposttemp =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]//isg;
	$inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]//isg;
	$maxsmailtemp = $maxsmail;
	$maxsmail     = 0;
	$inposttemp   = &doemoticons("$inposttemp");
	$maxsmail     = $maxsmailtemp;
	$inposttemp =~ s/\<img\s*(.*?)\s*\>//isg;
	$inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)//isg;
	$inposttemp =~ s/( )+$//isg;
	$inposttemp =~ s/^( )+//isg;
	$inposttemp =~ s/<(.|\n)+?>//g;
	$inposttemp =~ s/\[.+?\]//g;
	$inposttemp =~ s/[\a\f\n\e\0\r\t\n]//g;

        $inposttemp = &lbhz($inposttemp,$maxsavepost);
        $file = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
        &winunlock($file);
	$listall = @listall;

    if ($listall >= 200) {
        &winlock($file);
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        foreach (@listall) {
            ($listone,$noneed) = split(/\t/,$_);
	    next if ($listone !~ /^[0-9]+$/);
            if ($listone ne $intopic) {
                print LIST "$_";
            }
            else {
                print LIST "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t\n";
            }
        }
        close (LIST);
        }
        &winunlock($file);
    }
    else {
        rebuildLIST(-Forum=>"$inforum");
    }


            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>主题锁定成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$forumsprog?forum=$inforum">
            ~;

            } # end if clear to edit

            else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="lock">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题锁定]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end lockthread
sub repireforum {
#    &getmember("$inmembername");
    &moderator;
    $cleartoedit = "no";

    &mischeader("论坛修复");
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no" && $checked eq "yes") { &error("论坛修复&您不是本论坛坛主或版主，或者您的密码错误！"); }

        if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        rebuildLIST(-Forum=>"$inforum");
        ### Get the new last forum poster, and post date.

      $filetoopen = "$lbdir" . "data/allforums.cgi";
      $filetoopen1 = "$lbdir" . "boarddata/list$inforum.cgi";
      my $filetoopens1 = &lockfilename($filetoopen);
      my $filetoopens2 = &lockfilename($filetoopen1);
      if ((!(-e "$filetoopens1.lck"))&&(!(-e "$filetoopens2.lck"))) {
        $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $linetokeep = <FILE>;
        close(FILE);
        &winunlock($filetoopen);

        chomp $linetokeep;
        ($topicid, $topictitle, $trash, $trash, $trash, $trash, $lastforumposter1, $trash, $lastforumposter, $lastforumpostdate) = split(/\t/,$linetokeep);


        $filetoopen = "$lbdir" . "data/allforums.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);

        $filetomake = "$lbdir" . "data/allforums.cgi";
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
        next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    $posts = $posts - $postcount;
                    $threads--;
                    $lastforumposter = $lastforumposter1 if ($lastforumposter eq "");
                    $lastforumpostdate = "$lastforumpostdate\%\%\%$topicid\%\%\%$topictitle";
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastforumposter\t$lastforumpostdate\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetomake);
      }
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>论坛修复成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$forumsprog?forum=$inforum">
            ~;

            } # end if clear to edit

            else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="repireforum">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [论坛修复]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end lockthread
sub puttop {
#    &getmember("$inmembername");

    &moderator;
    $cleartoedit = "no";

    &mischeader("主题提升");
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit  = "yes"; }

    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no" && $checked eq "yes") { &error("主题提升&您不是本论坛坛主或版主，或者您的密码错误！"); }

        if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 1) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
        &winunlock($file) if ($OS_USED eq "Nt");
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate,$tmp,$inposttemp) = split(/\t/,$in);
 	$topictitle =~ s/^＊＃！＆＊//;

        &winlock($file) if ($OS_USED eq "Nt");
        if (open(FILE, ">$file")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t\t$inposttemp\t";
        close(FILE);
        }
        &winunlock($file) if ($OS_USED eq "Nt");
        my $file1 = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        open (TMP1, "$file1");
        @tmp = <TMP1>;
        close (TMP);
        $tmp1 = $tmp[-1];
        ($no, $no, $no, $no, $no ,$no, $post1, $no) = split(/\t/,$tmp1);
	$inposttemp = $post1;
	$inposttemp =~ s/\[这个贴子最后由(.+?)编辑\]\n//isg;
	$inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	$inposttemp =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]//isg;
	$inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]//isg;
	$maxsmailtemp = $maxsmail;
	$maxsmail     = 0;
	$inposttemp   = &doemoticons("$inposttemp");
	$maxsmail     = $maxsmailtemp;
	$inposttemp =~ s/\<img\s*(.*?)\s*\>//isg;
	$inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)//isg;
	$inposttemp =~ s/( )+$//isg;
	$inposttemp =~ s/^( )+//isg;
	$inposttemp =~ s/<(.|\n)+?>//g;
	$inposttemp =~ s/\[.+?\]//g;
	$inposttemp =~ s/[\a\f\n\e\0\r\t\n]//g;

        $inposttemp = &lbhz($inposttemp,$maxsavepost);
        $file = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
        &winunlock($file);
	$listall = @listall;

    if ($listall >= 200) {
        &winlock($file);
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        print LIST "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t$inposticon\t$inposttemp\t\n";
        foreach (@listall) {
            ($listone,$noneed) = split(/\t/,$_);
	    next if ($listone !~ /^[0-9]+$/);
            print LIST "$_" if ($listone ne $intopic);
        }
        close (LIST);
        }
        &winunlock($file);
    }
    else {
        rebuildLIST(-Forum=>"$inforum");
    }
        ### Get the new last forum poster, and post date.

      $filetoopen = "$lbdir" . "data/allforums.cgi";
      $filetoopen1 = "$lbdir" . "boarddata/list$inforum.cgi";
      my $filetoopens1 = &lockfilename($filetoopen);
      my $filetoopens2 = &lockfilename($filetoopen1);
      if ((!(-e "$filetoopens1.lck"))&&(!(-e "$filetoopens2.lck"))) {
        $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $linetokeep = <FILE>;
        close(FILE);
        &winunlock($filetoopen);

        chomp $linetokeep;
        ($topicid, $topictitle, $trash, $trash, $trash, $trash, $lastforumposter1, $trash, $lastforumposter, $lastforumpostdate) = split(/\t/,$linetokeep);


        $filetoopen = "$lbdir" . "data/allforums.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);

        $filetomake = "$lbdir" . "data/allforums.cgi";
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
        next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    $lastforumposter = $lastforumposter1 if ($lastforumposter eq "");
                    $lastforumpostdate = "$lastforumpostdate\%\%\%$topicid\%\%\%$topictitle";
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastforumposter\t$lastforumpostdate\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetomake);
    }
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>主题提升成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$forumsprog?forum=$inforum">
            ~;

            } # end if clear to edit

            else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="puttop">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题提升]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end lockthread
sub unlockthread {
#    &getmember("$inmembername");
    &moderator;
    $cleartoedit = "no";


    &mischeader("主题解锁");
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit  = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

        if ($cleartoedit eq "no" && $checked eq "yes") { &error("主题解锁&您不是本论坛坛主或版主，或者您的密码错误！"); }
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {

        my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 1) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
        &winunlock($file) if ($OS_USED eq "Nt");
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate,$inposttemp) = split(/\t/,$in);
 	$topictitle =~ s/^＊＃！＆＊//;

        if (($threadstate eq "pollclosed")||($threadstate eq "poll")) {
             $threadstate = "poll";
        }
        else {
            $threadstate = "open";
        }
        &winlock($file) if ($OS_USED eq "Nt");
        if (open(FILE, ">$file")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposttemp\t";
        close(FILE);
        }
        &winunlock($file) if ($OS_USED eq "Nt");
        my $file1 = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        open (TMP1, "$file1");
        @tmp = <TMP1>;
        close (TMP);
        $tmp1 = $tmp[-1];
        ($no, $no, $no, $no, $no ,$no, $post1, $no) = split(/\t/,$tmp1);
	$inposttemp = $post1;
	$inposttemp =~ s/\[这个贴子最后由(.+?)编辑\]\n//isg;
	$inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	$inposttemp =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]//isg;
	$inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]//isg;
	$maxsmailtemp = $maxsmail;
	$maxsmail     = 0;
	$inposttemp   = &doemoticons("$inposttemp");
	$maxsmail     = $maxsmailtemp;
	$inposttemp =~ s/\<img\s*(.*?)\s*\>//isg;
	$inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)//isg;
	$inposttemp =~ s/( )+$//isg;
	$inposttemp =~ s/^( )+//isg;
	$inposttemp =~ s/<(.|\n)+?>//g;
	$inposttemp =~ s/\[.+?\]//g;
	$inposttemp =~ s/[\a\f\n\e\0\r\t\n]//g;

        $inposttemp = &lbhz($inposttemp,$maxsavepost);
        $file = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
        &winunlock($file);
	$listall = @listall;

    if ($listall >= 200) {
        &winlock($file);
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        foreach (@listall) {
            ($listone,$noneed) = split(/\t/,$_);
	    next if ($listone !~ /^[0-9]+$/);
            if ($listone ne $intopic) {
        	print LIST "$_";
            }
            else {
	        print LIST "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t\n";
	    }
        }
        close (LIST);
        }
        &winunlock($file);
    }
    else {
        rebuildLIST(-Forum=>"$inforum");
    }


            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>主题解锁成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$forumsprog?forum=$inforum">
            ~;
            } # end if clear to edit

            else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="unlock">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题解锁]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end unlockthread
sub locktop {
#    &getmember("$inmembername");

    &moderator;
    $cleartoedit = "no";

    &mischeader("主题固定");
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no" && $checked eq "yes") { &error("主题固定首行&您不是本论坛坛主或版主，或者您的密码错误！"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
      my $file = "$lbdir" . "boarddata/ontop$inforum.cgi";
      if (-e $file) {
        open (ENT, $file);
        flock(ENT, 1) if ($OS_USED eq "Unix");
        @toptopic = <ENT>;
        close (ENT);
        if (open (ENT, ">$file")) {
        flock(ENT, 2) if ($OS_USED eq "Unix");
        print ENT "$intopic\n";
	$putno = 1;
	foreach $topic (@toptopic) {
	    chomp $topic;
	    if ($topic ne $intopic) {
	    	print ENT "$topic\n";
	    	$putno ++;
	    }
	    last if ($putno eq $maxtoptopic);
	}
        close (ENT);
        }
      }
      else {
        if (open (ENT, ">$file")) {
        flock(ENT, 2) if ($OS_USED eq "Unix");
        print ENT "$intopic\n";
        close (ENT);
        }
      }

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>主题固定首行成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$forumsprog?forum=$inforum">
            ~;

    } # end if clear to edit
    else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="locktop">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题固定首行]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end
sub unlocktop {
#    &getmember("$inmembername");

    &moderator;
    $cleartoedit = "no";

    &mischeader("主题取消固定");
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no" && $checked eq "yes") { &error("主题取消固定&您不是本论坛坛主或版主，或者您的密码错误！"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
      my $file = "$lbdir" . "boarddata/ontop$inforum.cgi";
      if (-e $file) {
        open (ENT, $file);
        flock(ENT, 1) if ($OS_USED eq "Unix");
        @toptopic = <ENT>;
        close (ENT);

        if (open (ENT, ">$file")) {
        flock(ENT, 2) if ($OS_USED eq "Unix");
	foreach $topic (@toptopic) {
	    chomp $topic;
	    if ($topic ne $intopic) {
	    	print ENT "$topic\n";
	    }
	}
        close (ENT);
        }
      }

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>主题取消固定成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$forumsprog?forum=$inforum">
            ~;

    } # end if clear to edit
    else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="unlocktop">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题取消固定]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end
sub unlockthread {
#    &getmember("$inmembername");
    &moderator;
    $cleartoedit = "no";


    &mischeader("主题解锁");
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

        if ($cleartoedit eq "no" && $checked eq "yes") { &error("主题解锁&您不是本论坛坛主或版主，或者您的密码错误！"); }
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {

        my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 1) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
        &winunlock($file) if ($OS_USED eq "Nt");
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate,$inposttemp) = split(/\t/,$in);
 	$topictitle =~ s/^＊＃！＆＊//;

        if (($threadstate eq "pollclosed")||($threadstate eq "poll")) {
             $threadstate = "poll";
        }
        else {
            $threadstate = "open";
        }
        &winlock($file) if ($OS_USED eq "Nt");
        if (open(FILE, ">$file")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposttemp\t";
        close(FILE);
        }
        &winunlock($file) if ($OS_USED eq "Nt");
        my $file1 = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        open (TMP1, "$file1");
        @tmp = <TMP1>;
        close (TMP);
        $tmp1 = $tmp[-1];
        ($no, $no, $no, $no, $no ,$no, $post1, $no) = split(/\t/,$tmp1);
	$inposttemp = $post1;
	$inposttemp =~ s/\[这个贴子最后由(.+?)编辑\]\n//isg;
	$inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	$inposttemp =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]//isg;
	$inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]//isg;
	$maxsmailtemp = $maxsmail;
	$maxsmail     = 0;
	$inposttemp   = &doemoticons("$inposttemp");
	$maxsmail     = $maxsmailtemp;
	$inposttemp =~ s/\<img\s*(.*?)\s*\>//isg;
	$inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)//isg;
	$inposttemp =~ s/( )+$//isg;
	$inposttemp =~ s/^( )+//isg;
	$inposttemp =~ s/<(.|\n)+?>//g;
	$inposttemp =~ s/\[.+?\]//g;
	$inposttemp =~ s/[\a\f\n\e\0\r\t\n]//g;

        $inposttemp = &lbhz($inposttemp,$maxsavepost);
        $file = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
        &winunlock($file);
	$listall = @listall;

    if ($listall >= 200) {
        &winlock($file);
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        foreach (@listall) {
            ($listone,$noneed) = split(/\t/,$_);
	    next if ($listone !~ /^[0-9]+$/);
            if ($listone ne $intopic) {
        	print LIST "$_";
            }
            else {
	        print LIST "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t\n";
	    }
        }
        close (LIST);
        }
        &winunlock($file);
    }
    else {
        rebuildLIST(-Forum=>"$inforum");
    }


            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>主题解锁成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$forumsprog?forum=$inforum">
            ~;
            } # end if clear to edit

            else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="unlock">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题解锁]</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end unlockthread
sub deletepost {


       my $p1=$postno-1;


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
       if (($sticky eq "on")&&($p1>0))
        {
       $p1=$#threads-$postno+2;
       }
       $tt=$#threads;




 #   &error("$p1 and $tt and $inpostno");


    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    if (-e $filetoopen) {
       &winlock($filetoopen) if ($OS_USED eq "Nt");
       open(FILE, "$filetoopen") or &error("删除&这个主题不存在！");
       flock(FILE, 1) if ($OS_USED eq "Unix");
       @allthreads = <FILE>;
       close(FILE);
       &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }
    else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("删除&这个主题不存在！"); }

    $posttodelete = $inpostno;
    $posttodelete--;
if ($sticky eq "on") {
$threadscount=@allthreads;
$posttodelete =$threadscount - $posttodelete if ($posttodelete ne 0);
}
    $postcountcheck = 0;
    $totalposts = @allthreads;

#    &getmember("$inmembername");
    &moderator;
    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }

    $linetemp=$allthreads[$posttodelete];
    ($startedby, my $no, $no, $no, $no ,$no, $no, $no, $no, $no) = split(/\t/,$linetemp);

    if ($arrowuserdel eq "on") {
        if ((lc($inmembername) eq lc($startedby)) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    }

    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

        if ($cleartoedit eq "no" && $checked eq "yes") { &error("删除回复&您不是本论坛坛主或版主，或者您的密码错误！"); }
        if ($cleartoedit eq "yes") {

            if ($posttodelete eq "0") { &error("删除回复&这里是用来删除回复的，不能删除主题！"); }

            ### First off, lets delete the post in the thread.

	if ((($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"))&&($inmembername ne $startedby)) {
	  $nametocheck = $startedby;
	  $nametocheck =~ s/ /\_/g;
	  $nametocheck =~ tr/A-Z/a-z/;
	  my $filetoopen = "$lbdir" . "$memdir/$nametocheck.cgi";
	  $filetoopen = &stripMETA($filetoopen);
	  if (-e $filetoopen) {
	    &winlock($filetoopen);
	    open(FILE,"$filetoopen");
	    flock (FILE, 1) if ($OS_USED eq "Unix");
            my $filedata = <FILE>;
            close(FILE);
	    chomp($filedata);
	    (my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $aolname, my $icqnumber ,my $location ,my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $misc1,my  $userxz, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno,my  $addjy,my  $meili, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $useradd1, my $useradd2,my $jhmp ,my $useradd3, my $useradd4, my $useradd5, my $useradd6, my $useradd7, my $useradd8 ) = split(/\t/,$filedata);
	  if (($membername ne "")&&($password ne "")) {
	    open(FILE,">$filetoopen");
	    flock (FILE, 2) if ($OS_USED eq "Unix");
	    $lastgone=time;
	    $postdel ++;
	    if ($usertype eq "0") {
		if (($membercode eq "rz")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo")) {
       		    $mymoney=$mymoney-$delmoney;
       		    $meili=$meili-$delml;
   		}
   	    }
   	    else {
   		$mymoney=$mymoney-$delmoney;
   		$meili=$meili-$delml;
   	    }
	    print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$misc1\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t\n";
	    close(FILE);
	  }
	  &winunlock($filetoopen);
	  }
	}

            $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $postline (@allthreads) {
                chomp $postline;
                    unless ($postcountcheck eq $posttodelete) { print FILE "$postline\n"; }
                    $postcountcheck++;
                    }
            close(FILE);
            }
            &winunlock($filetoopen) if ($OS_USED eq "Nt");

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allthreads = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");


        $totalposts = @allthreads;
        $posttograb = $totalposts;
        $posttograb--;

        ($postermembername2, $topictitle2, $postipaddress2, $showemoticons2, $showsignature2 ,$postdate2, $post2, $posticon2) = split(/\t/, $allthreads[$posttograb]);
	$inposttemp = $post2;
	$inposttemp =~ s/\[这个贴子最后由(.+?)编辑\]\n//isg;
	$inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	$inposttemp =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]//isg;
	$inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]//isg;
	$maxsmailtemp = $maxsmail;
	$maxsmail     = 0;
	$inposttemp   = &doemoticons("$inposttemp");
	$maxsmail     = $maxsmailtemp;
	$inposttemp =~ s/\<img\s*(.*?)\s*\>//isg;
	$inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)//isg;
	$inposttemp =~ s/( )+$//isg;
	$inposttemp =~ s/^( )+//isg;
	$inposttemp =~ s/<(.|\n)+?>//g;
	$inposttemp =~ s/\[.+?\]//g;
	$inposttemp =~ s/[\a\f\n\e\0\r\t\n]//g;

        $inposttemp = &lbhz($inposttemp,$maxsavepost);


        ### Now we have to adjust the post counts.

        $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @alltopics = <FILE>;
        close(FILE);
        &winunlock($filetoopen);

        $count = "0";
        foreach $line (@alltopics) { #start foreach @threads
            ($tempno, $trash) = split(/\t/, $line);
	    next if ($tempno !~ /^[0-9]+$/);
            if ($intopic eq $tempno) {
                $linetokeep = $line;
                $keepcounter = $count;
            }
        $count++;
        } # end foreach

        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $no) = split(/\t/,$linetokeep);

        $threadposts = $totalposts - 1;

        $filetomake = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($filetomake);
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $newline (@alltopics) { #start foreach @threads
        chomp($newline);
            ($tempno, $trash) = split(/\t/,$newline);
	    next if ($tempno !~ /^[0-9]+$/);
            if ($intopic eq $tempno) {
            print FILE "$topicid\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$postermembername2\t$postdate2\t$posticon\t$inposttemp\t\n";
            }
        else { print FILE "$newline\n"; }
        }
        close(FILE);
        }
        &winunlock($filetomake);
 ########################################




       my $dirtoopen2 = "$imagesdir" . "usr/$inforum";
        opendir (DIR, "$dirtoopen2");
       my @dirdata2 = readdir(DIR);
        closedir (DIR);
       my @fls = grep(/^$inforum\_$intopic\_$p1./,@dirdata2);
          foreach $file (@fls) {
                $filetoremove = "$dirtoopen2/$file";
                unlink $filetoremove;
         }


       @addtype=split(/\,/,$addtype);

       for (my $i=$p1;$i<=$tt;$i++)
       {


       	 foreach(@addtype)
       	 {
       	   if (-e "${imagesdir}usr/$inforum/$inforum\_$intopic\_$i.$_")
       	   {
       	   my $ii=$i-1;
       	   rename ("${imagesdir}usr/$inforum/$inforum\_$intopic\_$i.$_","${imagesdir}usr/$inforum/$inforum\_$intopic\_$ii.$_");
       	   }
       	 }

       }

 ######################################### delete attachment
        ### Get the new last forum poster, and post date.

        $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $linetokeep = <FILE>;
        close(FILE);
        &winunlock($filetoopen);

        chomp $linetokeep;

        ($topicid, $topictitle, $trash, $trash, $trash, $trash, $lastforumposter1, $trash, $lastforumposter, $lastforumpostdate) = split(/\t/,$linetokeep);
        chomp $forumlastposter;
        chomp $forumlastpostdate;

        ### Adjust the variables in the Forums Summary Page.

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        &winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);

        $filetomake = "$lbdir" . "data/allforums.cgi";
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
        next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    $posts--;
                    $lastforumposter = $lastforumposter1 if ($lastforumposter eq "");
                    $lastforumpostdate = "$lastforumpostdate\%\%\%$topicid\%\%\%$topictitle";
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastforumposter\t$lastforumpostdate\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetomake);

      require "$lbdir" . "data/boardstats.cgi";

      $filetomake = "$lbdir" . "data/boardstats.cgi";
      my $filetoopens = &lockfilename($filetomake);
      if (!(-e "$filetoopens.lck")) {
        $totalposts--;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
      }

       &mischeader("删除回复");

        if ($refreshurl == 1) {
	        $relocurl = "$threadprog?forum=$inforum&topic=$intopic";
	}
	else {
               	$relocurl = "$forumsprog?forum=$inforum";
        }

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>回复已删除，请务必刷新贴子页面</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$intopic">返回主题</a>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
             <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
            } # end if clear to edit

            else { &error("删除回复&您不是坛主或版主！"); }
} # end subdelete

sub editform { # start form
$filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
&winlock($filetoopen) if ($OS_USED eq "Nt");
open(FILE, "$filetoopen");
flock(FILE, 1) if ($OS_USED eq "Unix");
@threads = <FILE>;
close(FILE);
&winunlock($filetoopen) if ($OS_USED eq "Nt");
$posttoget = $inpostno;
$posttoget--;
if ($sticky eq "on") {
$threadscount=@threads;
$posttoget =$threadscount - $posttoget if ($posttoget ne 0);
}
($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, $threads[$posttoget]);
$topictitle =~ s/^＊＃！＆＊//;

$post =~ s/\<p\>/\n\n/ig;
$post =~ s/\<br\>/\n/ig;
#&getforum("$inforum");
#&getmember("$inmembername");
$tempaccess = "forumsallowed". "$inforum";
$testentry = $query->cookie("$tempaccess");

if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
            else { $allowed  = "no"; }
if (($privateforum eq "yes") && ($allowed ne "yes")) {
  &error("发表&对不起，您不允许在此论坛发表！");
}

&error("发表&对不起，不允许编辑投票贴子！") if (($posticon =~ m/<BR>/i)&&($posttoget eq 0));

$rawpost = $post;
if ($previewfirst eq "yes") {
    $rawpost = $inpost;
    $rawpost =~ s/\<p\>/\n\n/ig;
    $rawpost =~ s/\<br\>/\n/ig;
       &preview;
    }
    else {
        &mischeader("编辑贴子");
        }
    $helpurl = &helpfiles("阅读标记");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/help_b.gif" border=0></a>~;
if ($emoticons eq "on") {
    $emoticonslink = qq~<a href="javascript:openScript('$miscprog?action=showsmilies',300,350)">允许<B>使用</B>表情字符转换</a>~;
    $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>您是否希望<b>使用</b>表情字符转换在您的文章中？<br>~;
    }
    if ($htmlstate eq "on") { $htmlstates = "可用"; } else { $htmlstates = "不可用"; }
    if ($idmbcodestate eq "on") { $idmbcodestates = "可用"; } else { $idmbcodestates = "不可用"; }
    if ($arrawpostflash eq "on") { $postflashstates = "允许";} else {$postflashstates = "禁止";}

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
      &whosonline("$inmembername\t$forumname\tnone\t编辑<a href=\"$threadprog?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t") if ($privateforum ne "yes");
      &whosonline("$inmembername\t$forumname(密)\tnone\t编辑保密贴子\t") if ($privateforum eq "yes");
    }

	$emoticonsurl = qq~$imagesurl/emot~;
$output .= qq~ 
<script language="javascript"> 
function smilie(smilietext) { 
document.FORM.inpost.value=document.FORM.inpost.value+' :'+smilietext+': '; }
</script>
~;
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $rawpost =~ s/$bad/$good/isg;
                $topictitle =~ s/$bad/$good/isg;
                }
            }

if ($inpostno eq "1") {
$topictitle =~s/ \(无内容\)$//;
$topictitlehtml = qq~
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>贴子主题</b></font></td>
<td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="newtopictitle" value="$topictitle">　不得超过 40 个汉字</td>
~;
$topictitlehtml1="&nbsp;";
}
else {
 undef $topictitlehtml;
 $topictitlehtml1 = "<b>* 贴子主题</b>： $topictitle";
}
$output .= qq~
<form action="$thisprog" method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name="action" value="processedit">
<input type=hidden name="postno" value="$inpostno">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=4 cellspacing=1 border=0 width=100%>
<tr>
<td bgcolor=$titlecolor colspan=2><font color=$titlefontcolor>$topictitlehtml1</td>
</tr>
$topictitlehtml
<tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>用户名</b></font></td>
<td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"> &nbsp; <font color=$fontcolormisc><a href="$registerprog">您没有注册？</a></font></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>密　码</b></font></td>
<td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td>
</tr>
<tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>当前心情</b><BR><li>将放在贴子的前面<BR></font></td>
<td bgcolor=$miscbackone valign=top>
~;

    open (FILE, "${lbdir}data/lbpost.cgi");
     my @posticondata = <FILE>;
     close (FILE);
     chomp @posticondata;

    $tempiconnum=1;
    $posticon =~ s/[\a\f\n\e\0\r\t]//isg;
    if ($posticon ne "") {
        $tempoutput .= qq~<input type=radio value="$posticon" name="posticon" checked><img src="$imagesurl/posticons/$posticon" $defaultsmilewidth $defaultsmileheight border=0>&nbsp;~;
        $tempiconnum++;
    }
    foreach $picture (@posticondata) {
       if ($tempiconnum > 12) {
    	   $tempiconnum = 1;
    	   $tempoutput .= qq~<BR>~;
       }
       if ($picture ne $posticon) {
          $tempoutput .= qq~<input type=radio value="$picture" name="posticon"><img src="$imagesurl/posticons/$picture" $defaultsmilewidth $defaultsmileheight border=0>&nbsp;~;
          $tempiconnum ++;
       }
    } #endforeach
   $rawpost =~ s/\[这个贴子最后由(.+?)编辑\]\n//isg;
$output .= qq~
$tempoutput
</td>
</tr>
~;

        my $p1=$inpostno-1;
        $dirtoopen2 = "$imagesdir" . "usr/$inforum";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = grep(/^$inforum\_/,@dirdata2);

  if (($sticky eq "on")&&($p1!=0))
      {
        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
      if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @threads1 = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
      }
      else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("打开主题&这个主题不存在！可能已经被删除！"); }
        $p1=$#threads1-$inpostno+2;
      }


        if ($p1>0)
            { @files1 = grep(/^$inforum\_$intopic\_$p1\./,@files);}
        else
            { @files1 = grep(/^$inforum\_$intopic\./,@files);}
        $files1=@files1;

        if ( $files1 > 0 )
        {
	$delimg="<BR><input type=checkbox name='delimg' value='no'>删除原图像或附件</input>";
        }

if ((($arrowupload ne "off")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"))) {
$output .= qq~
<tr><td bgcolor=$miscbacktwo>
<b>上传附件或图片</b>(最大 $maxupload KB):
</td>
<td bgcolor=$miscbacktwo> <input type="file" size=30 name="addme">　　$addtypedisp$delimg
</td>
</tr>
~;
}

if ($arrowuserdel eq "on") {
    $arrowuserdelsmg = "坛主、版主和发贴者可以";
}
else {
   $arrowuserdelsmg= "只有坛主或版主才可以";
}
$output .= qq~
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>内容</b><p>
在此论坛中：<li>HTML 标签　: <b>$htmlstates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LB5000 标签</a>: <b>$idmbcodestates</b><li>贴图标签　 : <b>$postpicstates</b><li>Flash 标签 : <b>$postflashstates</b><li>音乐标签　 : <b>$postsoundstates</b><li>文字大小　 : <b>$postfontsizestates</b><li>$emoticonslink</font></td>
<td bgcolor=$miscbackone>
$insidejs
          <TEXTAREA cols=80 name=inpost rows=12 wrap="soft" onkeydown=ctlent()>$rawpost</TEXTAREA><br>
&nbsp;　模式:
<input type="radio" name="mode" value="help" onClick="thelp(1)">　帮助　
<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">　完全　
<input type="radio" name="mode" value="basic"  onClick="thelp(0)">　基本　
</td></tr>
		<tr>
                <td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>点击表情图即可在贴子中加入相应的表情(每个表情最多同时显示 $maxsmail 次)</B></font><br>&nbsp;
                ~;

    		 open (FILE, "${lbdir}data/lbemot.cgi");
		my @emoticondata = <FILE>;
		close (FILE);
		chomp @emoticondata;
        	foreach $picture (@emoticondata) {
    			$smileyname = $picture;
    			$smileyname =~ s/\.gif$//g;
       			$output .= qq~
                	<a href="javascript:smilie('$smileyname');"><img src="$emoticonsurl/$picture" border=0></a>
                	~;
                } #endforeach
    		$output .= qq~
    		</td>
                </tr>
<tr>
<td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>选项</b><p>$helpurl
</font></td>
<td bgcolor=$miscbacktwo><input type=checkbox name="inshowsignature" value="yes" checked>
<font color=$fontcolormisc>是否显示您的签名？<br>
$emoticonsbutton
&nbsp;<b>发表之前是否预览？</b><input name="previewfirst" type="radio" value="yes"> 是　 <input name="previewfirst" type="radio" value="no" checked> 否
</font></td>
</tr>
<tr>
<td bgcolor=$miscbackone>
<font color=$fontcolormisc><b>管理员选项</b></td>
<td bgcolor=$miscbackone>
<font color=$fontcolormisc>
<input type=checkbox name="deletepost" value="yes">删除此回复？($arrowuserdelsmg)
</font></td></tr>
<tr>
<td bgcolor=$miscbackone colspan=2 align=center>
<input type=Submit value="发 表" name=Submit>　　<input type="reset" name="Clear" value="清 除">
</td></form></tr></table></tr></td></table>
~;
} # end edit form

sub processedit {
           $inpostno1=$inpostno;
            $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
           if (-e $filetoopen) {
    	       &winlock($filetoopen) if ($OS_USED eq "Nt");
               open(FILE, "$filetoopen") or &error("编辑&这个主题不存在！");
               flock(FILE, 1) if ($OS_USED eq "Unix");
               @allthreads = <FILE>;
               close(FILE);
               &winunlock($filetoopen) if ($OS_USED eq "Nt");
           }
 	   else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("编辑&这个主题不存在！"); }

            if (($inpostno>1)&&($sticky eq "on"))
           {
            $inpostno=$#allthreads-$inpostno+3;
           }

            $delimg=$query->param('delimg');
            $posttoget = $inpostno;
            $posttoget--;
            $postcountcheck = 0;




            ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, $allthreads[$posttoget]);
#            &getmember("$inmembername");
            &moderator;
#            &getforum("$inforum");
            $tempaccess = "forumsallowed". "$inforum";
            $testentry = $query->cookie("$tempaccess");

            if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
            else { $allowed  = "no"; }

            if (($privateforum eq "yes") && ($allowed ne "yes")) {
                &error("发表&对不起，您不允许在此论坛发表！");
            }

	    &error("发表&对不起，不允许编辑投票贴子！") if (($posticon =~ m/<BR>/i)&&($posttoget eq 0));

            $cleartoedit = "no";
            if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
            if(($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes";}
            if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
            if ((lc($inmembername) eq lc($postermembername)) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
        unless ($cleartoedit eq "yes") { $cleartoedit eq "no"; }

        if ($cleartoedit eq "yes") {

            $editpostdate = time;
            $editpostdate = $editpostdate + ($timezone*3600) + ($timedifferencevalue*3600);
            $editpostdate = &dateformat("$editpostdate");
            $inpost =~ s/\t//g;
            $inpost =~ s/\r//g;
            $inpost =~ s/  / /g;
            $inpost =~ s/\n\n/\<p\>/g;
            $inpost =~ s/\n/\<br\>/g;
            if ($emote) {
 	    @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		($toemote, $beemote) = split(/=/,$_);
		chop $beemote;
		$beemote =~ s/对象/〖$inmembername〗/isg;
		$inpost =~ s/$toemote/$beemote/isg;
	    }
	}
            # Open the bad word filter
	    
	    $newtopictitle  = "＊＃！＆＊$newtopictitle";

            if ($badwords) {
              @pairs = split(/\&/,$badwords);
              foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $inpost =~ s/$bad/$good/isg;
                $newtopictitle =~ s/$bad/$good/isg;
              }
             }
             if (($newtopictitle eq "")&&($inpostno eq 1)) {
                &error("发表&对不起，贴子主题不能为空！");
             }
             if ($inpostno eq 1) {
	         $newtopictitle = "$newtopictitle (无内容)" if (($inpost eq "")&&($addme eq ""));
		 if ($topictitle eq $newtopictitle) {
		     $topictitlecomp = 1;
		 }
	         else {
	             $topictitle = $newtopictitle;
		     $topictitlecomp = 0;
	         }
             }

             $inpost = qq~[这个贴子最后由$inmembername在 $editpostdate 编辑]<br><br>$inpost~;

	$end_q_tag = 0;
	$srt_q_tag = 0;
	$end_q_tag++ while $inpost =~ m#\[/QUOTE\]#ig;
	$srt_q_tag++ while $inpost =~ m#\[QUOTE\]#ig;
	if ($end_q_tag ne $srt_q_tag) { &error("内容校验出错&你输入了 $srt_q_tag 个 [QUOTE] 标签和 $end_q_tag 个 [/QUOTE] 标签，数目不匹配！"); }

           $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $postline (@allthreads) {
                    chomp $postline;
                    if ($postcountcheck eq $posttoget) {
                        print FILE "$postermembername\t$topictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$postdate\t$inpost\t$inposticon\t\n";
                    }
                    else {
                    	(my $postermembertemp, my $topictitletemp, my @endall) = split(/\t/,$postline);
                        print FILE "$postermembertemp\t$topictitle\t";
                    	foreach (@endall) {
                    	    print FILE "$_\t";
                    	}
                    	print FILE "\n";
                    }
                    $postcountcheck++;
                }
            close(FILE);
            }
            &winunlock($filetoopen) if ($OS_USED eq "Nt");
        
        $topictitle =~ s/^＊＃！＆＊//;

	if (($inpostno eq 1)&&($topictitlecomp eq 0)) {
            $filetoopen = "$lbdir" . "forum$inforum/$intopic.pl";
            &winlock($filetoopen) if ($OS_USED eq "Nt");
	    open(FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
	    my $topicall = <FILE>;
            close(FILE);
	    (my $topicidtemp, my $topictitletemp, my @endall) = split (/\t/, $topicall);

            if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "$intopic\t$topictitle\t";
            foreach (@endall) {
               print FILE "$_\t";
            }
            close(FILE);
            }
            &winunlock($filetoopen) if ($OS_USED eq "Nt");

	    $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
            &winlock($filetoopen);
            open(FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @allthreads = <FILE>;
            close(FILE);

            if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            foreach (@allthreads) {
	      chomp $_;
	      ($tempno, my $nono) = split (/\t/,$_);
    	      next if ($tempno !~ /^[0-9]+$/);
              if ($tempno ne $intopic) {
                print FILE "$_\n"
              }
              else {
                print FILE "$intopic\t$topictitle\t";
                foreach (@endall) {
		    print FILE "$_\t";
                }
                print FILE "\n"
              }
            }
            close(FILE);
            }
            &winunlock($filetoopen);

	    $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
	    &winlock($filetomakeopen) if ($OS_USED eq "Nt");
	    open(FILE, "$filetomakeopen");
	    flock (FILE, 1) if ($OS_USED eq "Unix");
	    @recentposts=<FILE>;
	    close(FILE);

	    if (open (FILE, ">$filetomakeopen")) {
	    flock (FILE, 2) if ($OS_USED eq "Unix");
            foreach (@recentposts) {
	      chomp $_;
	      ($tempno1, $tempno2, $no, @endall) = split (/\t/,$_);
    	      next if (($tempno1 !~ /^[0-9]+$/)||($tempno2 !~ /^[0-9]+$/));

              if (($tempno1 eq $inforum)&&($tempno2 eq $intopic)) {
                print FILE "$inforum\t$intopic\t$topictitle\t";
                foreach (@endall) {
		    print FILE "$_\t";
                }
                print FILE "\n"
              }
              else {
                print FILE "$_\n"
              }
            }
	    close(FILE);
	    }
	    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
	}


            &mischeader("编辑贴子");

        if ($refreshurl == 1) {
	        $relocurl = "$threadprog?forum=$inforum&topic=$intopic";
	}
	else {
               	$relocurl = "$forumsprog?forum=$inforum";
        }

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>编辑成功</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            具体情况：
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$intopic">返回主题</a>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;

            } # end if clear to edit

            else { &error("编辑贴子&您不是原作者，或者用户名、密码错误！"); }

   #######################################################

       $p1=$inpostno-1;


        $dirtoopen2 = "$imagesdir" . "usr/$inforum";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = grep(/^$inforum\_/,@dirdata2);


        if ($p1>0)
            { @files1 = grep(/^$inforum\_$intopic\_$p1\./,@files);}
        else
            { @files1 = grep(/^$inforum\_$intopic\./,@files);}

        foreach (@files1)
        {
        $oldname=$_;
        }

        if ($addme ne "")
        {
        unlink ("$imagesdir/usr/$inforum/$oldname");
        }
        elsif ($delimg ne "")
        {
        unlink ("$imagesdir/usr/$inforum/$oldname");
        	}

       	my $filesize=0;
	if (($addme)&&(($arrowupload ne "off")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")))
	{


	 my $up_filename =$query->uploadInfo($addme);
	    my ($up_name,$up_ext) = split(/\./,$up_filename);
	        $up_ext = lc($up_ext);

	    my $checkadd=0;
            for (split(/\,\s*/,$addtype)){
                $checkadd=1,last if ($up_ext eq lc($_));
            }

           &error("上传出错&为了安全，不支持你所上传的附件，请重新选择！") if ($up_ext eq "exe"||$up_ext eq "com"||$up_ext eq "pl"||$up_ext eq "cgi"||$up_ext eq "asp"||$up_ext eq "php"||$up_ext eq "php3"||$up_ext eq "phtml"||$up_ext eq "jsp"||$up_ext eq "cfml"||$up_ext eq "dll");
	   &error("上传出错&不支持你所上传的附件或者图片，请重新选择！") if ($checkadd==0);
	   my $buffer;

 	    if ($p1==0)
 	    {
 	    	open (FILE,">$imagesdir/usr/$forum/$forum\_$topic.$up_ext")
 	    }
 	    else
 	    {
 	    	my $replynum=$postno-1;
 	        open (FILE,">$imagesdir/usr/$forum/$forum\_$topic\_$p1.$up_ext");
 	    }
		binmode (FILE);
		while ($buffer=$query->readUploadFile($addme,4096))
		{
		$filesize=$filesize+4;
		print FILE $buffer;
	        }
	    close (FILE);
	}

	if ($filesize>$maxupload) {
                if ($postno==1)
 	    {
 	    	unlink ("$imagesdir/usr/$forum/$forum\_$topic.$up_ext")
 	    }
 	    else
 	    {
 	    	my $replynum=$postno-1;
 	        unlink ("$imagesdir/usr/$forum/$forum\_$topic\_$replynum.$up_ext");
 	    }

 		&error("上传出错&上传文件大小超过$maxupload，请重新选择！ ");
	}



################################################################


} # end routine

sub preview {
    $postbackcolor = "$postcolorone";
    $postfontcolor = "$postfontcolorone";
    $inpost =~ s/&lt\;br&gt\;&lt\;br&gt\;//g;
    $post = $inpost;
    $post =~ s/\n\n/\<p\>/g;
    $post =~ s/\n/\<br\>/g;
    if ($emote) {
 	    @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		($toemote, $beemote) = split(/=/,$_);
		chop $beemote;
		$beemote =~ s/对象/〖$inmembername〗/isg;
		$post =~ s/$toemote/$beemote/isg;
	    }
	}

    $post = &lbcode("$post");

    if ($emoticons eq "on") {
           $post = &doemoticons("$post");
	   $post = &smilecode("$post");
    }
    &mischeader("编辑预览");
    $output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
        <tr><td>
        <table cellpadding=4 cellspacing=1 border=0 width=100%>
        <tr>
            <td bgcolor=$titlecolor colspan=3 width=100%><font color=$titlefontcolor>预览</td>
        </tr>
        <tr>
            <td bgcolor="$postbackcolor" rowspan=3 valign="top" width=20%><font face=$posternamefont color=$posternamecolor>
            <b>$inmembername</b></font></td>
            <td bgcolor="$postbackcolor" colspan=2><font color=$postfontcolor><b>预览</b> </td></tr>
        <tr>
            <td colspan=2 bgcolor="$postbackcolor"><font color=$postfontcolor>$post</td></tr></table></td>
            </tr></table>
        <p>
    ~;
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
