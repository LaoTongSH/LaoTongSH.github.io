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
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/membertitles.cgi";
require "lbmail.lib.pl";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                                    # Unbuffer the output
$thisprog = "profile.cgi";
$query = new LBCGI;

&ipbanned; #封杀一些 ip

$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;

$addme=$query->param('addme');

if ($arrowavaupload ne "on") { undef $addme; }

$action              = $query -> param('action');
$inmember            = $query -> param('member');
$inmember =~ s/\///g;
$inmember =~ s/\.\.//g;
$inmembername        = $query -> param("membername");
$inpassword          = $query -> param("password");
$oldpassword         = $query -> param("oldpassword");
$action              = &cleaninput("$action");
$inmember            = &cleaninput("$inmember");
$inmembername        = &cleaninput("$inmembername");
$inpassword          = &cleaninput("$inpassword");
$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");

    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
	&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
	$inmembername =~ s/\///g;
	$inmembername =~ s/\.\.//g;
	$inmembername =~ s/\\//g;
    if (($inmembername eq "")&&($action ne "lostpass")&&($action ne "lostpassword")){
    	$inmembername = "客人";
    	if ($dispprofile eq "no") {
            print header(-charset=>gb2312);
            &error("查看会员资料&客人无权查看会员资料！")
        }
    }
    else {
		&getmember("$inmembername");
        }
	if ($arrawsignpic eq "on") { $signpicstates = "允许";} else {$signpicstates = "禁止";}
	if ($arrawsignflash eq "on") { $signflashstates = "允许";} else {$signflashstates = "禁止";}
	if ($arrawsignfontsize eq "on") { $signfontsizestates = "允许";} else {$signfontsizestates = "禁止";}
	if ($arrawsignsound eq "on") { $signsoundstates = "允许";} else {$signsoundstates = "禁止";}
    # Print the page title

