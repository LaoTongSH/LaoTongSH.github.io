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
require "code.cgi";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "visitforum.lib.pl";
require "lb.lib.pl";
$|++;                                    # Unbuffer the output
$thisprog = "messanger.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$intouser         = $query -> param('touser');
$action           = $query -> param('action');
$inmsg            = $query -> param('msg');
$inwhere          = $query -> param('where');
$inmembername     = $query -> param('membername');
$inpassword       = $query -> param('password');
$inmsgtitle       = $query -> param('msgtitle');
$inmessage        = $query -> param('message');
$inmessage2       = $query -> param('message');
$inmembername        = &cleaninput($inmembername);
$inpassword          = &cleaninput($inpassword);
$inmessage           = &cleaninput($inmessage);
$inmsgtitle          = &cleaninput($inmsgtitle);
$inmessage2          = &cleaninput($inmessage2);

&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intouser =~  m/\//)||($intouser =~ m/\\/)||($intouser =~ m/\.\./));
$intouser =~ s/\///g;
$intouser =~ s/\.\.//g;
$intouser =~ s/\\//g;

$output .= qq~
<script>function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
function openscript(url, width, height) {
        var Win = window.open(url,"openwindow",'width=' + width + ',height=' + height + ',resizable=1,scrollbars=yes,menubar=yes,status=yes' );
        }
function enable(btn){
btn.filters.gray.enabled=0;}
function disable(btn){
btn.filters.gray.enabled=1;}
</script>
<style>
.gray {CURSOR:hand;filter:gray}
</style>
~;
$inboxpm  = qq~<img src=$imagesurl/images/inboxpm.gif border=0 alt="�ռ���" class="gray" onmouseover="enable(this)" onmouseout="disable(this)" width=50 height=40>~;
$outboxpm = qq~<img src=$imagesurl/images/outboxpm.gif border=0 alt="������" class="gray" onmouseover="enable(this)" onmouseout="disable(this)" width=50 height=40>~;
$newpm    = qq~<img src=$imagesurl/images/newpm.gif border=0 alt="������Ϣ" class="gray" onmouseover="enable(this)" onmouseout="disable(this)" width=50 height=40>~;
$replypm  = qq~<img src=$imagesurl/images/replypm.gif border=0 alt="�ظ���Ϣ" class="gray" onmouseover="enable(this)" onmouseout="disable(this)" width=50 height=40>~;
$fwpm  = qq~<img src=$imagesurl/images/fwpm.gif border=0 alt="ת����Ϣ" class="gray" onmouseover="enable(this)" onmouseout="disable(this)" width=50 height=40>~;
$deletepm = qq~<img src=$imagesurl/images/deletepm.gif border=0 alt="ɾ����Ϣ" class="gray" onmouseover="enable(this)" onmouseout="disable(this)" width=50 height=40>~;
$friendpm = qq~<img src=$imagesurl/images/friendpm.gif border=0 alt="�򿪺���¼" class="gray" onmouseover="enable(this)" onmouseout="disable(this)" width=50 height=40>~;

    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

    if ($inmembername eq "") {
        $inmembername = "����";
    }
    &getmember("$inmembername");

    print header(-charset=>gb2312);

if ($allowusemsg eq "off") {&messangererror("����Ϣ��ֹʹ��&�ܱ�Ǹ��̳������ĳ��ԭ���ѽ�ֹ�����û�ʹ�ö���Ϣ����")};

if (($inmsg) && ($inmsg !~ /^[0-9]+$/)) { &error("��ͨ����&�벻Ҫ�޸����ɵ� URL��"); }
$action = "inbox" if ($action eq "");
$output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
      <tr><td>
      <table cellpadding=3 cellspacing=1 border=0 width=100%>
