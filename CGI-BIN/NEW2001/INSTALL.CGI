#!/usr/bin/perl
########################################################
########################################################
#            本程序为Yuzi工作室 梦之星 提供              #
#        Yuzi 更新小记+站长小记 2001多用户版v1.2         #
#                                                      #
#     本程序版权归Yuzi工作室 梦之星 所有！任何人          #
#     皆可自由使用本程序于非商业用途，商业用途必          #
#     须付费人民币500元！                               #
#                                                      #
#                    谢谢您使用本程序　　梦之星          #
#                    E-mail: webmaster@popcgi.com      #
#                    http://www.yuzi.net	              #
#                                                      #
#     本程序为免费程序，您可以使用本程序，但必须          #
#     保留Yuzi工作室(http://www.yuzi.net)的链接！       #
########################################################
$cgipa=".";  # CGI程序文件的绝对路径(NT用户才要更改此项)
############### 下面内容请不要随便修改 ##################
require "$cgipa/setup.cgi";
####################################
mkdir("$filepath/data",0777);
mkdir("$filepath/session",0777);
mkdir("$filepath/user",0777);
chmod(0777,"$filepath/data");
chmod(0777,"$filepath/session");
chmod(0777,"$filepath/user");
open(TMP,">$filepath/user/userdata.cgi");
print TMP "$adminname|$adminpass|$adminmail|$net_name|$net_url|||||||||||\n";
close(TMP);
chmod(0777,"$filepath/user/userdata.cgi");
chmod(0755,"$filepath/new2001.cgi");
chmod(0755,"$filepath/setup.cgi");
####################################
unlink("$cgipa/install.cgi");
print "Content-type: text/html\n\n";
print <<EOF;
<meta http-equiv=Content-Type content=text/html; charset=gb2312>
<html><head><title>安装完成</title>
<style type=text/css>
<!--
A:link    {text-decoration:none;color:#8000FF}
A:active  {TEXT-DECORATION:none;color:#F4F9FF}
A:visited {TEXT-DECORATION:none;color:#008000}
A:hover   {TEXT-DECORATION:underline overline;color:#FF0000}
p,br,body,td,select,input,form,textarea,option {font-size:9pt;color:#555555}
-->
</style>
</head><body bgColor=$bgcolor>
<br>
<br>
<center>
安装已经完成<a href=new2001.cgi>登陆</a>。
</center>
</body></html>
EOF
exit;
