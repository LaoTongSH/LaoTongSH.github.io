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
$thisprog = "setstyles.cgi";

$query = new LBCGI;
&ipbanned; #封杀一些 ip

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam =~ s/'//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
        	$_ =~ s/[\n\r]//isg;
        	$theparam =~ s/[\n\r]//isg;
            $printme .= "\$" . "$_ = \'$theparam\'\;\n" if ($_ ne "");
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);
&admintitle;

&getmember("$inmembername");

if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

    if ($action eq "delstyle") {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>警告！！</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>完全删除此分论坛的所有自定义风格，不可恢复<p>
        <p>
        >> <a href="$thisprog?action=delstyleok&forum=$forum">开始删除</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
    }
    elsif ($action eq "delstyleok") {
        $filetomake = "$lbdir" . "data/style$forum.cgi";
    	unlink $filetomake;
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 分论坛风格删除</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>所有信息已经保存</b><br>此分论坛的风格已经完全删除。
                    </td></tr></table></td></tr></table>
                    ~;

    }
    elsif ($action eq "process") {


        $printme .= "1\;\n";

        $filetomake = "$lbdir" . "data/styles.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 风格设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE colspan=2>
                <font color=#333333><center><b>以下的信息全部成功保存</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/1\;//g;
                print $printme;

                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }

                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 风格设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>所有信息没有保存</b><br>文件或者目录不可写，请设置属性为 777 ！
                    </td></tr></table></td></tr></table>
                    ~;
                    }

            }
            else {
                if ($action ne ""){
                $stylefile = "$lbdir" . "data/skin/$action.cgi";
                if (-e $stylefile) {
         	require $stylefile;
                }
                }

        $dirtoopen = "$lbdir" . "data/skin";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);
        my $myskin="";
        @thd = grep(/\.cgi$/,@dirdata);
        $topiccount = @thd;
        @thd=sort @thd;
        for (my $i=0;$i<$topiccount;$i++){
       	$thd[$i]=~s /\.cgi//isg;
        $myskin.=qq~<option value="$thd[$i]">风格 [ $thd[$i] ]~;
        }
        $myskin =~ s/value=\"$action\"/value=\"$action\" selected/;
                $inmembername =~ s/\_/ /g;

                print qq~
                <tr><td bgcolor=#333333" colspan=3><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 风格设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#333333><b>设定风格</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>系统自带的风格</b><br>你选择后，需要正式确认提交才生效</font></td>
                <td bgcolor=#FFFFFF>
                <form action="$thisprog" method="post">
                <select name="action">
                <option value="">默认风格$myskin
                </select>
                <input type=submit value="运 用">
                </form>
                </td></tr>

                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛BODY标签</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>控制整个论坛风格的背景颜色或者背景图片等</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>默认：bgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛页首菜单</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带字体颜色</font></td>
                <td bgcolor=$menufontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menufontcolor" value="$menufontcolor" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带背景颜色</font></td>
                <td bgcolor=$menubackground  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackground" value="$menubackground" size=7 maxlength=7>　默认：#DDDDDD</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带背景图片</font></td>
                <td background=$imagesurl/images/$menubackpic  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackpic" value="$menubackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>菜单带边界颜色</font></td>
                <td bgcolor=$titleborder  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titleborder" value="$titleborder" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>字体外观和颜色</b>
                </font></td>
                </tr>


                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>主字体外观</font></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"font\">\n<option value=\"宋体\">宋体\n<option value=\"仿宋\">仿宋\n<option value=\"楷体\">楷体\n<option value=\"黑体\">黑体\n<option value=\"隶书\">隶书\n<option value=\"幼圆\">幼圆\n</select><p>\n";
                $tempoutput =~ s/value=\"$font\"/value=\"$font\" selected/;
                print qq~
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"最后发贴者"字体颜色</font></td>
                <td bgcolor=$lastpostfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lastpostfontcolor" value="$lastpostfontcolor" size=7 maxlength=7>　默认：#000000</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"加重区"字体颜色</font></td>
                <td bgcolor=$fonthighlight  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fonthighlight" value="$fonthighlight" size=7 maxlength=7>　默认：#990000</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>查看时发表者名称字体</font></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"posternamefont\">\n<option value=\"宋体\">宋体\n<option value=\"仿宋\">仿宋\n<option value=\"楷体\">楷体\n<option value=\"黑体\">黑体\n<option value=\"隶书\">隶书\n<option value=\"幼圆\">幼圆\n</select><p>\n";
                $tempoutput =~ s/value=\"$posternamefont\"/value=\"$posternamefont\" selected/;
                print qq~
                $tempoutput</td>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>一般用户名称字体颜色</font></td>
                <td bgcolor=$posternamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="posternamecolor" value="$posternamecolor" size=7 maxlength=7>　默认：#000066</td>
                </tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>一般用户名称上的光晕颜色</font></td>
		<td bgcolor=$memglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="memglow" value="$memglow" size=7 maxlength=7>　默认：#9898BA</td>
		</tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>坛主名称字体颜色</font></td>
                <td bgcolor=$adminnamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="adminnamecolor" value="$adminnamecolor" size=7 maxlength=7>　默认：#990000</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>坛主名称上的光晕颜色</font></td>
		<td bgcolor=$adminglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="adminglow" value="$adminglow" size=7 maxlength=7>　默认：#9898BA</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>总版主名称字体颜色</font></td>
                <td bgcolor=$smonamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="smonamecolor" value="$smonamecolor" size=7 maxlength=7>　默认：#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>总版主名称上的光晕颜色</font></td>
		<td bgcolor=$smoglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="smoglow" value="$smoglow" size=7 maxlength=7>　默认：#9898BA</td>
		</tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>版主名称字体颜色</font></td>
                <td bgcolor=$teamnamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="teamnamecolor" value="$teamnamecolor" size=7 maxlength=7>　默认：#0000ff</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>版主名称上的光晕颜色</font></td>
		<td bgcolor=$teamglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="teamglow" value="$teamglow" size=7 maxlength=7>　默认：#9898BA</td>
		</tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>过滤和禁言用户名称上的光晕颜色</font></td>
		<td bgcolor=$banglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="banglow" value="$banglow" size=7 maxlength=7>　默认：none</td>
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
                <input type=text name="fontcolormisc" value="$fontcolormisc" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色一</font></td>
                <td bgcolor=$miscbackone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbackone" value="$miscbackone" size=7 maxlength=7>　默认：#FFFFFF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色二</font></td>
                <td bgcolor=$miscbacktwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbacktwo" value="$miscbacktwo" size=7 maxlength=7>　默认：#EEEEEE</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景图片(在线名单)</font></td>
                <td background=$imagesurl/images/$otherbackpic width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="otherbackpic" value="$otherbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景图片(论坛图例)</font></td>
                <td background=$imagesurl/images/$otherbackpic1 width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="otherbackpic1" value="$otherbackpic1"></td>
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
                <input type=text name="catback" value="$catback" size=7 maxlength=7>　默认：#ebebFF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带背景图片</font></td>
                <td background=$imagesurl/images/$catbackpic  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catbackpic" value="$catbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带字体颜色</font></td>
                <td bgcolor=$catfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catfontcolor" value="$catfontcolor" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>所有表格边界颜色</font></td>
                <td bgcolor=$tablebordercolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablebordercolor" value="$tablebordercolor" size=7 maxlength=7>　默认：#000000</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>所有表格宽度</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablewidth" value="$tablewidth" size=5 maxlength=5>　默认：750</td>
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
                <input type=text name="titlecolor" value="$titlecolor" size=7 maxlength=7>　默认：#acbded</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>论坛/主题的标题栏字体颜色</font></td>
                <td bgcolor=$titlefontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titlefontcolor" value="$titlefontcolor" size=7 maxlength=7>　默认：#333333</td>
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
                <input type=text name="forumcolorone" value="$forumcolorone" size=7 maxlength=7>　默认：#f0F3Fa</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容颜色二</font></td>
                <td bgcolor=$forumcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumcolortwo" value="$forumcolortwo" size=7 maxlength=7>　默认：#F2F8FF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容字体颜色</font></td>
                <td bgcolor=$forumfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumfontcolor" value="$forumfontcolor" size=7 maxlength=7>　默认：#333333</td>
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
                <input type=text name="postcolorone" value="$postcolorone" size=7 maxlength=7>　默认：#EFF3F9</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复颜色二</font></td>
                <td bgcolor=$postcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcolortwo" value="$postcolortwo" size=7 maxlength=7>　默认：#F2F4EF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色一</font></td>
                <td bgcolor=$postfontcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolorone" value="$postfontcolorone" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色二</font></td>
                <td bgcolor=$postfontcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolortwo" value="$postfontcolortwo" size=7 maxlength=7>　默认：#555555</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>页面跨度</center></b><br>
                <font color=#333333>每页显示主题的回复数，当一篇主题回复超过一定数量时分页显示 (topic.cgi)
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每页主题数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxthreads" value="$maxthreads" size=3 maxlength=3>　一般为 20 -- 30</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每主题每页的回复数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtopics" value="$maxtopics" size=3 maxlength=3>　一般为 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复数超过多少后就是热门贴？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hottopicmark" value="$hottopicmark" size=3 maxlength=3>　一般为 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>投票数超过多少后就是热门投票贴？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hotpollmark" value="$hotpollmark" size=3 maxlength=3>　一般为 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>LB5000 标签设置</center></b>(坛主和版主不受此限)<br>
                </td></tr>
                ~;

                $tempoutput = "<select name=\"arrawpostpic\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostpic\"/value=\"$arrawpostpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许贴图？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostflash\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostflash\"/value=\"$arrawpostflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许 Flash？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostreal\"><option value=\"off\">不允许<option value=\"on\" >允许</select>\n";
                $tempoutput =~ s/value=\"$arrawpostreal\"/value=\"$arrawpostreal\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许播放 Real 文件？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostmedia\"><option value=\"off\">不允许<option value=\"on\" >允许</select>\n";
                $tempoutput =~ s/value=\"$arrawpostmedia\"/value=\"$arrawpostmedia\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许播放 Media 文件？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostsound\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostsound\"/value=\"$arrawpostsound\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许声音？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostfontsize\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostfontsize\"/value=\"$arrawpostfontsize\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许改变文字大小？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawsignpic\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignpic\"/value=\"$arrawsignpic\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许贴图？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"arrawsignflash\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignflash\"/value=\"$arrawsignflash\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许 Flash？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawsignsound\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignsound\"/value=\"$arrawsignsound\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许声音？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawsignfontsize\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignfontsize\"/value=\"$arrawsignfontsize\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许改变文字大小？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>论坛图像设置</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>自定义头像最大宽度</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxposticonwidth" value="$maxposticonwidth" size=3 maxlength=3>　请不要超过 110</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>自定义头像最大高度</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxposticonheight" value="$maxposticonheight" size=3 maxlength=3>　请不要超过 130</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>头像库默认图像宽度(为空则不限)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultwidth" value="$defaultwidth" size=3 maxlength=3>　默认 32 像数，如果为空，则不限制</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>头像库默认图像高度(为空则不限)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultheight" value="$defaultheight" size=3 maxlength=3>　默认 32 像数，如果为空，则不限制</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>表情符图像默认宽度(为空则不限)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsmilewidth" value="$defaultsmilewidth" size=3 maxlength=3>　默认 13 像数，如果为空，则不限制</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>表情符图像默认高度(为空则不限)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsmileheight" value="$defaultsmileheight" size=3 maxlength=3>　默认 13 像数，如果为空，则不限制</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>论坛特殊样式设置</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子段落间距调整</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"paraspace\">\n<option value=\"130\">默认间距<option value=\"100\">单倍行距<option value=\"150\">1.5倍行距<option value=\"200\">双倍行距";
                $tempoutput =~ s/value=\"$paraspace\"/value=\"$paraspace\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子字间距调整</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"wordspace\">\n<option value=\"0\">默认间距<option value=\"-1\">紧缩<option value=\"+2\">扩充<option value=\"+4\">加宽";
                $wordspace =~ s/\+/\\+/;
                $tempoutput =~ s/value=\"$wordspace\"/value=\"$wordspace\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中每个表情允许显示的次数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsmail" value="$maxsmail" size=2 maxlength=2>　一般 2 -- 5 个左右啦</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复时候默认列出的最后回复个数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxlistpost" value="$maxlistpost" size=2 maxlength=2>　一般 5 -- 8 个左右啦</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>允许固定在顶端的主题数？<br>可以固定几个重要话题在论坛的最上面。</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtoptopic" value="$maxtoptopic" size=2 maxlength=2>　一般 1 -- 5 个左右啦</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>最后贴子预览的字符数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsavepost" value="$maxsavepost" size=3 maxlength=2>　不要超过 50，否则严重影响速度</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名允许的行数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsignline" value="$maxsignline" size=5 maxlength=2>　一般 5 行(和下面参数配合使用)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名的最多字符数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsignlegth" value="$maxsignlegth" size=5 maxlength=4>　一般 200 个字</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>个人简介允许的行数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxinsline" value="$maxinsline" size=5 maxlength=2>　一般  5 行(和下面参数配合使用)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>个人简介的最多字符数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxinslegth" value="$maxinslegth" size=5 maxlength=4>　一般 100 个字</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>头像列表一行几个图标</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="interval" value="$interval" size=2 maxlength=2>　一般 10 个</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>头像列表一页几行</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="linesperpage" value="$linesperpage" size=2 maxlength=2>　一般 10 行</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛投票贴子中允许的最大项目数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpollitem" value="$maxpollitem" size=2 maxlength=2>　请设置 5 - 50 之间</td>
                </tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><center><b>初始化特效设置</b> (Leoboard.cgi & Forums.cgi)</center><br>
