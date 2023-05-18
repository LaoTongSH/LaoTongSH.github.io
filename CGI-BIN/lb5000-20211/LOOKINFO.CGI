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
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/membertitles.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "lookinfo.cgi";

    $query = new LBCGI;
&ipbanned; #封杀一些 ip

	@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }



$action      =  $PARAM{'action'};
$inforum     =  $PARAM{'forum'};
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));
$inmember            = $query -> param('member');
$inmembername        = $query -> param("membername");
$inpassword          = $query -> param("password");
$oldpassword         = $query -> param("oldpassword");
$action              = &cleaninput("$action");
$inmember            = &cleaninput("$inmember");
$inmembername        = &cleaninput("$inmembername");
$inpassword          = &cleaninput("$inpassword");

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

    if ($inmembername eq "") { $inmembername = "客人"; }
    else {
        &getmember("$inmembername");
    }   

&mischeader("论坛信息");

print header(-charset=>gb2312);

$output .= qq~
    <html>
    <head>
    <title>$forumname配色列表</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
    <style type="text/css">
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}
		
	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}
	        
		.t     {	LINE-HEIGHT: 1.4			}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		DIV	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
input {border-width: 1; border-color: #000000; font-family: 宋体; font-size: 9pt; font-style: bold;}
textarea {border-width: 1; border-color: #000000; background-color: #efefef; font-family: 宋体; font-size: 9pt; font-style: bold;}
select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: 宋体; font-size: 9pt; font-style: bold;}
    </style></head>
    <body $lbbody>
    ~;
          
            my %Mode = (             
            'style'               =>    \&styleform,   
            );

            if($Mode{$action}) { 
               $Mode{$action}->();
               }
##################################################################################
sub styleform {
&title;

$output .= qq~

         <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
             <tr>
               <td width=30% rowspan=2 valign=top>$forumgraphic
               </td>
               <td valign=top>
        <img src=$imagesurl/images/closedfold.gif width=15 height=11>　<a href=$forumsummaryprog>$boardname</a><br>
        <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>　查看论坛信息
      </td></tr></table><table width=$tablewidth border=0 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0 ><tr><td><div align="center">用 户 等 级</div></td></tr></table>
        <table width=$tablewidth border=1 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0 ><br>
        <tr><td bgcolor=$forumcolorone>级别名称</td><td  bgcolor=$forumcolortwo>发贴数量</td><td bgcolor=$forumcolorone>代表图片</td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle0</td><td  bgcolor=$forumcolortwo>0</td><td bgcolor=$forumcolorone>没有图片</td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle1</td><td  bgcolor=$forumcolortwo>$mpostmark1</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic1></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle2</td><td  bgcolor=$forumcolortwo>$mpostmark2</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic2></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle3</td><td  bgcolor=$forumcolortwo>$mpostmark3</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic3></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle4</td><td  bgcolor=$forumcolortwo>$mpostmark4</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic4></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle5</td><td  bgcolor=$forumcolortwo>$mpostmark5</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic5></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle6</td><td  bgcolor=$forumcolortwo>$mpostmark6</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic6></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle7</td><td  bgcolor=$forumcolortwo>$mpostmark7</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic7></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle8</td><td  bgcolor=$forumcolortwo>$mpostmark8</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic8></td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle9</td><td  bgcolor=$forumcolortwo>$mpostmark9</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic9></td><tr>
	~;
if ($mtitle10 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle10</td><td  bgcolor=$forumcolortwo>$mpostmark10</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic10></td><tr>
	~;
}
if ($mtitle11 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle11</td><td  bgcolor=$forumcolortwo>$mpostmark11</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic11></td><tr>
	~;
}
if ($mtitle12 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle12</td><td  bgcolor=$forumcolortwo>$mpostmark12</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic12></td><tr>
	~;
}
if ($mtitle13 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle13</td><td  bgcolor=$forumcolortwo>$mpostmark13</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic13></td><tr>
	~;
}
if ($mtitle14 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle14</td><td  bgcolor=$forumcolortwo>$mpostmark14</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic14></td><tr>
	~;
}
if ($mtitle15 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle15</td><td  bgcolor=$forumcolortwo>$mpostmark15</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic15></td><tr>
	~;
}
if ($mtitle16 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle16</td><td  bgcolor=$forumcolortwo>$mpostmark16</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic16></td><tr>
	~;
}
if ($mtitle17 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle17</td><td  bgcolor=$forumcolortwo>$mpostmark17</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic17></td><tr>
	~;
}
if ($mtitle18 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle18</td><td  bgcolor=$forumcolortwo>$mpostmark18</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic18></td><tr>
	~;
}
if ($mtitle19 ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitle19</td><td  bgcolor=$forumcolortwo>$mpostmark19</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphic19></td><tr>
	~;
}
if ($mtitlemax ne "") {
	$output .= qq~<tr><td bgcolor=$forumcolorone>$mtitlemax</td><td  bgcolor=$forumcolortwo>$mpostmarkmax</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$mgraphicmax></td><tr>
	~;
}
if ($motitle ne "") {
	$output .= qq~ <tr><td bgcolor=$forumcolorone>$motitle</td><td  bgcolor=$forumcolortwo>不受限制</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$modgraphic></td><tr>
~;
}
if ($smotitle ne "") {
	$output .= qq~ <tr><td bgcolor=$forumcolorone>$smotitle</td><td  bgcolor=$forumcolortwo>不受限制</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$smodgraphic></td><tr>
~;
}
$output .= qq~
	<tr><td bgcolor=$forumcolorone>$adtitle</td><td  bgcolor=$forumcolortwo>不受限制</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$admingraphic></td><tr>
</table><br><br>
<table width=$tablewidth border=0 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0 ><tr><td><div align="center">社 区 信 息</div></td></tr></table>
<table width=$tablewidth border=1 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0 ><br>
        <tr><td bgcolor=$forumcolorone>每推荐一个人增加的货币：</td><td  bgcolor=$forumcolortwo>$addtjhb</td><tr>
        <tr><td bgcolor=$forumcolorone>每推荐一个人增加的经验：</td><td  bgcolor=$forumcolortwo>$addtjjy</td><tr>
        <tr><td bgcolor=$forumcolorone>每推荐一个人增加的魅力：</td><td  bgcolor=$forumcolortwo>$addtjml</td><tr>
        <tr><td bgcolor=$forumcolorone>每发一个主题折算的经验数：</td><td  bgcolor=$forumcolortwo>$ttojy</td><tr>
        <tr><td bgcolor=$forumcolorone>每发一个回复折算的经验数：</td><td  bgcolor=$forumcolortwo>$rtojy</td><tr>
        <tr><td bgcolor=$forumcolorone>每登陆一次折算的经验数：</td><td  bgcolor=$forumcolortwo>$ltojy</td><tr>
        <tr><td bgcolor=$forumcolorone>被删除一个贴子减去的经验：</td><td  bgcolor=$forumcolortwo>$deljingyan</td><tr>
        <tr><td bgcolor=$forumcolorone width="50%">新用户注册分配的货币：</td><td  bgcolor=$forumcolortwo>$joinmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>发表新主题增加的货币：</td><td  bgcolor=$forumcolortwo>$addmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>发表新回复增加的货币：</td><td  bgcolor=$forumcolortwo>$replymoney</td><tr>
        <tr><td bgcolor=$forumcolorone>每次登陆时增加的货币：</td><td  bgcolor=$forumcolortwo>$loginmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>被删除贴子减少的货币：</td><td  bgcolor=$forumcolortwo>$delmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>新用户注册分配的经验：</td><td  bgcolor=$forumcolortwo>$joinjingyan</td><tr>
        <tr><td bgcolor=$forumcolorone>新用户注册分配的魅力：</td><td  bgcolor=$forumcolortwo>$joinml</td><tr>
        <tr><td bgcolor=$forumcolorone>发表新主题增加的魅力：</td><td  bgcolor=$forumcolortwo>$addml</td><tr>
        <tr><td bgcolor=$forumcolorone>发表新回复增加的魅力：</td><td  bgcolor=$forumcolortwo>$replyml</td><tr>
        <tr><td bgcolor=$forumcolorone>每次登陆时增加的魅力：</td><td  bgcolor=$forumcolortwo>$loginml</td><tr>
        <tr><td bgcolor=$forumcolorone>被删除贴子减少的魅力：</td><td  bgcolor=$forumcolortwo>$delml</td><tr>
</table>
~;
}



$output .= qq~</body></html>~;
&output(
     -Title   => "$boardname - 查看论坛信息", 
     -ToPrint => $output, 
     -Version => $versionnumber 
    );
exit;

