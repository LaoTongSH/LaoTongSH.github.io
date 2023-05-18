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
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ($inmembername eq "") {
    $inmembername = "客人";
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
	                    　<img src="$imagesurl/images/closedfold.gif" border=0>&nbsp;&nbsp;<a href="$forumsummaryprog">$boardname</a>
	                    <br>
                        　<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>　论坛公告
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
	                if (($membercode ne "ad") && ($membercode ne 'smo') && ($inmembmod ne "yes")) { &error("使用公告&您不是管理员！"); }
	                elsif ($inpassword ne $password) { &error("使用公告&您的密码错误！"); }

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
                        &doend("论坛公告已经被删除");
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
	            &whosonline("$inmembername\t公告栏\tnone\t添加公告\t");
		}
                $output .= qq~
                        <tr>
                        <td bgcolor=$miscbacktwo colspan=2 align=center>
                        <form action="$thisprog" method=post>
			<input type=hidden name="action" value="addannouncement">
			<input type=hidden name="forum" value="$inforum">
	                <font face="$font" color=$fontcolormisc><b>发表论坛公告</b></td>
	                </tr>
	                <tr>
	                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的用户名</font></td>
	                <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername"0></a></td></tr>
	                <tr>
	                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的密码</font></td>
	                <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"0></td></tr>
	                <tr>
	                <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>论坛公告标题</b></font></td>
	                <td bgcolor=$miscbackone valign=middle><input type=text name="announcementtitle" size=60 maxlength=100></td>
	                </tr>
	                <tr>
	                <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>论坛公告内容</b><br>请输入您的论坛公告内容。<p>如果使用了表情字符转换，LB5000 将自动在公告中转换表情字符。</font></td>
	                <td bgcolor=$miscbackone valign=middle><textarea cols=60 rows=10 name="announcementpost"></textarea></td>
	                </tr>
	                <tr>
	                <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	                <input type=Submit  value="提 交" name=Submit onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear">
	                </td></form></tr>
		~;
        }
       elsif ($action eq "addannouncement") {
		$currenttime = time;
#                &getmember("$inmembername");
                if (($membercode ne "ad")&&($membercode ne 'smo') && ($inmembmod ne "yes")) { &error("使用公告&您不是管理员！"); }
                elsif ($inpassword ne $password) { &error("使用公告&您的密码错误！"); }
                if ($inannouncementpost eq "") { &error("使用公告&请输入论坛公告内容！"); }
                if ($inannouncementtitle eq "") { &error("使用公告&请输入论坛公告标题！"); }

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

                &doend("论坛公告已经发表。");
	}
        elsif ($action eq "edit") {
		my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
		$filetoopens = &lockfilename($filetoopens);
		if (!(-e "$filetoopens.lck")) {
       	            &whosonline("$inmembername\t公告栏\tnone\t编辑公告\t");
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
	             <font face="$font" color=$fontcolormisc><b>编辑论坛公告</b></td>
	             </tr>
	             <tr>
	             <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的用户名</font></td>
	             <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername"0></a></td></tr>
	             <tr>
	             <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的密码</font></td>
	             <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"0></td></tr>
	             <tr>
	             <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>论坛公告标题</b></font></td>
	             <td bgcolor=$miscbackone valign=middle><input type=text name="announcementtitle" value="$announcementtitle"size=60 maxlength=100></td>
	             </tr>
	             <tr>
	             <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>论坛公告内容</b><br>请输入您的论坛公告内容。<p>如果使用了表情字符转换，LB5000 将自动在公告中转换表情字符。</font></td>
	             <td bgcolor=$miscbackone valign=middle><textarea cols=60 rows=10 name="announcementpost">$announcementpost</textarea></td>
	             </tr>
	             <tr>
	             <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	             <input type=Submit  value="提 交" name=Submit onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear">
	             </td></form></tr>
		~;
	}
        elsif ($action eq "doedit") {
                $currenttime = time;
#                &getmember("$inmembername");

                if (($membercode ne "ad") &&($membercode ne 'smo')&& ($inmembmod ne "yes")) { &error("使用公告&您不是管理员！"); }
                elsif ($inpassword ne $password) { &error("使用公告&您的密码错误！"); }
                if ($inannouncementpost eq "") { &error("使用公告&请输入论坛公告内容！"); }
                if ($inannouncementtitle eq "") { &error("使用公告&请输入论坛公告标题！"); }
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

                &doend("论坛公告已经被编辑并发表了");
                exit;
	}
        else {
		my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
		$filetoopens = &lockfilename($filetoopens);
		if (!(-e "$filetoopens.lck")) {
	            &whosonline("$inmembername\t公告栏\tnone\t查看公告\t");
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
                        @announcements[0] = "当前没有任何公告\t$dateposted\t请点击添加图标来发布一个公告(必须是管理员)。<br>当你发布一次公告后，本公告就会自动消失，无需你手动删除！";
                }
                foreach $line (@announcements) {
		    ($title, $dateposted, $post, $nameposted) = split(/\t/, $line);
                    $dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
                    $dateposted = &dateformat("$dateposted");

                    $post = &lbcode("$post");
                    $post = &doemoticons("$post");
	            $post = &smilecode("$post");

                 if ($post !~/<blockquote><font face=宋体>代码/isg){
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
		    $nameposted = "本站的默认公告" if (!$nameposted);
		    $output .= qq~
	                 <tr>
	                    <td bgcolor="$postbackcolor" valign=top style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word"><font face="$font" color=$postfontcolor>
	                        $post
	                    </td>
	                 </tr>
	                 <tr>
	                    <td bgcolor="$postbackcolor" valign=middle>
	                     <table width=100% border="0" cellpadding="0" cellspacing="0">
	                        <tr><td align=left>&nbsp;&nbsp;&nbsp;<font face="$font" color=$postfontcolor><b>发布人</b>： $nameposted</font>
	                        </td><td align=right><font face="$font" color=$postfontcolor><b>发布时间</b>： $dateposted</font>&nbsp;&nbsp;&nbsp;
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
              -Title   => "$boardname - 公告",
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
	       <font face="$font" color=$fontcolormisc><b>登陆前请输入管理员的详细信息</b><br>请注意，只有管理员才可以增加、删除、修改论坛公告！</font></td></tr>
	    <tr>
	       <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的用户名</font></td>
	       <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername"0></td></tr>
	    <tr>
	       <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的密码</font></td>
	       <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"0></td></tr>
	    <tr>
	       <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
    ~;
}

sub doend {
    my $action_taken = shift;
    $relocurl = "$boardurl/$thisprog?forum=$inforum";
    $output .= qq~
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>论坛公告</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
            如果你的浏览器没有自动返回论坛，请点击下面的链接直接返回。
            <ul>
            <li><b>$action_taken</b>
            <li><a href="$relocurl">返回论坛公告</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="5; url=$relocurl">
    ~;

    &output(
         -Title   => "$boardname - 公告",
         -ToPrint => $output,
         -Version => $versionnumber
    );
}
