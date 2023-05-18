#------------------------------------------------------#
#                                                      #
#              本程序为 中国CGI之家 提供	           #
#              Ajie的留言板多用户版V4.0                #
#------------------------------------------------------#
##################################
sub gotopage{
$gotourl = $FORM{'gotourl'};
print <<EOF ;
<html>
<head>
<title>$title</title>
</head>
<body>
<meta HTTP-EQUIV="REFRESH" CONTENT="1;URL=$cgiurl/gbook.cgi?user=$user&page=$gotourl">
</body>
</html>
EOF
exit ;
}
########################################################
sub ipwhere {
    my $fromwhere = shift;
    my $datapath="$ipdir";
    (my $ip1,my $ip2,my $ip3,my $ip4)=split(/\./,$fromwhere);
    my $ips=$ip1*1000000000+$ip2*1000000+$ip3*1000+$ip4;
    $ip1=int($ip1);
    if (-f "$datapath/$ip1.txt") {
        $datafile=$datapath."/".$ip1.".txt";
    }
    else {
        $datafile=$datapath."/other.txt";
    }
    my $from1='';
    my $from2='';
    open(IPF,"$datafile");
    my @ipdata=<IPF>;
    close(IPF);
    for ($i=0;$i<@ipdata;$i++){
        ($ip1,$ip2,$from1,$from2)=split(/__/,$ipdata[$i]);
        (my $ipa1,my $ipa2,my $ipa3,my $ipa4)=split(/\./,$ip1);
        (my $ipb1,my $ipb2,my $ipb3,my $ipb4)=split(/\./,$ip2);
        my $ipbegin =$ipa1*1000000000+$ipa2*1000000+$ipa3*1000+$ipa4;
        my $ipend =$ipb1*1000000000+$ipb2*1000000+$ipb3*1000+$ipb4;
        if (($ips<=$ipend)&&($ips>=$ipbegin)) {
            last;
        }
    }
    if ($from1 eq "") { $fromwhere="未知地区"; }
    else {$fromwhere="$from1$from2";}
    return $fromwhere;
}
#############
sub mailadmin
  {
   $texti       =~ s/&nbsp;/ /g;
   $textireturn =~ s/&nbsp;/ /g;
   if ($sendusermail eq "YES")
   {
    if ($email ne "保密")
    {
   open (MAIL, "|$mailprog $email");
   print MAIL "Reply-to:\n";
   print MAIL "Cc: softwt\@21cn.com\n";
   print MAIL "From: $ajiegbmail\n";
   print MAIL "Subject: 谢谢您在$title的留言\n\n";
   print MAIL "尊敬的$name您好,非常感谢您在$title的留言。 \n";
   print MAIL "------------------------------------------------------\n";
   print MAIL "您的主页地址是: $url\n";
   print MAIL "您的IP地址是  : $ipaddress\n";
   print MAIL "您的地址是  : $fromwhere\n";
   print MAIL "您留言的时间是: $date_time\n";
   print MAIL "以下是您的留言:\n\n";
   print MAIL "    $texti\n\n";
   print MAIL "                                  欢迎再次光临本网站!!\n\n";
   print MAIL "                     $title    $ajiebookurl\n";
   print MAIL "                                  E-MAIL: $ajiegbmail\n";
   print MAIL "------------------------------------------------------\n";
   print OUTMAIL "免费留言本服务由 $home($homeurl) 提供　技术支持:中国CGI之家(http://www.homecgi.com)\n";
   close (MAIL);
     }
   }
  }
#############
sub checknull
  {
   if ($_[0] eq "")
     {
      &errorinput($_[1]);
     }
   else
     {
      if ($allow_html ==0)
        {
         $return=&filterhtml($_[0]);
        }
      else
        {
         $return=$_[0];
        }
     }
   return $return;
  }
#############
sub filterhtml
  {
   local($return)=$_[0];
   $return =~ s/<!--(.|\n)*-->//g;
   if ($allow_html == 0)
     {
      $return =~ s/<([^>]|\n)*>//g;
      $return =~ s/<//g;
     }
   return $return;
  }
