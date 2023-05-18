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
use Archive::Tar;
use Cwd;

$query = new LBCGI;
@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/\'//g;
        $theparam =~ s/\"//g;
		      ${$param} = $theparam;
        if ($param ne "action") {
            $printme .= "\$" . "$param = \'$theparam\'\;\n";
            }
	}
$stylesheet =<<__end_of_sheet__;
<style>
<!--
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}
		
	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}
	        
		.t     {	LINE-HEIGHT: 1.4			}
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

-->
</style>
__end_of_sheet__

$thisprog = "install.cgi"; $|=1; 
$XHTML = 0;
if ($action ne "final_step" || !$action) { print header(-charset=>"gb2312"); print "<head><title>LB5000 安装向导 -- CGI 编程者之家</title></head>$stylesheet<body>"; }

if ($action eq "step_two") {
	
	if (-e "${lbdir}cgi-bin.tar"){
	my $cwd = cwd();
        my $tar =  Archive::Tar->new();
        unless ($tar->read("${lbdir}cgi-bin.tar", 0)) {
	        print qq~<td class='w' align='left' width='60%'>cgi-bin.tar不能读取，请检查是否使用二进制模式上传(一定要这个模式上传这个压缩包)</td></tr>~;
            exit;
        }
        chdir $lbdir;
        unless (-w $lbdir){
        chmod (0777,$lbdir) if ($lbdir !~ m/\/cgi-bin\/$/i);	
        opendir (FILE, "."); 
	@filename = readdir(FILE);
	closedir (FILE); 
	foreach (@filename) {
	    next if (($_ eq ".")||($_ eq ".."));
	    chmod(0755,"./$_");
        }
       }	
        my @files = $tar->list_files();
        $tar->extract(@files, $lbdir);
        chdir $cwd;
        }
        if (-e "${lbdir}non-cgi.tar"){
	my $cwd = cwd();
        my $tar =  Archive::Tar->new();
        unless ($tar->read("${lbdir}non-cgi.tar", 0)) {
	        print qq~<td class='w' align='left' width='60%'>non-cgi.tar不能读取，请检查是否使用二进制模式上传(一定要这个模式上传这个压缩包)</td></tr>~;
            exit;
        }
        mkdir($imagesdir,0777);
        chdir $imagesdir;
        unless (-w $imagesdir){
        chmod (0777,$imagesdir);
        opendir (FILE, "."); 
	@filename = readdir(FILE);
	closedir (FILE); 
	foreach (@filename) {
	chmod(0777,"./$_");
        }
	}
        my @files = $tar->list_files();
        $tar->extract(@files, $imagesdir);
        chdir $cwd;
        }
               
$endprint = "1\;\n";

$errorflag = 0;

        $filetomake = "$lbdir" . "data/boardinfo.cgi";

        open(FILE,">$filetomake");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        
#        &chmodfiles;
        
        if (-e $filetomake && -w $filetomake) {
            $saved_variables = qq(<font face="宋体">所有输入的信息已经成功的写入 ${lbdir}data/boardinfo.cgi 文件中。</font>);
            }
            else {
                $saved_variables = qq(<font face="宋体" color="#FF0000">对不起，不能够保存信息。<BR>
                                      请检测您输入的 ${lbdir}data 数据路径是否正确？是不是最后遗漏了除号 '/'？<BR>
                                      如果正确，请检查 'data' 目录属性是否设置正确。请返回修改后重新递交表单一次。);
                                       $errorflag = "1";
                }
      
        $filetocheck = "$lbdir" . "leoboard.cgi";
        if (-e $filetocheck) {
            $found_cgi = qq(<font face="宋体" color="#0000FF">正确</font>);
            }
            else {
                $errorflag = "1"; $found_cgi = qq(<font face="宋体" color="#FF0000">错误 - 找不到 $filetocheck，数据路径是不是最后遗漏了除号 '/'？请返回重新输入正确信息。</font>);
                }

opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
my @memdir = grep(/^members/, @files2);
$memdir=@memdir;
if ($memdir eq 0) {
	@memdir = grep(/^MEMBERS/, @files2);
	rename("${lbdir}MEMBERS","${lbdir}members");
}
if ($memdir eq 0) {
	@memdir = grep(/^Members/, @files2);
	rename("${lbdir}Members","${lbdir}members");
}
$memdir = $memdir[0];

if ($memdir eq "members") {
	srand;
	$x = rand;
	$x = int($x * 10000000);
	$x =sprintf("%08d",$x);
	rename("${lbdir}members","${lbdir}members$x");
	$memdir="members$x"; 
}

opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
my @memdir = grep(/^members/i, @files2);
$memdir = $memdir[0];

        $dirtocheck = "$lbdir" . "data";
        if (-d "$dirtocheck") {
            $datadir = "找到"; 
            $makefile = "$lbdir" . "data/test.txt";
            open (TEST, ">$makefile") or $datawritable = "目录 data 为不可写，请改变属性为 777 。";
            print TEST "-";
            close (TEST);
            $datawritable = "属性为<b>可写</b>！" if (!$datawritable);
            unlink "$makefile";
            } else { $errorflag = "1"; $datadir = "<b>没有找到</b>！"; }

        $dirtocheck = "$lbdir" . "help";
        if (-d "$dirtocheck") {
            $helpdir = "找到"; 
            $makefile = "$lbdir" . "help/test.txt";
            open (TEST, ">$makefile") or $helpwritable = "目录 help 为不可写，请改变属性为 777 。";
            print TEST "-";
            close (TEST);
            $helpwritable = "属性为<b>可写</b>！" if (!$helpwritable);
            unlink "$makefile";
            } else { $helpdir = "<b>没有找到</b>！"; }

        $dirtocheck = "$lbdir" . "$memdir";
        if (-d "$dirtocheck") {
            $membersdir = "找到"; 
            $makefile = "$lbdir" . "$memdir/test.txt";
            open (TEST, ">$makefile") or $memberswritable = "目录 $memdir 为不可写，请改变属性为 777 。";
            print TEST "-";
            close (TEST);
            $memberswritable = "属性为<b>可写</b>！" if (!$memberswritable);
            unlink "$makefile";
            } else { $errorflag = "1"; $membersdir = "<b>没有找到</b>！"; }

        $dirtocheck = "$lbdir" . "messages";
        if (-d "$dirtocheck") {
            $messagesdir = "找到"; 
            $makefile = "$lbdir" . "messages/test.txt";
            open (TEST, ">$makefile") or $messageswritable = "目录 messages 为不可写，请改变属性为 777 。";
            print TEST "-";
            close (TEST);
            $messageswritable = "属性为<b>可写</b>！" if (!$messageswritable);
            unlink "$makefile";
            } else { $errorflag = "1"; $messagesdir = "<b>没有找到</b>！"; }


        $filetocheck = "$imagesdir" . "images/logo.gif";
        if (-e $filetocheck) {
            $found_image = qq(<font face="宋体" color="#0000FF">正确</font>);
            }
            else {
                $errorflag = "1"; $found_image = qq(<font face="宋体" color="#FF0000">错误，请注意路径最后不要遗漏除号 '/'，请点击后退填入正确的信息(是不是你遗漏上传了 images 下的 logo.gif 呢？程序是利用这个文件是否存在来判断你设置是否正确的)。</font>);
                }
          
        $dirtocheck = "$imagesdir" . "images";
        if (-d "$dirtocheck") { $images_dir = "找到！"; } else { $errorflag = "1"; $images_dir = "<b>没有找到</b>！"; } 

        $dirtocheck = "$imagesdir" . "emoticons";
        if (-d "$dirtocheck") { $emoticonsdir = "找到！"; } else { $errorflag = "1"; $emoticonsdir = "<b>没有找到</b>！"; }

        $dirtocheck = "$imagesdir" . "avatars";
        if (-d "$dirtocheck") { $avatarsdir = "找到！"; } else { $errorflag = "1"; $avatarsdir = "<b>没有找到</b>！"; }

        $dirtocheck = "$imagesdir" . "usravatars";
        if (-d "$dirtocheck") { 
            $usravatarsdir = "找到！"; 
            $makefile = "$dirtocheck" . "/test.txt";
            open (TEST, ">$makefile") or $usravatarswritabler = "目录 $dirtocheck 为不可写，请改变属性为 777 。";
            print TEST "-";
            close (TEST);
            $usravatarswritable = "属性为<b>可写</b>！" if (!$usravatarswritable);
            unlink "$makefile";
        } else { $errorflag = "1"; $usravatarsdir = "<b>没有找到</b>！"; }

        $dirtocheck = "$imagesdir" . "usr";
        if (-d "$dirtocheck") { 
        	$usrdir = "找到！"; 
            $makefile = "$dirtocheck" . "/test.txt";
            open (TEST, ">$makefile") or $usrwritabler = "目录 $dirtocheck 为不可写，请改变属性为 777 。";
            print TEST "-";
            close (TEST);
            $usrwritabler = "属性为<b>可写</b>！" if (!$usrwritabler);
            unlink "$makefile";
        	} else { $errorflag = "1"; $usrdir = "<b>没有找到</b>！"; }

        $dirtocheck = "$imagesdir" . "btg";
        if (-d "$dirtocheck") { $btg = "找到！"; } else { $errorflag = "1"; $btg = "<b>没有找到</b>！"; }

        $dirtocheck = "$imagesdir" . "emot";
        if (-d "$dirtocheck") { $emot = "找到！"; } else { $errorflag = "1"; $emot = "<b>没有找到</b>！"; }

        @progs_to_search = ('admincenter.cgi', 'allnews.cgi', 'announcements.cgi', 'checkboard.cgi', 'code.cgi', 'forumoptions.cgi', 'forums.cgi', 'help.cgi', 'install.cgi', 'index.html', 'lb.lib.pl', 'lbadmin.lib.pl', 'lbfriend.cgi', 'lbmail.lib.pl', 'leoboard.cgi', 'loginout.cgi', 'mailmembers.cgi', 'massmsg.cgi', 'memberlist.cgi', 'messanger.cgi', 'misc.cgi', 'newposts.cgi', 'news.cgi', 'noreg.cgi', 'pag.cgi', 'poll.cgi', 'post.cgi', 'postings.cgi', 'postjs.cgi', 'printpage.cgi', 'profile.cgi', 'rateit.cgi', 'register.cgi', 'remmail.cgi', 'search.cgi', 'SendMail.pm.pl', 'setbadwords.cgi', 'setforums.cgi', 'setipbans.cgi', 'setmemberbak.cgi', 'setmembers.cgi', 'setmembertitles.cgi', 'setskin.cgi', 'setstyles.cgi', 'settemplate.cgi', 'setvariables.cgi', 'shareforums.cgi', 'team.cgi', 'topic.cgi', 'visitforum.lib.pl', 'whosonline.cgi', 'data/progs.cgi', 'data/styles.cgi');

        
		print qq(
		    <font size="5" face="宋体" color="#000000">
		    <h1>LB5000 安装向导</b></font></h1><font face="宋体" color="#000000">
		    汉化改进：<a href="mailto:webmaster\@cgier.com">山鹰糊</a>  参与制作:<a href="mailto:info\@cgier.net">花无缺</a><BR>
		    汉化版权：<a href="http://www.cgier.com/">CGI 编程者之家</a></font>
		    <hr noshade color="#000000">
		    <br>
		    <font face="宋体" color="#000000">
		    <b>欢迎使用 LB5000 安装向导！</b>
		    <br><br>
		    <b>第二步：</b> 谢谢您写入信息，下面是尝试安装的结果。<br>如果您得到了错误信息提示，请确定您已经完整上传了本程序，以及目录属性、位置设定正确。</font><br>

		    <hr noshade color="#000000">
		    <font face="宋体" color="#0000FF">
		    <br><b>您键入的安装信息是否正确保存？</b></font>
		    <br>
		    $saved_variables
		    <br><br>
		    <hr noshade color="#000000">
		    <font face="宋体" color="#0000FF">
		    <br><b>路径预览</b></font>
		    <br>
		    <font face="宋体" color="#000000">
		    所有程序(*.cgi)的路径： $lbdir - $found_cgi
		    <br><br>
		    -- 查找 ${lbdir}data　　　 - $datadir - $datawritable<br>
		    -- 查找 ${lbdir}help 　　　- $helpdir - $helpwritable<br>
		    -- 查找 ${lbdir}messages 　- $messagesdir - $messageswritable<br>
		    -- 查找 ${lbdir}$memdir　　- $membersdir - $memberswritable<br>
		    <br>
		    <br>
		    <font face="宋体" color="#000000">
		    所有非 CGI 文件(images)的路径： $imagesdir - $found_image
		    <br><br>
		    -- 查找 ${imagesdir}images　　　- $images_dir<br>
		    -- 查找 ${imagesdir}emoticons 　- $emoticonsdir<br>
		    -- 查找 ${imagesdir}avatars　 　- $avatarsdir<br><br>
		    -- 查找 ${imagesdir}usravatars　- $usravatarsdir - $usravatarswritable<br><br>
		    -- 查找 ${imagesdir}usr　 　    - $usrdir - $usrwritabler<br><br>
		    -- 查找 ${imagesdir}btg　　　 　- $btg<br><br>
		    -- 查找 ${imagesdir}emot　 　 　- $emot<br><br>

		    <hr noshade color="#000000">
		    <font face="宋体" color="#0000FF">
		    <br><b>URL 预览</b></font>
		    <br>
		    <font face="宋体" color="#000000">
		    您输入的图片 URL： $imagesurl
		    <br>
		    <br>
		    -- 查找 $imagesurl/images/announce.gif - <img src="$imagesurl/images/announce.gif" border=0><br>
		    -- 查找 $imagesurl/emoticons/smile.gif - <img src="$imagesurl/emoticons/smile.gif" border=0><br>
		    -- 查找 $imagesurl/avatars/noavatar.gif - <img src="$imagesurl/avatars/noavatar.gif" border=0><br><br>
		    如果您看到的是错误的图片，请检查这个 $imagesurl 路径是否正确，同时也请确定图片文件是否是以 Binary 方式上传的。<BR><BR>
		    );
		    if ($errorflag eq "1") { print qq(<br><br><font color="#FF0000">LB5000 安装向导发现错误，不能够继续。请返回重新填入正确的信息); print "</body></html>"; exit; }

		    
		    print qq(
		    <hr noshade color="#000000">
		    <font face="宋体" color="#0000FF">
		    <b>文件合法性检查</b></font>
		    <br>
		    <br>
		    <font face="宋体" color="#000000">
		    LB5000 安装向导将检查您的所有 CGI 文件是否已上传，并且是以 ASCII 方式上传的
		    <br><br>);

		    foreach (@progs_to_search) {

		        $filetotest = "$lbdir" . "$_";
		        if (-e $filetotest) {
		            open (TEST, "$filetotest");
		            @testfile = <TEST>;
			        close (TEST);
			        if (grep(/\r/, @testfile) && $^O ne "MSWin32") {
				        print "<b>找到 $_ ，但它好像是以 BINARY 方式上传的。请重新以 ASCII 方式上传！</b><br>";
		                }
		                else { print "找到 $_ - 上传正确！<br>"; }
		            }
		            else { print "<b>找不到 $_ ! - 是否上传了？</b><br>"; }

		            } # end foreach

		    print qq(
		        <br>
		        <hr noshade color="#000000">
		        <font face="宋体" color="#0000FF">
		        <br><b>报告结束</b></font>
		        <br>
		        <br>
		        <font face="宋体" color="#000000">
		        LB5000 安装向导已经完成报告。如果您发现错误，请返回重新填写信息。
		        <br>同时，您也可以使用管理员身份在任何时间重新填写信息。
		        <br><br>
		        如果您不确定一些问题，或者出现一些未知的错误，请到 <a href="http://www.cgier.com/"><b>CGI 编程者之家</b></a> 的论坛中提出！
		        <br><br><i>报告结束</i>
		        <br><br>
		        <hr noshade color="#000000">
		        <font face="宋体" color="#0000FF">
		        <br><b>下一步做什么？</b></font>
		        <br>
		        <br>
		        <font face="宋体" color="#000000">
		        <b>如果您是从 LB5000 的早期版本升级的，<a href="admincenter.cgi?action=remove">现在到管理中心界面</a></b>！
		        <br><br>从安全性上考虑，当你进入管理中心的同时，本安装文件将会被自动删除。<br>
		        当本安装文件存在的时候，管理中心是不能运行的！如果自动删除失败，那么请你自行利用 FTP 来删除这个本程序！
		        <br><br>
		        <b>如果你是第一次安装 LB5000，那么请<a href="$thisprog?action=step_three">点击这里进入第三步</a></b>！</font>
		        <br><br><br><br><br>
		        );

                }