&badwordfile;

    &title;
    $output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
        <tr>
            <td width=30% rowspan=2 valign=top>
            <img src="$imagesurl/images/$boardlogo" border=0>
            </td>
            <td valign=top align=left>
                <font color=$fontcolormisc>
	             　<img src="$imagesurl/images/closedfold.gif" border=0>　<a href="$forumsummaryprog">$boardname</a><br>
                 　<img src="$imagesurl/images/bar.gif" border=0 width=15 height=15><img src="$imagesurl/images/openfold.gif" border=0>　用户资料
            </td>
        </tr>
    </table>
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 border=0 width=100%>
    ~;
    my %Mode = (
    'show'                 =>    \&showprofile,
    'shows'                =>    \&showprofile,
    'process'              =>    \&savemodify,
    'lostpassword'         =>    \&lostpasswordform,
    'lostpass'             =>    \&lostpasswordform,
    'sendpassword'         =>    \&sendpassword,
    'modify'               =>    \&modify,
    );
    if($Mode{$action}) {
        $Mode{$action}->();
        }
        else{
        $inmembername =~ s/\_/ /g;
        $output .= qq~
        <tr>
        <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="modify">
        <font color=$fontcolormisc><b>请登陆后修改你的个人资料</b></font></td></tr>
        <tr>
        <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>请输入您的用户名</font></td>
        <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername"></td></tr>
        <tr>
        <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>请输入您的密码</font></td>
        <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword"></td></tr>
        <tr>
        <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
        ~;
        } # end else

        print header(-charset=>gb2312);
        &output(
	           -Title   => $boardname,
	           -ToPrint => $output,
	           -Version => $versionnumber
	            );
	# lost password routine
	sub lostpasswordform {
	    $helpurl = &helpfiles("遗忘密码");
	    $helpurl = qq~$helpurl<img src="$imagesurl/images/help_b.gif" border=0></a>~;

	    $output =~ s/\&nbsp\;用户资料/\&nbsp\;忘记密码/g;

	    $output .= qq~
	    <p>
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	    <form action="$thisprog" method="post">
	    <input type=hidden name="action" value="sendpassword">
	    <font color=$fontcolormisc><b>请输入您的用户名，我们可以将您的密码通过邮件发给您！</b></font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</td>
	    <td bgcolor=$miscbackone><input type=text name="membername">　 $helpurl</td></tr>
	    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name=submit value="提 交">
	    </td></form></tr></table></td></tr></table>
	    ~;
	} # end lost password form.
	sub sendpassword {

	&getmember("$inmembername");
	if (($membercode eq "ad")||($membercode eq "smo")) { &blocked; }
	elsif ($emailfunctions eq "off") { #  if close Email functions
	$output .= qq~
<tr><td bgcolor=$miscbacktwo valign=middle align=center><font color=$fontcolormisc><b>非常抱歉，$inmembername</b></font></td></tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>
由于这个论坛的发送邮件功能已经关闭，请通过另外的途径来联系坛主而拿取您的密码！
</td></tr></table></td></tr></table>
~;}
	elsif ($userregistered ne "no") { # start emailing functions
	                $message .= "\n";
	                $message .= "$boardname\n";
	                $message .= "$boardurl/$forumsummaryprog\n\n";
	                $message .= "------------------------------------\n";
	                $message .= "应您的要求，现将您的密码寄给您！\n\n";
	                $message .= "您的用户名：$inmembername\n";
	                $message .= "您的密码是：$password\n\n";
	                $message .= "------------------------------------\n";
	                $to = $emailaddress;
	                $from = $adminemail_out;
	                $subject = "忘记密码[$boardname]";
	                &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message );

	                $output =~ s/用户资料/密码已经寄出/g;

	                $output .= qq~
	                <tr>
	                <td bgcolor=$miscbacktwo valign=middle align=center><font color=$fontcolormisc><b>你好，$inmembername</b></font></td></tr>
	                <tr>
	                <td bgcolor=$miscbackone align=center><font color=$fontcolormisc>
	                您的密码已经成功的通过指定的邮件地址发送给您了。
	                </td></tr></table></td></tr></table>
	                 ~;

	                } # end user registered.

	                else {
	                    print header(-charset=>gb2312);
	                    &error("请求密码&不是注册用户！");
	                    }
	} # end routine.
	################ show profile subroutine
	sub showprofile {
	$inmember =~ s/\_/ /isg;
	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
        $filetoopens = &lockfilename($filetoopens);
	if (!(-e "$filetoopens.lck")) {
            &whosonline("$inmembername\t个人资料\tnone\t查看<b>$inmember</b>的个人资料\t");
        }
	&getmember("$inmember");
	    if ("$userregistered" eq "no") { print header(-charset=>gb2312);&error("修改资料&没有此用户名！"); }
	 $allnumberofposts=$numberofreplys+$numberofposts;
        if ($allnumberofposts >= $mpostmarkmax) { $mtitle =  $mtitlemax;  $membergraphic = $mgraphicmax; }
        elsif ($allnumberofposts >= $mpostmark19) { $mtitle =  $mtitle19;  $membergraphic = $mgraphic19; }
        elsif ($allnumberofposts >= $mpostmark18) { $mtitle =  $mtitle18;  $membergraphic = $mgraphic18; }
        elsif ($allnumberofposts >= $mpostmark17) { $mtitle =  $mtitle17;  $membergraphic = $mgraphic17; }
        elsif ($allnumberofposts >= $mpostmark16) { $mtitle =  $mtitle16;  $membergraphic = $mgraphic16; }
        elsif ($allnumberofposts >= $mpostmark15) { $mtitle =  $mtitle15;  $membergraphic = $mgraphic15; }
        elsif ($allnumberofposts >= $mpostmark14) { $mtitle =  $mtitle14;  $membergraphic = $mgraphic14; }
        elsif ($allnumberofposts >= $mpostmark13) { $mtitle =  $mtitle13;  $membergraphic = $mgraphic13; }
        elsif ($allnumberofposts >= $mpostmark12) { $mtitle =  $mtitle12;  $membergraphic = $mgraphic12; }
        elsif ($allnumberofposts >= $mpostmark11) { $mtitle =  $mtitle11;  $membergraphic = $mgraphic11; }
        elsif ($allnumberofposts >= $mpostmark10) { $mtitle =  $mtitle10;  $membergraphic = $mgraphic10; }
        elsif ($allnumberofposts >= $mpostmark9)  { $mtitle =  $mtitle9;   $membergraphic = $mgraphic9; }
        elsif ($allnumberofposts >= $mpostmark8)  { $mtitle =  $mtitle8;   $membergraphic = $mgraphic8; }
        elsif ($allnumberofposts >= $mpostmark7)  { $mtitle =  $mtitle7;   $membergraphic = $mgraphic7; }
        elsif ($allnumberofposts >= $mpostmark6)  { $mtitle =  $mtitle6;   $membergraphic = $mgraphic6; }
        elsif ($allnumberofposts >= $mpostmark5)  { $mtitle =  $mtitle5;   $membergraphic = $mgraphic5; }
        elsif ($allnumberofposts >= $mpostmark4)  { $mtitle =  $mtitle4;   $membergraphic = $mgraphic4; }
        elsif ($allnumberofposts >= $mpostmark3)  { $mtitle =  $mtitle3;   $membergraphic = $mgraphic3; }
        elsif ($allnumberofposts >= $mpostmark2)  { $mtitle =  $mtitle2;   $membergraphic = $mgraphic2; }
        elsif ($allnumberofposts >= $mpostmark1)  { $mtitle =  $mtitle1;   $membergraphic = $mgraphic1; }
        else { $mtitle = $mtitle0; $membergraphic = ""; }  #显示默认等级
		if ($showemail eq "no") { $emailaddress = "保密"; }
		elsif ($showemail eq "msn") { $emailaddress = qq~<img src=$imagesurl/images/msn.gif border=0 width=16 height=16 align=absmiddle> <a href="mailto:$emailaddress">$emailaddress</a>~; }
	        else { $emailaddress = qq~<a href="mailto:$emailaddress">$emailaddress</a>~; }
	    if ($aolname eq "") { $aolname = "没有"; $aollogo ="";} else {my $oicqimg=&getoicq($aolname);$aollogo = qq~<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$aolname target=_blank><img src="$oicqimg" alt="查看 OICQ:$aolname 的资料" border=0 width=16 height=16></a>~;}
	    if ($icqnumber eq "") { $icqnumber = "没有"; $icqlogo = ""; } else { $icqlogo = qq~<a href=$miscprog?action=icq&UIN=$icqnumber target=_blank><img src="http://wwp.icq.com/scripts/online.dll?icq=$icqnumber&img=7" alt="给 ICQ:$icqnumber 发个消息" border=0 width=16 height=16></a>~; }
        if ((($membercode eq "ad")&&($membertitle eq "Member"))||(($membercode eq "ad")&&($membertitle eq "member")))
         { $membertitle = "论坛坛主"; }

        if ((($membercode eq "mo")&&($membertitle eq "Member"))||(($membercode eq "mo")&&($membertitle eq "member")))
         { $membertitle = "论坛版主";}
         if ((($membercode eq "smo")&&($membertitle eq "Member"))||(($membercode eq "smo")&&($membertitle eq "member")))
         { $membertitle = "总版主";}

        $mtitle = $motitle if (($membercode eq "mo")&&($motitle ne ""));
        $mtitle = $adtitle if (($membercode eq "ad")&&($adtitle ne ""));
        $mtitle = $smotitle if (($membercode eq "smo")&&($smotitle ne ""));

        if ($membercode eq "banned") { $membertitle = "禁止发言"; }
        if ($membertitle eq "member" || $membertitle eq "Member" || $membertitle eq "") { $membertitle = "没有"; }
	if (($homepage eq "http://") || ($homepage eq "")) { $homepage = "没有"; } else { $homepage = qq~<a href="$homepage" target="_blank">$homepage</a>~; }

	    $lastgone   = $joineddate if($lastgone eq "");
	    $joineddate = &longdate($joineddate + ($timedifferencevalue*3600) + ($timezone*3600));
	    $lastgone   = &dateformat($lastgone + ($timedifferencevalue*3600) + ($timezone*3600));
	    ## Sort last post, and where

	    ($postdate, $posturl, $posttopic) = split(/\%%%/,$lastpostdate);
            $posttopic =~ s/^＊＃！＆＊//;

	    if ($postdate ne "没有发表过") {
	        $postdate = &longdate($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
	        $lastpostdetails = qq~<a href="$posturl">$posttopic</a> ($postdate)~;
	        }
	        else {
	            $lastpostdetails = "没有发表过";
	            }
        if ($avatars eq "on") {
	    if (($personalavatar)&&($personalwidth)&&($personalheight)) { #自定义头像存在
	        if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	            $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
	        }
	        else {
	            $useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>);
	        }
	    }
            elsif (($useravatar ne "noavatar") && ($useravatar)) {
                $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$useravatar.gif" border=0 $defaultwidth $defaultheight>);
            }
            else {$useravatar="没有"; }
        }
	    $interests = "没有" if ($interests eq "");
            $location = "没有" if ($location eq "");

        if ($signature) {
	  $signature = &signlbcode($signature);
        }
	else {$signature = "没有";}

	if ($jhmp) {
	  $jhmp = ($jhmp);
        }
	else {$jhmp = "无门无派";}

	if ($sex eq "f") {
	    $sex = "美女";
	}
	elsif ($sex eq "m") {
	    $sex = "帅哥";
	}
	else {
	    $sex = "保密";
	}
	$numberofreplys = 0 if ($numberofreplys eq "");
	$meili     = 0 if ($meili eq "");
	$postdel   = 0 if ($postdel eq "");
	$jhmp    = "无门无派" if ($jhmp eq "");
        if ($rating !~ /^[0-9\-]+$/) {$rating = 0;}
        if ($rating eq "") {$rating =0;}
	$mymoney   = 0 if ($mymoney eq "");
	$education = "未输入" if ($education eq "");
	$marry     = "未输入" if ($marry eq "");
	$work      = "未输入" if ($work eq "");
	$born      = "未输入" if (($born eq "")||($born eq "//"));
	$userflag  = "blank" if ($userflag eq "");
        $usersx    = "blank" if ($usersx eq "");
if ($usersx eq "sx1")     {$showsx = "<IMG src=$imagesurl/sx/sx1.gif  alt=子鼠 align=absmiddle>";}
elsif ($usersx eq "sx2")  {$showsx = "<IMG src=$imagesurl/sx/sx2.gif  alt=丑牛 align=absmiddle>";}
elsif ($usersx eq "sx3")  {$showsx = "<IMG src=$imagesurl/sx/sx3.gif  alt=寅虎 align=absmiddle>";}
elsif ($usersx eq "sx4")  {$showsx = "<IMG src=$imagesurl/sx/sx4.gif  alt=卯兔 align=absmiddle>";}
elsif ($usersx eq "sx5")  {$showsx = "<IMG src=$imagesurl/sx/sx5.gif  alt=辰龙 align=absmiddle>";}
elsif ($usersx eq "sx6")  {$showsx = "<IMG src=$imagesurl/sx/sx6.gif  alt=巳蛇 align=absmiddle>";}
elsif ($usersx eq "sx7")  {$showsx = "<IMG src=$imagesurl/sx/sx7.gif  alt=午马 align=absmiddle>";}
elsif ($usersx eq "sx8")  {$showsx = "<IMG src=$imagesurl/sx/sx8.gif  alt=未羊 align=absmiddle>";}
elsif ($usersx eq "sx9")  {$showsx = "<IMG src=$imagesurl/sx/sx9.gif  alt=申猴 align=absmiddle>";}
elsif ($usersx eq "sx10") {$showsx = "<IMG src=$imagesurl/sx/sx10.gif alt=葵鸡 align=absmiddle>";}
elsif ($usersx eq "sx11") {$showsx = "<IMG src=$imagesurl/sx/sx11.gif alt=戌狗 align=absmiddle>";}
elsif ($usersx eq "sx12") {$showsx = "<IMG src=$imagesurl/sx/sx12.gif alt=亥猪 align=absmiddle>";}
else {$showsx = "";}
	$userxz    = "blank" if ($userxz eq "");
