#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / 雷傲超级论坛 ver.5000
#
#  版权所有: 雷傲工作室(原蓝宝石软件工作室)
#
#  制作人  : 山鹰糊 (Shining Hu)
#            花无缺 (Ifairy Han)
#           
#  主页地址: http://www.CGIer.com/      CGI 编程者之家
#	     http://www.LeoBoard.com/   雷傲论坛支持主页
#	     http://www.leoBBS.com/     本论坛直通车
#            http://maildo.com/      大家一起邮
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
&testsystem;
use LBCGI;
$LBCGI::POST_MAX=1024*150;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/boardstats.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$thisprog = "admincenter.cgi";
$query = new LBCGI;
&ipbanned; #封杀一些 ip
$action       = $query -> param('action');
$inmembername = $query -> param('membername');
$inpassword   = $query -> param('password');
$inmembername = &unHTML("$inmembername");
$inpassword   = &unHTML("$inpassword");
if ($action eq "remove") {
    $filetounlink = "$lbdir" . "install.cgi";
    unlink "$filetounlink";
    $filetounlink = "$lbdir" . "non-cgi.tar";
    unlink "$filetounlink" if (-e $filetounlink);
    $filetounlink = "$lbdir" . "cgi-bin.tar";
    unlink "$filetounlink" if (-e $filetounlink);
}
$filetocheck = "$lbdir" . "install.cgi";
if (-e $filetocheck) {
    print "Content-type: text/html\n\n";
    print qq(
    <HTML><HEAD><TITLE>安装错误</TITLE></HEAD>
    <BODY BGCOLOR=#ffffff TEXT=#000000>
    <H1>LB5000 错误</H1><FONT COLOR=#ff0000><B>安全警告</B>：
    <br>install.cgi 文件仍然在您的服务器上，请马上利用 FTP 来将其删除！！<br> 当你删除之后，刷新本页面重新进入管理中心。</FONT></body></html>);
    exit;
}
if ($action eq "logout") {
    print "Set-Cookie: adminname=\"\"\n";
    print "Set-Cookie: adminpass=\"\"\n";
        print header(-charset=>gb2312);
        &admintitle;
                print qq(
                <tr><td bgcolor=#333333"><font face=$font color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center>
                <font face=$font color=#333333><b>您已经安全退出管理中心</b></font>
                </td></tr>
                <tr><td bgcolor=#FFFFFF>
                </td>
                </tr>
                </td></tr></table></td></tr></table>
                );
}
else {
  if  ($action eq "login") {
    print "Set-Cookie: adminname=$inmembername\n";
    print "Set-Cookie: adminpass=$inpassword\n";
  }
  else {
    $inmembername = $query->cookie('adminname');
    $inpassword   = $query->cookie('adminpass');
  }

        print header(-charset=>gb2312);
        &admintitle;
        &getmember("$inmembername");
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
		$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
		$trueipaddress = "no" if (($trueipaddress eq "")||($trueipaddress eq "unknown"));
		my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
		$trueipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
		my $thistime=time;
		$filetomake = "$lbdir" . "data/adminlogin.cgi";
        	open(FILE, ">>$filetomake");
        	print FILE "$inmembername\t密码不显示\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t登陆成功\t$thistime\t\n";
        	close(FILE);
        	undef $thistime;

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                $filetoopen = &stripMETA($filetoopen);
                open(FILE, "$filetoopen");
                @files = <FILE>;
                close(FILE);
                $check = @files;
                $check = "failed" unless ($check > 0);
                $filetoopen = "$lbdir" . "data/allforums.bak";
                $backup_file = "true" if (-e $filetoopen);
                
                $warning = qq~<br><font face=$font color=#000000>环境监测：<b>通过</b></font>~;
                if (($check eq "failed") && ($backup_file eq "true")) {
                    $warning = "<br><font face=宋体 color=#FF0000><b>警告！数据文件将已被破坏丢失！！</b><br><font> 请到<a href=checkboard.cgi>检测论坛</a>中恢复丢失的数据。</font>";
                }
                    
                $current_time = localtime;
                $inmembername =~ s/\_/ /g;
                $start_topic_ratio = $totalthreads / $totalmembers if $totalthreads;
                $start_topic_ratio = substr($start_topic_ratio, 0, 5) if $totalthreads;
                $posting_ratio     = $totalposts / $totalmembers if $totalposts;
                $posting_ratio     = substr($posting_ratio, 0, 5) if $totalposts;
		$start_topic_ratio = 0 if ($start_topic_ratio eq "");
		$posting_ratio     = 0 if ($posting_ratio eq "");
		
                $testcookie = $ENV{HTTP_COOKIE};
                if ($testcookie) {
                    $cookie_result = qq(Cookies 是否可用? == [通过]);
                }
                else {
                    $cookie_result = qq(<font color=#FF0000>Cookies 是否可用? == [失败]</font>);
                }
                $cgipath = $ENV{SCRIPT_FILENAME};
                $cgipath =~ s/$thisprog//g;
                
                print qq(
                <tr><td bgcolor=#333333"><font face=$font color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center>
                <font face=$font color=#333333><b>欢迎 $inmembername</b></font>
                </td></tr>
                <tr><td bgcolor=#FFFFFF>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=$font color=#000000>
                <center><br>
                服务器时间：<b>$current_time</b><br>
                </center>
                $warning
                
                <hr>
                <font color=#000000 face=$font>
                <p>
                <b>论坛数据摘要</b><br><br><br>
                注册用户数：$totalmembers 人
                <br>总发表主题：$totalthreads 篇
                <br>总发表回复：$totalposts 篇<br><br>
                <br>注册用户平均发表主题数：$start_topic_ratio 篇
                <br>注册用户平均回复主题数：$posting_ratio 篇
                <br><br><br>
                <br>目录路径　 ：<font color=#FF0000>$cgipath</font> == [正确]
                <br>Perl　 版本：<font color=#FF0000>$]</font> == [通过]
                <br>LBCGI.pm 版本：<font color=#FF0000>$version_needed</font> == [通过]
                <br>Cookie 测试：$cookie_result<br>
                <br><br><hr>
		    程序制作：<a href="mailto:webmaster\@cgier.com">山鹰糊</a> | <a href="mailto:info\@cgier.net">花无缺</a><BR>
		    版权所有：<a href="http://www.cgier.com/">CGI 编程者之家</a></font>
                </font>
                </td></tr></table></td></tr></table>
                );
                
	}
        else {
            &adminlogin;
            if (($inmembername ne "")&&($inpassword ne "")) {
		$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
		$trueipaddress = "no" if (($trueipaddress eq "")||($trueipaddress eq "unknown"));
		my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
		$trueipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
            	
		my $thistime=time;
		$filetomake = "$lbdir" . "data/adminlogin.cgi";
        	open(FILE, ">>$filetomake");
        	print FILE "$inmembername\t$inpassword\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t\<B\>登陆失败\<\/B\>\t$thistime\t\n";
        	close(FILE);
        	undef $thistime;
	    }
        }
       }
	print qq~</td></tr></table></body></html>~;
