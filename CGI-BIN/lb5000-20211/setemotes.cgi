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
$thisprog = "setemotes.cgi";

$query = new LBCGI;

$wordarray     = $query -> param('wordarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);

&admintitle;
            

if ($action eq "process") {
 
    &getmember("$inmembername");
        
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
 

	$wordarray =~ s/[\f\n\r]+/\n/ig;
	$wordarray =~ s/[\r \n]+$/\n/ig;
	$wordarray =~ s/^[\r\n ]+/\n/ig;
        $wordarray =~ s/\n\n//ig;
        $wordarray =~ s/\n/\&/ig;

        @savedwordarray = split(/\&/,$wordarray);
        
        $filetomake = "$lbdir" . "data/emote.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / EMOTE 设定</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>所有信息已经被成功保存。</b></center><br><br>
                <b>下列EMOTE被保存！</b><br><br>
                );
                
                foreach (@savedwordarray) {
                    chomp $_;
                    ($toemote, $beemote) = split(/\=/,$_);
                    print qq(所有出现 <b>$toemote</b> 的地方将被 <b>$beemote</b> 替换。<br>);
                }
                print qq(
                <br><br><br><center><a href="setemotes.cgi">再次增加EMOTE列表</a></center>);
        }
        else {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / EMOTE 设定</b>
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
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "data/emote.cgi";
                open (FILE, "$filetoopen");
                $emote = <FILE> if (!$emote);
                close (FILE);
                
                $emote =~ s/\&/\n/g;
        	$emote =~ s/\n\n/\n/ig;
        	$emote =~ s/\f\r//ig;

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / EMOTE 设定</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>EMOTE设定</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=宋体 color=#000000>
                EMOTE设定可以实现类似聊天室的EMOTE转换,使您的论坛更加丰富多彩.<br>
                <br>
                <b>使用方法：</b><br>1.输入一个要转换的EMOTE和转换后的动作，并在中间加上 "=" (等于号)。<BR>
                2.每一个要转换的EMOTE前面最好加上/// ，以区别与其他词汇。而转换后的动作中，“对象”将在发贴时转换成为发贴人的姓名，也可以不含“对象”，这样将完全不变的显示您在这里所设定以后的动作。<BR>
                <b>注意：<br>1.每行只能写一个！<br>
                2.设置要转换的EMOTE动作,可以是中文，英文，或者数字，最好不要含有半角状态下的标点符号，以免引起程序运行的错误。
                <br>3.设置的EMOTE不要重复，例如///hi和///hide是不被允许的，在转换时///hide将先转化为///hi的动作，然后在动作后面附上de。
                比如说，设置///hi=对象说到“大家好。”那么///hide将会显示：对象说到“大家好。”de。而///hi和///sohi则是允许的。</b><br><br>
                <b>例如：</b>///bug=对象把嘴一咧，说到：“我是害虫，我怕谁？”<br>
                如果发贴人是"傲寒九天"则这句话在查看贴子时将显示:<br>
                〖傲寒九天〗把嘴一咧，说到：“我是害虫，我怕谁？”<br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=60 rows=15 wrap="virtual" name="wordarray">$emote</textarea>
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
