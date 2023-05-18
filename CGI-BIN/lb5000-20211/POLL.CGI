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
require "lbmail.lib.pl";
require "lb.lib.pl";
require "postjs.cgi";
require "rebuildlist.pl";
$|++;                        # Unbuffer the output
$thisprog = "poll.cgi";
$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/\/$//;
$query = new LBCGI;
&ipbanned; #·âÉ±Ò»Ğ© ip

$addme=$query->param('addme');
for ('forum','topic','membername','password','action','postno','inshowsignature',
     'notify','inshowemoticons','intopictitle','intopicdescription','myChoice',
     'inpost','posticon','id','threadname') {
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
$postipaddress = "$ENV{'REMOTE_ADDR'}=$trueipaddress";
$inposticon    = $posticon;

$inselectstyle   = $query->cookie("selectstyle");
&error("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
else { if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; } }

$advpost=$query->param('advpost');
if ($advpost eq ""){$advpost   = $query->cookie("advpost");}
$advpost=0 if ($advpost eq "");

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

   $advcookie     = cookie(-name    =>   "advpost",
                         -value   =>   "$advpost",
                         -expires =>   "+30d",
                         -path    =>   "$cookiepath/"
                         );

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

    $maxpollitem = 5 if (($maxpollitem eq "")||($maxpollitem !~ /^[0-9]+$/));
    $maxpollitem = 5 if ($maxpollitem < 5);
    $maxpollitem = 50 if ($maxpollitem > 50);

    if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) 	{ &error("ÆÕÍ¨&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡"); }
    if (($threadname) && ($threadname !~ /^[0-9]+$/)) 	{ &error("ÆÕÍ¨&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡"); }
    if (($id) && ($id !~ /^[0-9]+$/)) 			{ &error("ÆÕÍ¨&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡"); }
    $helpurl = &helpfiles("ÔÄ¶Á±ê¼Ç");
    $helpurl = qq~$helpurl<img src=$imagesurl/images/help_b.gif border=0></a>~;

    my %Mode = (
    'new'   =>    \&newthread,
    );

    if ($arrawpostpic eq "on")      { $postpicstates = "ÔÊĞí";}      else {$postpicstates = "½ûÖ¹";}
    if ($arrawpostfontsize eq "on") { $postfontsizestates = "ÔÊĞí";} else {$postfontsizestates = "½ûÖ¹";}
    if ($arrawpostsound eq "on")    { $postsoundstates = "ÔÊĞí";}    else {$postsoundstates = "½ûÖ¹";}
    if($Mode{$action}) {
        $Mode{$action}->();
    }
    elsif ($action eq "addnew" )  { &addnewthread; }
    elsif ($action eq "poll" )  { &poll; }
    else { &error("ÆÕÍ¨&ÇëÒÔÕıÈ·µÄ·½Ê½·ÃÎÊ±¾³ÌĞò£¡"); }

    &output(
	-Title   => "$boardname - ÔÚ$forumnameÄÚ·¢ĞÂÍ¶Æ±",
	-ToPrint => $output,
	-Version => $versionnumber
    );

