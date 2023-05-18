#!/usr/bin/perl
#############################################################
#  功能: 1.对客人显示登录框, 2.对以登陆者显示欢迎信息,
#        3.对禁IP者显示禁止进入论坛信息,
#        4.对非禁IP者记录到论坛的访问统计中，“目前动作”显示为浏览主页
#
#  说明: 将本文件复制到leoboard.cgi同目录下,
#        在主页加上代码:
#        <SCRIPT type="text/javascript" language="javascript" src="论坛url地址/mainlogin.cgi"></SCRIPT>
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
&myipbanned; #封杀一些 ip
$query = new LBCGI;

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if ($inmembername eq "") {
    $inmembername = "客人";
}
else {
	&getmember("$inmembername");
	$inmembername = "客人" if ($userregistered eq "no");
}
my $filetoopen2 = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopen2.lck")) {
    &whosonline("$inmembername\t主页\tnone\t浏览主页\t");
}

if ($inmembername eq "客人") {
$str = qq~<FORM name=login action="$boardurl/loginout.cgi" method=post><INPUT type=hidden value=login name=action><INPUT type=hidden name=forum><BR>用户：<INPUT size=10 name=inmembername><BR>密码：<INPUT type=password size=10 name=inpassword><BR>Cookie <SELECT name=CookieDate><OPTION value="-1d" selected>不保存</OPTION><OPTION value=+1d>保存一天</OPTION><OPTION value=+30d>保存一月</OPTION><OPTION value=+20y>永久保存</OPTION></SELECT><BR><INPUT type=submit value=进入 name=Submit><INPUT type=reset value=取消 name=Submit></FORM><A target=_blank href="$boardurl/leoboard.cgi">参观</A> <A target=_blank href="$boardurl/register.cgi">注册</A> <A target=_blank href="$boardurl/profile.cgi?action=lostpassword">忘记密码</A><BR>~;
}
else {
$str = qq~<BR>欢迎您<BR>$inmembername<BR><BR><A target=_blank href="$boardurl/leoboard.cgi">进入</A> <A target=_blank href="$boardurl/loginout.cgi">重登陆</A> <A href="$boardurl/loginout.cgi?action=logout">退出</A><BR>~;
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
	    	$str="<BR>由于你没遵守本站规定！你的 IP ($term_postipaddress)被禁止访问论坛！如有疑问，请联系管理员。<BR>";
	    	print "document.write('$str')\n";
			exit;
		}
	}
}