exit;
sub testsystem {
    if (1 == 0) {
	print "Content-type: text/html\n\n";
	print qq(
	    <HTML><HEAD><TITLE>初始化错误</TITLE></HEAD>
	    <BODY BGCOLOR=#ffffff TEXT=#000000>
	    <H1>LB5000 出错</H1>如果您看到这个错误信息，那么说明本程序没有正确执行，它仅仅是作为普通的 HTML 输出显示。您必须要询问您的服务器管理员，这个目录是否有执行 CGI 程序的权限。<p></body></html>
	);
    	exit:
    }
	my $prog = $0;
	open (PROG, $prog);
	my @prog = <PROG>;
	close (PROG);
	my $perl = $prog[0];
	$perl =~ s/^#!//;
	$perl =~ s/\s+$//;
	if ($] < 5.004) {
	    print "Content-type: text/html\n\n";
	    print qq(
	    <HTML><HEAD><TITLE>初始化错误</TITLE></HEAD>
	    <BODY BGCOLOR=#ffffff TEXT=#000000>
	    <H1>LB5000 出错</H1><FONT COLOR=#ff0000><B>Perl 版本警告</B>：您选择的 Perl 路径 - <B>$perl</B>，程序检测到它的版本为 $]，而 LB5000 必须运行在 Perl 5.004 以上版本。 <U>强烈</U> 推荐您联系服务器管理员升级 Perl 到 Perl 5.004 以上版本。</FONT></body></html>);
	    exit;  
	}
	$version_needed = $LBCGI::VERSION;
}
