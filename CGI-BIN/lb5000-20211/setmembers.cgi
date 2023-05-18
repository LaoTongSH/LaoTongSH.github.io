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
require "lbmail.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setmembers.cgi";

$query = new LBCGI;

&ipbanned; #封杀一些 ip

$action          = $query -> param('action');
$checkaction     = $query -> param('checkaction');
$inletter        = $query -> param('letter');
$inmember        = $query -> param('member');
$inmember        = &unHTML("$inmember");
$action          = &unHTML("$action");

$indellast       = $query -> param('dellast');
$indellast       = &unHTML("$indellast");
$indelposts      = $query -> param('delposts');
$indelposts      = &unHTML("$indelposts");
$indeltime       = $query -> param('deltime');
$indeltime       = &unHTML("$indeltime");
$noofone         = $query -> param('noofone');
$noofone         = &unHTML("$noofone");
$beginone        = $query -> param('beginone');
$beginone        = &unHTML("$beginone");

$noofone      = 2000 if ($noofone !~ /^[0-9]+$/);
$beginone     = 0 if ($beginone !~ /^[0-9]+$/);

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");


opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
my @backupdir = grep(/^backup/, @files2);
$backupdir=@backupdir;
if ($backupdir eq 0) {
	@backupdir = grep(/^BACKUP/, @files2);
	rename("${lbdir}BACKUP","${lbdir}backup");
}
if ($backupdir eq 0) {
	@backupdir = grep(/^Backup/, @files2);
	rename("${lbdir}Backup","${lbdir}backup");
}
$backupdir = $backupdir[0];


print header(-charset=>gb2312);       
&admintitle;
        
&getmember("$inmembername");
        
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 用户管理</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'updatecount'        =>    \&docount,
            'uptop'       	 =>    \&dotop,
            'uptopnext'       	 =>    \&dotopnext,
            'upemot'       	 =>    \&doemot,
            'upuser'       	 =>    \&doava,
            'shareforums'      	 =>    \&doshareforums,
            'dellock'      	 =>    \&dodellock,
            'uponlineuser'     	 =>    \&douponlineuser,
            'upconter'		 =>    \&doupconter,
            'init'        	 =>    \&doinit,
            'viewletter'         =>    \&viewletter,
            'edit'               =>    \&edit,        
            'deletemember'       =>    \&deletemember,
            'unban'              =>    \&unban,
            'delnopost'		 =>    \&delnopost,
            'canceldel'		 =>    \&canceldel,
            'deleteavatar'	 =>    \&deleteavatar,
            'delok'		 =>    \&delok
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &memberoptions; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        

############### delete member

sub deleteavatar {

    $oldmembercode = $membercode;
    &getmember("$inmember");
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>总斑竹无权删除坛主和斑竹资料！</b></td></tr>";
            exit;
    }
    	unlink ("${imagesdir}usravatars/$inmember.gif");
    	unlink ("${imagesdir}usravatars/$inmember.png");
    	unlink ("${imagesdir}usravatars/$inmember.jpg");
    	unlink ("${imagesdir}usravatars/$inmember.swf");
    	unlink ("${imagesdir}usravatars/$inmember.bmp");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>用户头像已经删除了</b>
        </td></tr>
         ~;


} # end routine

##################################################################################
######## Subroutes (forum list)


sub memberoptions {

    $dirtoopen = "$lbdir" . "$memdir";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = sort(@filedata);
    @sortedfile = grep(/cgi$/i,@sortedfile);

    foreach (@sortedfile) {
    	if ($_ =~ /^\w/) {
        $fr = substr($_, 0, 1);
        $fr =~ tr/a-z/A-Z/;
        }
        else {
           $fr =substr($_, 0, 2);
        }
        push(@letters,$fr);
        }

    @sortedletters = sort(@letters);
     
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>请选择一项</b>
    </td>
    </tr>          
    ~;
  if ($membercode eq "ad") {
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=uptop">更新用户排名</a></b><br>
    用户排名其实不会自动更新的，除非你在这儿更新一下。<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=updatecount">重新计算用户总数</a></b><br>
    将更新首页显示的用户数，这样可以用来恢复正确总用户数。<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>删除符合条件的用户</b>(同时会自动更新用户排名)<BR>
    预删除并不会真正删除用户，只是做一个统计。斑竹和坛主是不允许在这里删除的。<BR>
    预删除和真正删除期间，如果用户访问了论坛，那么在真正删除的时候，此用户资料将被保留。<BR>
    真正删除后，用户的所有资料都会丢失，除非你做过备份，否则是无法恢复的。
	<form action="setmembers.cgi" method=get>
        <input type=hidden name="action" value="delnopost">
        <select name="deltime">
        <option value="90" >三个月内没访问和发言
        <option value="121">四个月内没访问和发言
        <option value="151">五个月内没访问和发言
        <option value="182">六个月内没访问和发言
        <option value="212">七个月内没访问和发言
        <option value="243">八个月内没访问和发言
        <option value="273">九个月内没访问和发言
        <option value="304">十个月内没访问和发言
        <option value="365">一年之内没访问和发言
        <option value="730">两年之内没访问和发言
        </select> 且 
        <select name="delposts">
        <option value="0"   >没有发过贴子
        <option value="10"  >总发贴少于 10
        <option value="50"  >总发贴少于 50
        <option value="100" >总发贴少于 100
        <option value="200" >总发贴少于 200
        <option value="300" >总发贴少于 300
        <option value="500" >总发贴少于 500
        <option value="800" >总发贴少于 800
        <option value="1000">总发贴少于 1000
        </select> 且 
        <select name="dellast">
        <option value="no"  >不管访问次数
        <option value="5"   >访问少于 5 次
        <option value="10"  >访问少于 10 次
        <option value="20"  >访问少于 20 次
        <option value="50"  >访问少于 50 次
        <option value="80"  >访问少于 80 次
        <option value="100" >访问少于 100 次
        <option value="200" >访问少于 200 次
        <option value="500" >访问少于 500 次
        </select>
        <input type=submit value="预 删 除">
        </form>
        ~;
	if (-e "${lbdir}data/delmember.cgi") {
	    open (FILE, "${lbdir}data/delmember.cgi");
	    @delmembers = <FILE>;
	    close (FILE);
	    $delmembersize = @delmembers;
	    $delmembersize --;
	    $pretime=$delmembers[0];
	    chomp $pretime;
    	    $nowtime = time;
    	    $nowtime = $nowtime - 3*24*3600;
    	    if ($nowtime > $pretime) {
    	    	$oooput = qq~距离上次预删除时间已经超过３天了 [<a href=$thisprog?action=delok>确定删除</a>]~;
    	    }
    	    else {
    	    	$oooput = qq~距离上次预删除时间还未到３天 [<a href=$thisprog?action=delok>不管，强制删除</a>]~;
    	    }
    	    $pretime=&dateformat($pretime);
    	    print qq~
        	上次预删除时间：$pretime (预删除用户个数： $delmembersize ) [<a href=$thisprog?action=canceldel>取消预删除</a>]<BR>
        	$oooput
    	    ~;
	}
	else {
    	    print qq~
        	预删除文件不存在，现在可以进行预删除。
    	    ~;
	}
    print qq~
    <BR><BR>
    </td>
    </tr>
    ~;
  }
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>查看、编辑、删除、禁止用户</b><br>
    点击下面的字母你可以查看到用户详细资料， 并可编辑、改变用户的信息。<br>
    禁止用户：只要简单的点击“编辑用户”，然后在“用户属性”中选择“禁止用户”就可以。<br>
    删除用户：只要找到用户，点击删除就可以。<br>
	<form action="setmembers.cgi" method=get>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="快速定位">
        </form>
    
    ~;
    
    $nowcount =0;
    foreach (@sortedletters) {
        unless ($_ eq "$ltr") {
            $tempoutput .= qq~<br>~ if ($nowcount == int($nowcount/15)*15);
            $tempoutput .= qq~&nbsp;<a href="$thisprog?action=viewletter&letter=$_">$_</a>&nbsp;~;
            $ltr = "$_";
            $nowcount ++;
       }
    }
    
    print qq~
    注册用户大致列表：<br>$tempoutput
    </td>
    </tr>           
                
                
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><BR>
    <b>注意事项：</b><p>
    如果您希望给您的用户一个自定义的头衔，只要编辑他（她）的资料。<br>
    这个论坛利用储存的发贴数来确定他们的成员身份.<br>
    如果您任命一个用户为版主，而他本身却没有自定义的头衔，那么就会自动添加一个版主头衔。
    如果他已有自定义的等级，那么他的原头衔将被保留。<br>
    版主只能够管理自己的论坛，但是他们也可以在其他论坛中使用 #Moderation Mode 下的功能。<br>
    请确保您所提升的版主是可靠的。<br>
    版主也和坛主一样，不受灌水预防机制限制。<br>
    只有坛主才能够进入管理中心。<br><br>
    如果你禁止了一个用户，那么也同时禁止了用他们原名称、邮件重新注册的可能。
    </td>
    </tr>             
     ~;        
     
     } # end routne
     
     
