#------------------------------------------------------#
#                 本程序为Yuzi工作室提供               #
#              Yuzi友情连接2000多用户版v1.20           #
#                                                      #
#     本程序版权归Yuzi工作室所有！任何人皆可自由       #
#     使用本程序于非商业用途，商业用途必须付费人       #
#     民币500元！                                      #
#                                                      #
#                    谢谢您使用本程序　　yuzi          #
#                    E-mail: huangzhiyu@163.net        #
#                    http://www.yuzi.net	       #
#                                                      #
#     本程序为免费程序，您可以使用本程序，但必须       #
#     保留Yuzi工作室(http://www.yuzi.net)的链接！      #
#------------------------------------------------------#
######################## 设定部分 ########################
$admname      = "laotong";               # 站长名字
$delpsd       = "laotongwin918";              # 站长密码
$zynames      = "赢家理财";             # 主页名称
$zyurl        = "http://www.win918.com";           # 主页地址
$imagurl      = "http://laotong.533.net/link2000img"; # 图片位置(后面不要加"/")
$filepath     = ".";                     # CGI程序文件的绝对路径(后面不要加"/")
$mailprg      = "/usr/sbin/sendmail -t"; # Server上送信软件的位置 通常用此默认路径
$perpage      = "10";                    # 每页显示的信息数
$time_hour    = "0";                     # Server时区调整，小时。
######################## 设定结束 ########################
## 以下部分不需修改 ##
######################
$urlyuzi=&myurl;
$ym="$urlyuzi";
$yuzicgi="link.cgi";
$cginame="友情连接";
$chklast="$filepath/data/chklast";
$list="$filepath/data/list";
sub errorview
{
print "Content-type: text/html\n\n";
print "<html><head></head><body><script>alert('$_[0]');history.back();</script></body></html>";
}
sub myurl
{
	local $myurl,$server_port;
	if ($ENV{'SERVER_PORT'} ne '80') { $server_port=$ENV{'SERVER_PORT'};}
	$fullcgiurl = "http://$ENV{'SERVER_NAME'}$server_port$ENV{'SCRIPT_NAME'}";
	$myurl=substr($fullcgiurl,0,rindex($fullcgiurl,"/"));
	return $myurl;
}
