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
#            http://maildo.com/      大家一起邮
#            
#############################################################

sub adminlogin {
    $inmembername =~ s/\_/ /g;
    print qq(
    <tr><td bgcolor="#333333" colspan=2><font face=$font color=#FFFFFF>
    <b>欢迎来到 LB5000 论坛管理中心</b>
    </td></tr>
    <form action="$boardurl/$adminprog" method="post">
    <input type=hidden name="action" value="login">
    <tr>
    <td bgcolor=#EEEEEE valign=middle colspan=2 align=center><font face=$font color=#333333><b>请输入您的用户名、密码登陆</b></font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle width=40% align=right><font face=$font color=#555555>请输入您的用户名</font></td>
    <td bgcolor=#FFFFFF valign=middle><input type=text name="membername" value="$inmembername" maxlength=15></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle width=40% align=right><font face=$font color=#555555>请输入您的密码</font></td>
    <td bgcolor=#FFFFFF valign=middle><input type=password name="password" value="$inpassword" maxlength=20></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle colspan=2 align=center><input type=submit name="submit" value="登 陆"></form></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2><font face=$font color=#555555>
    <blockquote><b>请注意</b><p><b>只有论坛的坛主才能登陆论坛管理中心。<br>未经过授权的尝试登陆行为将会被记录在案！</b><p>在进入论坛管理中心前，请确定你的浏览器打开了 Cookie 选项。<br> Cookie 只会存在于当前的浏览器进程中。为了安全起见，当你关闭了浏览器后，Cookie 会失效并被自动删除。</blockquote>
    </td></tr>
    </table></td></tr></table>
    );
    
}
sub admintitle {
    print qq~
    <html>
    <head>
    <title>LB5000 - 论坛管理中心</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style>
A:visited{TEXT-DECORATION: none}
A:active{TEXT-DECORATION: none}
A:hover{TEXT-DECORATION: underline overline}
A:link{text-decoration: none;}
.t{LINE-HEIGHT: 1.4}
TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: 宋体; FONT-SIZE: 9pt} 
INPUT{BORDER-TOP-WIDTH: 1px; PADDING-RIGHT: 1px; PADDING-LEFT: 1px; BORDER-LEFT-WIDTH: 1px; FONT-SIZE: 9pt; BORDER-LEFT-COLOR: #cccccc; BORDER-BOTTOM-WIDTH: 1px; BORDER-BOTTOM-COLOR: #cccccc; PADDING-BOTTOM: 1px; BORDER-TOP-COLOR: #cccccc; PADDING-TOP: 1px; HEIGHT: 18px; BORDER-RIGHT-WIDTH: 1px; BORDER-RIGHT-COLOR: #cccccc}
textarea, select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: 宋体; font-size: 9pt; font-style: bold;}
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
    <body bgcolor="#555555" topmargin=5 leftmargin=5>
    <table width=95% cellpadding=0 cellspacing=1 border=0 bgcolor=#000000 align=center>
    <tr><td>
    <table width=100% cellpadding=0 cellspacing=1 border=0>
    <tr><td width=25% valign=top bgcolor=#FFFFFF>
    <table width=100% cellpadding=6 cellspacing=0 border=0>
    <tr><td bgcolor="#333333"><font face=$font color=#FFFFFF>
    <b>管理菜单</b>
    </td></tr>
    <tr>
    <td bgcolor="#FFFFFF"><font face=$font color=#333333>
    >> <a href="admincenter.cgi">管理中心首页(*)</a><br>
    >> <a href="admincenter.cgi?action=logout">退出管理中心(*)</a><br>
    >> <a href="$boardurl/$forumsummaryprog">进入您的论坛(*)</a>
    </td></tr>
    <tr>
    <td bgcolor="#EEEEEE"><font face=$font color=#333333><b>用户管理</b>
    </td></tr>
    <tr>
    <td bgcolor="#FFFFFF"><font face=$font color=#333333>
    >> <a href="$setmembersprog">用户管理/排名(*)</a><BR>
    >> <a href="usermanager.cgi">用户分类/管理(*)</a><BR>
    >> <a href="setmemberbak.cgi">用户库备份/还原</a><BR>
    </td></tr>
    <tr>
    <td bgcolor="#EEEEEE"><font face=$font color=#333333><b>注册管理</b>
    </td></tr>
    <tr>
    <td bgcolor="#FFFFFF"><font face=$font color=#333333>
    >> <a href="noreg.cgi">保留特殊用户名(*)</a><BR>
    >> <a href="noregemail.cgi">保留特殊 Email(*)</a><BR>
    >> <a href="noregip.cgi">禁止特殊 IP 注册用户(*)</a><BR>
    </td></tr>
    
    <tr>
    <td bgcolor="#EEEEEE"><font face=$font color=#333333><b>论坛管理</b>
    </td></tr>
    <tr>
    <td bgcolor="#FFFFFF"><font face=$font color=#333333>
    >> <a href="$setforumsprog">论坛管理</a><br>
    >> <a href="merge.cgi">合并论坛</a><br>
    >> <a href="adbackup.cgi">论坛备份到本地/还原</a><BR>
    >> <a href="$shareforumsprog">联盟论坛管理</a><BR>
    >> <a href="rebuildall.cgi">重建所有论坛</a><br>
    >> <a href="rebuildmain.cgi">重新建立论坛主界面</a><br>
    </td></tr>

    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>设置管理</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="$setmembersprog?action=init">初始化数据</a><br>
    >> <a href="$stylesprog">默认风格设置</a><br>
    >> <a href="$varsprog">基本变量设置</a><br>
    >> <a href="setmemdir.cgi">用户信息目录设置</a><br>
    >> <a href="setmpic.cgi">论坛图片设置</a><br>
    >> <a href="setcity.cgi">社区货币设置</a><br>
    >> <a href="$membertitlesprog">用户等级设置</a><br>
    >> <a href="setemotes.cgi">EMOTE 设置</a><br>
    </td></tr>

    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>限制管理</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="setbadwords.cgi">不良词语过滤(*)</a><BR>
    >> <a href="setipbans.cgi">IP 禁止(*)</a><BR>
    >> <a href="setidbans.cgi">ID 禁止(*)</a><BR>
    </td></tr>

    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>特殊功能</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="massmsg.cgi">短消息广播</a><BR>
    >> <a href="mailmembers.cgi">Email 群发</a><BR>
    >> <a href="setplugin.cgi">论坛插件设定</a><br>      
    >> <a href="setskin.cgi">管理区插件设定</a><br>      
    </td></tr>
    <tr>
    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>论坛编辑</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="setregrules.cgi">修改注册声明</a><br>
    >> <a href="setregmsg.cgi">修改短消息欢迎信息</a><br>
    >> <a href="settemplate.cgi">编辑论坛模板</a><br>
    </td></tr>
    
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>其它设置</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="baddellogs.cgi">论坛安全日志</a><br>
    >> <a href="adminloginlogs.cgi">管理区安全日志</a><br>
    >> <a href="userratinglog.cgi">用户威望操作日志</a><br>
    >> <a href="sizecount.cgi">统计论坛占用空间</a><br>
    >> <a href="vercheck.cgi">论坛版本/更新</a><br>
    </td></tr>
    ~;
    
    if (-e "${lbdir}data/leoskin.cgi"){
	require "${lbdir}data/leoskin.cgi";
	if ($skin1name ne ""){
	    print qq~    
    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>论坛插件</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
	~;    
    print qq~>> <a href="$skin1url">$skin1name</a><br>~ if ($skin1name ne "");
    print qq~>> <a href="$skin2url">$skin2name</a><br>~ if ($skin2name ne "");
    print qq~>> <a href="$skin3url">$skin3name</a><br>~ if ($skin3name ne "");
    print qq~>> <a href="$skin4url">$skin4name</a><br>~ if ($skin4name ne "");
    print qq~>> <a href="$skin5url">$skin5name</a><br>~ if ($skin5name ne "");
    print qq~>> <a href="$skin6url">$skin6name</a><br>~ if ($skin6name ne "");
    print qq~>> <a href="$skin7url">$skin7name</a><br>~ if ($skin7name ne "");
    print qq~>> <a href="$skin8url">$skin8name</a><br>~ if ($skin8name ne "");
    print qq~>> <a href="$skin9url">$skin9name</a><br>~ if ($skin9name ne "");
    print qq~>> <a href="$skin10url">$skin10name</a><br>~ if ($skin10name ne "");    
    print qq~</td></tr>~;
	}
    }
    print qq~
    <td bgcolor=#EEEEEE><font face=$font color=#333333>&nbsp;
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="admincenter.cgi">管理中心首页(*)</a><br>
    >> <a href="$boardurl/$forumsummaryprog">进入您的论坛(*)</a><br>
    >> <a href="admincenter.cgi?action=logout">退出管理中心(*)</a><br>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>&nbsp;
    </td></tr>
    
    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>LB5000 信息</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF align=left>
    <span class="large">版本：</span><span class="body">$versionnumber</span><p>
    <font face=$font color="#333333">
    中文版权所有： <a href="http://www.cgier.com/" target=_blank>CGI 编程者之家</a><br>
    技术支持论坛： <a href="http://www.leobbs.com/">网酷超级论坛</a>
    </td></tr></table>
    </td><td width=70% valign=top bgcolor=#FFFFFF>
    <table width=100% cellpadding=6 cellspacing=0 border=0>
    ~;
}
sub parseadminform {
    read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    @pairs = split(/&/, $buffer);
    foreach $pair (@pairs) {
        ($name, $value) = split(/=/, $pair);
        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        $name =~ tr/+/ /;
        $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        $value =~ s/\"/&quot\;/g;
        $value =~ s/\</&lt\;/g;
        $value =~ s/\>/&gt\;/g;
        $value =~ s/\;/\\\;/g;
        $value =~ s/<!--(.|\n)*-->//g;
        $header =~ s/\@/\\\@/g;
        $FORM{$name} = $value;
    }
}
1;  
