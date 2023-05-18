#!/usr/bin/perl
#############################################################
#  LeoBoard ver.5000 / LB5000 / À×°Á³¬¼¶ÂÛÌ³ ver.5000
#
#  °æÈ¨ËùÓĞ: À×°Á¹¤×÷ÊÒ(Ô­À¶±¦Ê¯Èí¼ş¹¤×÷ÊÒ)
#
#  ÖÆ×÷ÈË  : É½Ó¥ºı (Shining Hu)
#            »¨ÎŞÈ± (Ifairy Han)
#
#  Ö÷Ò³µØÖ·: http://www.CGIer.com/      CGI ±à³ÌÕßÖ®¼Ò
#	     http://www.LeoBoard.com/   À×°ÁÂÛÌ³Ö§³ÖÖ÷Ò³
#	     http://www.leoBBS.com/     ±¾ÂÛÌ³Ö±Í¨³µ
#            http://mail@17do.com/      ´ó¼ÒÒ»ÆğÓÊ
#
#############################################################
use Benchmark;
$TT0  = new Benchmark;
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
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "lbmail.lib.pl";
require "postjs.cgi";
require "rebuildlist.pl";

$|++;                        # Unbuffer the output
$thisprog = "post.cgi";
$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/\/$//;
$query = new LBCGI;
&ipbanned; #·âÉ±Ò»Ğ© ip

$addme=$query->param('addme');

$listmy=$query->param('listmy');
for ('forum','topic','membername','password','action','postno','inshowsignature',
     'notify','inshowemoticons','previewfirst','intopictitle','intopicdescription',
     'inpost','posticon') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
    }
$intopictitle  = "£ª£££¡£¦£ª$intopictitle";
$inforum       = $forum;
$intopic       = $topic;
&error("´ò¿ªÎÄ¼ş&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("´ò¿ªÎÄ¼ş&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") if (($inforum) && ($inforum !~ /^[0-9]+$/));
$inmembername  = $membername;
$inpassword    = $password;
$inpostno      = $postno;
$innotify      = $notify;
$currenttime   = time;
$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
$trueipaddress = $ipaddress if (($trueipaddress eq "")||($trueipaddress eq "unknown"));
$trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
$trueipaddress = $trueipaddress1 if (($trueipaddress1 ne "")&&($trueipaddress1 ne "unknown"));
$postipaddress = $ENV{'HTTP_X_FORWARDED_FOR'} || $ENV{'REMOTE_ADDR'}; 
$postipaddress = "$postipaddress=$trueipaddress";
$inposticon    = $posticon;

$inselectstyle   = $query->cookie("selectstyle");
&error("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

$maxupload = 300 if ($maxupload eq "");
$LBCGI::POST_MAX=1024 * $maxupload;
$LBCGI::DISABLE_UPLOADS = 0;

if ($inshowemoticons ne "yes") { $inshowemoticons eq "no"; }
if ($innotify ne "yes")        { $innotify eq "no"; }

    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
&error("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

	    $inmembername =~ s/\&nbsp\;//ig;
	    $inmembername =~ s/¡¡/ /g;
	    $inmembername =~ s/©¡/ /g;
	    $inmembername =~ s/[ ]+/ /g;
	    $inmembername =~ s/\s*$//g;
	    $inmembername =~ s/^\s*//g;
	    $inmembername =~ s/ *$//g;
	    $inmembername =~ s/^ *//g;
	    $inmembername =~ s/[ ]+/ /;
	    $inmembername =~ s/[ ]+/ /;
	    $inmembername =~ s/ÿ//isg;
	    $inmembername =~ s///isg;
	    $inmembername =~ s/()+//isg;
	    $inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\$\%\^\&\*\(\)\+\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

    if ($inmembername eq "") {
        $inmembername = "¿ÍÈË";
    }
&getmember("$inmembername");
$cpudisp = 1 if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"));

$advpost1=$query->param('advpost');
$advpost1  = $query->cookie("advpost") if ($advpost1 eq "");
$advpost = $advpost1 if ($advpost1 ne "");
$advpost=0 if ($advpost eq "");

$advcookie     = cookie(-name    =>   "advpost",
                         -value   =>   "$advpost",
                         -expires =>   "+30d",
                         -path    =>   "$cookiepath/"
                         );

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

    print header(-cookie  =>[$advcookie],-charset=>gb2312);

    if ($mainonoff == 1) { &InMaintenance; }

if ($useemote eq "yes") {
    $filetoopen = "$lbdir" . "data/emote.cgi";
    open (FILE, "$filetoopen");
    flock (FILE, 1) if ($OS_USED eq "Unix");
    $emote = <FILE>;
    close (FILE);
}
else { undef $emote; }

    if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("ÆÕÍ¨&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡"); }
    $helpurl = &helpfiles("ÔÄ¶Á±ê¼Ç");
    $helpurl = qq~$helpurl<img src=$imagesurl/images/help_b.gif border=0></a>~;
&badwordfile;


	$addtypedisp = $addtype;
	$addtypedisp =~ s/\, /\,/gi;
	$addtypedisp =~ s/ \,/\,/gi;
	$addtypedisp =~ tr/A-Z/a-z/;
	my @addtypedisp = split(/\,/, $addtypedisp);
	$addtypedisp = "<select><option value=#>Ö§³ÖÀàĞÍ£º</option><option value=#>----------</option>";
	foreach my $name (@addtypedisp) {
	  chomp $name;
    	  $addtypedisp .= qq~<option>$name</option>~;

	}
   	$addtypedisp .= qq~</select>~;

    my %Mode = (
    'new'          =>    \&newthread,
    'reply'        =>    \&reply,
    'replyquote'   =>    \&replyquote,
    'copy1'        =>    \&copy1
    );
    if ($arrawpostpic eq "on") { $postpicstates = "ÔÊĞí";} else {$postpicstates = "½ûÖ¹";}
    if ($arrawpostflash eq "on") { $postflashstates = "ÔÊĞí";} else {$postflashstates = "½ûÖ¹";}
    if ($arrawpostfontsize eq "on") { $postfontsizestates = "ÔÊĞí";} else {$postfontsizestates = "½ûÖ¹";}
    if ($arrawpostsound eq "on") { $postsoundstates = "ÔÊĞí";} else {$postsoundstates = "½ûÖ¹";}
    if($Mode{$action}) {
       	$Mode{$action}->();
    }
    elsif ($action eq "addnew"   && $previewfirst eq "no")  { &addnewthread; }
    elsif ($action eq "addnew"   && $previewfirst eq "yes") { &newthread; }
    elsif ($action eq "addreply" && $previewfirst eq "no")  { &addreply; }
    elsif ($action eq "addreply" && $previewfirst eq "yes") { &reply; }
    else { &error("ÆÕÍ¨&ÇëÒÔÕıÈ·µÄ·½Ê½·ÃÎÊ±¾³ÌĞò£¡"); }

    &output(
      -Title   => "$boardname - ÔÚ$forumnameÄÚ·¢Ìù",
      -ToPrint => $output,
      -Version => $versionnumber
    );

sub newthread {
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
#    &getmember("$inmembername");
     &moderator;
        if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne 'smo') && ($membercode ne "mo") && ($inmembmod ne "yes")) {
        $currenttime = time;
        ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
        $lastpost = ($lastpost + $floodcontrollimit);
            if ($lastpost > $currenttime)  {
                &error("·¢±íĞÂÖ÷Ìâ&¹àË®Ô¤·À»úÖÆÒÑ¾­Ê¹ÓÃ£¬Äú±ØĞëµÈ´ı $floodcontrollimit ÃëÖÓ²ÅÄÜÔÙ´Î·¢±í£¡");
	    }
	}
	&getforum("$inforum");

	$tempaccess = "forumsallowed". "$inforum";
        $testentry = $query->cookie("$tempaccess");

        if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }

    if ($postopen eq "no") {
	&error("·¢±í»ò»Ø¸´Ö÷Ìâ&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±í»ò»Ø¸´Ö÷Ìâ£¡");
    }

        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("·¢±í&¶Ô²»Æğ£¬ÄúÃ»ÓĞÔÚ´ËÂÛÌ³ÖĞ·¢±íµÄÈ¨Àû£¡");
        }

	if ($emoticons eq "on") {
            $emoticonslink = qq~<li><a href="javascript:openScript('$miscprog?action=showsmilies',300,350)">ÔÊĞí<B>Ê¹ÓÃ</B>±íÇé×Ö·û×ª»»</a>~;
            $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>ÄúÊÇ·ñÏ£Íû<b>Ê¹ÓÃ</b>±íÇé×Ö·û×ª»»ÔÚÄúµÄÎÄÕÂÖĞ£¿<br>~;
	}

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") {
    	&whosonline("$inmembername\t$forumname\tnone\t·¢±íĞÂÖ÷Ìâ\t");
    }
    else {
        &whosonline("$inmembername\t$forumname(ÃÜ)\tnone\t·¢±íĞÂµÄ±£ÃÜÖ÷Ìâ\t");
    }
}

    if ($previewfirst eq "yes") {
        &preview;
        $inpost =~ s/\<p\>/\n\n/ig;
        $inpost =~ s/\<br\>/\n/ig;
    }
    else {
       &mischeader("·¢±íĞÂÖ÷Ìâ");
    }

    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") {
	    $requestnotify = qq~<input type=checkbox name="notify" value="yes" checked>ÓĞ»Ø¸´Ê±Ê¹ÓÃÓÊ¼şÍ¨ÖªÄú£¿<br>~;
	}
	else {
	    $requestnotify = qq~<input type=checkbox name="notify" value="yes">ÓĞ»Ø¸´Ê±Ê¹ÓÃÓÊ¼şÍ¨ÖªÄú£¿<br>~;
	}
    }

    if ($startnewthreads eq "no") {
        $startthreads = "ÔÚ´ËÂÛÌ³ÖĞĞÂµÄÖ÷ÌâºÍÌù×Ó»Ø¸´Ö»ÄÜÓÉÌ³Ö÷¡¢°æÖ÷·¢±í£¡";
    }
    elsif ($startnewthreads eq "follow") {
	 $startthreads = "ÔÚ´ËÂÛÌ³ÖĞĞÂµÄÖ÷ÌâÖ»ÄÜÓÉÌ³Ö÷¡¢°æÖ÷·¢±í£¡ÆÕÍ¨»áÔ±Ö»¿ÉÒÔ¸úÌù£¡";
    }
    elsif ($startnewthreads eq "all") {
	 $startthreads = "ÈÎºÎÈË¾ù¿ÉÒÔ·¢±íºÍ»Ø¸´Ö÷Ìâ£¬Î´×¢²áÓÃ»§·¢ÌùÃÜÂëÇëÁô¿Õ£¡";
    }
    else {
	$startthreads = "ËùÓĞ×¢²á»áÔ±¾ù¿ÉÒÔ·¢±íºÍ»Ø¸´Ö÷Ìâ£¡";
    }
        if (($advpost == 1)&&($emoticons eq "on")){
	$emoticonsurl = qq~$imagesurl/emot~;
$output .= qq~ 
<script language="javascript"> 
function smilie(smilietext) { 
document.FORM.inpost.value=document.FORM.inpost.value+' :'+smilietext+': '; }
</script>
~;
	}
	if ($htmlstate eq "on") { $htmlstates = "¿ÉÓÃ"; } else { $htmlstates = "²»¿ÉÓÃ"; }
	if ($idmbcodestate eq "on") { $idmbcodestates = "¿ÉÓÃ"; } else { $idmbcodestates = "²»¿ÉÓÃ"; }
    	if ($useemote eq "no") { $emotestates = "²»¿ÉÓÃ"; } else { $emotestates = "¿ÉÓÃ"; }

	if ($advpost == 1){
	$advpostmt="[<a href=$thisprog?action=new&forum=$inforum&advpost=0>¼ò½àÄ£Ê½</a>]";
	   }else{
        $advpostmt="[<a href=$thisprog?action=new&forum=$inforum&advpost=1>¸ß¼¶Ä£Ê½</a>]";
         }
