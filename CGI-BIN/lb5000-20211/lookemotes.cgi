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
    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

    if ($inmembername eq "") { $inmembername = "����"; }
    else {
    &getmember("$inmembername");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
        }   

&mischeader("��̳EMOTE�б�");

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
        <img src=$imagesurl/images/closedfold.gif width=15 height=11>��<a href=$forumsummaryprog>$boardname</a><br>
        <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>���鿴��̳ EMOTE �б�
      </td></tr></table><table width=$tablewidth border=0 bordercolor=$tablebordercolor align=center cellpadding=0 cellspacing=0><tr><td>ע��:</td><td>�������е�"����"�����滻�ɷ����˵��û���.</td></tr></table>
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
     -Title   => "$boardname - �鿴��̳ EMOTE �б�", 
     -ToPrint => $output, 
     -Version => $versionnumber 
    );
exit;