sub newthread {
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
#    &getmember("$inmembername");
     &moderator;
    if (($floodcontrol eq "on") && ($membercode ne "ad") && ($inmembmod ne "yes") && ($membercode ne 'smo')) {
	$currenttime = time;
        ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
        $lastpost = ($lastpost + $floodcontrollimit);
        if ($lastpost > $currenttime)  {
            &error("·¢±íĞÂÍ¶Æ±&¹àË®Ô¤·À»úÖÆÒÑ¾­Ê¹ÓÃ£¬Äú±ØĞëµÈ´ı $floodcontrollimit ÃëÖÓ²ÅÄÜÔÙ´Î·¢±í£¡");
        }
    }
    &getforum("$inforum");
    $tempaccess = "forumsallowed". "$inforum";
    $testentry = $query->cookie("$tempaccess");

    if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad") || ($membercode eq 'smo')) { $allowed = "yes"; }

    if ($pollopen eq "no") {
	&error("·¢±íĞÂÍ¶Æ±&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±íĞÂÍ¶Æ±£¡");
    }

    if (($privateforum eq "yes") && ($allowed ne "yes")) {
	&error("·¢±íĞÂÍ¶Æ±&¶Ô²»Æğ£¬ÄúÃ»ÓĞÔÚ´ËÂÛÌ³ÖĞ·¢±íµÄÈ¨Àû£¡");
    }

    if ($emoticons eq "on") {
        $emoticonslink = qq~<li><a href="javascript:openScript('$miscprog?action=showsmilies',300,350)">ÔÊĞí<B>Ê¹ÓÃ</B>±íÇé×Ö·û×ª»»</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>ÄúÊÇ·ñÏ£Íû<b>Ê¹ÓÃ</b>±íÇé×Ö·û×ª»»ÔÚÄúµÄÎÄÕÂÖĞ£¿<br>~;
    }

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") {
    	&whosonline("$inmembername\t$forumname\tnone\t·¢±íĞÂÍ¶Æ±\t");
    }
    else {
        &whosonline("$inmembername\t$forumname(ÃÜ)\tnone\t·¢±íĞÂµÄ±£ÃÜÍ¶Æ±\t");
    }
}

    &mischeader("·¢±íĞÂÍ¶Æ±");

    if ($emailfunctions eq "on") {
           if ($innotify eq "yes") {
              $requestnotify = qq~<input type=checkbox name="notify" value="yes" checked>ÓĞÍ¶Æ±Ê±Ê¹ÓÃÓÊ¼şÍ¨ÖªÄú£¿<br>~;
              }
              else {
                   $requestnotify = qq~<input type=checkbox name="notify" value="yes">ÓĞÍ¶Æ±Ê±Ê¹ÓÃÓÊ¼şÍ¨ÖªÄú£¿<br>~;
                   }
            }

    if ($startnewthreads eq "no") {
        $startthreads = "ÔÚ´ËÂÛÌ³ÖĞĞÂµÄÍ¶Æ±ºÍ»Ø¸´Ìù×ÓÖ»ÄÜÓÉÌ³Ö÷¡¢°æÖ÷·¢±í£¡";
    }
    elsif ($startnewthreads eq "follow") {
        $startthreads = "ÔÚ´ËÂÛÌ³ÖĞĞÂµÄÍ¶Æ±Ö»ÄÜÓÉÌ³Ö÷¡¢°æÖ÷·¢±í£¡ÆÕÍ¨»áÔ±Ö»¿ÉÒÔ¸úÌù£¡";
    }
    elsif ($startnewthreads eq "all") {
	 $startthreads = "ÈÎºÎÈË¾ù¿ÉÒÔ·¢±íĞÂµÄÍ¶Æ±ºÍ»Ø¸´Ìù×Ó£¬Î´×¢²áÓÃ»§·¢ÌùÃÜÂëÇëÁô¿Õ£¡";
    }
    else {
        $startthreads = "ËùÓĞ×¢²á»áÔ±¾ù¿ÉÒÔ·¢±íĞÂµÄÍ¶Æ±ºÍ»Ø¸´Ìù×Ó£¡";
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
        if ($arrawpostflash eq "on") { $postflashstates = "ÔÊĞí";} else {$postflashstates = "½ûÖ¹";}
    	if ($useemote eq "no") { $emotestates = "²»¿ÉÓÃ"; } else { $emotestates = "¿ÉÓÃ"; }
    	if ($advpost == 1){
	$advpostmt="[<a href=$thisprog?action=new&forum=$inforum&advpost=0>¼ò½àÄ£Ê½</a>]";
	   }else{
        $advpostmt="[<a href=$thisprog?action=new&forum=$inforum&advpost=1>¸ß¼¶Ä£Ê½</a>]";
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
                <input type=hidden name="action" value="addnew">
                <input type=hidden name="forum" value="$inforum">
        	<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            	<tr><td>
                <table cellpadding=3 cellspacing=1 border=0 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2><font color=$titlefontcolor><b>Ë­¿ÉÒÔ·¢±í£¿</b> $startthreads $advpostmt</td>
                </tr>
                <tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>Í¶Æ±±êÌâ</b></font>¡¡
              <SELECT name=font onchange=DoTitle(this.options[this.selectedIndex].value)>
              <OPTION selected value="">Ñ¡Ôñ»°Ìâ</OPTION> <OPTION value=[Ô­´´]>[Ô­´´]</OPTION>
              <OPTION value=[×ªÌû]>[×ªÌû]</OPTION> <OPTION value=[¹àË®]>[¹àË®]</OPTION>
              <OPTION value=[ÌÖÂÛ]>[ÌÖÂÛ]</OPTION> <OPTION value=[ÇóÖú]>[ÇóÖú]</OPTION>
              <OPTION value=[ÍÆ¼ö]>[ÍÆ¼ö]</OPTION> <OPTION value=[¹«¸æ]>[¹«¸æ]</OPTION>
              <OPTION value=[×¢Òâ]>[×¢Òâ]</OPTION> <OPTION value=[ÌùÍ¼]>[ÌùÍ¼]</OPTION>
              <OPTION value=[½¨Òé]>[½¨Òé]</OPTION> <OPTION value=[ÏÂÔØ]>[ÏÂÔØ]</OPTION>
              <OPTION value=[·ÖÏí]>[·ÖÏí]</OPTION></SELECT></td>
                <td bgcolor=$miscbackone>¡¡<input type=text size=60 maxlength=80 name="intopictitle">¡¡²»µÃ³¬¹ı 40 ¸öºº×Ö</td>
                </tr><tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>ÓÃ»§Ãû</b></font></td>
                <td bgcolor=$miscbackone>¡¡<input type=text name="membername" value="$inmembername">¡¡ <font color=$fontcolormisc><a href="$registerprog">ÄúÃ»ÓĞ×¢²á£¿</a></font></td>
                </tr><tr>
                <td bgcolor=$miscbackone><font color=$fontcolormisc><b>ÃÜ¡¡Âë</b></font></td>
                <td bgcolor=$miscbackone>¡¡<input type=password name="password" value="$inpassword">¡¡ <font color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td>
                </tr>
		<tr>
		<td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>Í¶Æ±ÏîÄ¿</b><br><li>Ã¿ĞĞÒ»¸öÍ¶Æ±ÏîÄ¿£¬×î¶à <B>$maxpollitem</b> Ïî<BR><li>³¬¹ı×Ô¶¯×÷·Ï£¬¿ÕĞĞ×Ô¶¯¹ıÂË<BR><li>Èç¹ûÍ¶Æ±ĞèÒª¶àÑ¡£¬ÇëÔÚÑ¡ÔñÖĞ´ò¹³</font></td>
		<td bgcolor=$miscbacktwo valign=top>
		¡¡<TEXTAREA cols=58 name=posticon rows=6 wrap=soft >$posticon</TEXTAREA><BR>
                ¡¡<input type=checkbox name="inshowsignature" value="yes">´ËÍ¶Æ±ÊÇ·ñÔÊĞí¶àÑ¡£¿<br>
		</td>
		</tr>
                <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>Í¶Æ±ÏîÄ¿ËµÃ÷£º</b><p>
                <li>HTML ¡¡±êÇ©: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE¡¡±êÇ©</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LB5000 ±êÇ©</a>: <b>$idmbcodestates</b><li>ÌùÍ¼±êÇ© ¡¡: <b>$postpicstates</b><li>Flash ±êÇ© : <b>$postflashstates</b><li>ÒôÀÖ±êÇ© ¡¡: <b>$postsoundstates</b><li>ÎÄ×Ö´óĞ¡ ¡¡: <b>$postfontsizestates</b>$emoticonslink</font></td>
		<td bgcolor=$miscbackone>
		~;
	if ($advpost == 1){
	$output .= qq~
	$insidejs
	~;}
	$output .= qq~
		<TEXTAREA cols=80 name=inpost rows=8 wrap="soft" onkeydown=ctlent()>$inpost</TEXTAREA><br>
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
                <td bgcolor=$miscbacktwo><font color=$fontcolormisc>
                ¡¡$requestnotify
                ¡¡$emoticonsbutton
                <BR>
                </td>
                </tr><tr>
                <td bgcolor=$miscbacktwo colspan=2 align=center>
                <input type=Submit value="·¢ ²¼" name=Submit"  onClick="return clckcntr();">¡¡¡¡¡¡<input type="reset" name="Clear" value="Çå ³ı">
                </td></form></tr>
            </table>
        </tr></td></table>
        ~;
}

sub addnewthread {
#    &getmember("$inmembername");
    &moderator;
    if (($floodcontrol eq "on") &&($membercode ne 'smo') && ($membercode ne "ad") && ($inmembmod ne "yes")) {
	$currenttime = time;
	($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	$lastpost = ($lastpost + $floodcontrollimit);
	if ($lastpost > $currenttime)  {
           &error("·¢±íĞÂÍ¶Æ±&¹àË®Ô¤·À»úÖÆÒÑ¾­Ê¹ÓÃ£¬Äú±ØĞëµÈ´ı $floodcontrollimit ÃëÖÓ²ÅÄÜÔÙ´Î·¢±í£¡");
	}
    }

    if ($pollopen eq "no") {
	&error("·¢±íĞÂÍ¶Æ±&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±íĞÂÍ¶Æ±£¡");
    }

    $inposticon=~s/<p>/<BR>/isg;
    $inposticon=~s/<BR><BR>/<BR>/isg;
    $inposticon =~ s/(.*)<BR>$/$1/i;
    $inposticon =~ s/^<BR>(.*)/$1/i;

    $inposticontemp = $inposticon;
    $inposticontemp=~s/<br>/\t/ig;
    @temppoll = split(/\t/, $inposticontemp);
    $temppoll = @temppoll;

    &getforum("$inforum");

    if (($userregistered eq "no")&&(length($inmembername) > 12)) { &error("·¢±íĞÂÖ÷Ìâ&ÄúÊäÈëµÄÓÃ»§ÃûÌ«³¤£¬Çë¿ØÖÆÔÚ6¸öºº×ÖÄÚ£¡");   }
    if (($userregistered eq "no")&&($inmembername =~ /^¿ÍÈË/)) { &error("·¢±íĞÂÖ÷Ìâ&Çë²»ÒªÔÚÓÃ»§ÃûµÄ¿ªÍ·ÖĞÊ¹ÓÃ¿ÍÈË×ÖÑù£¡");   }

    if (($userregistered eq "no")&&($startnewthreads ne "all")) { &error("·¢±íĞÂÖ÷Ìâ&ÄúÃ»ÓĞ×¢²á£¡");   }
    elsif ((($inpassword ne $password)&&($userregistered ne "no"))||(($inpassword ne "")&&($userregistered eq "no"))) { &error("·¢±íĞÂÖ÷Ìâ&ÄúµÄÃÜÂë´íÎó£¡"); }
    elsif ($membercode eq "banned")     { &error("Ìí¼Ó»Ø¸´&Äú±»½ûÖ¹·¢ÑÔ£¡"); }
    elsif ($intopictitle eq "")         { &error("·¢±íĞÂÍ¶Æ±&±ØĞëÊäÈëÖ÷Ìâ±êÌâ£¡"); }
    elsif (length($intopictitle) > 92)  { &error("·¢±íĞÂÍ¶Æ±&Ö÷Ìâ±êÌâ¹ı³¤£¡"); }
    elsif ($inposticon !~ m/<br>/i)	{ &error("·¢±íĞÂÍ¶Æ±&Í¶Æ±Ñ¡ÏîÌ«ÉÙ£¡"); }
    elsif ($temppoll > $maxpollitem )	{ &error("·¢±íĞÂÍ¶Æ±&Í¶Æ±Ñ¡Ïî¹ı¶à£¬²»ÄÜ³¬¹ı $maxpollitem Ïî£¡(Äú´Ë´ÎÍ¶Æ±µÄÑ¡ÏîÓĞ $temppoll Ïî)"); }
    else  {
	if ($startnewthreads eq "no") {
          unless ($membercode eq "ad" || $membercode eq 'smo'|| $inmembmod eq "yes") {
            &error("·¢±íĞÂÍ¶Æ±&ÔÚ´ËÂÛÌ³ÖĞÖ»ÄÜÓÉÌ³Ö÷»òÕß°æÖ÷·¢±íĞÂÍ¶Æ±£¡");
          }
    	}
	elsif (($startnewthreads eq "follow") &&($action eq "addnew")) {
	   unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes") {
		&error("·¢±íĞÂÖ÷Ìâ&ÔÚ´ËÂÛÌ³ÖĞÖ»ÄÜÓÉÌ³Ö÷»òÕß°æÖ÷·¢±íĞÂÖ÷Ìâ£¡");
	   }
	}
	elsif (($startnewthreads eq "all")&&($userregistered eq "no")) {
	    $inmembername = "$inmembername(¿Í)";
	}

        $intopictitle =~ s/()+//isg;
	$tempintopictitle = $intopictitle;
	$tempintopictitle =~ s/ //g;
	$tempintopictitle =~ s/\&nbsp\;//g;
	$tempintopictitle =~ s/¡¡//g;
	if ($tempintopictitle eq "") { &error("·¢±íĞÂÍ¶Æ±&Ö÷Ìâ±êÌâÓĞÎÊÌâ£¡"); }
        undef $tempintopictitle;

        $tempaccess = "forumsallowed". "$inforum";
        $testentry = $query->cookie("$tempaccess");

        if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')) { $allowed = "yes"; }
        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("·¢±íÍ¶Æ±&¶Ô²»Æğ£¬Äú²»ÔÊĞíÔÚ´ËÂÛÌ³·¢±íÍ¶Æ±£¡");
        }

        if ($emote) {
 	    @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		($toemote, $beemote) = split(/=/,$_);
		chop $beemote;
		$beemote =~ s/¶ÔÏó/¡¼$inmembername¡½/isg;
		$inpost =~ s/$toemote/$beemote/isg;
	    }
	}

     $filetoopen = "$lbdir" . "boarddata/lastnum$inforum.cgi";
     if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        $newthreadnumber = <FILE>;
        close(FILE);
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
            (my $amembername,my $atopictitle,my $no,my $no,my $no,my $no,my $apost,my $aposticon) = split(/\t/, $threaddata);
	    if (($amembername eq $inmembername)&&(($apost eq $inpost)&&($apost ne "")||($atopictitle eq $intopictitle)||($aposticon eq $inposticon))) {
		$filetoopen = "$lbdir" . "boarddata/lastnum$inforum.cgi";
	        if (open(FILE, ">$filetoopen")) {
        	flock(FILE, 2) if ($OS_USED eq "Unix");
        	print FILE $oldthreadnumber;
        	close(FILE);
        	}
	    	&error("·¢±íĞÂÍ¶Æ±&Çë²»ÒªÖØ¸´·¢Í¶Æ±£¬ÒÑ¾­´æÔÚÓë´ËÍ¶Æ±Ö÷ÌâÏàÍ¬»òÕßÄÚÈİÏàÍ¬µÄ¶øÇÒÊÇÄã·¢µÄÍ¶Æ±ÁË£¡");
	    }
	}
	$intopictitletemp = $intopictitle ;
	$intopictitletemp =~ s/^£ª£££¡£¦£ª//;
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
		$recentposts=@recentposts;
		if ($recentposts<$maxpostreport) {
		    $maxpostreport=$recentposts;
		}
		else {
		    $maxpostreport--;
		}
		if (open (FILE, ">$filetomakeopen")) {
		flock (FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inmembername\t\n";
		for ($i=0;$i<$maxpostreport;$i++) {
		    print FILE $recentposts[$i];
		}
		close(FILE);
		}
		&winunlock($filetomakeopen) if ($OS_USED eq "Nt");
	    }
	    else {
		if (open (FILE, ">$filetomakeopen")) {
		print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inmembername\t\n";
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
        &winunlock($file);
	$listall = @listall;
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
        print FILE "$newthreadnumber\t$intopictitletemp\t$intopicdescription\tpoll\t0\t0\t$inmembername\t$currenttime\t\t$currenttime\t<BR>\t$inposttemp\t";
        close(FILE);
	}
        
        $filetomake = "$lbdir" . "forum$inforum/$newthreadnumber.thd.cgi";
        if (open(FILE, ">$filetomake")) {
        print FILE "$inmembername\t$intopictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t";
        close(FILE);
        }

	if ($listall >= 300) {
            &winlock($file);
            if (open (LIST, ">$file")) {
            flock (LIST, 2) if ($OS_USED eq "Unix");
            print LIST "$newthreadnumber\t$intopictitletemp\t$intopicdescription\tpoll\t0\t0\t$inmembername\t$currenttime\t\t$currenttime\t<BR>\t$inposttemp\t\n";
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
            rebuildLIST(-Forum=>"$inforum");
	}

        &getforum("$inforum");

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
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);

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

        if (($emailfunctions eq "on") && ($innotify eq "yes")) {
            $filetomake = "$lbdir" . "forum$inforum/$newthreadnumber.mal.pl";
            if (open (FILE, ">$filetomake")) {
            print FILE "$inmembername\t$emailaddress\t\n";
            close (FILE);
            }
        }

        &mischeader("ĞÂÍ¶Æ±·¢±í³É¹¦");

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
            <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>Ğ»Ğ»£¡ÄúµÄĞÂÍ¶Æ±ÒÑ¾­·¢±í³É¹¦£¡</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$newthreadnumber">·µ»ØĞÂÍ¶Æ±</a>
            <li><a href="$forumsprog?forum=$inforum">·µ»ØÂÛÌ³</a>
            <li><a href="$forumsummaryprog">·µ»ØÂÛÌ³Ê×Ò³</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;

    }
}

