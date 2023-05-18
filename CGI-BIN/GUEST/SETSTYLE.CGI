#!/usr/bin/perl
#------------------------------------------------------#
#                                                      #
#              本程序为 中国CGI之家 提供	           #
#              Ajie的留言板多用户版V4.0                #
#------------------------------------------------------#
&mypath;
require "$mypath/"."info/setup.cgi";
require "$mypath/"."info/style.cgi";
require "$mypath/"."sub.cgi";
&parseadminform;
@cookies = split(/; /,$ENV{HTTP_COOKIE});
foreach (@cookies){
($name,$value) = split(/=/,$_);
$cookie{$name} = $value;}
$inmembername = $cookie{adminname};
$inpassword = $cookie{adminpass};
&header;
&admintitle;
if(($inmembername ne $admin)||($inpassword ne $password))
{
   &adminlogin;
}
else  {
$action=$FORM{'action'};
if ($action eq "setstyle") {
        $downgg =$FORM{'downgg'};
        $downgg =~ s/\"//g;
        $topgg=$FORM{'topgg'};
        $topgg =~ s/\"//g;
        $filetomake = "$mypath/info/style.cgi";
        open(FILE,">$filetomake");
        print FILE "\$gbbody=\"$FORM{'gbbody'}\";\n";
        print FILE "\$gbbgcolor=\"$FORM{'gbbgcolor'}\";\n";
        print FILE "\$cdfont=\"$FORM{'cdfont'}\";\n";
        print FILE "\$btbgcolor=\"$FORM{'btbgcolor'}\";\n";
        print FILE "\$btfont=\"$FORM{'btfont'}\";\n";
        print FILE "\$tbcolor=\"$FORM{'tbcolor'}\";\n";
        print FILE "\$guestbgcolor=\"$FORM{'guestbgcolor'}\";\n";
        print FILE "\$guestfont=\"$FORM{'guestfont'}\";\n";
        print FILE "\$guestnamefont=\"$FORM{'guestnamefont'}\";\n";
        print FILE "\$guestnamegy=\"$FORM{'guestnamegy'}\";\n";
		print FILE "\$lybgcolor=\"$FORM{'lybgcolor'}\";\n";
		print FILE "\$lyfont=\"$FORM{'lyfont'}\";\n";
		print FILE "\$adminfont=\"$FORM{'adminfont'}\";\n";
		print FILE "\$adminfontny=\"$FORM{'adminfontny'}\";\n";
		print FILE "\$tablewidth=\"$FORM{'tablewidth'}\";\n";
		print FILE "\$topgg=\"$topgg\";\n";
		print FILE "\$downgg=\"$downgg\";\n";
		print FILE "1\;\n";
        close(FILE);

        if (-e $filetomake && -w $filetomake) {
print qq(
<tr><td bgcolor="#73BAB4"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center>
                <font face=宋体 color=#336666><b>以下信息已经成功保存</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
                <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left>
                <font face=宋体 color=#336666>
         \$gbbody=\"$FORM{'gbbody'}\";<br>
         \$gbbgcolor=\"$FORM{'gbbgcolor'}\";<br>
         \$cdfont=\"$FORM{'cdfont'}\";<br>
         \$btbgcolor=\"$FORM{'btbgcolor'}\";<br>
         \$btfont=\"$FORM{'btfont'}\";<br>
         \$tbcolor=\"$FORM{'tbcolor'}\";<br>
         \$guestbgcolor=\"$FORM{'guestbgcolor'}\";<br>
         \$guestfont=\"$FORM{'guestfont'}\";<br>
         \$guestnamefont=\"$FORM{'guestnamefont'}\";<br>
         \$guestnamegy=\"$FORM{'guestnamegy'}\";<br>
		 \$lybgcolor=\"$FORM{'lybgcolor'}\";<br>
		 \$lyfont=\"$FORM{'lyfont'}\";<br>
		 \$adminfont=\"$FORM{'adminfont'}\";<br>
		 \$adminfontny=\"$FORM{'adminfontny'}\";<br>
		 \$tablewidth=\"$FORM{'tablewidth'}\";<br>
		 \$topgg=\"$FORM{'topgg'}\";<br>
		 \$downgg=\"$FORM{'downgg'}\";<br>
        <hr color=#DCECEA>
        </td></tr></table></td></tr></table>
        );}
        else {

print qq(
<tr><td bgcolor="#73BAB4"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center>
                <font face=宋体 color=#336666><b>错误</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
                <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left>
                <font face=宋体 color=#336666>所有信息没有保存<br>文件或者目录不可写<br>请检测你的 info 目录和 style.cgi 文件的属性！
        <hr color=#DCECEA>
        </td></tr></table></td></tr></table>
        );}
                    }


else {
print qq(
<tr><td bgcolor="#73BAB4" colspan="3"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="3">
                <font face=宋体 color=#336666><b>留言本BODY标签</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<form method="post" action="$cgiurl/setstyle.cgi">
<input type=hidden name="action" value="setstyle">);
print qq(
<tr bgColor=ECF6F5><td width=30%>控制整个留言本风格的背景颜色或者背景图片等：</td><td width=70% colspan="2"><input type=text name="gbbody" size=60 value="$gbbody"><br>默认：alink=#336666 vlink=#336666 link=#336666 topmargin=0 leftmargin=0</td></tr>
<tr>
<td bgcolor=#DCECEA valign=middle align=center colspan="3">
<font face=宋体 color=#336666><b>留言本外观颜色</b></font>
</td></tr>
<tr bgColor=ECF6F5><td width=30%>背景颜色：</td>
<td bgcolor=$gbbgcolor  width=5%></td>
<td width=65%><input type=text name="gbbgcolor" value="$gbbgcolor" size=7 maxlength=7>　默认：#ECF6F5</td></tr>
<tr bgColor=ECF6F5><td width=30%>留言本页首菜单字体颜色：</td>
<td bgcolor=$cdfont width=5%></td>
<td width=65%><input type=text name="cdfont" value="$cdfont" size=7 maxlength=7>　默认：#336666</td></tr>
<tr bgColor=ECF6F5><td width=30%>标题栏背景颜色：</td>
<td bgcolor=$btbgcolor  width=5%></td>
<td width=65%><input type=text name="btbgcolor" value="$btbgcolor" size=7 maxlength=7>　默认：#73BAB4</td></tr>
<tr bgColor=ECF6F5><td width=30%>标题栏字体颜色：</td>
<td bgcolor=$btfont  width=5%></td>
<td width=65%><input type=text name="btfont" value="$btfont" size=7 maxlength=7>　默认：#ffffff</td></tr>
<tr bgColor=ECF6F5><td width=30%>表格颜色：</td>
<td bgcolor=$tbcolor  width=5%></td>
<td width=65%><input type=text name="tbcolor" value="$tbcolor" size=7 maxlength=7>　默认：#336666</td></tr>
<tr bgColor=ECF6F5><td width=30%>留言者区背景颜色：</td>
<td bgcolor=$guestbgcolor  width=5%></td>
<td width=65%><input type=text name="guestbgcolor" value="$guestbgcolor" size=7 maxlength=7>　默认：#ECF6F5</td></tr>
<tr bgColor=ECF6F5><td width=30%>留言者区字体颜色：</td>
<td bgcolor=$guestfont  width=5%></td>
<td width=65%><input type=text name="guestfont" value="$guestfont" size=7 maxlength=7>　默认：#336666</td></tr>
<tr bgColor=ECF6F5><td width=30%>留言者名称字体颜色：</td>
<td bgcolor=$guestnamefont width=5%></td>
<td width=65%><input type=text name="guestnamefont" value="$guestnamefont" size=7 maxlength=7>　默认：#ffffff</td></tr>
<tr bgColor=ECF6F5><td width=30%>留言者名称上的光晕颜色：</td>
<td bgcolor=$guestnamegy width=5%></td>
<td width=65%><input type=text name="guestnamegy" value="$guestnamegy" size=7 maxlength=7>　默认：#336666</td></tr>
<tr bgColor=ECF6F5><td width=30%>留言区背景颜色：</td>
<td bgcolor=$lybgcolor width=5%></td>
<td width=65%><input type=text name="lybgcolor" value="$lybgcolor" size=7 maxlength=7>　默认：#ECF6F5</td></tr>
<tr bgColor=ECF6F5><td width=30%>留言区字体颜色：</td>
<td bgcolor=$lyfont width=5%></td>
<td width=65%><input type=text name="lyfont" value="$lyfont" size=7 maxlength=7>　默认：#336666</td></tr>
<tr bgColor=ECF6F5><td width=30%>"版主回复"字体颜色：</td>
<td bgcolor=$adminfont width=5%></td>
<td width=65%><input type=text name="adminfont" value="$adminfont" size=7 maxlength=7>　默认：#ff0000</td></tr>
<tr bgColor=ECF6F5><td width=30%>"版主回复"内容颜色：</td>
<td bgcolor=$adminfontny width=5%></td>
<td width=65%><input type=text name="adminfontny" value="$adminfontny" size=7 maxlength=7>　默认：#000000</td></tr>
<tr bgColor=ECF6F5><td width=30%>所有表格宽度：</td>
<td width=70% colspan="3"><input type=text name="tablewidth" value="$tablewidth" size=7 maxlength=7>　默认：90%</td></tr>
<tr>
<td bgcolor=#DCECEA valign=middle align=center colspan="3">
<font face=宋体 color=#336666><b>广告代码设置</b></font>
</td></tr>
<tr bgColor=ECF6F5><td width=30%>页首广告代码：(支持 HTML)</td>
<td width=70% colspan="2"><textarea name="topgg" cols="40">$topgg</textarea></td></tr>
<tr bgColor=ECF6F5><td width=30%>页尾广告代码：(支持 HTML)</td>
<td width=70% colspan="2"><textarea name="downgg" cols="40">$downgg</textarea></td></tr>
<tr><td width="100%" bgcolor=#DCECEA align="center" colspan="3">
<input type="submit" value="提交申请" name=ok>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td></tr></FORM>
</table></td></tr></table>
);}
}
######################################################
sub mypath{
local
$temp;
$temp=__FILE__;
$temp=~ s/\\/\//g if ($temp=~/\\/);
if ($temp) {$mypath=substr($temp,0,rindex($temp,"/"));}
else {
$mypath=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
$mypath=~ s/\\/\//g;
}
return
$mypath;
}