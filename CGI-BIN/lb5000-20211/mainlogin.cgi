#!/usr/bin/perl
#############################################################
#  ����: 1.�Կ�����ʾ��¼��, 2.���Ե�½����ʾ��ӭ��Ϣ,
#        3.�Խ�IP����ʾ��ֹ������̳��Ϣ,
#        4.�Էǽ�IP�߼�¼����̳�ķ���ͳ���У���Ŀǰ��������ʾΪ�����ҳ
#
#  ˵��: �����ļ����Ƶ�leoboard.cgiͬĿ¼��,
#        ����ҳ���ϴ���:
#        <SCRIPT type="text/javascript" language="javascript" src="��̳url��ַ/mainlogin.cgi"></SCRIPT>
#
#############################################################
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

$|++;                        # Unbuffer the output
###################################################
$thisprog = "mainlogin.cgi";
&myipbanned; #��ɱһЩ ip
$query = new LBCGI;

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
    $inmembername = "����";
}
else {
	&getmember("$inmembername");
	$inmembername = "����" if ($userregistered eq "no");
}
my $filetoopen2 = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopen2.lck")) {
    &whosonline("$inmembername\t��ҳ\tnone\t�����ҳ\t");
}

if ($inmembername eq "����") {
$str = qq~<FORM name=login action="$boardurl/loginout.cgi" method=post><INPUT type=hidden value=login name=action><INPUT type=hidden name=forum><BR>�û���<INPUT size=10 name=inmembername><BR>���룺<INPUT type=password size=10 name=inpassword><BR>Cookie <SELECT name=CookieDate><OPTION value="-1d" selected>������</OPTION><OPTION value=+1d>����һ��</OPTION><OPTION value=+30d>����һ��</OPTION><OPTION value=+20y>���ñ���</OPTION></SELECT><BR><INPUT type=submit value=���� name=Submit><INPUT type=reset value=ȡ�� name=Submit></FORM><A target=_blank href="$boardurl/leoboard.cgi">�ι�</A> <A target=_blank href="$boardurl/register.cgi">ע��</A> <A target=_blank href="$boardurl/profile.cgi?action=lostpassword">��������</A><BR>~;
}
else {
$str = qq~<BR>��ӭ��<BR>$inmembername<BR><BR><A target=_blank href="$boardurl/leoboard.cgi">����</A> <A target=_blank href="$boardurl/loginout.cgi">�ص�½</A> <A href="$boardurl/loginout.cgi?action=logout">�˳�</A><BR>~;
}

print header(-charset=>gb2312);
print "document.write('$str')\n";
exit;

sub myipbanned {
	my $term_postipaddress = $ENV{'REMOTE_ADDR'};
	my $term_postipaddress1 = $ENV{'HTTP_X_FORWARDED_FOR'};
	$term_postipaddress = $term_postipaddress1 if (($term_postipaddress1 ne "")&&($term_postipaddress1 ne "unknown"));
	my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
	$term_postipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
	my $term_filetoopen ="$lbdir" . "data/ipbans.cgi";
	open(FILE,"$term_filetoopen");
	flock (FILE, 1) if ($OS_USED eq "Unix");
	my @term_bannedmembers = <FILE>;
	close(FILE);
	foreach $term_bannedip (@term_bannedmembers) {
            $term_bannedip =~ s/\r//ig;
	    chomp $term_bannedip;
	    next if ($term_bannedip eq "");
	    if ($term_postipaddress =~ /^$term_bannedip/)
	    {
			print header(-charset=>gb2312);
	    	$str="<BR>������û���ر�վ�涨����� IP ($term_postipaddress)����ֹ������̳���������ʣ�����ϵ����Ա��<BR>";
	    	print "document.write('$str')\n";
			exit;
		}
	}
}
