************************************************************
*                                                          *
*         ★★★安装spboard/spnotice/spmem/必读★★★      *
*                  --=== 01世界汉化修改 ===--              *
*                    http://www.01-world.com               *
*                                                          *
************************************************************



一下以spboard为例说明，spnotice和spmemo与此类似。


#！c:/perl/bin/perl   
#这是perl解释器的位置，对于IIS+perl 5.x，这行没有用；
#对于apache服务器，无论win平台还是UNIX类平台，必须指定。
#####################################################################
$main_dir = "c:/apache/cgi-bin/spboard"; #这个是数据库所在目录的绝对路径
#对于apache服务器（无论是win平台还是unix类的），你可以使用.开头的表示法；
对于IIS服务器，必须给出完整的表示法；无论何种情况，完整的表示法都是正确的。
$main_url = "/cgi-bin/spboard";#数据库目录对应的URL；
#就是如果用浏览器调用数据库目录下的文件，要给出什么样的路径；
$cgi_url = "/cgi-bin/soboard/board.cgi";程序本身的url;
#也可以写为"./board.cgi";
$img_url = "/spboard/img";              #img图象目录的URL
因为大多服务器的CGI目录下不允许调用图象文件和html文件，所以要把它放在CGI目录之外；
$sendmail = "/usr/lib/sendmail"; #sendmail 程序位置
#####################################################################
要开板必须在数据库目录下建立一个目录，这个过程可以用FTP实现。
比如你预想要这样调用board.cgi
http://site.of.your/cgi-bin/spboard/board.cgi?id=myboard
那就必须事前在c:/apache/cgi-bin/spboard下建立一个myboard目录，
sp系列的缺省密码都是1234.
如果在操作中间出现错误，导致密码不认或发不了帖子，请把myboard目录删除重来一次。
如上设置你看了糊涂吗？下面给出目录树图：
c:/apache---cgi-bin--spboard--myboard
        |
        +-htdocs--spboard--img
说明：htdocs是我的非CGI目录的根；cgi-bin目录是我的有CGI权限目录。
如果你的站点不分CGI和非CGI，那就更简单了，不管什么葫芦搅茄子放一起就行了，不过这样有隐患，要注意安全问题。
还有对于UNIX类的平台，必须设置文件和目录的权限，.CGI要设成755;
建立的myboard目录要设成777
WIN平台不用管权限属性。

如果有问题请到我的论坛提出。
01世界论坛：http://www.01-world.com/cgi-bin/ubb/Ultimate.cgi
