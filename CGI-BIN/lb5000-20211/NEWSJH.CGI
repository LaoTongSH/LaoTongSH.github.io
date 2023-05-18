#!/usr/bin/perl
###################################################################################################
# LB5000 ����̳����������ʾ ver 1.9
# ��Ȩ���У� CGI �����֮��  http://www.CGIer.com  http://www.LeoBoard.com
###################################################################################################
# ʹ�ð취�� newsjh.cgi?forum=����̳��&max=��ʾ��������&maxlength=���ⳤ��&display=1&mode=ģʽ
# ���� ������ҳ���ʵ�λ�ü����������
#      <script src="newsjh.cgi?forum=1&max=20&maxlength=20&mode=topic"></script>
#      �����Ϳ�������Ӧλ����ʾ1����̳����10���������ӣ����ⳤ��Ϊ 20����ʾ����ʱ�䣬������ģʽ�鿴
#                                                    (display=0 ��ʾ����ʾ����ʱ��)
#                                                    (mode=view ��ʾ������ģʽ�鿴)
#
# ���в���������ʡ�ԣ�Ĭ��Ϊ�鿴��1����̳��ǰ20���������ӣ��������20���ַ�����ʾʱ�䡢������ģʽ
###################################################################################################
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
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "lb.lib.pl";

$|++;
$query = new LBCGI;
$mode       = $query -> param('mode');
$mode       = &stripMETA("$mode");
$inforum       = $query -> param('forum');
$inforum       = &stripMETA("$inforum");
$max	       = $query -> param('max');
$max           = &stripMETA("$max");
$display       = $query -> param('display');
$display       = &stripMETA("$display");
$maxlength     = $query -> param('maxlength');
$maxlength     = &stripMETA("$maxlength");
$mode = "" if (($mode ne "topic")&&($mode ne "view"));
$mode      = "topic" if ($mode eq "");  # Ĭ�����ӷ�ʽ�鿴
$inforum   = 1  if ($inforum eq "");    # Ĭ�ϲ鿴��һ����̳
$display   = 1  if ($display eq "");    # Ĭ����ʾ����ʱ��
$max	   = 20 if ($max eq "");        # Ĭ����ʾ 10 ����������
$maxlength = 20 if ($maxlength eq "");  # Ĭ�ϱ������ 20 ���ַ�
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

print header(-charset=>gb2312);
if ($inforum !~ /^[0-9]+$/) {
   print "document.write('��ͨ&�ϴ󣬱��Һ��ҵĳ���ѽ��')\n";
   exit;
}
    &badwordfile;
    $filetoopen = "$lbdir" . "boarddata/jinghua$inforum.cgi";
    if (-e $filetoopen) {
    	&winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @ontop = <FILE>;
        close(FILE);
        &winunlock($filetoopen);
    }
    else { undef @ontop; }
    $topcount = @ontop;
    $topcount=$max if ($topcount>$max);
    
    if ($topcount > 0) {
      $i=0;
      foreach $id (@ontop) {
      	chomp $id;
	next if ((!(-e "${lbdir}forum$inforum/$id.thd.cgi"))||($id eq ""));

	my $file = "$lbdir" . "forum$inforum/$id.pl";
	open (TMP, "$file");
	(my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $lastpostdate, my $posticon1, my $inposttemp) = split (/\t/,<TMP>);
	close (TMP);
 	$topictitle =~ s/^����������//;
       
	my $file1 = "$lbdir" . "forum$inforum/$id.thd.cgi";
	if (($topictitle eq "")||($startedby eq "")||($startedpostdate eq "")){
	open (TMP1, "$file1");
	my @tmp = <TMP1>;
	close (TMP);
	my $tmp = @tmp;
	$tmp --;
	my $tmp1 = $tmp[-1];
        $tmp1 =~ s/[\n\r]//isg;
	my $tmp2 = $tmp[0];
        $tmp1 =~ s/[\n\r]//isg;
	(my $membername, $topictitle, my $postipaddress, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/,$tmp2);
	(my $membername1, my $topictitle1, my $postipaddress1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, $posticon1) = split(/\t/,$tmp1);
 	    $topictitle =~ s/^����������//;
	    chomp $posticon;
	    $membername1 = "" if ($tmp eq 0);
	    $threadviews = ($tmp+1) * 8;
	    $postdate1 = $lastpostdate if ($lastpostdate ne "");
	    $inposttemp = $post1;
	    $inposttemp =~ s/\[������������(.+?)�༭\]\n//ig;
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

	    $rr = ("$id\t$topictitle\t$topicdescription\t$threadstate\t$tmp\t$threadviews\t$membername\t$postdate\t$membername1\t$postdate1\t$posticon1\t$inposttemp\t\n");
        }else{
   	    $threadviews = ($tmp+1) * 8 if ($threadviews eq "");
   	    $threadviews = 9999 if ($threadviews > 9999);
            $posticon1 = "<br>" if ($posticon1 =~/<br>/i);
	    $topictitle =~ s/^����������//;
            $rr = ("$id\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon1\t$inposttemp\t\n");
        }
	if ($topictitle ne "") {push (@topic, $rr); $i++;}
	last if ($i >= $max);
      }
   }
   else { undef @topic; }

