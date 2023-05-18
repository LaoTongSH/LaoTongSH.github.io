#!/usr/bin/perl

###########################[ 按情况修改 ]################################
#$main_dir = "/u/sunya/cgi-bin/fangke";   #这个是数据库所在目录的绝对路径
$main_dir = "/user/l/la/laotong/cgi-bin/memo";

$main_url = "http://cgi.laotong.533.net/memo";  #数据库目录对应的URL；

#$cgi_url = "/cgi-bin/fangke/memo.cgi";   #程序本身的url;
$cgi_url = "http://cgi.laotong.533.net/memo/memo.cgi"; 

#$img_url = "/fangke/img";            #img图象目录的URL
$img_url = "http://laotong.533.net/memoimg";
###############################################################################

##############################[ 环境色彩 ]###################################
@text_color = ( #唱凯瞪 地址 临荐父怒 祸 硅凯阑 眠啊唱 皑家 矫虐矫搁 邓聪促... ^.^
"#FF0033", "#FF6600", "#FF9900", "#00D300", "#009900", 
"#0000FF", "#0000AC", "#CC00CC", "#830083", "#999999",
"#CCCCCC", "#E9E9E9");                       
################################################################################

##############################[ 随机显示的标题 ]###################################
$word00 = "很晚了，还不睡觉吗？";  
$word01 = "你可真能熬夜，当心身体哟！";
$word02 = "夜深了，万蔌俱静，我似乎听到了你呼吸的声音。";
$word03 = "已经凌晨3时多了，你是否想度过一个不眠之夜？";
$word04 = "天快亮了。";
$word05 = "一日之际在于晨，出去锻炼锻炼吧。";
$word06 = "早上好";
$word07 = "管理员由此进入";
$word08 = "管理员由此进入";
$word09 = "管理员由此进入";
$word10 = "管理员由此进入";
$word11 = "管理员由此进入";
$word12 = "你吃了吗？哈哈，中国人的习惯。";
$word13 = "管理员由此进入";
$word14 = "管理员由此进入";
$word15 = "管理员由此进入";
$word16 = "管理员由此进入";
$word17 = "管理员由此进入";
$word18 = "管理员由此进入";
$word19 = "不看看新闻联播吗？";
$word20 = "管理员由此进入";
$word21 = "管理员由此进入";
$word22 = "管理员由此进入";
$word23 = "明天还要上班，早点睡吧。";
################################################################################
#以下不需修改 ^.^

&parseArgument;

