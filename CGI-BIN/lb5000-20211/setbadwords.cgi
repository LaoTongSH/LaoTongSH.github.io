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
$thisprog = "setbadwords.cgi";

$query = new LBCGI;

&ipbanned; #��ɱһЩ ip

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
 
 	$wordarray =~ s/[\f\n\r]+/\n/ig;
	$wordarray =~ s/[\r \n]+$/\n/ig;
	$wordarray =~ s/^[\r\n ]+/\n/ig;
        $wordarray =~ s/\n\n//g;
        $wordarray =~ s/\n/\&/g;

        @savedwordarray = split(/\&/,$wordarray);
        
        $filetomake = "$lbdir" . "data/badwords.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ����ɹ����档</b></center><br><br>
                <b>���С�������������棡</b><br><br>
                );
                
                foreach (@savedwordarray) {
                    chomp $_;
                    ($bad, $good) = split(/\=/,$_);
                    print qq(���г��� <b>$bad</b> �ĵط����� <b>$good</b> �滻��<br>);
                }
                print qq(
                <br><br><br><center><a href="setbadwords.cgi">�ٴ����ӹ��˵Ĳ�������</a></center>);
        }
        else {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>Welcome your lb board Administration Center</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>��Ϣû�б����棡</b><br>�ļ�����Ŀ¼����д��
                </td></tr></table></td></tr></table>
                );
        }
    }
    else {
        &adminlogin;
    }
        
 }
        
 else {
        
        &getmember("$inmembername");
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
                # Open the badword file

                $filetoopen = "$lbdir" . "data/badwords.cgi";
                open (FILE, "$filetoopen") or $badwords = "damn=d*amn\nhell=h*ll";
                $badwords = <FILE> if (!$badwords);
                close (FILE);
                
                $badwords =~ s/\&/\n/g;
        	$badwords =~ s/\n\n/\n/ig;
        	$badwords =~ s/\\//ig;
        	$emote =~ s/\f\r//ig;

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �����������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>�����������</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=���� color=#000000>
                ����������˿�����ֹһЩ���õ����۳�������̳�С������ѡ����˵ĵ��ʣ��͹��˺�ĵ��ʡ�<br>
                ����������������<b>��������</b>ʱ�������û��鿴������ʱ�������ᱻ��ʾ��<br>
                ����ζ�Ų�����������������Եġ���������һ���µĹ���ʱ�����е����¶��ᱻ���˽�����<br><br>
                <b>ʹ�÷�����</b>ʹ�÷�����</b>����һ��Ҫ���˵Ĵ���͹��˺�Ĵ�������м���� "=" (���ں�)��<BR><br>
                <b>ע��1��ÿ��ֻ��дһ����</b><br><br>
                <b>ע��2����������ʹ�� * ( ) ���ţ�</b><br><br>
                <b>���磺</b>fuck=f**k<br><br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=60 rows=6 wrap="virtual" name="wordarray">$badwords</textarea>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <input type=submit name=submit value="�� ��"></form></td></tr></table></td></tr></table>
                );
                
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