$intopictitle =~ s/^£ª£££¡£¦£ª//;
	$output .= qq~
<script>function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
function DoTitle(addTitle) {
var revisedTitle;
var currentTitle = document.FORM.intopictitle.value;
revisedTitle = currentTitle+addTitle;
document.FORM.intopictitle.value=revisedTitle;
document.FORM.intopictitle.focus();
return; }</script>
                <form action="$thisprog" method=post name="FORM" enctype="multipart/form-data">
                <input type=hidden name="action" value="addnew">
                <input type=hidden name="forum" value="$inforum">
		<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
		<tr><td>
                <table cellpadding=3 cellspacing=1 border=0 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2><font color=$titlefontcolor><b>Ë­¿ÉÒÔ·¢±í£¿</b> $startthreads $advpostmt</td>
                </tr>
                <tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>Ö÷Ìâ±êÌâ</b></font>¡¡
              <SELECT name=font onchange=DoTitle(this.options[this.selectedIndex].value)>
              <OPTION selected value="">Ñ¡Ôñ»°Ìâ</OPTION> <OPTION value=[Ô­´´]>[Ô­´´]</OPTION>
              <OPTION value=[×ªÌû]>[×ªÌû]</OPTION> <OPTION value=[¹àË®]>[¹àË®]</OPTION>
              <OPTION value=[ÌÖÂÛ]>[ÌÖÂÛ]</OPTION> <OPTION value=[ÇóÖú]>[ÇóÖú]</OPTION>
              <OPTION value=[ÍÆ¼ö]>[ÍÆ¼ö]</OPTION> <OPTION value=[¹«¸æ]>[¹«¸æ]</OPTION>
              <OPTION value=[×¢Òâ]>[×¢Òâ]</OPTION> <OPTION value=[ÌùÍ¼]>[ÌùÍ¼]</OPTION>
              <OPTION value=[½¨Òé]>[½¨Òé]</OPTION> <OPTION value=[ÏÂÔØ]>[ÏÂÔØ]</OPTION>
              <OPTION value=[·ÖÏí]>[·ÖÏí]</OPTION></SELECT></td>
                <td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="intopictitle" value="$intopictitle">¡¡²»µÃ³¬¹ı 40 ¸öºº×Ö</td>
                </tr><tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>ÓÃ»§Ãû</b></font></td>
                <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername">¡¡ <font color=$fontcolormisc><a href="$registerprog">ÄúÃ»ÓĞ×¢²á£¿</a></font></td>
                </tr><tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>ÃÜ¡¡Âë</b></font></td>
                <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword">¡¡ <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td>
                </tr>
                ~;

        $output .= qq~
	    <tr>
	<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>µ±Ç°ĞÄÇé</b><br><li>½«·ÅÔÚÌù×ÓµÄÇ°Ãæ<BR></font></td>
	<td bgcolor=$miscbackone valign=top>
	~;


     open (FILE, "${lbdir}data/lbpost.cgi");
     my @posticondata = <FILE>;
     close (FILE);
     chomp @posticondata;

    $tempiconnum=1;
    $tempselect = "";
#    $tempselect = "checked";
    foreach $picture (@posticondata) {
       if ($tempiconnum > 12) {
    	   $tempiconnum = 1;
    	   $output .= qq~<BR>~;
       }
       if ($picture eq $posticon) {$tempselect = "checked";} else {$tempselect = "";}
       $output .= qq~<input type=radio value="$picture" name="posticon" $tempselect><img src=$imagesurl/posticons/$picture $defaultsmilewidth $defaultsmileheight border=0>&nbsp;~;
       $tempiconnum ++;
       $tempselect = "";
    }

if (($arrowupload ne "off")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
    $output .= qq~
	</td>
	</tr>
	<tr><td bgcolor=$miscbackone>
	<b>ÉÏ´«¸½¼ş»òÍ¼Æ¬</b>(×î´ó $maxupload KB):
	</td>
	<td bgcolor=$miscbacktwo> <input type="file" size=40 name="addme">¡¡¡¡$addtypedisp
	~;
}
    $output .= qq~
	</td>
	</tr>
        <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>ÄÚÈİ</b><p>
        ÔÚ´ËÂÛÌ³ÖĞ£º<li>HTML ¡¡±êÇ©: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE¡¡±êÇ©</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LB5000 ±êÇ©</a>: <b>$idmbcodestates</b><li>ÌùÍ¼±êÇ© ¡¡: <b>$postpicstates</b><li>Flash ±êÇ© : <b>$postflashstates</b><li>ÒôÀÖ±êÇ© ¡¡: <b>$postsoundstates</b><li>ÎÄ×Ö´óĞ¡ ¡¡: <b>$postfontsizestates</b>$emoticonslink</font></td>
	<td bgcolor=$miscbackone>
	~;
	if ($advpost == 1){
	$output .= qq~
	$insidejs
	~;}
	$output .= qq~
        <TEXTAREA cols=80 name=inpost rows=12 wrap="soft" onkeydown=ctlent()>$inpost</TEXTAREA><br>
        ~;
        if ($advpost == 1){
        $output .= qq~
	&nbsp;¡¡Ä£Ê½:
	<input type="radio" name="mode" value="help" onClick="thelp(1)">¡¡°ïÖú¡¡
	<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">¡¡ÍêÈ«¡¡
	<input type="radio" name="mode" value="basic"  onClick="thelp(0)">¡¡»ù±¾¡¡¡¡¡¡¡¡ >> <a href=javascript:HighlightAll('FORM.inpost')>¸´ÖÆµ½¼ôÌù°å</a> | <a href=javascript:checklength(document.FORM);>²é¿´ÎÄÕÂ³¤¶È</a> <<
	~;}
	$output .= qq~
	</td></tr>
        </tr>
        ~;
        if (($advpost == 1)&&($emoticons eq "on")){
        $output .= qq~
        <tr>
	<td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>µã»÷±íÇéÍ¼¼´¿ÉÔÚÌù×ÓÖĞ¼ÓÈëÏàÓ¦µÄ±íÇé(Ã¿¸ö±íÇé×î¶àÍ¬Ê±ÏÔÊ¾ $maxsmail ´Î)</B></font><br>&nbsp;
    ~;

    		open (FILE, "${lbdir}data/lbemot.cgi");
		my @emoticondata = <FILE>;
		close (FILE);
		chomp @emoticondata;
        	foreach $picture (@emoticondata) {
    			$smileyname = $picture;
    			$smileyname =~ s/\.gif$//g;
       			$output .= qq~
                	<a href="javascript:smilie('$smileyname');"><img src=$emoticonsurl/$picture border=0></a>
                	~;
                }
    		$output .= qq~
    		</td>
                </tr>
      ~;
      }
      $output .= qq~
                <tr>
                <td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>Ñ¡Ïî</b><p>$helpurl</font></td>
                <td bgcolor=$miscbacktwo><font color=$fontcolormisc><input type=checkbox name="inshowsignature" value="yes" checked>ÊÇ·ñÏÔÊ¾ÄúµÄÇ©Ãû£¿<br>
                $requestnotify
                $emoticonsbutton
                &nbsp;<b>·¢±íÖ®Ç°ÊÇ·ñÔ¤ÀÀ£¿ </b><input name="previewfirst" type="radio" value="yes"> ÊÇ¡¡ <input name="previewfirst" type="radio" value="no" checked> ·ñ</font>
                </font><BR><BR></td>
                </tr><tr>
                <td bgcolor=$miscbacktwo colspan=2 align=center>
                <input type=Submit value="·¢ ±í" name=Submit onClick="return clckcntr();">¡¡¡¡<input type="reset" name="Clear" value="Çå ³ı">
                </td></form></tr>
            </table>
        </tr></td></table>
        ~;
}

