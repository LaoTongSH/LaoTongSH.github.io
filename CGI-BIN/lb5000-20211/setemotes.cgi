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
$thisprog = "setemotes.cgi";

$query = new LBCGI;

$wordarray     = $query -> param('wordarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {
 
    &getmember("$inmembername");
        
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
 

	$wordarray =~ s/[\f\n\r]+/\n/ig;
	$wordarray =~ s/[\r \n]+$/\n/ig;
	$wordarray =~ s/^[\r\n ]+/\n/ig;
        $wordarray =~ s/\n\n//ig;
        $wordarray =~ s/\n/\&/ig;

        @savedwordarray = split(/\&/,$wordarray);
        
        $filetomake = "$lbdir" . "data/emote.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / EMOTE �趨</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ����ɹ����档</b></center><br><br>
                <b>����EMOTE�����棡</b><br><br>
                );
                
                foreach (@savedwordarray) {
                    chomp $_;
                    ($toemote, $beemote) = split(/\=/,$_);
                    print qq(���г��� <b>$toemote</b> �ĵط����� <b>$beemote</b> �滻��<br>);
                }
                print qq(
                <br><br><br><center><a href="setemotes.cgi">�ٴ�����EMOTE�б�</a></center>);
        }
        else {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / EMOTE �趨</b>
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
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "data/emote.cgi";
                open (FILE, "$filetoopen");
                $emote = <FILE> if (!$emote);
                close (FILE);
                
                $emote =~ s/\&/\n/g;
        	$emote =~ s/\n\n/\n/ig;
        	$emote =~ s/\f\r//ig;

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / EMOTE �趨</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>EMOTE�趨</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=���� color=#000000>
                EMOTE�趨����ʵ�����������ҵ�EMOTEת��,ʹ������̳���ӷḻ���.<br>
                <br>
                <b>ʹ�÷�����</b><br>1.����һ��Ҫת����EMOTE��ת����Ķ����������м���� "=" (���ں�)��<BR>
                2.ÿһ��Ҫת����EMOTEǰ����ü���/// ���������������ʻ㡣��ת����Ķ����У������󡱽��ڷ���ʱת����Ϊ�����˵�������Ҳ���Բ��������󡱣���������ȫ�������ʾ�����������趨�Ժ�Ķ�����<BR>
                <b>ע�⣺<br>1.ÿ��ֻ��дһ����<br>
                2.����Ҫת����EMOTE����,���������ģ�Ӣ�ģ��������֣���ò�Ҫ���а��״̬�µı����ţ���������������еĴ���
                <br>3.���õ�EMOTE��Ҫ�ظ�������///hi��///hide�ǲ�������ģ���ת��ʱ///hide����ת��Ϊ///hi�Ķ�����Ȼ���ڶ������渽��de��
                ����˵������///hi=����˵������Һá�����ô///hide������ʾ������˵������Һá���de����///hi��///sohi��������ġ�</b><br><br>
                <b>���磺</b>///bug=�������һ�֣�˵���������Ǻ��棬����˭����<br>
                �����������"��������"����仰�ڲ鿴����ʱ����ʾ:<br>
                ���������졽����һ�֣�˵���������Ǻ��棬����˭����<br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=60 rows=15 wrap="virtual" name="wordarray">$emote</textarea>
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
