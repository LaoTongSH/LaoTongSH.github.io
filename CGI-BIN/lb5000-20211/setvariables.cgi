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
#            http://mail@17do.com/      大家一起邮
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
require "lbadmin.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setvariables.cgi";

$query = new LBCGI;
&ipbanned; #封杀一些 ip

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        	$theparam =~ s/"//g;
	        $theparam =~ s/'/\\\'/g;
        	$theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
        	$_ =~ s/[\n\r]//isg;
        	$theparam =~ s/[\n\r]//isg;
            $printme .= "\$" . "$_ = \'$theparam\'\;\n" if ($_ ne "");
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);
&admintitle;

&getmember("$inmembername");
        
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

    
    if ($action eq "process") {

        
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/boardinfo.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 变量结构</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>以下信息已经成功保存</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 变量设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=宋体 color=#333333><b>所有信息没有保存</b><br>文件或者目录不可写<br>请检测你的 data 目录和 boardinfo.cgi 文件的属性！
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 变量设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>论坛变量设置</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                ~;
                $tempoutput1 = "<select name=\"mainonoff\">\n<option value=\"0\">论坛开放\n<option value=\"1\">论坛关闭\n</select>\n";
                $tempoutput1 =~ s/value=\"$mainonoff\"/value=\"$mainonoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>论坛状态</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput1</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>维护说明</b> (支持 HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="line1" cols="40">$line1</textarea><BR><BR></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"regonoff\">\n<option value=\"0\">允许用户注册\n<option value=\"1\">不允许用户注册\n</select>\n";
                $tempoutput1 =~ s/value=\"$regonoff\"/value=\"$regonoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>是否允许用户注册</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput1<BR><BR></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333 ><b>不允许注册说明</b> (支持 HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="noregwhynot" cols="40">$noregwhynot</textarea><BR><BR></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boardname" value="$boardname"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛描述</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boarddescription" value="$boarddescription"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛 LOGO</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boardlogos" value="$boardlogos"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛 URL 地址</b><br>结尾不要加 "/"</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boardurl" value="$boardurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>主页名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="homename" value="$homename"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>版权信息</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛状态栏显示</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="statusbar" value="$statusbar"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>主页地址</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>图片目录 URL</b><br>在结尾不要加 "/images"</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="imagesurl" value="$imagesurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>图片绝对路径</b><br>结尾加 "/"</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="imagesdir" value="$imagesdir"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>程序绝对路径</b><br>结尾加 "/"</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="lbdir" value="$lbdir"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emoticons\">\n<option value=\"off\">不使用\n<option value=\"on\">使用\n</select>\n";
                $tempoutput =~ s/value=\"$emoticons\"/value=\"$emoticons\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否使用表情字符转换？</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"avatars\">\n<option value=\"off\">不使用\n<option value=\"on\">使用\n</select>\n";
                $tempoutput =~ s/value=\"$avatars\"/value=\"$avatars\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否使用个性图片</b><br>使用个性化图片，每个用户将拥有有自己特色的头像。</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>短消息功能</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"allowusemsg\">\n<option value=\"on\">使用\n<option value=\"off\">不使用\n</select>";
                $tempoutput =~ s/value=\"$allowusemsg\"/value=\"$allowusemsg\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否开启论坛短消息功能？</b><br>开启短消息功能，可使您及您的会员便于互相沟通。</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>短消息收件箱消息条数限制</font></b><br>如不限制，请留空</td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="maxmsgno" value="$maxmsgno" maxlength=3> 此功能对版主和坛主无效</td>
                </tr>                

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>邮件功能</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emailfunctions\">\n<option value=\"off\">不使用\n<option value=\"on\">使用\n</select>\n";
                $tempoutput =~ s/value=\"$emailfunctions\"/value=\"$emailfunctions\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否使用邮件功能？</b><br>推荐你使用</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"emailtype\">\n<option value=\"smtp_mail\">SMTP\n<option value=\"esmtp_mail\">ESMTP\n<option value=\"send_mail\">Sendmail\n<option value=\"blat_mail\">Blat\n</select>\n";
                $tempoutput =~ s/value=\"$emailtype\"/value=\"$emailtype\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>请选择一个可以使用的邮件协议</b><br>推荐使用 SMTP，可以同时在 NT 和 UNIX 下使用。而 SENDMAIL 只能在 UNIX 中用，Blat 只能在 NT 中用。</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>发送邮件程序位置</b><br>如果您使用的不是 Sendmail，请不要填写</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SEND_MAIL" value="$SEND_MAIL"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>SMTP 的位置</b><br>如果您使用的不是 SMTP，请不要填写，一般填写你 ISP 提供的发信服务器地址</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SMTP_SERVER" value="$SMTP_SERVER"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>SMTP 的端口</b><br>如果您使用的不是 SMTP，请不要填写，默认为 25</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=6 name="SMTP_PORT" value="$SMTP_PORT" maxlength=6></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>ESMTP 的用户名</b><br>如果您使用的不是 ESMTP，请不要填写</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SMTPUSER" value="$SMTPUSER"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>ESMTP 的密码</b><br>如果您使用的不是 ESMTP，请不要填写</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SMTPPASS" value="$SMTPPASS"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>坛主接收邮件使用的信箱</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adminemail_in" value="$adminemail_in"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>坛主发送邮件使用的信箱</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adminemail_out" value="$adminemail_out"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"passwordverification\">\n<option value=\"no\">否\n<option value=\"yes\">是\n</select>\n";
                $tempoutput =~ s/value=\"$passwordverification\"/value=\"$passwordverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否用邮件通知用户密码？</b><br>建议不使用。若要使用，请确定打开了上面的“是否使用邮件功能？”，并保证你发送邮件是没有问题的。</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"adminverification\">\n<option value=\"no\">否\n<option value=\"yes\">是\n</select>\n";
                $tempoutput =~ s/value=\"$adminverification\"/value=\"$adminverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>新用户注册，是否必须管理员认证？</b><br>建议不使用。若要使用，1,请确定打开了上面的“是否使用邮件功能？”，并保证你发送邮件是没有问题的。2,确认已经打开上面的邮件通知用户密码!</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"newusernotify\">\n<option value=\"no\">否\n<option value=\"yes\">是\n</select>\n";
                $tempoutput =~ s/value=\"$newusernotify\"/value=\"$newusernotify\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>有新用户注册是否用邮件通知您？</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"oneaccountperemail\">\n<option value=\"no\">否\n<option value=\"yes\">是\n</select>\n";
                $tempoutput =~ s/value=\"$oneaccountperemail\"/value=\"$oneaccountperemail\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>一个 Email 只能注册一个账号？</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~; 

               $tempoutput = "<select name=\"usertype\">\n<option value=\"1\">一般用户\n<option value=\"0\">认证用户\n</select>\n"; 
               $tempoutput =~ s/value=\"$usertype\"/value=\"$usertype\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=宋体 color=#333333><b>默认用户类型</b><br>设定默认用户的类型。如果选择认证用户，那么只有认证用户的社区参数才会累加；如果选择一般用户，那么所有的注册用户都会累加。</font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>广告选项</b>
                </font></td>
                </tr>
                    
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页广告</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="adscript" cols="40">$adscript</textarea>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页尾部代码</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="adfoot" rows="5" cols="40">$adfoot</textarea><BR><BR>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useimagead\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimagead\"/value=\"$useimagead\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=宋体 color=#333333><b>是否使用论坛首页浮动广告</b></font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页浮动广告图片 URL</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页浮动广告连接目标网址</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adimagelink" value="$adimagelink"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页浮动广告图片宽度</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="adimagewidth" value="$adimagewidth" maxlength=3>&nbsp;像素</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页浮动广告图片高度</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="adimageheight" value="$adimageheight" maxlength=3>&nbsp;像素</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum\"/value=\"$useimageadforum\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=宋体 color=#333333><b>分论坛是否使用此浮动广告</b><BR>如果分论坛有自定义的浮动广告，<BR>那么此选项无效</font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput<BR><BR></td> 
               </tr>
		~;
               
               $tempoutput = "<select name=\"useimagead1\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimagead1\"/value=\"$useimagead1\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=宋体 color=#333333><b>是否使用论坛首页右下固定广告</b></font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页右下固定广告图片 URL</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adimage1" value="$adimage1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页右下固定广告连接目标网址</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adimagelink1" value="$adimagelink1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页右下固定广告图片宽度</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="adimagewidth1" value="$adimagewidth1" maxlength=3>&nbsp;像素</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛首页右下固定广告图片高度</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="adimageheight1" value="$adimageheight1" maxlength=3>&nbsp;像素</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum1\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum1\"/value=\"$useimageadforum1\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF valign=middle align=left width=40%> 
               <font face=宋体 color=#333333><b>分论坛是否使用此右下固定广告</b><BR>如果分论坛有自定义的右下固定广告，<BR>那么此选项无效</font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>其他选项</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>支持上传的附件类型</b><br>用,分割</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="addtype" value="$addtype"></td>
                </tr>
                
                ~;
                $tempoutput = "<select name=\"OS_USED\">\n<option value=\"Nt\">Windows 系列\n<option value=\"Unix\">Unix 系列\n<option value=\"No\">不加锁\n</select>\n";
                $tempoutput =~ s/value=\"$OS_USED\"/value=\"$OS_USED\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>请选择操作系统平台用于文件加锁</b><BR>请千万不要选错，如果你不能确定，请选择 Windows 系列！！<BR>文件加锁可以有效的防止贴子数据丢失等问题，但会影响速度，请自己衡量！<br></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"floodcontrol\">\n<option value=\"off\">否\n<option value=\"on\">是\n</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否灌水预防机制？</b><br>强烈推荐使用</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>用户发贴的相隔时间</b><br>灌水预防机制不会影响到坛主或版主</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=5 name="floodcontrollimit" value="$floodcontrollimit" maxlength=4> 秒 (一般设置 30 左右)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>同 IP 的注册最小相隔时间</b><br>可以有效防止灌水注册机</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=5 name="regcontrollimit" value="$regcontrollimit" maxlength=4> 秒 (一般设置 30 左右)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛允许的最大在线人数</b><br>可以控制服务器的资源使用</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=6 name="arrowonlinemax" value="$arrowonlinemax" maxlength=5> 人 (一般设 50 左右，若不想限制，则设置 99999)</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"timezone\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
                $tempoutput =~ s/value=\"$timezone\"/value=\"$timezone\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>服务器时差</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>所在的时区</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="basetimes" value="$basetimes"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>引用最多多少字符？</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="maxquotenum" value="$maxquotenum" maxlength=4> 默认: 200</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>用户威望最大多少？</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="maxweiwang" value="$maxweiwang" maxlength=3> 默认: 10(不能小于5)</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>在多少区发送相同贴子就查封？</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="maxadpost" value="$maxadpost" maxlength=3> 默认: 4(不能小于3)，如果要取消，请设置 999</td>
                </tr>
                ~;
		
		$tempoutput = "<select name=\"coolwin\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n";
		$tempoutput =~ s/value=\"$coolwin\"/value=\"$coolwin\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>
		<font face=宋体 color=#333333><b>是否使用LB5000风格的弹出窗口</b><br>只有IE5.5支持，使用多线程浏览器（如魔装网神）将会报错。对部分弹出窗口有效。</font></td>
		<td bgcolor=#FFFFFF valign=middle align=left>
		$tempoutput</td>
		</tr>
		~;
		
		$tempoutput = "<select name=\"oicqshow\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n";
		$tempoutput =~ s/value=\"$oicqshow\"/value=\"$oicqshow\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>
		<font face=宋体 color=#333333><b>是否使用OICQ在线显示（占用相对多的服务器资源)。</font></td>
		<td bgcolor=#FFFFFF valign=middle align=left>
		$tempoutput</td>
		</tr>
		~;

		$tempoutput = "<select name=\"cpudisp\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n";
		$tempoutput =~ s/value=\"$cpudisp\"/value=\"$cpudisp\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>
		<font face=宋体 color=#333333><b>是否显示论坛CPU占用时间(只对 Unix 类主机有效)。</font></td>
		<td bgcolor=#FFFFFF valign=middle align=left>
		$tempoutput</td>
		</tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>显示论坛 CPU 占用时间的字体颜色</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=8 maxlength=7 name="cpudispcolor" value="$cpudispcolor"> 默认：#c0c0c0</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"useemote\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
                $tempoutput =~ s/value=\"$useemote\"/value=\"$useemote\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否使用 EMOTE 标签</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"announcements\">\n<option value=\"no\">不使用\n<option value=\"yes\">使用\n</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否使用公告论坛</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"sticky\">\n<option value=\"off\">正常顺序，新的放在最后\n<option value=\"on\">紧跟主题，新的放在最上面\n</select>\n";
                $tempoutput =~ s/value=\"$sticky\"/value=\"$sticky\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>查看贴子回复的时候，最新的回复是紧跟主题呢？还是放在最后！</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"refreshurl\">\n<option value=\"0\">自动返回当前论坛\n<option value=\"1\">自动返回当前贴子\n</select>\n";
                $tempoutput =~ s/value=\"$refreshurl\"/value=\"$refreshurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>发表、回复贴子后自动转移到？</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"defaulttopicshow\">\n<option value=>查看所有的主题\n<option value=1>查看一天内的主题\n<option value=2>查看两天内的主题\n<option value=7>查看一星期内的主题\n<option value=15>查看半个月内的主题\n<option value=30>查看一个月内的主题\n<option value=60>查看两个月内的主题\n<option value=180>查看半年内的主题\n</select>\n";
                $tempoutput =~ s/value=\"$defaulttopicshow\"/value=\"$defaulttopicshow\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>默认显示主题数</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"defaulforumcshow\"><option value=\"orderlastpostd\">按最后回复时间降序<option value=\"orderlastposta\">按最后回复时间升序<option value=\"orderthreadd\">按主题发布时间降序<option value=\"orderthreada\">按主题发布时间升序<option value=\"orderstartbyd\">按主题发布人降序<option value=\"orderstartbya\">按主题发布人升序<option value=\"orderclickd\">按主题点击数降序<option value=\"orderclicka\">按主题点击数升序<option value=\"orderreplyd\">按主题回复数降序<option value=\"orderreplya\">按主题回复数升序<option value=\"ordertitled\">按主题标题降序<option value=\"ordertitlea\">按主题标题升序</select>\n";
                $tempoutput =~ s/value=\"$defaulforumcshow\"/value=\"$defaulforumcshow\" selected/; 
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>默认贴子排序方式</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>       
                ~;

                $tempoutput = "<select name=\"dispboardonline\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardonline\"/value=\"$dispboardonline\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否在首页显示分论坛详细在线情况</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"disphideboard\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$disphideboard\"/value=\"$disphideboard\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>跳转论坛栏中是否显示隐含论坛</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"dispboardsm\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardsm\"/value=\"$dispboardsm\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否在最下面显示论坛声明</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"dispborn\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispborn\"/value=\"$dispborn\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>首页是否显示当天生日用户</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"dispprofile\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$dispprofile\"/value=\"$dispprofile\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否允许客人察看用户资料</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"recordviewstat\">\n<option value=\"no\">不记录\n<option value=\"yes\">记录\n</select>\n";
                $tempoutput =~ s/value=\"$recordviewstat\"/value=\"$recordviewstat\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>是否记录论坛访问统计资料</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"openiframe\">\n<option value=\"no\">不允许\n<option value=\"yes\">允许\n</select>\n";
                $tempoutput =~ s/value=\"$openiframe\"/value=\"$openiframe\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛是否允许 Iframe 标签</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"showfastlogin\">\n<option value=\"top\">顶部\n<option value=\"bottom\">底部\n<option value=\"all\">都显示\n<option value=\"none\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$showfastlogin\"/value=\"$showfastlogin\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>论坛快速登陆显示位置</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"flashavatar\">\n<option value=\"no\">不支持\n<option value=\"yes\">支持\n</select>\n";
                $tempoutput =~ s/value=\"$flashavatar\"/value=\"$flashavatar\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>上传头像是否支持 FLASH 格式</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>上传头像文件允许的最大值(单位：KB)</b><br>默认允许最大 200KB ！</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text name="maxuploadava" value="$maxuploadava" size=5 maxlength=5>　不要加 KB，建议不要超过 200</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>论坛首页音乐名称</b>(如果没有请留空)<br>请输入背景音乐名称，背景音乐<BR>应上传于 non-cgi/midi 目录下。<br><b>不要包含 URL 地址或绝对路径！</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="midiaddr2" value="$midiaddr2">~;
                $midiabsaddr = "$imagesdir" . "midi/$midiaddr2";
                print qq~　<EMBED src="$imagesurl/midi/$midiaddr2" autostart="false" width=70 height=25 loop="true" align=absmiddle>~ if ((-e "$midiabsaddr")&&($midiaddr2 ne ""));
                print qq~
                </td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
                ~;
                
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;