if (@topic) {
    foreach $topic (@topic) {
	chomp $topic;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp) = split(/\t/,$topic);
	$longdate=&longdate($startedpostdate + ($timedifferencevalue*3600) + ($timezone*3600));

           if (($posticon eq "")||($posticon !~ /^[0-9]+$/)) {
		$posticon = int(rand(23));
		if ($posticon <10 ) {$posticon="0$posticon.gif"};
                if ($posticon > 9 ) {$posticon="$posticon.gif"};
           }
        if ($badwords) {
             @pairs = split(/\&/,$badwords);
             foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chop $good;
                $topictitle =~ s/$bad/$good/isg;
                }
            }
 	$topictitle =~ s/\'/\`/g;
        $topictitle =~ s/\&amp;/\&/g;
	$topictitle =~ s/\&quot;/\"/g;
#	$topictitle =~ s/\&lt;/</g;
#	$topictitle =~ s/\&gt;/>/g;
	$topictitle =~ s/ \&nbsp;/��/g;
	$topictitle =~ s/  /��/g;
	if  ($display eq 1) {
	    $disptime= " $longdate";
	}
	else { undef $disptime; }
	if (length($topictitle)>$maxlength) {
	     $topictitletemp=&lbhz("$topictitle",$maxlength); 
             $topictitletemp =~ s/\&/\&amp;/g;
	     $topictitletemp =~ s/\"/\&quot;/g;
             $topictitletemp =~ s/</\&lt;/g;
	     $topictitletemp =~ s/>/\&gt;/g;
	     $topictitletemp =~ s/ /\&nbsp;/g;
	     $topictitletemp = $topictitletemp ."&nbsp;" if (length($topictitletemp) < $maxlength);
	     $str.=qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$inforum&topic=$topicid target=_blank><ACRONYM TITLE="���⣺ $topictitle">$topictitletemp</ACRONYM></a>��<a href=$boardurl/profile.cgi?action=show&member=$startedby target=_blank>[$startedby]</a>��$disptime<br>~;
	 }
	 else {
	     $topicspace=$maxlength-length($topictitle);
	     $addspace = "";
	     for ($i=0;$i<$topicspace;$i++) {
	     	$addspace = $addspace ."&nbsp;";
	     }
	     $str.=qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$inforum&topic=$topicid target=_blank>$topictitle</a>$addspace��<a href=$boardurl/profile.cgi?action=show&member=$startedby target=_blank>[$startedby]</a>��$disptime<br>~;
	 }
    }
}
else {
        $str="-* û����Ӧ����̳���ߴ���̳�޾������� *-";
}
print "document.write('$str')\n";
exit;