if ($userxz eq "z1")     {$showxz = "<IMG height=15 src=$imagesurl/star/z1.gif  width=15 alt=白羊座 align=absmiddle>";}
elsif ($userxz eq "z2")  {$showxz = "<IMG height=15 src=$imagesurl/star/z2.gif  width=15 alt=金牛座 align=absmiddle>";}
elsif ($userxz eq "z3")  {$showxz = "<IMG height=15 src=$imagesurl/star/z3.gif  width=15 alt=双子座 align=absmiddle>";}
elsif ($userxz eq "z4")  {$showxz = "<IMG height=15 src=$imagesurl/star/z4.gif  width=15 alt=巨蟹座 align=absmiddle>";}
elsif ($userxz eq "z5")  {$showxz = "<IMG height=15 src=$imagesurl/star/z5.gif  width=15 alt=狮子座 align=absmiddle>";}
elsif ($userxz eq "z6")  {$showxz = "<IMG height=15 src=$imagesurl/star/z6.gif  width=15 alt=处女座 align=absmiddle>";}
elsif ($userxz eq "z7")  {$showxz = "<IMG height=15 src=$imagesurl/star/z7.gif  width=15 alt=天秤座 align=absmiddle>";}
elsif ($userxz eq "z8")  {$showxz = "<IMG height=15 src=$imagesurl/star/z8.gif  width=15 alt=天蝎座 align=absmiddle>";}
elsif ($userxz eq "z9")  {$showxz = "<IMG height=15 src=$imagesurl/star/z9.gif  width=15 alt=射手座 align=absmiddle>";}
elsif ($userxz eq "z10") {$showxz = "<IMG height=15 src=$imagesurl/star/z10.gif width=15 alt=魔羯座 align=absmiddle>";}
elsif ($userxz eq "z11") {$showxz = "<IMG height=15 src=$imagesurl/star/z11.gif width=15 alt=水瓶座 align=absmiddle>";}
elsif ($userxz eq "z12") {$showxz = "<IMG height=15 src=$imagesurl/star/z12.gif width=15 alt=双鱼座 align=absmiddle>";}
else {$showxz = "";}


    	$jingyan = $addjy;
if ($usertype eq "0") {
    if (($membercode eq "rz")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo")) {
        $jingyan = $numberofposts * $ttojy + $numberofreplys * $rtojy + $visitno * $ltojy + $jingyan - $postdel * $deljingyan;
        $meili   = $numberofposts * $addml + $numberofreplys * $replyml + $visitno * $loginml + $meili - $postdel * $delml;
        $mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney;
    }
}
else {
        $jingyan = $numberofposts * $ttojy + $numberofreplys * $rtojy + $visitno * $ltojy + $jingyan - $postdel * $deljingyan;
        $meili   = $numberofposts * $addml + $numberofreplys * $replyml + $visitno * $loginml + $meili - $postdel * $delml;
        $mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney;
}
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $signature=~ s/$bad/$good/isg;
                $interests=~ s/$bad/$good/isg;
                }
            }
	    $output .= qq~
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font color=$fontcolormisc>"<b><font color=$fonthighlight>$inmember</b></font>" 的个人资料</td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle width=30%><font color=$fontcolormisc><b>注册时间：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$joineddate</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>当前头衔：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$membertitle</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>当前级别：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><a href="lookinfo.cgi?action=style" target="_blank">$mtitle</a></font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>最后发表：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$lastpostdetails</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>总共发表：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$numberofposts 篇</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>总共回复：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$numberofreplys 篇</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>贴子被删除：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$postdel 篇</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>邮件地址：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$emailaddress</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>主页地址：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$homepage</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>OICQ号码：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$aollogo $aolname</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>ICQ 号码：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$icqlogo $icqnumber</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>国家：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><img src=$imagesurl/flags/$userflag.gif width=21 height=14></font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>来自：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$location</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>江湖门派：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$jhmp</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>威望：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$rating</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>最后访问：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$lastgone</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>访问次数：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$visitno 次</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>魅力：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$meili</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>性别：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$sex</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>学历：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$education</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>婚姻状况：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$marry</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>职业：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$work</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>出生年月：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$born</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>你的生肖：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$showsx</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>你的星座：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$showxz</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>金钱：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$mymoney</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>经验：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$jingyan</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>自我简介：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$interests</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>签名：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$signature</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>个性图片：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle>$useravatar</td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>相关操作：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><a href="javascript:openScript('friendlist.cgi?action=adduser&adduser=$inmember',420,320)">把$inmember加为我的好友</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:openScript('messanger.cgi?action=new&touser=$inmember',420,320)">给$inmember发一个短消息</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="search.cgi?action=startsearch&TYPE_OF_SEARCH=username_search&NAME_SEARCH=topictitle_search&FORUMS_TO_SEARCH=all&SEARCH_STRING=$inmember" target=_blank>查找$inmember发表的所有帖子</a></td></tr>
	    </table></td></tr></table>
	    ~;


    }

	sub modify {
	    $helpurl = &helpfiles("遗忘密码");
	    $helpurl = qq~$helpurl<img src=$imagesurl/images/help_b.gif border=0></a>~;
	&getmember("$inmembername");
	if ("$userregistered" eq "no") { print header(-charset=>gb2312);&error("修改资料&没有此用户名！"); }
	if ("$inpassword" ne "$password") {&error("修改资料&密码错误！请重新登陆后修改！"); }
	if (("$passwordverification" eq "yes") && ("$emailfunctions" ne "off")) {
	    $newpassneeded = "<br><B>如果您修改了邮件地址，一个新的密码将通过邮件发给您。</B>";
	    undef $newpasswordaddon;
	}
	$newpasswordaddon = qq~
 	   <tr>
	   <td bgcolor=$miscbackone width=40%><font color=$fontcolormisc><b>密码：</b><br>请输入修改密码，区分大小写</td>
	   <td bgcolor=$miscbackone width=60%><input type=password name="newpassword1" maxlength=20>　$helpurl</td>
	   </tr><tr>
	   <td bgcolor=$miscbackone><font color=$fontcolormisc><b>密码：</b><br>再输一遍，以便确定！</td>
	   <td bgcolor=$miscbackone><input type=password name="newpassword2" maxlength=20>　$helpurl</td>
	   </tr><tr>
	   <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	   <font color=$fonthighlight><b>如果你不想修改密码，请保持上面空白！</b></font></td></tr>
	~;
    ### Avatar stuff
my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t个人资料\tnone\t修改<b>$inmembername</b>的个人资料\t");
}

