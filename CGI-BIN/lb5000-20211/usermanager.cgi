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
require "lbmail.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                                   # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "usermanager.cgi";
$query = new LBCGI;

$action          = $query -> param('action');
$usertype        = $query -> param('usertype');
$action          = &unHTML("$action");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);       
&admintitle;
        
&getmember("$inmembername");
        
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / �û��������</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'search' =>    \&searchusers,
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &searchoptions; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        
sub searchoptions {

    print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
	���� <font color=red>һ���û�</font> ��Ŀ�϶࣬�뵽 <a href="$setmembersprog">�û�����/����(*)</a> ������<br><br>
        <form method=get action="usermanager.cgi">
        <input type=hidden name="action" value="search">
        <div align=center>��ѡ����Ҫ��ѯ���û�����
	<select name="usertype">
	<option value="rz" selected>��֤�û�</option>
	<option value="mo">����̳����</option>
        <option value="smo">��̳�ܰ���</option>
	<option value="ad">̳��</option>
        <option value="banned">��ֹ�û�����</option>
        <option value="masked">���δ��û�����</option>
	</select> 
        <p><input type="submit" value='ȷ��'></p></div></form>
	</td></tr>
        ~;
        }

sub searchusers {
	unless ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
        }

        if ($usertype eq ""){
	print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>û��ѡ����Ҫ�������û����</font>
                    
        </td></tr>
         ~;
         }
         else {
	print qq~
        <tr>
        <td bgcolor=#FFFFFF colspan=2><br>
         ~;

	$filetoopen = "$lbdir" . "data/lbmember.cgi";
        open(FILE,"$filetoopen");
        flock (FILE, 1) if ($OS_USED eq "Unix");
        @memberfiles = <FILE>;
        close(FILE);
	$i=0;
        foreach $memtypedata (@memberfiles) {
	chomp $memtypedata;
        ($username, $membertype) = split(/\t/,$memtypedata);

       if ($membertype eq $usertype) {
       print qq~
       <a href="setmembers.cgi?action=edit&member=$username">$username</a><br><br>~;
       $i++;
       }
    }
       print qq~
       <br><br>
       <b>���ҵ� $i λ�û�</b><br>
       </td></tr>
       ~;
       }
     }

print qq~</td></tr></table></body></html>~;
exit;
