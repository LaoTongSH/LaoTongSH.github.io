#!/usr/bin/perl
###################################################
# LB5000 ��ҳ��ʾ�û����� ver 1.00
# ������ƣ� ����ң  xoyoren@inhe.net
# ��Ȩ���У� CGI �����֮��  http://www.CGIer.com
###################################################
# ʹ�ð취�� showmem.cgi?show=��ʾ����
# ���� ������ҳ���ʵ�λ�ü����������
#      <script src="showmem.cgi?show=20"></script>
#      �����Ϳ�������Ӧλ����ʾ��̳���û�ǰ20��
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
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "lb.lib.pl";

&ReadParse;
$show = $in{'show'} or 20;

$|++;
$thisprog = "showmem.cgi";
print "Content-type: text/html; charset=gb2312\n\n";

$filetoopen = "$lbdir" . "data/onlinedata.cgi";
&winlock($filetoopen);
open(FILE,"<$filetoopen");
flock (FILE, 1) if ($OS_USED eq "Unix");
@onlinedata1 = <FILE>;
close(FILE);
&winunlock($filetoopen);

foreach(@onlinedata1) {
	($name,$no,$gone) = split(/\t/);
	if((time - $gone) > ($membergone * 60)) {
		$_ = '';
	} else {
		$_ = $name;
	}
	
}
@onlinedata1 = grep(/.+/,@onlinedata1);
$filetoopen = "${lbdir}data/lbmember.cgi";
&winlock($filetoopen);
open(FILE,"<$filetoopen");
flock (FILE, 1) if ($OS_USED eq "Unix");
@members = <FILE>;
close(FILE);
&winunlock($filetoopen);
@memberstats = ();
foreach(@members) {
	($membername,$title,$post,$regtime,$email) = split(/\t/);
	if(grep(/^$membername$/i,@onlinedata1)) {
		$memberstat = "<font color=#FF0000>����</font>";
	} else {
		$memberstat = "������";
	}
	push(@memberstats,"$membername\t$post\t$memberstat");
}
@memberstats = sort bypost @memberstats;

$str = "";
$str.= "<table cellspacing=0 cellpadding=0 border=0 width=100%>";
$str.= "<tr><td align=center><b>����</b></td><td align=center><b>������</b></td><td align=center><b>״̬</b></td></tr>";
$i = 0;
while(($i < $show) and ($this = $memberstats[$i])) {
	($name,$post,$status) = split(/\t/,$this);
	$str .= "<tr><td align=center><a href=$boardurl/profile.cgi?action=show&member=$name>$name</a></td><td align=center>$post</td><td align=center>$status</td></tr>";
	$i++;
}
$str .= "</table>";
print "document.write('$str')\n";
exit;

sub ReadParse {
if ($ENV{'REQUEST_METHOD'} eq "POST") {
  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
} 
else {
  $buffer = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
   ($name, $value) = split(/=/, $pair);
   $value =~ tr/+/ /;
   $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
   $value =~ s/<!--(.|\n)*-->//g;
   $value =~ s/__/--/g;
   $value =~ s/>/&gt;/g;
   $value =~ s/</&lt;/g;
   $value =~ s/\t//g;
   $in{$name} = $value;
}
}
sub bypost {
	($no,$posta,$no) = split(/\t/,$a);
	($no,$postb,$no) = split(/\t/,$b);
	$postb <=> $posta;
}