
sub updateuserinfo {  #利用变化量来更新用户信息
        my($nametocheck,$cposts, $creplys, $crating,$cjinyan,$cmeili,$cmoney,$cpostdel) = @_;
#	用户名，发贴数变化量，回复数变化量，威望变化量，经验变化量，魅力变化量，金钱变化量，贴子被删除数变化量

	$cposts  = 0 if ($cposts  eq "");
	$creplys = 0 if ($creplys eq "");
	$crating = 0 if ($crating eq "");
	$cjinyan = 0 if ($cjinyan eq "");
	$cmeili	 = 0 if ($cmeili  eq "");
	$cmoney	 = 0 if ($cmoney  eq "");
	$cpostdel= 0 if ($postdel eq "");

	my $nametochecktemp = $nametocheck;
	$nametocheck =~ s/ /\_/g;
	$nametocheck =~ tr/A-Z/a-z/;
	$userregistered = "";
	my $filetoopen = "$lbdir" . "$memdir/$nametocheck.cgi";
	$filetoopen = &stripMETA($filetoopen);
	if (-e $filetoopen) {
	    &winlock($filetoopen);
	    open(FILE,"$filetoopen");
	    flock (FILE, 1) if ($OS_USED eq "Unix");
            my $filedata = <FILE>;
            close(FILE);
	    chomp($filedata);
	    (my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $aolname, my $icqnumber ,my $location ,my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $userflag,my  $userxz, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno,my  $addjy,my  $meili, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $useradd1,my  $useradd2, my $jhmp,my $useradd3,my $useradd4,my $useradd5,my $useradd6, my $useradd7, my $useradd8) = split(/\t/,$filedata);

	    (my $totleposts, my $totlecreplys) = split(/\|/,$numberofposts);

	    $totleposts   += $cposts;
	    $totlecreplys += $creplys;
	    $totleposts   = 0 if($totleposts   < 0);
	    $totlecreplys = 0 if($totlecreplys < 0);
	    $numberofposts = "$totleposts|$totlecreplys";

	    $rating  += $crating;
	    $addjy   += $cjinyan;
	    $meili   += $cmeili;
	    $mymoney += $cmoney;
	    $postdel += $cpostdel;

	    $postdel = 0 if ($postdel <0 );
	    $rating = -5 if ($rating < -5);
	    $rating = $maxweiwang  if ($rating >  $maxweiwang);

	    if (($membername ne "")&&($password ne "")) {
	      if (open(FILE,">$filetoopen")) {
	        flock (FILE, 2) if ($OS_USED eq "Unix");
	        $lastgone=time;
	        print FILE "$nametochecktemp\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t\n";
	        close(FILE);
	      }
	    }
	    &winunlock($filetoopen);
	}
}
1;
