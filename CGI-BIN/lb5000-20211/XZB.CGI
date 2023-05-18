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
#            http://mail@17do.com/      大家一起邮
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
require "data/boardinfo.cgi";
require "code.cgi";
require "data/progs.cgi";
require "data/styles.cgi";
require "lbmail.lib.pl";
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "postjs.cgi";
$|++;                        # Unbuffer the output
$thisprog = "xzb.cgi";
$query = new LBCGI;
&ipbanned; #封杀一些 ip


for ('forum','membername','password','action','inpost','message','id') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inforum       = $forum;
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));
$inmembername  = $membername;
$inpassword    = $password;
$currenttime   = time;
$postipaddress = "$ENV{'REMOTE_ADDR'}=$ENV{'HTTP_X_FORWARDED_FOR'}";

$inselectstyle   = $query->cookie("selectstyle");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
    if ($inmembername eq "") {
        $inmembername = "客人";
    }
    &getmember("$inmembername");

    if ($mainonoff == 1) { &InMaintenance; }
    print header(-charset=>gb2312);

    $helpurl = &helpfiles("阅读标记");
    $helpurl = qq~$helpurl<img src=$imagesurl/images/help_b.gif border=0></a>~;

    my %Mode = (
    'new'	=>	\&newthread,
    'addnew'	=>	\&addnewthread,
    'view'	=>	\&view,
    'del'	=>	\&del,
    );

    if($Mode{$action}) {
        $Mode{$action}->();
    }
    else { &error("普通&请以正确的方式访问本程序！"); }

    &output(
	-Title   => "$boardname - 在$forumname内发小字报",
	-ToPrint => $output,
	-Version => $versionnumber
    );

sub newthread {
#    &getmember("$inmembername");

    &getforum("$inforum");
    if (($privateforum eq "yes")||($xzbopen eq "no")||($startnewthreads eq "no")){
    	&error("张贴小字报&本论坛不允许张贴小字报!");
    	}

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t$forumname\tnone\t张贴小字报\t") if ($privateforum ne "yes");
    &whosonline("$inmembername\t$forumname(密)\tnone\t张贴新的保密小字报\t") if ($privateforum eq "yes");
}

    &mischeader("张贴小字报");



            $startthreads = "任何注册会员(除坛主和版主)均可以张贴！";

    	$output .= qq~
                <form action="$thisprog" method=post name="FORM" >
                <input type=hidden name="action" value="addnew">
                <input type=hidden name="forum" value="$inforum">
        	<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            	<tr><td>
                <table cellpadding=3 cellspacing=1 border=0 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2><font color=$titlefontcolor><b>谁可以张贴小字报？</b> $startthreads</td>
                </tr>
                <tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>用户名</b></font></td>
                <td bgcolor=$miscbackone>　<input type=text name="membername" value="$inmembername">　 <font color=$fontcolormisc><a href="$registerprog">您没有注册？</a></font></td>
                </tr><tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>密　码</b></font></td>
                <td bgcolor=$miscbackone>　<input type=password name="password" value="$inpassword">　 <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td>
                </tr>
		<tr>
		<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>小字报标题(最大 80 字)</b></td>
		<td bgcolor=$miscbackone>
		　<input type="text" maxlength="80" name=inpost onkeydown=ctlent() value="$inpost" size=80><br>

		</td></tr>
		<tr>
		<td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>小字报内容</b><p>
		 在此论坛中：<li>HTML 标签: <b>不可用</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LB5000 标签</a>: <b>可用</b>
		</td>
		<td bgcolor=$miscbacktwo valign=top>
		<b>　　每小时一贴，一旦发布可以免费宣传48小时</b><br>　
		<TEXTAREA cols=58 name=message rows=6 wrap=soft onkeydown=ctlent()>$message</TEXTAREA>
		</td>
		</tr>
		<tr>
                <td bgcolor=$miscbacktwo colspan=2 align=center>
                <input type=Submit value="发 布" name=Submit"  onClick="return clckcntr();">　　　<input type="reset" name="Clear" value="清 除">
                </td></form></tr>
            </table>
        </tr></td></table>
        ~;
}