elsif ($action eq "step_three") {

    print qq(
    <font size="5" face="宋体" color="#000000">
    <h1>LB5000 安装向导</b></font></h1><font face="宋体" color="#000000">
    汉化改进：<a href="mailto:webmaster\@cgier.com">山鹰糊</a> 参与制作:<a href="mailto:info\@cgier.net">花无缺</a><BR>
    汉化版权：<a href="http://www.cgier.com/">CGI 编程者之家</a></font>
    <hr noshade color="#000000">
     <br>
    <font face="宋体" color="#FF0000">
    <b>你是否以前到过这一步？</b>
    <br><br>
    <font face="宋体" color="#000000">
    <b>如果您是从 LB5000 的早期版本升级的，<a href="admincenter.cgi?action=remove">现在到管理中心界面</a></b>！
    <br><br>如果您运行这一步，您将<b>丢失</b>论坛的所有数据！！！
    <hr noshade color="#000000">
    <br>
    <b>第三步：</b><br>
    最后安装部分。这一步将完成论坛的安装，您将能够进入管理中心界面设置论坛风格、颜色等。
    <br>
    <hr noshade color="#000000">
    <br>
    <font face="宋体" color="#0000FF">
    <b>以管理员身份注册您自己</b></font>
    <br><br>
    <font face="宋体" color="#000000">
    您将以管理员身份注册自己，这样就可以正确访问管理中心界面</font>
    <br><br>
    <form action="$thisprog" method="post">
    <input type="hidden" name="action" value="final_step">
    <font face="宋体" color="#000000">
    输入您的管理员名称：(最大12字符)<br>
    <input type="text" name="membername" maxlength=12>
    <br><br>
    请输入管理员密码：<br>
    <input type="password" name="password_one" maxlength=20>
    <br><br>
    请重输管理员密码：<br>
    <input type="password" name="password_two" maxlength=20>
    <br><br>
    <input type="submit" value="提 交 这 个 信 息">
    </form>
    <hr noshade color="#000000">
    <br>
    <b>请仔细检查所有信息，并请紧记您的名称、密码。</b>
    <br><br>);

    } # end step 3