sub addnewthread {
#    &getmember("$inmembername");
    &moderator;
    if (($floodcontrol eq "on") && ($membercode ne "ad")&&($membercode ne 'smo') && ($membercode ne "mo") && ($inmembmod ne "yes")) {
	$currenttime = time;
	($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	$lastpost = ($lastpost + $floodcontrollimit);
	if ($lastpost > $currenttime)  {
	    &error("·¢±íĞÂÖ÷Ìâ&¹àË®Ô¤·À»úÖÆÒÑ¾­Ê¹ÓÃ£¬Äú±ØĞëµÈ´ı $floodcontrollimit ÃëÖÓ²ÅÄÜÔÙ´Î·¢±í£¡");
	}
    }

    if ($postopen eq "no") {
	&error("·¢±í»ò»Ø¸´Ö÷Ìâ&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±í»ò»Ø¸´Ö÷Ìâ£¡");
    }
    &getforum("$inforum");

    if (($userregistered eq "no")&&(length($inmembername) > 12)) { &error("·¢±íĞÂÖ÷Ìâ&ÄúÊäÈëµÄÓÃ»§ÃûÌ«³¤£¬Çë¿ØÖÆÔÚ6¸öºº×ÖÄÚ£¡");   }
    if (($userregistered eq "no")&&($inmembername =~ /^¿ÍÈË/)) { &error("·¢±íĞÂÖ÷Ìâ&Çë²»ÒªÔÚÓÃ»§ÃûµÄ¿ªÍ·ÖĞÊ¹ÓÃ¿ÍÈË×ÖÑù£¡");   }

    my $intopictitletemp = $intopictitle;
    $intopictitletemp =~ s/^£ª£££¡£¦£ª//;

    if (($userregistered eq "no")&&($startnewthreads ne "all")) { &error("·¢±íĞÂÖ÷Ìâ&ÄúÃ»ÓĞ×¢²á£¡");   }
    elsif ((($inpassword ne $password)&&($userregistered ne "no"))||(($inpassword ne "")&&($userregistered eq "no"))) { &error("·¢±íĞÂÖ÷Ìâ&ÄúµÄÃÜÂë´íÎó£¡"); }
    elsif ($membercode eq "banned")     { &error("Ìí¼Ó»Ø¸´&Äú±»½ûÖ¹·¢ÑÔ£¡"); }
    elsif ($intopictitletemp eq "")         { &error("·¢±íĞÂÖ÷Ìâ&±ØĞëÊäÈëÖ÷Ìâ±êÌâ£¡"); }
    elsif (length($intopictitle) > 92)  { &error("·¢±íĞÂÖ÷Ìâ&Ö÷Ìâ±êÌâ¹ı³¤£¡"); }
    else  {
    @allforums = @forums;

        $intopictitle =~ s/()+//isg;
	if (($inpost eq "")&&($addme eq "")) { $intopictitle.=" (ÎŞÄÚÈİ)"; }

	$tempintopictitle = $intopictitle;
	$tempintopictitle =~ s/ //g;
	$tempintopictitle =~ s/\&nbsp\;//g;
	$tempintopictitle =~ s/¡¡//g;
        $tempintopictitle =~ s/^£ª£££¡£¦£ª//;
	if ($tempintopictitle eq "") { &error("·¢±íĞÂÖ÷Ìâ&Ö÷Ìâ±êÌâÓĞÎÊÌâ£¡"); }
        undef $tempintopictitle;

        $tempaccess = "forumsallowed". "$inforum";
        $testentry = $query->cookie("$tempaccess");

        if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("·¢±í&¶Ô²»Æğ£¬Äú²»ÔÊĞíÔÚ´ËÂÛÌ³·¢±í£¡");
        }

	if ($startnewthreads eq "no") {
            unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes") {
                &error("·¢±íĞÂÖ÷Ìâ&ÔÚ´ËÂÛÌ³ÖĞÖ»ÄÜÓÉÌ³Ö÷»òÕß°æÖ÷·¢±íĞÂÖ÷Ìâ£¡");
            }
	}
	elsif (($startnewthreads eq "follow") &&($action eq "addnew")) {
            unless ($membercode eq "ad" ||$membercode eq 'smo' ||$membercode eq 'mo'|| $inmembmod eq "yes") {
                &error("·¢±íĞÂÖ÷Ìâ&ÔÚ´ËÂÛÌ³ÖĞÖ»ÄÜÓÉÌ³Ö÷»òÕß°æÖ÷·¢±íĞÂÖ÷Ìâ£¡");
            }
	}
	elsif (($startnewthreads eq "all")&&($userregistered eq "no")) {
	    $inmembername = "$inmembername(¿Í)";
	}

	$end_q_tag = 0;
	$srt_q_tag = 0;
	$end_q_tag++ while $inpost =~ m#\[/QUOTE\]#ig;
	$srt_q_tag++ while $inpost =~ m#\[QUOTE\]#ig;
	if ($end_q_tag ne $srt_q_tag) { &error("ÄÚÈİĞ£Ñé³ö´í&ÄãÊäÈëÁË $srt_q_tag ¸ö [QUOTE] ±êÇ©ºÍ $end_q_tag ¸ö [/QUOTE] ±êÇ©£¬ÊıÄ¿²»Æ¥Åä£¡"); }

        if ($emote) {
 	    @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		($toemote, $beemote) = split(/=/,$_);
		chop $beemote;
		$beemote =~ s/¶ÔÏó/¡¼$inmembername¡½/isg;
		$inpost =~ s/$toemote/$beemote/isg;
	    }
	}

     undef $newthreadnumber;
     $filetoopen = "$lbdir" . "boarddata/lastnum$inforum.cgi";
     if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $newthreadnumber = <FILE>;
        close(FILE);
        chomp $newthreadnumber;
	$newthreadnumber ++;
     }
      $filetoopen1 = "$lbdir" . "forum$inforum/$newthreadnumber.pl";
      if ((!(-e $filetoopen1))&&($newthreadnumber =~ /^[0-9]+$/)) {
        if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE $newthreadnumber;
        close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
       }
       else {
        $dirtoopen = "$lbdir" . "forum$inforum";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);
        @sorteddirdata = grep(/.thd.cgi$/,@dirdata);
        @newdirdata = sort numerically(@sorteddirdata);
        @neworderdirdata = reverse(@newdirdata);
        $highest = $neworderdirdata[0];
        $highest =~ s/.thd.cgi$//;
        $newthreadnumber = $highest + 1;

        if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE $newthreadnumber;
        close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
       }
	$oldthreadnumber = $newthreadnumber - 1;
        $filetoopen1 = "$lbdir" . "forum$inforum/$oldthreadnumber.thd.cgi";
        if (-e $filetoopen1) {
	    open(FILE, "$filetoopen1");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            my $threaddata =<FILE>;
            close(FILE);
            (my $amembername,my $atopictitle,my $no,my $no,my $no,my $no,my $apost,my $no) = split(/\t/, $threaddata);
	    if (($amembername eq $inmembername)&&(($apost eq $inpost)||($atopictitle eq $intopictitle))) {
		$filetoopen = "$lbdir" . "boarddata/lastnum$inforum.cgi";
	        if (open(FILE, ">$filetoopen")) {
        	flock(FILE, 2) if ($OS_USED eq "Unix");
        	print FILE $oldthreadnumber;
        	close(FILE);
        	}
	    	&error("·¢±íĞÂÖ÷Ìâ&Çë²»ÒªÖØ¸´·¢Ìù×Ó£¬ÒÑ¾­´æÔÚÓë´ËÌù×ÓÖ÷ÌâÏàÍ¬»òÕßÄÚÈİÏàÍ¬µÄ¶øÇÒÊÇÄã·¢µÄÌù×ÓÁË£¡");
	    }
	}

	if (($addme)&&(($arrowupload ne "off")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"))) {
	    my $up_filename =$query->uploadInfo($addme);
	    my ($up_name,$up_ext) = split(/.*\./,$up_filename);
	    $up_ext = lc($up_ext);

	    my $checkadd=0;
            for (split(/\,\s*/,$addtype)){
                $checkadd=1,last if ($up_ext eq lc($_));
            }
           &error("ÉÏ´«³ö´í&ÎªÁË°²È«£¬²»Ö§³ÖÄãËùÉÏ´«µÄ¸½¼ş£¬ÇëÖØĞÂÑ¡Ôñ£¡") if ($up_ext eq "exe"||$up_ext eq "com"||$up_ext eq "pl"||$up_ext eq "cgi"||$up_ext eq "asp"||$up_ext eq "php"||$up_ext eq "php3"||$up_ext eq "phtml"||$up_ext eq "jsp"||$up_ext eq "cfml"||$up_ext eq "dll");
	   &error("ÉÏ´«³ö´í&²»Ö§³ÖÄãËùÉÏ´«µÄ¸½¼ş»òÕßÍ¼Æ¬£¬ÇëÖØĞÂÑ¡Ôñ£¡") if ($checkadd==0);
	   my $filesize=0;
	   my $buffer;
 	    open (FILE,">$imagesdir/usr/$inforum/$inforum\_${newthreadnumber}.$up_ext");
		binmode (FILE);
		while ((($buffer=$query->readUploadFile($addme,4096)))&&!(($filesize>$maxupload)&&($membercode ne "ad"))) {
		print FILE $buffer;
		$filesize=$filesize+4;
	    }
	    close (FILE);
	    if (($filesize>$maxupload)&&($membercode ne "ad")) {
                unlink ("$imagesdir/usr/$inforum/$inforum\_${newthreadnumber}.$up_ext");
		&error("ÉÏ´«³ö´í&ÉÏ´«ÎÄ¼ş´óĞ¡³¬¹ı$maxupload£¬ÇëÖØĞÂÑ¡Ôñ£¡");
	    }
	}
	$intopictitletemp = $intopictitle ;

	$intopictitletemp =~ s/^£ª£££¡£¦£ª//;

        $inposttemp = $inpost;
	$inposttemp =~ s/\[Õâ¸öÌù×Ó×îºóÓÉ(.+?)±à¼­\]\n//isg;
	$inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	$inposttemp =~ s/\[quote\](.*)\[\/quote\]//isg;
	$inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/isg;
	$maxsmailtemp = $maxsmail;
	$maxsmail     = 0;
	$inposttemp   = &doemoticons("$inposttemp");
	$maxsmail     = $maxsmailtemp;
	$inposttemp =~ s/\<img\s*(.*?)\s*\>//isg;
        $inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)//isg;
	$inposttemp =~ s/( )+$//isg;
	$inposttemp =~ s/^( )+//isg;
	$inposttemp =~ s/<(.|\n)+?>//g;
	$inposttemp =~ s/\[.+?\]//g;
        $inposttemp =~ s/[\a\f\n\e\0\r\t]//g;
        chomp $inposttemp;

        $inposttemp = &lbhz($inposttemp,$maxsavepost);
        $filetoopen = "$lbdir" . "forum$inforum/$newthreadnumber.pl";
        if (open(FILE, ">$filetoopen")) {
        print FILE "$newthreadnumber\t$intopictitletemp\t$intopicdescription\topen\t0\t0\t$inmembername\t$currenttime\t\t$currenttime\t$inposticon\t$inposttemp\t";
        close(FILE);
        }

        $filetomake = "$lbdir" . "forum$inforum/$newthreadnumber.thd.cgi";
        if (open(FILE, ">$filetomake")) {
        print FILE "$inmembername\t$intopictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t";
        close(FILE);
        }

