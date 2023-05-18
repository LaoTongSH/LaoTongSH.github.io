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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "code.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                                     # Unbuffer the output
$thisprog = "fav.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$inshow         = $query -> param('show');
$inshow         = &stripMETA("$inshow");
for ('forum','topic','membername','password','action','checked','member') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
srand;
$inforum       = $forum;
$intopic       = $topic;
$inmembername  = $membername;
$inpassword    = $password;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

print header(-charset=>gb2312);
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

    if ($inmembername eq "") {
        $inmembername = "����";
        }
        else {
		&getmember("$inmembername");
		&error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
        }
&badwordfile;

$inmembername =~ s/ /_/g;
$inmembername =~ tr/A-Z/a-z/;
my %Mode = (
    'add'                 =>    \&add,
    'del'                 =>    \&del,
    );
if($Mode{$action}) {
        $Mode{$action}->();
        }
        elsif (($member ne "")&&($action eq "show")) { &list;   }
        else { &error("��ͨ&������ȷ�ķ�ʽ���ʱ�����"); }
    &output(
    -Title   => $boardname,
    -ToPrint => $output,
    -Version => $versionnumber
    );

sub add {

   if (($intopic eq "")&&($inforum eq "")){&error("��������ղ�&û��ָ������ID����̳ID");exit;}
    &getmember("$inmembername");

    if ($userregistered eq "no") { &error("��������ղ�&��û��ע�ᣡ"); exit; }
	elsif ($inpassword ne $password) { &error("��������ղ�&����������."); exit; }
	elsif ($inmembername eq "") { &error("��������ղ�&��û�и����ղ�."); exit; }
	elsif ($inmembername eq "����") { &error("��������ղ�&��û�и����ղ�."); exit; }


    &mischeader("��������ղ�");

    if ($checked eq "yes") {
    my $file = "$lbdir" . "memfav/$inmembername.cgi";
      if (-e $file) {
        open (ENT, $file);
        @toptopic = <ENT>;
        close (ENT);
        open (ENT, ">$file");
        print ENT "$intopic\t$inforum\t\n";
	foreach $topic (@toptopic) {
	    chomp $topic;
	    ($topic,$forum)=split(/\t/,$topic);
	    if (($topic eq $intopic)&&($forum eq $inforum)) {
	    	}else{
	    	print ENT "$topic\t$forum\t\n";
	       }

	}
        close (ENT);
      }
      else {
        open (ENT, ">$file");
        print ENT "$intopic\t$inforum\t\n";
        close (ENT);
      }

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>��������ղسɹ�</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ���������
            <ul>
            <li><a href="fav.cgi?action=show&member=$inmembername">�����ҵ��ղ�</a>
            <li><a href="$forumsprog?forum=$inforum">������̳</a>
            <li><a href="$forumsummaryprog">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;

    } # end if clear to edit
    else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="add">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>�����������û����������������ղ� </b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ½"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end
sub del {

        if (($intopic eq "")&&($inforum eq "")){&error("ɾ�������ղ�&û��ָ������ID����̳ID");exit;}
        &getmember("$inmembername");

        if ($userregistered eq "no") { &error("ɾ�������ղ�&��û��ע�ᣡ"); exit; }
	elsif ($inpassword ne $password) { &error("ɾ�������ղ�&����������."); exit; }
	elsif ($inmembername eq "") { &error("ɾ�������ղ�&��û�и����ղ�."); exit; }
	elsif ($inmembername eq "����") { &error("ɾ�������ղ�&��û�����ղ�."); exit; }

    &mischeader("ɾ�������ղ�");

    if  ($checked eq "yes") {
      my $file = "$lbdir" . "memfav/$inmembername.cgi";
      if (-e $file) {
        open (ENT, $file);
        @toptopic = <ENT>;
        close (ENT);

        open (ENT, ">$file");
	foreach $topic (@toptopic) {
	    chomp $topic;
	    ($topic,$forum)=split(/\t/,$topic);
	    if (($topic ne $intopic)||($forum ne $inforum)) {
	     	print ENT "$topic\t$forum\t\n";
	    }
	}
        close (ENT);
      }

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>ɾ�������ղسɹ�</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ���������
            <ul>
            <li><a href="fav.cgi?action=show&member=$inmembername">�����ҵ��ղ�</a>
            <li><a href="$forumsprog?forum=$inforum">������̳</a>
            <li><a href="$forumsummaryprog">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;

    } # end if clear to edit
    else {

            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="del">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <font color=$fontcolormisc><b>�����������û���������ɾ�������ղ�</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td>
            <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"0></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td>
            <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"0> &nbsp; <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="�� ½"></td></form></tr></table></td></tr></table>
            </table></td></tr></table>
            ~;

             }
} # end

sub list
{
    $member =~ s/ /_/g;
    $member =~ tr/A-Z/a-z/;
    &error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($member =~  m/\//)||($member =~ m/\\/)||($member =~ m/\.\./));
    $member =~ s/\///g;
    $member =~ s/\.\.//g;
    $member =~ s/\\//g;

    if ($member eq ""){&error("�鿴�����ղ�&û��ָ����Ա");}
    if (!(-e "$lbdir" . "$memdir/$member.cgi")){&error("��������ղ�&û�иû�Ա!");}
    &getmember("$inmembername");

        if ($userregistered eq "no") { &error("�鿴�����ղ�&��û��ע�ᣡ"); exit; }
	elsif ($inpassword ne $password) { &error("�鿴�����ղ�&����������."); exit; }
	elsif ($inmembername eq "") { &error("�鿴�����ղ�&��û��Ȩ���鿴���û��ĸ����ղ�."); exit; }
	elsif ($inmembername eq "����") { &error("�鿴�����ղ�&��û��Ȩ���鿴���û��ĸ����ղ�."); exit; }

    $cleartoedit = "no";


    if (($membercode eq "ad") || ($membercode eq 'smo')|| ($member eq $inmembername)) { $cleartoedit = "yes"; }

    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no") { &error("�鿴�����ղ�&�ø����ղ��趨�����У�ֻ�������˿��Կ���"); }


my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\tnone\tnone\t�鿴�����ղ�\t");
}
&title;
$forumgraphic = qq~<a href=$forumsummaryprog><img src=$imagesurl/images/$boardlogo border=0></a>~;
$output .= qq~

           <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
             <tr>
               <td width=30% rowspan=2 valign=top>$forumgraphic
               </td>
               <td valign=top>

          <font color=$fontcolormisc>
          <font color=$fontcolormisc>
	  ��<img src=$imagesurl/images/closedfold.gif width=15 height=11>��<a href=$forumsummaryprog>$boardname</a><br>
          ��<img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>���鿴�����ղ�
          </td>
         </tr>
             </tr>
        </table>
        <br>

<style>
.drb { border: $tablebordercolor solid; border-width: 0px 1px 1px 0px}
</style>
<span id=forum>
<table cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
              <tr><td height=1></td></tr>
              </table>
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
              <tr>
                <td bgcolor=$tablebordercolor width=1 height=24></td>
              <td bgcolor=$titlecolor width=32 align=center><font color=$titlefontcolor><b>״̬</b></td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor width=* align=center><font color=$titlefontcolor><b>������</b> (�������Ϊ���ŷ�ʽ���)</td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor align=center width=80><font color=$titlefontcolor><b>�� ��</b></td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor align=center width=32><font color=$titlefontcolor><b>�ظ�</b></td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor align=center width=32><font color=$titlefontcolor><b>���</b></td>
                <td bgcolor=$tablebordercolor width=1></td>
              <td bgcolor=$titlecolor width=195 align=center><b>������ | �ظ���</b></td>
                <td bgcolor=$tablebordercolor width=1></td>
              </tr>
	      </table>
              <table cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
              <tr><td height=1></td></tr>
              </table>
	~;

    $icon_num = int(rand(10));
    $topcount = 0;
    $filetoopen = "$lbdir" . "memfav/$member.cgi";
    $filetoopen = &stripMETA($filetoopen);
    if (-e $filetoopen) {
    	&winlock($filetoopen);
        open(FILE, "$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        @ontop = <FILE>;
        close(FILE);
        &winunlock($filetoopen);
    }
    else { undef @ontop; }
    $topcount = @ontop;
    $numberofpages = $topcount / $maxthreads;

   if ($topcount > $maxthreads) {
        $showmore = "yes";
        if ($inshow eq "" || $inshow < 0) { $inshow = 0; }
        if ($inshow > 0) { $startarray = $inshow; }
        else { $startarray = 0; }
        $endarray = $inshow + $maxthreads - 1;
        if ($endarray < ($topcount - 1)) { $more = "yes"; }
        elsif (($endarray > ($maxthreads - 1)) && ($more ne "yes")) { $endarray = $topcount -1; }
    }
    else {
        $showmore = "no";
        $startarray = 0;
        $topicpages = qq~<font color=$menufontcolor>���ղ���ֻ��һҳ</font>~;
        $endarray = $topcount -1;
    }

        if ($showmore eq "yes") {
	if ($maxthreads < $topcount) {
	    ($integer,$decimal) = split(/\./,$numberofpages);
	    if ($decimal > 0) { $numberofpages = $integer + 1; }
	    $mypages=$numberofpages;
	    #��ҳ
	    $intshow=$inshow/(12*$maxthreads);
	    ($intshow,$mydecimal) = split(/\./,$intshow);
	    $intshow = $intshow + 1;
	    $preshow=($intshow-1)*12*$maxthreads-$maxthreads;
	    $nextshow=$intshow*12*$maxthreads;
	    $pages=qq~<a href="$thisprog?action=show&member=$member&show=$preshow"><font color=$menufontcolor><b>��</b></font></a> ~ if ($intshow > 1);
	    if ($numberofpages > ($intshow*12)){
		$numberofpages=($intshow*12);
		$isnext=qq~<a href="$thisprog?action=show&member=$member&show=$nextshow"><font color=$menufontcolor><b>��</b></font></a> ~;
	    }
	    $pagestart = ($intshow-1)*12*$maxthreads;
            $counter = ($intshow-1)*12;
            while ($numberofpages > $counter) {
		$counter++;
		if ($inshow ne $pagestart) { $pages .= qq~<a href="$thisprog?action=show&member=$member&show=$pagestart"><font color=$menufontcolor><b>$counter</b></font></a> ~; }
		else { $pages .= qq~<font color=$fonthighlight><b>$counter</b></font> ~; }
		$pagestart = $pagestart + $maxthreads;
	    }
	    $pages .=  $isnext;
	    #��ҳend
	}
	$topicpages = qq~<font color=$menufontcolor><b>���ղ������� <font color=$fonthighlight>$mypages</font> ҳ</b> [ $pages ]~;
    }
    if ($topcount > 0) {

    for ($i=$startarray;$i<=$endarray;$i++) {
      	$id=$ontop[$i];
      	chop $id;
      	($id,$inforum)=split(/\t/,$id);
	my $file = "$lbdir" . "forum$inforum/$id.pl";
	open (TMP, "$file");
	(my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $lastpostdate, my $posticon1, my $inposttemp) = split (/\t/,<TMP>);
	close (TMP);
 	$topictitle =~ s/^����������//;

	my $file1 = "$lbdir" . "forum$inforum/$id.thd.cgi";
	if (($topictitle eq "")||($startedby eq "")||($startedpostdate eq "")||($threadposts eq "")){
	open (TMP1, "$file1");
	my @tmp = <TMP1>;
	close (TMP);

	my $tmp = @tmp;
	$tmp --;
	my $tmp1 = $tmp[-1];
        $tmp1 =~ s/[\n\r]//isg;
	my $tmp2 = $tmp[0];
        $tmp2 =~ s/[\n\r]//isg;
	(my $membername, $topictitle, my $postipaddress, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/,$tmp2);
	(my $membername1, my $topictitle1, my $postipaddress1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, $posticon1) = split(/\t/,$tmp1);
 	$topictitle =~ s/^����������//;
	$membername1 = "" if ($tmp eq 0);
	$threadviews =$tmp * 8 if (($threadviews eq "")||($threadviews > 10000));
	$postdate1 = $lastpostdate if ($lastpostdate ne "");
	$inposttemp = $post1;
	$inposttemp =~ s/\[������������(.+?)�༭\]\n//isg;
	$inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	$inposttemp =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]//isg;
	$inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2\n/isg;
	$inposttemp = &doemoticons("$inposttemp");
	$inposttemp =~ s/ \<img\s*(.*?)\s*\>//isg;
	$inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)//isg;
	$inposttemp =~ s/( )+$//isg;
	$inposttemp =~ s/^( )+//isg;
	$inposttemp =~ s/<(.|\n)+?>//g;
	$inposttemp =~ s/\[.+?\]//g;
	$inposttemp =~ s/[\a\f\n\e\0\r\t\n]//g;

	    $posticon =~ s/\s//isg;
	    if ($posticon =~/<br>/i) {
      		$posticon=~s/<br>/\t/ig;
      		@temppoll = split(/\t/, $posticon);
      		$temppoll = @temppoll;
      		if ($temppoll >1) {
      		    $posticon1 = "<br>";
      		}
      		else {
      		    $posticon1 = "";
      		}
	    }
	    $inposttemp = &lbhz($inposttemp,$maxsavepost);
            $posticon = "<br>" if ($posticon =~/<br>/i);

	$rr = ("$inforum\t$id\t$topictitle\t$topicdescription\t$threadstate\t$tmp\t$threadviews\t$membername\t$postdate\t$membername1\t$postdate1\t$posticon1\t$inposttemp\t\n");
        }else{
   	    $threadviews = ($tmp+1) * 8 if ($threadviews eq "");
   	    $threadviews = 9999 if ($threadviews > 9999);
            $posticon1 = "<br>" if ($posticon1 =~/<br>/i);
	    $topictitle =~ s/^����������//;
            $rr = ("$inforum\t$id\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon1\t$inposttemp\t\n");
        }
	if ($topictitle ne "") {push (@toptopic, $rr);}
    }
  }
  else { undef @toptopic; }
        $topiccount = 0;
        foreach $topic (@toptopic) {
	    chomp $topic;
            ($inforum,$topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp) = split(/\t/,$topic);
       	    next if ($topicid eq "");
            if ($posticon ne "") {
            	$poll=0;
            	if ($posticon =~/<br>/i){
                    $posticon = int(rand(23));
    		    $posticon = "0$posticon" if ($posticon<10);
		    $posticon = qq~<img src=$imagesurl/posticons/$posticon.gif $defaultsmilewidth $defaultsmileheight border=0 alt="���ŷ�ʽ���">~;
            	}
            	else{
            	    $posticon = qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight border=0 alt="���ŷ�ʽ���">~;
            	}
            }
	    else {
    		$posticon = int(rand(23));
    		$posticon = "0$posticon" if ($posticon<10);
		$posticon = qq~<img src=$imagesurl/posticons/$posticon.gif $defaultsmilewidth $defaultsmileheight border=0 alt="���ŷ�ʽ���">~;
	    }
	    if ($badwords) {
		@pairs = split(/\&/,$badwords);
		foreach (@pairs) {
		    ($bad, $good) = split(/=/,$_);
		    chomp $good;
		    $topictitle =~ s/$bad/$good/isg;
		}
	    }
	    $lastpostdatetemp=$lastpostdate;

	    $lastpostdate=$lastpostdatetemp;
            $topcount = $threadposts + 1;
            $topcount = $topcount / $maxtopics;
	    $counter = 0;
            if ($topcount > $maxtopics) {
		if ($maxtopics < $topcount) {
		    ($integer,$decimal) = split(/\./,$topcount);
		    if ($decimal > 0) { $topcount = $integer + 1; }
		    $pagestart = 0;
		    while ($topcount > $counter) {
			$counter++;
			$threadpages .= qq~<a href=$threadprog?forum=$inforum&topic=$topicid&start=$pagestart><font color=$fonthighlight><b>$counter</b></font></a> ~;
			$pagestart = $pagestart + $maxtopics;
		    }
		}
		$pagestoshow = qq~<font color=$forumfontcolor>����[�� $threadpages ҳ]</font>~;
	    }





	    if ($lastpostdate ne "") {
		$lastpostdate = $lastpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
		$longdate = &dateformatshort("$lastpostdate");
		$lastpostdate = qq~<font color=$fontcolormisc>$longdate</font>~;
	    }
	    else {
		$lastpostdate = qq~<font color=$fontcolormisc>û��~;
		$lastpoststamp = "";
	    }
	    $startedpostdate = $startedpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
	    $startedlongdate = &shortdate("$startedpostdate");
	    $startedshorttime = &shorttime("$startedpostdate");
	    $startedpostdate = qq~<font color=$fontcolormisc>$startedlongdate</font>~;
	    $screenmode   = $query->cookie("screenmode");
	    $topictitlemax = 54;
	    $topictitlemax = 84 if (($screenmode >=9)||($tablewidth > 770));

	    $posttemp = "(������)" if ($posttemp eq "");
	    $topictitletemp=&lbhz("$topictitle",$topictitlemax);
	    $topictitle = qq~<ACRONYM TITLE="���ظ�ժҪ��\n\n$posttemp"><a href=$threadprog?forum=$inforum&topic=$topicid target=_blank>$topictitletemp</a></ACRONYM>~;
	    $startedbyfilename = $startedby;
	    $startedbyfilename =~ s/ /\_/isg;
	    $startedbyfilename =~ tr/A-Z/a-z/;

	    if ($lastposter) {
		$lastposterfilename = $lastposter;
		$lastposterfilename =~ s/ /\_/isg;
		$lastposter = qq~<a href=$profileprog?action=show&member=$lastposterfilename>$lastposter</a>~;
	    }
	    else {$lastposter = qq~<font color=$fontcolormisc>--------</a>~;}

	    $topicdescriptiontemp = $topicdescription;

	    $topicdescriptiontemp =~s/\s*(.*?)\s*\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/$3/isg;
	    $topicdescriptiontemp =~s/\<\/a\>//isg;

	    if (length($topicdescriptiontemp) > ($topictitlemax-4)) {
		$topicdescriptiontemp=&lbhz("$topicdescriptiontemp",$topictitlemax-4);
		$topicdescription =~s/\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/\<a $1\>$topicdescriptiontemp\<\/a\>/isg;
	    }

	    if ($topicdescription) { $topicdescription = qq~<br>����-=> $topicdescription~; }
	    if (-e "$lbdir/forum$inforum/rate$topicid.file.pl") {
		require "$lbdir/forum$inforum/rate$topicid.file.pl";
		$average = int($rates / $votes);
	        if ($average > 0) {$ratestar =  qq(<img src=$imagesurl/images/1star.gif width=14 alt="̫����">);}
	        if ($average > 1) {$ratestar =  qq(<img src=$imagesurl/images/2star.gif width=14 alt="�е��">);}
	        if ($average > 2) {$ratestar =  qq(<img src=$imagesurl/images/3star.gif width=14 alt="һ����">);}
	        if ($average > 3) {$ratestar =  qq(<img src=$imagesurl/images/4star.gif width=14 alt="ͦ����">);}
	        if ($average > 4) {$ratestar =  qq(<img src=$imagesurl/images/5star.gif width=14 alt="�ر��">);}
	    } else {
	        $ratestar =  qq(<img src=$imagesurl/images/norate.gif width=0 height=0 alt="û��ͶƱ���ּ�¼">);
	    }

	    if ($ratings eq "") { $ratings2 = ""; }
	    else  { $ratings2 = qq~<td bgcolor=$forumcolortwo align=center width=27 class=drb><font color=$forumfontcolor>$ratestar</font></td>~; }

	    if ($counter == 0) { $pagestoshowtemp1 = 0; }
	    else { $pagestoshowtemp1 =7;}
	    $totlelength = $counter*3.3 + $pagestoshowtemp1 + length($topictitletemp) + 4; #���������ܳ���
	    undef $pagestoshowtemp1;



      	   $admini = qq~
		        <tr><td align=right><font color=$titlecolor>|<a href=$forumsprog?forum=$inforum target=_blank><font color=$titlecolor>������̳[forum$inforum]</font></a>|<a href=fav.cgi?action=del&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>ɾ��</font></a>|<a href=fav.cgi?action=add&forum=$inforum&topic=$topicid><font color=$titlecolor>����</font></a>|</font>&nbsp;</td></tr>
		    ~;

             $topicicon = "<img src=$imagesurl/images/topicnonew.gif width=14 border=0>";


	    if ($threadstate eq "closed") {
		$topicicon = "<img src=$imagesurl/images/topiclocked$icon_num.gif width=14 border=0>";
	    }
	    elsif ($threadstate eq "poll") {
		$topicicon = "<img src=$imagesurl/images/closedb.gif width=13 border=0>";
	    }
	    elsif ($threadstate eq "pollclosed") {
		$topicicon = "<img src=$imagesurl/images/closedb1.gif width=13 border=0>";
	    }

	    $topictitle=$topictitle."<BR>" if ($totlelength > $topictitlemax+5);
	    $output .=qq~
		<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
		<tr>
                <td bgcolor=$tablebordercolor width=1 height=24></td>
                  <td bgcolor=$forumcolorone align=center width=32 class=drb><font color=$forumfontcolor><a href=topic.cgi?forum=$inforum&topic=$topicid target=_blank>$topicicon</a></td>
                  <td bgcolor=$forumcolortwo width=* class=drb><font color=$forumfontcolor><img src="" width=0 height=4><BR>
                  <table cellpadding=0 cellspacing=0 width=100%><tr><td>&nbsp;<a href=view.cgi?forum=$inforum&topic=$topicid target=_blank>$posticon</a>&nbsp;$topictitle$pagestoshow$topicdescription</font></td></tr>$admini</table>
                  <img src="" width=0 height=4><BR></td>
                  <td bgcolor=$forumcolorone align=center width=80 class=drb><font color=$forumfontcolor><a href=$profileprog?action=show&member=$startedbyfilename>$startedby</a></font></td>
                  <td bgcolor=$forumcolortwo align=center width=32 class=drb><font color=$forumfontcolor>$threadposts</font></td>
                  <td bgcolor=$forumcolortwo align=center width=32 class=drb><font color=$forumfontcolor>$threadviews</a></font></td>
                  <td bgcolor=$forumcolorone width=195 class=drb><font color=$fonthighlight>&nbsp;$lastpostdate | $lastposter<br></td>
		  $ratings2
                </tr>
                </table>

	    ~;
	    $pagestoshow = undef;
	    $threadpages = undef;
	    $topiccount++;
	}
        $output .= qq~
        </tr></table></td>
        </tr></table></span>
        <table cellpadding=0 cellspacing=2 border=0 width=$tablewidth align=center>
	<tr height=4></tr>
        <tr>
        <td>$topicpages</td>
                   </tr></table>
            </tr>
            </table>
	    <br>
        ~;


}

