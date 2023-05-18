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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                        # Unbuffer the output
$thisprog = "misc.cgi";
$query = new LBCGI;
&ipbanned; #封杀一些 ip
	
$UIN                    = $query -> param('UIN');
$action                 = $query -> param('action');
$aimname                = $query -> param('aimname');
$aimname =~ s/ //g;
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if (!$inmembername) { $inmembername = "客人"; }
if ($action eq "showsmilies") {
    $output = qq~
    <html><head><title>表情转换</title>
	<style>
		.t     {	LINE-HEIGHT: 1.4			}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
	</style>
    </head>
    <body topmargin=0 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1 border=0>
            <tr>
                <td bgcolor=$titlecolor align=center colspan=2>
                    <font color=$titlefontcolor><b>$boardname - 表情转换</b></font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo align=center>
                    <font color="$fontcolormisc">代码</font>
                </td>
                    <td bgcolor=$miscbacktwo align=center>
                    <font color=$fontcolormisc>转换后</font>
                </td>
                </tr>
    ~;
    
        open (FILE, "$lbdir/data/lbemot.cgi");
	my @emoticondata = <FILE>;
	close (FILE);
	chomp @emoticondata;
        
    foreach $picture (@emoticondata) {
	$smileyname = $picture;
	$smileyname =~ s/\.gif//g;
	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone align=center>
	<font color=$fontcolormisc>:$smileyname:</font>
	</td>
	<td bgcolor=$miscbackone align=center>
	<img src=$imagesurl/emot/$picture>
	</td>
	</tr>
	~;
    }
    $output .= qq~
	</table>
	</td></tr>
	</table>
	</body>
	</html>
    ~;
}
elsif ($action eq "icq") {
    $output = qq~
    <html><head><title>$boardname 的 ICQ 寻呼</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}
		
	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}
	        
		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
	</style>
    </head>
    <body topmargin=10 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <form action="http://wwp.mirabilis.com/scripts/WWPMsg.dll" method="post">
        <input type="hidden" name="subject" value="来自 - $boardname"><input type="hidden" name="to" value="$UIN">
        <table width=100% cellpadding=5 cellspacing=1 border=0>
            <tr>
                <td bgcolor=$titlecolor align=center colspan=2>
                    <font color=$titlefontcolor><b>$boardname - ICQ 寻呼</b><br>发送一个消息给 $UIN</font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo valign=top>
                    <font color=$fontcolormisc>请输入您的姓名</font>
                </td>
                    <td bgcolor=$miscbacktwo>
                    <input type="text" name="from" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top>
                    <font color=$fontcolormisc>请输入您的 Email</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <input type="text" name="fromemail" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top>
                    <font color=$fontcolormisc>要发送的消息</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <textarea name="body" rows="3" cols="30" wrap="Virtual"></textarea>
                </td>
                </tr>
                <tr>
                <td bgcolor=$miscbacktwo align=center colspan=2>
                <input type="submit" name="Send" value="发送消息"></form>
                </td>
                </tr>
            </table>
        </td></tr>
    </table>
    </body>
    </html>
    ~;
}
elsif ($action eq "lbcode") {
    $output = qq~
    <html><head><title>LB5000 标签</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}
		
	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}
	        
		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
	</style>