if ($privateforum ne "yes") {
 $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
 my $filetoopens = &lockfilename($filetomakeopen);
 if (!(-e "$filetoopens.lck")) {
   if (-e $filetomakeopen) {
      &winlock($filetomakeopen) if ($OS_USED eq "Nt");
      open(FILE, "$filetomakeopen");
      flock (FILE, 1) if ($OS_USED eq "Unix");
      @recentposts=<FILE>;
      close(FILE);
      my $checknumber = 0;
      $maxadpost = 3 if ($maxadpost < 3);
      $maxadpost = 999 if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"));
      foreach (@recentposts) {
	  (my $no,$no,my $temptopic,$no,$no,my $tempmembername) = split(/\t/,$_);
	  $temptopic =~ s/^£ª£££¡£¦£ª//;
	  $checknumber ++ if (($intopictitletemp eq $temptopic)&&($tempmembername eq $inmembername));
      }
      
      if ($checknumber >= $maxadpost) {
        &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
        $filetoopen = "$lbdir" . "forum$inforum/$newthreadnumber.pl";
        unlink ($filetoopen);
        $filetomake = "$lbdir" . "forum$inforum/$newthreadnumber.thd.cgi";
        unlink ($filetomake);

#	&getmember("$inmembername");
	$memberfiletitle = $inmembername;
	$memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;
	if (($inmembername ne "")&&($password ne "")) {
	   $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
	   &winlock($filetomake) if ($OS_USED eq "Nt");
	   if (open(FILE0, ">$filetomake")) {
	   flock(FILE0, 2) if ($OS_USED eq "Unix");
	   print FILE0 "$inmembername\t$password\t$membertitle\tbanned\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t";
	   close(FILE0);
	   }
	   &winunlock($filetomake) if ($OS_USED eq "Nt");
	}
        $filetomake = "$lbdir" . "data/idbans.cgi";
        open (FILE, ">>$filetomake");
        print FILE "$inmembername\n";
        close (FILE);

	&error("³ö´í&ÓÉÓÚÄãÔÚ¶àÇø·¢ËÍ¹ã¸æ£¬ËùÒÔÄãÒÑ¾­±»½ûÖ¹·¢ÑÔ£¡");
      }

      $recentposts=@recentposts;
      if ($recentposts<$maxpostreport) {
          $maxpostreport=$recentposts;
      }
      else {
          $maxpostreport--;
      }
      if (open (FILE, ">$filetomakeopen")) {
          flock (FILE, 2) if ($OS_USED eq "Unix");
          print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inposticon\t$inmembername\t\n";

          for ($i=0;$i<$maxpostreport;$i++) {
              print FILE $recentposts[$i];
          }
          close(FILE);
      }
      &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
   }
   else {
      if (open (FILE, ">$filetomakeopen")) {
      print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inposticon\t$inmembername\t\n";
      close(FILE);
      }
   }
 }
}
        $file = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
	$listall = @listall;

    if ($listall >= 300) {
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        print LIST "$newthreadnumber\t$intopictitletemp\t$intopicdescription\tOpen\t0\t0\t$inmembername\t$currenttime\t\t$currenttime\t$inposticon\t$inposttemp\t\n";
        foreach (@listall) {
          (my $useid,my $no)=split(/\t/,$_);
	  $_ =~ s/[\n\r]//isg;
	  print LIST "$_\n" if (($useid ne "")&&($useid =~ /^[0-9]+$/));
        }
        close (LIST);
        }
        &winunlock($file);
    }
    else {
        &winunlock($file);
        rebuildLIST(-Forum=>"$inforum");
    }

        $cleanmembername = $inmembername;
        $cleanmembername =~ s/ /\_/isg;
	$cleanmembername =~ tr/A-Z/a-z/;
        $numberofposts++;
        $lastpostdate = "$currenttime\%\%\%$threadprog?forum=$inforum&topic=$newthreadnumber\%\%\%$intopictitletemp" if ($privateforum ne "yes");
        chomp $lastpostdate;

    if (($userregistered ne "no")&&($password ne "")) {
        $filetomake = "$lbdir" . "$memdir/$cleanmembername.cgi";
        $filetomake = &stripMETA($filetomake);
        &winlock($filetomake);
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$inmembername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t";
        close(FILE);
        }
        &winunlock($filetomake);
    }

      $filetoopen = "$lbdir" . "data/allforums.cgi";
      my $filetoopens = &lockfilename($filetoopen);
      if (!(-e "$filetoopens.lck")) {
        &winlock($filetoopen);
        if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) {
        chomp($forum);
        next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    $lastposter = $inmembername;
                    $lastposttime = $currenttime;
                    $threads++;
                    $lastposttime = "$lastposttime\%\%\%$newthreadnumber\%\%\%$intopictitletemp";
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetoopen);
      }
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        my $filetoopens = &lockfilename($filetomake);
  if (!(-e "$filetoopens.lck")) {
        $totalthreads++;
        &winlock($filetomake) if ($OS_USED eq "Nt");
      if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
      }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
  }

        if (($emailfunctions eq "on") && ($innotify eq "yes")) {
            $filetomake = "$lbdir" . "forum$inforum/$newthreadnumber.mal.pl";
            if (open (FILE, ">$filetomake")) {
            print FILE "$inmembername\t$emailaddress\t\n";
            close (FILE);
            }
        }

        &mischeader("ĞÂÖ÷Ìâ·¢±í³É¹¦");

        if ($refreshurl == 1) {
	        $relocurl = "$threadprog?forum=$inforum&topic=$newthreadnumber";
	}
	else {
               	$relocurl = "$forumsprog?forum=$inforum";
        }
        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>Ğ»Ğ»£¬$inmembername£¡ÄúµÄĞÂÖ÷ÌâÒÑ¾­·¢±í³É¹¦£¡</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$newthreadnumber">·µ»ØĞÂÖ÷Ìâ</a>
            <li><a href="$forumsprog?forum=$inforum">·µ»ØÂÛÌ³</a>
            <li><a href="$forumsummaryprog">·µ»ØÂÛÌ³Ê×Ò³</a>
            <li><a href="$postingsprog?action=locktop&forum=$inforum&topic=$newthreadnumber">ĞÂÖ÷Ìâ¹Ì¶¥</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
    }
}

sub reply {
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }

    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    open(FILE, "$filetoopen");
    flock (LIST, 1) if ($OS_USED eq "Unix");
    @threads = <FILE>;
    close(FILE);
    $posttoget = $inpostno;
    $posttoget--;
    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post) = split(/\t/, $threads[$posttoget]);
    $topictitle =~ s/^£ª£££¡£¦£ª//;

#    &getmember("$inmembername");
    if (($floodcontrol eq "on") && ($membercode ne "ad")&&($membercode ne 'smo') && ($membercode ne "mo") && ($inmembmod ne "yes")) {
	$currenttime = time;
	($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	$lastpost = ($lastpost + $floodcontrollimit);
	if ($lastpost > $currenttime)  {
	    &error("·¢±í»Ø¸´&¹àË®Ô¤·À»úÖÆÒÑ¾­Ê¹ÓÃ£¬Äú±ØĞëµÈ´ı $floodcontrollimit ÃëÖÓ²ÅÄÜÔÙ´Î·¢±í£¡");
	}
    }
    &getforum("$inforum");
    $tempaccess = "forumsallowed". "$inforum";
    $testentry = $query->cookie("$tempaccess");

    if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }

    if ($postopen eq "no") {
	&error("·¢±í»ò»Ø¸´Ö÷Ìâ&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±í»ò»Ø¸´Ö÷Ìâ£¡");
    }

    if (($privateforum eq "yes") && ($allowed ne "yes")) {
	&error("·¢±í&¶Ô²»Æğ£¬Äú²»ÔÊĞíÔÚ´ËÂÛÌ³·¢±í£¡");
    }

    if (($threadstate eq "closed")||($threadstate eq "pollclosed")) { &error("·¢±í»Ø¸´&¶Ô²»Æğ£¬Õâ¸öÖ÷ÌâÒÑ¾­±»Ëø¶¨£¡"); }
    if ($emoticons eq "on") {
        $emoticonslink = qq~<li><a href="javascript:openScript('$miscprog?action=showsmilies',300,350)">ÔÊĞí<B>Ê¹ÓÃ</B>±íÇé×Ö·û×ª»»</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>ÄúÊÇ·ñÏ£Íû<b>Ê¹ÓÃ</b>±íÇé×Ö·û×ª»»ÔÚÄúµÄÎÄÕÂÖĞ£¿<br>~;
    }
    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") {
	    $requestnotify = qq~<input type=checkbox name="notify" value="yes" checked>ÓĞ»Ø¸´Ê±Ê¹ÓÃÓÊ¼şÍ¨ÖªÄú£¿<br>~;
	}
	else {
	    $requestnotify = qq~<input type=checkbox name="notify" value="yes">ÓĞ»Ø¸´Ê±Ê¹ÓÃÓÊ¼şÍ¨ÖªÄú£¿<br>~;
	}
    }
    if ($previewfirst eq "yes") {
        &preview;
        $inpost =~ s/\<p\>/\n\n/ig;
        $inpost =~ s/\<br\>/\n/ig;
    }
    else {
        &mischeader("·¢±í»Ø¸´")
    }

	$emoticonsurl = qq~$imagesurl/emot~;
$output .= qq~ 
<script language="javascript"> 
function smilie(smilietext) { 
document.FORM.inpost.value=document.FORM.inpost.value+' :'+smilietext+': '; }
</script>
~;

    if ($htmlstate eq "on")     { $htmlstates = "¿ÉÓÃ";     } else { $htmlstates = "²»¿ÉÓÃ";     }
    if ($idmbcodestate eq "on") { $idmbcodestates = "¿ÉÓÃ"; } else { $idmbcodestates = "²»¿ÉÓÃ"; }
    if ($useemote eq "no") { $emotestates = "²»¿ÉÓÃ"; } else { $emotestates = "¿ÉÓÃ"; }

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") {
     	&whosonline("$inmembername\t$forumname\tnone\t»Ø¸´<a href=\"$threadprog?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
    }
    else {
        &whosonline("$inmembername\t$forumname(ÃÜ)\tnone\t»Ø¸´±£ÃÜÌù×Ó\t");
    }
}

    if ($badwords) {
	@pairs = split(/\&/,$badwords);
	foreach (@pairs) {
	    ($bad, $good) = split(/=/,$_);
	    chomp $good;
	    $topictitle =~ s/$bad/$good/isg;
	    $inpost =~ s/$bad/$good/isg;
	}
    }
    if ($advpost == 1){
	$advpostmt="[<a href=$thisprog?action=reply&forum=$inforum&topic=$intopic&advpost=0>¼ò½àÄ£Ê½</a>]";
	   }else{
        $advpostmt="[<a href=$thisprog?action=reply&forum=$inforum&topic=$intopic&advpost=1>¸ß¼¶Ä£Ê½</a>]";
         }
    $output .= qq~