</font></td>
</tr>
~;


$tempoutput = "<select name=\"pagechange\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
$tempoutput =~ s/value=\"$pagechange\"/value=\"$pagechange\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>调入页面时是否使用特效?</b><br>IE 4.0 以上版本浏览器有效</font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

$tempoutput = "<select name=\"cinoption\">\n
<option value=\"0\">盒状收缩\n
<option value=\"1\">盒状放射\n
<option value=\"2\">圆形收缩\n
<option value=\"3\">圆形放射\n
<option value=\"4\">向上擦除\n
<option value=\"5\">向下擦除\n
<option value=\"6\">向右擦除\n
<option value=\"7\">向左擦除\n
<option value=\"8\">垂直遮蔽\n
<option value=\"9\">水平遮蔽\n
<option value=\"10\">横向棋盘式\n
<option value=\"11\">纵向棋盘式\n
<option value=\"12\">随机分解\n
<option value=\"13\">左右向中央缩进\n
<option value=\"14\">中央向左右扩展\n
<option value=\"15\">上下向中央缩进\n
<option value=\"16\">中央向上下扩展\n
<option value=\"17\">从左下抽出\n
<option value=\"18\">从左上抽出\n
<option value=\"29\">从右下抽出\n
<option value=\"20\">从右上抽出\n
<option value=\"21\">随机水平线条\n
<option value=\"22\">随机垂直线条\n
<option value=\"23\">随机(上面任何一种)\n
</select>\n";
$tempoutput =~ s/value=\"$cinoption\"/value=\"$cinoption\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>特效类型?</b></font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>特效维持时间?</b><br>例： 1.0 = 1 秒, 0.5 = 1/2 秒.</font></td>
<td bgcolor=#FFFFFF>
<input type=text size=10 name="timetoshow" value="$timetoshow"> 默认：1</td>
</tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>其他设置</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认用户在线时间是多少分钟？<BR>如果用户超过这个时间还没有动作则默认用户已经离开了论坛。</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="membergone" value="$membergone" size=5 maxlength=5>　一般为 5 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>记录整个论坛最近几个主题？<br>用于在主页上显示最近 N 个话题。</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpostreport" value="$maxpostreport" size=3 maxlength=3>　一般 10 -- 20 个</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>一次删除贴子数超过多少就被纪录？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="logdelmax" value="$logdelmax" size=3 maxlength=3>　一般 5 - 10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每天允许最多删除贴子次数？(对坛主无效)<br>如果不想限制,请设置为 999.</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxdeloneday" value="$maxdeloneday" size=3 maxlength=3>　一般 5 - 10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>最近访问者来路统计个数？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newrefers" value="$newrefers" size=3 maxlength=3>　一般 20 - 40 个</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>多少小时内的新贴后面加 new 标志？<BR>(如果不想要，可以设置为 0)</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newmarktime" value="$newmarktime" size=3 maxlength=3>　一般 12 - 24 小时</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"noself\">\n<option value=\"on\">纪录\n<option value=\"off\">不纪录\n</select>\n";
                $tempoutput =~ s/value=\"$noself\"/value=\"$noself\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>纪录来路是自己主页的访问者？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>允许刷新论坛的时间间隔(秒)<BR>可以有效防止恶意刷新</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="banfreshtime" value="$banfreshtime" size=3 maxlength=3>　如果无需，请设置 0</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"look\">\n<option value=\"on\">开放\n<option value=\"off\">不开放\n</select>\n";
                $tempoutput =~ s/value=\"$look\"/value=\"$look\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否开放论坛配色？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"showskin\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$showskin\"/value=\"$showskin\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许用户自定义浏览论坛时的风格？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"announcemove\">\n<option value=\"on\">移动\n<option value=\"off\">不移动\n</select>\n";
               	$tempoutput =~ s/value=\"$announcemove\"/value=\"$announcemove\" selected/;
               	print qq~

               	<tr>
               	<td bgcolor=#FFFFFF colspan=2>
               	<font color=#333333>论坛公告是否采用移动风格？</font></td>
               	<td bgcolor=#FFFFFF>
               	$tempoutput</td>
               	</tr>
               	~;

                $tempoutput = "<select name=\"newmsgpop\">\n<option value=\"off\">不弹出\n<option value=\"on\">弹出\n</select>\n";
                $tempoutput =~ s/value=\"$newmsgpop\"/value=\"$newmsgpop\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>有新的短消息是否弹出窗口提示？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"xzbopen\"><option value=\"yes\">打开小字报<option value=\"no\">关闭小字报</select>\n";
                $tempoutput =~ s/value=\"$xzbopen\"/value=\"$xzbopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>打开论坛小字报功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"statsopen\"><option value=\"0\">任何人可以查看<option value=\"1\">注册用户可以查看<option value=\"2\">坛主和版主可以查看</select>\n";
                $tempoutput =~ s/value=\"$statsopen\"/value=\"$statsopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛统计察看开放方式？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"infosopen\"><option value=\"0\">任何人可以查看<option value=\"1\">注册用户可以查看<option value=\"2\">坛主和版主可以查看</select>\n";
                $tempoutput =~ s/value=\"$infosopen\"/value=\"$infosopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>列表排名资料察看开放方式？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"searchopen\"><option value=\"0\">任何人可以进行<option value=\"1\">注册用户可以进行</select>\n";
                $tempoutput =~ s/value=\"$searchopen\"/value=\"$searchopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛搜索可以由谁进行？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"regaccess\"><option value=\"off\">不，允许任何人访问<option value=\"on\">是，必须登陆后才能访问</select>\n";
                $tempoutput =~ s/value=\"$regaccess\"/value=\"$regaccess\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left  colspan=2>
                <font face=宋体 color=#333333>论坛只有注册用户可以访问？</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pvtip\">\n<option value=\"on\">显示 IP 和鉴定\n<option value=\"off\">保密 IP 和鉴定\n</select>\n";
                $tempoutput =~ s/value=\"$pvtip\"/value=\"$pvtip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><B>是否保密 IP 和鉴定？</B><BR>即使选择的是显示 IP，但普通用户还是<BR>只能看见 IP 的前两位</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能对坛主无效</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"smocanseeip\">\n<option value=\"yes\">有效\n<option value=\"no\">无效\n</select>\n";
                $tempoutput =~ s/value=\"$smocanseeip\"/value=\"$smocanseeip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>保密 IP 和鉴定对总斑竹是否有效？</B><BR>如选择无效，则总版主可查看所有的 IP<BR>而不受上面 IP 保密的限制</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowupload\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrowupload\"/value=\"$arrowupload\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子是否允许上传？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能对版主和坛主无效</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"allowattachment\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$allowattachment\"/value=\"$allowattachment\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复是否允许上传？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能对版主和坛主无效</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛上传文件允许的最大值(单位：KB)<br>如果设置了不允许上传，则此项无效！</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxupload" value="$maxupload" size=5 maxlength=5>　不要加 KB，建议不要超过 500</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowavaupload\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrowavaupload\"/value=\"$arrowavaupload\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许上传自定义头像？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowuserdel\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrowuserdel\"/value=\"$arrowuserdel\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许注册用户自己锁定或删除自己的贴子？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"quotemode\">\n<option value=\"0\">表格\n<option value=\"1\">线条\n</select>\n";
                $tempoutput =~ s/value=\"$quotemode\"/value=\"$quotemode\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>引用标签的样式？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"onlineview\">\n<option value=\"1\">显示\n<option value=\"0\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$onlineview\"/value=\"$onlineview\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认是否显示在线用户详细列表？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"advpost\">\n<option value=\"1\">高级模式\n<option value=\"0\">简洁模式\n</select>\n";
                $tempoutput =~ s/value=\"$advpost\"/value=\"$advpost\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认发贴模式？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"sendwelcomemessage\">\n<option value=\"yes\">发送\n<option value=\"no\">不发送\n</select>\n";
                $tempoutput =~ s/value=\"$sendwelcomemessage\"/value=\"$sendwelcomemessage" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否发欢迎消息给新注册用户？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"sortalltopic\">\n<option value=\"yes\">开放\n<option value=\"no\">不开放\n</select>\n";
                $tempoutput =~ s/value=\"$sortalltopic\"/value=\"$sortalltopic" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否开放论坛贴子排序察看功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"sortposticonshow\">\n<option value=\"yes\">最后回复人的心情符\n<option value=\"no\">发贴人的心情符\n</select>\n";
                $tempoutput =~ s/value=\"$sortposticonshow\"/value=\"$sortposticonshow" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛中贴子心情符号显示为？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"refreshforum\">\n<option value=\"off\">不要自动刷新\n<option value=\"on\">要自动刷新\n</select>\n";
                $tempoutput =~ s/value=\"$refreshforum\"/value=\"$refreshforum" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>分论坛是否自动刷新(请在下面设置间隔时间)？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>自动刷新论坛的时间间隔(秒)<BR>配合上面参数一起使用</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="autofreshtime" value="$autofreshtime" size= 5 maxlength=5>　一般设置 5 分钟，就是 300 秒。</td>
                </tr>
		~;

                $tempoutput = "<select name=\"movetopicname\">\n<option value=\"on\">显示\n<option value=\"off\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$movetopicname\"/value=\"$movetopicname" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>转移过的贴子是否显示转移字样？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"editusertitleself\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$editusertitleself\"/value=\"$editusertitleself" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许用户自行修改个人头衔？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"editjhmpself\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$editjhmpself\"/value=\"$editjhmpself" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许用户自行修改江湖门派？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispquickreply\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
                $tempoutput =~ s/value=\"$dispquickreply\"/value=\"$dispquickreply" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否启用快速回复？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispview\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispview\"/value=\"$dispview\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>是否显示论坛图例</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>主论坛标题图片<br>此图必须在 images 目录下，只能是名称，不可以加 URL 地址或绝对路径</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="boardlogo" value="$boardlogo"><BR></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <input type=submit value="提 交"></td></form></tr></table></td></tr></table>
                ~;
                }
                }
                else {
                    &adminlogin;
                    }

print qq~</td></tr></table></body></html>~;
exit;
