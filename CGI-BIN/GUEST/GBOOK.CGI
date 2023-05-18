#!/usr/bin/perl
#------------------------------------------------------#
#                                                      #
#              本程序为 中国CGI之家 提供	           #
#              Ajie的留言板多用户版V4.0                #
#------------------------------------------------------#
&mypath;
require "$mypath/"."info/setup.cgi";
require "$mypath/"."info/style.cgi";
require "$mypath/"."sub.cgi";
require "$mypath/"."codejs.cgi";

$adminame      = "$admin";
$admipass      = "$password";
$page          = 1;
$online =1;
$action        = "show";
($sec,$min,$hour,$mday,$mon,$year)=localtime(time);
$mon           = $mon+1;
$year          = $year+1900;
($reply_date,$reply_time)=&date;
&pagestyle;
&parseadminform;
if ($user eq "")
   {
    $finduser = "";
    $user = $FORM{'user'};
    dbmopen (%CONF,"$userpath/alluser.db",0666);
    foreach (%CONF)
       {
        if ($_ =~ "‖$user‖")
           {
            ($mark,$name,$pass,$email,$url,$title,$pagenum,$ipaddress,$date_time,$markend,$last)=split(/‖/,$_);
            $ajiebookurl   = $url;
            $ajiegbmail  = $email;
            $adminame   = $name;
            $admipass   = $pass;
            $finduser = "YES";
           }
       }
    dbmclose(%CONF);
   }

print "Content-type: text/html\n\n";
if ($mainonoff eq "off") {
$line1 =~ s/\&lt;/</g;
$line1 =~ s/\&gt;/>/g;
$line1 =~ s/ \&nbsp;/　/g;
$line1 =~ s/\&amp;/\&/g;
print qq($line1);exit(0);}
if ($topgg ne "") {
$topgg =~ s/\&lt;/</g;
$topgg =~ s/\&gt;/>/g;
$topgg =~ s/ \&nbsp;/　/g;
$topgg =~ s/\&amp;/\&/g;
print qq(<center><TABLE border=0 cellSpacing=0 width=$tablewidth>
  <tr align=center>
    <td>$topgg</td></tr></table><br>);}
if ($FORM{'action'} ne ""){$action = $FORM{'action'};}
if ($FORM{'page'} ne ""){$page=$FORM{'page'};}
if ($action eq "search"){
$searchswitch  = "ON";
$searchcontent = $FORM{'search'};
&show;
exit(0)}
elsif ($action eq "add"){&add;exit;}
elsif ($action eq "show"){&show;exit;}
elsif ($action eq "del"){&del;exit;}
elsif ($action eq "delok"){&delok;exit;}
elsif ($action eq "write"){&write;exit;}
elsif ($action eq "replay"){&replay;exit;}
elsif ($action eq "gotopage"){&gotopage;exit;}
elsif ($action eq "replayok"){&replayok;exit;}
&show;
exit;
#############
sub date{
	my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
	$year+=1900;
	$mon++;
	my $date=sprintf("%4d-%02d-%02d",$year,$mon,$mday);
	my $htime=sprintf("%02d:%02d:%02d",$hour,$min,$sec);
	return ($date,$htime);
}
#############