##################################################################################
######## Subroutes (Do member count)  
sub canceldel {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {
	unlink ("${lbdir}data/delmember.cgi");
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>取消预删除</b><p>
        <font color=#333333>预删除已经被取消！</font>
        </td></tr>
         ~;
}
}

sub docount {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {

    $dirtoopen = "$lbdir" . "$memdir";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @countvar = grep(/\.cgi$/i,@filedata);
    
    $newtotalmembers = @countvar;
    
        require "$lbdir" . "data/boardstats.cgi";
        
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$newtotalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
    
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>计算用户总数</b><p>
                    
        <font color=#333333>当前共有 $newtotalmembers 个注册用户，数据已经更新！</font>
                    
        </td></tr>
         ~;
 }         
} # end routine

sub dotop {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {

    $dirtoopen = "$lbdir" . "$memdir";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @countvar = grep(/\.cgi$/i,@filedata);
    $totaluserdata = @countvar;

    mkdir("${lbdir}$backupdir",0777) if (!(-e "${lbdir}$backupdir"));
    open(FILE,">${lbdir}$backupdir/allname.cgi");
    foreach (@countvar) {
        print FILE "$_\n";
    }
    close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>用户排名初始化</b><br>
                    
        <font color=#333333><B>当前共有 $totaluserdata 个注册用户，准备工作已经完成。</b><BR><BR><BR>
	<form action="setmembers.cgi" method=get>
        <input type=hidden name="action" value="uptopnext">输入每次进行排名的用户数 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="开始排名">
        </form>
	为了减少资源占用，请输入每次进行排名的用户数，默认 2000，<BR>一般不要超过 3000，如果发现进行排名无法正常完成，请尽量减少这个数目，延长排名时间。
	<BR><BR>

        </td></tr>
         ~;
}
} # end routine

sub dotopnext {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {
    $dirtoopen = "$lbdir" . "$memdir";
    $filename = "alluser.pl";
    open(FILE,"${lbdir}$backupdir/allname.cgi");
    @allname = <FILE>;
    close(FILE);
    $allnamenum = @allname;
    if ($beginone < $allnamenum) {
        $lastone = $beginone + $noofone;
        $lastone = $allnamenum if ($lastone > $allnamenum);

        if ($beginone == 0) {
            unlink ("${lbdir}data/lbmember.cgi")  ;
            unlink ("${lbdir}data/lbmember0.cgi")  ;
            unlink ("${lbdir}data/lbmember1.cgi") ;
            unlink ("${lbdir}data/lbmember2.cgi") ;
            unlink ("${lbdir}data/lbmember3.cgi") ;
        }

	open  (MEMFILE, ">>${lbdir}data/lbmember.cgi");
	flock (MEMFILE, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE0, ">>${lbdir}data/lbmember0.cgi");
	flock (MEMFILE0, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE1, ">>${lbdir}data/lbmember1.cgi");
	flock (MEMFILE1, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE2, ">>${lbdir}data/lbmember2.cgi");
	flock (MEMFILE2, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE3, ">>${lbdir}data/lbmember3.cgi");
	flock (MEMFILE3, 2) if ($OS_USED eq "Unix");

	for ($i = $beginone; $i < $lastone; $i ++) {
	    $memberfile = $allname[$i];
	    open (FILE, "${lbdir}$memdir/$memberfile");
	    flock (FILE, 2) if ($OS_USED eq "Unix");
	    $line = <FILE>;
	    close (FILE);
	    chomp $line;
	    @memberdaten = split(/\t/,$line);
	    $username =$memberdaten[0];   
	    $userad=$memberdaten[3];
	    $anzahl = $memberdaten[4];
	    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
	    $anzahl1 = 0 if ($anzahl1 eq "");
	    $anzahl2 = 0 if ($anzahl2 eq "");
	    $anzahl   = $anzahl1 + $anzahl2;
	    $useremail=$memberdaten[5];
	    $date1    = $memberdaten[13];
	    $logtime = $memberdaten[27];
	    $addjy   = $memberdaten[28];
	    $meili   = $memberdaten[29];
	    $mymoney = $memberdaten[30];
	    $postdel = $memberdaten[31];

	    $logtime = 0 if ($logtime eq "");
	    $addjy   = 0 if ($addjy   eq "");
	    $meili   = 0 if ($meili   eq "");
	    $mymoney = 0 if ($mymoney eq "");
	    $postdel = 0 if ($postdel eq "");

	    $birthday = $memberdaten[36];

	    print MEMFILE "$username\t$userad\t$anzahl\t$date1\t$useremail\t\n";   
	    print MEMFILE0 "$username\t$anzahl\t\n";   
	    print MEMFILE1 "$username\t$useremail\t\n";   
	    print MEMFILE2 "$username\t$anzahl1\t$anzahl2\t$logtime\t$postdel\t$addjy\t$meili\t$mymoney\t\n";   
	    print MEMFILE3 "$username\t$birthday\t\n" if (($birthday ne "")&&($birthday ne "//"));  
	} 
	close(MEMFILE3);
	close(MEMFILE2);
	close(MEMFILE1);
	close(MEMFILE0);
	close(MEMFILE);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>计算用户排名</b><p>
        <font color=#333333><B>当前共有 $allnamenum 个注册用户，已经进行排名了 $lastone 个用户。。。</b><BR><BR><BR>
        <font color=#333333>如果无法自动开始下 $noofone 个用户的排名，请点击下面的链接继续<p>
        >> <a href="$thisprog?action=uptopnext&beginone=$lastone&noofone=$noofone">继续进行排名用户</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=uptopnext&beginone=$lastone&noofone=$noofone">
	<BR><BR>

        </td></tr>
         ~;
     }
     else {


open (FILE, "$lbdir/data/lbmember0.cgi");
flock(FILE, 1) if ($OS_USED eq "Unix");
my @file = <FILE>;
close (FILE);
foreach my $line (@file) {
my @tmpuserdetail = split (/\t/, $line);
chomp @tmpuserdetail;
$postundmember {"$tmpuserdetail[0]"} = $tmpuserdetail[1];
}
my @sortiert = reverse sort { $postundmember{$a} <=> $postundmember{$b} } keys(%postundmember);

open  (MEMFILE0, ">${lbdir}data/lbmember0.cgi");
flock (MEMFILE0, 2) if ($OS_USED eq "Unix");
foreach my $member (@sortiert[0 ... 99]) {
    next if ($member eq "");
    print MEMFILE0 "$member\t$postundmember{\"$member\"}\t\n";
}
close(MEMFILE0);


        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>计算用户排名</b><p>
                    
        <font color=#333333>当前共有 $allnamenum 个注册用户，计算用户排名已经结束！<BR><BR>
        </td></tr>
         ~;
     }

}
} # end routine

