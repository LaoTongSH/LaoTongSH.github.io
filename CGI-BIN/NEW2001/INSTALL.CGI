#!/usr/bin/perl
########################################################
########################################################
#            ������ΪYuzi������ ��֮�� �ṩ              #
#        Yuzi ����С��+վ��С�� 2001���û���v1.2         #
#                                                      #
#     �������Ȩ��Yuzi������ ��֮�� ���У��κ���          #
#     �Կ�����ʹ�ñ������ڷ���ҵ��;����ҵ��;��          #
#     �븶�������500Ԫ��                               #
#                                                      #
#                    лл��ʹ�ñ����򡡡���֮��          #
#                    E-mail: webmaster@popcgi.com      #
#                    http://www.yuzi.net	              #
#                                                      #
#     ������Ϊ��ѳ���������ʹ�ñ����򣬵�����          #
#     ����Yuzi������(http://www.yuzi.net)�����ӣ�       #
########################################################
$cgipa=".";  # CGI�����ļ��ľ���·��(NT�û���Ҫ���Ĵ���)
############### ���������벻Ҫ����޸� ##################
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
<html><head><title>��װ���</title>
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
��װ�Ѿ����<a href=new2001.cgi>��½</a>��
</center>
</body></html>
EOF
exit;