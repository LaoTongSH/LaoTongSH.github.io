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
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
require "visitforum.lib.pl";

$|++;                                    # Unbuffer the output

print header(-charset=>gb2312);

$thisprog = "massmsg.cgi";

$query = new LBCGI;

$inmsgtitle       = $query -> param('msgtitle');
$inmessage        = $query -> param('message');
$action           = $query -> param('action');

$insendto        = $query -> param('sendto');

$inmessage           = &cleaninput($inmessage);
$inmsgtitle          = &cleaninput($inmsgtitle);



$inmembername = $query->cookie('adminname');
$inpassword   = $query->cookie('adminpass');

&getmember("$inmembername");

&admintitle;

if (($membercode ne "ad") || ($inpassword ne $password) || (lc($inmembername) ne lc($membername))) {
	&adminlogin;
	exit;
}

if ($action ne "send") {
	$output .= qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 短消息广播</b>
		</td></tr><tr><td><BR>
		<B>注意：请尽量不要使用此项功能，此功能及其消耗系统资源，而且会使用户反感。</b>
		</td></tr><tr><td>
		<FORM METHOD="post" ACTION="$thisprog">
		<INPUT TYPE="HIDDEN" NAME="action" VALUE="send"><BR>
		<TABLE BORDER="0">
		<TR VALIGN="TOP">
		<TD>短消息标题： </td>
		<TD><INPUT TYPE="TEXT" SIZE="20" NAME="msgtitle"></TD>
		<TR VALIGN="TOP">
		<TD>接受方选择： </td>
		<TD>
	        <select name="sendto" size="1">
        	  <option value="online">所有在线用户 </option>
        	  <option value="mo"    >所有管理员 </option>
        	  <option value="all"   >所有注册用户 </option>
        	</select>
        	</td>
		</tr>
		<TR VALIGN="TOP">
		<TD>短消息内容： </td>
		<TD>
		<TEXTAREA NAME="message" COLS="50" ROWS="8"></textarea><BR><BR>
		<center>
		<INPUT TYPE="SUBMIT" NAME="Submit" VALUE="发 送">
		</td>
		</tr>
		</table>
		</form>
	~;
}
else {
	if ($inmsgtitle eq "") { $blanks = "yes"; }
	if ($inmessage eq "")  { $blanks = "yes"; }
	if ($blanks eq "yes")  {
		&messangererror("短消息广播&请把标题和内容填写完整。");
	}
	
	$currenttime = time;
	if ($insendto eq "all") {
	    open (MEMFILE, "${lbdir}data/lbmember.cgi");
	    flock (MEMFILE, 1) if ($OS_USED eq "Unix");
	    @cgi = <MEMFILE>;
	    close(MEMFILE);
	}
	elsif ($insendto eq "mo") {
	    open (MEMFILE, "${lbdir}data/lbmember.cgi");
	    flock (MEMFILE, 1) if ($OS_USED eq "Unix");
	    @cgi1 = <MEMFILE>;
	    close(MEMFILE);
	    foreach (@cgi1) {
	    	chomp $_;
		($membername,$membercode,$no) = split(/\t/,$_);
	    	push (@cgi, $_) if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"));
	    }
	}
	else {
	    $filetoopen = "$lbdir" . "data/onlinedata.cgi";
	    &winlock($filetoopen);
	    open(FILE,"$filetoopen");
	    flock (FILE, 2) if ($OS_USED eq "Unix");
	    @cgi1 = <FILE>;
	    close(FILE);
	    &winunlock($filetoopen);
	    undef @cgi;
	    foreach (@cgi1) {
	    	chomp $_;
		($membername,$no) = split(/\t/,$_);
	    	push (@cgi, $_) if ($membername !~ /^客人/);
	    }
	}
	$totlemembers = @cgi;

	$inmessage1 = "<BR><BR>---------------------------<BR>LB5000 由雷傲工作室荣誉出品<BR>主页:http://www.LeoBoard.com";
	foreach $thisMember (@cgi) {
		($thisMember,$no) = split(/\t/,$thisMember);
	        $thisMember =~ s/ /\_/isg;
		$thisMember =~ tr/A-Z/a-z/;

		$filetoopen = "$lbdir". "$msgdir/in/$thisMember" . "_msg.cgi";
		$filetoopen = &stripMETA($filetoopen);

		open (FILE, "$filetoopen");
		@inboxmessages = <FILE>;
		close (FILE);

		open (FILE, ">$filetoopen");
		flock (FILE, 2);
		print FILE "系统短消息广播\tno\t$currenttime\t$inmsgtitle\t$inmessage$inmessage1\n";
		
		foreach $line (@inboxmessages) {
			chomp $line;
			print FILE "$line\n";
		}
		close (FILE);
	}	

	$output .= qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 短消息广播</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#333333><center><b>短消息广播发送完成，共发出$totlemembers个消息！</b></center><br><br>

	~;
}

print $output;
print qq~</td></tr></table></body></html>~;

1;
