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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                        # Unbuffer the output
$thisprog = "loginout.cgi";
$query = new LBCGI;
&ipbanned; #封杀一些 ip
$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/\/$//;

$inforum        = $query -> param('forum');
$inforum        = &stripMETA("$inforum");
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));

for ('inmembername','inpassword','action','threadages','CookieDate','myinfo','mess','onlineview','advpost','viewMode','nodispavatar','nodispsign','nodispphoto','freshtime','hidden','selectstyle','tanchumsg') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
}
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ($inmembername eq "") {
    $inmembername = "客人";
}
&getmember("$inmembername");
$memberfilename = $inmembername;
$memberfilename =~ s/ /\_/g;
$memberfilename =~ tr/A-Z/a-z/;
$filetotrash = "$lbdir". "$msgdir/main/$memberfilename" . "_mian.cgi";
&title;
$output .= qq~
  <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
    <tr>
        <td width=30% rowspan=2 valign=top><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td valign=top align=left><font face="$font" color=$fontcolormisc>
        <font face="$font" color=$fontcolormisc>
	　<img src="$imagesurl/images/closedfold.gif" border=0>　<a href="$forumsummaryprog">$boardname</a><br>
        　<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>　登陆/退出
        </td>
    </tr>
  </table>
  <p>
  <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
      <td>
      <table cellpadding=6 cellspacing=1 border=0 width=100%>