<script>function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
function DoTitle(addTitle) {
var revisedTitle;
var currentTitle = document.FORM.intopictitle.value;
revisedTitle = currentTitle+addTitle;
document.FORM.intopictitle.value=revisedTitle;
document.FORM.intopictitle.focus();
return; }</script>
	<form action="$thisprog" method=post name="FORM" enctype="multipart/form-data">
        <input type=hidden name="action" value="addreply">
        <input type=hidden name="forum" value="$inforum">
        <input type=hidden name="topic" value="$intopic">
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
        <tr><td>
	<table cellpadding=4 cellspacing=1 border=0 width=100%>
	    <tr>
             <td bgcolor=$titlecolor colspan=2><font color=$titlefontcolor><b>Ö÷Ìâ±êÌâ</b>£º $topictitle $advpostmt</td>
            </tr>
	    <tr>
              <td bgcolor=$miscbackone><font color=$fontcolormisc><b>ÓÃ»§Ãû</b></font></td>
              <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"><font color=$fontcolormisc>¡¡ <a href="$registerprog">ÄúÃ»ÓĞ×¢²á£¿</a></font></td>
            </tr><tr>
              <td bgcolor=$miscbackone><font color=$fontcolormisc><b>ÃÜ¡¡Âë</b></font></td>
              <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"><font color=$fontcolormisc>¡¡ <a href="$profileprog?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td>
            </tr>
            ~;

    $output .= qq~
	    <tr>
	      <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>µ±Ç°ĞÄÇé</b><br><li>½«·ÅÔÚÌù×ÓµÄÇ°Ãæ<BR></font></td>
	      <td bgcolor=$miscbackone valign=top>
    ~;

    open (FILE, "${lbdir}data/lbpost.cgi");
     my @posticondata = <FILE>;
     close (FILE);
     chomp @posticondata;

    $tempiconnum=1;
    $tempselect = "";
#    $tempselect = "checked";
    foreach $picture (@posticondata) {
       $posticonname = $picture;
       $posticonname =~ s/\.gif$//g;
       if ($tempiconnum > 12) {
    	   $tempiconnum = 1;
    	   $output .= qq~<BR>~;
       }
       if ($picture eq $posticon) {$tempselect = "checked";} else {$tempselect = "";}
       $output .= qq~<input type=radio value="$picture" name="posticon" $tempselect><img src=$imagesurl/posticons/$picture $defaultsmilewidth $defaultsmileheight border=0>&nbsp;~;
       $tempiconnum ++;
       $tempselect = "";
    }

      if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||($allowattachment eq "yes")) {
        $output .= qq~
	</td>
	</tr>
	<tr><td bgcolor=$miscbackone>
	<b>ÉÏ´«¸½¼ş»òÍ¼Æ¬</b>(×î´ó $maxupload KB):
	</td>
	<td bgcolor=$miscbacktwo> <input type="file" size=40 name="addme">¡¡¡¡$addtypedisp
	~;
      }

    $output .= qq~
	</td></tr>
	  <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>ÄÚÈİ</b><p>
	  ÔÚ´ËÂÛÌ³ÖĞ£º<li>HTML ¡¡±êÇ©: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE¡¡±êÇ©</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LB5000 ±êÇ©</a>: <b>$idmbcodestates</b><li>ÌùÍ¼±êÇ© ¡¡: <b>$postpicstates</b><li>Flash ±êÇ© : <b>$postflashstates</b><li>ÒôÀÖ±êÇ© ¡¡: <b>$postsoundstates</b><li>ÎÄ×Ö´óĞ¡ ¡¡: <b>$postfontsizestates</b>$emoticonslink</font></td>
	<td bgcolor=$miscbackone>
	~;
	if ($advpost == 1){
	$output .= qq~
	$insidejs
	~;}
	$output .= qq~
	<TEXTAREA cols=80 name=inpost rows=12 wrap="soft" onkeydown=ctlent()>$inpost</TEXTAREA><br>
	~;
	if ($advpost == 1){
	$output .= qq~
	&nbsp;¡¡Ä£Ê½:
	<input type="radio" name="mode" value="help" onClick="thelp(1)">¡¡°ïÖú¡¡
	<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">¡¡ÍêÈ«¡¡
	<input type="radio" name="mode" value="basic"  onClick="thelp(0)">¡¡»ù±¾¡¡¡¡¡¡¡¡ >> <a href=javascript:HighlightAll('FORM.inpost')>¸´ÖÆµ½¼ôÌù°å</a> | <a href=javascript:checklength(document.FORM);>²é¿´ÎÄÕÂ³¤¶È</a> <<
	~;}
	$output .= qq~
	</td></tr>
         </tr>
         ~;
        if (($advpost == 1)&&($emoticons eq "on")){
        $output .= qq~
         <tr>
	<td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>µã»÷±íÇéÍ¼¼´¿ÉÔÚÌù×ÓÖĞ¼ÓÈëÏàÓ¦µÄ±íÇé(Ã¿¸ö±íÇé×î¶àÍ¬Ê±ÏÔÊ¾ $maxsmail ´Î)</B></font><br>&nbsp;
   ~;

	 open (FILE, "${lbdir}data/lbemot.cgi");
	my @emoticondata = <FILE>;
	close (FILE);
	chomp @emoticondata;
	foreach $picture (@emoticondata) {
	    $smileyname = $picture;
	    $smileyname =~ s/\.gif$//g;
	    $output .= qq~
		<a href="javascript:smilie('$smileyname');"><img src=$emoticonsurl/$picture border=0></a>
	    ~;
	}
	$output .= qq~
	    </td>
            </tr>
            ~;}
            $output .= qq~
            <tr>
            <td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>Ñ¡Ïî</b><p>$helpurl</font></td>
            <td bgcolor=$miscbacktwo><font color=$fontcolormisc><input type=checkbox name="inshowsignature" value="yes" checked>ÊÇ·ñÏÔÊ¾ÄúµÄÇ©Ãû£¿<br>
            $requestnotify
            $emoticonsbutton
            &nbsp;<b>·¢±íÖ®Ç°ÊÇ·ñÔ¤ÀÀ£¿ </b><input name="previewfirst" type="radio" value="yes"> ÊÇ¡¡ <input name="previewfirst" type="radio" value="no" checked> ·ñ</font>
            </font><BR><BR></td>
            </tr><tr>
            <td bgcolor=$miscbacktwo colspan=2 align=center>
            <input type=Submit value="·¢ ±í" name=Submit onClick="return clckcntr();">¡¡¡¡<input type="reset" name="Clear" value="Çå ³ı">
            </td></form></tr>
            </table></tr></td>
	    </table>
        ~;

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @threads = <FILE>;
        close(FILE);
        @sortedthreads = reverse(@threads);
        &threadreview;
}

sub replyquote {
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
#    &getmember("$inmembername");
    &moderator;
    if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne 'smo') && ($membercode ne "mo") && ($inmembmod ne "yes")) {
        $currenttime = time;
        ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
        $lastpost = ($lastpost + $floodcontrollimit);
        if ($lastpost > $currenttime)  {
            &error("·¢±í»Ø¸´&¹àË®Ô¤·À»úÖÆÒÑ¾­Ê¹ÓÃ£¬Äú±ØĞëµÈ´ı $floodcontrollimit ÃëÖÓ²ÅÄÜÔÙ´Î·¢±í£¡");
        }
    }
    &getforum("$inforum");

    $tempaccess = "forumsallowed". "$inforum";
    $testentry = $query->cookie("$tempaccess");

    if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }

    if ($postopen eq "no") {
	&error("·¢±í»ò»Ø¸´Ö÷Ìâ&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±í»ò»Ø¸´Ö÷Ìâ£¡");
    }

    if (($privateforum eq "yes") && ($allowed ne "yes")) {
        &error("·¢±í&¶Ô²»Æğ£¬Äú²»ÔÊĞíÔÚ´ËÂÛÌ³·¢±í£¡");
    }

    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @threads = <FILE>;
    close(FILE);
    if (($threadstate eq "closed")||($threadstate eq "pollclosed")) { &error("·¢±í»Ø¸´&¶Ô²»Æğ£¬Õâ¸öÖ÷ÌâÒÑ¾­±»Ëø¶¨£¡"); }
    $posttoget = $inpostno;
    $posttoget--;

    if ($sticky eq "on") {
	$threadscount=@threads;
	$posttoget =$threadscount - $posttoget if ($posttoget ne 0);
    }
    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, $threads[$posttoget]);
	$topictitle =~ s/^£ª£££¡£¦£ª//;

    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;
    $post =~ s/ \&nbsp;/  /ig;

    $membernametemp=$membername;

    $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
    $postdate = &dateformat("$postdate");
    $rawpost = $post;
    if ($previewfirst eq "yes") {
        $rawpost = $inpost;
        $rawpost =~ s/\<p\>/\n\n/ig;
        $rawpost =~ s/\<br\>/\n/ig;
        &preview;
    }
    else {
        &mischeader("ÒıÓÃ»Ø¸´Ìù×Ó");
    }
    if ($emoticons eq "on") {
        $emoticonslink = qq~<li><a href="javascript:openScript('$miscprog?action=showsmilies',300,350)">ÔÊĞí<B>Ê¹ÓÃ</B>±íÇé×Ö·û×ª»»</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>ÄúÊÇ·ñÏ£Íû<b>Ê¹ÓÃ</b>±íÇé×Ö·û×ª»»ÔÚÄúµÄÎÄÕÂÖĞ£¿<br>~;
    }

    if ($emailfunctions eq "on") { $requestnotify = qq~<input type=checkbox name="notify" value="yes">ÓĞ»Ø¸´Ê±Ê¹ÓÃÓÊ¼şÍ¨ÖªÄú£¿<br>~; }

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") {
    	&whosonline("$inmembername\t$forumname\tnone\tÒıÓÃ»Ø¸´<a href=\"$threadprog?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
    }
    else {
    	&whosonline("$inmembername\t$forumname(ÃÜ)\tnone\tÒıÓÃ»Ø¸´±£ÃÜÌù×Ó\t");
    }
}

    $emoticonsurl = qq~$imagesurl/emot~;
