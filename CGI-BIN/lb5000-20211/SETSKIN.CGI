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
require "lbadmin.lib.pl";     # Require Admin func()
require "data/progs.cgi";    # Require prog names
require "data/boardinfo.cgi";# Require board info
require "data/leoskin.cgi";
require "lb.lib.pl";          # Require lbboard ()

$|++;                                      # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "setskin.cgi";


$query = new LBCGI;



	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \"$theparam\"\;\n";
            }
	}


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");

print header(-charset=>gb2312);
&admintitle;

&getmember("$inmembername");
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
             
    if ($action eq "process") {


        $printme .= "1\;\n";

        $filetomake = "$lbdir" . "data/leoskin.cgi";

        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        close(FILE);
        
         
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=����  color=#FFFFFF>
                <b>��ӭ������̳�������� / ��̳����趨</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=���� color=#333333 ><center><b>���е���Ϣ�Ѿ�����</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/1\;//g;
                print $printme;

                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }

                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=����  color=#FFFFFF>
                    <b>��ӭ���� LB5000 ��̳��������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font color=#333333><b>���е���Ϣû�б���</b><br>���ļ���Ŀ¼Ϊ����д������������ 777 ��
                    </td></tr></table></td></tr></table>
                    ~;
                    }
        
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                               print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=����  color=#FFFFFF>
                <b>��ӭ������̳�������� / ��̳����趨</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333 ><b>��̳����趨</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
            
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000 ><b><center>LB5000 ��̳����������̳����趨</center></b><br>
                <font face=���� color=#333333 >��������Ӻ�ɾ���������ĵ���̳�����������̳������
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 1 </a></b><br>��̳��� 1 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin1name" value="$skin1name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 1 URL</b><br>��̳���1������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin1url" value="$skin1url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 2 </a></b><br>��̳��� 2 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin2name" value="$skin2name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 2 URL</b><br>��̳���2������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin2url" value="$skin2url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 3 </a></b><br>��̳��� 3 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin3name" value="$skin3name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 3 URL</b><br>��̳���3������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin3url" value="$skin3url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 4 </a></b><br>��̳��� 4 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin4name" value="$skin4name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 4 URL</b><br>��̳���4������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin4url" value="$skin4url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 5 </a></b><br>��̳��� 5 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin5name" value="$skin5name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 5 URL</b><br>��̳���5������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin5url" value="$skin5url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 6 </a></b><br>��̳��� 6 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin6name" value="$skin6name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 6 URL</b><br>��̳���6������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin6url" value="$skin6url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 7 </a></b><br>��̳��� 7 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin7name" value="$skin7name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 7 URL</b><br>��̳���7������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin7url" value="$skin7url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 8 </a></b><br>��̳��� 8 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin8name" value="$skin8name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 8 URL</b><br>��̳���8������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin8url" value="$skin8url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 9 </a></b><br>��̳��� 9 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin9name" value="$skin9name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 9 URL</b><br>��̳���9������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin9url" value="$skin9url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 10 </a></b><br>��̳��� 10 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin10name" value="$skin10name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 10 URL</b><br>��̳���10������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="skin10url" value="$skin10url"></td>
                </tr>      
                               
               <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="�ύ"></form></td></tr></table></td></tr></table>
               
               ~;

                            
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;
