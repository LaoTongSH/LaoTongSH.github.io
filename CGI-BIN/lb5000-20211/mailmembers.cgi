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

$|++;                                     # Unbuffer the output

########################## Main Program #######################################################

$thisprog = "mailmembers.cgi";

$remprog = "remmail.cgi";

$query = new LBCGI;

$action          = $query -> param('action');
$subjekt         = $query -> param('subjekt');
$message         = $query -> param('text');
$sendto          = $query -> param('sendto');
$membersnamesin  = $query -> param('membersnames');
$footerlinein    = $query -> param('footerline');
$action          = &unHTML("$action");
$subjekt         = &unHTML("$subjekt");
$message         = &unHTML("$message");
$sendto          = &unHTML("$sendto");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");


print header(-charset=>gb2312);       
&admintitle;
        
&getmember("$inmembername");
        
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / Email Ⱥ��</b>
            </td></tr>
            ~;

            if ($action eq "send")       {&sendmymail;}
            elsif ($action eq "sent")    {&mailsent;}
            elsif ($action eq "compose") {&composemail;}
            elsif ($action eq "view")    {&view;}
            elsif ($action eq "Update")  {&update;}
            elsif ($action eq "footer")  {&viewfoot;}
            elsif ($action eq "Save")    {&updatefoot;}
            else {&mailoptions;}
            

            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }

sub mailoptions {

$output= qq~
 <tr>
 <br><br><td bgcolor=#eeeeee colspan=2 align=center><font color=#333333><b>���ܲ˵�</b><BR>Ϊ�˲������û����ڷǱ�Ҫ����£�������Ҫʹ�ô˹���</font>  </td>
 </tr>
 <tr  bgcolor="#ffffff"> 
 <td align="center"><BR><SELECT name=action style="WIDTH: 250px">
 <OPTION selected value="compose">�༭�������ʼ�</OPTION>
 <OPTION value="view">���˳��ʼ��û��б�</OPTION>
 <OPTION value="footer">�鿴���༭ҳ��</OPTION>
 </SELECT>
 <BR>
 <BR>
 </td>
 </tr>
 <tr> 
 <td colspan="2" width="100%" bgcolor=#eeeeee align=center>
 <input type="submit" name="Button" value="ȷ ��">
 </td>
 </tr>
~;
&displayoutput;

}

sub composemail {

$output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>�༭Ҫ���͵��ʼ�</td>
 </tr>
 <tr bgcolor="#FFFFFF" valign=top> 
 <td>
 <b>���⣺</b>
 </td>
 <td>
 <input type="text" name="subjekt">
 </td>
 </tr>
 <tr bgcolor="#FFFFFF" valign=top> 
 <td width="40%">
 <b>���ݣ�</b>
 </td>
 <td width="60%">
 <textarea size=20 name="text" cols="60" rows="10"></textarea>
 <br>
 </td>
 </tr>
 <tr> 
 <td colspan="2" align="center" width="100%" bgcolor=#EEEEEE>
 <SELECT name="sendto" style="HEIGHT: 22px; WIDTH: 148px"> 
 <OPTION selected value="members">����ע���û�</OPTION>
 <OPTION value="moderators">��̳���а���</OPTION>
 </SELECT>
 &nbsp;
 <input type=hidden name="action" value="send">
 <input type="submit" name="Button" value="ȷ ��">��<input type="reset" name="Button" value="�� ��">
 </td>
 </tr>
~;
&displayoutput;

}

sub sendmymail {

if (($message eq "") || ($subjekt eq "")) {

 $output = qq~
  <tr>
  <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>��������</td>
  </tr>
  <tr>
  <td width="100%" align="center">
  <br><br>
  <font color="#FF0000">������������ʼ�����</font><br>
  <a href="$thisprog?action=compose">���˷���</a>
  </tr>
  <tr>
  ~;
 &displayoutput
}

$filetoopen = "$lbdir" . "data/footer.cgi";
open (FILE,"<$filetoopen");
 flock (FILE,2);
 @footerin = <FILE>;
close (FILE);

$footer = "\n";
foreach $line (@footerin) {
 chomp($line);
 if ($line ne "") {
   $footer .= "$line\n";
 }
}

$filetoopen = "$lbdir" . "data/remmem.cgi";
open (FILE,"<$filetoopen");
 flock (FILE,2);
 @members = <FILE>;
close (FILE);

if ($sendto eq "members") {
 &sendmembers
}elsif ($sendto eq "moderators") {
 &sendmoderators
}else{
 &composemail
}
}

sub mailsent {

$output = qq~
 <tr>
 <br><br><td bgcolor=#eeeeee colspan=2><font color=#333333><b>Ⱥ�� Email</b></font>  </td>
 </tr>
 <tr  bgcolor="#ffffff">
 <Td align="center">
 �ʼ��Ѿ����͸��� $membercount ���û��ˡ�
 </td>
 </tr>
 <tr>
 <td colspan="2" width="100%" bgcolor=#eeeeee>
 <input type="submit" name="Button" value="�� ��">
 </td>
 </tr>
 ~;
&displayoutput;

}

sub sendmembers {
 $mail = "";
 open (MEMFILE, "${lbdir}data/lbmember.cgi");
 flock (MEMFILE, 1) if ($OS_USED eq "Unix");
 @cgi = <MEMFILE>;
 close(MEMFILE);

 $membercount = 0;
 foreach $member (@cgi) {
  @memberdaten = split(/\t/,$member);
  $mail = $memberdaten[4];
 
  $checkmember = 1;
  foreach $remmember (@members) {
   chomp($remmember);
   if ($remmember eq $memberdaten[0]) {$checkmember = 0;}
  } 
  if ($checkmember == 1) {
    if ($mail eq "") { $mail = $mail1; } else { $mail .= ", $mail1"; }
    $membercount++;
  }
 }
 &gosend;
 &mailsent;
}

