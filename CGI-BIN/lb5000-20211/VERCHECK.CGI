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
require "data/styles.cgi";   # Require styles info
require "data/cityinfo.cgi";
require "lb.lib.pl";          # Require lbboard ()

$|++;                                      # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "vercheck.cgi";


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
	$server_port = ":$ENV{'SERVER_PORT'}" if ($ENV{'SERVER_PORT'} ne '80');
	$fullurl     = "http://$ENV{'SERVER_NAME'}$server_port$ENV{'SCRIPT_NAME'}";
	$myurl       = substr($fullurl,0,rindex($fullurl,"/"));
        $geturl="http://www.leoboard.com/cgi-bin/lbver.cgi?ver=$versionnumber&url=$myurl";
        
	$out=&lbagent($geturl);
        
        ($lastver,  $finish, $downtime, $nowver, $hasfunc, $gb, $big5, $download) = split(/��/,$out);
        (my $tmp,$lastver) = split(/\|/,$lastver);
             
        
       if ($lastver ne "") {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=����  color=#FFFFFF>
                <b>��ӭ������̳�������� / �鿴��̳�汾����</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2><br>
               ~;
                
                if ($versionnumber =~/LB5000/g){
                $myver=$versionnumber;
                $myver=~s /LB5000II v//isg;
                $myver=~s /LB5000 II v//isg;
                $newver=$nowver;
                $newver=~s /LB5000II v//isg;
                $newver=~s /LB5000 II v//isg;
                
                my $gengxin="";
                if ($myver >= $newver){
                print qq~
                <font face=���� color=#333333 ><center><b>������ʹ�õ������°汾����л��ʹ�����ǵ���̳ ��</b><br><br>
                ~;
                $gengxin="��������";
                }else{
               print qq~
                <font face=���� color=#333333 ><center><b>$myver >= $newver��ǰ$nowver�Ѿ��ṩ���أ��������Ҫ��������ο���������� ��</b><br><br>
                ~;
                $gengxin="��Ҫ����";
               }
               print qq~
               <table><tr><td>��ǰ���°汾:$lastver  [ �㵱ǰʹ�ð汾:$versionnumber <font color=red>$gengxin</font>]<br><hr>
               <br>
               <font color=blue>����ɹ���:</font><br><br>
               $finish <br>
               �����ṩ����ʱ��:$downtime <br>
               <hr>
               </td></tr>
               <tr><td>��ǰ���ṩ���ص����°汾:$nowver <br><hr>
               <br>
               <font color=red>�����б�:</font><br><br>
               $hasfunc <br>
               ���ص�ַ:<br>
                [GB�汾]<a href=$gb>$gb</a> <br>
                [BIG5�汾]<a href=$big5>$big5</a><br>
               <hr><br>
               <b>��2001��5��15������������<b><font color=blue>$download</font></b>�˰�װ������̳��</b>
               <hr>
               </td></tr></table>
               ~;
               }else{
               print qq~
                <font face=���� color=#333333 ><center><b>��Ƿ��޸İ汾�ţ��뼰ʱ�Ļ����ӺͰ汾��ʾ��лл������</b><br><br>
                ~;
               }
               

                print qq~
                </center>
                </td></tr></table></td></tr></table>
                ~;
                }

                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=����  color=#FFFFFF>
                    <b>��ӭ���� LB5000 ��̳��������/�鿴��̳�汾����</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font color=#333333><b>û�а汾��Ϣ</b><br>����Socketģ�鲻������ʹ�ã�����Leoboard�����������������http://www.leoboard.com�鿴��������� ��
                    </td></tr></table></td></tr></table>
                    ~;
                    }
        
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                               print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=����  color=#FFFFFF>
                <b>��ӭ������̳�������� / ��̳�汾���</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333 ><b>��̳�汾���</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                
                <font face=���� color=#990000 ><b><center>LB5000 ��̳�������� / ��̳�汾���</center></b><br>
                <font face=���� color=#333333 >����Բ鿴��ǰLeoboardվ����̳�İ汾�����<br>֪����ǰ���°汾���Ƿ����������õĹ��ܣ��Ƿ��ʺ���������<br><br>
                ������û��Σ���ԣ�������������û�в��ü��ܷ�ʽ���ͣ�<br>������Ϊ���ô�һ�����°汾�������лл������װ���̳��
                
                </td>
                </tr>
                              
               <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="���汾�������"></form></td></tr></table></td></tr></table>
               
               ~;

                            
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;
