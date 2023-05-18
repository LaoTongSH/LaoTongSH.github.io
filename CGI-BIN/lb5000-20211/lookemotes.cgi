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
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "lookemotes.cgi";

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
    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

    if ($inmembername eq "") { $inmembername = "客人"; }
    else {
    &getmember("$inmembername");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
        }   

&mischeader("论坛EMOTE列表");

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
$filetoopen = "$lbdir" . "data/emote.cgi";
open (FILE, "$filetoopen");
flock (FILE, 1) if ($OS_USED eq "Unix");
$emote = <FILE>;
close (FILE);

$output .= qq~

         <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
             <tr>
               <td width=30% rowspan=2 valign=top>$forumgraphic
               </td>
               <td valign=top>
        <img src=$imagesurl/images/closedfold.gif width=15 height=11>　<a href=$forumsummaryprog>$boardname</a><br>
        <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>　查看论坛 EMOTE 列表
      </td></tr></table><table width=$tablewidth border=0 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0><tr><td>注意:</td><td>下列所有的"对象"将被替换成发贴人的用户名.</td></tr></table>
        <table width=$tablewidth border=1 bordercolor=$tablebordercolor align=center cellpadding=3 cellspacing=3><br>
       ~;  
       @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		($toemote, $beemote) = split(/=/,$_);
		chomp $beemote;
	$output .= qq~
	<tr><td bgcolor=$forumcolorone>$toemote</td><td  bgcolor=$forumcolortwo>$beemote</td>	           
~;
}
}




$output .= qq~</tr></table><br><br></body></html>~;
&output(
     -Title   => "$boardname - 查看论坛 EMOTE 列表", 
     -ToPrint => $output, 
     -Version => $versionnumber 
    );
exit;