~;

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\t����Ϣ\tnone\t�շ�����Ϣ\t");
}
&badwordfile;

    if ($action eq "new") {
#            &getmember("$inmembername");

$cleanintouser = $inmembername;
$cleanintouser =~ s/ /\_/g;
$cleanintouser =~ tr/A-Z/a-z/;
$messfilename = "$lbdir". "$msgdir/main/$cleanintouser" . "_mian.cgi";
&messangererror("�������Ͷ���Ϣ&�������˶���Ϣ����ţ����������޷����ܶ���Ϣ�ģ�������Ҳ�޷����Ͷ���Ϣ��<BR><font color=$fonthighlight>���ص�½��ȡ������Ϣ����ţ�Ȼ�������·��Ͷ���Ϣ��</font><BR><BR>") if (-e "$messfilename");

            if ($inmembername eq "") { &login("$thisprog?action=reply&touser=$intouser"); }
            elsif ($userregistered eq "no") {  &messangererror("������Ϣ&��û��ע�ᣡ"); }
            elsif ($inpassword ne $password) {  &messangererror("������Ϣ&����������"); }

            $cleanname = $intouser;
            $cleanname =~ s/\_/ /g;

        $filetomake = "$lbdir" . "memfriend/$inmembername.cgi";
	if (-e $filetomake) {
	open(FILE, "$filetomake");
	@currentlist = <FILE>;
	close (FILE);
	}
        $friendlist="";
        foreach $user (@currentlist) {
	chomp $user;
	$friendlist.=qq~<option value=$user>$user</option>~;
	}
            $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=3><font color=$fontcolormisc><b>���Ͷ���Ϣ</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center colspan=3><a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
            </tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action=$thisprog method=post name=FORM>
            <input type=hidden name="action" value="send">
            <font color=$fontcolormisc><b>����������������Ϣ</b></td>
            </tr>
		<SCRIPT LANGUAGE="JavaScript">
		<!--
		function friendls(){
		var myfriend = document.FORM.friend.options[document.FORM.friend.selectedIndex].value;
		document.FORM.touser.value = myfriend;
		}
		// -->
		</SCRIPT>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc><b>�ռ��ˣ�</b></font></td>
            <td bgcolor=$miscbackone><input type=text name="touser" value="$cleanname" size=16> ��<select name="friend" onchange="javascript:friendls()"><option>��������</option>$friendlist</select></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=top width=30%><font color=$fontcolormisc><b>���⣺</b></font></td>
            <td bgcolor=$miscbackone><input type=text name="msgtitle" size=36 maxlength=80 value=$inmsgtitle></td>
            </tr>
            <tr>
            <td bgcolor=$miscbackone valign=top width=30%><font color=$fontcolormisc><b>���ݣ�</b></td>
            <td bgcolor=$miscbackone><textarea cols=35 rows=6 name="message" onkeydown=ctlent()>$inmessage</textarea></td>
            </tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <input type=Submit value="�� ��" name=Submit"> ��<input type="reset" name="Clear" value="�� ��">
            </td></form></tr>
            ~;
    }
	 elsif ($action eq "exportall") {
#            &getmember("$inmembername");
            if ($inmembername eq "����") { &login("$thisprog?action=daochuall&where=$inwhere"); }
            elsif ($userregistered eq "no") { &messangererror("����Ϣ&��û��ע�ᣡ"); }
            elsif ($inpassword ne $password) { &messangererror("����Ϣ&�����������"); }
            $memberfilename = $inmembername;
            $memberfilename =~ s/ /\_/g;
	    $memberfilename =~ tr/A-Z/a-z/;

            if ($inwhere eq "inbox") {
                $filetotrash = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
            }
            elsif ($inwhere eq "outbox") {
                $filetotrash = "$lbdir". "$msgdir/out/$memberfilename" . "_out.cgi";
            }

            if (-e $filetotrash) {
    open (FILE, "$filetotrash");
     my @messanges = <FILE>;
	 close (FILE);

                $output .= qq~
<tr>
<td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>��������Ϣ</b></td></tr><tr>
<td bgcolor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td></tr><tr>
<td bgcolor=$miscbackone align=center>
<form name="FORM2">
<TEXTAREA name=inpost rows=12 style="width=90%">
~;
if ($inwhere eq "inbox") {$boxname="�ռ���"}
else {$boxname="������"};
$current_time=localtime;
$output.=qq~$boardname��$membername�Ķ���Ϣ$boxname��������\n(����ʱ�䣺$current_time)\n----------------------------------------\n~;
foreach (@messanges) {
$messangeswords = $_;
($usrname, $msgread, $msgtime, $msgtitle, $msgwords) = split(/\t/,$_);
$usrname =~ s/ /\_/g;
$usrname =~ tr/A-Z/a-z/;
$msgwords =~ s/\r//ig;
$msgwords =~ s/&nbsp;/ /g;
$msgwords =~ s/\s+/ /g;
$msgwords =~ s/<br>/\n/g;
$msgwords =~ s/<p>/\n/g;
$msgtime = $msgtime + ($timedifferencevalue*3600) + ($timezone*3600);
$msgtime = &dateformat("$msgtime");
$output .= qq~\n[�շ�����]��$usrname\n[�շ�ʱ��]��$msgtime\n[���ű���]��$msgtitle\n[��������]��$msgwords
~;
}
$output .=qq~</TEXTAREA><br>>> <a href="javascript:HighlightAll('FORM2.inpost')">���Ƶ������� <<</a></form><font color=red>����$boxname�еĶ���Ϣ��ȫ����������Щ����Ϣ��δ������ɾ����<br>
Ϊ���ٷ�����ѹ�����뾡��<a href=$thisprog?action=deleteall&where=$inwhere>[���]</a>����$boxname�еĶ���Ϣ��<br><br>
</td></tr>
~;
}
else {&messangererror("����Ϣ&�ļ�û���ҵ������ظ��ղŲ��裡");
}
}
    elsif ($action eq "markall"){
#	    &getmember("$inmembername");
	    if ($inmembername eq "����") { &login("$thisprog?action=daochuall&where=$inwhere"); }
            elsif ($userregistered eq "no") { &messangererror("����Ϣ&��û��ע�ᣡ"); }
            elsif ($inpassword ne $password) { &messangererror("����Ϣ&�����������"); }
            $memberfilename = $inmembername;
            $memberfilename =~ s/ /\_/g;
	    $memberfilename =~ tr/A-Z/a-z/;
	    
        $filetoopen = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        flock (FILE, 1) if ($OS_USED eq "Unix");
        @inboxmessages = <FILE>;
        $count = 0; 
        close (FILE);

        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open (FILE, ">$filetoopen");
        flock (FILE, 2) if ($OS_USED eq "Unix");
        foreach $line (@inboxmessages) {
            chomp $line;
            $msgtograb = @inboxmessages[$count];
            ($from, $readstate, $date, $messagetitle, $post) = split(/\t/,$msgtograb);
            print FILE "$from\tyes\t$date\t$messagetitle\t$post\n";
            $count++;$count2++
        }
        close (FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
$output.=qq~<tr>
<td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>���еĶ���Ϣ�ѱ����Ϊ�Ѷ�</b></td>
</tr>
<tr><td bgcolor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
</tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>����$inwhere�еĶ���Ϣ�Ѿ�ȫ�����Ϊ�Ѷ�</b><br><br>
</td></tr>
~;
}

    elsif ($action eq "outbox") {
#        &getmember("$inmembername");
        if ($inmembername eq "����") { &login("$thisprog?action=outbox"); }
        elsif ($userregistered eq "no") { &messangererror("������&��û��ע�ᣡ"); }
        elsif ($inpassword ne $password) { &messangererror("������&�������"); }

        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
	$memberfilename =~ tr/A-Z/a-z/;

        $filetoopen = "$lbdir". "$msgdir/out/$memberfilename" . "_out.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        @outboxmessages = <FILE>;
        close (FILE);
        $totalinboxmessages = @outboxmessages;
        $output .= qq~
        <style>
INPUT {
	BORDER-TOP-WIDTH: 1px; PADDING-RIGHT: 1px; PADDING-LEFT: 1px; BORDER-LEFT-WIDTH: 1px; FONT-SIZE: 9pt; BORDER-LEFT-COLOR: #cccccc; BORDER-BOTTOM-WIDTH: 1px; BORDER-BOTTOM-COLOR: #cccccc; PADDING-BOTTOM: 1px; BORDER-TOP-COLOR: #cccccc; PADDING-TOP: 1px; HEIGHT: 18px; BORDER-RIGHT-WIDTH: 1px; BORDER-RIGHT-COLOR: #cccccc
}
</style>
<script language="JavaScript">
function CheckAll(form)
  {
  for (var i=0;i<form.elements.length;i++)
    {
    var e = form.elements[i];
          e.checked = true;
    }
  }


function FanAll(form)
 {
  for (var i=0;i<form.elements.length;i++)
    {
    var e = form.elements[i];
      if (e.checked == true){
          e.checked = false;
          }
       else {
          e.checked = true;
          }
    }
}
</script>
        <form action="$thisprog" method=post>
        <input type=hidden name="where" value="outbox">
        <input type=hidden name="action" value="delete">
            <tr><td bgcolor=$miscbacktwo align=center colspan=3><font color=$fontcolormisc><b>��ӭʹ�ö���Ϣ���ͣ�$membername</b></td>
            </tr>
            <tr><td bgcolor=$miscbackone align=center colspan=4><a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center width=20%><font color=$fontcolormisc><b>�ռ���</b></td>
                <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>����</b></td>
                <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>ɾ�����</b></td>
            </tr>
        ~;
        $count = 0;
        foreach (@outboxmessages) {
            ($from, $readstate, $date, $messagetitle, $message) = split(/\t/,$_);
            if ($readstate eq "no") {
                $readstate = qq~<img src=$imagesurl/images/unread.gif border=0 alt="δ��" width=16 height=12>~;
            }
            else {
                $readstate = qq~<img src=$imagesurl/images/read.gif border=0 alt="�Ѷ�" width=16 height=14>~;
            }

	    if ($badwords) {
		@pairs = split(/\&/,$badwords);
		foreach (@pairs) {
		    ($bad, $good) = split(/=/,$_);
		    chomp $good;
		    $messagetitle=~ s/$bad/$good/isg;
		}
	    }
	    $output .= qq~
             <tr>
              <td bgcolor=$miscbackone align=center width=20%><font color=$fontcolormisc>$from</td>
              <td bgcolor=$miscbackone><font color=$fontcolormisc><a href=$thisprog?action=outread&msg=$count>$messagetitle</a></td>
              <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b><input type="checkbox" name="msg" value="$count"></b></td>
             </tr>
	    ~;
	    $count++;
 	}
        $output .=qq~
           <tr>
           <td bgcolor=$miscbacktwo align=center colspan=3><font color=$fontcolormisc><a href=$thisprog?action=deleteall&where=outbox>[ɾ������]</a>  <a href=$thisprog?action=exportall&where=outbox>[��������]</a>  <input type="button" name="chkall" value="ȫѡ" onclick="CheckAll(this.form)">
                            <input type="button" name="clear2" value="��ѡ" onclick="FanAll(this.form)">
                            <input type="reset" name="Reset" value="����">
                            <input type="submit" name="delete" value="ɾ��" ></td>
           </tr>
	~;
    }
    elsif ($action eq "deleteall") {
#            &getmember("$inmembername");
            if ($inmembername eq "����") { &login("$thisprog?action=deleteall&where=$inwhere"); }
            elsif ($userregistered eq "no") { &messangererror("����Ϣ&��û��ע�ᣡ"); }
            elsif ($inpassword ne $password) { &messangererror("����Ϣ&�����������"); }
            $memberfilename = $inmembername;
            $memberfilename =~ s/ /\_/g;
	    $memberfilename =~ tr/A-Z/a-z/;

            if ($inwhere eq "inbox") {
                $filetotrash = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
            }
            elsif ($inwhere eq "outbox") {
                $filetotrash = "$lbdir". "$msgdir/out/$memberfilename" . "_out.cgi";
            }

            if ($filetotrash ne "") {
                unlink "$filetotrash";
            }
            else {
                &messangererror("����Ϣ&�ļ�û���ҵ������ظ��ղŲ��裡");
            }

            $output .= qq~
              <tr>
                <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>���еĶ���Ϣ�ѱ�ɾ��</b></td>
              </tr>
              <tr>
                <td bgcolor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
              </tr>
              <tr>
              <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>����$inwhere�еĶ���Ϣ�Ѿ�ȫ��ɾ��</b><br><br>
</td>
              </tr>
            ~;
    }
    elsif ($action eq "outread") {
#        &getmember("$inmembername");

        if ($inmembername eq "����") { &login("$thisprog?action=outread&msg=$inmsg"); }
        elsif ($userregistered eq "no") { &messangererror("����Ϣ&��û��ע�ᣡ"); }
        elsif ($inpassword ne $password) { &messangererror("����Ϣ&�����������"); }

        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
	$memberfilename =~ tr/A-Z/a-z/;

        $filetoopen = "$lbdir". "$msgdir/out/$memberfilename" . "_out.cgi";
        open (FILE, "$filetoopen");
        @outboxmessages = <FILE>;
        close (FILE);

        $msgtograb = @outboxmessages[$inmsg];

        ($to, $readstate, $date, $messagetitle, $post) = split(/\t/,$msgtograb);

        $date = $date + ($timedifferencevalue*3600) + ($timezone*3600);
        $date = &dateformat("$date");
        $cleanmember = $to;
        $cleanmember =~ s/ /\_/g;
	$cleanmember =~ tr/A-Z/a-z/;
	$post = &lbcode("$post");
	if ($emoticons eq "on") {
	   $post = &doemoticons("$post");
	   $post = &smilecode("$post");
	}
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $messagetitle=~ s/$bad/$good/isg;
            }
        }
        $remsg="Re:$messagetitle";
        $fwmsg="Fw:$messagetitle";
        $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=3><font color=$fontcolormisc><b>��ӭʹ�ö���Ϣ���գ�$membername</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center colspan=3><a href=$thisprog?action=delete&where=outbox&msg=$inmsg>$deletepm</a> ��<a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a> &nbsp;<a href="$thisprog?action=new&touser=$cleanmember&msgtitle=$remsg&message=$replymodel">$replypm</a>��<a href="$thisprog?action=new&touser=$cleanmember&msgtitle=$fwmsg&message=$fwmodel">$fwpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
            </tr>

           <tr>
             <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc>
             ��<b>$date</b>�������ʹ���Ϣ��<b>$to</b>��</font></td>
           </tr>
           <tr>
             <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc>
             <b>��Ϣ���⣺$messagetitle</b><p>
             $post</td>
           </tr>
        ~;
    }
    elsif ($action eq "send") {
$cleanintouser = $intouser;
$cleanintouser =~ s/ /\_/g;
$cleanintouser =~ tr/A-Z/a-z/;
$maxmsgno = 0 if (($maxmsgno < 0)||($maxmsgno eq ""));
$msgnolimit = "off" if (($maxmsgno eq "")||($maxmsgno eq 0));
$msgnolimit = "off" if (($membercode eq "ad")||($membercode eq 'smo')||($membercode eq "mo"));

&getmember("$intouser");
if ($userregistered eq "no") { &messangererror("������Ϣ&û���ҵ��û���"); }
if ($msgnolimit ne "off") {
  if (($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne "mo")){
    my $filetoopen = "$lbdir". "$msgdir/in/$cleanintouser" . "_msg.cgi";
    open (FILE, "$filetoopen");
    flock (FILE, 1) if ($OS_USED eq "Unix");
    my @allmessages = <FILE>;
    close (FILE);
    $checkmsgnolimit = @allmessages;
    if ($checkmsgnolimit >= $maxmsgno) {&messangererror("�޷����Ͷ���Ϣ���Է�&�Է��Ķ���Ϣ�ռ��������� $maxmsgno ����Ϣ���ռ�����");};
  }
}

$messfilename = "$lbdir". "$msgdir/main/$cleanintouser" . "_mian.cgi";
if (-e "$messfilename") {
open(FILE,"<$messfilename");
$mess = <FILE>;
close(FILE);
}
else {$mess = "";}
                &getmember("$inmembername");
                if ($inmembername eq "����")     { &login("$thisprog?action=reply&touser=$intouser"); }
            	elsif ($userregistered eq "no")  { &messangererror("����Ϣ&��û��ע�ᣡ"); }
            	elsif ($membercode eq "banned")     { &messangererror("����Ϣ&������ֹ���ԣ�"); }
            	elsif ($inpassword ne $password) { &messangererror("����Ϣ&�����������"); }
            	elsif ($mess ne "") {  &messangererror("�޷����Ͷ���Ϣ���Է�&�Է������˶���Ϣ����Ź��ܣ�<BR><BR>�Զ�����Żظ�����<font color=$fonthighlight>$mess</font><BR><BR>");}

            	if ($inmsgtitle eq "") { $blanks = "yes"; }
            	if ($inmessage eq "")  { $blanks = "yes"; }
            	if ($intouser eq "")   { $blanks = "yes"; }
	        if ($blanks eq "yes")  { &messangererror("��������&�뽫��Ϣ��д������"); }
	        $memberfilename = $intouser;
        	$memberfilename =~ s/ /\_/g;
		$memberfilename =~ tr/A-Z/a-z/;
            	$currenttime    = time;
            	$filetoopen = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
            	$filetoopen = &stripMETA($filetoopen);
            	open (FILE, "$filetoopen");
            	@inboxmessages = <FILE>;
            	close (FILE);

	    	&winlock($filetoopen) if ($OS_USED eq "Nt");
            	open (FILE, ">$filetoopen");
            	flock (FILE, 2) if ($OS_USED eq "Unix");
            	print FILE "$membername\tno\t$currenttime\t$inmsgtitle\t$inmessage\n";
            	foreach $line (@inboxmessages) {
                    chomp $line;
                    print FILE "$line\n";
                }
                close (FILE);
                &winunlock($filetoopen) if ($OS_USED eq "Nt");

            	$memberfilename = $inmembername;
            	$memberfilename =~ s/ /\_/g;
		$memberfilename =~ tr/A-Z/a-z/;

            	$filetoopen = "$lbdir". "$msgdir/out/$memberfilename" . "_out.cgi";
            	$filetoopen = &stripMETA($filetoopen);
            	open (FILE, "$filetoopen");
            	@outboxmessages = <FILE>;
            	close (FILE);

	    	&winlock($filetoopen) if ($OS_USED eq "Nt");
            	open (FILE, ">$filetoopen");
            	flock (FILE, 2) if ($OS_USED eq "Unix");
            	print FILE "$intouser\tyes\t$currenttime\t$inmsgtitle\t$inmessage\n";
            	foreach $line (@outboxmessages) {
                chomp $line;
                print FILE "$line\n";
	    }
            close (FILE);
	    &winunlock($filetoopen) if ($OS_USED eq "Nt");

            $output .= qq~
              <tr>
                <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>�շ�����Ϣ</b></td>
              </tr>
              <tr>
                <td bgcolor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
              </tr>
              <tr>
                <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>��$intouser�Ķ���Ϣ�Ѿ�������</b><p>����ϢͬʱҲ���Ƶ����ķ��������ˣ�</td>
              </tr>
            ~;
    }
    elsif ($action eq "loggedin") {
#        &getmember("$inmembername");
        if ($inmembername eq "����")     { &login("$thisprog?action=loggedin"); }
        elsif ($userregistered eq "no")  { &messangererror("�ռ���&��û��ע�ᣡ"); }
        elsif ($inpassword ne $password) { &messangererror("�ռ���&�����������"); }

        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
	$memberfilename =~ tr/A-Z/a-z/;

        $filetoopen = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        @allmessages = <FILE>;
        close (FILE);

        $totalmessages = @allmessages;
        $unread = 0;
        foreach (@allmessages) {
            ($from, $readstate, $date, $messagetitle, $message) = split(/\t/,$_);
            if ($readstate eq "no") {
                $unread++;
            }
        }

        if ($unread eq "0") { $unread eq "no"; }
        $output .= qq~
          <tr>
            <td bgcolor=$miscbacktwo  align=center><font color=$fontcolormisc><b>��ӭʹ�ö���Ϣ��$membername</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center>
                <font color=$fontcolormisc><p>
                �������� <b>$totalmessages</b> ����Ϣ�������ռ����ڡ�<p>
                ������<b><font color=$fonthighlight>$unread</b><font color=$fontcolormisc>������Ϣ��
                <p>
                <blockquote><b>ע��</b>�� ���͸�������Ϣֻ���������鿴���뼰ʱɾ�����ڵ���Ϣ����������������ɹ�����</blockquote></font>
                </td></tr>
            <tr>
	~;
    }
    elsif ($action eq "inbox") {
#        &getmember("$inmembername");

        if ($inmembername eq "����") { &login("$thisprog?action=inbox");}
        elsif ($userregistered eq "no") { &messangererror("�ռ���&��û��ע�ᣡ"); }
        elsif ($inpassword ne $password) { &messangererror("�ռ���&�����������"); }

        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
	$memberfilename =~ tr/A-Z/a-z/;

        $filetoopen = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        @inboxmessages = <FILE>;
        close (FILE);

        $totalinboxmessages = @inboxmessages;
        $output .= qq~
<style>
INPUT {
	BORDER-TOP-WIDTH: 1px; PADDING-RIGHT: 1px; PADDING-LEFT: 1px; BORDER-LEFT-WIDTH: 1px; FONT-SIZE: 9pt; BORDER-LEFT-COLOR: #cccccc; BORDER-BOTTOM-WIDTH: 1px; BORDER-BOTTOM-COLOR: #cccccc; PADDING-BOTTOM: 1px; BORDER-TOP-COLOR: #cccccc; PADDING-TOP: 1px; HEIGHT: 18px; BORDER-RIGHT-WIDTH: 1px; BORDER-RIGHT-COLOR: #cccccc
}
</style>
<script language="JavaScript">
function CheckAll(form)
  {
  for (var i=0;i<form.elements.length;i++)
    {
    var e = form.elements[i];
          e.checked = true;
    }
  }


function FanAll(form)
 {
  for (var i=0;i<form.elements.length;i++)
    {
    var e = form.elements[i];
      if (e.checked == true){
          e.checked = false;
          }
       else {
          e.checked = true;
          }
    }
}
</script>
        <form action="$thisprog" method=post>
        <input type=hidden name="where" value="inbox">
        <input type=hidden name="action" value="delete">
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=4><font color=$fontcolormisc><b>��ӭʹ�������ռ��䣬$membername</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center colspan=4><a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>������</b></td>
                <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>����</b></td>
                <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>�Ƿ��Ѷ�</b></td>
                <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>ɾ�����</b></td>
            </tr>
        ~;

        $count = 0;

        foreach (@inboxmessages) {
            ($from, $readstate, $date, $messagetitle, $message) = split(/\t/,$_);
            if ($readstate eq "no") {
                $readstate = qq~<img src=$imagesurl/images/unread.gif border=0 alt="δ��" width=16 height=12>~;
            }
            else {
                $readstate = qq~<img src=$imagesurl/images/read.gif border=0 alt="�Ѷ�" width=16 height=14>~;
            }
            if ($badwords) {
                @pairs = split(/\&/,$badwords);
                foreach (@pairs) {
                    ($bad, $good) = split(/=/,$_);
                    chomp $good;
                    $messagetitle=~ s/$bad/$good/isg;
                }
            }

            $output .= qq~
                <tr>
                    <td bgcolor=$miscbackone align=center><font color=$fontcolormisc>$from</td>
                    <td bgcolor=$miscbackone><font color=$fontcolormisc><a href=$thisprog?action=read&msg=$count>$messagetitle</a></td>
                    <td bgcolor=$miscbackone align=center>$readstate</td>
                    <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b><input type="checkbox" name="msg" value="$count"></b></td>
                </tr>
            ~;
            $count++;
        }

        $output .= qq~
            <tr>
            <td bgcolor=$miscbacktwo align=center colspan=4><font color=$fontcolormisc><a href=$thisprog?action=deleteall&where=inbox>[ɾ������]</a> <a href=$thisprog?action=exportall&where=inbox>[��������]</a> <a href=$thisprog?action=markall&where=inbox>[�������Ϊ�Ѷ�]</a> <input type="button" name="chkall" value="ȫѡ" onclick="CheckAll(this.form)">
                            <input type="button" name="clear2" value="��ѡ" onclick="FanAll(this.form)">
                            <input type="reset" name="Reset" value="����">
                            <input type="submit" name="delete" value="ɾ��" ></td>
            </tr>
        ~;
    }
    elsif ($action eq "read") {
#        &getmember("$inmembername");

        if ($inmembername eq "����") { &login("$thisprog?action=read&msg=$inmsg"); }
        elsif ($userregistered eq "no") { &messangererror("����Ϣ&��û��ע�ᣡ"); }
        elsif ($inpassword ne $password) { &messangererror("����Ϣ&�����������"); }

        $memberfilename = $inmembername;
        $memberfilename =~ s/ /\_/g;
	$memberfilename =~ tr/A-Z/a-z/;

        $filetoopen = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen");
        @inboxmessages = <FILE>;
        close (FILE);

        $msgtograb = @inboxmessages[$inmsg];

        ($from, $readstate, $date, $messagetitle, $post) = split(/\t/,$msgtograb);

        $count = 0;

        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open (FILE, ">$filetoopen");
        flock (FILE, 2) if ($OS_USED eq "Unix");
        foreach $line (@inboxmessages) {
            chomp $line;
            if ($count eq $inmsg) {
                print FILE "$from\tyes\t$date\t$messagetitle\t$post";
            }
            else {
                print FILE "$line\n";
            }
            $count++;
        }
        close (FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");

        $date = $date + ($timedifferencevalue*3600) + ($timezone*3600);
        $date = &dateformat("$date");
        $cleanmember = $from;
        $cleanmember =~ s/ /\_/g;
	$cleanmember =~ tr/A-Z/a-z/;
	$post1 = $post;
        $post = &lbcode("$post");
        if ($emoticons eq "on") {
            $post = &doemoticons("$post");
	    $post = &smilecode("$post");
        }
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $messagetitle=~ s/$bad/$good/isg;
                $post=~ s/$bad/$good/isg;
            }
        }
        $remsg="Re:$messagetitle";
        $fwmsg="Fw:$messagetitle";
        $replymodel="$cleanmember�����ã��ϴ���д����$post1";
        $fwmodel="$cleanmember�����ã�������ת������Ϣ��$post1";
        $postmodel="$cleanmember�����ã�";
        $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=3><font color=$fontcolormisc><b>��ӭʹ�������ռ��䣬$membername</b></td>
            </tr>
            <tr>
                <td bgcolor=$miscbackone align=center colspan=3><a href="$thisprog?action=delete&where=inbox&msg=$inmsg">$deletepm</a> ��<a href="$thisprog?action=inbox">$inboxpm</a> ��<a href="$thisprog?action=outbox">$outboxpm</a> ��<a href="$thisprog?action=new">$newpm</a> ��<a href="$thisprog?action=new&touser=$cleanmember&msgtitle=$remsg&message=$replymodel">$replypm</a>��<a href="$thisprog?action=new&touser=$cleanmember&msgtitle=$fwmsg&message=$fwmodel">$fwpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
            </tr>
            <tr>
               <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc>
               ��Ϣ����<b>$from</b>�����͸�����ʱ�䣺<b>$date</b></font></td>
            </tr>
            <tr>
               <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc>
               <b>��Ϣ���⣺$messagetitle</b><p>
               $post</td>
            </tr>
	~;
    }
    elsif ($action eq "delete") {
#            &getmember("$inmembername");

            if ($inmembername eq "����") { &login("$thisprog?action=delete&where=$inwhere&msg=$inmsg"); }
            elsif ($userregistered eq "no") { &messangererror("����Ϣ&��û��ע�ᣡ"); }
            elsif ($inpassword ne $password) { &messangererror("����Ϣ&�����������"); }

            $memberfilename = $inmembername;
            $memberfilename =~ s/ /\_/g;
	    $memberfilename =~ tr/A-Z/a-z/;

            if ($inwhere eq "inbox") {
                $filetoopen = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
            }
            elsif ($inwhere eq "outbox") {
                $filetoopen = "$lbdir". "$msgdir/out/$memberfilename" . "_out.cgi";
            }

            $filetoopen = &stripMETA($filetoopen);
            open (FILE, "$filetoopen");
            @boxmessages = <FILE>;
            close (FILE);

            $count = 0;

            @inmsg            = $query -> param('msg');
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open (FILE, ">$filetoopen");
            flock (FILE, 2) if ($OS_USED eq "Unix");
            foreach $line (@boxmessages) {
                chomp $line;
                $checkmsg=0;
                foreach (@inmsg){
                if ($count eq $_) {
                $checkmsg=1;
                }
                }
                print FILE "$line\n" if ($checkmsg ==0);
	        $count++;
            }
            close (FILE);
            &winunlock($filetoopen) if ($OS_USED eq "Nt");
            undef $checkmsg;
            $output .= qq~
              <tr>
                <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>��Ϣɾ��</b></td>
              </tr>
              <tr>
                <td bgcolor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a> ��<a href=$thisprog?action=outbox>$outboxpm</a> ��<a href=$thisprog?action=new>$newpm</a>��<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a></td>
              </tr>
              <tr>
              <td bgcolor=$miscbackone align=center><font color=$fontcolormisc><b>����$inwhere�еĶ���Ϣ�Ѿ�ɾ����</b></td></tr>
            ~;
    }
    else {
        &login("$thisprog?action=loggedin");
    }
    $output .= qq~</table></td></tr></table>~;
    &printmessanger(
        -Title   => "$boardname - ����Ϣ",
        -ToPrint => $output,
        -Version => $versionnumber
    );
sub login {
    local($url) = @_;

    ($postto, $therest) = split(/\?/,$url);
    @pairs = split(/\&/,$therest);
    foreach (@pairs) {
        ($name, $value)=split(/\=/,$_);
        $hiddenvars .= qq~<input type=hidden name="$name" value="$value">\n~;
    }
    $output .= qq~
        <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
	    <form action="$postto" method="post">$hiddenvars
            <font color=$fontcolormisc><b>�����������û����������½</b></font></td></tr>
        <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"></td></tr>
        <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"></td></tr>
        <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ½"></td></form></tr></table></td></tr></table>
    ~;
    $output .= qq~</table></td></tr></table>~;
    &printmessanger(
       -Title   => "$boardname - ����Ϣ",
       -ToPrint => $output,
       -Version => $versionnumber
    );
}
