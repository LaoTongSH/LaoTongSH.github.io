#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ����������)
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
require "data/cityinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setcity.cgi";

$query = new LBCGI;

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam =~ s/'//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \'$theparam\'\;\n";
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);
&admintitle;

&getmember("$inmembername");
        
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

    
    if ($action eq "process") {

        
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/cityinfo.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �����ṹ</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ��ɹ�����</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                    <b>��ӭ������̳�������� / ��������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=���� color=#333333><b>������Ϣû�б���</b><br>�ļ�����Ŀ¼����д<br>������� data Ŀ¼�� cityinfo.cgi �ļ������ԣ�
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                $moneyname ="�װ�Ԫ" if ($moneyname eq "");
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / ��������</b>
                </td></tr>
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                ���������������ҵ��ƶȣ����ڻ�û��ʲô�ô��������Ժ���������չ�Ĺ����л��õ���
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>������������</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�������Ʒ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="moneyname" value="$moneyname" maxlength=6> Ĭ�ϣ��װ�Ԫ</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�Ƽ�һ�������ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjhb" value="$addtjhb"> Ĭ�ϣ�100</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�Ƽ�һ�������ӵľ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjjy" value="$addtjjy"> Ĭ�ϣ�0</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�Ƽ�һ�������ӵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjml" value="$addtjml"> Ĭ�ϣ�10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ��һ����������ľ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="ttojy" value="$ttojy"> Ĭ�ϣ�6</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ��һ���ظ�����ľ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="rtojy" value="$rtojy"> Ĭ�ϣ�6</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ��½һ������ľ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="ltojy" value="$ltojy"> Ĭ�ϣ�2</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ɾ��һ�����Ӽ�ȥ�ľ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="deljingyan" value="$deljingyan"> Ĭ�ϣ�10</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>���û�ע�����ľ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinjingyan" value="$joinjingyan"> Ĭ�ϣ�100</td>
                </tr>  
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�η������ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addmoney" value="$addmoney"> Ĭ�ϣ�10</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�λظ����ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="replymoney" value="$replymoney"> Ĭ�ϣ�8</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�ε�½���ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="loginmoney" value="$loginmoney"> Ĭ�ϣ�15</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�α�ɾ�����Ӽ�ȥ�Ļ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="delmoney" value="$delmoney"> Ĭ�ϣ�20</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>���û�ע�����Ļ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinmoney" value="$joinmoney"> Ĭ�ϣ�1000</td>
                </tr> 
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�η������ӵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addml" value="$addml"> Ĭ�ϣ�8</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�λظ����ӵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="replyml" value="$replyml"> Ĭ�ϣ�5</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�ε�½���ӵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="loginml" value="$loginml"> Ĭ�ϣ�5</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�α�ɾ�����Ӽ�ȥ������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="delml" value="$delml"> Ĭ�ϣ�10</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>���û�ע����������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinml" value="$joinml"> Ĭ�ϣ�100</td>
                </tr>  
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
                ~;
                
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;