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
require "code.cgi";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                                     # Unbuffer the output
$thisprog = "announcements.cgi";
$query = new LBCGI;

for ('membername','password','announcementtitle','announcementpost','action','checked','number', 'forum') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput($tp);
    ${$_} = $tp;
}
$inmembername           = $membername;
$inpassword             = $password;
$inannouncementtitle    = $announcementtitle;
$inannouncementpost     = $announcementpost;
$inforum		= $forum;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ($inmembername eq "") {
    $inmembername = "����";
}
&getmember("$inmembername");
&getforum($inforum);
        &moderator;
        print header(-charset=>gb2312);
        &title;
    if ($forumgraphic) { $forumgraphic = qq~<a href=$forumsprog?forum=$inforum><img src=$imagesurl/images/$forumgraphic border=0></a>~; }
        else { $forumgraphic = qq~<a href=$forumsummaryprog><img src=$imagesurl/images/$boardlogo border=0></a>~; }
        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
	                <tr>
	                   <td width=30% rowspan=2 valign=top>
	                    $forumgraphic
	                   </td>
	                   <td valign=top align=left>
	                    <font face="$font" color=$fontcolormisc>
	                    ��<img src="$imagesurl/images/closedfold.gif" border=0>&nbsp;&nbsp;<a href="$forumsummaryprog">$boardname</a>
	                    <br>
                        ��<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>����̳����
	                </tr>
                  </table>
	           <p>
	        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
	                <tr>
	                    <td>
	                    <table cellpadding=3 cellspacing=1 border=0 width=100% style="TABLE-LAYOUT: fixed">
	~;
	if ($action eq "delete") {
	        if ($checked eq "yes") {
#	                &getmember("$inmembername");
	                if (($membercode ne "ad") && ($membercode ne 'smo') && ($inmembmod ne "yes")) { &error("ʹ�ù���&�����ǹ���Ա��"); }
	                elsif ($inpassword ne $password) { &error("ʹ�ù���&�����������"); }

	                $filetoopen = "$lbdir" . "data/news$inforum.cgi";
                        $filetoopen = &stripMETA($filetoopen);
	                open(FILE, "$filetoopen");
	                @announcements = <FILE>;
	                close(FILE);

	                $count = 0;

	                $filetoopen = "$lbdir" . "data/news$inforum.cgi";
                        $filetoopen = &stripMETA($filetoopen);
		        &winlock($filetoopen) if ($OS_USED eq "Nt");
	                open(FILE, ">$filetoopen");
	                flock (FILE, 2) if ($OS_USED eq "Unix");
	                foreach $line (@announcements) {
			    chomp $line;
			    if ($count ne $number) {
                                print FILE "$line\n";
                            }
	                    $count++;
	                }
	                close(FILE);
		        &winunlock($filetoopen) if ($OS_USED eq "Nt");
                        &doend("��̳�����Ѿ���ɾ��");
	                exit;
		}
		else {
	        	&login("$thisprog?action=delete&number=$number&checked=yes&forum=$inforum");
	        }
	}
        elsif ($action eq "add") {
		my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    		$filetoopens = &lockfilename($filetoopens);
		if (!(-e "$filetoopens.lck")) {
	            &whosonline("$inmembername\t������\tnone\t��ӹ���\t");
		}
                $output .= qq~
                        <tr>
                        <td bgcolor=$miscbacktwo colspan=2 align=center>
                        <form action="$thisprog" method=post>
			<input type=hidden name="action" value="addannouncement">
			<input type=hidden name="forum" value="$inforum">
	                <font face="$font" color=$fontcolormisc><b>������̳����</b></td>
	                </tr>
	                <tr>
	                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>�����������û���</font></td>
	                <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername"0></a></td></tr>
	                <tr>
	                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>��������������</font></td>
	                <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"0></td></tr>
	                <tr>
	                <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳�������</b></font></td>
	                <td bgcolor=$miscbackone valign=middle><input type=text name="announcementtitle" size=60 maxlength=100></td>
	                </tr>
	                <tr>
	                <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳��������</b><br>������������̳�������ݡ�<p>���ʹ���˱����ַ�ת����LB5000 ���Զ��ڹ�����ת�������ַ���</font></td>
	                <td bgcolor=$miscbackone valign=middle><textarea cols=60 rows=10 name="announcementpost"></textarea></td>
	                </tr>
	                <tr>
	                <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	                <input type=Submit  value="�� ��" name=Submit onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear">
	                </td></form></tr>
		~;
        }
       elsif ($action eq "addannouncement") {
		$currenttime = time;
#                &getmember("$inmembername");
                if (($membercode ne "ad")&&($membercode ne 'smo') && ($inmembmod ne "yes")) { &error("ʹ�ù���&�����ǹ���Ա��"); }
                elsif ($inpassword ne $password) { &error("ʹ�ù���&�����������"); }
                if ($inannouncementpost eq "") { &error("ʹ�ù���&��������̳�������ݣ�"); }
                if ($inannouncementtitle eq "") { &error("ʹ�ù���&��������̳������⣡"); }

                $filetoopen = "$lbdir" . "data/news$inforum.cgi";
                $filetoopen = &stripMETA($filetoopen);
                open(FILE, "$filetoopen");
                @announcements = <FILE>;
                close(FILE);

                $newline = "$inannouncementtitle\t$currenttime\t$inannouncementpost\t$inmembername\t";
                chomp $newline;

                $filetoopen = "$lbdir" . "data/news$inforum.cgi";
                $filetoopen = &stripMETA($filetoopen);
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
	        open(FILE, ">$filetoopen");
	        flock(FILE, 2) if ($OS_USED eq "Unix");
	        print FILE "$newline\n";
	        foreach $line (@announcements) {
	             chomp $line;
	             print FILE "$line\n";
	        }
	        close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                &doend("��̳�����Ѿ�����");
	}
        elsif ($action eq "edit") {
		my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
		$filetoopens = &lockfilename($filetoopens);
		if (!(-e "$filetoopens.lck")) {
       	            &whosonline("$inmembername\t������\tnone\t�༭����\t");
		}

                $filetoopen = "$lbdir" . "data/news$inforum.cgi";
                $filetoopen = &stripMETA($filetoopen);
                open(FILE, "$filetoopen");
                @announcements = <FILE>;
                close(FILE);
                $count = 0;

                foreach (@announcements) {
                        if ($count eq $number) {
                                ($announcementtitle, $notneeded, $announcementpost,$notneeded) = split(/\t/,$_);
                        }
                        $count++;
                }

                $announcementpost =~ s/\<p\>/\n\n/g;
                $announcementpost =~ s/\<br\>/\n/g;
		$output .= qq~
	             <tr>
	             <td bgcolor=$miscbacktwo colspan=2 align=center>
	             <form action="$thisprog" method=post>
                     <input type=hidden name="forum" value="$inforum">
                     <input type=hidden name="action" value="doedit">
                     <input type=hidden name="number" value="$number">
	             <font face="$font" color=$fontcolormisc><b>�༭��̳����</b></td>
	             </tr>
	             <tr>
	             <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>�����������û���</font></td>
	             <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername"0></a></td></tr>
	             <tr>
	             <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>��������������</font></td>
	             <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"0></td></tr>
	             <tr>
	             <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳�������</b></font></td>
	             <td bgcolor=$miscbackone valign=middle><input type=text name="announcementtitle" value="$announcementtitle"size=60 maxlength=100></td>
	             </tr>
	             <tr>
	             <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳��������</b><br>������������̳�������ݡ�<p>���ʹ���˱����ַ�ת����LB5000 ���Զ��ڹ�����ת�������ַ���</font></td>
	             <td bgcolor=$miscbackone valign=middle><textarea cols=60 rows=10 name="announcementpost">$announcementpost</textarea></td>
	             </tr>
	             <tr>
	             <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	             <input type=Submit  value="�� ��" name=Submit onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear">
	             </td></form></tr>
		~;
	}
        elsif ($action eq "doedit") {
                $currenttime = time;
#                &getmember("$inmembername");

                if (($membercode ne "ad") &&($membercode ne 'smo')&& ($inmembmod ne "yes")) { &error("ʹ�ù���&�����ǹ���Ա��"); }
                elsif ($inpassword ne $password) { &error("ʹ�ù���&�����������"); }
                if ($inannouncementpost eq "") { &error("ʹ�ù���&��������̳�������ݣ�"); }
                if ($inannouncementtitle eq "") { &error("ʹ�ù���&��������̳������⣡"); }
                $filetoopen = "$lbdir" . "data/news$inforum.cgi";
                $filetoopen = &stripMETA($filetoopen);
	        open(FILE, "$filetoopen") ;
	        @announcements = <FILE>;
	        close(FILE);

		$count = 0;
                $newline = "$inannouncementtitle\t$currenttime\t$inannouncementpost\t$inmembername\t";
                chomp $newline;

                $filetoopen = "$lbdir" . "data/news$inforum.cgi";
                $filetoopen = &stripMETA($filetoopen);
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, ">$filetoopen");
                flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $line (@announcements) {
                        chomp $line;
                        if ($count eq $number) {
                                print FILE "$newline\n";
                        }
                        else {
                                print FILE "$line\n";
                        }
                        $count++;
                }
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                &doend("��̳�����Ѿ����༭��������");
                exit;
	}
        else {
		my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
		$filetoopens = &lockfilename($filetoopens);
		if (!(-e "$filetoopens.lck")) {
	            &whosonline("$inmembername\t������\tnone\t�鿴����\t");
		}
                $filetoopen = "$lbdir" . "data/news$inforum.cgi";
                $filetoopen = &stripMETA($filetoopen);
                open(FILE, "$filetoopen");
                @announcements = <FILE>;
                close(FILE);
                $postcountcheck = 0;
                $totals = @announcements;
                if ($totals eq "0") {
                        $dateposted = time;
                        @announcements[0] = "��ǰû���κι���\t$dateposted\t�������ͼ��������һ������(�����ǹ���Ա)��<br>���㷢��һ�ι���󣬱�����ͻ��Զ���ʧ���������ֶ�ɾ����";
                }
                foreach $line (@announcements) {
		    ($title, $dateposted, $post, $nameposted) = split(/\t/, $line);
                    $dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
                    $dateposted = &dateformat("$dateposted");

                    $post = &lbcode("$post");
                    $post = &doemoticons("$post");
	            $post = &smilecode("$post");

                 if ($post !~/<blockquote><font face=����>����/isg){
                    $post =~ s/&lt\;/\</g;
                    $post =~ s/&gt\;/\>/g;
                    $post =~ s/&quot\;/\"/g;
                    $post =~ s/\&amp\;/\&/g;
                  }




                    if ($count eq "1") {
			$postbackcolor = "$postcolorone";
	                $postfontcolor = "$postfontcolorone";
	                $count++;
	            }
	            else {
	                $postbackcolor = "$postcolortwo";
	                $postfontcolor = "$postfontcolortwo";
	                $count = 1;
	            }
                    $post = qq~<p><blockquote>$post</blockquote><p>~;
                    $adminadd = qq~<a href="$thisprog?action=add&forum=$inforum"><img src="$imagesurl/images/a_add.gif" border=0"></a>~;
                    $admindelete = qq~<a href="$thisprog?action=delete&number=$postcountcheck&forum=$inforum"><img src="$imagesurl/images/a_delete.gif" border=0"></a>~;
                    $adminedit = qq~<a href="$thisprog?action=edit&number=$postcountcheck&forum=$inforum"><img src="$imagesurl/images/a_edit.gif" border=0"></a>~;

#		    &getmember("$inmembername");
		    $output .= qq~
	                  <tr>
	                  <td bgcolor=$titlecolor align=center valign=top><font face="$font" color=$titlefontcolor><b>>> $title <<</b></td></tr>
		    ~;
		    if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
			  $output .= qq~
	                      	<tr>
	                      	    <td bgcolor=$postbackcolor align=left>$admindelete &nbsp; $adminedit &nbsp; $adminadd</td>
	                       	</tr>
			  ~;
		    }
		    $nameposted = "��վ��Ĭ�Ϲ���" if (!$nameposted);
		    $output .= qq~
	                 <tr>
	                    <td bgcolor="$postbackcolor" valign=top style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word"><font face="$font" color=$postfontcolor>
	                        $post
	                    </td>
	                 </tr>
	                 <tr>
	                    <td bgcolor="$postbackcolor" valign=middle>
	                     <table width=100% border="0" cellpadding="0" cellspacing="0">
	                        <tr><td align=left>&nbsp;&nbsp;&nbsp;<font face="$font" color=$postfontcolor><b>������</b>�� $nameposted</font>
	                        </td><td align=right><font face="$font" color=$postfontcolor><b>����ʱ��</b>�� $dateposted</font>&nbsp;&nbsp;&nbsp;
	                        </tr>
	                        </table>
	                        </td>
	                        </font>
	                        </tr>

	              ~;
		      $postcountcheck++;
	        }
	}
        $output .= qq~</table></td></tr></table>~;
        &output(
              -Title   => "$boardname - ����",
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
        <form action="$postto" method="post">
	    <tr>
	      <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	       $hiddenvars
	       <font face="$font" color=$fontcolormisc><b>��½ǰ���������Ա����ϸ��Ϣ</b><br>��ע�⣬ֻ�й���Ա�ſ������ӡ�ɾ�����޸���̳���棡</font></td></tr>
	    <tr>
	       <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>�����������û���</font></td>
	       <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername"0></td></tr>
	    <tr>
	       <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>��������������</font></td>
	       <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"0></td></tr>
	    <tr>
	       <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="�� ½"></td></form></tr></table></td></tr></table>
    ~;
}

sub doend {
    my $action_taken = shift;
    $relocurl = "$boardurl/$thisprog?forum=$inforum";
    $output .= qq~
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>��̳����</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
            �����������û���Զ�������̳���������������ֱ�ӷ��ء�
            <ul>
            <li><b>$action_taken</b>
            <li><a href="$relocurl">������̳����</a>
            <li><a href="$forumsummaryprog">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="5; url=$relocurl">
    ~;

    &output(
         -Title   => "$boardname - ����",
         -ToPrint => $output,
         -Version => $versionnumber
    );
}