elsif ($action eq "final_step") {

		$namecookie = cookie(-name    =>   "adminname",
		                     -value   =>   "$membername");

		$passcookie = cookie(-name    =>   "adminpass",
		                     -value   =>   "$password_one");

		print header(-cookie=>[$namecookie, $passcookie],-charset=>"gb2312"); print "<head><title>LB5000 安装向导 -- CGI 编程者之家</title></head>$stylesheet<body>";

		print qq(
		<font size="5" face="宋体" color="#000000">
   		<h1>LB5000 安装向导</b></font></h1><font face="宋体" color="#000000">
		汉化改进：<a href="mailto:webmaster\@cgier.com">山鹰糊</a> 参与制作:<a href="mailto:info\@cgier.net">花无缺</a><BR>
		汉化版权：<a href="http://www.cgier.com/">CGI 编程者之家</a></font>
		<hr noshade color="#000000">
		<br>
		<font face="宋体" color="#000000">
		<b>欢迎使用 LB5000 安装向导！</b>
		<br><br>
		<b>最后一步：</b><br>
		LB5000 安装向导现在建立您的管理员账号。
		<br>
		<hr noshade color="#000000">
		<br>
		);

		require "${lbdir}data/boardinfo.cgi";

		$currenttime = time;
		$blanks = "yes" if (!$membername);
		$blanks = "yes" if (!$password_one);
		$blanks = "yes" if (!$password_two);

		if ($blanks) { print qq(<br><br><font color="#FF0000">请填写完所有选项，使用后退返回上一步。); print "</body></html>"; exit; }
		if ($password_one ne $password_two)  { print qq(<br><br><font color="#FF0000">输入的两次密码不同，请返回上一步重新输入。); print "</body></html>"; exit; }
		if(length($membername)<2)  { print qq(<br><br><font color="#ff0000">管理员用户名太短了！); print "</body></html>"; exit; }
		if($membername =~ /^客人/) { print qq(<br><br><font color="#ff0000">管理员用户名不能为客人字样！);print "</body></html>";exit; }
		if($membername =~ /_/) { print qq(<br><br><font color="#ff0000">请不要在管理员帐号名中使用下划线！); print "</body></html>";exit;}
		if($membername =~ /\t/) { print qq(<br><br><font color="#ff0000">请不要在管理员帐号名中使用特殊字符！);print "</body></html>";exit; }
		if(($password_one =~ /\t/)||($password_two =~ /\t/)) { print qq(<br><br><font color="#ff0000">请不要在密码中使用特殊字符！); print "</body></html>";exit;}
		if(length($password_one)<6) { print qq(<br><br><font color="#ff0000">管理员密码太短了，请更换！密码必须 6 位以上！); print "</body></html>";exit;}
		if ($password_one =~ /^[0-9]+$/) { print qq(<br><br><font color="#ff0000">管理员密码请不要全部为数字，请更换！); print "</body></html>";exit;}

opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
my @memdir = grep(/^members/i, @files2);
$memdir = $memdir[0];

		$memberfilename = $membername;
		$memberfilename =~ y/ /_/;
        	$memberfilename =~ tr/A-Z/a-z/;
		$membersdir = "$lbdir" . "$memdir";

		$filetomake = "$lbdir" . "$memdir/$memberfilename.cgi";

		open (ADMIN, ">$filetomake");
		print ADMIN "$membername\t$password_one\tmember\tad\t0\t$adminemail_in\tno\t保密\t\t\t\t\t\t$currenttime\t\t";
		close (ADMIN);

	    if (-e $filetomake) {
		$filerequire = "$lbdir"."data/boardinfo.cgi";
		if (-e $filerequire) {
		}else {
			 print qq(
			<font face="宋体" color="#FF0000">
			<b>错误！不能够找到 $filerequire 文件！</b>
			<br><br>
			请检查 data 目录属性是否正确： $lbdir/data );
			 print "</body></html>"; exit;
		}
	
		print qq(
		<font face="宋体" color="#000000">
		<b>恭喜，您的 LB5000 已经成功安装好了！</b>
		<br><br>
		现在，您可以<a href="admincenter.cgi?action=remove">进入管理中心</a>设置您的论坛。<br>从安全角度考虑，本自动安装程序将会被自动删除，以免您的论坛受到不安全的威胁！<br>
		同时我们已经安装了两个论坛附加功能:<br>
		1. LB5000 论坛新新贴子，显示整个论坛的最新贴 ver 1.2<br>
		############################################################################<br>
		# 使用办法： allnews.cgi&maxlength=标题长度<br>
		# 例： 在你主页的适当位置加入以下语句<br>
		#      &lt;script src="$boardurl/allnews.cgi&maxlength=20&display=1"&gt;&lt;/script&gt;<br>
		#      这样就可以在相应位置显示整个论坛的最新贴，标题长度 20，显示发贴时间<br>
		#                                            (display=0 表示不显示发贴时间)<br>
		# <br>
		#    对于显示贴子个数，请在 LB5000 中的管理区设置<br>
		#    所有参数均可以省略<br>
		############################################################################<br>
		2. LB5000 分论坛新新贴子 ver 1.2<br>
		###################################################################################<br>
		# 使用办法： news.cgi?forum=分论坛号&max=显示几条贴子&maxlength=标题长度&display=1<br>
		# 例： 在你主页的适当位置加入以下语句<br>
		#      &lt;script src="$boardurl/news.cgi?forum=1&max=10&maxlength=20"&gt;&lt;/script&gt;<br>
		#      这样就可以在相应位置显示1号论坛的最新10个贴子，标题长度为 20，显示发贴时间<br>
		#                                                   (display=0 表示不显示发贴时间)<br>
		#      所有参数均可以省略<br>
		###################################################################################<br>
		3. LB5000 分论坛精华贴子显示 ver 1.2<br>
		###################################################################################<br>
		# 使用办法： newsjh.cgi?forum=分论坛号<br>
		# 例： 在你主页的适当位置加入以下语句<br>
		#      &lt;script src="newsjh.cgi?forum=1"&gt;&lt;/script&gt;<br>
		#      这样就可以在相应位置显示1号论坛的最新20个贴子<br>
		###################################################################################<br>
		4. LB5000 公告显示 ver 1.2<br>
		###################################################################################<br>
		# 使用办法： getanc.cgi<br>
		# 例： 在你主页的适当位置加入以下语句<br>
		#      &lt;script src="getanc.cgi"&gt;&lt;/script&gt;<br>
		#      这样就可以在相应位置显示论坛的最新公告<br>
		###################################################################################<br>
		<br><br>
		还有8个附加功能存放在 addon 目录中，是<br>
		1. bm2lb5000.cgi "UBB=>LB5000 用户资料转换器"<br>
		2. ubb2lb5000.cgi "bm=>LB5000 用户数据转换 v0.2" <br>
		3. yuzi2lb5000.cgi "yuzi BBS2000(3000)=>LB5000 用户资料转换器"<br>
		4. ys2lb5000.cgi "一山草堂 BBS=>LB5000 用户资料转换器"<br>
		5. yaBB2LB5000.cgi "YaBB=>LB5000 用户资料转换器"<br>
		6. bbs2lbt.cgi "yuzi BBS3000=>LB5000 贴子资料转换器"<br>
		7. ys2lbt.cgi "一山草堂 BBS=>LB5000 贴子资料转换器"<br>
		8. u2lbt.cgi  "UBB=>LB5000 贴子资料转换器"<br>
		);
	    }
	    else {
        	print qq(
		<font face="宋体" color="#FF0000">
		<b>错误！不能够建立 admin 文件！</b>
		<br><br>
		请检查 $memdir 目录是否正确： $membersdir );
		 print "</body></html>"; exit;
	    }

      $filetomake = "$lbdir" . "data/boardstats.cgi";
        
        
        
       open(FILE, ">$filetomake");
       print FILE "\$lastregisteredmember = \'$membername\'\;\n";
       print FILE "\$totalmembers = \'1\'\;\n";
       print FILE "\$totalthreads = \'0\'\;\n";
       print FILE "\$totalposts = \'0\'\;\n";
       print FILE "\n1\;";
       close (FILE);

		print qq(
		<br><br>
		<hr noshade color="#000000">
		<font face="宋体" color="#0000FF">
		感谢你使用 LB5000！</font>
		<br><br>
		<font face="宋体" color="#000000">
		我们希望安装向导对您安装本论坛是有帮助的。<br>
		如果您还有其他问题，请参观 <a href="http://www.cgier.com/"><b>CGI 编程者之家</b></a> 的论坛，本站提供 LB5000 的完全技术支持！
		<br><br>
		);

		} # end final step   
    

            else {

			eval '$home = (getpwuid($<))[7];';
			if (!-e "C:/") { $pwd = `pwd`; chop $pwd; }
			if (!eval 'use Cwd;') { eval '$cwd = cwd();'; } else { $cwd = ""; }
			$prog = $0;
			if ($prog =~ m|install\.(\w+)|) { $prog = "install.$1"; $cgi_extension = $1; }
			$b4 = $`;
			$b4 =~ s/\/$//;
			$b4 =~ s/\\$//;
			$document_root = $ENV{'DOCUMENT_ROOT'};
			$document_root =~ s/\/$//;
			$document_root =~ s/\\$//;
			$filename = $ENV{'SCRIPT_FILENAME'};
			$filename =~ s/\/$prog//;
			$filename =~ s/\\$prog//;
			$path = $ENV{'PATH_TRANSLATED'};
			$path =~ s/\/$//;
			$path =~ s/\\$//;
			&check($pwd); &check($b4); &check($home); &check($document_root); &check($filename); &check($path); &check($cwd);
			opendir(CURDIR, "..");
			while ($q = readdir(CURDIR)) { push (@founddir, $q); }
			closedir(CURDIR);
			$true_path =~ s%\\%/%g;
			$true_path =~ s%//%/%g;
			if ($true_path =~ m|(.*)/(.+)|) {
			   $base = $1;
			   $cgi = $2;
			} else {
			   $base = $true_path;
			   $cgi = "cgi-bin";
			}
			$poss_html_dir = "public_html htdocs";
			$unsure_html_dir = "htdoc html www wwwdoc wwwdocs wwwroot httpd doc docs";
			@poss = split(/\s/, $poss_html_dir);
			
			@founddir = grep(!/\./, @founddir);
			$checker = 0;
			foreach $test_dir (@poss) {
			   if (grep(/^$test_dir$/, @founddir)) {
			      $html_dir = "$base/$test_dir/lb5000";
			      $checker = 1;
			      last;
			   }
			}
			if ($checker == 0) {
			   @poss = split(/\s/, $unsure_html_dir);
			   foreach $test_dir (@poss) {
			      if (grep(/^$test_dir$/, @founddir)) {
			      	  if (-e "$base/$test_dir/index.html" || -e "$base/$test_dir/index.htm" || -e "$base/$test_dir/index.php" || -e "$base/$test_dir/index.php3") {
			             $html_dir = "$base/$test_dir/lb5000";
			             if (-e "$base/$test_dir/index.html" || -e "$base/$test_dir/index.htm" || -e "$base/$test_dir/index.php" || -e "$base/$test_dir/index.php3") {
			                $checker = 2;
			                $test_dir_me = $test_dir;
			                last;
			             } else {
			                $checker = 1;
			                last; 
			             }
			          } else {
			             if (-e "$base/$test_dir/index.html" || -e "$base/$test_dir/index.htm" || -e "$base/$test_dir/index.php" || -e "$base/$test_dir/index.php3") {
			                $html_dir = "$base/$test_dir/lb5000";
			                $checker = 2;
			                $test_dir_me = $test_dir;
			                last;
			             } else {
			             	$checker = 1;
			             	last;
			             }
			          }
			      }
			   }
			}
			if ($html_dir eq "") {$html_dir = "$base"; }
			$script_dir = "$true_path";
			$test_ss = "";
			if ($ENV{'SCRIPT_URI'} ne "") {
			   $test_ss = $ENV{'SCRIPT_URI'};
			} elsif ($ENV{'SCRIPT_URL'} ne "") {
			   $test_ss = $ENV{'SCRIPT_URL'};
			} elsif ($ENV{'REQUEST_URI'}) {
			   $test_ss = $ENV{'REQUEST_URI'};
			} elsif ($ENV{'SCRIPT_NAME'} ne "") {
			   $test_ss = $ENV{'SCRIPT_NAME'}; 
			}
			if ($test_ss ne "") {
			   if ($test_ss =~ m|^http://([^/]+)|) { $test_ss = $'; }
			   if ($test_ss =~ m|/$prog|) { $test_ss = $`; }
			   if ($test_ss ne "") { $script_url = "http://$ENV{'HTTP_HOST'}$test_ss"; }
			} else {
			   $script_url = "http://$ENV{'HTTP_HOST'}/$cgi"; 
			}
			if ($script_url =~ m|^http://([^/]+)/~([^/]+)/|) { $uinfo = "~" . $2 . "/"; }
			$html_url = "http://$ENV{'HTTP_HOST'}/$uinfo" . "lb5000";
#			$html_dir =~ s%/%\\%g if $html_dir =~ m|^(\w+):|;
#			$script_dir =~ s%/%\\%g if $script_dir =~ m|^(\w+):|;
			$bdcgi = "$base/$cgi";
			$html_dir =~ s%\\\\%\\%g;
			$script_dir =~ s%\\\\%\\%g;
			$bdcgi =~ s%\\\\%\\%g;
			if (-e "C:/" || $^O eq "MSWin32") { $OS_USED = 'NT'; }
			$adminemail_in = "incoming\@yourdomain.com";
			$adminemail_out = "outgoing\@yourdomain.com";
			$timezone_choice = "<select name=\"timezone\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\" selected>0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
			$time_is_now = localtime;
			$website_url = "http://$ENV{'HTTP_HOST'}";
			$mailprogram = &mailprogram;  #自动测试 Sendmail 路径
                    print qq~
				    <form action="$thisprog" method="post">
				    <input type="hidden" name="action" value="step_two">
				    <font size="5" face="宋体" color="#000000">
				    <h1>LB5000 安装向导</b></font></h1><font face="宋体" color="#000000">
				    汉化改进：<a href="mailto:webmaster\@cgier.com">山鹰糊</a> 参与制作:<a href="mailto:info\@cgier.net">花无缺</a><BR>
		    		    汉化版权：<a href="http://www.cgier.com/">CGI 编程者之家</a></font>
				    <hr noshade color="#000000">
				    <br>
				    <font face="宋体" color="#000000">
				    <b>欢迎使用 LB5000 安装向导！</b>
				    <br><br>
				    <b>第一步：</b> 在递交表单前，请仔细查看整个下面的内容指示，并检查自动提供的数据是否正确！<br>
				    当你递交表单后，本安装向导会检测所有你输入的数据，如果数据输入错误，将会有详细的提示！<br><br>
				    <b>在执行本程序下一步之前，请确定你已经把本程序完整上传，并已经将所有文件的属性设置正确了！</b><br><br>
				    下面的所有设置数据都可以在 LB5000 的管理中心中重新设置。为了安全起见，本程序在成功完成设置任务后，将会自毁。
				    如果你希望重新利用本程序来设置的话，请重新上传运行本程序。</font><br>

				    <hr noshade color="#000000">

				    <br>
				    <font face="宋体" color="#000000">
				    <b>请选择运行本程序的操作系统平台用于文件加锁</b><br>
				    如果你是 Windows 系列的主机，请千万不要选成 Unix，否则会有意想不到的错误发生！<BR>
				    文件加锁可以有效的防止贴子数据丢失等问题，但会影响速度，请自己衡量！<br>
				    <br>
				    <select name="OS_USED">
				    <option value="NT" selected>Windows 系列
				    <option value="Unix">Unix 系列
				    <option value="No">不加锁
				    </select>

				    <br>
				    <br>
				    <hr noshade color="#000000">
				    <br>
				    <font face="宋体" color="#000000">
				    <b>文件路径设置</b><br><br>
				    下面的默认设置仅仅适用于大部分安装本程序的客户，不是所有的客户都适用。如果有错误，请自行修改成正确的值。<font color="#FF0000"><br>
				    请仔细检查所有的设置，如果你对这些设置有任何的疑问，请询问你的主机提供商！</font><br><br>
				    <font color="#FF0000">如果你使用的是 Windows 系列操作系统，请双写反斜杠（比如： c:\\\\path\\\\to\\\\lb5000\\\\），或者使用除号来代替反斜杠（比如：c:/path/to/lb5000/）！
				    <br><br><font color="#000000"><b>设置时请务必在路径的最后加上除号 '/'。</b>
				    <br><br>
				    <font face="宋体" color="#0000FF">
				    <b>设置 *.cgi 脚本的安装路径。</b></font><br>
				    <font face="宋体" color="#000000">
				    在这里设置的是安装“路径”，不是 URL，所以它肯定<B>不是</B> 'http://' 开头的。<br>
				    这个位置包含了所有 LB5000 中的 *.cgi 文件。
				    要注意，下列目录程序会自动建立。
				    <ul>
				    <li>data
				    <li>members
				    <li>messages
				    <li>help
				    </ul>
				    <input type="text" size="70" name="lbdir" value="$script_dir/">
				    
				    <br><br><br>
				    <font face="宋体" color="#0000FF">
				    <b>设置 image 图像文件的安装路径。</b></font><br><br>
				    <font face="宋体" color="#000000">
				    在这里设置的是安装“路径”，不是 URL，所以它肯定<B>不是</B> 'http://' 开头的。<br>
				    这个位置包含了所有 LB5000 中的图像文件。
				    要注意，下列目录程序会自动建立。
				    <ul>
				    <li>images
				    <li>emoticons
				    <li>avatars
				    <li>usravatars
				    <li>usr
				    <li>btg
				    <li>emot
				    </ul>
				    <b>请注意，<B>不要</B>在路径的最后加 'images/' ！</b><BR><BR>
				    
				    <input type="text" size="70" name="imagesdir" value="$html_dir/">
				    <br><BR>

				    <hr noshade color="#000000">
				    <br>
				    <font face="宋体" color="#000000">
				    <b>设置你网站的 URL 路径</b><br><br>
				    下面的默认设置仅仅适用于大部分安装本程序的客户，不是所有的客户都适用。如果有错误，请自行修改成正确的值。<font color="#FF0000"><br>
				    请仔细检查所有的设置，如果你对这些设置有任何的疑问，请询问你的主机提供商！</font><br><br>
				    <b>请不要在每个 URL 地址结尾加反斜杠 '/' ！</b>
				    <br><br>

				    <font face="宋体" color="#0000FF">
				    <b>设置图片文件 URL 路径。</b></font><br>
				    <font face="宋体" color="#000000">
				    这里是 URL 路径。<b>必须</b>以 'http://' 开始。<br>
				    这个路径包含了所有的 LB5000 图片。
				    <br><br>
				    <input type="text" size="70" name="imagesurl" value="$html_url">
				    <br><br><br>
				    
				    <font face="宋体" color="#0000FF">
				    <b>设置您主页的 URL 地址。</b></font><br>
				    <font face="宋体" color="#000000">
				    这里是 URL 路径。<b>必须</b>以 'http://' 开始。<br>
				    简单的说，就是你在浏览器上输入的访问你主页的地址。
				    <br><br>
				    <input type="text" size="70" name="homeurl" value="$website_url">

				    <br><br><br>
				    <font face="宋体" color="#0000FF">
				    <b>LB5000 的 URL 路径。</b></font><br>
				    <font face="宋体" color="#000000">
				    这里是 URL 路径。<b>必须</b>以 'http://' 开始。<br>
				    <b>请不要在结尾加 CGI 文件名。这里是目录地址，不是文件地址。</b>
				    <br><br>
				    <input type="text" size="70" name="boardurl" value="$script_url"><br><br>

				    <hr noshade color="#000000">
				    <br>
				    <font face="宋体" color="#000000">
				    <b>个性化图片和表情自动转换</b><br><br>
				    <font face="宋体" color="#000000">
				    使用个性化图片，每个用户将拥有有自己特色的头像。<br>
				    字符自动转换，会自动将输入的表情字符自动转换成图片形式（如输入 :) 将自动转换成图片形式）。
				    <br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>你是否使用个性化图片？</b></font><br>
				    <font face="宋体" color="#000000">
				    <br>
				    <select name="avatars">
				    <option value="on" selected>使用
				    <option value="off">不使用
				    </select>

				    <br>
				    <br><br>
				    <font face="宋体" color="#0000FF">
				    <b>您是否使用表情自动转换？</b></font><br>
				    <font face="宋体" color="#000000">
				    <br>
				    <select name="emoticons">
				    <option value="on" selected>使用
				    <option value="off">不使用
				    </select><br><br>

				    <hr noshade color="#000000">
				    <br>
				    <font face="宋体" color="#000000">
				    <b>邮件功能</b><br><br>
				    下面的默认设置仅仅适用于大部分安装本程序的客户，不是所有的客户都适用。如果有错误，请自行修改成正确的值。<br><font color="#FF0000">
				    请仔细检查所有的设置，如果你对这些设置有任何的疑问，请询问你的主机提供商！</font>
				    <br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>您是否希望在论坛上使用邮件功能？</b></font><br>
				    <font face="宋体" color="#000000">
				    <br>
				    <select name="emailfunctions">
				    <option value="off">关闭邮件功能
				    <option value="on" selected>使用邮件功能
				    </select>
				    <br><br><br>
				    <font face="宋体" color="#0000FF">
				    <b>您使用何种邮件发送协议？</b></font><br>
				    <font face="宋体" color="#000000">
				    Unix 类主机请选择 Sendmail，Windows 类主机请选择 SMTP 或者 ESMTP，如果你的主机采用了是 Blat 邮件发送程序，那么请选择 Blat。
				    <br><BR>
				    <select name="emailtype">
				    <option value="smtp_mail" selected>SMTP
				    <option value="esmtp_mail">ESMTP
				    <option value="send_mail">Sendmail
				    <option value="blat_mail">Blat
				    </select>
				    <br><br><br>
				    <font face="宋体" color="#0000FF">
				    <b>Sendmail 路径(只有当你选择了 Sendmail 来发信此项才有效)。</b></font><br><br>
				    <input type=text size="60" name="SEND_MAIL" value="$mailprogram">
				    <br><br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>SMTP 服务器(只有当你选择了 SMTP 或 ESMTP 来发信，此项才有效)。</b></font><br><br>
				    <input type=text size="60" name="SMTP_SERVER" value="localhost">
				    <br><br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>SMTP 的端口(只有当你选择了 SMTP 或 ESMTP 来发信此项才有效)。</b></font><br><br>
				    <input type=text size="60" name="SMTP_PORT" value="$SMTP_PORT">
				    <br><br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>ESMTP 的用户名(只有当你选择了 ESMTP 来发信此项才有效)。</b></font><br><br>
				    <input type=text size="60" name="SMTPUSER" value="$SMTPUSER">
				    <br><br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>ESMTP 的密码(只有当你选择了 ESMTP 来发信此项才有效)。</b></font><br><br>
				    <input type=text size="60" name="SMTPPASS" value="$SMTPPASS">
				    <br><br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>您的发送邮件地址。</b></font><br><br>
				    <input type=text size="60" name="adminemail_in" value="$adminemail_in">
				    <br><br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>您的接收邮件地址。</b></font><br><br>
				    <input type=text size="60" name="adminemail_out" value="$adminemail_out">
				    <br><br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>您是否希望使用邮件来发送用户在论坛中的密码？</b></font><br>
				    <font face="宋体" color="#000000">
				    如果你发送邮件是有问题的话，那么请务必不要使用这个功能！！
				    <br><br>
				    <select name="passwordverification">
				    <option value="no" selected>不要
				    <option value="yes" >需要
				    </select><br><br><br>
				    
				    <font face="宋体" color="#0000FF">
				    <b>有新用户注册是否用邮件通知您？</b></font>
				    <br><br>
				    <select name="newusernotify">
				    <option value="no">不要
				    <option value="yes" selected>需要
				    </select><br><br>

				    <hr noshade color="#000000">
				    <br>
				    <font face="宋体" color="#000000">
				    <b>您论坛的详细资料</b><br><br>
				    这里将询问您的 LB5000 论坛的一些详细资料。</font>
				    <br>
				    
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>论坛名称</b></font><br>
				    <input type=text size="60" name="boardname" value="CGI 编程者之家的论坛">
				    <br>

				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>论坛描述</b></font><br>
				    <input type=text size="60" name="boarddescription" value="我的 LB5000 论坛，好酷酷 :)">
				    <br><br>
				    <font face="宋体" color="#0000FF">
				    <b>您的版权信息</b><br>这里不需要加 '&copy\;'，程序会自动产生。<br>
				    &copy\;</font><input type=text size="58" name="copyrightinfo" value="中文版权所有： <a href=http://www.cgier.com>CGI 编程者之家</a>">
				    <br><br>
				    <font face="宋体" color="#0000FF">
				    <b>您的主页名称</b></font><br>
				    <input type=text size="60" name="homename" value="CGI 编程者之家">
				    <br><br><br>
				    <font face="宋体" color="#0000FF">
				    <b>是否采用灌水预防机制？</b></font><br>
				    <font face="宋体" color="#000000">
				    灌水预防机制将控制您的用户在一定的时间内不能重复发贴。 避免了一些用户为了升级而进行的灌水。<BR>
				    但这个功能不会影响论坛的坛主和版主的连续发贴。
				    <br>
				    <br>
				    <select name="floodcontrol">
				    <option value="off">关闭灌水预防机制
				    <option value="on" selected>打开灌水预防机制
				    </select>
				    <br><br>
				    
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>用户发言相隔时间(只有当灌水预防机制启动后，此项才有效)。</b></font><br>
				    <input type=text size="10" name="floodcontrollimit" value="30"> &nbsp; 秒
				    <br><br>

				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>服务器时差设置</b></font><br>
				    <font face="宋体" color="#000000">
				    您的服务器现在时间是 $time_is_now。如果不正确，请使用下面的表单来改变服务器时差。 
				    <br>
				    <br>
				    $timezone_choice 小时
				    <br><br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>您所在的时区</b></font><br><br>
				    <input type=text size="60" name="basetimes" value="北京时间">
				    <br><br>
				    <br>
				    <font face="宋体" color="#0000FF">
				    <b>是否使用论坛公告？</b></font><br>
				    <font face="宋体" color="#000000">
				    您可以在论坛公告中发布论坛的重要说明、信息等。
				    <br>
				    <br>
				    <select name="announcements">
				    <option value="no">不用
				    <option value="yes" selected>使用
				    </select>
				    <br><br><BR>
				    <font face="宋体" color="#0000FF">
				    <b>查看贴子回复的时候，最新的回复是紧跟主题呢？还是放在最后！</b></font><br>
				    <br>
                		    <select name="sticky">
                		    <option value="off" selected>正常顺序，新的放在最后
                		    <option value="on">紧跟主题，新的放在最上面
                		    </select>
				    <br><br><BR>
		
				    <font face="宋体" color="#0000FF">
				    <b>发表贴子、回复贴子后自动转移到？</b></font><br>
				    <br>
				    <select name="refreshurl">
				    <option value="0" selected>自动返回当前论坛
				    <option value="1">自动返回当前贴子
				    </select>
				    <br><br>
				    
				    <font face="宋体" color="#0000FF">
				    <b>支持上传的附件类型</b><br>用,分割</font><br>
				    <br>
				     <input type=text size=40 name="addtype" value="gif,jpg,bmp,zip,png,swf,doc,txt,htm,html">
				    <br><br>
                
				    <hr noshade color="#000000">
				    <br>
				    <font face="宋体" color="#000000">
				    <b>请仔细检查上面您输入的信息</b><br>
				    </font>
				    <br>
				    
				    <input type=submit value="OK，进入下一步">
				    </form>~;
				    }
    print "</body></html>";
    exit(0);

