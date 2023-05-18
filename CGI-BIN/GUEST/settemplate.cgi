#!/usr/bin/perl
#------------------------------------------------------#
#                                                      #
#              本程序为 中国CGI之家 提供	           #
#              Ajie的留言板多用户版V4.0                #
#------------------------------------------------------#
&mypath;
require "$mypath/info/setup.cgi";
require "$mypath/sub.cgi";
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
if ($action eq "settemplate") {
$template_data=$FORM{'template_data'};
$template_data =~ s/\&lt;/</g;
$template_data =~ s/\&gt;/>/g;
$template_data =~ s/ \&nbsp;/　/g;
$template_data =~ s/\&amp;/\&/g;
        $filetomake = "$mypath/info/template.cgi";
        open(FILE,">$filetomake");
        print FILE $template_data;
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
                <font face=宋体 color=#336666><b>所有模板信息已经写入</b>
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
                <font face=宋体 color=#336666>所有信息没有保存<br>文件或者目录不可写<br>请检测你的 info 目录和 template.cgi 文件的属性！
        <hr color=#DCECEA>
        </td></tr></table></td></tr></table>
        );}
                    }


else {
      $templatefile = "$mypath/info/template.cgi";
      open (TEMPLATE, "$templatefile");
      local $/ = undef;
      $template_data = <TEMPLATE>;
      close (TEMPLATE);
   $template_data =~ s/</&lt;/g;
   $template_data =~ s/>/&gt;/g;
   $template_data =~ s/\"/&quot;/g;
   $template_data =~ s/\n\n/\n/ig;
   $template_data =~ s/[\f\n\r]+/\n/ig;
   $template_data =~ s/[\r \n]+$/\n/ig;
   $template_data =~ s/^[\r\n ]+/\n/ig;
   $template_data =~ s/\s+$//ig;
print qq(
<tr><td bgcolor="#73BAB4" colspan="3"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b></font>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="3">
                <font face=宋体 color=#336666><b>编辑留言本模板</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5>
                </td>
                </tr>
<form method="post" action="$cgiurl/settemplate.cgi">
<input type=hidden name="action" value="settemplate">);
print qq(
<tr bgColor=ECF6F5><td width=100%><textarea name="template_data" wrap="soft" cols="85" rows="20">
   $template_data
   </textarea>
   <br><br></td></tr>
<tr><td width="100%" bgcolor=#DCECEA align="center" colspan="3">
<input type="submit" value="保存模板" name=ok>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td></tr></FORM>
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