sub delnopost {
opendir (DIR, "${lbdir}$memdir"); 
@files = readdir(DIR);
closedir (DIR);
@memberfiles = grep(/\.cgi$/i, @files);
$size=@memberfiles;
$size1=0;
$currenttime = time;

$from = "$homename <$adminemail_out>";
$subject = "来自$boardname的重要邮件！！";
$message = "";
$message .= "\n";
$message .= "$boardname\n";
$message .= "$boardurl/$forumsummaryprog\n";
$message .= "------------------------------------------\n\n";
$message .= "系统发现你已经长时间未访问本论坛并发言了，\n";
$message .= "为了释放空间，你的用户名将在３日后删除。\n";
$message .= "如果你想保留你的用户名，请登陆本论坛一次。\n";
$message .= "------------------------------------------\n";
$message .= "LeoBoard 5000 由 www.cgier.com 荣誉出品。\n";

if (-e "${lbdir}data/delmember.cgi") {
    print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>计算用户排名</b><p>
        <font color=#333333>预删除文件存在，不可重复预删除！</font>
        </td></tr>
    ~;
}
else {
  open (FILE, ">${lbdir}data/delmember.cgi");
  print FILE "$currenttime\t\n";
  close (FILE);

  open (MEMFILE, ">${lbdir}data/lbmember.cgi");
  flock (MEMFILE, 2) if ($OS_USED eq "Unix");
  foreach $memberfile (@memberfiles) { # start foreach
    open (FILE, "${lbdir}$memdir/$memberfile");
    flock (FILE, 2) if ($OS_USED eq "Unix");
    $line = <FILE>;
    close (FILE);
    undef $joineddate;
    undef $lastgone;
    undef $anzahl;
    undef $lastpostdate;
    undef $userad;
    undef $visitno;
    undef $anzahl1;
    undef $anzahl2;
    undef $emailaddr;
    undef $membername;
    
    ($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no ,$no ,$no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $addjy, $meili, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $useradd1, $useradd2, $jhmp) = split(/\t/,$line);

    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
    $anzahl = $anzahl1 + $anzahl2;
    ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);

    $lastgone = $lastpost   if ($lastpost > $lastgone);
    $lastgone = $joineddate if ($joineddate > $lastgone);

    $lastgone1 = $lastgone + $indeltime*3600*24;
    $to ="";
    
    if (($lastgone1 <= $currenttime)&&($anzahl <= $indelposts)&&($userad ne "ad")&&($userad ne "mo")&&($userad ne "smo")) {
  	if ($indellast ne "no") {
  	  if ($visitno <= $indellast) {
            open (FILE, ">>${lbdir}data/delmember.cgi");
            flock (FILE, 2) if ($OS_USED eq "Unix");
            print FILE "$memberfile\t$lastgone\t\n";
            close (FILE);
            $size1++;
	    if ($to eq "") { $to = $emailaddr; } else { $to .= ", $emailaddr"; }
	  }
        }
        else {
          open (FILE, ">>${lbdir}data/delmember.cgi");
          flock (FILE, 2) if ($OS_USED eq "Unix");
          print FILE "$memberfile\t$lastgone\t\n";
          close (FILE);
          $size1++;
	  if ($to eq "") { $to = $emailaddr; } else { $to .= ", $emailaddr"; }
        }
    }
    print MEMFILE "$membername\t$userad\t$anzahl\t$joineddate\t\n";
  } 
  close(MEMFILE);

  if (($emailfunctions eq "on")&&($to ne "")) {
      &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
      $delwarn = "";
  }
  else { $delwarn = "<BR><BR><font color=red><B>邮件功能没有打开，所以用户无法接收预删除信息！<B></font>"; }
  unlink ("${lbdir}data/delmember.cgi") if ($size1 eq 0);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>计算用户排名</b><p>
        <font color=#333333>当前共有 $size 个注册用户，排名数据已经更新！</font><BR>
        <font color=#333333>预删除 $size1 个注册用户，排名数据已经更新，３天后可以进入管理区进行真正删除！</font>
        $delwarn
        </td></tr>
         ~;
  }
} # end routine

sub delok {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {

if ($checkaction eq "yes") {
        open (FILE, "${lbdir}data/delmember.cgi");
        @alldelname=<FILE>;
        close (FILE);
 	$delsize = @alldelname;
 	$delno = 0;

$from = "$homename <$adminemail_out>";
$subject = "来自$boardname的重要邮件！！";
$message = "";
$message .= "\n";
$message .= "$boardname\n";
$message .= "$boardurl/$forumsummaryprog\n";
$message .= "------------------------------------------\n\n";
$message .= "系统发现你已经长时间未访问本论坛并发言了，\n";
$message .= "为了释放空间，你的用户名已经被完全删除。\n";
$message .= "------------------------------------------\n";
$to = "";
 	for ($i=1;$i<$delsize;$i++) {
	    ($memberfile, $deltime)= split(/\t/,$alldelname[$i]);
	    open (FILE, "${lbdir}$memdir/$memberfile");
    	    flock (FILE, 2) if ($OS_USED eq "Unix");
    	    $line = <FILE>;
    	    close (FILE);
	    undef $joineddate;
	    undef $lastgone;
	    undef $anzahl;
	    undef $lastpostdate;
	    undef $userad;
	    undef $visitno;
	    undef $anzahl1;
	    undef $anzahl2;
	    undef $emailaddr;
	    undef $membername;

    	    ($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no ,$no ,$no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $addjy, $meili, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $useradd1, $useradd2, $jhmp) = split(/\t/,$line);

	    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
	    $anzahl = $anzahl1 + $anzahl2;
	    ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	    $lastgone = $lastpost   if ($lastpost > $lastgone);
	    $lastgone = $joineddate if ($joineddate > $lastgone);
	    
	    if ($lastgone <= $deltime) {
	        $membername =~ s/ /\_/isg;
		$membername =~ tr/A-Z/a-z/;

        	$filetounlink = "$lbdir" . "$memdir/$membername.cgi";
	        unlink $filetounlink;

	        $filetounlink = "$lbdir" . "$msgdir/in/$membername" . "_msg.cgi";
        	unlink $filetounlink;
	        $filetounlink = "$lbdir" . "$msgdir/out/$membername" . "_out.cgi";
        	unlink $filetounlink;
	        $filetounlink = "$lbdir" . "$msgdir/main/$membername" . "_mian.cgi";
        	unlink $filetounlink;
	    	unlink ("${imagesdir}usravatars/$membername.gif");
    		unlink ("${imagesdir}usravatars/$membername.png");
	    	unlink ("${imagesdir}usravatars/$membername.jpg");
    		unlink ("${imagesdir}usravatars/$membername.swf");
	    	unlink ("${imagesdir}usravatars/$membername.bmp");

	        $filetounlink = "$lbdir" . "memfav/$membername.cgi";
        	unlink $filetounlink;
	        $filetounlink = "$lbdir" . "memfriend/$membername.cgi";
	        unlink $filetounlink;
	        $delno ++;
	  	if ($to eq "") { $to = $emailaddr; } else { $to .= ", $emailaddr"; }
	    }
 	}
 	
  	if (($emailfunctions eq "on")&&($to ne "")) {
            &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
        }
 	
 	&dotop;
 	
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers=$totalmembers - $delno;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        # Delete the database for the member

	unlink ("${lbdir}data/delmember.cgi");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$delno 个过期注册用户已经被完整删除<BR>
        用户库已经全部更新</b>
        </td></tr>
         ~;
}

else {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>警告！！</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>完全删除所有符合条件的预删除用户，点击下面的链接继续。<BR>
        在预删除期间访问过论坛的用户不会被删除<p>
        <p>
        >> <a href="$thisprog?action=delok&checkaction=yes">开始删除</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
        }
}
} # end routine