sub parseArgument {
	if($ENV{'REQUEST_METHOD'} eq "GET") {
		$buffer = $ENV{'QUERY_STRING'};
    } 
	else {
        read( STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    }
    @pairs = split(/&/,$buffer);
    foreach $pair( @pairs ) {
        ($name,$value)=split(/=/,$pair);
        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
		unless (($name eq 'comments') || ($name eq 'html_up') || ($name eq 'html_down')) {
			$value =~ s/<([^>]|\n)*>//g;
		}
        $FORM{$name} = $value;
    }
	if($FORM{'id'}){
		$main_dir = "$main_dir/$FORM{'id'}";
	}
	else{
		$err="id";
		&error;
	}
	&selectAction;
}

sub selectAction{
	&get_conf;
	if($FORM{'id'}) {
		if(($FORM{'action'}) eq "" || ($FORM{'action'} eq "reload")) {
			&display;
		}
		elsif($FORM{'action'} eq "write") {
			if(($FORM{'name'} eq "") || ($FORM{'comments'} eq "")) {
				$err = "normal";
				&error;
			}
			else { 
				&write;
			}
		}
		elsif($FORM{'action'} eq "admin_login") {
			&admin_login;
		}
		elsif($FORM{'action'} eq "loginok") {
			if($FORM{'passwd'} eq "") {
				&error;
			}
			&loginok;
		}
		elsif($FORM{'action'} eq "erase") {
			&erase;
		}
		elsif($FORM{'action'} eq "eraseok") {
			if($FORM{'passwd'} eq "") {
				&error;
			}
			&eraseok;
		}
		elsif($FORM{'action'} eq "conf_chg") {
			&conf_chg;
		}
		else {
			&display;
		}
	}
	else{
		$err = "id";
		&error;
	}
}

sub get_conf{
	unless(-e "$main_dir/conf.txt"){
		mkdir("$main_dir/data",0777);
		open(DATA, ">$main_dir/data/data.txt");
		print DATA "0\n";
		close(DATA);
	}
 	if(open(CONF,"<$main_dir/conf.txt")){
	    $conf_list = <CONF>;
	    close(CONF);
	    @conf = split(/\|/,$conf_list);
		$admin_pass = $conf[1];
		$list_num = $conf[2];
	    $table_size = $conf[3];
		$max_data = $conf[4];
	    $table_color = $conf[5];
		$cell_color = $conf[6];
		$html = $conf[7];
		$bgcolor = $conf[8];
		$bgimage = $conf[9];
		$quick_num = $conf[10];
		$good_char = $conf[11];
	}
	else{
		$admin_pass = "1234";
		$list_num = "12";
	    $table_size = "570";
		$max_data = "500";
	    $table_color = "#658AFF";
		$cell_color = "#E5F0FF";
		$html = "yes";
		$bgcolor = "#ffffff";
		$bgimage = "";
		$quick_num = "5";
		$good_char = "【】■□《》△▼▽▲◆◇◢◣◤◥★☆♀♂『』←↑→↓↖↗↘↙○◎●℃№※√≤≥☉";
		&put_conf;
	}
   
}

sub put_conf {
	$cryptpass = crypt($admin_pass,sp);
    open(CONF,">$main_dir/conf.txt");
    print CONF "|$cryptpass|$list_num|$table_size|$max_data|$table_color|$cell_color|$html|$bgcolor|$bgimage|$quick_num|$good_char|\n";
    close(CONF);
}

sub error {
	&head;
    print "<p>&nbsp;<H1><u><font color=#FFBCEF>！！！ Error!!! ！！！</font></u></H1>\n";
   
    if($err eq "normal"){
		print "第一TXT<br> 殿废捞 啊瓷钦聪促<p>\n";
    }
    elsif($err eq "id"){
		print "memo.cgi?id=<font color=red>叼泛配府名称</font> 请侥栏肺 阂矾林技夸<p>\n";
    }
	else{
		print "输入密码错误，仔细核对你输入的对吗？<p>\n";
	}
	
	print "<a href=\"javascript:history.go(-1)\">返回</a>\n";
	&foot;	
}

sub display {
	open(Num,"<$main_dir/data/data.txt");
	$num = <Num>;
	close(Num); 
  
	opendir (DATA,"$main_dir/data");
	@num_data = readdir(DATA);
	$fil_data = @num_data-3;
	closedir(DATA);

	$file_num = $num;
	$tot_pg = int($fil_data/$list_num);
	if(($tot_pg*$list_num) < $fil_data) {$tot_pg = $tot_pg + 1; }
	&read_cookie;
	&head;

	if(-e "$main_dir/up.txt"){
		open(UPDATA,"<$main_dir/up.txt");
		@html_up = <UPDATA>;
		close(UPDAQTA);
		foreach $_(@html_up) {
			print "$_";	
		}		 
	}

	print "<form method=post action=$cgi_url><input type=hidden name=action value=write><input type=hidden name=id value=\"$FORM{'id'}\">\n";
	print "<div align=center><table border=0 width=$table_size cellspacing=0 cellpadding=1 bgcolor=black><tr><td>\n";
	print "<table border=0 width=100% cellspacing=0 cellpadding=3 bgcolor=$table_color>\n";
	print "<tr><td><table border=0 cellspacing=0 cellpadding=1 width=100%>\n";
	print "<tr>	<td><center><img src=$img_url/dot2.gif>\n";
	print "<a href=$cgi_url?id=$FORM{'id'}&action=admin_login><b><font color=white>\n";
	&getdate;
	&insa;
	print "</font></b></a><img src=$img_url/dot.gif></center></td>\n";
	print "</tr><tr><td colspan=3> <font color=$cell_color>网站名称</font> <input type=text name=name value=\"$COOKIE{'UN'}\" size=7 maxlength=7 style=\"background-color:#FAFAFA;border:1 solid black\">\n";
	print "<font color=$cell_color>网址</font> <input type=text name=comments size=26 maxlength=26 style=\"background-color:#FAFAFA;border:1 solid black\"> <input type=submit value=\"登记\" style=\"height:20px;background-color:#FAFAFA;border:1 solid black\">\n";
	print "<a href=$cgi_url?id=$FORM{'id'}&action=reload><font color=#ffffff>[刷新]</font></a></td></tr><tr><td>\n";
	print "<table border=0 width=100% cellspacing=0 cellpadding=1 bgcolor=$cell_color>\n";

	if(($FORM{'page'} eq "") || ($FORM{'page'} ==1)) {
		$d = 0;
		$num = $num+1;
		until ($num<=0) {
			$num = ($num - 1);
            if(-e "$main_dir/data/$num") {
				$d = ($d+1);
				&fileForm;
			}
			if($d >= $list_num) { $page=1; last}
		 }
      	
	}

	if(($FORM{'page'} ne "") &&($FORM{'page'} !=1)) {
		$scount = (($FORM{'page'}-1)*$list_num);
		$icount = 0;
		$d = 0;
		$pre_pg= $FORM{'page'} - 1;
		$next_pg = $FORM{'page'} + 1;
		until ($num<=0) {
			if(-e "$main_dir/data/$num") {
				$icount = $icount + 1;
				if($icount >= $scount) {
					$d = ($d+1);
					&fileForm;
				}
			if($d >= $list_num) { $page= $FORM{'page'}; last}
			}
	$num = ($num - 1);
	
		}
	}

	print "</table></td></tr></table></td></tr></table></td></tr></table>";

	if(($tot_pg <= 1) || ($FORM{'page'} eq "")){$page = 1; }
	else {$page= $FORM{'page'}; }
	&pagemove;

	if(-e "$main_dir/down.txt"){
		open(DOWNDATA,"<$main_dir/down.txt");
		@html_down = <DOWNDATA>;
		close(DOWNDATA);
		foreach $_(@html_down) {
			print "$_";	
		}		 
	}
	&foot;
}

sub getdate {     
    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

    $word_0="";
	if($min < 10) {
        $min = "0$min";
    }
    if($hour < 10) {
        $hour = "0$hour";
    }
    $mon++;
    if($mon < 10) {
        $mon = "0$mon";
    }
    if($mday < 10) {
        $mday = "0$mday";
    }
    $year1 = $year + 1900;
    $date = "$year1/$mon/$mday($hour:$min)";
}  

sub head {
	print "Content-type: text/html\n\n";
    print "<html>\n";
    print "<head><title></title></head>\n";
    print "<style type='text/css'>\n";
    print "<!--\n";
    print "BODY, table, tr, td{\n";
    print "font-family: 宋体, verdana, arial, helvetica, sans-serif;\n";
    print "font-size: 9pt;\n";
    print "}\n";
	print " A:link    {font:9pt 宋体;color:#0099FF;text-decoration:none;}\n";
	print " A:visited {font:9pt 宋体;color:#0099FF;text-decoration:none;color:$font_color;}\n";
	print " A:active  {color:#8FFF8A;font:9pt 宋体;}\n";
	print " A:hover  {color:red;text-decoration:underline;}\n";
	print " .big {font-size:14px;}\n";
    print "-->\n";
    print "</style>\n" ;
	print "<script language=\"JavaScript\">\n";
	print "function nextWin()\n";
	print "{location = \"$cgi_url\#memo\"}\n";
	print "</script>\n";
	print "</head>\n";

	if($FORM{'action'} eq "write") {
		$load="onLoad=\"setTimeout(\'nextWin()\',0)\"\n";
	}

	if ($bgimage eq ""){
		print"<body bgcolor=$bgcolor $load>\n";
	}
	else {
		print"<body background=$bgimage $load>\n";
	}

	print"<center>\n";
}

sub foot {
	print "</center></body></html>\n";
	exit;
}

sub read_cookie{
    if($ENV{'HTTP_COOKIE'}) {
        @cookies = split(/; /,$ENV{'HTTP_COOKIE'});
        foreach(@cookies) {
        ($name,$value) = split(/=/,$_);
        $COOKIE{$name} = $value;
        }
	}
}

sub insa{
	print $hour==0 ? $word00:
		  $hour==1 ? $word01:
		  $hour==2 ? $word02:
		  $hour==3 ? $word03:
		  $hour==4 ? $word04:
		  $hour==5 ? $word05:
		  $hour==6 ? $word06:
		  $hour==7 ? $word07:
		  $hour==8 ? $word08:
		  $hour==9 ? $word09:
		  $hour==10 ? $word10:
		  $hour==11 ? $word11:
		  $hour==12 ? $word12:
		  $hour==13 ? $word13:
		  $hour==14 ? $word14:
		  $hour==15 ? $word15:
		  $hour==16 ? $word16:
		  $hour==17 ? $word17:
		  $hour==18 ? $word18:
		  $hour==19 ? $word19:
		  $hour==20 ? $word20:
		  $hour==21 ? $word21:
		  $hour==22 ? $word22:
		  $hour==23 ? $word23:"\n";
}

sub fileForm{
	open(FILE,"<$main_dir/data/$num");
	$data = <FILE>;
	@wdata= split(/\|/,$data);
	close (FILE);

	if ($html ne "yes") {
		$wdata[2] =~ s/</&lt;/g;
		$wdata[2] =~ s/>/&gt;/g;
		$wdata[2] =~ s/"/&quot;/g;
		$wdata[2] =~ s/&lt;br&gt;/<br>/g;
	}
    $wdata[2] =~ s/\|/&#124;/g;
	$wdata[2]=~ s/(http:\/\/)([\w\+\-\/\=\?\.\~]+)/$url <img src=$img_url\/home.gif> <a href=\"$1$2\" target=\"_new\">$1$2<\/a>/g;
	$wdata[2]=~ s/([\w\-]+\@[\w\-+\.]+[\w\-]+)/$mail <img src=$img_url\/mail.gif> <a href=\"mailto:$1\">$1<\/a>/g;
	print"<tr><td> <a href=$cgi_url?id=$FORM{'id'}&action=erase&number=$num><img src=$img_url/del.gif  width=12 height=12 border=0 alt=\"删除\"></a> <font color=$text_color[$d-1]>[$wdata[1]]...\n";
	print "$wdata[2]</td><td nowrap width=102><font color=green>$wdata[3]</font></td></tr>\n";
}

sub pagemove{
	print "<table width=$table_size bgcolor=$table_color><tr><td align=center>";
	$first = 1;
	$last = $quick_num;
	while ($first <= $tot_pg) {
		if (($first <= $page) && ($page <= $last)) {
		$prevp = $first - 1;
			if ($prevp > 0) {
				print "[<a href=$cgi_url?id=$FORM{'id'}&page=$prevp onmouseover=\"window.status='捞傈 其捞瘤 焊扁';return true\" onmouseout=\"window.status='';return true\">prev</a>].....";
			}
			else {
				print "[<font color=C0C0C0>prev</font>].....";
			}
		if ($last <= $tot_pg) {
			for ($pa = $first; $pa <= $last; $pa++) {
				if ($pa == $page) {
					print "[<font color=red><b>$pa</b></font>] ";
				}
				else {
					print "[<a href=$cgi_url?id=$FORM{'id'}&page=$pa onmouseover=\"window.status='到第 $pa 页';return true\" onmouseout=\"window.status='';return true\">$pa</a>] ";
				}
			}
		}
		else {
			for ($pa = $first; $pa <= $tot_pg; $pa++) {
				if ($pa == $page) {
					print "[<font color=red><b>$pa</b></font>] ";
				}
				else {
					print "[<a href=$cgi_url?id=$FORM{'id'}&page=$pa onmouseover=\"window.status='到第 $pa 页';return true\" onmouseout=\"window.status='';return true\">$pa</a>]  ";
				}
			}
		}
		$nextp = $last + 1;
		if ($nextp <= $tot_pg) {
			print ".....[<a href=$cgi_url?id=$FORM{'id'}&page=$nextp onmouseover=\"window.status='促澜 其捞瘤 焊扁';return true\" onmouseout=\"window.status='';return true\">next</a>]";
		}
		else {
			print ".....[<font color=C0C0C0>next</font>]";
		}
	}
	$first = $first + $quick_num;
	$last = $last + $quick_num;
	}
	print "</td></tr></table></div></form>\n";
}

sub write {
	print "Set-Cookie: UN=$FORM{'name'}; expires=Sunday, 12-Dec-2002 12:12:12 GMT;\r\n";
	open(Num,"<$main_dir/data/data.txt");
	$num = <Num>;
	close(Num);   
	&lock;
	open(Num,">$main_dir/data/data.txt");
	$num = $num+1;
	print Num "$num\n";
	close(Num);
	&unlock;
	$FORM{'comments'} =~ s/\cM//g;

	&getdate;
	open(WFILE,">$main_dir/data/$num");
	print WFILE "|$FORM{'name'}|$FORM{'comments'}|$date|\n";
	close(WFILE);

	opendir (DATA,"$main_dir/data");
	@num_data = readdir(DATA);
	$fil_data = @num_data-3;
	closedir(DATA);
	if($fil_data > $max_data ) {
		$count = 0;
		until($num <= 0) {
			if (-e "$main_dir/data/$num") {
				$count = ($count + 1); 
			}
			$num = ($num - 1);
			if($count >= $max_data) {
				last  
			}
		}
		until($num <=0) {
			unlink ("$main_dir/data/$num") ;
			$num = ($num - 1);
		}
	}
            
	&display;
}

sub lock {
    local($LockFile) = "$main_dir/lock.txt";
    local($EndTime) = time+45;
    
    while (-s $LockFile && time < $EndTime) {
    	sleep(1);
    }
    open(LOCK, ">$main_dir/$LockFile");
    print LOCK "lock";
    close(LOCK);
}

sub unlock {
    local($LockFile) = "$main_dir/lock.txt";
    
    open(LOCK, ">$main_dir/$LockFile");
    print LOCK "";
    close(LOCK);
}

sub admin_login {
	&head;

print <<START;
<p>&nbsp;
<p>&nbsp;
<table border="0" cellpadding="3" cellspacing="0" width="420" bgcolor=$table_color>
    <tr>
        <td><table border="0" cellpadding="3" cellspacing="0" width="100%"
             bgcolor=$cell_color>
                <tr>
                    <td>						<p>&nbsp;<p align="center"><font size="2" color="$table_color">管理员专用.<br>请输入管理员密码</font>
<form method=post action=$cgi_url>
<input type=hidden name=id value=$FORM{'id'}>
<input type=hidden name=action value=loginok>
<input type=hidden name=number value=$FORM{'number'}>
<div align=center><table><tr><td>输入密码</td><td><input type=password name=passwd size=10 style="background-color:#EFEFEF;border:1 solid #000000"></td><td><input type=submit value=\"确定\" style="color:black;background-color:#EFEFEF;border:1 solid black;height:21px"></td><td></form></td></tr></table></div>
<p>&nbsp;</td></tr></table></td></tr></table>
START

	&foot;
}

sub loginok {
	$pass = $FORM{'passwd'};
	$cryptpass = crypt($pass,sp);
	$FORM{'passwd'} =  $cryptpass;
	if($admin_pass eq $FORM{'passwd'}) {
		&adminform;
	}
	else {
		&error;
	}
}

sub adminform {
	&get_conf;
	&head;
	print "<form method=post action=$cgi_url>\n";
	print "<input type=hidden name=action value=conf_chg>\n";
	print "<input type=hidden name=id value=$FORM{'id'}>\n";
	print "<table border=0 align=center cellpadding=1 cellspacing=0 bgcolor=black><tr><td>\n";
	print "<table border=0 width=100% cellpadding=3 cellspacing=0 bgcolor=#F4F4F4>\n";
	print "<table border=0 width=100% cellpadding=3 cellspacing=0 bgcolor=#F4F4F4>\n";
	
	if(-e "$main_dir/up.txt"){
		open(UPHTML,"$main_dir/up.txt");
		@html_up = <UPHTML>;
		close(UPHTML);
		print "<tr><td>顶部HTML代码<br><textarea name=html_up rows=8 cols=55>\n";
		foreach $_(@html_up) {
			print "$_";	
		}	
		print "</TextArea></td></tr>\n";
	}
	else{
		print "<tr><td>顶部HTML代码<br><textarea name=html_up rows=8 cols=55></TextArea></td></tr>\n";
	}

	if(-e "$main_dir/down.txt"){
		open(DOWNHTML,"$main_dir/down.txt");
		@html_down = <DOWNHTML>;
		close(DOWNHTML);
		print "<tr><td>底部HTML代码<br><textarea name=html_down rows=8 cols=55>\n";
		foreach $_(@html_down) {
			print "$_";	
		}	
		print "</TextArea></td></tr>\n";
	}
	else{
		print "<tr><td>底部HTML代码<br><textarea name=html_down rows=8 cols=55></TextArea></td></tr>\n";
	}
	print "<tr><td align=right><font color=000000>[请务必修改缺省的密码！！！]<br> 输入密码</font> <input type=password name=passad size=8>\n";
	print "&nbsp; <font color=000000>再输入一次</font> <input type=password name=repassad size=8></td></td></table>\n";
	print "<table border=0 width=100% cellpadding=3 cellspacing=0  bgcolor=#F4F4F4>\n";
	print "<tr><td align=right><font color=000000>每页显示的条目数</font> <input type=text name=list_num size=8 value=$list_num></td></tr>\n";
	print "<tr><td align=right><font color=000000>列表宽度</font> <input type=text name=table_size size=8 value=$table_size></td></tr>\n";
	print "<tr><td align=right><font color=000000>条目颜色(吗茄祸)</font> <input type=text name=table_color size=8 value=$table_color></td></tr>\n";
	print "<tr><td align=right><font color=000000>表框颜色</font> <input type=text name=cell_color size=8 value=$cell_color></td></tr>\n";
	print "<tr><td align=right><font color=000000>地址栏最大限制</font> <input type=text name=max_data size=8 value=$max_data></td></tr>\n";
	print "<tr><td align=right><font color=000000>允许HTML标签</font> <select name=html_ok>\n";
    if($html eq "yes"){
		print"<option value=no>No<option value=yes selected>Yes</select><br>\n";
	}
    else {
		print"<option value=no selected> No <option value=yes> Yes </select><br>\n";
	}
	print "<tr><td align=right><font color=000000>背景色</font> <input type=text name=bgcolor size=8 value=$bgcolor>\n";
	print " or <font color=000000>或背景图像的URL</font> <input type=text name=bgimage size=20 value=$bgimage></td></tr>\n";
  	print "<tr><td align=right><font color=000000>([prev].....[1] [2] [3] [4] [5] .....[next]) 其它页连接数</font> <input type=text name=quick_num size=2 value=$quick_num></td></tr>\n";
 	print "<tr><td align=right><font color=000000>特殊字符</font> <input type=text name=good_char size=46 value=$good_char></td></tr></table>\n";
	print "</td></tr></table></td></tr></table><br>\n";
	print "<input type=submit value=确认提交 style=\"background-color:#F6F6F6;border:1 solid black;height:20\"> <input type=reset value=清除重来 style=\"background-color:#F6F6F6;border:1 solid black;height:20\">\n";
	print "</form>\n";
	&foot;	
}

sub erase {
	&head;

print <<START;
<p>&nbsp;
<p>&nbsp;
<form method=post action=$cgi_url>
<input type=hidden name=action value=eraseok>
<input type=hidden name=number value=$FORM{'number'}>
<table border="0" cellpadding="3" cellspacing="0" width="420" bgcolor="$table_color">
    <tr>
        <td width="740"><table border="0" cellpadding="3" cellspacing="0" width="100%"
             bgcolor="$cell_color">
                <tr>
                    <td width="730">
					<p>&nbsp;
<br><input type=hidden name=id value="$FORM{'id'}">
					<p align="center"><font size="2" color="$table_color">删除操作需要密码.<br>请输入管理员密码</font>
<p>&nbsp;<div align=center><table><tr><td>输入密码</td><td><input type=password name=passwd size=10 style="background-color:#FAFAFA;border:1 solid #000000"></td><td><input type=submit value=删除 style="color:black;background-color:#FAFAFA;border:1 solid black;height:21px"></td><td></form></td></tr></table></div.
<br>
					<p>&nbsp;
						</td>
                </tr>
            </table></td>
    </tr>
</table>
<p>&nbsp;
START
	
	&foot;
}

sub eraseok {
	$pass = $FORM{'passwd'};
	$cryptpass = crypt($pass,sp);
	$FORM{'passwd'} =  $cryptpass;
	open(FILE,"<$main_dir/data/$FORM{'number'}");
	$data = <FILE>;
	@wdata= split(/\|/,$data);
	close (FILE);
	if(($wdata[1] eq $FORM{'passwd'}) || ($admin_pass eq $FORM{'passwd'})) {
		unlink("$main_dir/data/$FORM{'number'}");
		&display;
	}
	else {
		&error;
	}
}

sub conf_chg {
	if($FORM{'html_up'} ne ""){
		$FORM{'html_up'} =~ s/\cM//g;
		open(UPDATA, ">$main_dir/up.txt");
		print UPDATA "$FORM{'html_up'}";
		close(UPDATA);
	}

	if($FORM{'html_down'} ne ""){
		$FORM{'html_down'} =~ s/\cM//g;
		open(DOWNDATA, ">$main_dir/down.txt");
		print DOWNDATA "$FORM{'html_down'}";
		close(DOWNDATA);
	}

	$passad = $FORM{'passad'};
	$repassad = $FORM{'repassad'};
	$list_num = $FORM{'list_num'};
	$table_size = $FORM{'table_size'};
	$max_data  = $FORM{'max_data'};
	$table_color = $FORM{'table_color'};
	$cell_color = $FORM{'cell_color'};
	$html = $FORM{'html_ok'};
	$bgcolor = $FORM{'bgcolor'};
	$bgimage = $FORM{'bgimage'};
	$quick_num = $FORM{'quick_num'};
	$good_char = $FORM{'good_char'};
	
	if ($passad ne ""){
		if ($passad eq $repassad){
			$cryptpass = crypt($passad,sp);
			close(PASS);
		}
		else {
			&head;
			print "<center>\n";
			print "<form><hr width=300 noshade>\n";
			print "输入密码啊.\n";
			print "<hr width=300 noshade>\n";
			print "<INPUT type=button value=退后一步 onClick=history.go(-1) style=\"background-color:#ffffff;border:1 solid black;height:20\"></form>\n";
			&foot
		}
	}
	else{
		$cryptpass = $admin_pass;
	}
	open(CFG,">$main_dir/conf.txt");
	print CFG "|$cryptpass|$list_num|$table_size|$max_data|$table_color|$cell_color|$html|$bgcolor|$bgimage|$quick_num|$good_char|";
	close(CFG);

	&head;
	print "<center>\n";
	print "<META HTTP-EQUIV=Refresh CONTENT=0;URL=$cgi_url?id=$FORM{'id'}>\n";
	print "<p>&nbsp;<p>&nbsp;<p>&nbsp;<hr width=300 noshade>\n";
	print "自动返回.\n";
	print "<hr width=300 noshade>\n";
	print "<a href=$cgi_url?id=$FORM{'id'}>按此返回</a>\n";
	&foot
}