sub addnewthread {

#    &getmember("$inmembername");


    if    ($userregistered eq "no")     { &error("张贴小字报&您没有注册！"); }
    elsif ($inpassword ne $password)    { &error("张贴小字报&您的密码错误！"); }
    elsif ($membercode eq "banned")     { &error("张贴小字报&您被禁止发言！"); }
    elsif ($inpost eq "")               { &error("张贴小字报&必须输入标题！"); }
    elsif (length($inpost) > 82)        { &error("发表新投票&标题过长！"); }
    else  {
        &getforum("$inforum");
if (($privateforum eq "yes")||($xzbopen eq "no")||($startnewthreads eq "no")){
    	&error("张贴小字报&本论坛不允许张贴小字报!");
    	}

        $dirtoopen = "$lbdir" . "boarddata";
        open (DIR, "<$dirtoopen/xzb$inforum.cgi");
        @xzbdata = <DIR>;
        close (DIR);
        chomp(@xzbdata);
        $sizexzb=@xzbdata;
        $currenttime = time;
        if (($membercode eq "ad") ||($membercode eq 'smo')|| ($inmembmod eq "yes")) {
           &error("张贴小字报&斑竹和坛主不得参与,谢谢合作！");
        }

	($tmp, $tmp,$tmp,$tmp,$lastpost)=split(/\t/,$xzbdata[0]);
	$lastpost = ($lastpost + 3600);

	if ($lastpost > $currenttime)  {
           &error("张贴小字报&这个小时已经有人发表过一次小字报了，请过一个小时继续！");
	}

        $inpost=~s/</&lt;/sg;
        $inpost=~s/>/&gt;/sg;
        $sizexzb=48 if ($sizexzb >48);
        $write="＃—＃—·\t$inpost\t$inmembername\t$message\t$currenttime\t";
        @newxzb=($write,@xzbdata);
        open(DIR,">$dirtoopen/xzb$inforum.cgi");
        for ($i=0;$i<=$sizexzb;$i++){
             	print DIR "$newxzb[$i]\n";
        }

        &mischeader("新小字报张贴成功");

            	$relocurl = "$forumsprog?forum=$inforum";

        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>谢谢！您的新小字报已经张贴成功！</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            如果浏览器没有自动返回，请点击下面的链接！
            <ul>
            <li><a href="$forumsprog?forum=$inforum">返回论坛</a>
            <li><a href="$forumsummaryprog">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;

    }
}



sub view {
&error("老大你别黑我的程序阿!") if (($id eq "")||($inforum eq ""));
	$dirtoopen = "$lbdir" . "boarddata";
	open (DIR, "<$dirtoopen/xzb$inforum.cgi");
        @xzbdata = <DIR>;
        close (DIR);
        chomp(@xzbdata);
        &getforum("$inforum");
        $xzbdata[$id] =~ s/^＃—＃—·\t//isg;
        ($title,$postid,$msg,$posttime)=split(/\t/,$xzbdata[$id]);

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t$forumname\tnone\t阅读小字报\t") if ($privateforum ne "yes");
        &whosonline("$inmembername\t$forumname(密)\tnone\t阅读保密小字报\t") if ($privateforum eq "yes");
}

#       &getmember("$inmembername");
	$dateposted = $posttime + ($timedifferencevalue*3600) + ($timezone*3600);
        $dateposted = &dateformat("$dateposted");
        $msg = &lbcode("$msg");
       $admindelete=qq~
       <a href=xzb.cgi?action=del&forum=$inforum&id=$id>删除</a>
       ~;
	$output=qq~
	<html><body><head>
	<title>阅读小字报</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline 	}
		A:link 	  {	text-decoration: none;}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}

</style>
	</head>
	<table cellpadding=0 cellspacing=0 border=0 width=97% bgcolor=#000000 align=center>
	                <tr>
	                    <td>
	                    <table cellpadding=3 cellspacing=1 border=0 width=100% style="TABLE-LAYOUT: fixed">
	~;




	$output .= qq~
	                  <tr>
	                  <td bgcolor=$titlecolor align=center valign=top><font face="$font" color=$titlefontcolor><b>>> $title <<</b></td></tr>
		    ~;
		    if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||($postid eq "$inmembername")) {
			  $output .= qq~
	                      	<tr>
	                      	    <td bgcolor=$postcolortwo align=right>$admindelete</td>
	                       	</tr>
			  ~;
		    }

       $output .= qq~
	                 <tr>
	                    <td bgcolor="$postcolortwo" valign=top style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word"><font face="$font" color=$postfontcolortwo>
	                        $msg
	                    </td>
	                 </tr>
	                 <tr>
	                    <td bgcolor="$postcolortwo" valign=middle>
	                     <table width=100% border="0" cellpadding="0" cellspacing="0">
	                        <tr><td align=left>&nbsp;&nbsp;&nbsp;<font face="$font" color=$postfontcolortwo><b>发布人</b>： $postid</font>
	                        </td><td align=right><font face="$font" color=$postfontcolortwo><b>发布时间</b>： $dateposted</font>&nbsp;&nbsp;&nbsp;
	                        </tr>
	                        </table>
	                        </td>
	                        </font>
	                        </tr></table></td></tr></table></body></html>

	              ~;
	             print header(-charset=>gb2312);
	             print $output;

exit;
}

sub del {
	&error("老大你别黑我的程序阿!") if (($id eq "")||($inforum eq ""));
	$dirtoopen = "$lbdir" . "boarddata";
	open (DIR, "<$dirtoopen/xzb$inforum.cgi");
        @xzbdata = <DIR>;
        $sizexzb=@xzbdata;
        close (DIR);
        chomp(@xzbdata);
#        &getmember("$inmembername");
        ($nouse, $title,$postid,$msg,$posttime)=split(/\t/,$xzbdata[$id]);
         if (($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes")&&($postid ne "$inmembername")) {
        &error("删除小字报&你没权力删除!");
}

        open (DIR, ">$dirtoopen/xzb$inforum.cgi");
        for ($i=0;$i<$sizexzb;$i++){
        	if ($i ne $id){
             	print DIR "$xzbdata[$i]\n";

             	}
        }
        close (DIR);

	$output=qq~
	<script>top.window.close();</script>
	~;
	             print header(-charset=>gb2312);
	             print $output;

exit;
}