sub doemot {
unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {

$dirtoopen = "$imagesdir" . "emot";
opendir (DIR, "$dirtoopen"); 
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/gif$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbemot.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);

$dirtoopen = "$imagesdir" . "posticons";
opendir (DIR, "$dirtoopen");
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/gif$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbpost.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化EMOT和POST图片</b><p>
                    
        <font color=#333333>所有EMOT和表情图片已经更新！</font>
                    
        </td></tr>
         ~;
}         
} # end routine
     
sub doava {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {
$dirtoopen = "$imagesdir" . "avatars";
opendir (DIR, "$dirtoopen");
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/gif$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbava.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化用户头像图片</b><p>
                    
        <font color=#333333>所有用户头像图片已经更新！</font>
                    
        </td></tr>
         ~;
}         
} # end routine

sub doupconter {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {
	my $onlinemaxtime = time;
	my $filetomake = "$lbdir" . "data/counter.cgi";
	open(FILE,">$filetomake");
        print FILE "1\t1\t1\t$onlinemaxtime\t";
	close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化在线统计及访问次数</b><p>
                    
        <font color=#333333>访问次数数据已经初始化！</font>
                    
        </td></tr>
         ~;
}         
} # end routine
	
sub douponlineuser {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {
	$currenttime = time;
	my $filetoopen = "$lbdir" . "data/onlinedata.cgi";
        open(FILE9,">$filetoopen");
	print FILE9 "$inmembername\t$currenttime\t$currenttime\t管理区\t保密\t保密\t保密\t管理区\t保密\t$membercode\t" ;
	close (FILE9);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化在线统计及访问次数</b><p>
                    
        <font color=#333333>在线人数统计数据已经初始化！</font>
                    
        </td></tr>
         ~;
}         
} # end routine

sub doshareforums {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {
	my $filetoopen = "$lbdir" . "data/shareforums.cgi";
	unlink $filetoopen;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化论坛联盟数据为空</b><p>
                    
        <font color=#333333>在线联盟数据已经初始化！</font>
                    
        </td></tr>
         ~;
}         
}

sub dodellock {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {
	my $dirtoopen = "$lbdir" . "lock";

opendir (DIRS, "$dirtoopen");
my @files = readdir(DIRS);
closedir (DIRS);
        foreach $file (@files) {
            $filetoremove = "$dirtoopen/$file";
            unlink $filetoremove;
            }

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化锁定文件</b><p>
                    
        <font color=#333333>所有锁定文件已经初始化！</font>
                    
        </td></tr>
         ~;
}         
} # end routine

sub doinit  {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>错误！</b><p>
                    
        <font color=#333333>你没有权限使用这个功能！</font>
                    
        </td></tr>
         ~;
}
else {
print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化论坛数据</b><p>
                    
        <font color=#333333>首次运行论坛必须运行，以后如果更新了论坛表情图片等，也需要运行！</font>
                    
        </td></tr>
        
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>１．<b><a href="$thisprog?action=uptop">初始化用户排名</a></b><br>
    用户排名其实不会自动更新的，除非你在这儿更新一下。<BR><BR>
    </td>
    </tr>
    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>２．<b><a href="$thisprog?action=upemot">初始化表情图片和EMOT图片</a></b><br>
    表情图片和EMOT其实不会自动更新的，除非你在这儿更新一下。<BR><BR>
    </td>
    </tr>
    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>３．<b><a href="$thisprog?action=upuser">初始化用户头像图片</a></b><br>
    用户头像其实不会自动更新的，除非你在这儿更新一下。<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>４．<b><a href="$thisprog?action=uponlineuser">初始化在线统计</a></b><br>
    如果你的在线人数统计数据出错的话，可以在这里初始化一下。<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>５．<b><a href="$thisprog?action=upconter">初始化访问次数</a></b><br>
    如果你的访问次数统计和最大在线人数等数据出错的话，可以在这里初始化一下。<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>６．<b><a href="$thisprog?action=shareforums">初始化联盟数据</a></b><br>
    如果你的联盟数据删除不掉或是出错的话，可以在这里初始化一下。<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>７．<b><a href="$thisprog?action=dellock">初始化锁定文件</a></b><br>
    如果你的锁定文件目录中有多余的或者删除不掉的锁定文件的话，可以在这里初始化一下。<BR><BR>
    </td>
    </tr>

         ~;
}
}     
##################################################################################
######## Subroutes (Do member count) 


sub viewletter {

    $dirtoopen = "$lbdir" . "$memdir";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = sort(@filedata);
    @sortedfile = grep(/cgi$/i,@sortedfile);
    @sortedfile = sort alphabetically(@sortedfile);
    
    foreach (@sortedfile) {
    	if ($_ =~ /^\w/) {
        $fr = substr($_, 0, 1);
        $fr =~ tr/a-z/A-Z/;
        }
        else {
           $fr =substr($_, 0, 2);
        }
        push(@letters,$fr);
        }
    @sortedletters = sort(@letters);
    $nowcount =0;
    foreach (@sortedletters) {
        unless ($_ eq "$ltr") {
            $tempoutput .= qq~<br>~ if ($nowcount == int($nowcount/15)*15);
            $tempoutput .= qq~&nbsp;<a href="$thisprog?action=viewletter&letter=$_">$_</a>&nbsp;~;
            $ltr = "$_";
            $nowcount ++;
        }
    }

     
    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2><center>
    <font color=#990000><b>查看所有以 "$inletter" 开头的用户</b><p>
	<form action="setmembers.cgi" method=get>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="快速定位">
        </form>
    注册用户大致列表：</center>
    $tempoutput
    </td>
    </tr>          
    <tr>
    <td bgcolor=#FFFFFF align=center colspan=2>
    &nbsp;
    </td>
    </tr>          
    ~;
               
               
    foreach (@sortedfile) {
    	if ($_ =~ /^\w/) {
        $frr = substr($_, 0, 1);
        $frr =~ tr/a-z/A-Z/;
        }
        else {
           $frr =substr($_, 0, 2);
        }
        if ($inletter eq $frr) {
            $_ =~ s/\.cgi$//;
            $member = $_;
            &getmember("$member");
            &showmember;
            }
        }
        
   } # end route



##################################################################################
######## Subroutes (Show member) 


