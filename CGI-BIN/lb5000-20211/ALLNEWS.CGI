#!/usr/bin/perl
#########################################################################################################################
# LB5000 论坛新新贴子，显示整个论坛的最新贴 ver 1.9
# 程序编制： 山鹰糊  webmaster@cgier.com
# 版权所有： CGI 编程者之家  http://www.CGIer.com  http://www.LeoBoard.com
#########################################################################################################################
# 使用办法： allnews.cgi?maxlength=标题长度&display=显示方式&name=名字显示&link=颜色代码&vlink=颜色代码&alink=颜色代码
# 例： 在你主页的适当位置加入以下语句
#      <script src="allnews.cgi?maxlength=20&display=1&name=1&link=0000ff&vlink=7f007f&alink=ff0000&mode=topic"></script>
#      这样就可以在相应位置显示整个论坛的最新贴，标题长度 20，显示发贴时间，显示发贴人，用帖子模式查看
#                                            (display=0 表示不显示发贴时间)
#                                            (name=0 表示不显示发贴人)
#                                            (mode=view 表示用新闻模式查看)
# link是超链接的颜色，vlink是已访问过的超链接，alink是当前超链接
# 
#    对于显示贴子个数，请在 LB5000 中的管理区设置
#
# 所有参数均可以省略，默认为标题最多20个字符、显示时间、用帖子模式
#########################################################################################################################
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
$maxlength     = $query -> param('maxlength');
$maxlength     = &stripMETA("$maxlength");
$display       = $query -> param('display');
$display       = &stripMETA("$display");
$name       = $query -> param('name');
$name       = &stripMETA("$name");
$link       = $query -> param('link');
$link       = &stripMETA("$link");
$vlink       = $query -> param('vlink');
$vlink       = &stripMETA("$vlink");
$alink       = $query -> param('alink');
$alink       = &stripMETA("$alink");
$mode       = $query -> param('mode');
$mode       = &stripMETA("$mode");
$mode = "" if (($mode ne "topic")&&($mode ne "view"));
$mode      = "topic" if ($mode eq "");  # 默认帖子方式查看
$maxlength = 20 if ($maxlength eq "");  # 默认标题最多 20 个字符
$display   = 1  if ($display eq "");    # 默认显示贴子时间
$name      = 1  if ($name eq "");       # 默认显示发贴人
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
print header(-charset=>gb2312);
    $filetoopen = "$lbdir" . "data/recentpost.cgi";
    if (-e $filetoopen) {
        open(FILE, "$filetoopen");
	flock (FILE, 1) if ($OS_USED eq "Unix");
        @topics = <FILE>;
        close(FILE);
        $topics = @topics -1;
        $str="<span LINK=#$link VLINK=#$vlink ALINK=#$alink>";
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

        foreach $topic (@topics[0 ... $topics]) {
            chomp $topic;
           ($forumid, $topicid, $topictitle, $posttime, $posticon1, $membername) = split(/\t/,$topic);
           $posttime = dateformat($posttime + ($timedifferencevalue*3600) + ($timezone*3600));
           if (($posticon1 eq "")||($posticon1 !~ /^[0-9]+$/)) {
		$posticon1 = int(rand(23));
		if ($posticon1 <10 ) {$posticon1="0$posticon1.gif"};
                if ($posticon1 > 9 ) {$posticon1="$posticon1.gif"};
           }
           if ($badwords) {
               @pairs = split(/\&/,$badwords);
               foreach (@pairs) {
                 ($bad, $good) = split(/=/,$_);
                 chomp $good;
                 $topictitle =~ s/$bad/$good/isg;
               }
           }
	$topictitle =~ s/\'/\`/g;
        $topictitle =~ s/\&amp;/\&/g;
	$topictitle =~ s/\&quot;/\"/g;
#	$topictitle =~ s/\&lt;/</g;
#	$topictitle =~ s/\&gt;/>/g;
	$topictitle =~ s/ \&nbsp;/　/g;
	if  ($display eq 1) {
	    $disptime= " ($posttime)";
	}
	else { undef $disptime; }
	if  ($name eq 1) {
	       $memberspace=16-length($membername)-1;
	       $addmspace = "";
	       for ($i=0;$i<$memberspace;$i++) {
	     	   $addmspace = $addmspace ."&nbsp;";
		}
		$addmspace = qq~　　<a href=$boardurl/profile.cgi?action=show&member=$membername title=点击查看$membername的资料 target=_blank>[$membername]</a>$addmspace~;
	}
	else { undef $addmspace; }

 	   if (length($topictitle)>$maxlength) {
	        $topictitletemp=&lbhz("$topictitle",$maxlength); 
	        $topictitletemp =~ s/\&/\&amp;/g;
		$topictitletemp =~ s/\"/\&quot;/g;
		$topictitletemp =~ s/</\&lt;/g;
		$topictitletemp =~ s/>/\&gt;/g;
	        $topictitletemp =~ s/ /\&nbsp;/g;
  	        $topictitletemp = $topictitletemp ."&nbsp;" if (length($topictitletemp) < $maxlength);
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$forumid&topic=$topicid target=_blank><ACRONYM TITLE=\"主题： $topictitle\"><font color=$color>$topictitletemp</font></ACRONYM></a>$addmspace$disptime<br>";
	   }
	   else {
  	       $topicspace=$maxlength-length($topictitle);
	       $addspace = "";
	       for ($i=0;$i<$topicspace;$i++) {
	     	   $addspace = $addspace ."&nbsp;";
	       }
	       $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$forumid&topic=$topicid target=_blank><font color=$color>$topictitle</font></a>$addspace$addmspace$disptime<br>";
	   }
        }
    }
    else {
        $str.="论坛上没有最新贴子";
    }    

print "document.write('$str')\n";
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
sub dateformat {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    my @months = ('01','02','03','04','05','06','07','08','09','10','11','12');
    $mon = $months[$mon];
    my $ampm = "am";
    if ($hour > 11) {  $ampm = "pm"; }
    if ($hour > 12) { $hour = $hour - 12; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min = "0$min"; }
    if ($sec < 10) { $sec = "0$sec"; }
    if ($mday < 10) { $mday = "0$mday"; }
    $year = $year + 1900;
    return "$year/$mon/$mday $hour:$min$ampm";
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
