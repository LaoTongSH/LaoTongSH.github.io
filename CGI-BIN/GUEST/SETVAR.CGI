#!/usr/bin/perl
#------------------------------------------------------#
#                                                      #
#              本程序为 中国CGI之家 提供	           #
#              Ajie的留言板多用户版V4.0                #
#------------------------------------------------------#
&mypath;
require "$mypath/"."info/setup.cgi";
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
if ($action eq "process") {
		$admail=$FORM{'adminmail'};
		$admail =~ s/\@/\\\@/g;
        $line0=$FORM{'line1'};
        $line0 =~ s/\"//g;
        $filetomake = "$mypath/info/setup.cgi";
        open(FILE,">$filetomake");
        print FILE "\$mainonoff=\"$FORM{'mainonoff'}\";\n";
        print FILE "\$line1=\"$line0\";\n";
        print FILE "\$gbname=\"$FORM{'gbname'}\";\n";
        print FILE "\$home=\"$FORM{'home'}\";\n";
        print FILE "\$homeurl=\"$FORM{'homeurl'}\";\n";
        print FILE "\$adminmail=\"$admail\";\n";
        print FILE "\$admin=\"$FORM{'admin'}\";\n";
        print FILE "\$password=\"$FORM{'password'}\";\n";
        print FILE "\$mailprog=\"$FORM{'mailprog'}\";\n";
        print FILE "\$cgiurl=\"$FORM{'cgiurl'}\";\n";
        print FILE "\$images=\"$FORM{'images'}\";\n";
		print FILE "\$cgiabs=\"$FORM{'cgiabs'}\";\n";
		print FILE "\$datapath=\"$FORM{'datapath'}\";\n";
		print FILE "\$infopath=\"$FORM{'infopath'}\";\n";
		print FILE "\$userpath=\"$FORM{'userpath'}\";\n";
		print FILE "\$ipdir=\"$FORM{'ipdir'}\";\n";
		print FILE "\$lymax=\"$FORM{'lymax'}\";\n";
		print FILE "\$pagenum=\"$FORM{'pagenum'}\";\n";
		print FILE "\$sendusermail=\"$FORM{'sendusermail'}\";\n";
		print FILE "\$mailtoadmin=\"$FORM{'mailtoadmin'}\";\n";
		print FILE "\$shenqing=\"$FORM{'shenqing'}\";\n";
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
		 \$mainonoff=$FORM{'mainonoff'};<br>
         \$line1=$FORM{'line1'};<br>
         \$gbname=$FORM{'gbname'};<br>
         \$home=$FORM{'home'};<br>
         \$homeurl=$FORM{'homeurl'};<br>
         \$adminmail=$FORM{'adminmail'};<br>
         \$admin=$FORM{'admin'};<br>
         \$password=$FORM{'password'};<br>
         \$mailprog=$FORM{'mailprog'};<br>
         \$cgiurl=$FORM{'cgiurl'};<br>
         \$images=$FORM{'images'};<br>
		 \$cgiabs=$FORM{'cgiabs'};<br>
		 \$datapath=$FORM{'datapath'};<br>
		 \$infopath=$FORM{'infopath'};<br>
		 \$userpath=$FORM{'userpath'};<br>
		 \$ipdir=$FORM{'ipdir'};<br>
		 \$lymax=$FORM{'lymax'};<br>
		 \$pagenum=$FORM{'pagenum'};<br>
		 \$sendusermail=$FORM{'sendusermail'};<br>
		 \$mailtoadmin=$FORM{'mailtoadmin'};<br>
		 \$shenqing=$FORM{'shenqing'};<br>
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
                <font face=宋体 color=#336666>所有信息没有保存<br>文件或者目录不可写<br>请检测你的 info 目录和 setup.cgi 文件的属性！
        <hr color=#DCECEA>
        </td></tr></table></td></tr></table>
        );}
                    }