sub showmember {

    $joineddate = &longdate("$joineddate");
    
    $cleanmember = $member;
    $cleanmember =~ s/\_/ /g;
    
    ## Sort last post, and where
    
    ($postdate, $posturl, $posttopic) = split(/\%%%/,$lastpostdate);
    
    if ($postdate ne "没有发表过") {
        $postdate = &longdate("$postdate");
        $lastpostdetails = qq~最后发表 <a href="$posturl">$posttopic</a> 在 $postdate~;
        }
        else {
            $lastpostdetails = "没有发表过";
            }

    if ($membercode eq "banned") {
        $unbanlink = qq~ | [<a href="$thisprog?action=unban&member=$member">取消禁止发言</a>]~;
        }
    $totlepostandreply = $numberofposts+$numberofreplys;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2 align=center><font face=$font color=$fontcolormisc><b><font color=$fonthighlight>"$cleanmember"</b> 的详细资料 　 [ <a href="$thisprog?action=edit&member=$member">编辑</a> ] | [ <a href="$thisprog?action=deletemember&member=$member">删除</a> ]$unbanlink</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF width=30%><font color=#333333><b>注册时间：</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户头衔：</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$membertitle</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>最后发表：</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastpostdetails</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>发表总数：</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$totlepostandreply</font> 篇</td></tr>
    <tr>
    <td bgcolor=#FFFFFF>&nbsp;</td>
    <td bgcolor=#FFFFFF>&nbsp;</td></tr>
    
    ~;
    $unbanlink = "";
    } # end routine


##################################################################################
######## Subroutes (Edit member) 


sub edit {
    $oldmembercode = $membercode;
    
    if ($checkaction eq "yes") {
    
    
    $innewpassword      = $query -> param('password');
    $inrating           = $query -> param('rating');
    $inmembertitle      = $query -> param('membertitle');
    $inemailaddress     = $query -> param('emailaddress');
    $inhomepage         = $query -> param('homepage');
    $inaolname          = $query -> param('aolname');
    $inicqnumber        = $query -> param('icqnumber');
    $inlocation         = $query -> param('location');
    $innumberofposts    = $query -> param('numberofposts');
    $innumberofreplys   = $query -> param('numberofreplys');
    $intimedifference   = $query -> param('timedifference');
    $inmembercode       = $query -> param('membercode');
    $invisitno          = $query -> param('visitno');
    $injhmp             = $query -> param('jhmp');
    $inaddjy            = $query -> param('addjy');
    $inmeili            = $query -> param('meili');
    $inmymoney          = $query -> param('mymoney');
    $insex              = $query -> param('sex');
    $ineducation        = $query -> param('education');
    $inmarry            = $query -> param('marry');
    $inwork             = $query -> param('work');
    $inyear             = $query -> param('year');
    $inmonth            = $query -> param('month');
    $inday              = $query -> param('day');
    $inpostdel          = $query -> param('postdel');
    $inrating           = $query -> param('rating');
    $newsignature       = $query -> param('newsignature');
    $inuserflag         = $query -> param('userflag');
    $inusersx           = $query -> param('usersx');
    $inuserxz           = $query -> param('userxz');
    $injoineddate       = $query -> param('joineddate');

    $inlocation = &cleaninput("$inlocation");

    $inyear =~ s/\D//g;
    if (($inyear eq "")||($inmonth eq "")||($inday eq "")) {
    	$inyear  = "";
    	$inmonth = "";
    	$inday   = "";
    }
    $inborn = "$inyear/$inmonth/$inday";
    
    if ($inborn ne "//") { #开始自动判断星座
        if ($inyear-1900 < 0) {$inusersx = "";}	# 无效年份
    	else {
    		$inusersx = "sx".(($inyear-1900) % 12 + 1);
    	}
    	if ($inmonth eq "01") {
    	    if (($inday >= 1)&&($inday <=19)) {
    	        $inuserxz = "z10";
    	    }
    	    else {
    	        $inuserxz = "z11";
    	    }
    	}
        elsif ($inmonth eq "02") {
    	    if (($inday >= 1)&&($inday <=18)) {
    	        $inuserxz = "z11";
    	    }
    	    else {
    	        $inuserxz = "z12";
    	    }
        }
        elsif ($inmonth eq "03") {
    	    if (($inday >= 1)&&($inday <=20)) {
    	        $inuserxz = "z12";
    	    }
    	    else {
    	        $inuserxz = "z1";
    	    }

        }
        elsif ($inmonth eq "04") {
    	    if (($inday >= 1)&&($inday <=19)) {
    	        $inuserxz = "z1";
    	    }
    	    else {
    	        $inuserxz = "z2";
    	    }
        }
        elsif ($inmonth eq "05") {
    	    if (($inday >= 1)&&($inday <=20)) {
    	        $inuserxz = "z2";
    	    }
    	    else {
    	        $inuserxz = "z3";
    	    }
        }
        elsif ($inmonth eq "06") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z3";
    	    }
    	    else {
    	        $inuserxz = "z4";
    	    }
        }
        elsif ($inmonth eq "07") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z4";
    	    }
    	    else {
    	        $inuserxz = "z5";
    	    }
        }
        elsif ($inmonth eq "08") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z5";
    	    }
    	    else {
    	        $inuserxz = "z6";
    	    }
        }
        elsif ($inmonth eq "09") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z6";
    	    }
    	    else {
    	        $inuserxz = "z7";
    	    }
        }
        elsif ($inmonth eq "10") {
    	    if (($inday >= 1)&&($inday <=23)) {
    	        $inuserxz = "z7";
    	    }
    	    else {
    	        $inuserxz = "z8";
    	    }
        }
        elsif ($inmonth eq "11") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z8";
    	    }
    	    else {
    	        $inuserxz = "z9";
    	    }
        }
        elsif ($inmonth eq "12") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z9";
    	    }
    	    else {
    	        $inuserxz = "z10";
    	    }
        }
        
    }

    if ($inpassword eq "")     { $blank = "yes"; }
    if ($inemailaddress eq "") { $blank = "yes"; }
    
    if ($blank eq "yes") {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>必须输入用户密码、邮件地址</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    
    $inmembertitle = "Member" if ($inmembertitle eq "");

    if (length($injhmp) > 20) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>江湖门派的输入请控制在20个字符（10个汉字）内。</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if (length($inmembertitle) > 20) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>个人头衔的输入请控制在20个字符（10个汉字）内。</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if (length($inlocation) > 12) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>来自的输入请控制在12个字符（6个汉字）内。</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if ((($inmembercode eq "ad")||($inmembercode eq "smo")||($inmembercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>总斑竹无权提升任何人为坛主和斑竹！</b></td></tr>";
            exit;
    }

    if ($injhmp eq "") { $jhmp = "无门无派"; }
    else { $jhmp = ($jhmp); }
    if ($inrating eq "") { $inrating = 0; }
    elsif ($inrating > $maxweiwang) { $inrating = $maxweiwang; }
    elsif ($inrating < -5) { $inrating = -5; $inmembercode = "banned"; }
        
        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE,"$filetoopen");
        @forums = <FILE>;
        close(FILE);
        
        foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $trash) = split(/\t/,$forum);
            $namekey = "allow" . "$forumid";
            $tocheck = $query -> param("$namekey");
            if ($tocheck eq "yes") {
                $allowedforums2 .= "$forumid=$tocheck&";
                }
            }
            
        &getmember("$inmember");
    
        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;


        if ($inmembercode eq "banned") {
            $filetoopen = "$lbdir" . "data/banemaillist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$inemailaddress\t";
            close(FILE);
            $filetoopen = "$lbdir" . "data/baniplist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$ipaddress\t";
            close(FILE);
            $banresult = "禁止 $membername 发言成功";
       }


        $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$innewpassword\t$inmembertitle\t$inmembercode\t$innumberofposts|$innumberofreplys\t$inemailaddress\t$showemail\t$ipaddress\t$inhomepage\t$inaolname\t$inicqnumber\t$inlocation\t$interests\t$injoineddate\t$lastpostdate\t$newsignature\t$intimedifference\t$allowedforums2\t$useravatar\t$inuserflag\t$inuserxz\t$inusersx\t$personalavatar\t$personalwidth\t$personalheight\t$inrating\t$lastgone\t$invisitno\t$inaddjy\t$inmeili\t$inmymoney\t$inpostdel\t$insex\t$ineducation\t$inmarry\t$inwork\t$inborn\t$useradd1\t$useradd2\t$injhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

                print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>所有信息已经保存</b><br><br>$banresult<br>
                </td></tr>
                ~;
    
    }
    
    else {
    
    $filetoopen = "$lbdir" . "data/allforums.cgi";
         open(FILE,"$filetoopen");
         @forums = <FILE>;
         close(FILE);

         
         foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);   
            if ($privateforum eq "yes") { 
                $grab = "$forumid\t$forumname";
                push(@newforums, $grab);
                }
            }
        $cleanmember = $inmember;
        $cleanmember =~ s/\_/ /g;
    
        &getmember("$inmember");
        if($privateforums) {
            @private = split(/&/,$privateforums);
            foreach $accessallowed (@private) {
                chomp $accessallowed;
                ($access, $value) = split(/=/,$accessallowed);
                $allowedentry2{$access} = $value;
                }
            }
    
        @allowedforums = sort alphabetically(@newforums);
        foreach $line (@allowedforums) {
            ($forumid, $forumname) = split(/\t/,$line);
            if ($allowedentry2{$forumid} eq "yes") { $checked = " checked"; }
            else { $checked = ""; }
            $privateoutput .= qq~<input type="checkbox" name="allow$forumid" value="yes" $checked>$forumname<br>\n~;
            }
            
    $memberstateoutput = qq~<select name="membercode"><option value="me">一般用户<option value="rz">认证用户<option value="banned">禁止此用户发言<option value="masked">屏蔽此用户贴子<option value="mo">分论坛版主<option value="smo">论坛总版主 *<option value="ad">坛主 **</select>~;
    
    $memberstateoutput =~ s/value=\"$membercode\"/value=\"$membercode\" selected/g;
        if ($userregistered eq "no") {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>无此用户！</b></td></tr>";
            exit;
        }
    
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>总斑竹无权查看坛主和斑竹资料！</b></td></tr>";
            exit;
    }