sub check { local ($dr) = @_; return 0 if $dr eq ""; if (-e "$dr/$prog") { $true_path = $dr; return 1; } }

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

sub chmodfiles {
opendir (FILE, "."); 
@filename = readdir(FILE);
closedir (FILE); 
foreach (@filename) {
next if (($_ eq ".")||($_ eq "..")||$_ eq "install.cgi");
chmod(0755,"./$_") if ($_ !~/forum/isg);
}

chmod(0755,"./forums.cgi");
chmod(0755,"./shareforums.cgi");
chmod(0755,"./forumoptions.cgi");
chmod(0755,"./setforums.cgi");
chmod(0777,"data");
chmod(0777,"help");
chmod(0777,"$memdir");
chmod(0777,"memfav");
chmod(0777,"memfriend");
chmod(0777,"backup");
chmod(0777,"lock");
chmod(0777,"forumdata");
chmod(0777,"messages");
chmod(0777,"search");
chmod(0777,"Archive");
chmod(0777,"MIME");

opendir (FILE, "./data"); 
@filename = readdir(FILE);
closedir (FILE); 
foreach (@filename) {
    chmod(0777,"data/$_");
}
opendir (FILE, "./data/skin"); 
@filename = readdir(FILE);
closedir (FILE); 
foreach (@filename) {
    chmod(0777,"data/skin/$_");
}
opendir (FILE, "./Archive"); 
@filename = readdir(FILE);
closedir (FILE); 
foreach (@filename) {
    chmod(0777,"Archive/$_");
}
opendir (FILE, "./MIME"); 
@filename = readdir(FILE);
closedir (FILE); 
foreach (@filename) {
    chmod(0777,"MIME/$_");
}
}
