#!/usr/bin/perl
#########################################################################################################################
# LB5000 ��̳�������ӣ���ʾ������̳�������� ver 1.9
# ������ƣ� ɽӥ��  webmaster@cgier.com
# ��Ȩ���У� CGI �����֮��  http://www.CGIer.com  http://www.LeoBoard.com
#########################################################################################################################
# ʹ�ð취�� allnews.cgi?maxlength=���ⳤ��&display=��ʾ��ʽ&name=������ʾ&link=��ɫ����&vlink=��ɫ����&alink=��ɫ����
# ���� ������ҳ���ʵ�λ�ü����������
#      <script src="allnews.cgi?maxlength=20&display=1&name=1&link=0000ff&vlink=7f007f&alink=ff0000&mode=topic"></script>
#      �����Ϳ�������Ӧλ����ʾ������̳�������������ⳤ�� 20����ʾ����ʱ�䣬��ʾ�����ˣ�������ģʽ�鿴
#                                            (display=0 ��ʾ����ʾ����ʱ��)
#                                            (name=0 ��ʾ����ʾ������)
#                                            (mode=view ��ʾ������ģʽ�鿴)
# link�ǳ����ӵ���ɫ��vlink���ѷ��ʹ��ĳ����ӣ�alink�ǵ�ǰ������
# 
#    ������ʾ���Ӹ��������� LB5000 �еĹ���������
#
# ���в���������ʡ�ԣ�Ĭ��Ϊ�������20���ַ�����ʾʱ�䡢������ģʽ
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
$mode      = "topic" if ($mode eq "");  # Ĭ�����ӷ�ʽ�鿴
$maxlength = 20 if ($maxlength eq "");  # Ĭ�ϱ������ 20 ���ַ�
$display   = 1  if ($display eq "");    # Ĭ����ʾ����ʱ��
$name      = 1  if ($name eq "");       # Ĭ����ʾ������
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
	$topictitle =~ s/ \&nbsp;/��/g;
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
		$addmspace = qq~����<a href=$boardurl/profile.cgi?action=show&member=$membername title=����鿴$membername������ target=_blank>[$membername]</a>$addmspace~;
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
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$forumid&topic=$topicid target=_blank><ACRONYM TITLE=\"���⣺ $topictitle\"><font color=$color>$topictitletemp</font></ACRONYM></a>$addmspace$disptime<br>";
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
        $str.="��̳��û����������";
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
return substr($str,0,$maxlen-5)."��...";
}
}