$userflag = "blank" if ($userflag eq "");
$flaghtml = qq~
<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>所在国家:</b></td>
<td bgcolor=#ffffff>
<select name="userflag" size=1 onChange="showflag()">
<option value="blank">保密</option>
<option value="China">中国</option>
<option value="Angola">安哥拉</option>
<option value="Antigua">安提瓜</option>
<option value="Argentina">阿根廷</option>
<option value="Armenia">亚美尼亚</option>
<option value="Australia">澳大利亚</option>
<option value="Austria">奥地利</option>
<option value="Bahamas">巴哈马</option>
<option value="Bahrain">巴林</option>
<option value="Bangladesh">孟加拉</option>
<option value="Barbados">巴巴多斯</option>
<option value="Belgium">比利时</option>
<option value="Bermuda">百慕大</option>
<option value="Bolivia">玻利维亚</option>
<option value="Brazil">巴西</option>
<option value="Brunei">文莱</option>
<option value="Canada">加拿大</option>
<option value="Chile">智利</option>
<option value="Colombia">哥伦比亚</option>
<option value="Croatia">克罗地亚</option>
<option value="Cuba">古巴</option>
<option value="Cyprus">塞浦路斯</option>
<option value="Czech_Republic">捷克斯洛伐克</option>
<option value="Denmark">丹麦</option>
<option value="Dominican_Republic">多米尼加</option>
<option value="Ecuador">厄瓜多尔</option>
<option value="Egypt">埃及</option>
<option value="Estonia">爱沙尼亚</option>
<option value="Finland">芬兰</option>
<option value="France">法国</option>
<option value="Germany">德国</option>
<option value="Great_Britain">英国</option>
<option value="Greece">希腊</option>
<option value="Guatemala">危地马拉</option>
<option value="Honduras">洪都拉斯</option>
<option value="Hungary">匈牙利</option>
<option value="Iceland">冰岛</option>
<option value="India">印度</option>
<option value="Indonesia">印度尼西亚</option>
<option value="Iran">伊朗</option>
<option value="Iraq">伊拉克</option>
<option value="Ireland">爱尔兰</option>
<option value="Israel">以色列</option>
<option value="Italy">意大利</option>
<option value="Jamaica">牙买加</option>
<option value="Japan">日本</option>
<option value="Jordan">约旦</option>
<option value="Kazakstan">哈萨克</option>
<option value="Kenya">肯尼亚</option>
<option value="Kuwait">科威特</option>
<option value="Latvia">拉脱维亚</option>
<option value="Lebanon">黎巴嫩</option>
<option value="Lithuania">立陶宛</option>
<option value="Malaysia">马来西亚</option>
<option value="Malawi">马拉维</option>
<option value="Malta">马耳他</option>
<option value="Mauritius">毛里求斯</option>
<option value="Morocco">摩洛哥</option>
<option value="Mozambique">莫桑比克</option>
<option value="Netherlands">荷兰</option>
<option value="New_Zealand">新西兰</option>
<option value="Nicaragua">尼加拉瓜</option>
<option value="Nigeria">尼日利亚</option>
<option value="Norway">挪威</option>
<option value="Pakistan">巴基斯坦</option>
<option value="Panama">巴拿马</option>
<option value="Paraguay">巴拉圭</option>
<option value="Peru">秘鲁</option>
<option value="Poland">波兰</option>
<option value="Portugal">葡萄牙</option>
<option value="Romania">罗马尼亚</option>
<option value="Russia">俄国</option>
<option value="Saudi_Arabia">沙特阿拉伯</option>
<option value="Singapore">新加坡</option>
<option value="Slovakia">斯洛伐克</option>
<option value="Slovenia">斯洛文尼亚</option>
<option value="Solomon_Islands">所罗门</option>
<option value="Somalia">索马里</option>
<option value="South_Africa">南非</option>
<option value="South_Korea">韩国</option>
<option value="Spain">西班牙</option>
<option value="Sri_Lanka">印度</option>
<option value="Surinam">苏里南</option>
<option value="Sweden">瑞典</option>
<option value="Switzerland">瑞士</option>
<option value="Thailand">泰国</option>
<option value="Trinidad_Tobago">多巴哥</option>
<option value="Turkey">土耳其</option>
<option value="Ukraine">乌克兰</option>
<option value="United_Arab_Emirates">阿拉伯联合酋长国</option>
<option value="United_States">美国</option>
<option value="Uruguay">乌拉圭</option>
<option value="Venezuela">委内瑞拉</option>
<option value="Yugoslavia">南斯拉夫</option>
<option value="Zambia">赞比亚</option>
<option value="Zimbabwe">津巴布韦</option>
</select>
<img src="$imagesurl/flags/$userflag.gif" name="userflags" border=0 height=14 width=21>
</td></tr>
~;
$flaghtml =~ s/value=\"$userflag\"/value=\"$userflag\" selected/;

        if ($userxz eq "") {$userxz = "blank"};
        $xzhtml =qq~
        <SCRIPT language=javascript>
        function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>所属星座：</b>请选择你所属的星座。<br>如果输入了生日的话，那么此项无效！</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"z1\">白羊座(3月21--4月19日)</OPTION> <OPTION value=\"z2\">金牛座(4月20--5月20日)</OPTION> <OPTION value=\"z3\">双子座(5月21--6月21日)</OPTION> <OPTION value=\"z4\">巨蟹座(6月22--7月22日)</OPTION> <OPTION value=\"z5\">狮子座(7月23--8月22日)</OPTION> <OPTION value=\"z6\">处女座(8月23--9月22日)</OPTION> <OPTION value=\"z7\">天秤座(9月23--10月23日)</OPTION> <OPTION value=\"z8\">天蝎座(10月24--11月21日)</OPTION> <OPTION value=\"z9\">射手座(11月22--12月21日)</OPTION> <OPTION value=\"z10\">魔羯座(12月22--1月19日)</OPTION> <OPTION value=\"z11\">水瓶座(1月20--2月18日)</OPTION> <OPTION value=\"z12\">双鱼座(2月19--3月20日)</OPTION></SELECT> <IMG border=0 height=15 name=userxzs src=$imagesurl/star/$userxz.gif width=15 align=absmiddle>
        </TD></TR>
	~;
        $xzhtml =~ s/value=\"$userxz\"/value=\"$userxz\" selected/;

        if ($usersx eq "") {$usersx = "blank"};
        $sxhtml =qq~
        <SCRIPT language=javascript>
        function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>所属生肖：</b>请选择你所属的生肖。<br>如果输入了生日的话，那么此项无效！</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"sx1\">子鼠</OPTION> <OPTION value=\"sx2\">丑牛</OPTION> <OPTION value=\"sx3\">寅虎</OPTION> <OPTION value=\"sx4\">卯兔</OPTION> <OPTION value=\"sx5\">辰龙</OPTION> <OPTION value=\"sx6\">巳蛇</OPTION> <OPTION value=\"sx7\">午马</OPTION> <OPTION value=\"sx8\">未羊</OPTION> <OPTION value=\"sx9\">申猴</OPTION> <OPTION value=\"sx10\">葵鸡</OPTION> <OPTION value=\"sx11\">戌狗</OPTION> <OPTION value=\"sx12\">亥猪</OPTION></SELECT> <IMG border=0 name=usersxs src=$imagesurl/sx/$usersx.gif align=absmiddle>
        </TD></TR>
	~;
        $sxhtml =~ s/value=\"$usersx\"/value=\"$usersx\" selected/;
        if ($avatars eq "on") {
	    if (($personalavatar)&&($personalwidth)&&($personalheight)) { #自定义头像存在
	        if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	            $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>　[ <a href="$thisprog?action=deleteavatar&member=$inmember">删 除 头 像</a> ]);
	        }
	        else {
	            $useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>　[ <a href="$thisprog?action=deleteavatar&member=$inmember">删 除 头 像</a> ]);
	        }
	    }
            elsif (($useravatar ne "noavatar") && ($useravatar)) {
                $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$useravatar.gif" border=0 $defaultwidth $defaultheight>);
            }
            else {$useravatar="没有"; }
        }

  if ($oldmembercode eq "ad") {
    print qq~
    <form action="$thisprog" method=post name="creator">
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>要编辑的用户名称： </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户头衔：</b><br>您可以自定义一个头衔，<br>默认 Member 表示无头衔</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>发表总数：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofposts" value="$numberofposts"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>回复总数：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofreplys" value="$numberofreplys"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>贴子被删除数：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="postdel" value="$postdel"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>密码：</b></td>
    <td bgcolor=#FFFFFF><input type=password name="password" value="$password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>邮件地址/MSN地址：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="emailaddress" value="$emailaddress"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>主页地址：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="homepage" value="$homepage"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>OICQ 号：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="aolname" value="$aolname"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ICQ 号：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="icqnumber" value="$icqnumber"></td>
    </tr>$flaghtml<tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>来自何方：</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="location" value="$location" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>江湖门派:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>个人威望:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 到 $maxweiwang 之间)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>格外经验：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="addjy" value="$addjy" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>格外魅力：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="meili" value="$meili" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>个人签名：</b></td>
    <td bgcolor=#FFFFFF><textarea name="newsignature" cols="60" rows="8">$signature</textarea></td>
    </tr><tr>
	~;

        $tempoutput = "<select name=\"sex\" size=\"1\"><option value=\"no\">保密 </option><option value=\"m\">帅哥 </option><option value=\"f\">美女 </option></select>\n";
        $tempoutput =~ s/value=\"$sex\"/value=\"$sex\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>性别：</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"education\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"小学\">小学 </option><option value=\"初中\">初中 </option><option value=\"高中\">高中</option><option value=\"中专\">中专</option><option value=\"大专\">大专</option><option value=\"本科\">本科</option><option value=\"硕士\">硕士</option><option value=\"博士\">博士</option><option value=\"博士后\">博士后</option></select>\n";
        $tempoutput =~ s/value=\"$education\"/value=\"$education\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>最高学历：</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"marry\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"未婚\">未婚 </option><option value=\"已婚\">已婚 </option><option value=\"离婚\">离婚 </option><option value=\"丧偶\">丧偶 </option></select>\n";
        $tempoutput =~ s/value=\"$marry\"/value=\"$marry\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>婚姻状况：</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"work\" size=\"1\"><option value=\"保密\">保密 </option><option value=\"计算机业\">计算机业 </option><option value=\"金融业\">金融业 </option><option value=\"商业\">商业 </option><option value=\"服务行业\">服务行业 </option><option value=\"教育业\">教育业 </option><option value=\"学生\">学生 </option><option value=\"工程师\">工程师 </option><option value=\"主管，经理\">主管，经理 </option><option value=\"政府部门\">政府部门 </option><option value=\"制造业\">制造业 </option><option value=\"销售/广告/市场\">销售/广告/市场 </option><option value=\"失业中\">失业中 </option></select>\n";
        $tempoutput =~ s/value=\"$work\"/value=\"$work\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>职业状况：</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;
	($year, $month, $day) = split(/\//, $born);
        $tempoutput1 = "<select name=\"month\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option></select>\n";
        $tempoutput1 =~ s/value=\"$month\"/value=\"$month\" selected/;

        $tempoutput2 = "<select name=\"day\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option><option value=\"13\">13</option><option value=\"14\">14</option><option value=\"15\">15</option><option value=\"16\">16</option><option value=\"17\">17</option><option value=\"18\">18</option><option value=\"19\">19</option><option value=\"20\">20</option><option value=\"21\">21</option><option value=\"22\">22</option><option value=\"23\">23</option><option value=\"24\">24</option><option value=\"25\">25</option><option value=\"26\">26</option><option value=\"27\">27</option><option value=\"28\">28</option><option value=\"29\">29</option><option value=\"30\">30</option><option value=\"31\">31</option></select>\n";
        $tempoutput2 =~ s/value=\"$day\"/value=\"$day\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>生日：</b>如不想填写，请全部留空。</td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><input type="text" name="year" size=4 maxlength=4 value="$year">年$tempoutput1月$tempoutput2日</font></td>
	</tr>$xzhtml
        </tr>$sxhtml
	~;
	
    print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>格外金钱：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="mymoney" value="$mymoney" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>访问次数：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="visitno" value="$visitno" maxlength=7></td>
    </tr><tr>
    ~;
   $timedifference = 0 if ($timedifference eq '');
   $tempoutput = "<select name=\"timedifference\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
   $tempoutput =~ s/value=\"$timedifference\"/value=\"$timedifference\" selected/;
   $joineddate = $lastgone if ($joineddate eq "");
   $joineddate1 = $joineddate;
   $joineddate = &dateformat($joineddate);
   if ($lastgone ne "") {$lastgone   = &dateformat($lastgone); } else {$lastgone = $joineddate; }
   print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>时差：</b></td>
    <td bgcolor=#FFFFFF>$tempoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>私有论坛访问权限：</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户类型：</b><br>注意：坛主为论坛管理员，有绝对高的权限。<br>所以务必少添加此类型的用户。<br>总版主在任何论坛都具有版主权限，<br>在管理中心只有一定权限。</td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>注册时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>注册时的 IP 地址：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$ipaddress</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>最后访问时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>用户头像：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <input type=hidden name="joineddate" value="$joineddate1">
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmember">删 除 此 用 户</a> ]</td>
    </tr>
    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="提 交" name=submit></form></td>
    </tr>
    ~;
  }
  else {
    $memberstateoutput = qq~<select name="membercode"><option value="me">一般用户<option value="rz">认证用户<option value="banned">禁止此用户发言<option value="masked">屏蔽此用户贴子</select>~;
    $memberstateoutput =~ s/value=\"$membercode\"/value=\"$membercode\" selected/g;
    ($year, $month, $day) = split(/\//, $born);
    if ($lastgone ne "") {$lastgone   = &dateformat($lastgone); } else {$lastgone = $joineddate; }
    $joineddate = $lastgone if ($joineddate eq "");
    print qq~
    <form action="$thisprog" method=post>
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <input type=hidden name="numberofposts" value="$numberofposts">
    <input type=hidden name="numberofreplys" value="$numberofreplys">
    <input type=hidden name="postdel" value="$postdel">
    <input type=hidden name="emailaddress" value="$emailaddress">
    <input type=hidden name="homepage" value="$homepage">
    <input type=hidden name="aolname" value="$aolname">
    <input type=hidden name="icqnumber" value="$icqnumber">
    <input type=hidden name="location" value="$location">
    <input type=hidden name="newsignature" value="$signature">
    <input type=hidden name="sex" value="$sex">
    <input type=hidden name="education" value="$education">
    <input type=hidden name="marry" value="$marry">
    <input type=hidden name="work" value="$work">
    <input type=hidden name="month" value="$month">
    <input type=hidden name="day" value="$day">
    <input type=hidden name="year" value="$year">
    <input type=hidden name="visitno" value="$visitno">
    <input type=hidden name="joineddate" value="$joineddate">
    <input type=hidden name="userflag" value="$userflag">
    <input type=hidden name="usersx" value="$usersx">
    <input type=hidden name="userxz" value="$userxz">
    <input type=hidden name="timedifference" value="$timedifference">

    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>要编辑的用户名称： </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户头衔：</b><br>您可以自定义一个头衔，<br>默认 Member 表示无头衔</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>密码：</b></td>
    <td bgcolor=#FFFFFF><input type=password name="password" value="$password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>江湖门派:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>个人威望:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 到 $maxweiwang 之间)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>格外经验：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="addjy" value="$addjy" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>格外魅力：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="meili" value="$meili" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>格外金钱：</b></td>
    <td bgcolor=#FFFFFF><input type=text name="mymoney" value="$mymoney" maxlength=12></td>
    </tr><tr>
    ~;
   $joineddate = &dateformat($joineddate);
   print qq~
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>私有论坛访问权限：</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>用户类型：</b></td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>注册时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>注册时的 IP 地址：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$ipaddress</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>最后访问时间：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>用户头像：</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmember">删 除 此 用 户</a> ]</td>
    </tr>

    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="提 交" name=submit></form></td>
    </tr>
    ~;
  	
  }  
 } # end else
    
} # endroute


