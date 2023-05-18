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
                    <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 用户信息目录设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=宋体 color=#333333><b>用户信息目录增加的部分必须全为数字和字母组成，并且长度为 8-16 位！</b>
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
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 用户信息目录设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>以下信息已经成功保存</b><br>目前用户库目录为 members$membersdir 。<br>
                <font face=宋体 color=#333333><center><b>以下信息已经成功保存</b><br>目前用户库备份目录为 backup$membersdir 。<br>
                <font face=宋体 color=#333333><center><b>以下信息已经成功保存</b><br>目前短消息目录为 messages$membersdir 。<br>
                </center></td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 用户信息目录设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=宋体 color=#333333><b>所有信息没有保存</b><br>cgi-bin 目录不可写<br>
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
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 用户信息目录设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>用户信息目录设置</b>
                </td></tr>

                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
		<input type=hidden name="oldmembersdir" value="$membersdir">
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=宋体 color=#333333><b>当前用户库目录</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                members$membersdir</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=宋体 color=#333333><b>当前备份库目录</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                backup$membersdir</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=宋体 color=#333333><b>当前短消息目录</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                messages$membersdir</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=宋体 color=#333333></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=16 name="membersdir" value="$membersdir" maxlength=16> 请任意输入 8-16 个随机数字和字母</td>
                </tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
                ~;

                }
            }
            else {
                 &adminlogin;
                 }

print qq~</td></tr></table></body></html>~;
exit;
