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
require "data/styles.cgi";
require "lbmail.lib.pl";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                        # Unbuffer the output
$thisprog = "lbfriend.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip
$inforum         = $query -> param('forum');
$intopic         = $query -> param('topic');
$action          = $query -> param('action');
$inrealname      = $query -> param('realname');
$intoname        = $query -> param('toname');
$infromemail     = $query -> param('fromemail');
$intoemail       = $query -> param('toemail');
$insubject       = $query -> param('subject');
$inemailmessage  = $query -> param('emailmessage');
$emailtopictitle = $query -> param('emailtopictitle');
$inrealname          = &cleaninput($inrealname);
$insubject           = &cleaninput($insubject);
$inemailmessage      = &cleaninput($inemailmessage);
$emailtopictitle     = &cleaninput($emailtopictitle);
$inforum             = &cleaninput($inforum);
$intopic             = &cleaninput($intopic);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
&badwordfile;

print header(-charset=>gb2312);
&title;
$output .= qq~
  <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
    <tr>
        <td width=30% rowspan=2 valign=top><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td valign=middle align=left><font face="$font" color=$fontcolormisc>
        &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0>&nbsp;&nbsp;<a href="$forumsummaryprog">$boardname</a>
	    <br>
        &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;�����ʼ�������
        </td>
    </tr>
  </table>
  <p>
  <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
      <td>
      <table cellpadding=6 cellspacing=1 border=0 width=100%>
~;
if ($emailfunctions ne "on") { &error("���ʼ�������&�Բ�����̳����Աû�н��ʼ����ܴ򿪣�"); }
  if ($action eq "send") {
    $blankfields = "";
    if(!$inrealname)        { $blankfields = "yes"; }
    elsif(!$intoname)       { $blankfields = "yes"; }
    elsif(!$intoemail)      { $blankfields = "yes"; }
    elsif(!$infromemail)    { $blankfields = "yes"; }
    elsif(!$insubject)      { $blankfields = "yes"; }
    elsif(!$inemailmessage) { $blankfields = "yes"; }
    
    if ($blankfields) {
        &error("���ʼ�������&��������������Ȼ���ͣ�");
    }
    
    if ($infromemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) { &error("���ʼ�������&������ʼ���ַ��"); }
    if ($intoemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) { &error("���ʼ�������&������ʼ���ַ��"); }
      if ($badwords) {
         @pairs = split(/\&/,$badwords);
         foreach (@pairs) {
             ($bad, $good) = split(/=/,$_);
             chomp $good;
             $insubject =~ s/$bad/$good/isg;
             $inemailmessage=~ s/$bad/$good/isg;
             $emailtopictitle=~ s/$bad/$good/isg;
         }
      }
    $to = $intoemail;
    $from = $infromemail;
    $subject = "$insubject";
    $message .= "\n";
    $message .= "$boardname\n";
    $message .= "$boardurl/$forumsummaryprog\n";
    $message .= "���� LB5000 ��̳�����ѵ���Ϣ\n";
    $message .= "---------------------------------------------------------------------\n\n";
    $message .= "$inrealname �� $homename �����ʼ�������\n";
    $message .= "---------------------------------------------------------------------\n\n";
    $message .= "$inemailmessage\n\n";
    $message .= "���⣺ $emailtopictitle\n\n\n";
    $message .= "��ַ�� $boardurl/$threadprog?forum=$inforum&topic=$intopic\n";
    $message .= "---------------------------------------------------------------------\n\n";
    $message .= "��ʾ����û�б�Ҫ�ظ�����ʼ�����ֻ����̳������֪ͨ��\n\n";
    $message .= "---------------------------------------------------------------------\n";
                
    &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
    $output .= qq~
        <tr>
         <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>Email ������ɣ�</b></font></td></tr>
         <tr>
         <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
         �����������
         <ul>
         <li><a href="$threadprog?forum=$inforum&topic=$intopic">��������</a>
         <li><a href="$forumsprog?forum=$inforum">������̳</a>
         <li><a href="$forumsummaryprog">������̳��ҳ</a>
         </ul>
         </tr>
         </td>
         </table></td></tr></table>
    ~;
}
else {
    $filetoopen = "$lbdir" . "data/allforums.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
    @forums = <FILE>;
    close(FILE);
    foreach $forumline (@forums) {
        ($tempno, $trash) = split(/\t/,$forumline);
        if ($inforum eq $tempno) {
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forumline);
            }
        }
    $filetoopen = "$lbdir" . "boarddata/list$inforum.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
    @allthreads = <FILE>;
    close(FILE);
    
    foreach $line (@allthreads) {
        ($tempno, $trash) = split(/\t/, $line);
        if ($intopic eq $tempno) {
            $linetokeep = $line;
        }
    }
    ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\t/,$linetokeep);
    $topictitle = &cleanarea("$topictitle");
    $topictitle =~ s/^����������//;
    if ($badwords) {
        @pairs = split(/\&/,$badwords);
        foreach (@pairs) {
            ($bad, $good) = split(/=/,$_);
            chomp $good;
            $topictitle=~ s/$bad/$good/isg;
        }
    }
    $output .= qq~
    <form action="$boardurl/$thisprog" method=post>
    <input type=hidden name="action" value="send">
    <input type=hidden name="forum" value="$inforum">
    <input type=hidden name="topic" value="$intopic">
    <tr>
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc><b>�����ʼ�������</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc>
    <b>ͨ���ʼ��������� <a href="$threadprog?forum=$inforum&topic=$intopic">$topictitle</a> ���������ѡ�</b>������������������������ȷ���ʼ���ַ��<br>���������һЩ�Լ�����Ϣ����������ݿ��ڡ�����������ӵ������ URL ����Բ���д����Ϊ��������ڷ��͵� Email ���Զ����ӵģ�
    </td>
    <tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>����������</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="realname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc><b>���� Email ��ַ��</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="fromemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>�����ѵ����֣�</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="toname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc><b>�����ѵ� Email��</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="toemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>Email ���⣺</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="subject" value="$topictitle"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>��Ϣ���ݣ�</b></td>
    <td bgcolor=$miscbackone><textarea name="emailmessage" cols="55" rows="6">������� '$homename' �� '$topictitle' ����������ݻ����Ȥ�ģ���ȥ������</textarea></td>
    </tr><tr>
    <td colspan=2 bgcolor=$miscbacktwo align=center><input type=hidden name="emailtopictitle" value="$topictitle"><input type=submit value="�� ��" name="Submit"></table></td></form></tr></table>
    ~;
}
&output(
 -Title   => $boardname, 
 -ToPrint => $output, 
 -Version => $versionnumber 
);