<script language="javaScript" type="text/javascript" SRC="$imagesurl/images/board.js"></SCRIPT>
    </head>
    <body topmargin=10 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1 border=0>
            <tr>
                <td bgcolor=$titlecolor align=center colspan=2>
                    <font color=$titlefontcolor><b>LB5000 标签</b>
                    <br>LB5000 标签很象 HTML 标签，但比 HTML 标签安全。你可以参照下面手册中的格式来使用它！
                    </font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone><ul>
                    <font color=$fontcolormisc>
                    <font color=$fonthighlight>[quote]</font>这个标签是用来做为引用所设置的，如果你有什么内容是引用自别的地方，请加上这个标签！<font color=$fonthighlight>[/quote]</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><hr noshade color=$fonthighlight><blockquote>这个标签是用来做为引用所设置的，如果你有什么内容是引用自别的地方，请加上这个标签！</blockquote><hr noshade color=$fonthighlight></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone><UL>
                    <font color=$fontcolormisc>
                    <font color=$fonthighlight>[code]</font>
                    	<BR>unless ( eq "$authenticateme") {
			<BR>print "错误的管理密码";
			<BR>&unlock;
			<BR>exit;
			<BR>}<BR>
			<font color=$fonthighlight>[/code]</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc>
			<BLOCKQUOTE>代码：<hr noshade color=$fonthighlight>
			unless ( eq "$authenticateme") { <BR>
			print "错误的管理密码"; <BR>
			&unlock; <BR>
			exit; <BR>
			}<hr noshade color=$fonthighlight></FONT></BLOCKQUOTE>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[html]</font>&lt;font size=5&gt;HTML 和 JS 代码支持&lt;/font&gt;<font color=$fonthighlight>[/html]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><SPAN><IMG src=$imagesurl/images/code.gif align=absBottom> HTML 代码片段如下:<BR><TEXTAREA style="WIDTH: 94%; BACKGROUND-COLOR: #f7f7f7" name=textfield rows=4>&lt;font size=5&gt;HTML 和 JS 代码支持&lt;/font&gt;<\/TEXTAREA><BR><INPUT onclick=runEx() type=button value=运行此代码 name=Button> [Ctrl+A 全部选择   提示:你可先修改部分代码，再按运行]</SPAN><BR></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[url]</font>http://www.CGIer.com<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="http://www.CGIer.com">http://www.CGIer.com</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[url=http://www.CGIer.com]</font>CGI 编程者之家<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="http://www.CGIer.com">CGI 编程者之家</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[email=webmaster\@cgier.com]</font>写信给我<font color=$fonthighlight>[/email]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="mailto:webmaster\@cgier.com">写信给我</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[email]</font>webmaster\@cgier.com<font color=$fonthighlight>[/email]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="mailto:webmaster\@cgier.com">webmaster\@cgier.com</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[b]</font>文字加粗体效果<font color=$fonthighlight>[/b]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><b>文字加粗体效果</b></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[i]</font>文字加倾斜效果<font color=$fonthighlight>[/i]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><i>文字加倾斜效果</i></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[u]</font>文字加下划线效果<font color=$fonthighlight>[/u]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><u>文字加下划线效果</u></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[size=4]</font>改变文字大小<font color=$fonthighlight>[/size]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font size=4>改变文字大小</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[font=impact]</font>改变字体<font color=$fonthighlight>[/font]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font face=impact>改变字体</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[color=red]</font>改变文字颜色<font color=$fonthighlight>[/color]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=red>改变文字颜色</font>
                </td>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[s]</font>文字上加删除线<font color=$fonthighlight>[/s]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><s>文字上加删除线</s></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sup]</font>上标文字<font color=$fonthighlight>[/sup]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><sup>上标文字</sup></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sub]</font>下标文字<font color=$fonthighlight>[/sub]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><sub>下标文字</sub></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[FLIPH]</font>左右颠倒文字<font color=$fonthighlight>[/FLIPH]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:flipH">左右颠倒文字</table></FLIPH>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[FLIPV]</font>上下颠倒文字<font color=$fonthighlight>[/FLIPV]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:flipV">上下颠倒文字</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[INVERT]</font>底片效果<font color=$fonthighlight>[/INVERT]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:invert"><img src="$imagesurl/images/ad8831.gif" border=0></table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[XRAY]</font>曝光效果<font color=$fonthighlight>[/XRAY]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:xray"><img src="$imagesurl/images/logo.gif" border=0></table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[shadow=文字宽度,颜色,边界大小]</font>阴影文字<font color=$fonthighlight>[/shadow]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:shadow\(color=#f000ff\, direction=1)">阴影文字</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[GLOW=文字宽度,颜色,边界大小]</font>光晕文字<font color=$fonthighlight>[/GLOW]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:glow\(color=#00f0ff\, strength=1)">光晕文字</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[BLUR=文字宽度,方向,浓度]</font>模糊文字<font color=$fonthighlight>[/BLUR]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:blur\(Add=0, direction=6\, strength=2)">模糊文字</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[list]</font>开始列表<br><font color=$fonthighlight>[*]</font>列表项目<br><font color=$fonthighlight>[/list]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><ul>开始列表<br><li>列表项目</ul></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[img]</font>http://www.17do.com/ib2000/images/mainlogo.gif<font color=$fonthighlight>[/img]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><img src="$imagesurl/images/mainlogo.gif" border=0></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[fly]</font>飞行文字特效<font color=$fonthighlight>[/fly]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><marquee width=90% behavior=alternate scrollamount=3>飞行文字特效<\/marquee></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[move]</font>滚动文字特效<font color=$fonthighlight>[/move]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><marquee width=90% scrollamount=3>滚动文字特效<\/marquee></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[swf]</font>http://www.micromedia.com/demo.swf<font color=$fonthighlight>[/swf]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个 FLASH 文件(自动控制大小)</font>
                </td> 
                </tr> 
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[flash=宽度,高度]</font>http://www.micromedia.com/demo.swf<font color=$fonthighlight>[/flash]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个 FLASH 文件(手动设置大小)</font>
                </td> 
                </tr> 
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sound]</font>http://www.cgier.com/demo.wav<font color=$fonthighlight>[/sound]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个背景声音文件(*.mid,*.wav)</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[mms]</font>mms://www.microsoft.com/demo.asf<font color=$fonthighlight>[/mms]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个 WM 格式流数据</font>
                </td> 
                </tr> 
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[rtsp]</font>rtsp://www.real.com/demo.ram<font color=$fonthighlight>[/rtsp]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个 Real 格式流数据</font>
                </td> 
                </tr> 
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[ra]</font>http://www.cgier.com/demo.ra<font color=$fonthighlight>[/ra]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Real Player播放音频文件(*.mp3,*.ra)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[rm]</font>http://www.cgier.com/demo.rm<font color=$fonthighlight>[/rm]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Real Player播放视频文件(*.rm)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wmv]</font>http://www.cgier.com/demo.wmv<font color=$fonthighlight>[/wmv]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Windows Media Player播放视频文件(*.wmv)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wma]</font>http://www.cgier.com/demo.wma<font color=$fonthighlight>[/wma]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Windows Media Player播放音频文件(*.wma)</font>
                </td>
                </tr>
            </table>
        </td></tr>
    </table>
    </body>
    </html>
    ~;
}
elsif ($action eq "newmsg") {
    $output = qq~
    <html><head><title>有新的短消息</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}
		
	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}
	        
		.t     {	LINE-HEIGHT: 1.4			}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
</style>
</head>
    
<body topmargin=8 leftmargin=13 bgcolor=#FFFFFF>
<br>
<table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center height=280>
  <tr> 
    <td> 
      <table cellpadding=6 cellspacing=1 border=0 width=100% height=279>
        <tr> 
          <td  bgcolor=$titlecolor colspan=2 height=27> 
            <div align=center>短消息通知</div>
          </td>
        </tr>
        <tr> 
          <td colspan=2 bgcolor=$forumcolorone>
            <div align=center><br>
              
              <center>
                <font color=$titlefontcolor><a href=$messangerprog><img src=$imagesurl/images/newmail.gif border=0></a>有新的短消息<br>
                <br>
                <a href=$messangerprog>按此查看</a><br>
                </font>
              </center>
              <br></div>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
    </html>
~;
}
print header(-charset=>gb2312);
print $output;
exit;