$output .= qq~ 
<script language="javascript"> 
function smilie(smilietext) { 
document.FORM.inpost.value=document.FORM.inpost.value+' :'+smilietext+': '; }
</script>
~;
    $rawpost =~ s/\[Õâ¸öÌù×Ó×îºóÓÉ(.+?)±à¼­\]\n//isg;
    $rawpost =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[quote\](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/isg;
    $maxsmailtemp = $maxsmail;
    $maxsmail     = 0;
    $rawpost   = &doemoticons("$rawpost");
    $maxsmail     = $maxsmailtemp;
    $rawpost =~ s/\<img\s*(.*?)\s*\>//isg;
    $rawpost =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)/($2\.$3)/isg;
    $rawpost =~ s/(\n)+/\n/isg;
    $rawpost =~ s/^\n//isg;
    $rawpost =~ s/( )+$//isg;
    $rawpost =~ s/^( )+//isg;
    $rawpost =~ s/\[.+?\]//g;

    chomp $rawpost;

    @postall = split(/\n/,$rawpost);
    $postall = @postall;
    $addpoint = 0;
    if ($postall > 4) {
    	$rawpost = "$postall[0]\n$postall[1]\n$postall[2]\n$postall[3]\n...";
    	$addpoint = 1;
    }
    $maxquotenum = 200 if ($maxquotenum eq "");
    $rawpost = &lbhz($rawpost,$maxquotenum);

    $temppost = qq~\[quote\]\[b\]ÏÂÃæÒıÓÃÓÉ\[u\]$membernametemp\[\/u\]ÔÚ \[i\]$postdate\[\/i\] ·¢±íµÄÄÚÈİ£º\[\/b\]\n$rawpost\n\[\/quote\]\n~;
    if ($htmlstate eq "on")     { $htmlstates = "¿ÉÓÃ";     } else { $htmlstates = "²»¿ÉÓÃ";     }
    if ($idmbcodestate eq "on") { $idmbcodestates = "¿ÉÓÃ"; } else { $idmbcodestates = "²»¿ÉÓÃ"; }
    if ($useemote eq "no") { $emotestates = "²»¿ÉÓÃ"; } else { $emotestates = "¿ÉÓÃ"; }

    if ($badwords) {
	@pairs = split(/\&/,$badwords);
        foreach (@pairs) {
	    ($bad, $good) = split(/=/,$_);
            chomp $good;
            $topictitle =~ s/$bad/$good/isg;
            $temppost =~ s/$bad/$good/isg;
        }
    }
    if ($advpost == 1){
	$advpostmt="[<a href=$thisprog?action=replyquote&forum=$inforum&topic=$intopic&postno=$inpostno&advpost=0>¼ò½àÄ£Ê½</a>]";
	   }else{
        $advpostmt="[<a href=$thisprog?action=replyquote&forum=$inforum&topic=$intopic&postno=$inpostno&advpost=1>¸ß¼¶Ä£Ê½</a>]";
         }
    $output .= qq~
<script>function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
function DoTitle(addTitle) {
var revisedTitle;
var currentTitle = document.FORM.intopictitle.value;
revisedTitle = currentTitle+addTitle;
document.FORM.intopictitle.value=revisedTitle;
document.FORM.intopictitle.focus();
return; }</script>
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
          <tr><td>
             <table cellpadding=4 cellspacing=1 border=0 width=100%>
              <tr>
                <td bgcolor=$titlecolor colspan=2>
                <form action="$thisprog" method=post name="FORM" enctype="multipart/form-data">
                <input type=hidden name="action" value="addreply">
                <input type=hidden name="forum" value="$inforum">
                <input type=hidden name="topic" value="$intopic">
                <font color=$titlefontcolor><b>Ö÷Ìâ±êÌâ</b>£º $topictitle $advpostmt</td>
              </tr>
	      <tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>ÓÃ»§Ãû</b></font></td>
                <td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"><font color=$fontcolormisc>¡¡ <a href="$registerprog">ÄúÃ»ÓĞ×¢²á£¿</a></font></td>
              </tr><tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>ÃÜ¡¡Âë</b></font></td>
                <td bgcolor=$miscbackone><input type=password name="password" value="$inpassword"><font color=$fontcolormisc>¡¡ <a href="$profileprog?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td>
              </tr>
              ~;

               $output .= qq~
	      <tr>
		<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>µ±Ç°ĞÄÇé</b><br><li>½«·ÅÔÚÌù×ÓµÄÇ°Ãæ<BR></font></td>
		<td bgcolor=$miscbackone valign=top>
    ~;

    open (FILE, "${lbdir}data/lbpost.cgi");
     my @posticondata = <FILE>;
     close (FILE);
     chomp @posticondata;

    $tempiconnum=1;
    $tempselect = "";
#    $tempselect = "checked";
    foreach $picture (@posticondata) {
       if ($tempiconnum > 12) {
    	   $tempiconnum = 1;
    	   $output .= qq~<BR>~;
       }
       if ($picture eq $posticon) {$tempselect = "checked";} else {$tempselect = "";}
       $output .= qq~<input type=radio value="$picture" name="posticon" $tempselect><img src=$imagesurl/posticons/$picture $defaultsmilewidth $defaultsmileheight border=0>&nbsp;~;
       $tempiconnum ++;
       $tempselect = "";
    }
      if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||($allowattachment eq "yes")) {
        $output .= qq~
	</td>
	</tr>
	<tr><td bgcolor=$miscbackone>
	<b>ÉÏ´«¸½¼ş»òÍ¼Æ¬</b>(×î´ó $maxupload KB):
	</td>
	<td bgcolor=$miscbacktwo> <input type="file" size=40 name="addme">¡¡¡¡$addtypedisp
	~;
      }
    $output .= qq~
	</td>
	</tr>
	<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>ÄÚÈİ</b><p>
        ÔÚ´ËÂÛÌ³ÖĞ£º<li>HTML ¡¡±êÇ©: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE¡¡±êÇ©</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LB5000 ±êÇ©</a>: <b>$idmbcodestates</b><li>ÌùÍ¼±êÇ©¡¡ : <b>$postpicstates</b><li>Flash ±êÇ© : <b>$postflashstates</b><li>ÒôÀÖ±êÇ© ¡¡: <b>$postsoundstates</b><li>ÎÄ×Ö´óĞ¡ ¡¡: <b>$postfontsizestates</b>$emoticonslink</font></td>
	<td bgcolor=$miscbackone>
	~;
	if ($advpost == 1){
	$output .= qq~
	$insidejs
	~;}
	$output .= qq~
        <TEXTAREA cols=80 name=inpost rows=12 wrap=soft onkeydown=ctlent()>$temppost</TEXTAREA><br>
	~;
	if ($advpost == 1){
	$output .= qq~
	&nbsp;¡¡Ä£Ê½:
	<input type="radio" name="mode" value="help" onClick="thelp(1)">¡¡°ïÖú¡¡
	<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">¡¡ÍêÈ«¡¡
	<input type="radio" name="mode" value="basic"  onClick="thelp(0)">¡¡»ù±¾¡¡¡¡¡¡¡¡ >> <a href=javascript:HighlightAll('FORM.inpost')>¸´ÖÆµ½¼ôÌù°å</a> | <a href=javascript:checklength(document.FORM);>²é¿´ÎÄÕÂ³¤¶È</a> <<
	~;}
	$output .= qq~
	</td></tr>
        </tr>
        ~;
        if (($advpost == 1)&&($emoticons eq "on")){
        $output .= qq~
        <tr>
         <td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>µã»÷±íÇéÍ¼¼´¿ÉÔÚÌù×ÓÖĞ¼ÓÈëÏàÓ¦µÄ±íÇé(Ã¿¸ö±íÇé×î¶àÍ¬Ê±ÏÔÊ¾ $maxsmail ´Î)</B></font><br>&nbsp;
    ~;


     open (FILE, "${lbdir}data/lbemot.cgi");
	my @emoticondata = <FILE>;
	close (FILE);
	chomp @emoticondata;
      	foreach $picture (@emoticondata) {
    		$smileyname = $picture;
    		$smileyname =~ s/\.gif//g;
       		$output .= qq~
               	    <a href="javascript:smilie('$smileyname');"><img src=$emoticonsurl/$picture border=0></a>
               	~;
	}
	$output .= qq~
    	    </td>
            </tr>
            ~;}
            $output .= qq~
            <tr>
              <td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>Ñ¡Ïî</b><p>$helpurl</font></td>
              <td bgcolor=$miscbacktwo><font color=$fontcolormisc><input type=checkbox name="inshowsignature" value="yes" checked>ÊÇ·ñÏÔÊ¾ÄúµÄÇ©Ãû£¿<br>
              $requestnotify
              $emoticonsbutton
              &nbsp;<b>·¢±íÖ®Ç°ÊÇ·ñÔ¤ÀÀ£¿</b><input name="previewfirst" type="radio" value="yes"> ÊÇ¡¡ <input name="previewfirst" type="radio" value="no" checked> ·ñ</font>
              </font></td>
            </tr><tr>
              <td bgcolor=$miscbacktwo colspan=2 align=center>
              <input type=Submit value="·¢ ±í" name=Submit onClick="return clckcntr();">¡¡¡¡<input type="reset" name="Clear" value="Çå ³ı">
            </td></form></tr></table></tr></td></table>
	~;
	@sortedthreads = reverse(@threads);
	&threadreview;
}

sub copy1 {
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @threads = <FILE>;
    close(FILE);
    $posttoget = $inpostno;
    $posttoget--;
    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post) = split(/\t/, $threads[$posttoget]);
	$topictitle =~ s/^£ª£££¡£¦£ª//;

    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;

    $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
    $postdate = &dateformat("$postdate");
    $rawpost = $post;
    if ($previewfirst eq "yes") {
        $rawpost = $inpost;
        $rawpost =~ s/\<p\>/\n\n/ig;
        $rawpost =~ s/\<br\>/\n/ig;
        &preview;
    }
    else {
        &mischeader("¸´ÖÆÌù×Ó");
    }
    if ($badwords) {
        @pairs = split(/\&/,$badwords);
        foreach (@pairs) {
            ($bad, $good) = split(/=/,$_);
            chomp $good;
            $rawpost =~ s/$bad/$good/isg;
            $topictitle =~ s/$bad/$good/isg;
        }
    }

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") {
     	&whosonline("$inmembername\t$forumname\tnone\t¸´ÖÆÌù×Ó<a href=\"$threadprog?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
    }
    else {
	&whosonline("$inmembername\t$forumname(ÃÜ)\tnone\t¸´ÖÆ±£ÃÜÌù×Ó\t");
    }
}

    $temppost = qq~-=-=-=-=-=>\n$rawpost\n-=-=-=-=-=>~;
    $output .= qq~
         <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
                <table cellpadding=4 cellspacing=1 border=0 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2>
                    <form action="$thisprog" method=post>
                    <input type=hidden name="action" value="addreply">
                    <input type=hidden name="forum" value="$inforum">
                    <input type=hidden name="topic" value="$intopic">
                    <font color=$titlefontcolor>Ö÷Ìâ£º $topictitle</td>
                </tr><tr>
                    <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>¸´ÖÆÌù×Ó</b><p></font></td>
                    <td bgcolor=$miscbackone>&nbsp;&nbsp;<textarea cols=90 rows=12 wrap="soft" name="inpost">$temppost</textarea><BR><BR></td>
                </tr><tr>
                 <center>
                <td bgcolor=$miscbackone colspan=2 align=center>
                 <input type="button" value="¸ßÁÁÏÔÊ¾ÎÄ×Ö" onClick="this.form.inpost.focus();this.form.inpost.select();">¡¡¡¡
  		<input type="button" value="¸´ÖÆµ½¼ôÌù°å" name="cmdCopy" onClick="copy(this.form.inpost)"></center></td>
	  </tr></td></table></table>
    ~;
}