~;
if ($action eq "login") {

    if (($userregistered ne "no") && ($inpassword eq $password)) {

     &whosonline("$inmembername\t论坛登陆\tnone\t登陆论坛\t");

     my $filetoopen2 = "$lbdir" . "data/onlinedata.cgi";
     my $filetoopens = &lockfilename($filetoopen2);
     if (!(-e "$filetoopens.lck")) {
	my $ipaddresstemp1  = $ENV{'REMOTE_ADDR'};
	$ipaddresstemp = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ipaddresstemp = $ipaddresstemp1 if (($ipaddresstemp eq "")||($ipaddresstemp eq "unknown"));
	my $ipaddresstemp2 = $ENV{'HTTP_CLIENT_IP'};
	$ipaddresstemp = $ipaddresstemp2 if (($ipaddresstemp2 ne "")&&($ipaddresstemp2 ne "unknown"));
        &winlock($filetoopen2);
        open(FILE,">$filetoopen2");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $line (@onlinedata) {
                chomp $line;
                (my $savedusername, my $no) = split(/\t/, $line);
		print FILE "$line\n" if ($savedusername ne "客人($ipaddresstemp)");
        }
        close(FILE);
        &winunlock($filetoopen2);
     }

	if ($inforum eq "") {
            $refrashurl = $forumsummaryprog;
	}
    	else {
	    $refrashurl = $forumsprog."?forum=$inforum";
	}
	$output .= qq~
	<tr>
	<td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>感谢你登陆 $inmembername</b></font></td></tr>
	<tr>
	<td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
	具体情况：
	<ul>
	<li><a href="$refrashurl">进入论坛</a>
	<meta http-equiv="refresh" content="3; url=$refrashurl">
	</ul>
	</tr></td>
	</table></td></tr></table>~;

       if ($myinfo==1) {
           if (length($mess) == 0) {$mess = "对不起，我现在很忙，请您稍后再联系我。";}
           else { $mess =~ s/[\a\f\n\e\0\r\t\`\~\!\@\$\%\^\&\*\=\+\\\'\:\"\/\<\>\?]//isg; }
       	   if (open(FILE,">$filetotrash")) {
       	     print FILE "$mess";
       	     close(FILE);
       	   }
       }
       else {
           unlink "$filetotrash" if (-e "$filetotrash");
       }

	$namecookie = cookie(-name    =>"amembernamecookie",
                         -value   =>   "$inmembername",
			 -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
    	$passcookie = cookie(-name    =>"apasswordcookie",
                         -value   =>   "$inpassword",
			 -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
       $onlineviewcookie = cookie(-name    =>   "onlineview",
                         -value   =>   "$onlineview",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
	   $advpostcookie = cookie(-name    =>   "advpost",
                        -values   =>   "$advpost",
                        -path    =>   "$cookiepath/",
                        -expires =>   "$CookieDate");
       $threadcookie = cookie(-name    =>   "threadages",
                        -value   =>   "$threadages",
                        -path    =>   "$cookiepath/",
                        -expires =>   "$CookieDate");
       $viewcookie = cookie(-name    =>   "viewMode",
                         -value   =>   "$viewMode",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
       $nodisp     = cookie(-name    =>   "nodisp",
                         -value   =>   "$nodispavatar|$nodispsign|$nodispphoto",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
       $freshtimecookie = cookie(-name    =>   "freshtime",
		    	 -value   =>   "$freshtime",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
       $selectstylecookie = cookie(-name    =>   "selectstyle",
		    	 -value   =>   "$selectstyle",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
	$tanchumsgcookie = cookie(-name    =>   "tanchumsg",
		    	 -value   =>   "$tanchumsg",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");

    	print header(-cookie=>[$onlineviewcookie,$advpostcookie,$threadcookie,$viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie, $namecookie,$passcookie], -charset=>gb2312);
    }
    else {
	print header(-charset=>gb2312);
	$output .= qq~
	<tr><td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>登陆错误</b></font></td></tr>
	<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
	登陆错误的可能原因：
	<ul>
	<li>密码错误<li>用户名错误<li>您不是<a href=$registerprog>注册</a>用户
	</ul>
	</tr></td>
	</table></td></tr></table>
	~;
    }
}
elsif ($action eq "logout") {
   $filetoopen = "$lbdir" . "data/onlinedata.cgi";
   my $filetoopens = &lockfilename($filetoopen);
   if (!(-e "$filetoopens.lck")) {
      &winlock($filetoopen);
      open(FILE,"$filetoopen");
      flock(FILE, 1) if ($OS_USED eq "Unix");
      @onlinedata = <FILE>;
      close(FILE);
      $onlinedata = @onlinedata;
      if ($onlinedata > 0) {
        open(ONLINEFILE,">$filetoopen");
        flock(ONLINEFILE, 2) if ($OS_USED eq "Unix");
        foreach $line (@onlinedata) {
            chomp $line;
            ($savedusername, my $no) = split(/\t/, $line);
			if (lc($savedusername) ne lc($inmembername)) {
		    	print ONLINEFILE "$line\n";
			}
			else {
        	    &uplogintime("$savedusername","")
			}
        }
        close(ONLINEFILE);
      }
      else { unlink("$filetoopen") if ($onlinedata eq 0); }
      &winunlock($filetoopen);
   }
   unlink "$filetotrash" if (-e "$filetotrash");
	$output .= qq~
	<tr><td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>您现在已经退出论坛</b></font></td></tr>
	<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
	具体选项：
	<ul>
	<li><a href="$forumsummaryprog">返回论坛</a>
	<li><a href=javascript:close();>关闭您的浏览器</a>
	</ul>
	</tr>
	</td>
	</table></td></tr></table>
	~;

        $namecookie = cookie(-name    =>   "amembernamecookie",
			     -path    =>   "$cookiepath/",
                             -value   =>   "");
	$passcookie = cookie(-name    =>   "apasswordcookie",
                             -value   =>   "",
			     -path    =>   "$cookiepath/",
                             -expires =>   "");
        $trashcookie = cookie(-name    =>   "templastvisit",
			      -path    =>   "$cookiepath/",
                              -value   =>   "");

        $threadages = cookie(-name    =>   "threadages",
			      -path    =>   "$cookiepath/",
                              -value   =>   "");
        $onlineviewcookie= cookie(-name    =>   "onlineview",
                      	      -value   =>   "",
                              -path    =>   "$cookiepath/");
	    $advpostcookie= cookie(-name    =>   "advpost",
                           -values   =>   "",
                             -path    =>   "$cookiepath/");
        $viewcookie = cookie(-name    =>   "viewMode",
                       -value   =>   "",
                       -path    =>   "$cookiepath/");
        $nodisp = cookie(-name    =>   "nodisp",
                       -value   =>   "",
                       -path    =>   "$cookiepath/");
       $freshtimecookie = cookie(-name    =>   "freshtime",
		    	 -value   =>   "",
                         -path    =>   "$cookiepath/");
       $selectstylecookie = cookie(-name    =>   "$selectstyle",
		    	 -value   =>   "",
                         -path    =>   "$cookiepath/");
       $tanchumsgcookie = cookie(-name    =>   "$tanchumsg",
		    	 -value   =>   "",
                         -path    =>   "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie, $trashcookie,$threadages,$onlineviewcookie,$advpostcookie,$viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie], -charset=>gb2312);
}
else {
if ($defaulttopicshow ne "") { $inthreadages = $defaulttopicshow; }
if ($query->cookie("threadages")) { $inthreadages = $query->cookie("threadages"); }
if ($query->cookie("selectstyle")) { $inselectstyle = $query->cookie("selectstyle"); }
if ($query->cookie("viewMode") ne ""){
$checked ="checked";
$checked1 ="";
}else{
$checked1 ="checked" ;
$checked ="" ;
}
if ($query->cookie("tanchumsg") eq ""){
$tcchecked ="checked";
$tcchecked1 ="";
}else{
$tcchecked1 ="checked" ;
$tcchecked ="" ;
}
if (($query->cookie("onlineview") == 1)||($query->cookie("onlineview") eq "")){
$online ="checked";
$online1 ="";
}else{
$online1 ="checked";
$online ="";
}
if (($query->cookie("advpost") == 1)||($query->cookie("advpost") eq "")){
$aadvpost ="checked";
$aadvpost1 ="";
}else{
$aadvpost1 ="checked";
$aadvpost ="";
}

$nodisp = $query->cookie("nodisp");
($nodispavatar, $nodispsign, $nodispphoto)  = split(/\|/,$nodisp);

if ($nodispavatar eq "yes"){
$checked2 ="checked" ;
}
if ($nodispsign eq "yes"){
$checked3 ="checked" ;
}
if ($nodispphoto eq "yes"){
$checked4 ="checked" ;
}

    print header(-charset=>gb2312);
    $inmembername =~ s/\_/ /g;

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t论坛登陆\tnone\t登陆论坛\t");
}

        $dirtoopen = "$lbdir" . "data/skin";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);
        my $myskin="";
        @thd = grep(/\.cgi$/,@dirdata);
        $topiccount = @thd;
        @thd=sort @thd;
        for (my $i=0;$i<$topiccount;$i++){
       	$thd[$i]=~s /\.cgi//isg;
        $myskin.=qq~<option value="$thd[$i]">[ $thd[$i] ]</option>~;
        }

    $output .= qq~
    <tr>
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="login">
    <input type=hidden name="forum" value="$inforum">
    <font face="$font" color=$fontcolormisc><b>请输入您的用户名、密码登陆</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的用户名</font></td>
    <td bgcolor=$miscbackone valign=middle><input type=text name="inmembername" value="$inmembername"> &nbsp; <a href="$registerprog"><font face="$font" color=$fontcolormisc>您没有注册？</font></a></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>请输入您的密码</font></td>
    <td bgcolor=$miscbackone valign=middle><input type=password name="inpassword" value="$inpassword"> &nbsp; <font face="$font" color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
    <tr>
    <td bgcolor=$miscbacktwo colspan=2 valign=middle><font face="$font" color=$fontcolormisc><b>论坛登陆选项</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>论坛隐身</b> 请选择你的登陆显示方式，可以适当保密你的隐私。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="hidden" value="0" checked id=1> <label for=1>正常登陆，显示在在线会员列表中</label><br>
                <input type="radio" name="hidden" value="1" id=2> <label for=2>隐身登陆，不要把我显示在在线列表中</label><br>
                </font>
                </td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>Cookie 选项</b><BR> 请选择你的 Cookie 保存时间，下次访问可以方便输入。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="CookieDate" value="-1d" checked id=3> <label for=3>不保存，关闭浏览器就失效</label><br>
                <input type="radio" name="CookieDate" value="+1d" id=4> <label for=4>保存一天</label><br>
                <input type="radio" name="CookieDate" value="+30d" id=5> <label for=5>保存一月</label><br>
                <input type="radio" name="CookieDate" value="+20y" id=6> <label for=6>永久保存</label><br>
                </font>
                </td></tr>
<tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>短消息选项</b><br> 请选择你登陆后是否接收短消息，避免被打扰。<BR>免打扰模式打开后，只有退出或重登陆才能解除</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="myinfo" value="0" checked onclick=h_display(mess),mess.value="" id=7> <label for=7>允许接收短消息</label><br>
                <input type="radio" name="myinfo" value="1" onclick=n_display(mess),mess.value="对不起，我现在很忙，请您稍后再联系我。" id=8> <label for=8>免打扰模式</label>　<input type="text" name="mess" size=40 maxlength=40 id=mess style="DISPLAY: none">
                </font>
                </td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>在线列表</b> 请选择你的在线名单显示方式，可以加快论坛显示。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="onlineview" value="1" $online id=9> <label for=9>显示详细名单</label><br>
                <input type="radio" name="onlineview" value="0" $online1 id=10> <label for=10>关闭详细名单</label><br>
                </font>
                </td></tr>
<tr>
   <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>默认发帖方式</b> 请选择你发帖时显示的方式。</font></td>
   <td bgcolor=$miscbackone valign=middle><font class='misc'>
               <input type="radio" name="advpost" values="1" $aadvpost id=18> <label for=18>高级模式</label><br>
               <input type="radio" name="advpost" values="0" $aadvpost1 id=19> <label for=19>简单模式</label><br>
               </font>
               </td></tr>      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>查看主题</b> 请选择你喜好查看主题的多少，可以加快论坛显示。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
        <select name="threadages">
        <option value="all">查看所有的主题</option>
        <option value="1">查看一天内的主题</option>
        <option value="2">查看两天内的主题</option>
        <option value="7">查看一星期内的主题</option>
        <option value="15">查看半个月内的主题</option>
        <option value="30">查看一个月内的主题</option>
        <option value="61">查看两个月内的主题</option>
        <option value="182">查看半年内的主题</option>
        <option value="365">查看一年内的主题</option>
        </select>
                </font>
                </td></tr>
      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>查看贴子</b> 请选择你喜好的查看贴子方式，可以方便阅读。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="viewMode" value="" $checked1 id=11> <label for=11>在原窗口中浏览</label><br>
                <input type="radio" name="viewMode" value="_blank" $checked id=12> <label for=12>在新窗口中浏览</label><br>
                </font>
                </td></tr>

      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>查看贴子内容</b> 请选择查看贴子内容时候是否显示用户头像、签名和贴图。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="checkbox" name="nodispavatar" value="yes" $checked2 id=13> <label for=13>不显示用户头像</label><br>
                <input type="checkbox" name="nodispsign"   value="yes" $checked3 id=14> <label for=14>不显示用户签名</label><br>
                <input type="checkbox" name="nodispphoto"  value="yes" $checked4 id=15> <label for=15>不显示用户贴图</label><br>
                </font>
                </td></tr>
		   <tr>
~;
if ($showskin ne "off") {$output.=qq~
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>风格设定</b> 请选择你的论坛风格。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
		  <select name="selectstyle">
        <option value="">默认风格</option>
	$myskin
        </select>
        </font>
        </td></tr>
~;}
$output.=qq~
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>有短消息是否弹出？</b> <BR>（如果管理员设置了不弹出则此选择无效）</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" class=1 name="tanchumsg" value="" $tcchecked id=16> <label for=16>弹出短消息窗口</label><br>
                <input type="radio" class=1 name="tanchumsg" value="no" $tcchecked1 id=17> <label for=17>不弹出短消息窗口</label><br>
                </font></td></tr>

<tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>页面自动刷新时间</b> <BR>请输入分论坛首页自动刷新的时间（不输入则按照分论坛的默认设置进行刷新或者不刷新）</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
每隔 <input type=text name="freshtime" value="$freshtime" maxlength="2" size="2"> 分钟自动刷新一次
<tr>
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="登 陆"></td></form></tr></table></td></tr></table>
    ~;
}

$output =~ s/option value=\"$inthreadages\"/option value=\"$inthreadages\" selected/;
$inselectstyle =~ s/\(/\\(/isg;
$inselectstyle =~ s/\)/\\)/isg;
$output =~ s/option value=\"$inselectstyle\"/option value=\"$inselectstyle\" selected/;
&output(
-Title   => "$boardname - 登陆/退出",
-ToPrint => $output,
-Version => $versionnumber
);
