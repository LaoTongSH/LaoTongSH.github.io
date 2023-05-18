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
$thisprog = "lookstyles.cgi";

    $query = new LBCGI;
&ipbanned; #封杀一些 ip

	@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }



$action      =  $PARAM{'action'};
$inforum     =  $PARAM{'forum'};
$inmembername        = $query -> param("membername");
$inpassword          = $query -> param("password");
$action              = &cleaninput("$action");
$inmembername        = &cleaninput("$inmembername");
$inpassword          = &cleaninput("$inpassword");
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

    if ($inmembername eq "") { $inmembername = "客人"; }
    else {
    &getmember("$inmembername");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
        }   

&mischeader("本版配色列表");

print header(-charset=>gb2312);
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));
&styleform;                
##################################################################################
sub styleform {
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
&error("本版配色&对不起，本版块不允许查看配色！") if ($look eq "off");
&title;
if ($privateforum ne "yes") {
    	&whosonline("$inmembername\t$forumname\tnone\t查看论坛$forumname的配色\t");
    }
    else {
	&whosonline("$inmembername\t$forumname(密)\tnone\t查看保密论坛$forumname的配色\t");
    }

$output .= qq~

         <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
             <tr>
               <td width=30% rowspan=2 valign=top>$forumgraphic
               </td>
               <td valign=top>
        <img src=$imagesurl/images/closedfold.gif width=15 height=11>　<a href=$forumsummaryprog>$boardname</a><br>
       <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/closedfold.gif width=15 height=11>　<a href=forums.cgi?forum=$inforum>$forumname</a><br>
          　 <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>　查看$forumname的配色
      </td></tr></table>
        <table width=97% align=center><br>
        
                
              
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛BODY标签</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>控制整个论坛风格的背景颜色或者背景图片等</font></td>
                <td bgcolor=#FFFFFF>
                $lbbody</td>
                </tr>
                              
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛页首菜单</b>
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>页首背景颜色 (菜单带上方)</font></td>
                <td bgcolor=$titleback  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titleback</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>页首字体颜色 (菜单带上方)</font></td>
                <td bgcolor=$titlefont  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titlefont</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>页首边界颜色 (菜单带上方)</font></td>
                <td bgcolor=$titleborder  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titleborder</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带字体颜色</font></td>
                <td bgcolor=$menufontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $menufontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带背景颜色</font></td>
                <td bgcolor=$menubackground  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $menubackground</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>字体外观和颜色</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"最后发贴者"字体颜色</font></td>
                <td bgcolor=$lastpostfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $lastpostfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"加重区"字体颜色</font></td>
                <td bgcolor=$fonthighlight  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $fonthighlight</td>
                </tr>
                
                                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>一般用户名称字体颜色</font></td>
                <td bgcolor=$posternamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $posternamecolor</td>
                </tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>一般用户名称上的光晕颜色</font></td>
		<td bgcolor=$memglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$memglow</td>
		</tr>
               
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>坛主名称字体颜色</font></td>
                <td bgcolor=$adminnamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $adminnamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>坛主名称上的光晕颜色</font></td>
		<td bgcolor=$adminglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$adminglow</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>总版主名称字体颜色</font></td>
                <td bgcolor=$smonamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $smonamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>总版主名称上的光晕颜色</font></td>
		<td bgcolor=$smoglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$smoglow</td>
		</tr>                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>版主名称字体颜色</font></td>
                <td bgcolor=$teamnamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $teamnamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>版主名称上的光晕颜色</font></td>
		<td bgcolor=$teamglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$teamglow</td>
		</tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>过滤和禁言用户名称上的光晕颜色</font></td>
		<td bgcolor=$banglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$banglow</td>
		</tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>所有页面颜色</center></b><br>
                <font color=#333333>这些颜色配置将用于每个页面。用于注册、登陆、在线以及其他页面。
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>主字体颜色</font></td>
                <td bgcolor=$fontcolormisc  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $fontcolormisc</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色一</font></td>
                <td bgcolor=$miscbackone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $miscbackone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色二</font></td>
                <td bgcolor=$miscbacktwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $miscbacktwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>表格颜色</center></b><br>
                <font color=#333333>这些颜色大部分用于lbboard.cgi，forums.cgi和topic.cgi
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带背景颜色</font></td>
                <td bgcolor=$catback  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $catback</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带字体颜色</font></td>
                <td bgcolor=$catfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $catfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>所有表格边界颜色</font></td>
                <td bgcolor=$tablebordercolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $tablebordercolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>所有表格宽度</font></td>
                <td bgcolor=#FFFFFF>
                $tablewidth</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>标题颜色</center></b><br>
                <font color=#333333>这里颜色配置用于发表第一个主题的标题
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>论坛/主题的标题栏背景颜色</font></td>
                <td bgcolor=$titlecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titlecolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>论坛/主题的标题栏字体颜色</font></td>
                <td bgcolor=$titlefontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titlefontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>论坛内容颜色</center></b><br>
                <font color=#333333>查看论坛内容时颜色 (forums.cgi)
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容颜色一</font></td>
                <td bgcolor=$forumcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $forumcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容颜色二</font></td>
                <td bgcolor=$forumcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $forumcolortwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容字体颜色</font></td>
                <td bgcolor=$forumfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $forumfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>回复颜色</center></b><br>
                <font color=#333333>回复贴子颜色(topic.cgi)
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复颜色一</font></td>
                <td bgcolor=$postcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $postcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复颜色二</font></td>
                <td bgcolor=$postcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $postcolortwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色一</font></td>
                <td bgcolor=$postfontcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $postfontcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色二</font></td>
                <td bgcolor=$postfontcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $postfontcolortwo</td>
                </tr>
               
              
                ~;             

}






$output .= qq~</td></tr></table><br><br></body></html>~;
&output(
     -Title   => "查看$forumname的配色", 
     -ToPrint => $output, 
     -Version => $versionnumber 
    );
exit;

