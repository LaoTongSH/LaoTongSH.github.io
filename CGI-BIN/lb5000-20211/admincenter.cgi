#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ���������)
#
#  ������  : ɽӥ�� (Shining Hu)
#            ����ȱ (Ifairy Han)
#           
#  ��ҳ��ַ: http://www.CGIer.com/      CGI �����֮��
#	     http://www.LeoBoard.com/   �װ���̳֧����ҳ
#	     http://www.leoBBS.com/     ����ֱ̳ͨ��
#            http://maildo.com/      ���һ����
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
&ipbanned; #��ɱһЩ ip
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
    <HTML><HEAD><TITLE>��װ����</TITLE></HEAD>
    <BODY BGCOLOR=#ffffff TEXT=#000000>
    <H1>LB5000 ����</H1><FONT COLOR=#ff0000><B>��ȫ����</B>��
    <br>install.cgi �ļ���Ȼ�����ķ������ϣ����������� FTP ������ɾ������<br> ����ɾ��֮��ˢ�±�ҳ�����½���������ġ�</FONT></body></html>);
    exit;
}
if ($action eq "logout") {
    print "Set-Cookie: adminname=\"\"\n";
    print "Set-Cookie: adminpass=\"\"\n";
        print header(-charset=>gb2312);
        &admintitle;
                print qq(
                <tr><td bgcolor=#333333"><font face=$font color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center>
                <font face=$font color=#333333><b>���Ѿ���ȫ�˳���������</b></font>
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
        	print FILE "$inmembername\t���벻��ʾ\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t��½�ɹ�\t$thistime\t\n";
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
                
                $warning = qq~<br><font face=$font color=#000000>������⣺<b>ͨ��</b></font>~;
                if (($check eq "failed") && ($backup_file eq "true")) {
                    $warning = "<br><font face=���� color=#FF0000><b>���棡�����ļ����ѱ��ƻ���ʧ����</b><br><font> �뵽<a href=checkboard.cgi>�����̳</a>�лָ���ʧ�����ݡ�</font>";
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
                    $cookie_result = qq(Cookies �Ƿ����? == [ͨ��]);
                }
                else {
                    $cookie_result = qq(<font color=#FF0000>Cookies �Ƿ����? == [ʧ��]</font>);
                }
                $cgipath = $ENV{SCRIPT_FILENAME};
                $cgipath =~ s/$thisprog//g;
                
                print qq(
                <tr><td bgcolor=#333333"><font face=$font color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center>
                <font face=$font color=#333333><b>��ӭ $inmembername</b></font>
                </td></tr>
                <tr><td bgcolor=#FFFFFF>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=$font color=#000000>
                <center><br>
                ������ʱ�䣺<b>$current_time</b><br>
                </center>
                $warning
                
                <hr>
                <font color=#000000 face=$font>
                <p>
                <b>��̳����ժҪ</b><br><br><br>
                ע���û�����$totalmembers ��
                <br>�ܷ������⣺$totalthreads ƪ
                <br>�ܷ���ظ���$totalposts ƪ<br><br>
                <br>ע���û�ƽ��������������$start_topic_ratio ƪ
                <br>ע���û�ƽ���ظ���������$posting_ratio ƪ
                <br><br><br>
                <br>Ŀ¼·���� ��<font color=#FF0000>$cgipath</font> == [��ȷ]
                <br>Perl�� �汾��<font color=#FF0000>$]</font> == [ͨ��]
                <br>LBCGI.pm �汾��<font color=#FF0000>$version_needed</font> == [ͨ��]
                <br>Cookie ���ԣ�$cookie_result<br>
                <br><br><hr>
		    ����������<a href="mailto:webmaster\@cgier.com">ɽӥ��</a> | <a href="mailto:info\@cgier.net">����ȱ</a><BR>
		    ��Ȩ���У�<a href="http://www.cgier.com/">CGI �����֮��</a></font>
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
        	print FILE "$inmembername\t$inpassword\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t\<B\>��½ʧ��\<\/B\>\t$thistime\t\n";
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
	    <HTML><HEAD><TITLE>��ʼ������</TITLE></HEAD>
	    <BODY BGCOLOR=#ffffff TEXT=#000000>
	    <H1>LB5000 ����</H1>������������������Ϣ����ô˵��������û����ȷִ�У�����������Ϊ��ͨ�� HTML �����ʾ��������Ҫѯ�����ķ���������Ա�����Ŀ¼�Ƿ���ִ�� CGI �����Ȩ�ޡ�<p></body></html>
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
	    <HTML><HEAD><TITLE>��ʼ������</TITLE></HEAD>
	    <BODY BGCOLOR=#ffffff TEXT=#000000>
	    <H1>LB5000 ����</H1><FONT COLOR=#ff0000><B>Perl �汾����</B>����ѡ��� Perl ·�� - <B>$perl</B>�������⵽���İ汾Ϊ $]���� LB5000 ���������� Perl 5.004 ���ϰ汾�� <U>ǿ��</U> �Ƽ�����ϵ����������Ա���� Perl �� Perl 5.004 ���ϰ汾��</FONT></body></html>);
	    exit;  
	}
	$version_needed = $LBCGI::VERSION;
}