sub addreply {
#    &getmember("$inmembername");
    &moderator;
    if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne 'smo') && ($membercode ne "mo") && ($inmembmod ne "yes")) {
	$currenttime = time;
	($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	$lastpost = ($lastpost + $floodcontrollimit);
	if ($lastpost > $currenttime)  {
	    &error("·¢±í»Ø¸´&¹àË®Ô¤·À»úÖÆÒÑ¾­Ê¹ÓÃ£¬Äú±ØĞëµÈ´ı $floodcontrollimit ÃëÖÓ²ÅÄÜÔÙ´Î·¢±í£¡");
	}
    }

    if ($postopen eq "no") {
	&error("·¢±í»ò»Ø¸´Ö÷Ìâ&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±í»ò»Ø¸´Ö÷Ìâ£¡");
    }

    &getforum("$inforum");

    if (($userregistered eq "no")&&(length($inmembername) > 12)) { &error("·¢±íĞÂÖ÷Ìâ&ÄúÊäÈëµÄÓÃ»§ÃûÌ«³¤£¬Çë¿ØÖÆÔÚ6¸öºº×ÖÄÚ£¡");   }
    if (($userregistered eq "no")&&($inmembername =~ /^¿ÍÈË/)) { &error("·¢±íĞÂÖ÷Ìâ&Çë²»ÒªÔÚÓÃ»§ÃûµÄ¿ªÍ·ÖĞÊ¹ÓÃ¿ÍÈË×ÖÑù£¡");   }

    if (($userregistered eq "no")&&($startnewthreads ne "all")) { &error("·¢±íĞÂÖ÷Ìâ&ÄúÃ»ÓĞ×¢²á£¡");   }
    elsif ((($inpassword ne $password)&&($userregistered ne "no"))||(($inpassword ne "")&&($userregistered eq "no"))) { &error("·¢±íĞÂÖ÷Ìâ&ÄúµÄÃÜÂë´íÎó£¡"); }

    elsif ($membercode eq "banned")  { &error("·¢±í&ÒÑ±»½ûÖ¹·¢ÑÔ£¡"); }
    elsif ($inpost eq "")            { &error("·¢±íĞÂ»Ø¸´&±ØĞëÊäÈëÄÚÈİ£¡"); }
    else {
    @allforums = @forums;

    if ($startnewthreads eq "no") {
        unless ($membercode eq "ad" || $membercode eq 'smo' || $inmembmod eq "yes") {
            &error("·¢±íĞÂ»Ø¸´&ÔÚ´ËÂÛÌ³ÖĞÖ»ÄÜÓÉÌ³Ö÷»òÕß°æÖ÷·¢±íĞÂ»Ø¸´£¡");
        }
    }
        $tempaccess = "forumsallowed". "$inforum";
        $testentry = $query->cookie("$tempaccess");


        if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("·¢±í&¶Ô²»Æğ£¬Äú²»ÔÊĞíÔÚ´ËÂÛÌ³·¢±í£¡");
        }

 	if (($startnewthreads eq "all")&&($userregistered eq "no")) {
	    $inmembername = "$inmembername(¿Í)";
	}

	$end_q_tag = 0;
	$srt_q_tag = 0;
	$end_q_tag++ while $inpost =~ m#\[/QUOTE\]#ig;
	$srt_q_tag++ while $inpost =~ m#\[QUOTE\]#ig;
	if ($end_q_tag ne $srt_q_tag) { &error("ÄÚÈİĞ£Ñé³ö´í&ÄãÊäÈëÁË $srt_q_tag ¸ö [QUOTE] ±êÇ©ºÍ $end_q_tag ¸ö [/QUOTE] ±êÇ©£¬ÊıÄ¿²»Æ¥Åä£¡"); }

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        if (-e $filetoopen) {
           &winlock($filetoopen) if ($OS_USED eq "Nt");
           open(FILE, "$filetoopen");
           flock(FILE, 1) if ($OS_USED eq "Unix");
           @allmessages = <FILE>;
           close(FILE);
           &winunlock($filetoopen) if ($OS_USED eq "Nt");
        }
	else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("·¢±í&Õâ¸öÖ÷Ìâ²»´æÔÚ£¡¿ÉÄÜÒÑ¾­±»É¾³ı£¡"); }

        my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 2) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon) = split(/\t/,$in);
        if (($threadstate eq "closed")||($threadstate eq "pollclosed")) { &error("·¢±í»Ø¸´&¶Ô²»Æğ£¬Õâ¸öÖ÷ÌâÒÑ¾­±»Ëø¶¨£¡"); }

        if ($emote) {
 	    @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		($toemote, $beemote) = split(/=/,$_);
		chop $beemote;
		$beemote =~ s/¶ÔÏó/¡¼$inmembername¡½/isg;
		$inpost =~ s/$toemote/$beemote/isg;
	    }
	}

	my $filesize=0;
	if (($addme)&&(($allowattachment ne "no")||($arrowupload ne "off")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"))) {
	   my $up_filename =$query->uploadInfo($addme);
	   my ($up_name,$up_ext) = split(/\./,$up_filename);
	   $up_ext = lc($up_ext);
	   my $checkadd=0;
           for (split(/\,\s*/,$addtype)){
                $checkadd=1,last if ($up_ext eq lc($_));
           }
           if ($up_ext eq "exe"||$up_ext eq "com"||$up_ext eq "pl"||$up_ext eq "cgi"||$up_ext eq "asp"||$up_ext eq "php"||$up_ext eq "php3"||$up_ext eq "phtml"||$up_ext eq "jsp"||$up_ext eq "cfml"||$up_ext eq "dll") {
	       &winunlock($file) if ($OS_USED eq "Nt");
	       &error("ÉÏ´«³ö´í&ÎªÁË°²È«£¬²»Ö§³ÖÄãËùÉÏ´«µÄ¸½¼ş£¬ÇëÖØĞÂÑ¡Ôñ£¡");
	   }
	   if ($checkadd==0) {
		&winunlock($file) if ($OS_USED eq "Nt");
		&error("ÉÏ´«³ö´í&²»Ö§³ÖÄãËùÉÏ´«µÄ¸½¼ş»òÕßÍ¼Æ¬£¬ÇëÖØĞÂÑ¡Ôñ£¡");
	   }

	   my $buffer;
           $replynumber=$#allmessages+1;
 	    open (FILE,">$imagesdir/usr/$inforum/$inforum\_$intopic\_$replynumber.$up_ext");
		binmode (FILE);
		while ((($buffer=$query->readUploadFile($addme,4096)))&&!(($filesize>$maxupload)&&($membercode ne "ad"))){
		$filesize=$filesize+4;
		print FILE $buffer;
	    }
	    close (FILE);
	    if (($filesize>$maxupload)&&($membercode ne "ad")) {
                unlink ("$imagesdir/usr/$inforum/$inforum\_$intopic\_$replynumber.$up_ext");
        	&winunlock($file) if ($OS_USED eq "Nt");
		&error("ÉÏ´«³ö´í&ÉÏ´«ÎÄ¼ş´óĞ¡³¬¹ı$maxupload£¬ÇëÖØĞÂÑ¡Ôñ£¡ ");
	    }
	}

        $inposttemp = $inpost;
	$inposttemp =~ s/\[Õâ¸öÌù×Ó×îºóÓÉ(.+?)±à¼­\]\n//isg;
	$inposttemp =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//ig;
	$inposttemp =~ s/\[quote\](.*)\[\/quote\]//ig;
	$inposttemp =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/ig;
	$maxsmailtemp = $maxsmail;
	$maxsmail     = 0;
	$inposttemp   = &doemoticons("$inposttemp");
	$maxsmail     = $maxsmailtemp;
	$inposttemp =~ s/\<img\s*(.*?)\s*\>//isg;
	$inposttemp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|bmp|gif)//isg;
	$inposttemp =~ s/( )+$//isg;
	$inposttemp =~ s/^( )+//isg;
	$inposttemp =~ s/<(.|\n)+?>//g;
	$inposttemp =~ s/\[.+?\]//g;
        $inposttemp =~ s/[\a\f\n\e\0\r\t]//g;
        chomp $inposttemp;

        $inposttemp = &lbhz($inposttemp,$maxsavepost);

	$lastreplymessgae = $allmessages[-1];
        (my $ainmembername,my $no,my $no,my $no,my $no,my $no,my $ainpost,my $no) = split(/\t/,$lastreplymessgae);
 	if (($inmembername eq $ainmembername)&&($inpost eq $ainpost)) {
            &winunlock($file) if ($OS_USED eq "Nt");
    	    &error("·¢±í»Ø¸´&Çë²»ÒªÖØ¸´»Ø¸´£¬ÒÑ¾­´æÔÚÓë´Ë»Ø¸´ÄÚÈİÏàÍ¬µÄ¶øÇÒÊÇÄã·¢µÄ»Ø¸´ÁË£¡");
	}
        ($trash, $topictitle) = split(/\t/,$allmessages[0]);
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $messages (@allmessages) {
            chomp $messages;
            print FILE "$messages\n";
        }
        print FILE "$inmembername\t$topictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t";
        close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");

        $threadposts = @allmessages;

        $posticon = $inposticon if ($sortposticonshow eq "yes");

        $threadviews = ($threadposts+1)*6 if ($threadviews < $threadposts);
	$threadviews = 9999 if ($threadviews > 10000);

        if (open(FILE, ">$file")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        my $topictitletemp = $topictitle;
        $topictitletemp =~ s/^£ª£££¡£¦£ª//;
        print FILE "$intopic\t$topictitletemp\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$inmembername\t$currenttime\t$posticon\t$inposttemp\t";
        close(FILE);
        }
        &winunlock($file) if ($OS_USED eq "Nt");
        $topictitle2 = $topictitle;
        $topictitle2 =~ s/^£ª£££¡£¦£ª//;
        $file = "$lbdir" . "boarddata/list$inforum.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
	$listall = @listall;

    if ($listall >= 300) {
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        print LIST "$intopic\t$topictitle2\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$inmembername\t$currenttime\t$posticon\t$inposttemp\t\n";
        foreach (@listall) {
            ($listone,my $noneed) = split(/\t/,$_);
	    $_ =~ s/[\n\r]//isg;
            print LIST "$_\n" if (($listone ne $intopic)&&($listone ne "")&&($listone =~ /^[0-9]+$/));
        }
        close (LIST);
        }
        &winunlock($file);
    }
    else {
        &winunlock($file);
        rebuildLIST(-Forum=>"$inforum");
    }

        $cleanmembername = $inmembername;
        $cleanmembername =~ s/ /\_/isg;
	$cleanmembername =~ tr/A-Z/a-z/;
        $numberofreplys++;
        $lastpostdate = "$currenttime\%\%\%$threadprog?forum=$inforum&topic=$intopic\%\%\%$topictitle2" if ($privateforum ne "yes");
        chomp $lastpostdate;

    if (($userregistered ne "no")&&($password ne "")) {
        $filetomake = "$lbdir" . "$memdir/$cleanmembername.cgi";
        $filetomake = &stripMETA($filetomake);
        &winlock($filetomake);
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$inmembername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t";
        close(FILE);
        }
        &winunlock($filetomake);
    }

      $filetoopen = "$lbdir" . "data/allforums.cgi";
      my $filetoopens = &lockfilename($filetoopen);
      if (!(-e "$filetoopens.lck")) {
        &winlock($filetoopen);
        if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) {
        chomp($forum);
        next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    $lastposter = $inmembername;
                    $lastposttime = $currenttime;
                    $posts++;
                    $lastposttime = "$lastposttime\%\%\%$intopic\%\%\%$topictitle2";
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
        }
        close(FILE);
        }
        &winunlock($filetoopen);
      }
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        my $filetoopens = &lockfilename($filetomake);
  if (!(-e "$filetoopens.lck")) {
        $totalposts++;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
       }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
  }

        if ($emailfunctions eq "on") {
            $filetoopen = "$lbdir" . "forum$inforum/$intopic.mal.pl";
            open (FILE, "$filetoopen");
            @maildata = <FILE>;
            close (FILE);

            $mailall = "$inmembername\t$emailaddress\t";
            if ($innotify eq "yes") {
              if (open (FILE, ">$filetoopen")) {
                print FILE "$mailall\n";
                foreach $line (@maildata) {
                    chomp $line;
                    print FILE "$line\n" if ($mailall ne $line);
                }
                close (FILE);
              }
            }
	    $toemail = '';
            foreach $dataline (@maildata) {
                ($postersname,$posteremailaddress) = split(/\t/,$dataline);
                if ($lastemailsent ne $postersname) {
                        if ($inmembername eq $postersname) { next; }
                        next if ($posteremailaddress eq "");
        		$posteremailaddress =~ s/[\a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
        		next if ($posteremailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/);
            		if ($toemail eq "") {$toemail = '$posteremailaddress';} else {$toemail .= ', $posteremailaddress';}
                        $lastemailsent = $postersname;
		}
	    }

            $output .= "\n\n<!-- ´¦Àí Email ·¢ËÍ --> \n\n";
            chomp $toemail;
            $toemail =~ s/\\//g;
            $fromemail = $adminemail_out;
            chomp $fromemail;
            $fromemail =~ s/\\//g;
            $topictitle =~ s/&quot\;/\"/g;

            $to = $toemail;
            $from = $fromemail;
            $subject = "[$forumname] »Ø¸´Í¨Öª";
            $message .= "$boardname\n";
            $message .= "$boardurl/$forumsummaryprog\n";
            $message .= "---------------------------------------------------------------------\n\n";
            $message .= "$postersname, ÄãµÄÌù×ÓÓĞÁËÒ»¸öĞÂ»Ø¸´£¡\n\n";
            $message .= "»Ø¸´ÈË£º $inmembername\n";
            $message .= "·ÖÀà£º $category\n";
            $message .= "ÂÛÌ³£º $forumname\n";
            $message .= "Ö÷Ìâ£º $topictitle\n";
            $message .= "µã»÷ÏÂÃæµÄÁ´½ÓÈ¥²é¿´ÏêÏ¸ÄÚÈİ£º\n\n";
            $message .= "$boardurl/$threadprog?forum=$inforum&topic=$intopic\n\n";
            $message .= "---------------------------------------------------------------------\n";

            &sendmail($from, $emailaddress, $to, $SMTP_SERVER, $subject, $message);
        }

    $numberofitems = $totalthreadposts + 1;
    $numberofpages = $numberofitems / $maxthreads;
        if ($numberofitems > $maxthreads) {
            if ($maxthreads < $numberofitems) {
                ($integer,$decimal) = split(/\./,$numberofpages);
                if ($decimal > 0) { $numberofpages = $integer + 1; }
                $pagestart = 0;
                $counter = 0;
                while ($numberofpages > $counter) {
                    $counter++;
                    $threadpages .= qq~ <a href="$threadprog?forum=$inforum&topic=$topicid&start=$pagestart">$counter</a> ~;
                    $pagestart = $pagestart + $maxthreads;
                }
            }
	    $pagestoshow = qq~<font color=$forumfontcolor> &nbsp;[ µÚ&nbsp;$threadpagesÒ³ ]~;
        }

        &mischeader("»Ø¸´³É¹¦");

        if ($refreshurl == 1) {
	        $relocurl = "$threadprog?forum=$inforum&topic=$intopic";
	}
	else {
               	$relocurl = "$forumsprog?forum=$inforum";
        }
        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>Ğ»Ğ»£¡ÄúµÄ»Ø¸´ÒÑ¾­³É¹¦·¢±í£¡</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡£º
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$intopic">·µ»ØÖ÷Ìâ</a>  $pagestoshow $pages
            <li><a href="$forumsprog?forum=$inforum">·µ»ØÂÛÌ³</a>
            <li><a href="$forumsummaryprog">·µ»ØÂÛÌ³Ê×Ò³</a>
            <li><a href="$postingsprog?action=lock&forum=$inforum&topic=$intopic&checked=yes">Ëø¶¨Ìù×Ó</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
    }
}

