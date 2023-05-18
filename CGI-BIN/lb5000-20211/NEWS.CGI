#!/usr/bin/perl
###############################################################################################################################################
# LB5000 分论坛新贴子 ver 1.9
# 程序编制： 山鹰糊  webmaster@cgier.com
# 版权所有： CGI 编程者之家  http://www.CGIer.com  http://www.LeoBoard.com
###############################################################################################################################################
# 使用办法： news.cgi?forum=分论坛号&max=显示几条贴子&maxlength=标题长度&display=1&link=颜色16进制代码&vlink=颜色16进制代码&alink=颜色16进制代码
# 例： 在你主页的适当位置加入以下语句
#      <script src="news.cgi?forum=1&max=10&maxlength=20&link=0000ff&vlink=7f007f&alink=ff0000&mode=topic"></script>
#      这样就可以在相应位置显示1号论坛的最新10个贴子，标题长度为 20，显示发贴时间，用帖子模式查看
#                                                   (display=0 表示不显示发贴时间)
#                                                   (mode=view 表示用新闻模式查看)
# link是自定义超链接的颜色，vlink是自定义已访问的超链接的颜色，alink是自定义当前超链接的颜色
#
# 所有参数均可以省略，默认为查看第1个论坛的前10个帖子，标题最多20个字符、显示时间、用帖子模式
###############################################################################################################################################
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

$|++;
$query = new LBCGI;
$number        = $query -> param('forum');
$number        = &stripMETA("$number");
$max	       = $query -> param('max');
$max           = &stripMETA("$max");
$display       = $query -> param('display');
$display       = &stripMETA("$display");
$maxlength     = $query -> param('maxlength');
$maxlength     = &stripMETA("$maxlength");
$link	       = $query -> param('link');
$link           = &stripMETA("$link");
$alink	       = $query -> param('alink');
$alink           = &stripMETA("$alink");
$vlink	       = $query -> param('vlink');
$vlink           = &stripMETA("$vlink");
$mode       = $query -> param('mode');
$mode       = &stripMETA("$mode");
$mode = "" if (($mode ne "topic")&&($mode ne "view"));
$mode      = "topic" if ($mode eq "");  # 默认帖子方式查看
$number    = 1  if ($number eq "");     # 默认查看第一个论坛
$display   = 1  if ($display eq "");    # 默认显示贴子时间
$max	   = 10 if ($max eq "");        # 默认显示 10 个帖子
$maxlength = 20 if ($maxlength eq "");  # 默认标题最多 20 个字符
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
print header(-charset=>gb2312);
if ($number !~ /^[0-9]+$/) {
   print "document.write('普通&老大，别乱黑我的程序呀！')\n";
   exit;
}

 if ($privateforum ne "yes") {
  $filetoopen = "$lbdir" . "data/badwords.cgi";
  if (open (FILE, "$filetoopen")) {
#	flock (FILE, 1) if ($OS_USED eq "Unix");
	$badwords = <FILE>;
	close (FILE);
	$badwords=~ s/[\r\t\n\f]//ig;
	$badwords=~ s/\./\\\./ig;
	$badwords=~ s/\(/\\\(/ig;
	$badwords=~ s/\*/\\\*/ig;
	$badwords=~ s/\)/\\\)/ig;
  }
  else { $badwords = "";}
    $filetoopen = "$lbdir" . "boarddata/list$number.cgi";
    if (-e $filetoopen) {
	&winlock($filetoopen);
        open(FILE, "$filetoopen");
	flock (FILE, 1) if ($OS_USED eq "Unix");
        @topics = <FILE>;
        close(FILE);
	&winunlock($filetoopen);
    $topics = @topics;
    
    $max=$topics if ($topics<$max);
    
    $max--;
    undef $str;

    foreach $topic (@topics[0 ... $max]) {
        chomp $topic;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon1) = split(/\t/,$topic);
        $lastpostdate = &longdate($lastpostdate + ($timedifferencevalue*3600) + ($timezone*3600));
 	$topictitle =~ s/^＊＃！＆＊//;

           if (($posticon1 eq "")||($posticon1 !~ /^[0-9]+$/)) {
		$posticon1 = int(rand(23));
		if ($posticon1 <10 ) {$posticon1="0$posticon1.gif"};
                if ($posticon1 > 9 ) {$posticon1="$posticon1.gif"};
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
	$topictitle =~ s/ \&nbsp;/　/g;
	$topictitle =~ s/  /　/g;
	if  ($display eq 1) {
	    $disptime= " $lastpostdate";
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
	     $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$number&topic=$topicid target=_blank><ACRONYM TITLE=\"主题： $topictitle\">$topictitletemp</ACRONYM></a>$disptime<br>";
	 }
	 else {
	     $topicspace=$maxlength-length($topictitle);
	     $addspace = "";
	     for ($i=0;$i<$topicspace;$i++) {
	     	$addspace = $addspace ."&nbsp;";
	     }
	     $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$number&topic=$topicid target=_blank>$topictitle</a>$addspace$disptime<br>";
	 }
        }
    }
    else {
        $str="-* 没有找到相应的论坛 *-";
    }
}
else {
    $str="-* 这是保密论坛 *-";
}
print "document.write('<body link=$link vlink=$vlink alink=$alink>$str')\n";
exit;
sub stripMETA {
    my $file = shift;
    $file =~ s/[<>\^\(\)\{\}\$\n\r"\`\&\;\|\*\?]//g;
    return $file;
}

sub winlock{
    my ($lockfile) = shift;
    my $i = 0;
    $lockfile =~ s/\\/\//isg;
    $lockfile =~ s/\://isg;
    $lockfile =~ s/\//\_/isg;
    $lockfile = "$lbdir" . "lock/$lockfile";
    while (-e "$lockfile.lck") {
	last if ($i >= 177);
	select(undef,undef,undef,0.1);
	$i++;
    }
    open (LOCKFILE, ">$lockfile.lck");
    close (LOCKFILE);
}
sub winunlock{
    my ($lockfile) = shift;
    $lockfile =~ s/\\/\//isg;
    $lockfile =~ s/\://isg;
    $lockfile =~ s/\//\_/isg;
    $lockfile = "$lbdir" . "lock/$lockfile";
#    chmod(0777,"$lockfile.lck");
    unlink("$lockfile.lck");
}
sub longdate {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    my @months = ('01','02','03','04','05','06','07','08','09','10','11','12');
    $year = $year + 1900;
    if ($mday < 10) { $mday = "0$mday"; }
    return "$year年$months[$mon]月$mday日";
}

sub lbhz{
my($str,$maxlen) = @_;
if (length($str) <= $maxlen){    return $str;    }
if (substr($str,0,$maxlen-4) =~ /^([\000-\177]|[\200-\377][\200-\377])*([\000-\177]|[\200-\377][\200-\377])$/ ){
return substr($str,0,$maxlen-4)." ...";
}else{
return substr($str,0,$maxlen-5)."　...";
}
}