#############
sub sendmail
{
open (MAIL, "|$mailprog $email");
if ($mailtoadmin eq "YES")
 {
  print MAIL "Reply-to: $adminmail\n";
 }
else
 {
  print MAIL "Reply-to:\n";
 }
print MAIL "From: $adminmail\n";
print MAIL "Subject: 留言本开通通知！\n\n";
print MAIL "尊敬的$name您好,非常感谢您申请了$home($homeurl)的留言本服务\n";
print MAIL "------------------------------------------------------\n";
print MAIL "您的用户名是    :$name\n";
print MAIL "您的管理密码是  :$pass\n";
print MAIL "您申请的版名是  :$title\n";
print MAIL "每页记录数      :$pagenum\n";
print MAIL "您EMAIL地址     :$email\n";
print MAIL "您的主页地址    :$url\n";
print MAIL "以下是您查看留言本应插入的HTML源代码:\n\n";
print MAIL "$cgiurl/gbook.cgi?user=$name\n";
print MAIL "以下是给您留言页面应插入的HTML源代码:\n\n";
print MAIL "$cgiurl/gbook.cgi?action=write&user=$name\n";
print MAIL "您可以通过您的账号修改您的留言本, 欢迎再次光临本网站!!\n";
print MAIL "请将本站加入到您的链接中, 不论是友情链接还是首页链接!!\n\n";
print MAIL "           有什么问题请E-MAIL给我: $adminmail\n";
print MAIL "------------------------------------------------------\n";
print MAIL "免费留言本服务由 $home($homeurl) 提供　技术支持:中国CGI之家(http://www.homecgi.com)\n";
close (MAIL);
}
##############################################
sub header{print "Content-type: text/html\n\n";}
##############################################
sub mailprogram
{
    $mailprogram='/usr/sbin/sendmail';
    if (!(-e $mailprogram)) {$mailprogram='/usr/bin/sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='/bin/sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='/lib/sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='/usr/slib/sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='sendmail';}
    if (!(-e $mailprogram)) {$mailprogram='/usr/lib/sendmail';};
    if (!(-e $mailprogram)) {$mailprogram='perlmail';};
    if (!(-e $mailprogram)) {$mailprogram="没有找到 Sendmail 路径，可能你的主机不支持";};
    return $mailprogram;
}
##############################################
sub admintitle {
     print qq(
    <html>
    <head>
    <title>留言本管理中心</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
    <style type="text/css">
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}

	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
    </style>
    <script language="javascript">
    function save_changes() {
    document.the_form.process.value="true";
    }
    function preview_template() {
    document.the_form.target="_blank";
    document.the_form.process.value="preview template";
    }
    </script>
    </head>
    <body bgcolor="#83C6C0" text="#336666" link="#336666" vlink="#333333" topmargin=5 leftmargin=15>
    <table width=100% cellpadding=0 cellspacing=1 border=0 height="300" bgcolor="#336666">
        <tr><td width=22% valign=top bgcolor=#ECF6F5>
            <table width=100% cellpadding=6 cellspacing=0 border=0>
              <tr>
                <td bgcolor="#73BAB4"><font face=宋体 color=#FFFFFF> <b>管理菜单</b>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5><font face=宋体 color=#336666> >> <a href="$cgiurl/admin.cgi">管理中心首页</a> << <br>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#DCECEA"><font face=宋体 color=#336666><b>留言本管理</b>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#ECF6F5"><font face=宋体 color=#336666> >> <a href="$cgiurl/admin.cgi?action=register">申请留言本</a><br> >> <a href="$cgiurl/admin.cgi?action=supervision">注册留言本管理</a>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#DCECEA"><font face=宋体 color=#336666><b>留言数据管理</b>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#ECF6F5"><font face=宋体 color=#336666>
                  >> 删除留言<br>
                  >> 清空留言<br>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#DCECEA"><font face=宋体 color=#336666><b>设置管理</b> </font></td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5><font face=宋体 color=#336666>>> <a href="./setvar.cgi">基本变量设置</a><br>
                  >> <a href="./setstyle.cgi">留言本风格设置</a><br>
                  >> <a href="./settemplate.cgi">编辑留言本模板</a>
                  </font></td>
              </tr>
              <tr><td bgcolor="#DCECEA"><font face=宋体 color=#336666><b>其它设置</b> </font></td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5><font face=宋体 color=#336666>
                  >> <a href="./loginlogs.cgi">管理区安全日志</a><br>
                  >> 留言本版本/更新<br>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor="#DCECEA"><font face=宋体 color=#336666><b>留言本 信息</b>
                  </font></td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5 align=left> <span class="large">版本：</span><span class="body">Ajie的留言本
                  V4.0 </span>
                  <p> <font face=宋体 color="#336666"> 中文版权所有： <a href="http://www.homecgi.com/" target=_blank>中国CGI之家</a><br>
                    技术支持论坛： <a href="http://www.homecgi.com/lb5000/leoboard.cgi" target="_blank">CGI技术论坛</a>
                    </font>
                </td>
              </tr>
            </table>
</td><td width=75% valign=top bgcolor=#ECF6F5>
    <table width=100% cellpadding=6 cellspacing=0 border=0>
);
}
##############################################
sub adminlogin {
    $current_time = localtime;
    print qq(
    <tr><td bgcolor="#73BAB4" colspan="2"><font face=宋体 color=#FFFFFF>
                <b>欢迎来到留言本管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#DCECEA valign=middle align=center colspan="2">
                <font face=宋体 color=#336666><b>管 理 员 登 陆</b></font>
                </td></tr>
                <tr><td bgcolor=#ECF6F5 colspan="2">
                </td>
                </tr>

                <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left colspan=2>
                <font face=宋体 color=#336666>
                <center><br>
                服务器时间：<b>$current_time</b><br>
                </center>
                <hr color=#DCECEA></tr>
             <form method="POST" action="$cgiurl/admin.cgi">
             <input type=hidden name="action" value="login">
              <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left width="39%">
                  <div align="right">版主账号：</div>
                </td>
                <td bgcolor=#ECF6F5 valign=middle align=left width="61%">&nbsp;
                  <input type=text name=adminname size=20>
                </td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left width="39%">
                  <div align="right">版主密码：</div>
                </td>
                <td bgcolor=#ECF6F5 valign=middle align=left width="61%">&nbsp;
                  <input type=password name=adminpass size=20>
                </td>
              </tr>
              <tr>
                <td bgcolor=#ECF6F5 valign=middle align=left colspan="2">
                  <div align="center"><font face=宋体 color=#336666>
                    <input type="submit" value="超级登陆">
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <input type="reset" value="重新来过" name="B1">
                    </font></div>
                </td>
              </tr>
              </form><tr>
                <td bgcolor=#ECF6F5 valign=middle align=left colspan="2">
                  <p><font face=宋体 color=#336666><font color=#336666 face=宋体>请注意<br>
                    只有论坛的坛主才能登陆论坛管理中心。<br>
                    未经过授权的尝试登陆行为将会被记录在案！</font></font></p>
                  <p>在进入论坛管理中心前，请确定你的浏览器打开了 Cookie 选项。<br>
                    Cookie 只会存在于当前的浏览器进程中。为了安全起见，当你关闭了浏览器后，Cookie 会失效并被自动删除。<br>
                  </p>
                  <p><font face=宋体 color=#336666>程序制作：<a href="mailto:webmaster\@homecgi.com">Ajie</a><br>
                    版权所有：<a href="http://www.homecgi.com">中国CGI之家</a></font>
                  </p>
               </td></tr></table></td></tr></table>
);
exit;}
##############################################
sub parseadminform {
if ($ENV{'REQUEST_METHOD'} eq "POST")
{read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'});}
else{$buffer=$ENV{'QUERY_STRING'};}
@pairs = split(/&/, $buffer);
   foreach $pair (@pairs) {
   ($name, $value) = split(/=/, $pair);
   $value =~ tr/+/ /;
   $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
   $value=~s/\t/--/g;
   $value=~s/\n/\<br\>/g;
   $value =~ s/<!--(.|\n)*-->//g;
   $value =~ s/<([^>]|\n)*>//g;
   $FORM{$name} = $value;
}
@querys = split(/&/, $ENV{'QUERY_STRING'});
foreach $query (@querys) {
($name, $value) = split(/=/, $query);
$FORM{$name} = $value;   }
}
#############
sub errorinput
  {&pagestyle;
print qq(
<html>
    <head>
    <title>错误信息</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
    </head>
    <body bgcolor="$gbbgcolor" $gbbody>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor>
            <div align="center"><font color=$btfont>错误信息</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
                <td width="30%" align="center">$_[0]<br></td>
              </tr>
        <tr><td bgcolor=$btbgcolor><div align="center">
<input type=button name=ok class=input2 value=' 返 回 ' onclick=javascript:history.go(-1)></div>
</td></tr></table>
</td></tr></table>
);
   exit;
  }
############################################
sub pagestyle{
   $templatefile = "$mypath/info/template.cgi";
   open (TEMPLATE, "$templatefile");
   local $/ = undef;
   $template_data = <TEMPLATE>;
   close (TEMPLATE);
$template_data =~ s/\&lt;/</g;
$template_data =~ s/\&gt;/>/g;
$template_data =~ s/ \&nbsp;/　/g;
$template_data =~ s/\&amp;/\&/g;
$pagestyle = qq($template_data);
return $pagestyle;
}
sub getdate{
($no,$no,$no,$day,$month,$year)= localtime(time);
$month++;
if($month <10){$month="0".$month;}
if($day<10){$day="0".$day;}
$year=$year+1900;
$date=$year."-".$month."-".$day;
}
sub gettime{
($sec,$min,$hour,$no,$no,$no)= localtime(time);
if($sec<10){$sec="0".$sec;}
if($min<10){$min="0".$min;}
if($hour<10){$hour="0".$hour;}
$time=$hour.":".$min.":".$sec;
}
######################################################
sub code {
    my $signature = shift;

	$signature =~ s/\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<img src=$1:\/\/$2 border=0>/isg;
    $signature =~ s/\<p>/<br><br>/isg;
    $signature =~ s|\[\[|\{\{|g;
    $signature =~ s|\]\]|\}\}|g;
    $signature =~ s|\n\[|\[|g;
    $signature =~ s|\]\n|\]|g;
    $signature =~ s|<br>| <br>|g;
    $signature =~ s|\[hr\]\n| |g;
    $signature =~ s|\[hr\]| |g;
    $signature =~ s/\[br\]/<br>/isg;
    $signature =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]/$1$2<br>$3<br>/isg;
    $signature =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]/$1/isg;
    $signature =~ s/\[url\](\[\S+\])(\S+?)(\[\S+\])\[\/url\]/<a href=$2 target=_blank>$1$2$3<\/a>/isg;
    $signature =~ s/\[url=(http|https|ftp):\/\/(\S+?)\]/<a href=$1:\/\/$2 target=_blank>/isg;
    $signature =~ s/\[url=(\S+?)\]/<a href=http:\/\/$1 target=_blank>/isg;
    $signature =~ s/\[url=\s*(.*?)\s*\]\s*(.*?)\s*\[\/url\]/<a href=$1 target=_blank>$2<\/a>/isg;
    $signature =~ s/\[url\]\s*(http|https|ftp):\/\/(.*?)\s*\[\/url\]/<a href=$1:\/\/$2 target=_blank>$1:\/\/$2<\/a>/isg;
    $signature =~ s/\[url\]\s*(.*?)\s*\[\/url\]/<a href=http:\/\/$1 target=_blank>$1<\/a>/isg;
    $signature =~ s/\[\/url\]/<\/a>/isg;
    $signature =~ s/(\[email\])(\S+\@\S+?)(\[\/email\])/<A HREF="mailto:$2">$2<\/A>/isg;
    $signature =~ s/\ (http|https|ftp):\/\/(\S+?)\ / <a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
    $signature =~ s/<br>(http|https|ftp):\/\/(\S+?)\ /<br><a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
    $signature =~ s/^(http|https|ftp|rtsp):\/\/(\S+?)\ /<a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
    $signature =~ s/\ www\.(\S+?)\ / <a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
    $signature =~ s/<br>www\.(\S+?)\ /<br><a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
    $signature =~ s/^www\.(\S+?)\ /<a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
    $signature =~ s/\[b\]/<b>/isg;
    $signature =~ s/\[\/b\]/<\/b>/isg;
    $signature =~ s/\[i\]/<i>/isg;
    $signature =~ s/\[\/i\]/<\/i>/isg;
    $signature =~ s/\[font=\s*(.*?)\s*\]\s*(.*?)\s*\[\/font\]/<font face=$1>$2<\/font>/isg;
    $signature =~ s/\[u\]/<u>/isg;
    $signature =~ s/\[\/u\]/<\/u>/isg;
    $signature =~ s/\[color=(\S+?)\]/<font color=$1>/isg;
    $signature =~ s/\[\/color\]/<\/font>/isg;
    $signature =~ s/\\(http|https|ftp):\/\/(\S+)/<a href=$1:\/\/$2 target=_blank>$1:\/\/$2<\/a>/isg;
    $signature =~ s/\[code\](.+?)\[\/code\]/$1/isg;
    $signature =~ s/\\(\S+?)\@(\S+)/<a href=mailto:$1\@$2\>$1\@$2<\/a>/ig;
    $signature =~ s/\[email=(\S+?)\]/<a href=mailto:$1>/isg;
    $signature =~ s/\[\/email\]/<\/a>/isg;
    $signature=~ s/<br>(\w+\@\w+\.\w+)/<br><A HREF=mailto:$1>$1<\/A>/isg;
    $signature =~ s/^(\w+\@\w+\.\w+)/<A HREF=mailto:$1>$1<\/A>/isg;
    $signature =~ s/\\(\w+\@\w+\.\w+)/<A HREF=mailto:$1>$1<\/A>/isg;
    $signature =~ s/(\[fly\])(.+?)(\[\/fly\])/<marquee width=90% behavior=alternate scrollamount=3>$2<\/marquee>/isg;
    $signature =~ s/(\[s\])(.+?)(\[\/s\])/<s>$2<\/s>/isg;
    $signature =~ s/(\[sup\])(.+?)(\[\/sup\])/<sup>$2<\/sup>/isg;
    $signature =~ s/(\[sub\])(.+?)(\[\/sub\])/<sub>$2<\/sub>/isg;
    $signature =~ s/(\[align=)(left|center|right)(\])(.+?)(\[\/align\])/<DIV Align=$2>$4<\/DIV>/isg;
    $signature =~ s/(\[SHADOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/SHADOW\])/<table width=$2 style="filter:shadow\(color=$4\, direction=$6)">$8<\/table>/isg;
    $signature =~ s/(\[GLOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/GLOW\])/<table width=$2 style="filter:glow\(color=$4\, strength=$6)">$8<\/table>/isg;
    $signature =~ s/(\[BLUR=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/BLUR\])/<table width=$2 style="filter:blur\(Add=0, direction=$4\, strength=$6)">$8<\/table>/isg;
    $signature =~ s/(\[FLIPH\])(.+?)(\[\/FLIPH\])/<table style="filter:flipH">$2<\/table>/isg;
    $signature =~ s/(\[FLIPV\])(.+?)(\[\/FLIPV\])/<table style="filter:flipV">$2<\/table>/isg;
    $signature =~ s/(\[INVERT\])(.+?)(\[\/INVERT\])/<table style="filter:invert">$2<\/table>/isg;
    $signature =~ s/(\[xray\])(.+?)(\[\/xray\])/<table style="filter:xray">$2<\/table>/isg;
    $signature =~ s/(\[MOVE\])(.+?)(\[\/Move\])/<MARQUEE>$2<\/MARQUEE>/isg;

    $signature =~ s|\{\{|\[|g;
    $signature =~ s|\}\}|\]|g;
    $signature =~ s/\&amp;/\&/ig;
    $signature =~ s/&quot\;/\"/ig;
    $signature =~ s/ \&nbsp;/　/ig;
    $signature =~ s/apasswordcookie/apassword cookies/isg;
    $signature =~ s/adminpass/admin password/isg;
    $signature =~ s/document.cookie/documents .cookie/isg;
    $signature =~ s/file:\/\//文件\:\/\//isg;
    $signature =~ s/javascript/java script/isg;
    return $signature;
}
1;