sub show
  {
   dbmopen(%TEMP,"$datapath/$user.db",0666);
   %USERLIST = %TEMP;
   dbmclose(%TEMP);
   @userno=keys %USERLIST;
   @userno=sort @userno;
   $totalrecode = $#userno+1;
   print qq(

<BODY bgcolo=$gbbgcolor $gbbody>
$pagestyle
</head>
<center>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$tbcolor>
<tr><td>
<table width=100% cellspacing=0 cellpadding=4 border=0>
<tr><td bgcolor=$btbgcolor align=center>
<a href="$cgiurl/gbook.cgi?action=write&amp;user=$user"><font color=$btfont>[签写留言] </font></a>&nbsp;
<a href="$homeurl"><font color=$btfont>[返回首页]</font></a>&nbsp;
<a href="mailto:$ajiegbmail"><font color=$btfont>[版主信箱]</font></a>&nbsp;
<a href=$cgiurl/register.cgi><font color=$btfont>[免费申请]</font></a>&nbsp;
<a href="$cgiurl/register.cgi?action=modify&amp;user=$user" target="_blank"><font color=$btfont>[修改资料]</font></a>&nbsp;
<a href="$cgiurl/admin.cgi" target="_blank"><font color=$btfont>[超级管理]</font></a>&nbsp;
<a href="http://person.zj.cninfo.net/~laotong/guestbook/guestbook.html" target="_blank"><font color=$btfont>[老留言簿]</font></a>
</td>
</tr></table>
</td></tr></table>
  <p align="center">
);
if ($searchswitch ne "ON")
   {
    $temp = $totalrecode-($page)*$pagenum;
   }
else
   {
    $temp = 0;
    $searchtotal = 0;
    foreach (%USERLIST)
     {
      if ($_ =~ /$searchcontent/)
         {
          $searchtotal++;
         }
     }
   }

   if ($temp < 0) {$temp = 0};
   for ($inti = ($totalrecode-($page-1)*$pagenum-1);$inti >= $temp;$inti--)
     {
      $tmp=$userno[$inti];
      ($mark,$name,$email,$place,$photo,$texti,$url,$fromwhere,$date_time,$oicq,$posticons,$markend,$last)=split(/‖/,$USERLIST{$tmp});
      $recode = $inti+1;
      $photoimage = substr($photo,0,2);
      $photoname  = substr($photo,4,4);
      $photoimage = "$images/$photoimage.gif";
      $texti =~ s/&nbsp;/ /g;
      if ($searchswitch ne "ON")
         {
          &writegb;
         }
      else
         {
          if ($USERLIST{$tmp} =~ /$searchcontent/)
             {
              &writegb;
             }
         }
     }
   $tmp = $totalrecode / $pagenum;
   $tmp = int($tmp);
   $temp= $totalrecode % $pagenum;
   if ($temp != 0) {$tmp++;}
   if (($totalrecode == 0) || ($searchtotal == 0))
     {
      if ($searchswitch ne "ON")
         {
          if ($totalrecode == 0)
           {
            if ($finduser ne "YES")
              {
print qq(<center><table width=$tablewidth align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=0 cellpadding=4 border=0 height="100%"><tr>
          <td bgcolor=$guestbgcolor rowspan="4" width="25%" valign="top" align=center>
<table style="filter:glow(color=$guestnamegy,direction=135)">&nbsp;
<font color=$guestnamefont>Ajie</font><br></table><img src="$images/14.gif"><br><br>
            主页：<a href=http://www.homecgi.com target=_blank title=访问Ajie的主页>中国CGI之家</a><br>
            信箱：<a href=mailto:$myemail title=给Ajie写信>写信给我</a><br>
            OICQ：5858314</td>
          <td bgcolor=$lybgcolor align=center width="1" rowspan="4">
            <table width=1 height=100% cellpadding=0 cellspacing=0 bgcolor=#83c6c0>
              <tr>
                <td width=1></td>
              </tr>
            </table>
          </td>
          <td bgcolor=$lybgcolor width="75%">非常感谢您使用Ajie的留言本！
            <hr width=100% size=1 color=#336666>
          </td>
        </tr>
        <tr>
          <td bgcolor=$lybgcolor width="75%">
      ①.如果你刚第一次使用本留言本，请<a href=$cgiurl/gbook.cgi?action=register>点击这里申请新用户</a>！<br><br>
	  ②.如果申请后还是出现这个界面，请检查"管理中心"中的"基本变量设置"是否配置正确！<br><br>
	  ③.如果你已正常使用过本留言本后出现这个界面,请检查你的用户名是否正确或帐号被网管删除，请<a href=$cgiurl/gbook.cgi?action=register>点击这里重新申请</a>！<br></td>
        </tr>
        <tr>
          <td bgcolor=$lybgcolor width="75%">
            <hr width=100% size=1 color=$tbcolor="#336666";>
&nbsp;&nbsp;如果你还有任何不清楚的地方，请访问：
	  <a href=http://www.cgiubb.com target=_blank>[CGI技术论坛]</a>
</td></tr></table></td></tr></table>);
              }
            else
              {
               print qq(
<form method=POST action=$cgiurl/gbook.cgi?action=add&user=$user>
<table width=70% align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="3">
            <div align="center"><font color=$btfont>恭 喜 您 成 为 第 一 个 留 言 者 ！</font></div>
          </td>
        </tr>
        <tr>
          <td bgcolor=$guestbgcolor width="50%">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="24%">留言标题：</td>
                <td width="76%">&nbsp;
                  <input type="text" name="place" size="25" maxlength="50" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">您的名字：</td>
                <td width="76%">&nbsp;
                  <input type="text" name="name" size="25" maxlength="50" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">电子邮件：</td>
                <td width="76%">&nbsp;
                  <input type="text" name="email" size="25" maxlength="30" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">OICQ号码：</td>
                <td width="76%">&nbsp;
                  <input type="text" name="oicq" size="25" maxlength="50" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">主页地址： </td>
                <td width="76%">&nbsp;
                  <input type="text" name="url" size="25" maxlength="50" value="http://" class="input2">
                </td>
              </tr>
              <tr>
                <td width="24%">选择头像：</td>
                <td width="76%">&nbsp;&nbsp;<select name="photo">
				<option value=01 selected>头像01
				<option value=02>头像02
				<option value=03>头像03
				<option value=04>头像04
				<option value=04>头像05
				<option value=05>头像06
				<option value=07>头像07
				<option value=08>头像08
				<option value=09>头像09
				<option value=10>头像10
				<option value=11>头像11
				<option value=12>头像12
				<option value=13>头像13
				<option value=14>头像14
				<option value=15>头像15
				<option value=16>头像16
				<option value=17>头像17
				<option value=18>头像18
				<option value=19>头像19
				<option value=20>头像20
				</select>
                  <a href=$cgiurl/avatarslist.cgi target=_blank>查看头像列表</a></td>
              </tr>
            </table>
          </td>
          <td bgcolor=$guestbgcolor width="1">
            <table width=1 height=100% cellpadding=0 cellspacing=0 bgcolor=#83c6c0>
              <tr>
                <td width=1></td>
              </tr>
            </table>
          </td>
          <td bgcolor=$guestbgcolor width="50%">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td>
                  <div align="center">
				  <textarea rows="8" name="texti" cols="35" class="input3" wrap="PHYSICAL"></textarea>
				  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td bgcolor=$btbgcolor colspan="3">            <div align="center">
			<input type="submit" value="签写留言" name="B1" class="input2">&nbsp;&nbsp;&nbsp;&nbsp;
             <input type="reset" value="重新来过" name="B2" class="input2"></div></td>
        </tr>
      </table>
    </td></tr></table>

</form>
);
              }
           }
         }
      else
         {
          print qq(
<table width=$tablewidth align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor>
            <div align="center"><font color=$btfont>错误信息</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
                <td align="center">对不起，没有找到符合条件的记录!<br></td>
              </tr>
        <tr><td bgcolor=$btbgcolor><div align="center">
<input type=button name=ok class=input2 value=' 返 回 ' onclick=javascript:history.go(-1)></div>
</td></tr></table>
</td></tr></table>
);
         }
     }
$pageup = $page-1;
$pagedown = $page+1;
if ($page == 1){$output = qq~
<font color=$btfont>共 $tmp 页&nbsp;最前页&nbsp;上一页&nbsp;转第&nbsp;<input type="text" name="gotourl" size="2" class="input2" value=$page>&nbsp;页&nbsp;&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$pagedown><font color=$btfont>下一页</font></a>&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$tmp><font color=$btfont>最后页</font></a></font>
~;
}
elsif ($page == $tmp){$output = qq~
<font color=$btfont>共 $tmp 页&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=1><font color=$btfont>最前页</font></a>&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$pageup><font color=$btfont>上一页</font></a>&nbsp;转第&nbsp;<input type="text" name="gotourl" size="2" class="input2" value=$page>&nbsp;页&nbsp;下一页&nbsp;最后页</font>
~;
}
else {$output = qq~
<font color=$btfont>共 $tmp 页&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=1><font color=$btfont>最前页</font></a>&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$pageup><font color=$btfont>上一页</font></a>&nbsp;转第&nbsp;<input type="text" name="gotourl" size="2" class="input2" value=$page>&nbsp;页&nbsp;&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$pagedown><font color=$btfont>下一页</font></a>&nbsp;<a href = $cgiurl/gbook.cgi?user=$user&page=$tmp><font color=$btfont>最后页</font></a></font>
~;}

print qq(
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$tbcolor>
<tr><td>
<table width=100% cellspacing=0 cellpadding=4 border=0>
<tr><form method="POST" action="$cgiurl/gbook.cgi?action=search&user=$user&page=&$inti">
<td bgcolor=$btbgcolor align=center>
<font color=$btfont>关键字：</font><input name="search" size="20" class="input2">&nbsp;&nbsp;&nbsp;
<input name="B1" type="submit" value="搜索" class="input2">
</td></form><form method="post" action="$cgiurl/gbook.cgi?action=gotopage&user=$user">
<td bgcolor=$btbgcolor align=center>$output
</td></form>
</tr></table>
</td></tr></table>);
if ($downgg ne ""){
$downgg =~ s/\&lt;/</g;
$downgg =~ s/\&gt;/>/g;
$downgg =~ s/ \&nbsp;/　/g;
$downgg =~ s/\&amp;/\&/g;
print qq(
<TABLE border=0 cellSpacing=0 width=$tablewidth>
  <tr align=center>
    <td><br>$downgg</td></tr></table>);}
print qq(<TABLE border=0 cellSpacing=0 width=$tablewidth>
  <tr align=middle>
    <td><br>
    免费留言服务由<a target="_blank" href="$homeurl"> <b>$home</b> </a>提供 技术支持：<b>Ajie</b><br>
     <a target="_blank" href="http://www.homecgi.com">Ajie 的留言本 V4.0</a>  版权所有<script>
		var tc_user="homecgi";
		var tc_class="2";
		var tc_union="";
		var tc_type="1";
		_dw('<a href=http://www.textclick.com/viewmain.asp?name='+tc_user+' target=_blank><img WIDTH=0 EIGHT=0 src=http://ad.t2t2.com/scripts/stat.dll?default&user='+tc_user+'&refer='+escape(document.referrer)+'&cur=type2 border=0></a>');
		function _dw(string) {document.write(string);}
		</script>：<a href="http://www.homecgi.com" target="_blank"><b>中国CGI之家</b></a></p></td></tr></table>
);
}
#####################################################################
sub add
  {$writetoad=$FORM{'writetoad'};
   $qqtoad=$FORM{'qqtoad'};
   if (($qqtoad eq "on")&&($writetoad eq "on")){print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>不能同时选择[悄悄话]和[发送给版主]功能！</h2><br><input type=button name=ok class=input2 value=\"返 回\" onclick=javascript:history.go(-1)></div>";exit;}
   $name       = &checknull($FORM{'name'}   ,"名字不能为空!!");
   if (length($name)>20) {print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>名字不能超过10个字！</h2><br><input type=button name=ok class=input2 value=\"返 回\" onclick=javascript:history.go(-1)></div>";exit;}
   $email      = $FORM{'email'};
   if ($email eq ""){$email="不告诉你";}
   $place      = &checknull($FORM{'place'}  ,"标题不能为空!!");
if (length($place)>40) {print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>标题长度不得超过 20 个汉字</h2><br><input type=button name=ok class=input2 value=\"返 回\" onclick=javascript:history.go(-1)></div>";exit;}
   if ($place eq ""){$place="不告诉你";}
   $oicq      = $FORM{'oicq'};
   $posticon  = $FORM{'posticon'};
   $posticons = "$images/posticons/$posticon";
   if ($oicq eq ""){$oicq="OICQ";}
   $url        = $FORM{'url'};
   if ($url   eq ""){$url  ="不告诉你";}
   $texti = &checknull($FORM{'texti'}  ,"留言不说是不行的!!一定要说两句哦！");
   $texti =~ s/ /&nbsp;/g;
   $texti =~ s/\<p\>/\n\n/ig;
   $texti =~ s/\<br\>/\n/ig;
   $texti = &code("$texti");
   if (length($oicq)>8) {print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>错误的OICQ号码!</h2><br><input type=button name=ok class=input2 value=\"返 回\" onclick=javascript:history.go(-1)></div>";}
   if (length($texti)>$lymax) {print "<head><BODY bgcolo=$gbbgcolor $gbbody>$pagestyle</head><br><br><br><br><div align=center><h2>你的留言内容不能超过$lymax个字符哦！<br>如果你想长篇大论的话，到本站论坛去吧！</h2><br><input type=button name=ok class=input2 value=' 返 回 '  onclick=javascript:history.go(-1)></div>";exit;}
   $photo      = $FORM{'photo'} ;
   $newuserno  = sprintf ("%04d%02d%02d%02d%02d%02d",$year,$mon,$mday,$hour,$min,$sec);
   $ipaddress  = $ENV{'REMOTE_ADDR'};
   $fromwhere = &ipwhere("$ipaddress");
   $date_time  = sprintf ("%04d/%02d/%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
   $message =  "留言信息如下： \n";
   $message.=  "------------------------------------------------------\n";
   $message.=  "留言标题: $place\n";
   $message.=  "姓    名: $name\n";
   $message.=  "电子邮件: $email\n";
   $message.=  "OICQ号码: $oicq\n";
   $message.=  "主页地址: $url\n";
   $message.=  "I P 地址: $ipaddress\n";
   $message.=  "来    自: $fromwhere\n";
   $message.=  "留言时间: $date_time\n";
   $message.=  "留言内容:\n\n";
   $message.=  "    $texti\n\n";
   $message.=  "\n\n";
   $message.=  "回复留言：$cgiurl/gbook.cgi?action=replay&user=$user&recode1=$newuserno\n\n";
   $message.=  "------------------------------------------------------\n";
if ($qqtoad eq "on"){
   $user = $FORM{'user'};
   open (MAIL, "|$mailprog $ajiegbmail");
   print MAIL "Reply-to:$email\n";
   print MAIL "From: $ajiegbmail\n";
   print MAIL "Subject: $title有网友给你发悄悄话啦\n\n";
   print MAIL "$message";
   close (MAIL);
   $texti="此留言为悄悄话，留言内容已发送给版主……";
}
if ($writetoad eq "on"){
   $user = $FORM{'user'};
   open (MAIL, "|$mailprog $ajiegbmail");
   print MAIL "Reply-to:$email\n";
   print MAIL "From: $ajiegbmail\n";
   print MAIL "Subject: $title有网友给你留言啦\n\n";
   print MAIL "$message";
   close (MAIL);
}
   dbmopen(%USERFILE,"$datapath/$user.db",0666);
   $USERFILE{$newuserno} = "start‖$name‖$email‖$place‖$photo‖$texti‖$url‖$fromwhere‖$date_time‖$oicq‖$posticons‖end‖\n";
   dbmclose(%USERFILE);
   &mailadmin;
   $linkurl      = "$cgiurl/gbook.cgi?user=$user";
print <<EOF;
<html>
<head>
<title>返回留言本</title>
<meta HTTP-EQUIV="REFRESH" CONTENT="3;URL=$linkurl">
$pagestyle
</head>
<BODY bgcolo=$gbbgcolor $gbbody>
<ul>
<p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">
  <h2>
  请等待 系统正在处理你的留言信息..... <br>
  留言成功,3秒后我们将带你返回这个留言本的首页.<br>
  如果系统没有反应请按下面的链接返回留言本！<br>
  <a href=$cgiurl/gbook.cgi?user=$user>返回我的留言本</a>
  </h2>
</p>


  </font>


EOF
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
sub writegb
  {
print <<EOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>$home</title></head>
<body bgcolor="$gbbgcolor" $gbbody>
EOF
print qq(<center><table width=$tablewidth align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=0 cellpadding=4 border=0 height="100%"><tr>
          <td bgcolor=$guestbgcolor rowspan="4" width="25%" valign="top" align=center>
<table style="filter:glow(color=$guestnamegy,direction=135)">&nbsp;
<font color=$guestnamefont>$name</font></table><img src="$photoimage"><br><br>
 第 $recode 条留言</td>
          <td bgcolor=$lybgcolor align=center width="1" rowspan="4">
            <table width=1 height=100% cellpadding=0 cellspacing=0 bgcolor=#83c6c0>
              <tr>
                <td width=1></td>
              </tr>
            </table>
          </td>
          <td bgcolor=$lybgcolor width="75%"><b>标题：</b>$place);
if ($url eq "http://"){print qq~&nbsp;<img src="$images/homepage.gif" width="16" height="15" border=0>主页~;}
else {print qq~&nbsp;&nbsp;<a href="$url" target="_blank" title="访问$name的主页" target="_blank"><img src="$images/homepage.gif" width="16" height="15" alt="访问$name的主页" border=0>主页</a>~;}
if ($email eq "不告诉你"){print qq~&nbsp;<img src="$images/email.gif" width="16" height="15" border=0>信箱</a>~;}
else {print qq~&nbsp;<a href="mailto:$email" title="给$name发信" target="_blank"><img src="$images/email.gif" width="16" height="15" alt="给$name发信" border=0>信箱</a>~;}
if ($oicq eq "OICQ"){print qq~&nbsp;&nbsp;<img src="$images/oicq.gif" width="16" height="15" alt="$name的QQ号码:$oicq" border=0>$oicq~;}
else {print qq~&nbsp;&nbsp;<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$oicq target=_blank><img src="$images/oicq.gif" width="16" height="15" alt="$name的QQ号码:$oicq" border=0>$oicq</a>~;}
print qq( <hr width=100% size=1 color=$tbcolor>
          </td>
        </tr>
        <tr>
          <td bgcolor=$lybgcolor width="75%"><TABLE border=0 cellPadding=3 cellSpacing=0 height="100%" width="100%"><TBODY><TR><TD vAlign=top width="100%"><img src=$posticons width=13 height=13 border=0>&nbsp;&nbsp;$texti</TD></TR></TBODY></TABLE></td>
        </tr>
        <tr>
          <td bgcolor=$lybgcolor width="75%">
            <hr width=100% size=1 color=$tbcolor>
<img src="$images/posttime.gif" width="16" height="15" alt="留言时间">：$date_time&nbsp;&nbsp;<img src="$images/ip.gif" width="16" height="15" alt="来自哪里">：$fromwhere&nbsp;&nbsp;<a href="gbook.cgi?action=replay&user=$user&recode1=$tmp" target="_blank"><img src="$images/replynow.gif" width="16" height="15" alt="回复留言" border=0>回复</a>&nbsp;
<a href="gbook.cgi?action=del&user=$user&recode1=$tmp" target="_blank"><img src="$images/del.gif" width="16" height="15" alt="删除留言" border=0>删除</a>
</td></tr></table></td></tr></table>);
   }
#############
sub del
  {
   dbmopen(%TEMP,"$datapath/$user.db",0666);
   %USERLIST = %TEMP;
   dbmclose(%TEMP);
   @userno=keys %USERLIST;
   @userno=sort @userno;
   $totalrecode = $#userno+1;
   $deleteyes = "del";
   print <<HTMLEOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>$gbname</title></head>
<center>
<form method="post" action="$cgiurl/gbook.cgi?action=delok&user=$user&recode1=$FORM{'recode1'}">

<table width=230 align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont>删 除 留 言</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
                <td width="30%" align="center">版主账号：</td>
                <td width="70%">&nbsp;<!--$admin-->
<input type=text name=adminame size=20 class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="30%" align="center">版主密码：</td>
                <td width="70%"><!--$password-->&nbsp;
<input type=password name=admipass size=20 class="input2">
                </td>
              </tr>
        <tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
<input type="submit" value="确认删除" class="input2">
&nbsp;&nbsp;&nbsp;&nbsp;
<input type="reset" value="重新来过" class="input2"></div>
</td></tr></table>
</td></tr></table>
</form>
</body></html>
HTMLEOF
}
#############
sub replay
  {
   dbmopen(%TEMP,"$datapath/$user.db",0666);
   %USERLIST = %TEMP;
   dbmclose(%TEMP);
   @userno=keys %USERLIST;
   @userno=sort @userno;
   $totalrecode = $#userno+1;
   $deleteyes = "del";
   print <<HTMLEOF;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>$title</title></head><body><center>
<form method="post" action="$cgiurl/gbook.cgi?action=replayok&user=$user&recode1=$FORM{'recode1'}">
<table width=230 align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont>回 复 留 言</font></div>
          </td>
        </tr>
<tr bgcolor=$lybgcolor>
                <td width="30%" align="center">版主账号：</td>
                <td width="70%">&nbsp;<!--$admin-->
&nbsp;<input type=text name=adminame size=20 class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="30%" align="center">版主密码：</td>
                <td width="70%"><!--$password-->&nbsp;
&nbsp;<input type=password name=admipass size=20 class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="30%" align="center" colspan="2">
<textarea rows="6" name="tempre" cols="30" class=input3></textarea></td>
              </tr>
        <tr><td bgcolor=$btbgcolor colspan="2"><div align="center">
              <input type="submit" value="确认回复" class="input2">
              &nbsp;&nbsp;&nbsp;&nbsp;
              <input type="reset" value="重新来过" name="B1" class="input2"></div>
</td></tr></table>
</td></tr></table>
</form>

</body></html>




HTMLEOF
}

#############
sub replayok
  {
   if ((($FORM{'adminame'} eq $adminame) && ($FORM{'admipass'} eq $admipass)) || (($FORM{'adminame'} eq $admin) && ($FORM{'admipass'} eq $password)))
      {
       dbmopen(%USERLIST,"$datapath/$user.db",0666);
       @userno=keys %USERLIST;
       @userno=sort @userno;
       $totalrecode = $#userno+1;
       for ($inti = $totalrecode-1;$inti >= 0;$inti--)
         {
          $tempint=$inti+1;
          $tempnum = "recode$tempint";
          $tempno=$FORM{$tempnum};
          $tempjob = "job$tempint";
          $tmpjob  = $FORM{$tempjob};
          $tempre  = "re$tempint";
          $tmpre   = $FORM{$tempre};
          if ($tempno ne "")
            {
             foreach (@userno)
               {
               	if ($tempno eq $_)
                  {
             ($mark,$name,$email,$place,$photo,$texti,$url,$fromwhere,$date_time,$oicq,$posticons,$markend,$last)=split(/‖/,$USERLIST{$tempno});
             $textireturn=$texti;
             $tmpre =~ s/\n/<br>/g;
             $tmpre =~ s/ /&nbsp;/g;
             $texti="$texti<br>&nbsp;&nbsp;&nbsp;&nbsp;<font size=2 color=$adminfont>【版主回复】：</font><font size=2 color=$adminfontny>$FORM{'tempre'}</font>";
             $USERLIST{$tempno} = "start‖$name‖$email‖$place‖$photo‖$texti‖$url‖$fromwhere‖$date_time‖$oicq‖$posticons‖end‖\n";
             $tmpre =~ s/<br>/\n/g;
             $tmpre =~ s/&nbsp;/ /g;
             &mailadmin;
                  }
               }
            }
         }
dbmclose(%USERLIST);
print <<EOF;
<html>
<head>
<title></title>
<BODY bgcolo=$gbbgcolor $gbbody>
<meta HTTP-EQUIV="REFRESH" CONTENT="3;URL=$cgiurl/gbook.cgi?user=$user">
$pagestyle
</head>
<ul><center>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">
  <h2>
  请等待 系统正在处理你的留言信息..... <br>
  回复成功,3秒后我们将带你返回这个留言本的首页.<br>
  如果系统没有反应请按下面的链接返回留言本！<br>
  <a href=$cgiurl/gbook.cgi?user=$user>返回我的留言本</a>
  </h2>
</p>

  <p align="center">
</html>
EOF
}else{
print <<EOF;
<html>
<head>
<title></title>
<BODY bgcolo=$gbbgcolor $gbbody>
<meta HTTP-EQUIV="REFRESH" CONTENT="3;URL=$cgiurl/gbook.cgi?user=$user">
$pagestyle
</head>
<ul>
<p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">
  <h2>错&nbsp;&nbsp;&nbsp;&nbsp;误<br>
  请等待 系统正在处理你的留言信息..... <br>
  用户名或密码错误,3秒后我们将带你返回这个留言本的首页.<br>
  如果系统没有反应请按下面的链接返回留言本！<br>
  <a href=$cgiurl/gbook.cgi?user=$user>返回我的留言本</a>
  </h2>
</p>

</html>
EOF
     }
  }
#############
sub write
   {
print qq(
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
$pagestyle
<title>$home</title></head>
<body bgcolor="$gbbgcolor" $gbbody>
<form name=form method="POST" action="$cgiurl/gbook.cgi?action=add&user=$user">
<script>
function emoticon(theSmilie){
document.form.texti.value += theSmilie + ' ';
document.form.texti.focus();
}
</SCRIPT>
<SCRIPT src=$images/code.js></SCRIPT>
<table width=70% align=center cellspacing=0 cellpadding=0  border=0 bgcolor=$tbcolor><tr><td>
      <table width=100% cellspacing=1 cellpadding=4 border=0 height="100%">
        <tr>
          <td bgcolor=$btbgcolor colspan="2">
            <div align="center"><font color=$btfont><B>签  写  留  言</b></font></div>
          </td>
        </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>留言标题：</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="place" size="35" maxlength="40" class="input2">
                  * 不得超过 20 个汉字
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>您的名字：</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="name" size="25" maxlength="50" class="input2"> *
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>电子邮件：</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="email" size="25" maxlength="30" class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>OICQ号码：</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="oicq" size="25" maxlength="50" class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>主页地址：</b></td>
                <td width="77%">&nbsp;
                  <input type="text" name="url" size="25" maxlength="50" value="http://" class="input2">
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>当前心情：</b><br>贴图方法：点击相应的心情图标即可</td>
                <td width="77%" valign=top>);

     open (FILE, "$cgiabs/info/post.cgi");
     my @posticondata = <FILE>;
     close (FILE);
     chomp @posticondata;

    $tempiconnum=1;
    $tempselect = "checked";
    foreach $picture (@posticondata) {
       if ($tempiconnum > 10) {
    	   $tempiconnum = 1;
    	   print qq~<BR>~;
                              }
       print qq(<input type=radio value="$picture" name="posticon" $tempselect><a href="javascript:emoticon('[img]$images/posticons/$picture\[/img]');"><img src=$images/posticons/$picture border=0></a>&nbsp;);
       $tempiconnum ++;
       $tempselect = "";
                                     }

     print qq(</td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>选择头像：</b></td>
                <td width="77%">&nbsp;&nbsp;<select name="photo">
				<option value=01 selected>头像01
				<option value=02>头像02
				<option value=03>头像03
				<option value=04>头像04
				<option value=04>头像05
				<option value=05>头像06
				<option value=07>头像07
				<option value=08>头像08
				<option value=09>头像09
				<option value=10>头像10
				<option value=11>头像11
				<option value=12>头像12
				<option value=13>头像13
				<option value=14>头像14
				<option value=15>头像15
				<option value=16>头像16
				<option value=17>头像17
				<option value=18>头像18
				<option value=19>头像19
				<option value=20>头像20
				</select>
                  <a href=$cgiurl/avatarslist.cgi target=_blank>查看头像列表</a></td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>留言内容：</b></td>
                <td width="77%" align=center>$insidejs<br>
<TEXTAREA rows=6 name=texti cols=64 class=input3 wrap=hard></TEXTAREA>
                </td>
              </tr>
              <tr bgcolor=$lybgcolor>
                <td width="23%"><B>其它功能：</b></td>
                <td width="77%">
<input type=checkbox value=on name=qqtoad> 悄悄话&nbsp;&nbsp;
<input type=checkbox value=on name=writetoad> 把留言发送给版主
                </td>
              </tr>
        <tr>
          <td bgcolor=$btbgcolor colspan="2"><div align="center">
<input type=submit value=签写留言 class=input2 name=submit1>&nbsp;&nbsp;&nbsp;&nbsp;
<input type=button name=ok class=input2 value=查看留言 onclick=javascript:history.go(-1)></div></td>
        </tr>
      </table>
    </td></tr></table>

</form>

<p align="center" class="newfont6">免费留言本由
<a href=$homeurl target=_blank><b>$home</b></a></font>
<font color=#cc0033></font>提供 技术支持：<a href=http://www.homecgi.com target=_blank><b>Ajie</b></a></p>
</body>
);
}
#############
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
#############
sub delok
  {
   if ((($FORM{'adminame'} eq $adminame) && ($FORM{'admipass'} eq $admipass)) || (($FORM{'adminame'} eq $admin) && ($FORM{'admipass'} eq $password)))
      {

          $tempint=$inti+1;
          $tempnum = "recode$tempint";
          $tempno=$FORM{$tempnum};
          $tempjob = "job$tempint";
          $tempre  = "re$tempint";
          $tmpre   = $FORM{$tempre};
       dbmopen(%USERLIST,"$datapath/$user.db",0666);
       @userno=keys %USERLIST;
       @userno=sort @userno;
       $totalrecode = $#userno+1;
       delete $USERLIST{$tempno};
       dbmclose(%USERLIST);
print <<EOF;
<html>
<head>
<title>$home</title>
<BODY bgcolo=$gbbgcolor $gbbody>
<meta HTTP-EQUIV="REFRESH" CONTENT="3;URL=$cgiurl/gbook.cgi?user=$user">
$pagestyle
</head>
<ul><center>
<p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">
  <h2>
  请等待 系统正在处理你的留言信息..... <br>
  删除成功,3秒后我们将带你返回这个留言本的首页.<br>
  如果系统没有反应请按下面的链接返回留言本！<br><br>
  <a href=$cgiurl/gbook.cgi?user=$user>返回留言本</a>
  </h2>
</p>


</html>
EOF
     }
   else
     {
print <<EOF;
<html>
<head>
<title>$home</title>
<BODY>
$pagestyle
</head>
<ul><center>
<p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">　</p>
  <p align="center">
  <h2>&nbsp;&nbsp;错误:&nbsp;&nbsp;<br>
  请等待 系统正在处理你的留言信息..... <br>
  用户名或密码错误.<br><br>
  <input type=button name=ok class=input2 value=' 返 回 ' 定 onclick=javascript:history.go(-1)>
  </h2>
</p>

</html>
EOF
     }
  }