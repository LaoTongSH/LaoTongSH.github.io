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
use LBCGI;
$LBCGI::POST_MAX=1024*150;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "lb.lib.pl";
$|++;

#################--- Begin the program ---###################

$thisprog = "setregrules.cgi";

$query = new LBCGI;


$rules        = $query -> param('therules');
$action       = $query -> param("action");
$action       = &cleaninput("$action");


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {
        
        $rules =~ s/\n\n/\n/ig;
        $rules =~ s/\s+/\n/ig;

        $filetomake = "$lbdir" . "data/register.dat";
        open (FILE, ">$filetomake");
        print FILE $rules;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font color=#333333><center><b>������Ϣ�Ѿ�����</b></center><br><br>
                <b>ע������������Ѿ�����.Ŀǰ��ע��������������£�</b><br><HR><ul>$rules</ul>
                <HR><br><br><br><center><a href="setregrules.cgi">�޸�ע�����������</a></center>);
                }
                else {
                    print qq(
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳��������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                    <font color=#333333><b>��Ϣ�޷�����</b><br>�ļ�����Ŀ¼����д��
                    </td></tr></table></td></tr></table>
                    );
                    }
                }
        
    else {
        &getmember("$inmembername");
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "/data/register.dat";
                open (FILE, "$filetoopen") or $rules = "����ע�����������";
                @rules = <FILE> if (!$rules);
                close (FILE);

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / ע���������������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font color=#333333><b>����ע�����������</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <br>
                <b>ע��:</b>������ʹ�� HTML ��������ʹ�� LB5000 ��ǩ��<br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=70 rows=15 wrap="virtual" name="therules">);
		                foreach (@rules) {
		                   $rules = $_;
		                   #$rules =~ s/\n//isg;
		                   print qq($rules);
		                }
		                print qq(</textarea>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit name=submit value=�ύ></form></td></tr></table></td></tr></table>
                );
                
                }
                else {
                    &adminlogin;
                    }
        }

print qq~</td></tr></table></body></html>~;
exit;
