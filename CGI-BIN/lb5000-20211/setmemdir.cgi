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
require "data/cityinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setmemdir.cgi";

$query = new LBCGI;

$action              = $query -> param('action');
$oldmembersdir       = $query -> param('oldmembersdir');
$membersdir          = $query -> param('membersdir');

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);
&admintitle;

&getmember("$inmembername");


if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

    if ($action eq "process") {
	if (($membersdir !~ /^[0-9a-zA-Z]+$/)||($membersdir eq "")||(length($membersdir) < 8)||(length($membersdir) > 16)) {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                    <b>��ӭ������̳�������� / �û���ϢĿ¼����</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=���� color=#333333><b>�û���ϢĿ¼���ӵĲ��ֱ���ȫΪ���ֺ���ĸ��ɣ����ҳ���Ϊ 8-16 λ��</b>
                    </td></tr></table></td></tr></table>
                    </td></tr></table></body></html>~;
					exit;
	}

opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
my @backupdir = grep(/^backup/i, @files2);
$backupdir = $backupdir[0];

        $filetomake = "$lbdir" . "members$membersdir";
	rename("${lbdir}members$oldmembersdir","${lbdir}members$membersdir") if ($membersdir ne $oldmembersdir);
	rename("${lbdir}$backupdir","${lbdir}backup$membersdir") if ($backupdir ne "backup$membersdir");
	rename("${lbdir}$msgdir","${lbdir}messages$membersdir") if ($msgdir ne "messages$membersdir");

        if (-e $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �û���ϢĿ¼����</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ��ɹ�����</b><br>Ŀǰ�û���Ŀ¼Ϊ members$membersdir ��<br>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ��ɹ�����</b><br>Ŀǰ�û��ⱸ��Ŀ¼Ϊ backup$membersdir ��<br>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ��ɹ�����</b><br>Ŀǰ����ϢĿ¼Ϊ messages$membersdir ��<br>
                </center></td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                    <b>��ӭ������̳�������� / �û���ϢĿ¼����</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=���� color=#333333><b>������Ϣû�б���</b><br>cgi-bin Ŀ¼����д<br>
                    </td></tr></table></td></tr></table>
                    ~;
                    }
            }
            else {
		opendir (DIRS, "$lbdir");
		@files2 = readdir(DIRS);
		closedir (DIRS);
		@memdir = grep(/^members/, @files2);
		$memdir=@memdir;
		if ($memdir eq 0) {
			@memdir = grep(/^MEMBERS/, @files2);
			rename("${lbdir}MEMBERS","${lbdir}members");
		}
		$membersdir = $memdir[0];
		$membersdir =~ s/members//i;
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �û���ϢĿ¼����</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�û���ϢĿ¼����</b>
                </td></tr>

                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
		<input type=hidden name="oldmembersdir" value="$membersdir">
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=���� color=#333333><b>��ǰ�û���Ŀ¼</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                members$membersdir</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=���� color=#333333><b>��ǰ���ݿ�Ŀ¼</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                backup$membersdir</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=���� color=#333333><b>��ǰ����ϢĿ¼</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                messages$membersdir</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=���� color=#333333></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=16 name="membersdir" value="$membersdir" maxlength=16> ���������� 8-16 ��������ֺ���ĸ</td>
                </tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
                ~;

                }
            }
            else {
                 &adminlogin;
                 }

print qq~</td></tr></table></body></html>~;
exit;