if ($avatars eq "on") {

        if ($arrowavaupload eq "on") {
            $avaupload = qq~<br>上传头像： <input type="file" size=20 name="addme">　上传自定义头像。<br>~;
        }
        else { undef $avaupload; }


        open (FILE, "${lbdir}data/lbava.cgi");
        my @images = <FILE>;
        close (FILE);
        chomp @images;

        $selecthtml .= qq~<option value="noavatar" selected>不要头像</option>\n~;
        $currentface = "noavatar";
        foreach (@images) {
	$totleavator=@images -1;

            $cleanavatar =  $_;
            $cleanavatar =~ s/.gif$//i;

            if (($cleanavatar =~ /admin_/) && ($membercode eq "me")) { next; }

            if ($cleanavatar eq "$useravatar") {
	            $selecthtml .= qq~<option value="$cleanavatar" selected>$cleanavatar</option>\n~;
                $currentface = "$cleanavatar";
                }
                elsif (($cleanavatar eq "noavatar") && (!$useravatar)) {
                    }
	                else {
                        $selecthtml .= qq~<option value="$cleanavatar">$cleanavatar</option>\n~;
                        }
                    }

            $avatarhtml = qq~
            <script language="javascript">
            function showimage(){document.images.useravatars.src="$imagesurl/avatars/"+document.creator.useravatar.options[document.creator.useravatar.selectedIndex].value+".gif";}
            </script>

            <tr>
                <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>个性图片：</b><br>您可以选择一个个性图片，当你发表时将显示在您的名字下方。<BR>如果你填写了下面的自定义头像部分，那么你的头像以自定义的为准。否则，请你留空自定义头像的所有栏目！<BR>
                <br><br><b>关于自定义头像</b>：<br>你也可以在这里给出你自定义头像的 URL 地址，头像的高度和宽度(像素)。 如果不想要自定义头像，请将相应栏目栏目全部留空！<BR><BR>
                <br><b>如果你不想要任何的头像，那么请首先在菜单上选“noavatar”，然后留空所有自定义头像的部分！</b><BR><br>
                <td bgcolor=$miscbackone valign=top>总头像个数： $totleavator 个。　<a href=viewavatars.cgi target=_blank><B>按此查看</B></a>所有头像名称列表。<BR>
                    <select name="useravatar" size=1 onChange="showimage()">
                    $selecthtml
                    </select>
                    <img src=$imagesurl/avatars/$currentface.gif name="useravatars" width=32 height=32 hspace=15><br><br><br>
                $avaupload
                <br>图像位置： <input type="text" name="newpersonalavatar" size="26" value="$personalavatar">　输入完整的 URL 路径。<br>
                <br>图像宽度： <input type="text" name="newpersonalwidth" size="2" maxlength=3 value="$personalwidth">　必须是 20 -- $maxposticonwidth 之间的一个整数。<br>
                <br>图像高度： <input type="text" name="newpersonalheight" size="2" maxlength=3 value="$personalheight">　必须是 20 -- $maxposticonheight 之间的一个整数。<br></td>
                </td>
            </tr>
            ~;
} # end avatar if
$userflag = "blank" if ($userflag eq "");
$flaghtml = qq~
<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc><b>所在国家:</b><br>请选择你所在的国家。</td>
<td bgcolor=$miscbackone>
<select name="userflag" size=1 onChange="showflag()">
<option value="blank">保密</option>
<option value="China">中国</option>
<option value="Angola">安哥拉</option>
<option value="Antigua">安提瓜</option>
<option value="Argentina">阿根廷</option>
<option value="Armenia">亚美尼亚</option>
<option value="Australia">澳大利亚</option>
<option value="Austria">奥地利</option>
<option value="Bahamas">巴哈马</option>
<option value="Bahrain">巴林</option>
<option value="Bangladesh">孟加拉</option>
<option value="Barbados">巴巴多斯</option>
<option value="Belgium">比利时</option>
<option value="Bermuda">百慕大</option>
<option value="Bolivia">玻利维亚</option>
<option value="Brazil">巴西</option>
<option value="Brunei">文莱</option>
<option value="Canada">加拿大</option>
<option value="Chile">智利</option>
<option value="Colombia">哥伦比亚</option>
<option value="Croatia">克罗地亚</option>
<option value="Cuba">古巴</option>
<option value="Cyprus">塞浦路斯</option>
<option value="Czech_Republic">捷克斯洛伐克</option>
<option value="Denmark">丹麦</option>
<option value="Dominican_Republic">多米尼加</option>
<option value="Ecuador">厄瓜多尔</option>
<option value="Egypt">埃及</option>
<option value="Estonia">爱沙尼亚</option>
<option value="Finland">芬兰</option>
<option value="France">法国</option>
<option value="Germany">德国</option>
<option value="Great_Britain">英国</option>
<option value="Greece">希腊</option>
<option value="Guatemala">危地马拉</option>
<option value="Honduras">洪都拉斯</option>
<option value="Hungary">匈牙利</option>
<option value="Iceland">冰岛</option>
<option value="India">印度</option>
<option value="Indonesia">印度尼西亚</option>
<option value="Iran">伊朗</option>
<option value="Iraq">伊拉克</option>
<option value="Ireland">爱尔兰</option>
<option value="Israel">以色列</option>
<option value="Italy">意大利</option>
<option value="Jamaica">牙买加</option>
<option value="Japan">日本</option>
<option value="Jordan">约旦</option>
<option value="Kazakstan">哈萨克</option>
<option value="Kenya">肯尼亚</option>
<option value="Kuwait">科威特</option>
<option value="Latvia">拉脱维亚</option>
<option value="Lebanon">黎巴嫩</option>
<option value="Lithuania">立陶宛</option>
<option value="Malaysia">马来西亚</option>
<option value="Malawi">马拉维</option>
<option value="Malta">马耳他</option>
<option value="Mauritius">毛里求斯</option>
<option value="Morocco">摩洛哥</option>
<option value="Mozambique">莫桑比克</option>
<option value="Netherlands">荷兰</option>
<option value="New_Zealand">新西兰</option>
<option value="Nicaragua">尼加拉瓜</option>
<option value="Nigeria">尼日利亚</option>
<option value="Norway">挪威</option>
<option value="Pakistan">巴基斯坦</option>
<option value="Panama">巴拿马</option>
<option value="Paraguay">巴拉圭</option>
<option value="Peru">秘鲁</option>
<option value="Poland">波兰</option>
<option value="Portugal">葡萄牙</option>
<option value="Romania">罗马尼亚</option>
<option value="Russia">俄国</option>
<option value="Saudi_Arabia">沙特阿拉伯</option>
<option value="Singapore">新加坡</option>
<option value="Slovakia">斯洛伐克</option>
<option value="Slovenia">斯洛文尼亚</option>
<option value="Solomon_Islands">所罗门</option>
<option value="Somalia">索马里</option>
<option value="South_Africa">南非</option>
<option value="South_Korea">韩国</option>
<option value="Spain">西班牙</option>
<option value="Sri_Lanka">印度</option>
<option value="Surinam">苏里南</option>
<option value="Sweden">瑞典</option>
<option value="Switzerland">瑞士</option>
<option value="Thailand">泰国</option>
<option value="Trinidad_Tobago">多巴哥</option>
<option value="Turkey">土耳其</option>
<option value="Ukraine">乌克兰</option>
<option value="United_Arab_Emirates">阿拉伯联合酋长国</option>
<option value="United_States">美国</option>
<option value="Uruguay">乌拉圭</option>
<option value="Venezuela">委内瑞拉</option>
<option value="Yugoslavia">南斯拉夫</option>
<option value="Zambia">赞比亚</option>
<option value="Zimbabwe">津巴布韦</option>
</select>
<img src="$imagesurl/flags/$userflag.gif" name="userflags" border=0 height=14 width=21>
</td></tr>
~;
$flaghtml =~ s/value=\"$userflag\"/value=\"$userflag\" selected/;

	$signature =~ s/\[br\]/\n/isg;
        $signature =~ s/</&lt;/g;
        $signature =~ s/>/&gt;/g;
        $signature =~ s/\&amp;/\&/isg;
        $signature =~ s/&quot\;/\"/g;
        $interests =~ s/\<br>/\n/isg;
        $interests =~ s/\<p>/\n/isg;
        $interests =~ s/\n+/\n/isg;

        $tempoutput = "<select name=\"newshowemail\">\n<option value=\"yes\">是\n<option value=\"msn\">MSN\n<option value=\"no\">否\n</select>\n";
        $tempoutput =~ s/value=\"$showemail\"/value=\"$showemail\" selected/;

	$output .= qq~
	<tr>
	<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	<form action="$thisprog" method=post name="creator" enctype="multipart/form-data">
	<input type=hidden name="action" value="process">
        <input type=hidden name="oldpassword" value="$inpassword">
	<font color=$fontcolormisc><b>修改 <font color=$fonthighlight>$inmembername</b></font> 的个人资料</td></tr>
	$newpasswordaddon
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>邮件地址：</b><br>请输入有效的邮件地址，这将保证您在论坛中的私人资料。$newpassneeded</td>
	<td bgcolor=$miscbackone><input type=text name="newemailaddress" value="$emailaddress"></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>显示邮件地址</b><br>
	您是否希望在您发表文章之后显示您的邮件？</td>
	<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;
	$membertitle = "" if ($membertitle =~ m/^member$/i);
	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>个人头衔：</b><BR>最大 20 个字符（10个汉字）</td>
	<td bgcolor=$miscbackone><input type=text name="newmembertitle" value="$membertitle" size=10 maxlength=20></td>
	</tr>
	~ if ($editusertitleself eq "on");

	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>江湖门派：</b><BR>最大 20 个字符（10个汉字）</td>
	<td bgcolor=$miscbackone><input type=text name="newjhmp" value="$jhmp" size=10 maxlength=20></td>
	</tr>
	~ if ($editjhmpself eq "on");

        $tempoutput = "<select name=\"newsex\" size=\"1\"><option value=\"no\">保密 </option><option value=\"m\">帅哥 </option><option value=\"f\">美女 </option></select>\n";
        $tempoutput =~ s/value=\"$sex\"/value=\"$sex\" selected/;

	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>性别：</b></td>
	<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"neweducation\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"小学\">小学 </option><option value=\"初中\">初中 </option><option value=\"高中\">高中</option><option value=\"中专\">中专</option><option value=\"大专\">大专</option><option value=\"本科\">本科</option><option value=\"硕士\">硕士</option><option value=\"博士\">博士</option><option value=\"博士后\">博士后</option></select>\n";
        $tempoutput =~ s/value=\"$education\"/value=\"$education\" selected/;

	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>最高学历：</b></td>
	<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"newmarry\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"未婚\">未婚 </option><option value=\"已婚\">已婚 </option><option value=\"离婚\">离婚 </option><option value=\"丧偶\">丧偶 </option></select>\n";
        $tempoutput =~ s/value=\"$marry\"/value=\"$marry\" selected/;

	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>婚姻状况：</b></td>
	<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"newwork\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"计算机业\">计算机业 </option><option value=\"金融业\">金融业 </option><option value=\"商业\">商业 </option><option value=\"服务行业\">服务行业 </option><option value=\"教育业\">教育业 </option><option value=\"学生\">学生 </option><option value=\"工程师\">工程师 </option><option value=\"主管，经理\">主管，经理 </option><option value=\"政府部门\">政府部门 </option><option value=\"制造业\">制造业 </option><option value=\"销售/广告/市场\">销售/广告/市场 </option><option value=\"失业中\">失业中 </option></select>\n";
        $tempoutput =~ s/value=\"$work\"/value=\"$work\" selected/;

	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>职业状况：</b></td>
	<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;
	($year, $month, $day) = split(/\//, $born);
        $tempoutput1 = "<select name=\"newmonth\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option></select>\n";
        $tempoutput1 =~ s/value=\"$month\"/value=\"$month\" selected/;

        $tempoutput2 = "<select name=\"newday\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option><option value=\"13\">13</option><option value=\"14\">14</option><option value=\"15\">15</option><option value=\"16\">16</option><option value=\"17\">17</option><option value=\"18\">18</option><option value=\"19\">19</option><option value=\"20\">20</option><option value=\"21\">21</option><option value=\"22\">22</option><option value=\"23\">23</option><option value=\"24\">24</option><option value=\"25\">25</option><option value=\"26\">26</option><option value=\"27\">27</option><option value=\"28\">28</option><option value=\"29\">29</option><option value=\"30\">30</option><option value=\"31\">31</option></select>\n";
        $tempoutput2 =~ s/value=\"$day\"/value=\"$day\" selected/;

	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>生日：</b>如不想填写，请全部留空。此项可选</td>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><input type="text" name="newyear" size=4 maxlength=4 value="$year">年$tempoutput1月$tempoutput2日</font></td>
	</tr>
	~;
        if ($usersx eq "") {$usersx = "blank"};
        $tempoutput="<SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"sx1\">子鼠</OPTION> <OPTION value=\"sx2\">丑牛</OPTION> <OPTION value=\"sx3\">寅虎</OPTION> <OPTION value=\"sx4\">卯兔</OPTION> <OPTION value=\"sx5\">辰龙</OPTION> <OPTION value=\"sx6\">巳蛇</OPTION> <OPTION value=\"sx7\">午马</OPTION> <OPTION value=\"sx8\">未羊</OPTION> <OPTION value=\"sx9\">申猴</OPTION> <OPTION value=\"sx10\">葵鸡</OPTION> <OPTION value=\"sx11\">戌狗</OPTION> <OPTION value=\"sx12\">亥猪</OPTION></SELECT>\n";
        $tempoutput =~ s/value=\"$usersx\"/value=\"$usersx\" selected/;
        $output.=qq~
        <SCRIPT language=javascript>
        function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
        </SCRIPT>
        <tr><td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>所属生肖：</b>请选择你所属的生肖。<br>如果你正确输入了生日的话，那么此项无效！</td>
        <td bgcolor=$miscbackone>$tempoutput<IMG border=0 name=usersxs src=$imagesurl/sx/$usersx.gif align=absmiddle>
        </TD></TR>
	~;
        if ($userxz eq "") {$userxz = "blank"};
        $tempoutput="<SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"z1\">白羊座(3月21--4月19日)</OPTION> <OPTION value=\"z2\">金牛座(4月20--5月20日)</OPTION> <OPTION value=\"z3\">双子座(5月21--6月21日)</OPTION> <OPTION value=\"z4\">巨蟹座(6月22--7月22日)</OPTION> <OPTION value=\"z5\">狮子座(7月23--8月22日)</OPTION> <OPTION value=\"z6\">处女座(8月23--9月22日)</OPTION> <OPTION value=\"z7\">天秤座(9月23--10月23日)</OPTION> <OPTION value=\"z8\">天蝎座(10月24--11月21日)</OPTION> <OPTION value=\"z9\">射手座(11月22--12月21日)</OPTION> <OPTION value=\"z10\">魔羯座(12月22--1月19日)</OPTION> <OPTION value=\"z11\">水瓶座(1月20--2月18日)</OPTION> <OPTION value=\"z12\">双鱼座(2月19--3月20日)</OPTION></SELECT>\n";
        $tempoutput =~ s/value=\"$userxz\"/value=\"$userxz\" selected/;
        $output.=qq~
        <SCRIPT language=javascript>
        function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
        </SCRIPT>
        <tr><td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>所属星座：</b>请选择你所属的星座。<br>如果你正确输入了生日的话，那么此项无效！</td>
        <td bgcolor=$miscbackone>$tempoutput<IMG border=0 height=15 name=userxzs src=$imagesurl/star/$userxz.gif width=15 align=absmiddle>
        </TD></TR>
	~;

	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>主页地址：</b><br>如果您有主页，请输入主页地址。此项可选</td>
	<td bgcolor=$miscbackone><input type=text name="newhomepage" value="$homepage"></td>
	</tr>
	<tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>OICQ 号：</b><br>如果您有 OICQ，请输入号码。此项可选</td>
	<td bgcolor=$miscbackone><input type=text name="newaolname" value="$aolname"></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ICQ 号：</b><br>如果您有 ICQ，请输入号码。此项可选</td>
	<td bgcolor=$miscbackone><input type=text name="newicqnumber" value="$icqnumber"></td>
	</tr>$flaghtml<tr>
<script src=$imagesurl/images/comefrom.js></script>
<body onload="init()">
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>来自：</b><br>请输入您所在的地方。此项可选</td>
	<td bgcolor=$miscbackone>
省份 <select name="province" onChange = "select()"></select>　城市 <select name="city" onChange = "select()"></select><br>
我在 <input type=text name="newlocation" value="$location" maxlength=12 size=20 style="font-weight: bold">　不能超过12个字符（6个汉字）</td>
	</tr><tr>
        ~;
        $timedifference = 0 if ($timedifference eq '');
        $tempoutput = "<select name=\"timedifference\"><option value=\"-23\">- 23</option><option value=\"-22\">- 22</option><option value=\"-21\">- 21</option><option value=\"-20\">- 20</option><option value=\"-19\">- 19</option><option value=\"-18\">- 18</option><option value=\"-17\">- 17</option><option value=\"-16\">- 16</option><option value=\"-15\">- 15</option><option value=\"-14\">- 14</option><option value=\"-13\">- 13</option><option value=\"-12\">- 12</option><option value=\"-11\">- 11</option><option value=\"-10\">- 10</option><option value=\"-9\">- 9</option><option value=\"-8\">- 8</option><option value=\"-7\">- 7</option><option value=\"-6\">- 6</option><option value=\"-5\">- 5</option><option value=\"-4\">- 4</option><option value=\"-3\">- 3</option><option value=\"-2\">- 2</option><option value=\"-1\">- 1</option><option value=\"0\">0</option><option value=\"1\">+ 1</option><option value=\"2\">+ 2</option><option value=\"3\">+ 3</option><option value=\"4\">+ 4</option><option value=\"5\">+ 5</option><option value=\"6\">+ 6</option><option value=\"7\">+ 7</option><option value=\"8\">+ 8</option><option value=\"9\">+ 9</option><option value=\"10\">+ 10</option><option value=\"11\">+ 11</option><option value=\"12\">+ 12</option><option value=\"13\">+ 13</option><option value=\"14\">+ 14</option><option value=\"15\">+ 15</option><option value=\"16\">+ 16</option><option value=\"17\">+ 17</option><option value=\"18\">+ 18</option><option value=\"19\">+ 19</option><option value=\"20\">+ 20</option><option value=\"21\">+ 21</option><option value=\"22\">+ 22</option><option value=\"23\">+ 23</select>";
        $tempoutput =~ s/value=\"$timedifference\"/value=\"$timedifference\" selected/;

     $output .= qq~
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>时差：</b><br>
	服务器所在时区：$basetimes<br>如果您所在的位置和服务器有时差，请输入。<br>以后您看到所有的时间将按照您所在的地区时间显示。</td>
	<td bgcolor=$miscbackone>$tempoutput</td>
	</tr><tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>自我简介： </b><BR>不能超过 <B>$maxinsline</B> 行，也不能超过 <B>$maxinslegth</B> 个字符<br><br>您可以输入您的个人简介。此项可选</td>
	<td bgcolor=$miscbackone><textarea name="newinterests" cols="60" rows="5">$interests</textarea></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font color=$fontcolormisc><b>签名：</b><br>不能超过 <B>$maxsignline</B> 行，也不能超过 <B>$maxsignlegth</B> 个字符
	<br><br>不能使用 HTML 标签<br>可以使用 <a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LB5000 标签</a><BR>
	<li>贴图标签　: <b>$signpicstates</b><li>Flash 标签: <b>$signflashstates</b><li>音乐标签　: <b>$signsoundstates</b><li>文字大小　: <b>$signfontsizestates</b>
	</td>
	<td bgcolor=$miscbackone><textarea name="newsignature" cols="60" rows="8">$signature</textarea></td>
	</tr>
    $avatarhtml
    <tr>
	<td colspan=2 bgcolor=$miscbacktwo align=center><input type=submit value="提 交" name=submit></td>
	<input type=hidden name="membername" value="$inmembername"></form></tr></table></td></tr></table>
	~;
	} # end modify routine
	############################## save profile modification
	sub savemodify {
        &getmember("$inmembername");
	    if ("$userregistered" eq "no") {&error("修改资料&没有此用户名！"); }
	    if ("$oldpassword" ne "$password") {&error("修改资料&密码错误！"); }
	    $newpassword1           = $query -> param('newpassword1');
	    $newpassword2           = $query -> param('newpassword2');
	    $newshowemail           = $query -> param('newshowemail');
	    $newhomepage            = $query -> param('newhomepage');
	    $newaolname             = $query -> param('newaolname');
	    $newicqnumber           = $query -> param('newicqnumber');
	    $newlocation            = $query -> param('newlocation');
	    $newinterests           = $query -> param('newinterests');
	    $newtimedifference      = $query -> param('newtimedifference');
	    $newpersonalavatar      = $query -> param('newpersonalavatar');
	    $newpersonalwidth       = $query -> param('newpersonalwidth');
	    $newpersonalheight      = $query -> param('newpersonalheight');
	    $newemailaddress        = $query -> param('newemailaddress');
	    $newmembertitle         = $query -> param('newmembertitle');
	    $newjhmp                = $query -> param('newjhmp');
	    $inuserflag		    = $query -> param('userflag');
	    $inuserxz		    = $query -> param('userxz');
            $inusersx		    = $query -> param('usersx');

	    $newyear        = $query -> param('newyear');
	    $newmonth       = $query -> param('newmonth');
	    $newday         = $query -> param('newday');
	    $newsex         = $query -> param('newsex');
	    $neweducation   = $query -> param('neweducation');
	    $newmarry       = $query -> param('newmarry');
	    $newwork        = $query -> param('newwork');

	    $newsignature           = $query -> param('newsignature');
            $inuseravatar           = $query -> param('useravatar');

            $newsignature           = &unHTML("$newsignature");
	    $newpassword            = &cleanarea("$newpassword");
	    $newshowemail           = &cleanarea("$newshowemail");
	    $newhomepage            = &cleanarea("$newhomepage");
	    $newaolname             = &cleanarea("$newaolname");
	    $newicqnumber           = &cleanarea("$newicqnumber");
	    $newlocation            = &cleanarea("$newlocation");
	    $newinterests           = &cleanarea("$newinterests");
	    $newtimedifference      = &cleanarea("$newtimedifference");
	    $newpersonalavatar      = &cleanarea("$newpersonalavatar");
	    $newpersonalwidth       = &cleanarea("$newpersonalwidth");
	    $newpersonalheight      = &cleanarea("$newpersonalheight");
	    $newemailaddress        = &cleanarea("$newemailaddress");
            $inuseravatar           = &cleaninput("$inuseravatar");
	    $newmembertitle         = &cleanarea("$newmembertitle");
	    $newjhmp       	    = &cleanarea("$newjhmp");
	    $inuserflag       	    = &cleanarea("$inuserflag");
	    $inuserxz       	    = &cleanarea("$inuserxz");
            $inusersx       	    = &cleanarea("$inusersx");

        if ($newsignature) {
        $newsignature =~ s/\t//g;
        $newsignature =~ s/\r//g;
        $newsignature =~ s/  / /g;
        $newsignature =~ s/\n\n/\n\&nbsp;\n/isg;
        $newsignature =~ s/\n/\[br\]/isg;
        $newsignature =~ s/\[br\]\[br\]/\[br\]\&nbsp;\[br\]/isg;
        }

        if ($newinterests) {
        $newinterests =~ s/<P>/<BR>/ig;
        $newinterests =~ s/<BR><BR>/<BR>/ig;
        }
	    # make sure its a valid form

	    @testsig = split(/\[br\]/,$newsignature);
	    $siglines = @testsig;

    if(length($newlocation)>12) { &error("修改资料&来自地区过长，请不要超过12个字符（6个汉字）！"); }
    if ($siglines > $maxsignline) { &error("修改资料&对不起，在您的签名中只允许有 $maxsignline 行！"); }
    if (length($newsignature) > $maxsignlegth) {print header(-charset=>gb2312);&error("修改资料&对不起，签名不能超过 $maxsignlegth 字符！"); }
    if($newpassword1 =~ /\t/) {print header(-charset=>gb2312);&error("修改资料&警告！请不要在用户资料中使用特殊字符！"); }

    if(length($newmembertitle)>20) { &error("修改资料&个人头衔过长，请不要超过20个字符（10个汉字）！"); }
    $newmembertitle =~ s/\t//isg;
    if(length($newjhmp)>20) { &error("修改资料&江湖门派过长，请不要超过20个字符（10个汉字）！"); }
    $newjhmp =~ s/\t//isg;

    @testins = split(/\<br\>/,$newinterests);
    $inslines = @testins;
    if ($inslines > $maxinsline) { print header(-charset=>gb2312);&error("用户注册&对不起，个人简介只允许有 $maxinsline 行！"); }

    if (length($newinterests) > $maxinslegth) {&error("修改资料&对不起，个人简介不能超过 $maxinslegth 字符！"); }

    $newyear =~ s/\D//g;
    if (($newyear eq "")||($newmonth eq "")||($newday eq "")) {
    	$newyear  = "";
    	$newmonth = "";
    	$newday   = "";
    }
    $newborn = "$newyear/$newmonth/$newday";

    if ($newborn ne "//") { #开始自动判断星座
    	if ($newyear-1900 < 0) {$inusersx = "";}	# 无效年份
    	else {
    		$inusersx = "sx".(($newyear-1900) % 12 + 1);
    	}
    	if ($newmonth eq "01") {
    	    if (($newday >= 1)&&($newday <=19)) {
    	        $inuserxz = "z10";
    	    }
    	    else {
    	        $inuserxz = "z11";
    	    }
    	}
        elsif ($newmonth eq "02") {
    	    if (($newday >= 1)&&($newday <=18)) {
    	        $inuserxz = "z11";
    	    }
    	    else {
    	        $inuserxz = "z12";
    	    }
        }
        elsif ($newmonth eq "03") {
    	    if (($newday >= 1)&&($newday <=20)) {
    	        $inuserxz = "z12";
    	    }
    	    else {
    	        $inuserxz = "z1";
    	    }

        }
        elsif ($newmonth eq "04") {
    	    if (($newday >= 1)&&($newday <=19)) {
    	        $inuserxz = "z1";
    	    }
    	    else {
    	        $inuserxz = "z2";
    	    }
        }
        elsif ($newmonth eq "05") {
    	    if (($newday >= 1)&&($newday <=20)) {
    	        $inuserxz = "z2";
    	    }
    	    else {
    	        $inuserxz = "z3";
    	    }
        }
        elsif ($newmonth eq "06") {
    	    if (($newday >= 1)&&($newday <=21)) {
    	        $inuserxz = "z3";
    	    }
    	    else {
    	        $inuserxz = "z4";
    	    }
        }
        elsif ($newmonth eq "07") {
    	    if (($newday >= 1)&&($newday <=22)) {
    	        $inuserxz = "z4";
    	    }
    	    else {
    	        $inuserxz = "z5";
    	    }
        }
        elsif ($newmonth eq "08") {
    	    if (($newday >= 1)&&($newday <=22)) {
    	        $inuserxz = "z5";
    	    }
    	    else {
    	        $inuserxz = "z6";
    	    }
        }
        elsif ($newmonth eq "09") {
    	    if (($newday >= 1)&&($newday <=22)) {
    	        $inuserxz = "z6";
    	    }
    	    else {
    	        $inuserxz = "z7";
    	    }
        }
        elsif ($newmonth eq "10") {
    	    if (($newday >= 1)&&($newday <=23)) {
    	        $inuserxz = "z7";
    	    }
    	    else {
    	        $inuserxz = "z8";
    	    }
        }
        elsif ($newmonth eq "11") {
    	    if (($newday >= 1)&&($newday <=21)) {
    	        $inuserxz = "z8";
    	    }
    	    else {
    	        $inuserxz = "z9";
    	    }
        }
        elsif ($newmonth eq "12") {
    	    if (($newday >= 1)&&($newday <=21)) {
    	        $inuserxz = "z9";
    	    }
    	    else {
    	        $inuserxz = "z10";
    	    }
        }

    }

    if (($newpersonalavatar)&&($newpersonalwidth)&&($newpersonalheight)) {
        if ($newpersonalavatar !~ /^http:\/\/[\w\W]+\.[\w\W]+$/) {
            print header(-charset=>gb2312);&error("用户注册&自定义头像的 URL 地址有问题！");
        }
        if (($newpersonalavatar !~ /\.gif$/isg)&&($newpersonalavatar !~ /\.jpg$/isg)&&($newpersonalavatar !~ /\.png$/isg)&&($newpersonalavatar !~ /\.bmp$/isg)&&($newpersonalavatar !~ /\.swf$/isg)) {
            print header(-charset=>gb2312);&error("用户注册&自定义头像必须为 PNG、GIF、JPG、BMP、SWF 格式") ;
        }
        if (($newpersonalwidth < 20)||($newpersonalwidth > $maxposticonwidth)) {
           &error("用户注册&对不起，自定义图像宽度必须在 20 -- $maxposticonwidth 像素之间！");
        }
        if (($newpersonalheight < 20)||($newpersonalheight > $maxposticonheight)) {
           &error("用户注册&对不起，自定义图像高度必须在 20 -- $maxposticonheight 像素之间！");
        }
        $inuseravatar = "noavatar";
    }
   else {
    	if ($addme){
    	    $newpersonalavatar="";
    	}else{
    	    $newpersonalavatar=""; $newpersonalwidth=""; $newpersonalheight="";
    	}
        $memberfiletitle = $inmembername;
        $memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;
    	unlink ("${imagesdir}usravatars/$memberfiletitle.gif");
    	unlink ("${imagesdir}usravatars/$memberfiletitle.png");
    	unlink ("${imagesdir}usravatars/$memberfiletitle.jpg");
    	unlink ("${imagesdir}usravatars/$memberfiletitle.swf");
    	unlink ("${imagesdir}usravatars/$memberfiletitle.bmp");
   } #清除自定义头像信息

	    if ($newemailaddress eq "") { $blankfields = "yes"; }
	    if ($newpassword1 ne $newpassword2)  {&error("修改资料&你输入的两次密码不相同，如果你不想修改密码，请保持这两项为空！"); }

	    if (($newpassword1 ne "")&&($newpassword2 ne "")) {
    		if(length($newpassword1)<6) { &error("用户注册&密码太短了，请更换！密码必须 6 位以上！"); }
#    		if ($newpassword1 =~ /^[0-9]+$/) { &error("用户注册&密码请不要全部为数字，请更换！"); }
	    	$newpassword = $newpassword1;
	    }
	    else { $newpassword = $oldpassword; }

	    if ($blankfields) {
	       &error("修改资料&请输入用户名、邮件地址，这些是必需的！");
	        }

	        $memberfiletitle = $inmembername;
	        $memberfiletitle =~ s/ /\_/isg;
		$memberfiletitle =~ tr/A-Z/a-z/;

if ($addme) {
	if (($newpersonalwidth < 20)||($newpersonalwidth > $maxposticonwidth)) {
             print header(-charset=>gb2312);&error("用户注册$personalwidth&对不起，自定义图像宽度必须在 20 -- $maxposticonwidth 像素之间！");
        }
        if (($newpersonalheight < 20)||($newpersonalheight > $maxposticonheight)) {
             print header(-charset=>gb2312);&error("用户注册$personalheight&对不起，自定义图像高度必须在 20 -- $maxposticonheight 像素之间！");
        }


#modified by GDD of Leoboard Team
#Begin of part
	my $filename =$query->uploadInfo($addme);
	my $fileexp;
	$fileexp = ($filename =~ /\.jpe?g\s*$/i) ? 'jpg'
		  :($filename =~ /\.gif\s*$/i)  ? 'gif'
		  :($filename =~ /\.png\s*$/i)  ? 'png'
		  :($filename =~ /\.swf\s*$/i)  ? 'swf'
		  :($filename =~ /\.bmp\s*$/i)  ? 'bmp'
		  :undef;
	$maxuploadava = 200 if (($maxuploadava eq "")||($maxuploadava < 1));
	if (($fileexp eq "swf")&&($flashavatar ne "yes")) {
	    print header(-charset=>gb2312);
	    &error("不支持你所上传的图片，请重新选择！&仅支持 GIF，JPG，PNG，BMP 类型!");
	}

	if (!defined $fileexp) {
	    print header(-charset=>gb2312);
	    &error("不支持你所上传的图片，请重新选择！&仅支持 GIF，JPG，PNG，BMP，SWF 类型!");
	}

	my $filesize=0;
	my $buffer;
 	open (FILE,">${imagesdir}usravatars/$memberfiletitle.$fileexp");
	binmode (FILE);
	while ((($buffer=$query->readUploadFile($addme,4096)))&&!($filesize>$maxuploadava)) {
	print FILE $buffer;
	$filesize=$filesize+4;
	}
 	close (FILE);
	if ($filesize>$maxuploadava) {
            unlink ("${imagesdir}usravatars/$memberfiletitle.$fileexp");
	    &error("上传出错&上传文件大小超过$maxuploadava，请重新选择！");
	}
#End of part


$inuseravatar="noavatar";
$newpersonalavatar="$imagesurl/usravatars/$memberfiletitle.$fileexp";
}

	    if($newemailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) {print header(-charset=>gb2312);&error("注册&Email 地址非法！"); }
	    $newemailaddress =~ s/[\a\f\n\e\0\r\t\`\~\!\#\$\%\^\&\*\(\)\=\+\\\[\]\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
	    &getmember("$inmembername");


$filetomakeopen = "${lbdir}data/lbmember1.cgi";
&winlock($filetomakeopen);
open (MEMFILE, "$filetomakeopen");
flock (MEMFILE, 1) if ($OS_USED eq "Unix");
@allmembers = <MEMFILE>;
close (MEMFILE);

if (open (MEMFILE, ">$filetomakeopen")) {
flock (MEMFILE, 2) if ($OS_USED eq "Unix");
foreach (@allmembers) {
    chomp $_;
    ($user, $mail) = split(/\t/,$_);
    if ($user eq $inmembername){
	print MEMFILE "$inmembername\t$newemailaddress\t\n";
    }
    else {
	print MEMFILE "$_\n";
    }
}
close (MEMFILE);
}
&winunlock($filetomakeopen);


	    if (($passwordverification eq "yes") && ($emailfunctions ne "off") && ($newemailaddress ne $emailaddress)) {

	        $seed = int(rand 100000);
	        $password = crypt($seed, aun);
	        $password =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	        $password =~ s/\.//g;
            	$password =~ s/\|//g;
	        $newpassword = substr($password, 0, 7);

            # Sort out new cookies

            $passcookie = cookie(-name    =>   "apasswordcookie",
                                 -value   =>   "",
   		                 -path    =>   "$cookiepath/",
                                 -expires =>   "-1d");

	        ### send the email


	                $to = $newemailaddress;
	                $from = $adminemail_out;
	                $subject = "您改变了在 $boardname 中注册的邮件地址";

	                $message .= "\n";
	                $message .= "$homename\n";
	                $message .= "$boardurl/$forumsummaryprog\n\n\n";
	                $message .= "------------------------------------\n";
	                $message .= "您的用户名、新密码如下：\n\n";
	                $message .= "用户名： $inmembername\n";
	                $message .= "新密码： $newpassword\n\n\n";
	                $message .= "请注意：用户名和密码区分大小写！\n\n";
	                $message .= "------------------------------------\n";

	                &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);


	        } # end new password request

if ($editusertitleself eq "on") {
    $newmembertitle = "Member" if ($newmembertitle eq "");
    $membertitle = $newmembertitle;
}

if ($editjhmpself eq "on") {
    $jhmp = $newjhmp;
}

	if (($inmembername ne "")&&($newpassword ne "")) {
	        $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
	        &winlock($filetomake) if ($OS_USED eq "Nt");
	        if (open(FILE, ">$filetomake")) {
	        flock(FILE, 2) if ($OS_USED eq "Unix");
	        print FILE "$inmembername\t$newpassword\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$newemailaddress\t$newshowemail\t$ipaddress\t$newhomepage\t$newaolname\t$newicqnumber\t$newlocation\t$newinterests\t$joineddate\t$lastpostdate\t$newsignature\t$newtimedifference\t$privateforums\t$inuseravatar\t$inuserflag\t$inuserxz\t$inusersx\t$newpersonalavatar\t$newpersonalwidth\t$newpersonalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$newsex\t$neweducation\t$newmarry\t$newwork\t$newborn\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t";
	        close(FILE);
	        }
	        &winunlock($filetomake) if ($OS_USED eq "Nt");
	}
		if ($newsignature) {
		  $previewsig = &signlbcode($newsignature);
		}

        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $previewsig=~ s/$bad/$good/isg;
                }
            }
	        $output .= qq~
	            <tr>
	            <td bgcolor=$miscbacktwo valign=middle align=center><font color=$fontcolormisc><b>个人信息已经保存</b></font></td></tr>
	            <tr>
	            <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>
	            具体情况：
	            <ul>
	            <li><a href="$forumsummaryprog">返回论坛首页</a>
	            </ul>
  	  	    </td></tr>
		    <tr>
		       <td bgcolor=$miscbackone valign=middle><font color=$postfontcolor>
           		你的新签名预览：<br>
			<hr><br>
			$previewsig
			<br>
			<hr>
			</font>
			</td>
			</tr>
	            </table></td></tr></table>
	            ~;

	            if (($passwordverification eq "yes") && ($emailfunctions ne "off") && ($newemailaddress ne $emailaddress)) {
	            $output =~ s/具体情况：/<B>由于你修改了 Email，所以你直接修改的密码是无效的，而你的新密码已经通过 Email 发送给你了！<\/B>/g;
	            }

	} # end save details.
	########### Lets stop people trying to get the Admin's password.
	sub blocked {
	    if ($inmembername eq "") { $inusername = "客人"; }
	    $ipaddress = "$ENV{'REMOTE_ADDR'}($ENV{'HTTP_X_FORWARDED_FOR'})";
	    $inmembername =~ s/\_/ /g;


	    $output .= qq~
	    <p>
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font color=$fontcolormisc><b><font color=$fonthighlight>不允许发送管理员的密码</b></font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone><font color=$fontcolormisc>
	    <b>从安全角度考虑，坛主和总版主的密码是锁定的，不允许通过 Email 来寄送。</b><p>
	    为了防止有 hacker 攻击服务器，你的 IP 地址 $ipaddress 已经被记入，并通过 Email 发送给管理员了。<br>
	    你用的浏览器： $ENV{'HTTP_USER_AGENT'}<p>
	    如果你不是故意的，你不要过于担心。<p><p>
	    ---- 山鹰糊,花无缺  <a href=http://www.cgier.com/ target=_blank>http://www.cgier.com/</a>
	    </td></tr></table></td></tr></table>
	    ~;

	                $message .= "\n";
	                $message .= "$boardname\n";
	                $message .= "$boardurl/$forumsummaryprog\n\n";
	                $message .= "--------------------------------------------------------\n";
	                $message .= "这是自动发送的邮件。\n\n";
	                $message .= "很可能是有人想通过指定的电子邮件来得到您的超级密码！\n";
	                $message .= "这仅仅是一封警告邮件，他们是不能通过这种方式得到密码的。\n";
	                $message .= "--------------------------------------------------------\n\n";
	                $message .= "注册名： $inmembername\n";
	                $message .= "IP地址： $ipaddress\n\n";
	                $message .= "---------------------------------------------------------\n";
	                $to = $adminemail_in;
	                $from = $adminemail_out;
	                $subject = "警告！！可能是 hacker 在攻击您的论坛！";
	                &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message );

	                $output =~ s/用户资料/警告！/g;
	                           print header(-charset=>gb2312);
	                            &output(
	                            -Title   => $boardname,
	                            -ToPrint => $output,
	                            -Version => $versionnumber
	                            );
	    }
