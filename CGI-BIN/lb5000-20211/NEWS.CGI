#!/usr/bin/perl
###############################################################################################################################################
# LB5000 ����̳������ ver 1.9
# ������ƣ� ɽӥ��  webmaster@cgier.com
# ��Ȩ���У� CGI �����֮��  http://www.CGIer.com  http://www.LeoBoard.com
###############################################################################################################################################
# ʹ�ð취�� news.cgi?forum=����̳��&max=��ʾ��������&maxlength=���ⳤ��&display=1&link=��ɫ16���ƴ���&vlink=��ɫ16���ƴ���&alink=��ɫ16���ƴ���
# ���� ������ҳ���ʵ�λ�ü����������
#      <script src="news.cgi?forum=1&max=10&maxlength=20&link=0000ff&vlink=7f007f&alink=ff0000&mode=topic"></script>
#      �����Ϳ�������Ӧλ����ʾ1����̳������10�����ӣ����ⳤ��Ϊ 20����ʾ����ʱ�䣬������ģʽ�鿴
#                                                   (display=0 ��ʾ����ʾ����ʱ��)
#                                                   (mode=view ��ʾ������ģʽ�鿴)
# link���Զ��峬���ӵ���ɫ��vlink���Զ����ѷ��ʵĳ����ӵ���ɫ��alink���Զ��嵱ǰ�����ӵ���ɫ
#
# ���в���������ʡ�ԣ�Ĭ��Ϊ�鿴��1����̳��ǰ10�����ӣ��������20���ַ�����ʾʱ�䡢������ģʽ
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
$mode      = "topic" if ($mode eq "");  # Ĭ�����ӷ�ʽ�鿴
$number    = 1  if ($number eq "");     # Ĭ�ϲ鿴��һ����̳
$display   = 1  if ($display eq "");    # Ĭ����ʾ����ʱ��
$max	   = 10 if ($max eq "");        # Ĭ����ʾ 10 ������
$maxlength = 20 if ($maxlength eq "");  # Ĭ�ϱ������ 20 ���ַ�
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
print header(-charset=>gb2312);
if ($number !~ /^[0-9]+$/) {
   print "document.write('��ͨ&�ϴ󣬱��Һ��ҵĳ���ѽ��')\n";
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
 	$topictitle =~ s/^����������//;

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
	$topictitle =~ s/ \&nbsp;/��/g;
	$topictitle =~ s/  /��/g;
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
	     $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$number&topic=$topicid target=_blank><ACRONYM TITLE=\"���⣺ $topictitle\">$topictitletemp</ACRONYM></a>$disptime<br>";
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
        $str="-* û���ҵ���Ӧ����̳ *-";
    }
}
else {
    $str="-* ���Ǳ�����̳ *-";
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
    return "$year��$months[$mon]��$mday��";
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