sub poll {
	$filetomake = "$lbdir" . "forum$id/$threadname.poll.cgi";
	undef @myChoice;
        @myChoice = $query -> param('myChoice');

	&error("Í¶Æ±´íÎó&ÄãÊÇ¿ÍÈËÎŞÈ¨Í¶Æ±£¡")  if (($inmembername eq "¿ÍÈË")||($inmembername eq ""));

	&winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, "$filetomake");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allpoll = <FILE>;
        close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	foreach (@allpoll){
	    (my $tmpinmembername, my $tmpmyChoice)=split(/\t/, $_);
	    &error("Í¶Æ±´íÎó&ÄãÒÑ¾­Í¶¹ıÆ±ÁË£¬²»ÄÜÔÙÍ¶£¡") if (lc($tmpinmembername) eq lc($inmembername));
	}

	$myChoicenow = 0;

	&winlock($filetomake) if ($OS_USED eq "Nt");
        if (open (FILE, ">>$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $myChoice (@myChoice) {
            if (($myChoice ne "") && ($myChoice =~ /^[0-9]+$/)) {
            	print FILE "$inmembername\t$myChoice\t\n";
                $myChoicenow = 1;
            }
	}
        close (FILE);
        }
	&winunlock($filetomake) if ($OS_USED eq "Nt");

	&error("Í¶Æ±´íÎó&ÄãÎ´Ñ¡Í¶Æ±£¬ÇëÖØÍ¶£¡") if ($myChoicenow eq 0);

	my $file = "$lbdir" . "forum$id/$threadname.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 1) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\t/,$in);

        if (open(FILE, ">$file")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$threadname\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t";
        close(FILE);
        }
        &winunlock($file) if ($OS_USED eq "Nt");

        my $file1 = "$lbdir" . "forum$id/$threadname.thd.cgi";
        open (TMP1, "$file1");
        flock (TMP1, 1) if ($OS_USED eq "Unix");
        @tmp = <TMP1>;
        close (TMP);
        $tmp1 = $tmp[-1];
        ($no, $no, $no, $no, $no ,$no, $post1, $no) = split(/\t/,$tmp1);
	$inposttemp = $post1;
	$inposttemp =~ s/<(.|\n)*>//g;

        $inposttemp = &lbhz($inposttemp,$maxsavepost);
        $file = "$lbdir" . "boarddata/list$id.cgi";
        &winlock($file);
        open (LIST, "$file");
        flock (LIST, 1) if ($OS_USED eq "Unix");
        @listall=<LIST>;
        close (LIST);
	$listall = @listall;

    if ($listall >= 200) {
        if (open (LIST, ">$file")) {
        flock (LIST, 2) if ($OS_USED eq "Unix");
        print LIST "$threadname\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t$inposticon\t$inposttemp\t\n";
        foreach (@listall) {
            ($listone,my $noneed) = split(/\t/,$_);
	    $_ =~ s/[\n\r]//isg;
            print LIST "$_\n" if (($listone ne $threadname)&&($listone ne "")&&($listone =~ /^[0-9]+$/));
        }
        close (LIST);
        }
        &winunlock($file);
    }
    else {
        &winunlock($file);
        rebuildLIST(-Forum=>"$inforum");
    }
$inforum=$id;
&mischeader("ĞÂÍ¶Æ±³É¹¦");
$output .= qq~
	<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
	<tr><td>
	<table cellpadding=6 cellspacing=1 border=0 width=100%>
	<tr><td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>Ğ»Ğ»£¡Äú²ÎÓëÍ¶Æ±³É¹¦£¡</b></font></td></tr>
	<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
	Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡
	<ul>
	<li><a href="$threadprog?forum=$id&topic=$threadname">·µ»Ø´ËÍ¶Æ±Ìù</a>
	<li><a href="$forumsprog?forum=$id">·µ»ØÂÛÌ³</a>
	<li><a href="$forumsummaryprog">·µ»ØÂÛÌ³Ê×Ò³</a>
	</ul>
	</td></tr>
	</table></td></tr></table>
	<meta http-equiv="refresh" content="3; url=$threadprog?forum=$id&topic=$threadname">
~;
}
