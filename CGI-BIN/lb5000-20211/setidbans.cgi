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
$thisprog = "setidbans.cgi";

$query = new LBCGI;

#$cookiepath = $query->url(-absolute=>1);
#$cookiepath =~ s/$thisprog//sg;

$boardurltemp =$boardurl;

$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/$thisprog//sg;

$wordarray     = $query -> param('wordarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {
        
        &getmember("$inmembername");
        
                if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 

        $wordarray =~ s/\s+/\n/ig;
        $wordarray =~ s/\n\n/\n/ig;

        $wordarray2display = $wordarray;
        $wordarray2display =~ s/\n/<br>/g;

        $filetomake = "$lbdir" . "data/idbans.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ID ��ֹ</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#333333><center><b>���е���Ϣ�Ѿ�����</b></center><br><br>
		<b>���Ѿ���ֹ������ ID</b><br><br>
		);
                    print qq(<b>$wordarray2display</b><br>);
                print qq(
                <br><br><br><center><a href="setidbans.cgi">�ٴ�����һЩ��ֹ�� ID</a></center>);
                }
                else {
                    print qq(
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
			<b>��ӭ���� LB5000 ��̳��������</b>
			</td></tr>
			<tr>
			<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
			<font color=#333333><b>���е���Ϣû�б���</b><br>���ļ���Ŀ¼Ϊ����д������������ 777 ��
                    	</td></tr></table></td></tr></table>
		     	);
                    }
                }
        }
        
    else {
        
        &getmember("$inmembername");
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $idfiletoopen = "$lbdir" . "data/idbans.cgi";
                open (FILE, "$idfiletoopen");
                @bannedids = <FILE>;
                close (FILE);
                
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ID ��ֹ</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>ID ��ֹ�б�</b>
		</td></tr>
		<form action="$thisprog" method="post">
		<input type=hidden name="action" value="process">
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#000000>
		<b>��ע��:</b>������ֹ��һ�� ID �Ļ�����ô��� ID �����޷���½��<br>
		<br>
		<b>˵��:</b><BR>
		             �����Ҫ��ֹһ�� ID������ֱ������ ID ��������磺 Tom<BR>
		             ÿ��дһ�� ID��ע�����س���<BR>
	                </font></td>
		</tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
		<textarea cols=60 rows=6  name="wordarray">);
		                foreach (@bannedids) {
		                   $singleid = $_;
		                   chomp $_;
		                   next if ($_ eq "");
						   #$singleid =~ s/\n\s/\n/g;
		                   print qq($singleid);
		                }
		                print qq(</textarea><BR>
		</td>
		</tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<input type=submit name=submit value=�ύ></td></form></tr></table></td></tr></table>
);
                
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