sub sendmoderators {
 $mail = "";
 open (MEMFILE, "${lbdir}data/lbmember.cgi");
 flock (MEMFILE, 1) if ($OS_USED eq "Unix");
 @cgi = <MEMFILE>;
 close(MEMFILE);

 $membercount = 0;
 foreach $member (@cgi) {
  @memberdaten = split(/\t/,$member);
  $mail1 = $memberdaten[4];
  if (($memberdaten[1] eq "ad") || ($memberdaten[1] eq 'smo') || ($memberdaten[1] eq "mo")) {
 
   $checkmember = 1;
   foreach $remmember (@members) {
    chomp($remmember);
    if ($remmember eq $memberdaten[0]) {$checkmember = 0;}
   } 
   if ($checkmember == 1) {
    if ($mail eq "") { $mail = $mail1; } else { $mail .= ", $mail1"; }
    $membercount++;
   }
  }
 }
 &gosend;
 &mailsent;
}

sub gosend {
$mymessage = "$message\n\n$footer\n\n����Ժ����յ����Ƶ��ż���������������ӣ�\n$boardurl/$remprog?member=$memberdaten[0]\n.\n";
&sendmail($adminemail_out, $adminemail_in, $mail, $SMTP_SERVER, $subjekt, $mymessage);
#&sendmail($from, $emailaddress, $to, $SMTP_SERVER, $subject, $message);
}

sub view {

$filetoopen = "$lbdir" . "data/remmem.cgi";
open (FILE,"<$filetoopen");
 flock (FILE,2);
 @members = <FILE>;
close (FILE);

$memberoutput = "\n";
foreach $member (@members) {
 chomp($member);
 if ($member ne "") {
   $memberoutput .= "$member\n";
 }
}


$output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>���˳��ʼ��û��б�</td>
 </tr>
 <tr bgcolor="#FFFFFF">
 <td align="center">
 <center>
 <TEXTAREA style="WIDTH: 200px; HEIGHT: 400px" name=membersnames rows=29 cols=25>$memberoutput</TEXTAREA>
 </center>
 </td>
 </tr>
 <tr>
 <td align="center" width="100%" bgcolor=#EEEEEE>
 &nbsp;
 <input type="hidden" name="action" value="Update">
 <input type="submit" value="�� ��">
 </td>
 </tr>
~;
&displayoutput;

}

sub update {

@membersname  = split(" ", $membersnamesin);

foreach $membername (@membersname) {
 chomp($membername);
 if ($membername ne "") {
  chomp($membername);
  $membersnames .= "$membername\n";
 }
}

$filetoopen = "$lbdir" . "data/remmem.cgi";
open (FILE,">$filetoopen");
 flock (FILE,2);
 print FILE "$membersnames";
close (FILE);

$output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>���˳��ʼ��û��б�</td>
 </tr>
 <tr bgcolor="#FFFFFF">
 <td align="center">
 <center>
 ���������Ѿ�����
 </center>
 </td>
 </tr>
 <tr>
 <td align="center" width="100%" bgcolor=#EEEEEE>
 &nbsp;
 <input type="submit" name="Button" value="�� ��">
 </td>
 </tr>
~;
&displayoutput;
}

sub viewfoot {
$filetoopen = "$lbdir" . "data/footer.cgi";
open (FILE,"<$filetoopen");
 flock (FILE,2);
 @footer = <FILE>;
close (FILE);
$footeroutput ="";
foreach $line (@footer) {
 chomp($line);
 if ($line ne "") {
   $footeroutput .= "$line\n";
 }
}


$output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>�༭ҳ��</td>
 </tr>
 <tr bgcolor="#FFFFFF">
 <td align="center">
 <center>
 <TEXTAREA style="WIDTH: 400px; HEIGHT: 100px" name=footerline rows=29 cols=25>$footeroutput</TEXTAREA>
 </center>
 </td>
 </tr>
 <tr>
 <td align="center" width="100%" bgcolor=#EEEEEE>
 &nbsp;
 <input type="hidden" name="action" value="Save">
 <input type="submit" value="�� ��">
 </td>
 </tr>
~;
&displayoutput;

}

sub updatefoot {

@footerline  = split("\n", $footerlinein);

foreach $line (@footerline) {
 chomp($line);
 if ($line ne "") {
  chomp($line);
  $footerlines .= "$line\n";
 }
}

$filetoopen = "$lbdir" . "data/footer.cgi";
open (FILE,">$filetoopen");
 flock (FILE,2);
 print FILE "$footerlines";
close (FILE);

$output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>����ҳ�����</td>
 </tr>
 <tr bgcolor="#FFFFFF">
 <td align="center">
 <center>
 ��Ϣ�Ѿ�����
 </center>
 </td>
 </tr>
 <tr>
 <td align="center" width="100%" bgcolor=#EEEEEE>
 &nbsp;
 <input type="submit" name="Button" value="�� ��">
 </td>
 </tr>
~;
&displayoutput;
}

sub displayoutput {

print qq~
 <form action="$thisprog" method="post">
 <table border="0" align="center" width="456">
 $output
 </table>
 </form>
 </table>
 </body>
 </html>
~;
exit;

}
