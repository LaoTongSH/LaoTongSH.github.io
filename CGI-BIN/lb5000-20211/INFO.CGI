#!/usr/bin/perl
###################################################
# LB5000 ��ҳ��ʾ��̳��Ϣ ver 1.2
# ������ƣ� ɽӥ��  webmaster@cgier.com
# ��Ȩ���У� CGI �����֮��  http://www.CGIer.com
###################################################
# ʹ�ð취�� info.cgi
# ���� ������ҳ���ʵ�λ�ü����������
#      <script src="info.cgi"></script>
#      �����Ϳ�������Ӧλ����ʾ������̳��һЩ��Ϣ
#
#   �������Ҫ��ʾ��ô��ϸ�����Լ��������������
#   ������֣�ɾ������Ҫ��ʾ���У��Ϳ����ˡ�
###################################################
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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/boardstats.cgi";

$|++;
$thisprog = "info.cgi";
print "Content-type: text/html\n\n";

my $filetoopen = "$lbdir" . "data/onlinedata.cgi";
&winlock($filetoopen);
open(FILE,"$filetoopen");
flock (FILE, 1) if ($OS_USED eq "Unix");
my @onlinedata1 = <FILE>;
close(FILE);
&winunlock($filetoopen);
$total_users = @onlinedata1;

$filetomake = "$lbdir" . "data/counter.cgi";
&winlock($filetomake);
open(FILE,"$filetomake");
flock (FILE, 1) if ($OS_USED eq "Unix");
my $count = <FILE>;
close(FILE);
&winunlock($filetomake);
($count1,$count2,$onlinemax1,$onlinemaxtime1) = split(/\t/, $count);
	
$all= $totalthreads+$totalposts;
$cleanlastregistered = $lastregisteredmember;
$cleanlastregistered =~ y/ /_/;
$cleanlastregistered =~ tr/A-Z/a-z/;
$cleanlastregistered = qq~<a href=$boardurl/$profileprog?action=show&member=$cleanlastregistered target=_blank>$lastregisteredmember</a>~;
$onlinemaxtime1 =&dateformatshort($onlinemaxtime1 + ($timezone*3600) + ($timedifferencevalue*3600));

$str = "";
$str.= "��������: $total_users<br>";
$str.= "�ܷ�����: $count1<br>";
$str.= "�ܵ����: $count2<br>";
$str.= "���߷�ֵ: $onlinemax1<br>";
$str.= "��ֵʱ��: $onlinemaxtime1<br>";
$str.= "ע���Ա: $totalmembers<br>";
$str.= "��������: $totalthreads<br>";
$str.= "�ظ�����: $totalposts<br>";
$str.= "��������: $all<br>";
$str.= "������: $cleanlastregistered<br>";
print "document.write('$str')\n";
exit;
sub dateformatshort {
    my $time = shift;
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($time);
    my @months = ('01','02','03','04','05','06','07','08','09','10','11','12');
    $mon = $months[$mon];
    if ($hour < 10) { $hour = "0$hour"; }
    if ($mday < 10) { $mday = "0$mday"; }
    if ($min < 10) { $min = "0$min"; }
    if ($sec < 10) { $sec = "0$sec"; }
    $year = $year + 1900;
    return "$year/$mon/$mday $hour:$min";
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