sub accessneeded {
    $output .= qq~
        <form action="forums.cgi" method=post>
        <input type=hidden name="forum" value="$inforum">
        <input type=hidden name="action" value="accessrequired">
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
        <tr><td>
	<table cellpadding=3 cellspacing=1 border=0 width=100%>
        <tr><td bgcolor=$miscbacktwo colspan=2 align=center><font color=$fontcolormisc><b>�������������ơ������½˽����̳</b></font></td></tr>
        <tr><td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc><br>ÿ�������ֻ��Ҫ��½һ�Σ�ͬʱ��ȷ�����Ѿ������������ Cookies ѡ�<br>ֻ�о�������Ա���ɵ��û��ſ��Է��ʸ���̳������㲻�ܵ�½������ϵ����Ա��<br><br></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td>
        <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername">�� <a href=$registerprog><font color=$fontcolormisc>��û��ע�᣿</font></a></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td>
        <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword">�� <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">�������� ?</a></font></td></tr>
        <tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc>��������̳��������</font></td>
        <td bgcolor=$miscbackone><input type=password name="forumpassword" value="$forumpassword">�� <font color=$fontcolormisc>������Ѿ���Ȩ�������룬�򲻱���������.</font></td></tr>
        <tr height=28><td bgcolor=$miscbackone colspan=2 align=center><font color=$fontcolormisc>�����ȷ����������ȷ�����룬�������޷���½�Ļ�����ˢ�´�ҳ��(�����ٴΰ���½��һ��)��</td></tr>
        <tr>
        <td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="��  ½"></td></tr></table></td></tr></table>
       </form>
    ~;

    &output(
     -Title   => "$forumname",
     -ToPrint => $output,
     -Version => $versionnumber
    );
}