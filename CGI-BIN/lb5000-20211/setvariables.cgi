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
$thisprog = "setvariables.cgi";

$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        	$theparam =~ s/"//g;
	        $theparam =~ s/'/\\\'/g;
        	$theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
        	$_ =~ s/[\n\r]//isg;
        	$theparam =~ s/[\n\r]//isg;
            $printme .= "\$" . "$_ = \'$theparam\'\;\n" if ($_ ne "");
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

        $filetomake = "$lbdir" . "data/boardinfo.cgi";

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
                    <font face=���� color=#333333><b>������Ϣû�б���</b><br>�ļ�����Ŀ¼����д<br>������� data Ŀ¼�� boardinfo.cgi �ļ������ԣ�
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / ��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>��̳��������</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                ~;
                $tempoutput1 = "<select name=\"mainonoff\">\n<option value=\"0\">��̳����\n<option value=\"1\">��̳�ر�\n</select>\n";
                $tempoutput1 =~ s/value=\"$mainonoff\"/value=\"$mainonoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳״̬</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput1</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>ά��˵��</b> (֧�� HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="line1" cols="40">$line1</textarea><BR><BR></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"regonoff\">\n<option value=\"0\">�����û�ע��\n<option value=\"1\">�������û�ע��\n</select>\n";
                $tempoutput1 =~ s/value=\"$regonoff\"/value=\"$regonoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>�Ƿ������û�ע��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput1<BR><BR></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>������ע��˵��</b> (֧�� HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="noregwhynot" cols="40">$noregwhynot</textarea><BR><BR></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boardname" value="$boardname"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boarddescription" value="$boarddescription"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳ LOGO</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boardlogos" value="$boardlogos"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳ URL ��ַ</b><br>��β��Ҫ�� "/"</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boardurl" value="$boardurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ҳ����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="homename" value="$homename"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��Ȩ��Ϣ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳״̬����ʾ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="statusbar" value="$statusbar"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ҳ��ַ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ͼƬĿ¼ URL</b><br>�ڽ�β��Ҫ�� "/images"</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="imagesurl" value="$imagesurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ͼƬ����·��</b><br>��β�� "/"</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="imagesdir" value="$imagesdir"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�������·��</b><br>��β�� "/"</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="lbdir" value="$lbdir"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emoticons\">\n<option value=\"off\">��ʹ��\n<option value=\"on\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$emoticons\"/value=\"$emoticons\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ�ñ����ַ�ת����</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"avatars\">\n<option value=\"off\">��ʹ��\n<option value=\"on\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$avatars\"/value=\"$avatars\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ�ø���ͼƬ</b><br>ʹ�ø��Ի�ͼƬ��ÿ���û���ӵ�����Լ���ɫ��ͷ��</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>����Ϣ����</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"allowusemsg\">\n<option value=\"on\">ʹ��\n<option value=\"off\">��ʹ��\n</select>";
                $tempoutput =~ s/value=\"$allowusemsg\"/value=\"$allowusemsg\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ�����̳����Ϣ���ܣ�</b><br>��������Ϣ���ܣ���ʹ�������Ļ�Ա���ڻ��๵ͨ��</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>����Ϣ�ռ�����Ϣ��������</font></b><br>�粻���ƣ�������</td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="maxmsgno" value="$maxmsgno" maxlength=3> �˹��ܶ԰�����̳����Ч</td>
                </tr>                

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ʼ�����</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emailfunctions\">\n<option value=\"off\">��ʹ��\n<option value=\"on\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$emailfunctions\"/value=\"$emailfunctions\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ���ʼ����ܣ�</b><br>�Ƽ���ʹ��</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"emailtype\">\n<option value=\"smtp_mail\">SMTP\n<option value=\"esmtp_mail\">ESMTP\n<option value=\"send_mail\">Sendmail\n<option value=\"blat_mail\">Blat\n</select>\n";
                $tempoutput =~ s/value=\"$emailtype\"/value=\"$emailtype\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ѡ��һ������ʹ�õ��ʼ�Э��</b><br>�Ƽ�ʹ�� SMTP������ͬʱ�� NT �� UNIX ��ʹ�á��� SENDMAIL ֻ���� UNIX ���ã�Blat ֻ���� NT ���á�</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�����ʼ�����λ��</b><br>�����ʹ�õĲ��� Sendmail���벻Ҫ��д</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SEND_MAIL" value="$SEND_MAIL"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>SMTP ��λ��</b><br>�����ʹ�õĲ��� SMTP���벻Ҫ��д��һ����д�� ISP �ṩ�ķ��ŷ�������ַ</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SMTP_SERVER" value="$SMTP_SERVER"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>SMTP �Ķ˿�</b><br>�����ʹ�õĲ��� SMTP���벻Ҫ��д��Ĭ��Ϊ 25</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=6 name="SMTP_PORT" value="$SMTP_PORT" maxlength=6></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ESMTP ���û���</b><br>�����ʹ�õĲ��� ESMTP���벻Ҫ��д</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SMTPUSER" value="$SMTPUSER"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ESMTP ������</b><br>�����ʹ�õĲ��� ESMTP���벻Ҫ��д</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SMTPPASS" value="$SMTPPASS"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>̳�������ʼ�ʹ�õ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adminemail_in" value="$adminemail_in"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>̳�������ʼ�ʹ�õ�����</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adminemail_out" value="$adminemail_out"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"passwordverification\">\n<option value=\"no\">��\n<option value=\"yes\">��\n</select>\n";
                $tempoutput =~ s/value=\"$passwordverification\"/value=\"$passwordverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ����ʼ�֪ͨ�û����룿</b><br>���鲻ʹ�á���Ҫʹ�ã���ȷ����������ġ��Ƿ�ʹ���ʼ����ܣ���������֤�㷢���ʼ���û������ġ�</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"adminverification\">\n<option value=\"no\">��\n<option value=\"yes\">��\n</select>\n";
                $tempoutput =~ s/value=\"$adminverification\"/value=\"$adminverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>���û�ע�ᣬ�Ƿ�������Ա��֤��</b><br>���鲻ʹ�á���Ҫʹ�ã�1,��ȷ����������ġ��Ƿ�ʹ���ʼ����ܣ���������֤�㷢���ʼ���û������ġ�2,ȷ���Ѿ���������ʼ�֪ͨ�û�����!</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"newusernotify\">\n<option value=\"no\">��\n<option value=\"yes\">��\n</select>\n";
                $tempoutput =~ s/value=\"$newusernotify\"/value=\"$newusernotify\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�����û�ע���Ƿ����ʼ�֪ͨ����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"oneaccountperemail\">\n<option value=\"no\">��\n<option value=\"yes\">��\n</select>\n";
                $tempoutput =~ s/value=\"$oneaccountperemail\"/value=\"$oneaccountperemail\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>һ�� Email ֻ��ע��һ���˺ţ�</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~; 

               $tempoutput = "<select name=\"usertype\">\n<option value=\"1\">һ���û�\n<option value=\"0\">��֤�û�\n</select>\n"; 
               $tempoutput =~ s/value=\"$usertype\"/value=\"$usertype\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=���� color=#333333><b>Ĭ���û�����</b><br>�趨Ĭ���û������͡����ѡ����֤�û�����ôֻ����֤�û������������Ż��ۼӣ����ѡ��һ���û�����ô���е�ע���û������ۼӡ�</font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>���ѡ��</b>
                </font></td>
                </tr>
                    
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="adscript" cols="40">$adscript</textarea>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳβ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="adfoot" rows="5" cols="40">$adfoot</textarea><BR><BR>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useimagead\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimagead\"/value=\"$useimagead\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=���� color=#333333><b>�Ƿ�ʹ����̳��ҳ�������</b></font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�������ͼƬ URL</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�����������Ŀ����ַ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adimagelink" value="$adimagelink"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�������ͼƬ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="adimagewidth" value="$adimagewidth" maxlength=3>&nbsp;����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�������ͼƬ�߶�</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="adimageheight" value="$adimageheight" maxlength=3>&nbsp;����</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum\"/value=\"$useimageadforum\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=���� color=#333333><b>����̳�Ƿ�ʹ�ô˸������</b><BR>�������̳���Զ���ĸ�����棬<BR>��ô��ѡ����Ч</font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput<BR><BR></td> 
               </tr>
		~;
               
               $tempoutput = "<select name=\"useimagead1\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimagead1\"/value=\"$useimagead1\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=���� color=#333333><b>�Ƿ�ʹ����̳��ҳ���¹̶����</b></font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���¹̶����ͼƬ URL</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adimage1" value="$adimage1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���¹̶��������Ŀ����ַ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adimagelink1" value="$adimagelink1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���¹̶����ͼƬ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="adimagewidth1" value="$adimagewidth1" maxlength=3>&nbsp;����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���¹̶����ͼƬ�߶�</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="adimageheight1" value="$adimageheight1" maxlength=3>&nbsp;����</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum1\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum1\"/value=\"$useimageadforum1\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=���� color=#333333><b>����̳�Ƿ�ʹ�ô����¹̶����</b><BR>�������̳���Զ�������¹̶���棬<BR>��ô��ѡ����Ч</font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>����ѡ��</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>֧���ϴ��ĸ�������</b><br>��,�ָ�</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="addtype" value="$addtype"></td>
                </tr>
                
                ~;
                $tempoutput = "<select name=\"OS_USED\">\n<option value=\"Nt\">Windows ϵ��\n<option value=\"Unix\">Unix ϵ��\n<option value=\"No\">������\n</select>\n";
                $tempoutput =~ s/value=\"$OS_USED\"/value=\"$OS_USED\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ѡ�����ϵͳƽ̨�����ļ�����</b><BR>��ǧ��Ҫѡ������㲻��ȷ������ѡ�� Windows ϵ�У���<BR>�ļ�����������Ч�ķ�ֹ�������ݶ�ʧ�����⣬����Ӱ���ٶȣ����Լ�������<br></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"floodcontrol\">\n<option value=\"off\">��\n<option value=\"on\">��\n</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ��ˮԤ�����ƣ�</b><br>ǿ���Ƽ�ʹ��</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�û����������ʱ��</b><br>��ˮԤ�����Ʋ���Ӱ�쵽̳�������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=5 name="floodcontrollimit" value="$floodcontrollimit" maxlength=4> �� (һ������ 30 ����)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ͬ IP ��ע����С���ʱ��</b><br>������Ч��ֹ��ˮע���</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=5 name="regcontrollimit" value="$regcontrollimit" maxlength=4> �� (һ������ 30 ����)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳����������������</b><br>���Կ��Ʒ���������Դʹ��</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=6 name="arrowonlinemax" value="$arrowonlinemax" maxlength=5> �� (һ���� 50 ���ң����������ƣ������� 99999)</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"timezone\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
                $tempoutput =~ s/value=\"$timezone\"/value=\"$timezone\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>������ʱ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>���ڵ�ʱ��</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="basetimes" value="$basetimes"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�����������ַ���</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="maxquotenum" value="$maxquotenum" maxlength=4> Ĭ��: 200</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�û����������٣�</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="maxweiwang" value="$maxweiwang" maxlength=3> Ĭ��: 10(����С��5)</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ڶ�����������ͬ���ӾͲ�⣿</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="maxadpost" value="$maxadpost" maxlength=3> Ĭ��: 4(����С��3)�����Ҫȡ���������� 999</td>
                </tr>
                ~;
		
		$tempoutput = "<select name=\"coolwin\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
		$tempoutput =~ s/value=\"$coolwin\"/value=\"$coolwin\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>
		<font face=���� color=#333333><b>�Ƿ�ʹ��LB5000���ĵ�������</b><br>ֻ��IE5.5֧�֣�ʹ�ö��߳����������ħװ���񣩽��ᱨ���Բ��ֵ���������Ч��</font></td>
		<td bgcolor=#FFFFFF valign=middle align=left>
		$tempoutput</td>
		</tr>
		~;
		
		$tempoutput = "<select name=\"oicqshow\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
		$tempoutput =~ s/value=\"$oicqshow\"/value=\"$oicqshow\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>
		<font face=���� color=#333333><b>�Ƿ�ʹ��OICQ������ʾ��ռ����Զ�ķ�������Դ)��</font></td>
		<td bgcolor=#FFFFFF valign=middle align=left>
		$tempoutput</td>
		</tr>
		~;

		$tempoutput = "<select name=\"cpudisp\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
		$tempoutput =~ s/value=\"$cpudisp\"/value=\"$cpudisp\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>
		<font face=���� color=#333333><b>�Ƿ���ʾ��̳CPUռ��ʱ��(ֻ�� Unix ��������Ч)��</font></td>
		<td bgcolor=#FFFFFF valign=middle align=left>
		$tempoutput</td>
		</tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ʾ��̳ CPU ռ��ʱ���������ɫ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=8 maxlength=7 name="cpudispcolor" value="$cpudispcolor"> Ĭ�ϣ�#c0c0c0</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"useemote\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$useemote\"/value=\"$useemote\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ�� EMOTE ��ǩ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"announcements\">\n<option value=\"no\">��ʹ��\n<option value=\"yes\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ�ù�����̳</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"sticky\">\n<option value=\"off\">����˳���µķ������\n<option value=\"on\">�������⣬�µķ���������\n</select>\n";
                $tempoutput =~ s/value=\"$sticky\"/value=\"$sticky\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�鿴���ӻظ���ʱ�����µĻظ��ǽ��������أ����Ƿ������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"refreshurl\">\n<option value=\"0\">�Զ����ص�ǰ��̳\n<option value=\"1\">�Զ����ص�ǰ����\n</select>\n";
                $tempoutput =~ s/value=\"$refreshurl\"/value=\"$refreshurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�����ظ����Ӻ��Զ�ת�Ƶ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"defaulttopicshow\">\n<option value=>�鿴���е�����\n<option value=1>�鿴һ���ڵ�����\n<option value=2>�鿴�����ڵ�����\n<option value=7>�鿴һ�����ڵ�����\n<option value=15>�鿴������ڵ�����\n<option value=30>�鿴һ�����ڵ�����\n<option value=60>�鿴�������ڵ�����\n<option value=180>�鿴�����ڵ�����\n</select>\n";
                $tempoutput =~ s/value=\"$defaulttopicshow\"/value=\"$defaulttopicshow\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>Ĭ����ʾ������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"defaulforumcshow\"><option value=\"orderlastpostd\">�����ظ�ʱ�併��<option value=\"orderlastposta\">�����ظ�ʱ������<option value=\"orderthreadd\">�����ⷢ��ʱ�併��<option value=\"orderthreada\">�����ⷢ��ʱ������<option value=\"orderstartbyd\">�����ⷢ���˽���<option value=\"orderstartbya\">�����ⷢ��������<option value=\"orderclickd\">��������������<option value=\"orderclicka\">��������������<option value=\"orderreplyd\">������ظ�������<option value=\"orderreplya\">������ظ�������<option value=\"ordertitled\">��������⽵��<option value=\"ordertitlea\">�������������</select>\n";
                $tempoutput =~ s/value=\"$defaulforumcshow\"/value=\"$defaulforumcshow\" selected/; 
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>Ĭ����������ʽ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>       
                ~;

                $tempoutput = "<select name=\"dispboardonline\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardonline\"/value=\"$dispboardonline\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ�����ҳ��ʾ����̳��ϸ�������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"disphideboard\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$disphideboard\"/value=\"$disphideboard\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ת��̳�����Ƿ���ʾ������̳</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"dispboardsm\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardsm\"/value=\"$dispboardsm\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ�����������ʾ��̳����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"dispborn\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispborn\"/value=\"$dispborn\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ҳ�Ƿ���ʾ���������û�</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"dispprofile\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$dispprofile\"/value=\"$dispprofile\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ�������˲쿴�û�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"recordviewstat\">\n<option value=\"no\">����¼\n<option value=\"yes\">��¼\n</select>\n";
                $tempoutput =~ s/value=\"$recordviewstat\"/value=\"$recordviewstat\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�Ƿ��¼��̳����ͳ������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"openiframe\">\n<option value=\"no\">������\n<option value=\"yes\">����\n</select>\n";
                $tempoutput =~ s/value=\"$openiframe\"/value=\"$openiframe\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳�Ƿ����� Iframe ��ǩ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"showfastlogin\">\n<option value=\"top\">����\n<option value=\"bottom\">�ײ�\n<option value=\"all\">����ʾ\n<option value=\"none\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$showfastlogin\"/value=\"$showfastlogin\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��̳���ٵ�½��ʾλ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"flashavatar\">\n<option value=\"no\">��֧��\n<option value=\"yes\">֧��\n</select>\n";
                $tempoutput =~ s/value=\"$flashavatar\"/value=\"$flashavatar\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ϴ�ͷ���Ƿ�֧�� FLASH ��ʽ</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ϴ�ͷ���ļ���������ֵ(��λ��KB)</b><br>Ĭ��������� 200KB ��</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text name="maxuploadava" value="$maxuploadava" size=5 maxlength=5>����Ҫ�� KB�����鲻Ҫ���� 200</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>��̳��ҳ��������</b>(���û��������)<br>�����뱳���������ƣ���������<BR>Ӧ�ϴ��� non-cgi/midi Ŀ¼�¡�<br><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="midiaddr2" value="$midiaddr2">~;
                $midiabsaddr = "$imagesdir" . "midi/$midiaddr2";
                print qq~��<EMBED src="$imagesurl/midi/$midiaddr2" autostart="false" width=70 height=25 loop="true" align=absmiddle>~ if ((-e "$midiabsaddr")&&($midiaddr2 ne ""));
                print qq~
                </td>
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
