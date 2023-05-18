#!/usr/bin/perl
#------------------------------------------------------#
#                                                      #
#              本程序为 中国CGI之家 提供	       #
#              Ajie的留言板多用户版V3.01               #
#------------------------------------------------------#
&mypath;
require "$mypath/"."info/setup.cgi";
require "$mypath/"."info/style.cgi";
require "$mypath/"."sub.cgi";
&pagestyle;
&parseadminform;
&header;
print qq(
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>$title</title></head>
<body bgcolor="$gbbgcolor" $gbbody>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
<table width=100% cellspacing=1 align=center cellpadding=4 border=0>
  <tr bgcolor=$btbgcolor>
    <td colspan=5><div align=center><font color=$btfont>头 像 列 表</font></div></td>
  </tr>
  <tr bgcolor=$lybgcolor>
    <td><div align=center>头像01<br><img src=$images/01.gif></div></td>
    <td><div align=center>头像02<br><img src=$images/02.gif></div></td>
    <td><div align=center>头像03<br><img src=$images/03.gif></div></td>
    <td><div align=center>头像04<br><img src=$images/04.gif></div></td>
    <td><div align=center>头像05<br><img src=$images/05.gif></div></td>
  </tr>
  <tr bgcolor=$lybgcolor>
    <td><div align=center>头像06<br><img src=$images/06.gif></div></td>
    <td><div align=center>头像07<br><img src=$images/07.gif></div></td>
    <td><div align=center>头像08<br><img src=$images/08.gif></div></td>
    <td><div align=center>头像09<br><img src=$images/09.gif></div></td>
    <td><div align=center>头像10<br><img src=$images/10.gif></div></td>
  </tr>
  <tr bgcolor=$lybgcolor>
    <td><div align=center>头像11<br><img src=$images/11.gif></div></td>
    <td><div align=center>头像12<br><img src=$images/12.gif></div></td>
    <td><div align=center>头像13<br><img src=$images/13.gif></div></td>
    <td><div align=center>头像14<br><img src=$images/14.gif></div></td>
    <td><div align=center>头像15<br><img src=$images/15.gif></div></td>
  </tr>
  <tr bgcolor=$lybgcolor>
    <td><div align=center>头像16<br><img src=$images/16.gif></div></td>
    <td><div align=center>头像17<br><img src=$images/17.gif></div></td>
    <td><div align=center>头像18<br><img src=$images/18.gif></div></td>
    <td><div align=center>头像19<br><img src=$images/19.gif></div></td>
    <td><div align=center>头像20<br><img src=$images/20.gif></div></td>
  </tr>
  <tr bgcolor=$btbgcolor>
    <td colspan=5><div align=center><font color=$btfont>头像共 20 个 共 [1] 页</font></div></td>
  </tr>
</table>
</td></tr></table>
</body>
</head>
</html>
);
sub mypath{
local
$temp;
$temp=__FILE__;
$temp=~ s/\\/\//g if ($temp=~/\\/);
if ($temp) {$mypath=substr($temp,0,rindex($temp,"/"));}
else{
$mypath=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
$mypath=~ s/\\/\//g;}
return
$mypath;
}