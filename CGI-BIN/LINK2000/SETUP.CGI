#------------------------------------------------------#
#                 ������ΪYuzi�������ṩ               #
#              Yuzi��������2000���û���v1.20           #
#                                                      #
#     �������Ȩ��Yuzi���������У��κ��˽Կ�����       #
#     ʹ�ñ������ڷ���ҵ��;����ҵ��;���븶����       #
#     ���500Ԫ��                                      #
#                                                      #
#                    лл��ʹ�ñ����򡡡�yuzi          #
#                    E-mail: huangzhiyu@163.net        #
#                    http://www.yuzi.net	       #
#                                                      #
#     ������Ϊ��ѳ���������ʹ�ñ����򣬵�����       #
#     ����Yuzi������(http://www.yuzi.net)�����ӣ�      #
#------------------------------------------------------#
######################## �趨���� ########################
$admname      = "laotong";               # վ������
$delpsd       = "laotongwin918";              # վ������
$zynames      = "Ӯ������";             # ��ҳ����
$zyurl        = "http://www.win918.com";           # ��ҳ��ַ
$imagurl      = "http://laotong.533.net/link2000img"; # ͼƬλ��(���治Ҫ��"/")
$filepath     = ".";                     # CGI�����ļ��ľ���·��(���治Ҫ��"/")
$mailprg      = "/usr/sbin/sendmail -t"; # Server������������λ�� ͨ���ô�Ĭ��·��
$perpage      = "10";                    # ÿҳ��ʾ����Ϣ��
$time_hour    = "0";                     # Serverʱ��������Сʱ��
######################## �趨���� ########################
## ���²��ֲ����޸� ##
######################
$urlyuzi=&myurl;
$ym="$urlyuzi";
$yuzicgi="link.cgi";
$cginame="��������";
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