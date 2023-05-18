sub rebuildLIST {
	my %IN = (
           -Forum  => "",
           @_,
	);

	$dirtoopen = "$lbdir" . "forum$IN{-Forum}";
	opendir (DIR, "$dirtoopen");
	my @dirdata = readdir(DIR);
	closedir (DIR);

	my @entry = grep(/\.thd\.cgi$/,@dirdata);
	foreach (@entry) {
	  (my $id, my $tr) = split(/\./,$_);

	  my $file = "$lbdir" . "forum$IN{-Forum}/$id.pl";
	  open (TMP, "$file");
	  my $tmp = <TMP>;
	  close (TMP);
	  chomp $tmp;
          $tmp =~ s/[\n\r]//isg;
	  (my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $lastpostdate, my $posticon1,my $inposttemp) = split (/\t/,$tmp);
 	    $topictitle =~ s/^＊＃！＆＊//;

	    $posticon =~ s/\s//isg;
	    if ($posticon =~/<br>/i) {
      		$posticon=~s/<br>/\t/ig;
      		@temppoll = split(/\t/, $posticon);
      		$temppoll = @temppoll;
      		if ($temppoll >1) {
      		    $posticon = "<br>";
      		}
      		else {
      		    $posticon = "";
      		}
	    }

	  if (($topictitle eq "")||($startedby eq "")||($startedpostdate eq "")||($threadposts eq "")){
	    my $file1 = "$lbdir" . "forum$IN{-Forum}/$id.thd.cgi";
	    open (TMP1, "$file1");
	    my @tmp = <TMP1>;
	    close (TMP);
            my $tmp = @tmp;
	    $tmp --;
	    my $tmp1 = $tmp[-1];
            $tmp1 =~ s/[\n\r]//isg;
	    my $tmp2 = $tmp[0];
            $tmp2 =~ s/[\n\r]//isg;
	    (my $membername, $topictitle, my $postipaddress, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/,$tmp2);
	    (my $membername1, my $topictitle1, my $postipaddress1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, $posticon1) = split(/\t/,$tmp1);
 	    $topictitle =~ s/^＊＃！＆＊//;
	    chomp $posticon;
	    $membername1 = "" if ($tmp eq 0);
	    $threadviews = ($tmp+1) * 8;
	    $postdate1 = $lastpostdate if ($lastpostdate ne "");
	    $inposttemp = $post1;
	    $inposttemp =~ s/\[这个贴子最后由(.+?)编辑\]\n//ig;
	    $inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//ig;
	    $inposttemp =~ s/\[quote\](.*)\[\/quote\]//ig;
	    $inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/ig;
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

	    $posticon =~ s/\s//isg;
	    if ($posticon =~/<br>/i) {
      		$posticon=~s/<br>/\t/ig;
      		@temppoll = split(/\t/, $posticon);
      		$temppoll = @temppoll;
      		if ($temppoll >1) {
      		    $posticon1 = "<br>";
      		}
      		else {
      		    $posticon1 = "";
      		}
	    }
	    $inposttemp = &lbhz($inposttemp,$maxsavepost);
            $posticon = "<br>" if ($posticon =~/<br>/i);
	    $rr = ("$postdate1\t$id\t$topictitle\t$topicdescription\t$threadstate\t$tmp\t$threadviews\t$membername\t$postdate\t$membername1\t$posticon\t$inposttemp\t");
	  }else{
   	    $threadviews = ($tmp+1) * 8 if ($threadviews eq "");
   	    $threadviews = 9999 if ($threadviews > 9999);
            $posticon1 = "<br>" if ($posticon1 =~/<br>/i);
	    $topictitle =~ s/^＊＃！＆＊//;
	    $rr = ("$lastpostdate\t$id\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$posticon1\t$inposttemp\t");
	  }
	  if ($topictitle ne "") {push (@dat, $rr);}
        }
        @sortdat = sort({$a<=>$b}@dat); undef @dat;
        @sortdat = reverse(@sortdat);
        my $file = "$lbdir" . "boarddata/list$IN{-Forum}.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        foreach (@sortdat) {
            chomp $_;
            $_ =~ s/[\n\r]//isg;
            next if ($_ eq "");
            ($lastpostdate, $topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $posticon, $posttemp) = split (/\t/,$_);
            next if ($topicid eq "");
            next if ($topicid !~ /^[0-9]+$/);
            $threadstate = "poll" if (($posticon =~ m/<br>/i)&&($threadstate ne "poll")&&($threadstate ne "pollclosed"));
            if ($threadstate eq "") {$threadstate="open";}
	    $topictitle =~ s/^＊＃！＆＊//;
            print LIST "$topicid\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t\n" unless (!$topictitle);
            undef $posticon; undef $threadstate;
        }
        close (LIST);
        }
        &winunlock($file) if ($OS_USED eq "Nt");
}
1;