############### delete member

sub deletemember {

    $oldmembercode = $membercode;
    &getmember("$inmember");
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>总斑竹无权删除坛主和斑竹资料！</b></td></tr>";
            exit;
    }
    if ($inmembername eq $inmember) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>自己不能删除自己的资料哟！</b></td></tr>";
            exit;
    }

if ($checkaction eq "yes") {
####################################################
    # Check to see if they were the last member to register

    require "$lbdir" . "data/boardstats.cgi";
        
    if($inmember eq "$lastregisteredmember") { #start

        $dirtoopen = "$lbdir" . "$memdir";
        opendir (DIR, "$dirtoopen"); 
        @filedata = readdir(DIR);
        closedir (DIR);
        @inmembers = grep(/cgi$/i,@filedata);

        local($highest) = 0;

        foreach (@inmembers) {
            $_ =~ s/\.cgi$//g;
            &getmember("$_");
            if (($joineddate > $highest) && ($inmember ne $membername)) {
                $highest = $joineddate;
                $memberkeep = $membername;
                }
        }
        
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers--;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$memberkeep\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        } # end if new/delete member

    else {
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers--;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        } # end if else

        # Delete the database for the member

        $filetounlink = "$lbdir" . "$memdir/$inmember.cgi";
        unlink $filetounlink;

        $filetounlink = "$lbdir" . "$msgdir/in/$inmember" . "_msg.cgi";
        unlink $filetounlink;
        $filetounlink = "$lbdir" . "$msgdir/out/$inmember" . "_out.cgi";
        unlink $filetounlink;
        $filetounlink = "$lbdir" . "$msgdir/main/$inmember" . "_mian.cgi";
       	unlink $filetounlink;

        $filetounlink = "$lbdir" . "memfav/$inmember.cgi";
        unlink $filetounlink;
        $filetounlink = "$lbdir" . "memfriend/$inmember.cgi";
        unlink $filetounlink;
    	unlink ("${imagesdir}usravatars/$inmember.gif");
    	unlink ("${imagesdir}usravatars/$inmember.png");
    	unlink ("${imagesdir}usravatars/$inmember.jpg");
    	unlink ("${imagesdir}usravatars/$inmember.swf");
    	unlink ("${imagesdir}usravatars/$inmember.bmp");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>用户已经从数据库中完全删除了</b>
        </td></tr>
         ~;


} # end checkaction else

else {

        $cleanedmember = $inmember;
        $cleanedmember =~ s/\_/ /g;

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>警告！！</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>只有点击下面的链接才可以删除用户<b>"$cleanedmember"</b><p>
        >> <a href="$thisprog?action=deletemember&checkaction=yes&member=$inmember">删除用户</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
        }

} # end routine

sub unban {

        &getmember("$inmember");
    
        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;

        # Remove from ban lists
            
        $filetoopen = "$lbdir" . "data/banlist.cgi";
        open(FILE,"$filetoopen");
        @bandata = <FILE>;
        close(FILE);

        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE,">$filetoopen");
        flock (FILE, 2) if ($OS_USED eq "Unix");
        foreach (@bandata) {
            chomp $_;
            ($bannedname, $bannedemail) = split(/\t/,$_);
            $bannedname =~ s/\_/ /g;
            unless ($bannedname eq $membername) { print FILE "$_\n"; }
            }
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
            

        $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$password\t$membertitle\tme\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$allowedforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$membername 已经取消禁止发言</b>
        </td></tr>
        ~;

} # end route


print qq~</td></tr></table></body></html>~;
exit;