sub threadreview {

        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $topictitle =~ s/$bad/$good/isg;
                }
            }
    $threadsize=@sortedthreads;
    $listmy=0 if ($listmy eq "");
    if ($listmy==0){
    $listmy=qq~[<a href=$thisprog?action=$action&forum=$inforum&topic=$intopic&postno=$inpostno&listmy=1>ÁĞ³öËùÓĞ»Ø¸´</a>]
    ~;
    $listme=",×î¶àÁĞ³ö $maxlistpost ¸ö";
    $threadsize=$maxlistpost if ($threadsize>$maxlistpost);
    }else{
    $listmy=qq~[<a href=$thisprog?action=$action&forum=$inforum&topic=$intopic&postno=$inpostno&listmy=0>ÁĞ³öÇ° $maxlistpost ¸ö»Ø¸´</a>]
    ~;
    $listme="";
    }
    $output .= qq~
        <p>
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
        <tr><td>
        <table cellpadding=8 cellspacing=1 border=0 width=100% >
        <tr>
        <td bgcolor=$titlecolor colspan=2 ><font color=$titlefontcolor><b>Ìù×ÓÒ»ÀÀ $topictitle (ĞÂ»Ø¸´ÔÚ×îÇ°$listme)</b>¡¡ $listmy</td>
        ~;

    for (my $i=0;$i<$threadsize;$i++){
    	$threadline=$sortedthreads[$i];
        ($membername, $topictitle, $postipaddress ,$showemoticons ,$showsignature ,$postdate ,$post, $posticon) = split(/\t/, $threadline);
        $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
        $postdate = &dateformat("$postdate");
        $post = &lbcode("$post");
        $post = &doemoticons("$post");
        if (($emoticons eq 'on') && ($showemoticons eq 'yes')) {
	   $post = &smilecode("$post");
	}

        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $post =~ s/$bad/$good/isg;
                }
            }
    $output .= qq~
    <table style="TABLE-LAYOUT: fixed" cellpadding=8 cellspacing=1 border=0 width=100%>
        <tr>
            <td bgcolor="$miscbackone" rowspan=2 valign="top" width=20%><font color=$fontcolormisc>
            <b>$membername</b></font></td>
            <td bgcolor="$miscbackone" ><font color=$fontcolormisc><b>·¢±íÓÚ£º $postdate</b></td>
        </tr>
        <tr>
         <td bgcolor="$miscbackone" style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word"><font color=$fontcolormisc>$post</td>
        </tr>
        <tr>
            <td colspan=2 bgcolor="$miscbacktwo">&nbsp;</td>
        </tr>
        </table>
        ~;
    }
    $output .= qq~</table></td></tr></table>~;
}

sub preview {
    $postbackcolor = "$postcolorone";
    $postfontcolor = "$postfontcolorone";
    $inpost =~ s/&lt\;br&gt\;&lt\;br&gt\;//g;
    $post = $inpost;
    $post =~ s/\n\n/\<p\>/g;
    $post =~ s/\n/\<br\>/g;
    if ($emote) {
 	    @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		($toemote, $beemote) = split(/=/,$_);
		chop $beemote;
		$beemote =~ s/¶ÔÏó/¡¼$inmembername¡½/isg;
		$post =~ s/$toemote/$beemote/isg;
	    }
	}

    $post = &lbcode("$post");

    if ($emoticons eq "on") {
           $post = &doemoticons("$post");
	   $post = &smilecode("$post");
    }
    &mischeader("»Ø¸´Ô¤ÀÀ");
    $output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
        <tr><td>
        <table cellpadding=4 cellspacing=1 border=0 width=100%>
        <tr>
            <td bgcolor=$titlecolor colspan=3 width=100%><font color=$titlefontcolor>Ô¤ÀÀ</td>
        </tr>
        <tr>
            <td bgcolor="$postbackcolor" rowspan=3 valign="top" width=20%><font face=$posternamefont color=$posternamecolor>
            <b>$inmembername</b></font></td>
            <td bgcolor="$postbackcolor" colspan=2><font color=$postfontcolor><b>Ô¤ÀÀ</b> </td></tr>
        <tr>
            <td colspan=2 bgcolor="$postbackcolor"><font color=$postfontcolor>$post</td></tr></table></td>
            </tr></table>
        <p>
    ~;
}

END {
  if ($cpudisp eq "1") {
    $TT1 = new Benchmark;
    $td  = Benchmark::timediff($TT1,  $TT0);
    $td  = Benchmark::timestr($td);
    $td  =~ /(\d+)\s*wallclock secs \(\s*?(\d*?\.\d*?)\s*usr\s*\+\s*(\d*?\.\d*?)\s*sys/i;
    print "<center><font color=$cpudispcolor>³ÌĞòÕ¼ÓÃ CPU Ê±¼ä£º$2 usr + $3 sys";
  }
}
