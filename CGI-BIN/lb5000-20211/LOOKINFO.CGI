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
&ipbanned; #��ɱһЩ ip

	@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }



$action      =  $PARAM{'action'};
$inforum     =  $PARAM{'forum'};
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
$inmember            = $query -> param('member');
$inmembername        = $query -> param("membername");
$inpassword          = $query -> param("password");
$oldpassword         = $query -> param("oldpassword");
$action              = &cleaninput("$action");
$inmember            = &cleaninput("$inmember");
$inmembername        = &cleaninput("$inmembername");
$inpassword          = &cleaninput("$inpassword");

$inselectstyle   = $query->cookie("selectstyle");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

    if ($inmembername eq "") { $inmembername = "����"; }
    else {
        &getmember("$inmembername");
    }   

&mischeader("��̳��Ϣ");

print header(-charset=>gb2312);

$output .= qq~
    <html>
    <head>
    <title>$forumname��ɫ�б�</title>
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
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		DIV	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
input {border-width: 1; border-color: #000000; font-family: ����; font-size: 9pt; font-style: bold;}
textarea {border-width: 1; border-color: #000000; background-color: #efefef; font-family: ����; font-size: 9pt; font-style: bold;}
select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: ����; font-size: 9pt; font-style: bold;}
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
        <img src=$imagesurl/images/closedfold.gif width=15 height=11>��<a href=$forumsummaryprog>$boardname</a><br>
        <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>���鿴��̳��Ϣ
      </td></tr></table><table width=$tablewidth border=0 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0 ><tr><td><div align="center">�� �� �� ��</div></td></tr></table>
        <table width=$tablewidth border=1 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0 ><br>
        <tr><td bgcolor=$forumcolorone>��������</td><td  bgcolor=$forumcolortwo>��������</td><td bgcolor=$forumcolorone>����ͼƬ</td><tr>
	<tr><td bgcolor=$forumcolorone>$mtitle0</td><td  bgcolor=$forumcolortwo>0</td><td bgcolor=$forumcolorone>û��ͼƬ</td><tr>
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
	$output .= qq~ <tr><td bgcolor=$forumcolorone>$motitle</td><td  bgcolor=$forumcolortwo>��������</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$modgraphic></td><tr>
~;
}
if ($smotitle ne "") {
	$output .= qq~ <tr><td bgcolor=$forumcolorone>$smotitle</td><td  bgcolor=$forumcolortwo>��������</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$smodgraphic></td><tr>
~;
}
$output .= qq~
	<tr><td bgcolor=$forumcolorone>$adtitle</td><td  bgcolor=$forumcolortwo>��������</td><td bgcolor=$forumcolorone><img src=$imagesurl/images/$admingraphic></td><tr>
</table><br><br>
<table width=$tablewidth border=0 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0 ><tr><td><div align="center">�� �� �� Ϣ</div></td></tr></table>
<table width=$tablewidth border=1 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0 ><br>
        <tr><td bgcolor=$forumcolorone>ÿ�Ƽ�һ�������ӵĻ��ң�</td><td  bgcolor=$forumcolortwo>$addtjhb</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ�Ƽ�һ�������ӵľ��飺</td><td  bgcolor=$forumcolortwo>$addtjjy</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ�Ƽ�һ�������ӵ�������</td><td  bgcolor=$forumcolortwo>$addtjml</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ��һ����������ľ�������</td><td  bgcolor=$forumcolortwo>$ttojy</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ��һ���ظ�����ľ�������</td><td  bgcolor=$forumcolortwo>$rtojy</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ��½һ������ľ�������</td><td  bgcolor=$forumcolortwo>$ltojy</td><tr>
        <tr><td bgcolor=$forumcolorone>��ɾ��һ�����Ӽ�ȥ�ľ��飺</td><td  bgcolor=$forumcolortwo>$deljingyan</td><tr>
        <tr><td bgcolor=$forumcolorone width="50%">���û�ע�����Ļ��ң�</td><td  bgcolor=$forumcolortwo>$joinmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>�������������ӵĻ��ң�</td><td  bgcolor=$forumcolortwo>$addmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>�����»ظ����ӵĻ��ң�</td><td  bgcolor=$forumcolortwo>$replymoney</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ�ε�½ʱ���ӵĻ��ң�</td><td  bgcolor=$forumcolortwo>$loginmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>��ɾ�����Ӽ��ٵĻ��ң�</td><td  bgcolor=$forumcolortwo>$delmoney</td><tr>
        <tr><td bgcolor=$forumcolorone>���û�ע�����ľ��飺</td><td  bgcolor=$forumcolortwo>$joinjingyan</td><tr>
        <tr><td bgcolor=$forumcolorone>���û�ע������������</td><td  bgcolor=$forumcolortwo>$joinml</td><tr>
        <tr><td bgcolor=$forumcolorone>�������������ӵ�������</td><td  bgcolor=$forumcolortwo>$addml</td><tr>
        <tr><td bgcolor=$forumcolorone>�����»ظ����ӵ�������</td><td  bgcolor=$forumcolortwo>$replyml</td><tr>
        <tr><td bgcolor=$forumcolorone>ÿ�ε�½ʱ���ӵ�������</td><td  bgcolor=$forumcolortwo>$loginml</td><tr>
        <tr><td bgcolor=$forumcolorone>��ɾ�����Ӽ��ٵ�������</td><td  bgcolor=$forumcolortwo>$delml</td><tr>
</table>
~;
}



$output .= qq~</body></html>~;
&output(
     -Title   => "$boardname - �鿴��̳��Ϣ", 
     -ToPrint => $output, 
     -Version => $versionnumber 
    );
exit;
