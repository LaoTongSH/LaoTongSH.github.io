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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                        # Unbuffer the output

########################## Program #####################################

$thisprog = "remmail.cgi";

$query = new LBCGI;

@params = $query->param;
foreach $param(@params) {
    $theparam = $query->param($param);
    $theparam = &unHTML("$theparam");
    ${$param} = $theparam;
}

$inmembername = $query->cookie("amembernamecookie");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if (lc($inmembername) eq lc($member)) {
 $filetoopen = "$lbdir" . "data/remmem.cgi";
 open (FILE,"$filetoopen");
 flock (FILE,2);
  @members = <FILE>;
 close (FILE);

foreach $removed (@members) {
 chomp($removed);
 if ($removed eq $member) {
  $output = qq~
   <tr bgcolor="#FFFFFF">
   <td align="center">
   ��ã�$member�����Ѿ��˳� LB5000 �ʼ��б��ˡ�
   </td>
   </tr>
  ~;
  &displayoutput;
 }
}


$filetoopen = "$lbdir" . "data/remmem.cgi";
open (FILE,">>$filetoopen");
 print FILE "$member\n";
close (FILE);

$output = qq~
 <tr bgcolor="#FFFFFF">
 <td align="center">
 ��ã�$member�����Ѿ��˳� LB5000 �ʼ��б��ˡ�
 <br>����������¼��룬����ϵ <a href="mailto:$adminemail_out">̳��</a> ��
 </td>
 </tr>
~;
&displayoutput;

} else {

$output = qq~
 <tr bgcolor="#FFFFFF">
 <td align="center">
 �Բ������ Cookie ��ƥ�䡣<br>��������˳����ʼ��б�����ô�������ȵ�½��̳��
 <br><a href="$boardurl/$loginprog">���˵�½������</a>
 </td>
 </tr>
~;
&displayoutput;
}

sub displayoutput {

print qq~
 <html>
 <head>
 <title></title>
 </head>
 <body bgcolor="#FFFFFF">
 <table border="0" align="center" width="456">
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333 size=3><b>��ӭʹ�� LB5000 �ʼ��б�</td>
 </tr>
 $output
 </table>
 </body>
 </html>~;
exit;
}