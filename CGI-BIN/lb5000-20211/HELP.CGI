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
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "visitforum.lib.pl";
$|++;                                     # Unbuffer the output
$thisprog = "help.cgi";
$query = new LBCGI;
&ipbanned; #封杀一些 ip

$inadmin                = $query -> param('admin');
$action                 = $query -> param('action');
$inhelpon               = $query -> param('helpon');
$inadminmodpass         = $query -> param("adminmodpass");
$inadminmodname         = $query -> param("adminmodname");
$inadminmodpass         = &cleaninput($inadminmodpass);
$inadminmodname         = &cleaninput($inadminmodname);
&error("普通错误&老大，别乱黑我的程序呀！") if (($inadminmodname =~ m/\//)||($inadminmodname =~ m/\\/)||($inadminmodname =~ m/\.\./));
$inadminmodname =~ s/\///g;
$inadminmodname =~ s/\.\.//g;
$inadminmodname =~ s/\\//g;

$inhelpon               = &cleaninput($inhelpon);
$inhelpon =~ s/\///g;
$inhelpon =~ s/\.cgi//ig;
$inhelpon =~ s/\.\.//g;
$inhelpon =~ s/\\//g;
$inadmin =~ s/\///g;
$inadmin =~ s/\.\.//g;
$inadmin =~ s/\\//g;
$cleanhelpname = $inhelpon;
$cleanhelpname =~ s/\_/ /g;
$cleanadminname = $inadmin;
$cleanadminname =~ s/\_/ /g;
if (($number) && ($number !~ /^[0-9]+$/)) { &error("普通错误&请不要修改生成的 URL！"); }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ($inmembername eq "") {
    $inmembername = "客人";
}
else {
	&getmember("$inmembername");
	&error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
print header(-charset=>gb2312);
    if ($inhelpon) {
        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
              <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 border=0 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>$boardname的帮助文件</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                       <br><center>$inmembername，希望下面的帮助对您有用</center><br><br>
                       <font face="$font" color=$fontcolormisc>
                       <b>关于$cleanhelpname的帮助：</b><p>
	~;
        $filetoopen = "$lbdir" . "help/$inhelpon.dat";
        $filetoopen = &stripMETA($filetoopen);
        open (FILE, "$filetoopen") or die "无法定位所需文件！";
        @helpdata = <FILE>;
        close (FILE);

        foreach (@helpdata) {
            $output .= $_;
        }
    }
    elsif ($action eq "login") {

            &getmember("$inadminmodname");

            unless ($membercode eq "ad" ||($membercode eq 'smo')|| $membercode eq "mo") { &messangererror("查看帮助&您没有权限查看此文件！"); }
            if ($inadminmodpass ne $password) { &messangererror("查看帮助&您的密码错误！"); }

            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
               <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 border=0 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>$boardname的帮助文件</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                      <br><center>$inadminmodname，希望下面的帮助对您有用</center><br><br>
                      <font face="$font" color=$fontcolormisc>
                      <b>　　坛主/版主帮助文件</b><p>
             ~;
            $dirtoopen = "$lbdir" . "help";
            opendir (DIR, "$dirtoopen") or die "不能够找到帮助文件所在目录：$dirtoopen";
            @dirdata = readdir(DIR);
            closedir (DIR);
            @sorteddirdata = grep(/cgi$/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);

            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.cgi$//g;
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                $output .= qq~&nbsp;&nbsp;&nbsp;&nbsp;关于<a href="$thisprog?admin=$filename" target="_self"><b>$cleanname</b></a>的帮助<p>~;
            }
	}
        elsif ($inadmin) {
	    &getmember("$inmembername");
            unless ($membercode eq "ad" || $membercode eq 'smo'|| $membercode eq "mo") { &messangererror("查看帮助&您没有权限查看此文件！"); }
            if ($inpassword ne $password) { &messangererror("查看帮助&您的密码错误！"); }
	    $output .= qq~
		<table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
                 <tr>
                  <td>
                  <table cellpadding=3 cellspacing=1 border=0 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>$boardname的帮助文件</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                      <br><center>$inmembername，希望下面的帮助对您有用</center><br><br>
                      <font face="$font" color=$fontcolormisc>
                      <b>关于$cleanadminname的帮助</b><p>
            ~;

	    $filetoopen = "$lbdir" . "help/$inadmin.cgi";
            $filetoopen = &stripMETA($filetoopen);
            open (FILE, "$filetoopen") or die "无法定位所需文件！";
            @helpdata = <FILE>;
            close (FILE);

	    foreach (@helpdata) {
                $output .= $_;
            }
        }
        else {
	    $output .= qq~
              <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
                <tr>
                <td>
                    <table cellpadding=3 cellspacing=1 border=0 width=100%>
                        <tr>
                            <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>$boardname的帮助文件</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                            <br><center>$inmembername，希望下面的帮助对您有用</center><br><br>
                            <font face="$font" color=$fontcolormisc>
                            <b>&nbsp;&nbsp;&nbsp;&nbsp;常规帮助文件</b><p>
            ~;

            $dirtoopen = "$lbdir" . "help";
            opendir (DIR, "$dirtoopen") or die "不能够找到帮助文件所在目录：$dirtoopen";
            @dirdata = readdir(DIR);
            closedir (DIR);
            @sorteddirdata = grep(/dat$/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);

            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.dat$//g;
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                $output .= qq~&nbsp;&nbsp;&nbsp;&nbsp;关于<a href="$thisprog?helpon=$filename" target="_self"><b>$cleanname</b></a>的帮助<p>~;
            }
	}

    if ($passwordverification eq "yes") { $passwordverification = "是必需的"; }
    else { $passwordverification = "不是必需的"; }

    if ($emailfunctions ne "on") { $emailfunctions = "关闭"; }

    if ($emoticons eq "on") {
	$emoticons = "使用";
        $emoticonslink = qq~| 查看<a href=javascript:openwin('$miscprog?action=showsmilies',300,350)>表情转换</a>~;
    }
    else { $emoticons = "没有使用"; }
    $output .= qq~<p><br><br>查看<a href=\"$thisprog\" target=\"_self\">所有的帮助文件</a> $emoticonslink | 查看 <a href=\"javascript:openwin('$miscprog?action=lbcode',300,350)\">LB5000 标签</a> | 查看 <a href=\"javascript:openwin('lookemotes.cgi?action=style',300,350)\">EMOTE 标签</a>~;

    $output .= qq~
    </td></tr>
    <tr>
    <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc><b>论坛常规信息</b><br><br>
    表情自动转换：<b>$emoticons</b><br>邮件地址确认：<b>$passwordverification</b><br>论坛邮件功能：<b>$emailfunctions</b><br><br>
    </td>
    </tr>
    <tr>
    <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc><b>登陆访问坛主/版主的帮助</b><br>

    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="login">
    <font face="$font" color=$fontcolormisc>
    用户名：&nbsp; <input type=text name="adminmodname" value="$inmembername"5> &nbsp;
    密　码：&nbsp; <input type=password name="adminmodpass" value="$inpassword"5> &nbsp; <input type=submit value="登 陆"></td></tr></form>
    </table></td></tr></table>
    ~;

    &printmessanger(
        -Title   => "$boardname - 帮助",
        -ToPrint => $output,
        -Version => $versionnumber
    );

sub messangererror {
    my $errorinfo = shift;
    (my $where,my $errormsg) = split(/\&/, $errorinfo);
    $output = qq~
      <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
	<tr>
        <td>
        <table cellpadding=6 cellspacing=1 border=0 width=100%>
        <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>错误：$where</b></font></td></tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
                <b>关于$where错误的详细原因：</b>
                <ul>
                <li><b>$errormsg</b>
                <li>您是否需要查看<a href=>帮助文件</a>?
                </ul>
                <b>产生$where错误的可能原因：：</b>
                <ul>
                <li>密码错误<li>用户名错误<li>您不是<a href=>注册</a>用户
                </ul>
                </tr>
                </td></tr>
                <tr>
                <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc> <a href="javascript:history.go(-1)"> << 返回上一页</a>
                </td></tr>
                </table></td></tr></table>
    ~;
    &printmessanger(
       -Title   => $boardname,
       -ToPrint => $output,
       -Version => $versionnumber
    );
}
