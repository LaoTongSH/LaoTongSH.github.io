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
require "data/styles.cgi";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "visitforum.lib.pl";
$|++;                                     # Unbuffer the output
$thisprog = "lmcode.cgi";
print header(-charset=>gb2312);
$output = qq~
  <table cellpadding="5" style="border-collapse: collapse" width="97%" cellspacing="0" bordercolor=$tablebordercolor border=1>
    <tr>
      <td width="100%" colspan="3" bgcolor=$titlecolor>
      <p align="center"><font color="#333333"><b>��ӭ���� <u>$boardname</u> ���˴���</b></font></td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>��̳���ƣ�</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>$boardname</td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>��̳��ַ��</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>
      <a href="$boardurl/$forumsummaryprog" target=_blank>
      $boardurl/$forumsummaryprog</a></td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>��̳ͼ�꣺</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>
~;
if ($boardlogos ne "http://") {$output .=qq~<a href="$boardlogos" target=_blank>$boardlogos</a>~;}
else {$output .=qq~û��~;}
      $output.= qq~
      </td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>��̳˵����</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>$boarddescription</td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>������ʾ��</b></td>
      <td width="100" bgcolor=$forumcolortwo>
      <p align="center">
~;
if ($boardlogos ne "http://") {$output .=qq~<a href="$boardurl/$forumsummaryprog" target=_blank><img src="$boardlogos" align="left" width="88" height="31" border="0"></a>~;}
else {$output .=qq~��ȱͼ��~;}
      $output.= qq~
      </td>
      <td width="*" bgcolor=$forumcolortwo>
      <a target="_blank" href="$boardurl/$forumsummaryprog">
      <b>$boardname</b></a><br>
      $boarddescription</td>
    </tr>
    <tr>
      <td width="100%" colspan="3" bgcolor=$catback>
      <p align="center">
<input type=submit name="winclose" value="�� ��" onclick=window.close();></td>
    </tr>
  </table>
~;
    &printmessanger(
        -Title   => "$boardname - �鿴������̳���롡", 
        -ToPrint => $output, 
        -Version => $versionnumber 
    );
exit;