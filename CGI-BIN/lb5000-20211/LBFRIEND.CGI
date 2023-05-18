#!/usr/bin/perl
#############################################################
#  LeoBoard ver.5000 / LB5000 / 雷傲超级论坛 ver.5000
#
#  版权所有: 雷傲工作室(原蓝宝石软件工作室)
#
#  制作人  : 山鹰糊 (Shining Hu)
#            花无缺 (Ifairy Han)
#           
#  主页地址: http://www.CGIer.com/      CGI 编程者之家
#	     http://www.LeoBoard.com/   雷傲论坛支持主页
#	     http://www.leoBBS.com/     本论坛直通车
#            http://maildo.com/      大家一起邮
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
&ipbanned; #封杀一些 ip
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
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));
$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
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
        &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;发个邮件给朋友
        </td>
    </tr>
  </table>
  <p>
  <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
      <td>
      <table cellpadding=6 cellspacing=1 border=0 width=100%>
~;
if ($emailfunctions ne "on") { &error("发邮件给朋友&对不起，论坛管理员没有将邮件功能打开！"); }
  if ($action eq "send") {
    $blankfields = "";
    if(!$inrealname)        { $blankfields = "yes"; }
    elsif(!$intoname)       { $blankfields = "yes"; }
    elsif(!$intoemail)      { $blankfields = "yes"; }
    elsif(!$infromemail)    { $blankfields = "yes"; }
    elsif(!$insubject)      { $blankfields = "yes"; }
    elsif(!$inemailmessage) { $blankfields = "yes"; }
    
    if ($blankfields) {
        &error("发邮件给朋友&请输入所有内容然后发送！");
    }
    
    if ($infromemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) { &error("发邮件给朋友&错误的邮件地址！"); }
    if ($intoemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) { &error("发邮件给朋友&错误的邮件地址！"); }
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
    $message .= "来自 LB5000 论坛中朋友的消息\n";
    $message .= "---------------------------------------------------------------------\n\n";
    $message .= "$inrealname 从 $homename 发送邮件给您。\n";
    $message .= "---------------------------------------------------------------------\n\n";
    $message .= "$inemailmessage\n\n";
    $message .= "主题： $emailtopictitle\n\n\n";
    $message .= "网址： $boardurl/$threadprog?forum=$inforum&topic=$intopic\n";
    $message .= "---------------------------------------------------------------------\n\n";
    $message .= "提示：您没有必要回复这封邮件，这只是论坛的内容通知。\n\n";
    $message .= "---------------------------------------------------------------------\n";
                
    &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
    $output .= qq~
        <tr>
         <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>Email 发送完成！</b></font></td></tr>
         <tr>
         <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
         具体情况：：
         <ul>
         <li><a href="$threadprog?forum=$inforum&topic=$intopic">返回主题</a>
         <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
         <li><a href="$forumsummaryprog">返回论坛首页</a>
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
    $topictitle =~ s/^＊＃！＆＊//;
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
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc><b>发个邮件给朋友</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc>
    <b>通过邮件发送主题 <a href="$threadprog?forum=$inforum&topic=$intopic">$topictitle</a> 给您的朋友。</b>　下列所有项必填，并请输入正确的邮件地址！<br>你可以添加一些自己的信息在下面的内容框内。至于这个贴子的主题和 URL 你可以不必写，因为本程序会在发送的 Email 中自动添加的！
    </td>
    <tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>您的姓名：</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="realname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc><b>您的 Email 地址：</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="fromemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>您朋友的名字：</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="toname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc><b>您朋友的 Email：</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="toemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>Email 标题：</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="subject" value="$topictitle"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>消息内容：</b></td>
    <td bgcolor=$miscbackone><textarea name="emailmessage" cols="55" rows="6">我想你对 '$homename' 的 '$topictitle' 这个贴子内容会感兴趣的！请去看看！</textarea></td>
    </tr><tr>
    <td colspan=2 bgcolor=$miscbacktwo align=center><input type=hidden name="emailtopictitle" value="$topictitle"><input type=submit value="发 送" name="Submit"></table></td></form></tr></table>
    ~;
}
&output(
 -Title   => $boardname, 
 -ToPrint => $output, 
 -Version => $versionnumber 
);
