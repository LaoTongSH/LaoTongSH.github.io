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
#            http://maildo.com/      ���һ����
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
		<b>��ӭ������̳�������� / ����Ϣ�㲥</b>
		</td></tr><tr><td><BR>
		<B>ע�⣺�뾡����Ҫʹ�ô���ܣ��˹��ܼ�������ϵͳ��Դ�����һ�ʹ�û����С�</b>
		</td></tr><tr><td>
		<FORM METHOD="post" ACTION="$thisprog">
		<INPUT TYPE="HIDDEN" NAME="action" VALUE="send"><BR>
		<TABLE BORDER="0">
		<TR VALIGN="TOP">
		<TD>����Ϣ���⣺ </td>
		<TD><INPUT TYPE="TEXT" SIZE="20" NAME="msgtitle"></TD>
		<TR VALIGN="TOP">
		<TD>���ܷ�ѡ�� </td>
		<TD>
	        <select name="sendto" size="1">
        	  <option value="online">���������û� </option>
        	  <option value="mo"    >���й���Ա </option>
        	  <option value="all"   >����ע���û� </option>
        	</select>
        	</td>
		</tr>
		<TR VALIGN="TOP">
		<TD>����Ϣ���ݣ� </td>
		<TD>
		<TEXTAREA NAME="message" COLS="50" ROWS="8"></textarea><BR><BR>
		<center>
		<INPUT TYPE="SUBMIT" NAME="Submit" VALUE="�� ��">
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
		&messangererror("����Ϣ�㲥&��ѱ����������д������");
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
	    	push (@cgi, $_) if ($membername !~ /^����/);
	    }
	}
	$totlemembers = @cgi;

	$inmessage1 = "<BR><BR>---------------------------<BR>LB5000 ���װ�������������Ʒ<BR>��ҳ:http://www.LeoBoard.com";
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
		print FILE "ϵͳ����Ϣ�㲥\tno\t$currenttime\t$inmsgtitle\t$inmessage$inmessage1\n";
		
		foreach $line (@inboxmessages) {
			chomp $line;
			print FILE "$line\n";
		}
		close (FILE);
	}	

	$output .= qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ����Ϣ�㲥</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#333333><center><b>����Ϣ�㲥������ɣ�������$totlemembers����Ϣ��</b></center><br><br>

	~;
}

print $output;
print qq~</td></tr></table></body></html>~;

1;