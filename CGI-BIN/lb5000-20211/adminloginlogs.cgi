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
#            http://mail@17do.com/      ���һ����
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
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "adminloginlogs.cgi";

$query = new LBCGI;


$boardurltemp =$boardurl;

$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/$thisprog//sg;

$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {
        
        &getmember("$inmembername");
        
                if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 

                $filetoopen = "$lbdir" . "data/adminlogin.cgi";
                open (FILE, "$filetoopen");
                @baddel = <FILE>;
                close (FILE);
		$baddels = $baddel[-1];
		chomp $baddels;
                open (FILE, ">$filetoopen");
                print FILE "$baddels\n";
                close (FILE);


           print qq~
           <tr><td bgcolor=#333333"><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ɾ����־</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center>
		<font color=#333333><b>�ļ�ɾ��������־</b>
		</td></tr>
		<tr><td align=center><br><br>��ȫ��־�Ѿ�ɾ��!</td></tr>
           ~;
         
                }
        
        }
        
    else {
        
        &getmember("$inmembername");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "data/adminlogin.cgi";
                open (FILE, "$filetoopen");
                @baddel = <FILE>;
                close (FILE);
                
                print qq(
                <tr><td bgcolor=#333333" colspan=6><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ��������ȫ��־</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=6>
		<font color=#333333><b>��̳��ȫ������־</b>
		</td></tr>
		<tr><td>������</td><td>����</td><td>IP ��ַ</td><td>���� IP</td><td>������־</td><td>����ʱ��</td></tr>
		);
		foreach (@baddel){
		(my $name, my $pass, my $ip, my $proxy, my $logs,my $oldtime) = split(/\t/,$_);
    		$oldtime = $oldtime + ($timedifferencevalue*3600) + ($timezone*3600);
    		$oldtime = &dateformatshort($oldtime);
		print qq~
		<tr><td>$name</td><td>$pass</td><td>$ip</td><td>$proxy</td><td>$logs</td><td>$oldtime</td></tr>
		~;
		}
                print qq~
                <tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=6><br>
		<font color=#333333><b><a href=$thisprog?action=process>ɾ����ȫ��־</a></b>
		</td></tr>
                ~;
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
