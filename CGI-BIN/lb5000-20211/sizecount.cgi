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
use File::Find;
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
$thisprog = "sizecount.cgi";

$query = new LBCGI;

$nextforum     = $query -> param('nextforum');
$action        = $query -> param("action");
$action        = &cleaninput("$action");
$nextforum=0 if ($nextforum eq "");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;


if ($action eq "process") {#1
    &getmember("$inmembername");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { #2
  		$tsize = 0;
                find(\&countsize,$lbdir);
                $lbsd = 'Bytes';
                $cgisize = $progsize = $osize = $tsize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

            print qq~
                <tr><td bgcolor="#333333" colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 统计论坛占用空间</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<br><br><br>
		<table width=85% align=center cellspacing=0 cellpadding=0 border=0>
		<tr><td><B><font color=blue>cgi-bin 占用空间：</B></td><td><b><font color=blue>&nbsp;$tsize $lbsd</b></td><td><b><font color=blue>($osize 字节)</b></td></tr>
		~;
				$tsize = 0;
		find(\&countsize,"${lbdir}$memdir");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 用户库占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
				$tsize = 0;

opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
my @backupdir = grep(/^backup/, @files2);
$backupdir=@backupdir;
if ($backupdir eq 0) {
	@backupdir = grep(/^BACKUP/, @files2);
	rename("${lbdir}BACKUP","${lbdir}backup");
}
if ($backupdir eq 0) {
	@backupdir = grep(/^Backup/, @files2);
	rename("${lbdir}Backup","${lbdir}backup");
}
$backupdir = $backupdir[0];

		find(\&countsize,"${lbdir}$backupdir");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 备份文件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
				$tsize = 0;
		find(\&countsize,"${lbdir}data");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 数据文件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
				$tsize = 0;
		find(\&countsize,"${lbdir}help");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 帮助文件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
				$tsize = 0;
		find(\&countsize,"${lbdir}memfav");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 用户个人收藏占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
				$tsize = 0;
		find(\&countsize,"${lbdir}boarddata");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 论坛重要数据目录占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
				$tsize = 0;
		find(\&countsize,"${lbdir}lock");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 论坛锁定文件目录占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
				$tsize = 0;

		find(\&countsize,"${lbdir}memfriend");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 用户好友列表占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

		$tsize = 0;
		find(\&countsize,"${lbdir}$msgdir");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 用户短消息占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

		$tsize = 0;
		find(\&countsize,"${lbdir}search");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $progsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 搜索记录占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

		open(FILE,"<${lbdir}data/allforums.cgi");
		@forumslist = <FILE>;
		close(FILE);
		chomp @forumslist;
		foreach(@forumslist) {
			($forumid,$typename,$no,$forumname) = split(/\t/);
			$forumtypes{$typename}->{$forumid} = $forumname;
		}
		$output = '';
		while(($typename,$pointer) = each %forumtypes) {
			while(($forumid,$forumname) = each %$pointer) {
				$path = "${lbdir}forum$forumid";
				$tsize = 0;
				find(\&countsize,$path);
				$lbsd = 'Bytes';
                		$osize = $tsize;
		                if($tsize > 1024) {
		                	$tsize /= 1024;
		                	$lbsd = 'KB';
		                }
		                if($tsize > 1024) {
		                	$tsize /= 1024;
		                	$lbsd = 'MB';
		                }
		                if($tsize > 1024) {
		                	$tsize /= 1024;
		                	$lbsd = 'GB';
		                }
		                $tsize = sprintf("%6.2f",$tsize);
		                $tsize =~ s/\s//g;

				$forumsizes{$forumid} = "$forumname\t&nbsp;$tsize $lbsd\t$osize";
			}
		}
		$forumsize = 0;
		while(($typename,$pointer) = each %forumtypes) {
			@forumids = keys %$pointer;
			$tsize = 0;
			foreach(@forumsizes{@forumids}) {
				($no,$no,$size) = split(/\t/);
				$tsize += $size;
			}
			$lbsd = 'Bytes';
               		$osize = $tsize;
               		$forumsize += $tsize;
	                if($tsize > 1024) {
	                	$tsize /= 1024;
	                	$lbsd = 'KB';
	                }
	                if($tsize > 1024) {
	                	$tsize /= 1024;
	                	$lbsd = 'MB';
	                }
	                if($tsize > 1024) {
	                	$tsize /= 1024;
	                	$lbsd = 'GB';
	                }
	                $tsize = sprintf("%6.2f",$tsize);
	                $tsize =~ s/\s//g;

	                $output .= "<tr><td>||- <font color=blue>$typename</td><td><font color=blue>&nbsp;$tsize $lbsd</td><td><font color=blue>($osize 字节)</td></tr>\n";
	                foreach(@forumsizes{@forumids}) {
	                	($forumname,$showsize,$osize) = split(/\t/);
	                	$output .= "<tr><td>|||- $forumname</td><td>$showsize</td><Td>($osize 字节)</td><tr>\n";
	                }
	        }
	        $osize = $tsize = $forumsize;
                $progsize -= $osize;
	        $lbsd = 'Bytes';
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;
	        print "<tr><td>|- <B>论坛帖子占用空间：</B></td><td><B>&nbsp;$tsize $lbsd</B></td><td><B>($osize 字节)</B></td></tr>\n";
	        print $output;

	        $osize = $tsize = $progsize;
	        $lbsd = 'Bytes';
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;
	        print "<tr><td>|- 程序文件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";


		$tsize = 0;
                find(\&countsize,$imagesdir);
                $lbsd = 'Bytes';
                $nonsize = $osize = $tsize;
                $allsize = $cgisize + $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr height=20><td colspan=3>&nbsp;</td></tr>\n";
		print "<tr><td><font color=blue><b>non-cgi 占用空间：</b></td><td><font color=blue><b>&nbsp;$tsize $lbsd</b></td><td><font color=blue><b>($osize 字节)</b></td></tr>\n";

		$tsize = 0;
                find(\&countsize,"${imagesdir}usr");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $nonsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 帖子附件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

		$tsize = 0;
                find(\&countsize,"${imagesdir}usravatars");
                $lbsd = 'Bytes';
                $osize = $tsize;
                $nonsize -= $osize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 用户上传头像占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";

		$osize = $tsize = $nonsize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td>|- 其他文件占用空间：</td><td>&nbsp;$tsize $lbsd</td><td>($osize 字节)</td></tr>\n";
		print "<tr height=50><td colspan=3>&nbsp;</td></tr>\n";

		$osize = $tsize = $allsize;
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'KB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'MB';
                }
                if($tsize > 1024) {
                	$tsize /= 1024;
                	$lbsd = 'GB';
                }
                $tsize = sprintf("%6.2f",$tsize);
                $tsize =~ s/\s//g;

		print "<tr><td><font color=red><b>论坛占用总空间：</b></td><td><font color=red><b>&nbsp;$tsize $lbsd</b></td><td><font color=red><b>($osize 字节)</b></td></tr>\n";


		print qq~
		</table>
		</td></tr>
		~;
	}
      else {
         &adminlogin;
      }
} else {
        &getmember("$inmembername");
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 统计论坛占用空间</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>统计论坛占用空间</b>
		</td></tr>
		<form action="$thisprog" method="post">
		<input type=hidden name="action" value="process">
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#000000>
		<b>请注意:</b><br>此过程将耗费大量CPU时间和系统资源，请尽量少用本功能！
		</td>
		</tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<input type=submit name=submit value=提交></td></form></tr></table></td></tr></table>
		);
	}
        else {
		&adminlogin;
	}
}
print qq~</td></tr></table></body></html>~;
exit;
sub countsize {
	$tsize += -s $File::Find::name;
}
