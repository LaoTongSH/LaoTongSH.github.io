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
$thisprog = "setbadwords.cgi";

$query = new LBCGI;

&ipbanned; #封杀一些 ip

$wordarray     = $query -> param('wordarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {
 
    &getmember("$inmembername");
        
    if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
 
 	$wordarray =~ s/[\f\n\r]+/\n/ig;
	$wordarray =~ s/[\r \n]+$/\n/ig;
	$wordarray =~ s/^[\r\n ]+/\n/ig;
        $wordarray =~ s/\n\n//g;
        $wordarray =~ s/\n/\&/g;

        @savedwordarray = split(/\&/,$wordarray);
        
        $filetomake = "$lbdir" . "data/badwords.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>所有信息已经被成功保存。</b></center><br><br>
                <b>下列“不良词语”被保存！</b><br><br>
                );
                
                foreach (@savedwordarray) {
                    chomp $_;
                    ($bad, $good) = split(/\=/,$_);
                    print qq(所有出现 <b>$bad</b> 的地方将被 <b>$good</b> 替换。<br>);
                }
                print qq(
                <br><br><br><center><a href="setbadwords.cgi">再次增加过滤的不良词语</a></center>);
        }
        else {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>Welcome your lb board Administration Center</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>信息没有被保存！</b><br>文件或者目录不可写。
                </td></tr></table></td></tr></table>
                );
        }
    }
    else {
        &adminlogin;
    }
        
 }
        
 else {
        
        &getmember("$inmembername");
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
                # Open the badword file

                $filetoopen = "$lbdir" . "data/badwords.cgi";
                open (FILE, "$filetoopen") or $badwords = "damn=d*amn\nhell=h*ll";
                $badwords = <FILE> if (!$badwords);
                close (FILE);
                
                $badwords =~ s/\&/\n/g;
        	$badwords =~ s/\n\n/\n/ig;
        	$badwords =~ s/\\//ig;
        	$emote =~ s/\f\r//ig;

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 不良词语过滤</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>不良词语过滤</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=宋体 color=#000000>
                不良词语过滤可以阻止一些不好的字眼出现在论坛中。你可以选择过滤的单词，和过滤后的单词。<br>
                这样，不良词语在<b>发表文章</b>时，或在用户查看、引用时，都不会被显示。<br>
                这意味着不良词语过滤是永久性的。当你增加一个新的过滤时，所有的文章都会被过滤交换。<br><br>
                <b>使用方法：</b>使用方法：</b>输入一个要过滤的词语和过滤后的词语，并在中间加上 "=" (等于号)。<BR><br>
                <b>注意1，每行只能写一个！</b><br><br>
                <b>注意2，尽量避免使用 * ( ) 符号！</b><br><br>
                <b>例如：</b>fuck=f**k<br><br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=60 rows=6 wrap="virtual" name="wordarray">$badwords</textarea>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <input type=submit name=submit value="提 交"></form></td></tr></table></td></tr></table>
                );
                
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