else {
print qq(
<tr><td bgcolor="#73BAB4" colspan="2"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=宋体 color=#336666><b>论坛变量设置</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<form method="post" action="$cgiurl/setvar.cgi">
<input type=hidden name="action" value="process">);
$tempoutput="<select name=\"mainonoff\"><option value=\"on\">留言本开放<option value=\"off\">留言本关闭</select>";
$tempoutput=~ s/value=\"$mainonoff\"/value=\"$mainonoff\" selected/;
print qq(<tr bgColor=ECF6F5><td width=30%><b>留言本状态：</b></td><td width=70%>$tempoutput</td></tr>
<tr bgColor=ECF6F5><td width=30%><b>维护说明：</b>(支持 HTML)</td><td width=70%><textarea name="line1" cols="40">$line1</textarea></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>留言本名称：</b></td><td width=70%><input type="text" name="gbname" size="40" value=$gbname></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>主页名称：</b></td><td width=70%><input type="text" name="home" size="40" value=$home></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>主页地址：</b></td><td width=70%><input type="text" name="homeurl" size=40 value="$homeurl"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>版主邮箱：</b><br></td><td width=70%><input type="text" name="adminmail" size="40" value=$adminmail></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>管理员名称：</b></td><td width=70%><input type="text" name="admin" size="40" value="$admin"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>管理员密码：</b></td><td width=70%><input type="text" name="password" size="40" value = "$password"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>发送邮件程序位置：</b><br>暂时不支持NT下发信</td><td width=70%><input type="text" name="mailprog" size="40" value="$mailprog"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>留言本URL地址：</b><br>结尾不要加 "/"</td><td width=70%><input type="text" name="cgiurl" size="40" value="$cgiurl"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>图片目录的URL：</b><br>结尾不要加 "/"</td><td width=70%><input type="text" name="images" size="40" value="$images"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>程序的绝对路径：</b><br>结尾不要加 "/"</td><td width=70%><input type="text" name="cgiabs" size="40" value="$cgiabs"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>data目录的绝对路径：</b><br>结尾不要加 "/"</td><td width=70%><input type="text" name="datapath" size="40" value="$datapath"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>info目录的绝对路径：</b><br>结尾不要加 "/"</td><td width=70%><input type="text" name="infopath" size="40" value="$infopath"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>user目录的绝对路径：</b><br>结尾不要加 "/"</td><td width=70%><input type="text" name="userpath" size="40" value="$userpath"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>ipdata目录的绝对路径：</b><br>结尾不要加 "/"</td><td width=70%><input type="text" name="ipdir" size="40" value="$ipdir"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>最大留言字数：</b></td><td width=70%><input type="text" name="lymax" size="40" value="$lymax"></td></tr>
<tr bgColor=ECF6F5><td width=30%><b>每页记录数：</b></td><td width=70%><input type="text" name="pagenum" size="40" value="$pagenum"></td></tr>);
$tempoutput="<select name=\"sendusermail\"><option value=\"yes\">是<option value=\"no\">否</select>";
$tempoutput=~ s/value=\"$sendusermail\"/value=\"$sendusermail\" selected/;
print qq(<tr bgColor=ECF6F5><td width=30%><b>是否给申请者发送邮件：</b></td><td width=70%>$tempoutput</td></tr>);
$tempoutput="<select name=\"mailtoadmin\"><option value=\"yes\">是<option value=\"no\">否</select>";
$tempoutput=~ s/value=\"$mailtoadmin\"/value=\"$mailtoadmin\" selected/;
print qq(<tr bgColor=ECF6F5><td width=30%><b>是否给管理员发送邮件：</b></td><td width=70%>$tempoutput</td></tr>);
$tempoutput="<select name=\"shenqing\"><option value=\"on\">是<option value=\"off\">否</select>";
$tempoutput=~ s/value=\"$shenqing\"/value=\"$shenqing\" selected/;
print qq(<tr bgColor=ECF6F5><td width=30%><b>是否允许申请新留言本：</b></td><td width=70%>$tempoutput</td></tr>
<tr><td width="100%" bgcolor=#DCECEA align="center" colspan="2">
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