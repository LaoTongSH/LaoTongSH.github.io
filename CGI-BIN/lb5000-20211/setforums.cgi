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
require "data/mpic.cgi";
require "lb.lib.pl";
require "rebuildlist.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setforums.cgi";

    $query = new LBCGI;

&ipbanned; #封杀一些 ip

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

	@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }



    $action      =  $PARAM{'action'};
    $inforum     =  $PARAM{'forum'};
    $incategory  =  $PARAM{'category'};
    $checkaction =  $PARAM{'checkaction'};

    $new_categoryname     = $PARAM{'categoryname'};
    $new_categorynumber   = $PARAM{'categorynumber'};
    $new_forumname        = $PARAM{'forumname'};
    $new_forumdescription = $PARAM{'forumdescription'};
    $new_forummoderator   = $PARAM{'forummoderator'};
    $new_htmlstate        = $PARAM{'htmlstate'};
    $new_idmbcodestate    = $PARAM{'idmbcodestate'};
    $new_privateforum     = $PARAM{'privateforum'};
    $new_forumpass	  = $PARAM{'forumpass'};
    $new_hiddenforum	  = $PARAM{'hiddenforum'};
    $new_indexforum	  = $PARAM{'indexforum'};
    $new_startnewthreads  = $PARAM{'startnewthreads'};
    $new_forumgraphic     = $PARAM{'forumgraphic'};

    $new_ratings	  = $PARAM{'ratings'};
    $new_teamlogo         = $PARAM{'teamlogo'};
    $new_teamurl          = $PARAM{'teamurl'};


print header(-charset=>gb2312);

&admintitle;

&getmember("$inmembername");

        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { #s1

            my %Mode = (
            'addforum'            =>    \&addforum,
            'processnew'          =>    \&createforum,
            'edit'                =>    \&editform,
            'doedit'              =>    \&doedit,
            'bakcat'              =>    \&bakcat,
            'upcat'              =>     \&upcat,
            'style'               =>    \&styleform,
            'dostyle'             =>    \&dostyle,
            'addcategory'         =>    \&catform,
            'doaddcategory'       =>    \&doaddcategory,
            'editcatname'         =>    \&editcatname,
            'reordercategories'   =>    \&reordercats,
            'updatecount'  	  =>    \&updatecount,
            'recount'             =>    \&recount,
            'reorder'             =>    \&reorder

            );


            if($Mode{$action}) {
               $Mode{$action}->();
               }
                elsif (($action eq "delete") && ($checkaction ne "yes")) { &warning; }
                elsif (($action eq "delete") && ($checkaction eq "yes")) { &deleteforum; }
                else { &forumlist; }

            } #e1

                else {
                    &adminlogin;
                    }


##################################################################################
sub bakcat {
    $filetoopen = "$lbdir" . "data/allforums.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    $size=@forums;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
open(FILE, ">$filetoopen.pl");
foreach (@forums){
print FILE $_;
}
close(FILE);
print qq~
    <tr><td bgcolor=#333333 colspan=3><font color=#FFFFFF>
    <b>欢迎来到论坛管理中心 / 论坛管理</b>
    </td></tr>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>所有分类已经备份</b><br>
    当前论坛$size个已经备份！
    </td></tr>
    ~;
}

sub upcat {
    $filetoopen = "$lbdir" . "data/allforums.cgi";

    open(FILE, "$filetoopen.pl");
    @forums = <FILE>;
    $size=@forums;
    close(FILE);

open(FILE, ">$filetoopen");
foreach (@forums){
print FILE $_;
}
close(FILE);
print qq~
    <tr><td bgcolor=#333333 colspan=3><font color=#FFFFFF>
    <b>欢迎来到论坛管理中心 / 论坛管理</b>
    </td></tr>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>所有分类已经还原</b><br>
    当前论坛$size个已经还原！
    </td></tr>
    ~;
}

######## Subroutes (forum list)
sub updatecount {

    $filetoopen = "$lbdir" . "data/allforums.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $totle1 = 0;
    $totle2 = 0;

    foreach $forum (@forums) {
        chomp $forum;
	next if ($forum eq "");
        (my $tempno,my $no, $no, $no, $no, $no ,$no ,$no ,$no, $no ,$no ,$no, $threads, $posts, $no, $no, $no,$no,$no,$no) = split(/\t/,$forum);
   	next if ($tempno !~ /^[0-9]+$/);
	$totle1 += $threads;
	$totle2 += $posts;
    }
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $filetomake = &stripMETA($filetomake);

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totle1\'\;\n";
        print FILE "\$totalposts = \'$totle2\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

    print qq~
    <tr><td bgcolor=#333333 colspan=3><font color=#FFFFFF>
    <b>欢迎来到论坛管理中心 / 论坛管理</b>
    </td></tr>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>所有信息已经保存</b><br>
    主题总数：$totle1 篇<BR>
    回复总数：$totle2 篇
    </td></tr>
    ~;

}
sub forumlist {
    $highest = 0;
    print qq~
    <tr><td bgcolor=#333333 colspan=3><font color=#FFFFFF>
    <b>欢迎来到论坛管理中心 / 论坛管理</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font color=#333333>
    <b>１．<a href="$thisprog?action=updatecount">重新统计</a>：</b><br>
    对整个论坛的贴子重新统计总数，这样可以修复首页上总数显示的错误。<br><br>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font color=#333333>
    <b>２．<a href="$thisprog?action=bakcat">备份论坛分类</a>/<a href="$thisprog?action=upcat">还原论坛分类</a></b><br>
    对整个论坛的分类进行备份，这样可以修复所有论坛丢失的情况。(论坛也会自动进行备份和恢复)<br><br>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font color=#333333>
    <b>３．注意事项：</b><br>
    在下面，您将看到目前所有的论坛分类。您可以编辑论坛分类名或是增加一个新的论坛到这个分类中。
    也可以编辑或删除目前存在的论坛。您可以对目前的分类重新进行排列。<br>
    </td></tr>
    ~;

    $filetoopen = "$lbdir" . "data/allforums.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    foreach $forum (@forums) { #start foreach @forums
        chomp $forum;
	next if ($forum eq "");
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
    	next if ($forumid !~ /^[0-9]+$/);
        $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$forumid\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
        push (@rearrangedforums, $rearrange);

    } # end foreach (@forums)

       @finalsortedforums = sort({$a<=>$b}@rearrangedforums);

    foreach $sortedforums (@finalsortedforums) { #start foreach @finalsortedforums

        ($categoryplace, $category, $forumname, $forumdescription, $forumid, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$sortedforums);

        if ($categoryplace ne $lastcategoryplace) { #start if $categoryplace
          $has=0;
          foreach (@hascat){
          $has=1 if ($_ eq $categoryplace);
          }
           if ($has ==0){
            print qq~
            <tr>
            <td bgcolor=#FFFFFF colspan=3 ><font color=#333333><hr noshade>
            </td></tr>
            <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font color=#333333>
            分类名： <b>$category</b><td bgcolor=#EEEEEE width=15% align=center nowrap><font color=#333333><a href="$thisprog?action=editcatname&category=$categoryplace">编辑分类名称</a></td><td bgcolor=#EEEEEE width=25%><font color=#333333><a href="$thisprog?action=addforum&category=$categoryplace">增加论坛到此分类中</a></font></td>
            </td></tr>
            ~;
            foreach my $myforums (@rearrangedforums) {
            (my $mycategoryplace, my $category,my $forumname, my $forumdescription, my $forumid, my $threads, my $posts, my $forumgraphic, my $ratings, my $misc,my $forumpass,my $hiddenforum,my $indexforum,my $teamlogo,my $teamurl,my $miscadd1,my $miscadd2,my $miscadd3,my $miscadd4,my $miscad5) = split(/\t/,$myforums);
            if ($categoryplace eq $mycategoryplace){
            print qq~
            <tr>
            <td bgcolor=#FFFFFF colspan=3 nowrap><font color=#333333>
            论坛名： <b>$forumname</b><br>主题数： <b>$threads</b>　<-->　<font color=#333333>回复数： <b>$posts</b><br><br><a href="$thisprog?action=edit&forum=$forumid">编辑</a> | <font color=#333333><a href="$thisprog?action=delete&forum=$forumid">删除</a> | <a href="$thisprog?action=recount&forum=$forumid">重新计算主题和回复数 / 修复</a>| <font color=#333333><a href="$thisprog?action=style&forum=$forumid">自定义风格</a></font>| <font color=#333333><a href="setstyles.cgi?action=delstyle&forum=$forumid">删除自定义风格</a></font>| <font color=#333333><a href="$thisprog?action=reorder&forum=$forumid">分区内排序</a></font></td>
             </font></td></tr>
            ~;
            }
                        }
                 }
            } # end if

            $lastcategoryplace = $categoryplace;
            push (@hascat, $categoryplace);
            if ($categoryplace > $highest) { $highest = $categoryplace; }
            } # end foreach

        $highest++;

        print qq~
        <td bgcolor=#FFFFFF colspan=3 ><font color=#333333><hr noshade>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE colspan=3 align=center><font color=#333333>
        <a href="$thisprog?action=reordercategories">论坛分类重新排序</a>
        　　--　　
        <a href="$thisprog?action=addcategory&category=$highest">增加分类(同时增加一个论坛)</a>
        </font></td>
        </tr>
        </tr></table></td></tr></table>~;

} # end routine.

##################################################################################
######## Recount forum posts


sub recount { #start


        $dirtoopen = "$lbdir" . "forum$inforum";

        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);

        @thd = grep(/thd.cgi$/,@dirdata);
        $topiccount = @thd;


        foreach $topic (@thd) {

            $filetoopen = "$lbdir" . "forum$inforum/$topic";

            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open (FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @threads = <FILE>;
            close (FILE);
            &winunlock($filetoopen) if ($OS_USED eq "Nt");

            $newthreads = @threads;
            $newthreads--;
            $threadcount = $threadcount + $newthreads;
         }

         $threadcount = "0" if (!$threadcount);
         $topiccount  = "0" if (!$topiccount);


         $filetoopen = "$lbdir" . "data/allforums.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         @allforums = <FILE>;
         close(FILE);

         $filetomake = "$lbdir" . "data/allforums.cgi";
         open(FILE, ">$filetomake");
         flock(FILE, 2) if ($OS_USED eq "Unix");
         foreach $forum (@allforums) { #start foreach @forums
         chomp($forum);
 	 next if ($forum eq "");
            ($tempno, $trash) = split(/\t/,$forum);
    	    next if ($tempno !~ /^[0-9]+$/);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    $posts = $threadcount;
                    $threads = $topiccount;
	            $dirtomake = "$lbdir" . "forum$forumid";
	            $filetomake1 = "$dirtomake/foruminfo.cgi";
          	    open(FILE1,">$filetomake1");
                    print FILE1 "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t";
                    close(FILE1);
                    print FILE "$forumid\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }
            else { print FILE "$forum\n"; }
         }
         close(FILE);
         &winunlock($filetomake) if ($OS_USED eq "Nt");

         rebuildLIST(-Forum=>"$inforum");

         print qq~
         <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
         <b>欢迎来到论坛管理中心 / 重计算主题和回复数</b>
         </td></tr>
         <tr>
         <td bgcolor=#FFFFFF colspan=2>
         <font color=#990000>
         <center><b>论坛更新成功</b></center><p>
         主题数： $topiccount<p>
         回复数： $threadcount
         </td></tr></table></td></tr></table>
         ~;


} # routine ends

##################################################################################
######## Subroutes ( Add forum Form )


sub addforum {

        print qq~
        <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 增加论坛</b>
        </td></tr>
        ~;

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @forums = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");


# Find the category name from the number

        foreach (@forums) {
            ($trash, $tempcategoryname, $tempcategoryplace, $trash) = split(/\t/, $_);
            if ($incategory eq $tempcategoryplace) {
                $category = $tempcategoryname;
            }
        }


# Present the form to be filled in


        print qq~

        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>在 '$category' 分类中增加新论坛</b>
        </td></tr>

        <form action="$thisprog" method="post">
        <input type=hidden name="categorynumber" value="$incategory">
        <input type=hidden name="categoryname" value="$category">
        <input type=hidden name="action" value="processnew">
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛名称</b><br>请输入新论坛的名称<BR>(请控制在 20 个汉字内)</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumname" value="$forumname" maxlength=40></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛描述</b><br>请输入新论坛的描述</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛版主</b><br>请输入论坛版主，如果您希望有多个版主，请使用 "," (英文逗号，不是中文逗号)隔开。<BR><B>例如</B>：山鹰糊, 花无缺</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否使用 HTML 标签？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="htmlstate">
        <option value="on">使用<option value="off" selected>不使用</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否使用 LB5000 标签？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="idmbcodestate">
        <option value="on" selected>使用<option value="off">不使用</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否作为私有论坛？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="privateforum">
        <option value="yes">是<option value="no" selected>否</select> 对坛主和总斑竹无效
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>私有论坛密码</b>(只对私有论坛有效)</font></td>
        <td bgcolor=#FFFFFF>
       <input type=text size=12 name="forumpass" value="$forumpass" maxlength=20> 对坛主和总斑竹无效</td>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否隐藏论坛？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="hiddenforum">
        <option value="yes">是<option value="no" selected>否</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否显示导航栏？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="indexforum">
        <option value="yes" selected>是<option value="no" >否</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛性质</b><br>1. 正规论坛-只允许注册会员发言<br>2. 开放论坛-允许所有人发言<br>3. 评论论坛-坛主和版主允许发言，其他注册用户只能回复<br>4. 精华区-只允许版主和坛主发言和操作<br>5. 认证论坛-除坛主和版主外，其他注册用户发言需要认证</font></td>
        <td bgcolor=#FFFFFF>
        <select name="startnewthreads">
        <option value="yes" selected>正规论坛<option value="all">开放论坛<option value="follow">评论论坛<option value="no">精华区</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>允许对贴子投票评分？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="ratings">
        <option value="On">允许<option value="" selected>不允许</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛图片</b><br>请输入图片名称，此图片被用来放置在论坛页面左边菜单下。<BR><b>不要包含 URL 地址或绝对路径！</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumgraphic" value="logo.gif"></td>
        </tr>

	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>队伍图片</b>(如果没有，请保持原样)<br>请输入图片名称，此图片被用来放置在首页面下。<BR><b>不要包含 URL 地址或绝对路径！</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamlogo" value=""></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>队伍网址</b>(如果没有，请保持原样)<br>用来做上面论坛图片的地址链接</td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamurl" value="http://"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
        ~;

} # end route


##################################################################################
######## Subroutes ( Create Forum )


sub createforum {
		&errorout("保密论坛，密码不能空！！") if (($new_privateforum eq "yes")&&($new_forumpass eq ""));
		&errorout("对不起，论坛名字过长，请控制在 20 个汉字内！") if (length($new_forumname) >40);
		&errorout("论坛名字不能空！！") if ($new_forumname eq "");
		&errorout("论坛描述不能空！！") if ($new_forumdescription eq "");
		$new_privateforum = "yes" if ($new_forumpass ne "");

                $filetoopen = "$lbdir" . "data/allforums.cgi";
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
  	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                # Create a new number for the new forum folder, and files.

                foreach (@forums) {
                    ($forumid, $binit) = split(/\t/,$_);
                    if ($forumid > $high) { $high = $forumid; }
                    }

                $high++;

                $newforumid = $high;


                # Lets create the directory.

                $dirtomake = "$lbdir" . "forum$newforumid";
                mkdir ("$dirtomake", 0777);

                # Lets add a file to stop snoops, and to use to see if the forum was created

                $filetomake = "$dirtomake/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);

                $filetomake = "$lbdir" . "boarddata/list$newforumid.cgi";
                open(FILE,">$filetomake");
                close(FILE);

                $filetomake = "$dirtomake/.htaccess";
                open(FILE, ">$filetomake");
                print FILE "AuthUserFile /dev/null\n";
                print FILE "AuthGroupFile /dev/null\n";
                print FILE "AuthName DenyViaWeb\n";
                print FILE "AuthType Basic\n";
                print FILE "\n\n\n\n";
                print FILE "<Limit GET>\n";
                print FILE "order allow,deny\n";
                print FILE "deny from all\n";
                print FILE "</Limit>\n";
                close (FILE);

                $filetomake1 = "$dirtomake/foruminfo.cgi";
                open(FILE,">$filetomake1");
                print FILE "$newforumid\t$new_categoryname\t$new_categorynumber\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t\t\t0\t0\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_miscadd1\t$new_miscadd2\t$new_miscadd3\t$new_miscadd4\t$new_miscad5\t";
                close(FILE);

                $filetoopen = "$lbdir" . "data/allforums.cgi";
		&winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                open(FILE, ">$filetoopen");
                flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $line (@forums) {
                    chomp $line;
                    print FILE "$line\n";
                    }
                print FILE "$newforumid\t$new_categoryname\t$new_categorynumber\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t\t\t0\t0\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_miscadd1\t$new_miscadd2\t$new_miscadd3\t$new_miscadd4\t$new_miscad5\t";
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                $dirtomake1 = "$imagesdir" . "usr/$newforumid";
                mkdir ("$dirtomake1", 0777);

                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 增加论坛结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>
                ~;

                print "<b>详细资料</b><p>\n";
                print "<ul>\n";
                if (-e $dirtomake) {
                print "<li><b>新论坛目录已经建立</b><p>\n";
                    }
                    else {
                        print "<li><b>新论坛目录没有建立</b><p>请查看是否改变了目录属性？请改属性回 777 ！<p>\n";
                        }


                $filetoopen = "$dirtomake/index.html";
                if (-e $filetoopen) {
                    print "<li><b>新论坛 (index.html) 文件建立</b><p>\n";
                    }
                    else {
                        print "<li><b>新论坛 (index.html) 文件没有建立</b><p>请查看是否改变了目录属性？请改属性回 777 ！\n";
                        }
                print "$filetoopen<p>\n";
                print "</ul></td></tr></table></td></tr></table>\n";

} ######## end routine

##################################################################################
######## Subroutes ( Warning of Delete Forum )

sub warning { #start

        print qq~
        <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 删除论坛</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>警告！！</b>
        </td></tr>

        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>如果您确定要删除论坛，那么请点击下面链接<p>
        >> <a href="$thisprog?action=delete&checkaction=yes&forum=$inforum">删除论坛以及论坛下的所有文件</a> <<
        </td></tr>
        </table></td></tr></table>

        ~;

} # end routine

##################################################################################

sub deleteforum { #start

        my $thistime=time;
        &getforum($inforum);
        $thistime=&dateformatshort($thistime);
        $filetomake = "$lbdir" . "data/baddel.cgi";
        open(FILE, ">>$filetomake");
        print FILE "$inmembername\t密码不显示\t$ENV{'REMOTE_ADDR'}\t$ENV{'HTTP_X_FORWARDED_FOR'}\t删除论坛$forumname\t$thistime\t\n";
        close(FILE);
        undef $thistime;

        $dirtoopen = "$lbdir" . "forum$inforum";

        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);

        @thd = grep(/thd.cgi$/,@dirdata);
        $thdcount = @thd;

        $dirtoopen2 = "$imagesdir" . "usr/$inforum";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = @dirdata2;

        foreach $topic (@thd) {

	    $filetoopen = "$lbdir" . "forum$inforum/$topic";

	    &winlock($filetoopen) if ($OS_USED eq "Nt");
            open (FILE, "$filetoopen");
	    flock(FILE, 1) if ($OS_USED eq "Unix");
            @threads = <FILE>;
            close (FILE);
    	    &winunlock($filetoopen) if ($OS_USED eq "Nt");

            $newthreads = @threads;

            $threadcount = $threadcount + $newthreads -1;

            }

        foreach $file (@dirdata) {
            $filetoremove = "$dirtoopen/$file";
            unlink $filetoremove;
            }

        $filetoremove = "$lbdir" . "boarddata/list$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/xzb$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/xzbs$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/lastnum$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/ontop$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/jinghua$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "data/news$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "data/style$inforum.cgi";
        unlink $filetoremove;

         $dirtoremove = "$lbdir" . "forum$inforum";
         rmdir $dirtoremove;

         $dirtoremove = "$imagesdir" . "usr/$inforum";
         rmdir $dirtoremove;

         $filetoopen = "$lbdir" . "data/allforums.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         @forums = <FILE>;
         close(FILE);

         open(FILE,">$filetoopen");
         flock(FILE,2) if ($OS_USED eq "Unix");
         foreach $forum (@forums) {
         chomp $forum;
	 next if ($forum eq "");
            ($forumid,$category,$notneeded,$notneeded) = split(/\t/,$forum);
    	    next if ($forumid !~ /^[0-9]+$/);
                unless ($forumid eq "$inforum") {
                    print FILE "$forum\n";
                    }
                }
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");

        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";

        $totalthreads = $totalthreads - $thdcount;
        $totalposts = $totalposts - $threadcount;

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

                    $threadcount = 0 if ($threadcount eq "");
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 删除论坛结果</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF colspan=2>
                    <font color=#990000>

                    <center><b>论坛已被删除</b></center><p>

                    共有 $thdcount 主题被删除<p>

                    共有 $threadcount 回复被删除

                    </td></tr></table></td></tr></table>
                    ~;


} # routine ends

##################################################################################
sub styleform {

        if ($incategory ne "main"){
         $filerequire = "$lbdir" . "data/style${inforum}.cgi";
        if (-e $filerequire) {
         	require $filerequire;
                }
        if ($incategory ne ""){
        $stylefile = "$lbdir" . "data/skin/$incategory.cgi";
                if (-e $stylefile) {
         	require $stylefile;
        }
        }
        }



        $dirtoopen = "$lbdir" . "data/skin";

        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);
        my $myskin="";
        @thd = grep(/\.cgi$/,@dirdata);
        $topiccount = @thd;
        @thd=sort {$a<=>$b} @thd;
        for (my $i=0;$i<$topiccount;$i++){
       	$thd[$i]=~s /\.cgi//isg;
        $myskin.=qq~<option value="$thd[$i]">风格 [ $thd[$i] ]~;
        }
        $myskin =~ s/value=\"$incategory\"/value=\"$incategory\" selected/;
       &getforum("$inforum");

print qq~
        <tr><td bgcolor=#333333" colspan=3><font color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 编辑论坛风格</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=3>
        <font color=#000000><b>编辑 $forumname 的分论坛风格,<Br>如果你不想更改，请留空选项，不填写！！！</b>
        </td></tr>
        <tr><td bgcolor=#FFFFFF align=center colspan=3><font color=#ffffff>LEOBOARD 5000 VII</font></td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛风格选择</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>系统自带的风格</b><br>你选择后，需要正式确认提交才生效</font></td>
                <td bgcolor=#FFFFFF>
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="style">
                <input type=hidden name="forum" value="$inforum">
                <select name="category"><option value="main">默认风格
                $myskin
                </select>
                <input type=submit value="运 用">
                </form>
                </td></tr>

        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="dostyle">
        <input type=hidden name="forum" value="$inforum">

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛BODY标签</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>控制整个论坛风格的背景颜色或者背景图片等</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>默认：bgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>主页地址</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛页首菜单</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带字体颜色</font></td>
                <td bgcolor=$menufontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menufontcolor" value="$menufontcolor" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带背景颜色</font></td>
                <td bgcolor=$menubackground  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackground" value="$menubackground" size=7 maxlength=7>　默认：#DDDDDD</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带背景图片</font></td>
                <td background=$imagesurl/images/$menubackpic  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackpic" value="$menubackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>菜单带边界颜色</font></td>
                <td bgcolor=$titleborder  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titleborder" value="$titleborder" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>字体外观和颜色</b>
                </font></td>
                </tr>


                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>主字体外观</font></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"font\">\n<option value=\"宋体\">宋体\n<option value=\"仿宋\">仿宋\n<option value=\"楷体\">楷体\n<option value=\"黑体\">黑体\n<option value=\"隶书\">隶书\n<option value=\"幼圆\">幼圆\n</select><p>\n";
                $tempoutput =~ s/value=\"$font\"/value=\"$font\" selected/;
                print qq~
                $tempoutput</td>
                </tr>


                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"最后发贴者"字体颜色</font></td>
                <td bgcolor=$lastpostfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lastpostfontcolor" value="$lastpostfontcolor" size=7 maxlength=7>　默认：#000000</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"加重区"字体颜色</font></td>
                <td bgcolor=$fonthighlight  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fonthighlight" value="$fonthighlight" size=7 maxlength=7>　默认：#990000</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>查看时发表者名称字体</font></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"posternamefont\">\n<option value=\"宋体\">宋体\n<option value=\"仿宋\">仿宋\n<option value=\"楷体\">楷体\n<option value=\"黑体\">黑体\n<option value=\"隶书\">隶书\n<option value=\"幼圆\">幼圆\n</select><p>\n";
                $tempoutput =~ s/value=\"$posternamefont\"/value=\"$posternamefont\" selected/;
                print qq~
                $tempoutput</td>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>一般用户名称字体颜色</font></td>
                <td bgcolor=$posternamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="posternamecolor" value="$posternamecolor" size=7 maxlength=7>　默认：#000066</td>
                </tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font color=#333333>一般用户名称上的光晕颜色</font></td>
		<td bgcolor=$memglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="memglow" value="$memglow" size=7 maxlength=7>　默认：#9898BA</td>
		</tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>坛主名称字体颜色</font></td>
                <td bgcolor=$adminnamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="adminnamecolor" value="$adminnamecolor" size=7 maxlength=7>　默认：#990000</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>坛主名称上的光晕颜色</font></td>
		<td bgcolor=$adminglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="adminglow" value="$adminglow" size=7 maxlength=7>　默认：#9898BA</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>总版主名称字体颜色</font></td>
                <td bgcolor=$smonamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="smonamecolor" value="$smonamecolor" size=7 maxlength=7>　默认：#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>总版主名称上的光晕颜色</font></td>
		<td bgcolor=$smoglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="smoglow" value="$smoglow" size=7 maxlength=7>　默认：#9898BA</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>版主名称字体颜色</font></td>
                <td bgcolor=$teamnamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="teamnamecolor" value="$teamnamecolor" size=7 maxlength=7>　默认：#0000ff</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>版主名称上的光晕颜色</font></td>
		<td bgcolor=$teamglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="teamglow" value="$teamglow" size=7 maxlength=7>　默认：#9898BA</td>
		</tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>过滤和禁言用户名称上的光晕颜色</font></td>
		<td bgcolor=$banglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="banglow" value="$banglow" size=7 maxlength=7>　默认：none</td>
		</tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>所有页面颜色</center></b><br>
                <font color=#333333>这些颜色配置将用于每个页面。用于注册、登陆、在线以及其他页面。
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>主字体颜色</font></td>
                <td bgcolor=$fontcolormisc  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fontcolormisc" value="$fontcolormisc" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色一</font></td>
                <td bgcolor=$miscbackone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbackone" value="$miscbackone" size=7 maxlength=7>　默认：#FFFFFF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色二</font></td>
                <td bgcolor=$miscbacktwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbacktwo" value="$miscbacktwo" size=7 maxlength=7>　默认：#EEEEEE</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景图片(在线名单)</font></td>
                <td background=$imagesurl/images/$otherbackpic width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="otherbackpic" value="$otherbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景图片(论坛图例)</font></td>
                <td background=$imagesurl/images/$otherbackpic1 width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="otherbackpic1" value="$otherbackpic1"></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>表格颜色</center></b><br>
                <font color=#333333>这些颜色大部分用于lbboard.cgi，forums.cgi和topic.cgi
                </td></tr>


                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带背景颜色</font></td>
                <td bgcolor=$catback  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catback" value="$catback" size=7 maxlength=7>　默认：#ebebFF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带背景图片</font></td>
                <td background=$imagesurl/images/$catbackpic  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catbackpic" value="$catbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带字体颜色</font></td>
                <td bgcolor=$catfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catfontcolor" value="$catfontcolor" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>所有表格边界颜色</font></td>
                <td bgcolor=$tablebordercolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablebordercolor" value="$tablebordercolor" size=7 maxlength=7>　默认：#000000</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>所有表格宽度</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablewidth" value="$tablewidth" size=5 maxlength=5>　默认：750</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>标题颜色</center></b><br>
                <font color=#333333>这里颜色配置用于发表第一个主题的标题
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>论坛/主题的标题栏背景颜色</font></td>
                <td bgcolor=$titlecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titlecolor" value="$titlecolor" size=7 maxlength=7>　默认：#acbded</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>论坛/主题的标题栏字体颜色</font></td>
                <td bgcolor=$titlefontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titlefontcolor" value="$titlefontcolor" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>论坛内容颜色</center></b><br>
                <font color=#333333>查看论坛内容时颜色 (forums.cgi)
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容颜色一</font></td>
                <td bgcolor=$forumcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumcolorone" value="$forumcolorone" size=7 maxlength=7>　默认：#f0F3Fa</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容颜色二</font></td>
                <td bgcolor=$forumcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumcolortwo" value="$forumcolortwo" size=7 maxlength=7>　默认：#F2F8FF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容字体颜色</font></td>
                <td bgcolor=$forumfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumfontcolor" value="$forumfontcolor" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>回复颜色</center></b><br>
                <font color=#333333>回复贴子颜色(topic.cgi)
                </td></tr>


                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复颜色一</font></td>
                <td bgcolor=$postcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcolorone" value="$postcolorone" size=7 maxlength=7>　默认：#EFF3F9</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复颜色二</font></td>
                <td bgcolor=$postcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcolortwo" value="$postcolortwo" size=7 maxlength=7>　默认：#F2F4EF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色一</font></td>
                <td bgcolor=$postfontcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolorone" value="$postfontcolorone" size=7 maxlength=7>　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色二</font></td>
                <td bgcolor=$postfontcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolortwo" value="$postfontcolortwo" size=7 maxlength=7>　默认：#555555</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>页面跨度</center></b><br>
                <font color=#333333>每页显示主题的回复数，当一篇主题回复超过一定数量时分页显示 (topic.cgi)
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每页主题数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxthreads" value="$maxthreads" size=3 maxlength=3>　一般为 20 -- 30</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每主题每页的回复数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtopics" value="$maxtopics" size=3 maxlength=3>　一般为 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复数超过多少后就是热门贴？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hottopicmark" value="$hottopicmark" size=3 maxlength=3>　一般为 10 -- 15</td>
                </tr>
                <tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>投票数超过多少后就是热门投票贴？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hotpollmark" value="$hotpollmark" size=3 maxlength=3>　一般为 10 -- 15</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostpic\"><option value=\"off\">不允许<option value=\"on\">允许</select>\n";
                $tempoutput =~ s/value=\"$arrawpostpic\"/value=\"$arrawpostpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>LB5000 标签设置</center></b>(坛主和版主不受此限)<br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许贴图？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostflash\"><option value=\"off\">不允许<option value=\"on\" >允许</select>\n";
                $tempoutput =~ s/value=\"$arrawpostflash\"/value=\"$arrawpostflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许 Flash？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostreal\"><option value=\"off\">不允许<option value=\"on\" >允许</select>\n";
                $tempoutput =~ s/value=\"$arrawpostreal\"/value=\"$arrawpostreal\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许播放 Real 文件？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostmedia\"><option value=\"off\">不允许<option value=\"on\" >允许</select>\n";
                $tempoutput =~ s/value=\"$arrawpostmedia\"/value=\"$arrawpostmedia\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许播放 Media 文件？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostsound\"><option value=\"off\">不允许<option value=\"on\" >允许</select>\n";
                $tempoutput =~ s/value=\"$arrawpostsound\"/value=\"$arrawpostsound\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许声音？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostfontsize\"><option value=\"off\">不允许<option value=\"on\">允许</select>\n";
                $tempoutput =~ s/value=\"$arrawpostfontsize\"/value=\"$arrawpostfontsize\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许改变文字大小？</font></td>
                <td bgcolor=#FFFFFF>
                 $tempoutput
		</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"arrawsignpic\"><option value=\"off\">不允许<option value=\"on\">允许</select>\n";
                $tempoutput =~ s/value=\"$arrawsignpic\"/value=\"$arrawsignpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许贴图？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;
		$tempoutput = "<select name=\"arrawsignflash\"><option value=\"off\">不允许<option value=\"on\">允许</select>\n";
                $tempoutput =~ s/value=\"$arrawsignflash\"/value=\"$arrawsignflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许 Flash？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;


		$tempoutput = "<select name=\"arrawsignsound\"><option value=\"off\">不允许<option value=\"on\">允许</select>\n";
                $tempoutput =~ s/value=\"$arrawsignsound\"/value=\"$arrawsignsound\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许声音？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"arrawsignfontsize\"><option value=\"off\">不允许<option value=\"on\">允许</select>\n";
                $tempoutput =~ s/value=\"$arrawsignfontsize\"/value=\"$arrawsignfontsize\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许改变文字大小？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

		<tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛按钮设置</b> (此图必须在 images 目录下，只能是名称，不可以加 URL 地址或绝对路径)<br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>发新帖按钮图标</font>　(大小：99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newthreadlogo" value="$newthreadlogo" onblur="document.images.i_newthreadlogo.src='$imagesurl/images/'+this.value;">　
                <img src=$imagesurl/images/$newthreadlogo name="i_newthreadlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>发起投票按钮图标</font>　(大小：99*25)</td>
                <td bgcolor=#FFFFFF>
		<input type=text name="newpolllogo" value="$newpolllogo" onblur="document.images.i_newpolllogo.src='$imagesurl/images/'+this.value;">　
                <img src=$imagesurl/images/$newpolllogo name="i_newpolllogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>小字报按钮图标</font>　(大小：99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newxzblogo" value="$newxzblogo" onblur="document.images.i_newxzblogo.src='$imagesurl/images/'+this.value;">　
                <img src=$imagesurl/images/$newxzblogo name="i_newxzblogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复帖子按钮图标</font>　(大小：99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newreplylogo" value="$newreplylogo" onblur="document.images.i_newreplylogo.src='$imagesurl/images/'+this.value;">　
                <img src=$imagesurl/images/$newreplylogo name="i_newreplylogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>原窗口按钮图标</font>　(大小：74*21)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="wlogo" value="$wlogo" onblur="document.images.i_wlogo.src='$imagesurl/images/'+this.value;">　
                <img src=$imagesurl/images/$wlogo name="i_wlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>新窗口按钮图标</font>　(大小：74*21)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="nwlogo" value="$nwlogo" onblur="document.images.i_nwlogo.src='$imagesurl/images/'+this.value;">　
                <img src=$imagesurl/images/$nwlogo name="i_nwlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>帮助按钮图标</font>　(大小：不限)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="help_blogo" value="$help_blogo" onblur="document.images.i_help_blogo.src='$imagesurl/images/'+this.value;">　
                <img src=$imagesurl/images/$help_blogo name="i_help_blogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>新贴最后的 new 图标</font>　(大小：不限)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="new_blogo" value="$new_blogo" onblur="document.images.i_new_blogo.src='$imagesurl/images/'+this.value;">　
                <img src=$imagesurl/images/$new_blogo name="i_new_blogo"></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>论坛特殊样式设置</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中每个表情允许显示的次数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsmail" value="$maxsmail" size=2 maxlength=2>　一般 2 -- 5 个左右啦</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复时候默认列出的最后回复个数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxlistpost" value="$maxlistpost" size=2 maxlength=2>　一般 5 -- 8 个左右啦</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>允许固定在顶端的主题数？<br>可以固定几个重要话题在论坛的最上面。</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtoptopic" value="$maxtoptopic" size=2 maxlength=2>　一般 1 -- 5 个左右啦</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>最后贴子预览的字符数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsavepost" value="$maxsavepost" size=3 maxlength=3>　不要超过 50，否则严重影响速度</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛投票贴子中允许的最大项目数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpollitem" value="$maxpollitem" size=2 maxlength=2>　请设置 5 - 50 之间</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>广告设置</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>贴子尾部广告代码</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adfoot" rows="5" cols="40">$adfoot</textarea><BR><BR>
                </td>
                </tr>
		~;

               $tempoutput = "<select name=\"forumimagead\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n";
               $tempoutput =~ s/value=\"$forumimagead\"/value=\"$forumimagead\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=宋体 color=#333333><b>是否使用分论坛浮动广告</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>分论坛浮动广告图片 URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>分论坛浮动广告连接目标网址</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink" value="$adimagelink"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>分论坛浮动广告图片宽度</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth" value="$adimagewidth" maxlength=3>&nbsp;像素</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>分论坛浮动广告图片高度</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight" value="$adimageheight" maxlength=3>&nbsp;像素</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"useimageadtopic\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n";
               $tempoutput =~ s/value=\"$useimageadtopic\"/value=\"$useimageadtopic\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=宋体 color=#333333><b>查看此分论坛的贴子时是否<BR>使用此浮动广告</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput如果上面设置了<BR>分论坛不使用浮动广告的话，此选项无效<BR><BR></td>
               </tr>
		~;

               $tempoutput = "<select name=\"forumimagead1\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n";
               $tempoutput =~ s/value=\"$forumimagead1\"/value=\"$forumimagead1\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=宋体 color=#333333><b>是否使用分论坛右下固定广告</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>分论坛右下固定广告图片 URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage1" value="$adimage1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>分论坛右下固定广告连接目标网址</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink1" value="$adimagelink1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>分论坛右下固定广告图片宽度</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth1" value="$adimagewidth1" maxlength=3>&nbsp;像素</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>分论坛右下固定广告图片高度</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight1" value="$adimageheight1" maxlength=3>&nbsp;像素</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"useimageadtopic1\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n";
               $tempoutput =~ s/value=\"$useimageadtopic1\"/value=\"$useimageadtopic1\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=宋体 color=#333333><b>查看此分论坛的贴子时是否<BR>使用此右下固定广告</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput如果上面设置了<BR>分论坛不使用右下固定广告的话，此选项无效</td>
               </tr>
<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><center><b>初始化特效设置</b> (Leoboard.cgi & Forums.cgi)</center><br>
</font></td>
</tr>
~;


$tempoutput = "<select name=\"pagechange\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
$tempoutput =~ s/value=\"$pagechange\"/value=\"$pagechange\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>调入页面时是否使用特效?</b><br>IE 4.0 以上版本浏览器有效</font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

$tempoutput = "<select name=\"cinoption\">\n
<option value=\"0\">盒状收缩\n
<option value=\"1\">盒状放射\n
<option value=\"2\">圆形收缩\n
<option value=\"3\">圆形放射\n
<option value=\"4\">向上擦除\n
<option value=\"5\">向下擦除\n
<option value=\"6\">向右擦除\n
<option value=\"7\">向左擦除\n
<option value=\"8\">垂直遮蔽\n
<option value=\"9\">水平遮蔽\n
<option value=\"10\">横向棋盘式\n
<option value=\"11\">纵向棋盘式\n
<option value=\"12\">随机分解\n
<option value=\"13\">左右向中央缩进\n
<option value=\"14\">中央向左右扩展\n
<option value=\"15\">上下向中央缩进\n
<option value=\"16\">中央向上下扩展\n
<option value=\"17\">从左下抽出\n
<option value=\"18\">从左上抽出\n
<option value=\"29\">从右下抽出\n
<option value=\"20\">从右上抽出\n
<option value=\"21\">随机水平线条\n
<option value=\"22\">随机垂直线条\n
<option value=\"23\">随机(上面任何一种)\n
</select>\n";
$tempoutput =~ s/value=\"$cinoption\"/value=\"$cinoption\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>特效类型?</b></font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>特效维持时间?</b><br>例： 1.0 = 1 秒, 0.5 = 1/2 秒.</font></td>
<td bgcolor=#FFFFFF>
<input type=text size=10 name="timetoshow" value="$timetoshow"> 默认：1</td>
</tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>其他设置</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>版权信息</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>
                 ~;

                $tempoutput = "<select name=\"floodcontrol\"><option value=\"off\">否<option value=\"on\">是</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>是否灌水预防机制？</b><br>强烈推荐使用</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>用户发贴的相隔时间</b><br>灌水预防机制不会影响到坛主或版主</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="floodcontrollimit" value="$floodcontrollimit" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>多少小时内的新贴后面加 new 标志？<BR>(如果不想要，可以设置为 0)</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newmarktime" value="$newmarktime" size=3 maxlength=3>　一般 12 - 24 小时</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"look\">\n<option value=\"on\">开放\n<option value=\"off\">不开放\n</select>\n";
                $tempoutput =~ s/value=\"$look\"/value=\"$look\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否开放本版配色功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"announcemove\">\n<option value=\"on\">移动\n<option value=\"off\">不移动\n</select>\n";
               	$tempoutput =~ s/value=\"$announcemove\"/value=\"$announcemove\" selected/;
               	print qq~

               	<tr>
               	<td bgcolor=#FFFFFF colspan=2>
               	<font color=#333333>论坛公告是否采用移动风格？</font></td>
               	<td bgcolor=#FFFFFF>
               	$tempoutput</td>
               	</tr>
               	~;

                $tempoutput = "<select name=\"announcements\"><option value=\"no\">不使用<option value=\"yes\">使用</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>是否使用公告论坛</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;

                $tempoutput = "<select name=\"sticky\"><option value=\"off\">正常顺序，新的放在最后<option value=\"on\">紧跟主题，新的放在最上面</select>\n";
                $tempoutput =~ s/value=\"$sticky\"/value=\"$sticky\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>查看贴子回复的时候，最新的回复是紧跟主题呢？还是放在最后！</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"refreshurl\"><option value=\"0\">自动返回当前论坛<option value=\"1\">自动返回当前贴子</select>\n";
                $tempoutput =~ s/value=\"$refreshurl\"/value=\"$refreshurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>发表、回复贴子后自动转移到？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"postopen\"><option value=\"yes\">可以发表或回复主题<option value=\"no\">不允许发表或回复主题</select>\n";
                $tempoutput =~ s/value=\"$postopen\"/value=\"$postopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>打开论坛发表或回复主题功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pollopen\"><option value=\"yes\">打开投票<option value=\"no\">关闭投票</select>\n";
                $tempoutput =~ s/value=\"$pollopen\"/value=\"$pollopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>打开论坛投票功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"xzbopen\"><option value=\"yes\">打开小字报<option value=\"no\">关闭小字报</select>\n";
                $tempoutput =~ s/value=\"$xzbopen\"/value=\"$xzbopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>打开论坛小字报功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"useemote\"><option value=\"yes\">使用<option value=\"no\">不使用</select>\n";
                $tempoutput =~ s/value=\"$useemote\"/value=\"$useemote\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否使用 EMOTE 标签？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"regaccess\"><option value=\"off\">不，允许任何人访问<option value=\"on\">是，必须登陆后才能访问</select>\n";
                $tempoutput =~ s/value=\"$regaccess\"/value=\"$regaccess\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛只有注册用户可以访问？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowuserdel\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrowuserdel\"/value=\"$arrowuserdel\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许注册用户自己删除自己的贴子？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"newmsgpop\"><option value=\"off\">不弹出<option value=\"on\">弹出</select>\n";
                $tempoutput =~ s/value=\"$newmsgpop\"/value=\"$newmsgpop\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>有新的短消息是否弹出窗口提示？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pvtip\">\n<option value=\"on\">显示 IP 和鉴定\n<option value=\"off\">保密 IP 和鉴定\n</select>\n";
                $tempoutput =~ s/value=\"$pvtip\"/value=\"$pvtip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>是否保密 IP 和鉴定？</b><BR>即使选择的是显示 IP，但普通用户还是<BR>只能看见 IP 的前两位</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能对坛主无效</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"smocanseeip\">\n<option value=\"yes\">有效\n<option value=\"no\">无效\n</select>\n";
                $tempoutput =~ s/value=\"$smocanseeip\"/value=\"$smocanseeip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>保密 IP 和鉴定对总斑竹是否有效？</b><BR>如选择无效，则总版主可查看所有的 IP<BR>而不受上面 IP 保密的限制</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"arrowupload\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$arrowupload\"/value=\"$arrowupload\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子是否允许上传？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能对版主和坛主无效</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"allowattachment\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
                $tempoutput =~ s/value=\"$allowattachment\"/value=\"$allowattachment\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复是否允许上传？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能对版主和坛主无效</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛上传文件允许的最大值(单位：KB)<br>如果设置了不允许上传，则此项无效！</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxupload" value="$maxupload" size=5 maxlength=5>　不要加 KB 字样，建议不要超过 500 ！</td>
                </tr>

                ~;

                $tempoutput = "<select name=\"quotemode\">\n<option value=\"0\">表格\n<option value=\"1\">线条\n</select>\n";
                $tempoutput =~ s/value=\"$quotemode\"/value=\"$quotemode\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>引用标签的样式？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"defaulttopicshow\"><option value=>查看所有的主题<option value=\"1\">查看一天内的主题<option value=\"2\">查看两天内的主题<option value=\"7\">查看一星期内的主题<option value=\"15\">查看半个月内的主题<option value=\"30\">查看一个月内的主题<option value=\"60\">查看两个月内的主题<option value=\"180\">查看半年内的主题</select>\n";
                $tempoutput =~ s/value=\"$defaulttopicshow\"/value=\"$defaulttopicshow\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认显示主题数</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"defaulforumcshow\"><option value=\"orderlastpostd\">按最后回复时间降序<option value=\"orderlastposta\">按最后回复时间升序<option value=\"orderthreadd\">按主题发布时间降序<option value=\"orderthreada\">按主题发布时间升序<option value=\"orderstartbyd\">按主题发布人降序<option value=\"orderstartbya\">按主题发布人升序<option value=\"orderclickd\">按主题点击数降序<option value=\"orderclicka\">按主题点击数升序<option value=\"orderreplyd\">按主题回复数降序<option value=\"orderreplya\">按主题回复数升序<option value=\"ordertitled\">按主题标题降序<option value=\"ordertitlea\">按主题标题升序</select>\n";
                $tempoutput =~ s/value=\"$defaulforumcshow\"/value=\"$defaulforumcshow\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认贴子排序方式</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"onlineview\">\n<option value=\"1\">显示\n<option value=\"0\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$onlineview\"/value=\"$onlineview\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认是否显示在线用户详细列表？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"advpost\">\n<option value=\"1\">高级模式\n<option value=\"0\">简洁模式\n</select>\n";
                $tempoutput =~ s/value=\"$advpost\"/value=\"$advpost\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认发贴模式？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"sortalltopic\">\n<option value=\"yes\">开放\n<option value=\"no\">不开放\n</select>\n";
                $tempoutput =~ s/value=\"$sortalltopic\"/value=\"$sortalltopic" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否开放论坛贴子排序察看功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"dispquickreply\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
                $tempoutput =~ s/value=\"$dispquickreply\"/value=\"$dispquickreply" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否启用快速回复？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispview\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
                $tempoutput =~ s/value=\"$dispview\"/value=\"$dispview\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>是否显示论坛图例</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"refreshforum\">\n<option value=\"off\">不要自动刷新\n<option value=\"on\">要自动刷新\n</select>\n";
                $tempoutput =~ s/value=\"$refreshforum\"/value=\"$refreshforum" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>本分论坛是否自动刷新(请在下面设置间隔时间)？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>自动刷新论坛的时间间隔(秒)<BR>配合上面参数一起使用</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="autofreshtime" value="$autofreshtime" size= 5 maxlength=4>　一般设置 5 分钟，就是 300 秒。</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>分论坛背景音乐名称</b>(如果没有请留空)<br>请输入背景音乐名称，背景音乐<BR>应上传于 non-cgi/midi 目录下。<br><b>不要包含 URL 地址或绝对路径！</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="midiaddr" value="$midiaddr">~;
                $midiabsaddr = "$imagesdir" . "midi/$midiaddr";
                print qq~　<EMBED src="$imagesurl/midi/$midiaddr" autostart="false" width=70 height=25 loop="true" align=absmiddle>~ if ((-e "$midiabsaddr")&&($midiaddr ne ""));
                print qq~
                </td>
                </tr>
                <td bgcolor=#FFFFFF align=center colspan=3>
                <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
                ~;

}

sub dostyle {
  $filerequire = "$lbdir" . "data/style${inforum}.cgi";
  foreach (@params) {
	$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam =~ s/'//g;
        $theparam = &unHTML("$theparam");
	${$_} = $theparam;
        if (($_ ne 'action')&&($_ ne 'forum')&&($theparam ne "")) {
            $printme .= "\$" . "$_ = \"$theparam\"\;\n";
            }
	}
	$endprint = "1\;\n";
	&winlock($filerequire) if ($OS_USED eq "Nt");
        open(FILE,">$filerequire");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filerequire) if ($OS_USED eq "Nt");

if (-e $filerequire && -w $filerequire) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 分论坛风格设定</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE colspan=2>
                <font color=#333333><center><b>以下信息已经成功保存</b><br><br>
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
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 分论坛风格设定</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>所有信息没有保存</b><br>文件或者目录不可写<br>请检测你的 data 目录和 styles*.cgi 文件的属性！
                    </td></tr></table></td></tr></table>
                    ~;
                    }


}

######## Subroutes ( Editing of a Forum )
sub editform {


        # Grab the line to edit.

         $filetoopen = "$lbdir" . "data/allforums.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         @forums = <FILE>;
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");


         foreach $forum (@forums) {
            chomp $forum;
	    next if ($forum eq "");
            ($forumid,$notneeded,$notneeded,$notneeded) = split(/\t/,$forum);
    	    next if ($forumid !~ /^[0-9]+$/);
                if ($forumid eq "$inforum") {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                }
         }

# Present the form to be filled in


        print qq~
        <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 编辑论坛</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>编辑 '$category' 分类中的 '$forumname' 论坛</b>
        </td></tr>

        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="doedit">
        <input type=hidden name="forum" value="$inforum">
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛名称</b><br>请输入论坛名称</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumname" value="$forumname"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛描述</b><br>请输入论坛描述</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛版主</b><br>请输入论坛版主，如果您希望有多个版主，请使用 "," (英文逗号，不是中文逗号)隔开。<BR><B>例如</B>：山鹰糊, 花无缺</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>
        ~;

        $tempoutput = qq~<select name="htmlstate"><option value="on">使用<option value="off">不使用</select>~;
        $tempoutput =~ s/value=\"$htmlstate\"/value=\"$htmlstate\" selected/g;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否使用 HTML 标签？</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="idmbcodestate"><option value="on">使用<option value="off">不使用</select>~;
        $tempoutput =~ s/value=\"$idmbcodestate\"/value=\"$idmbcodestate\" selected/g;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否使用 LB5000 标签？</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="privateforum"><option value="yes">是<option value="no">否</select>~;
        $tempoutput =~ s/value=\"$privateforum\"/value=\"$privateforum\" selected/g;
        if (!$privateforum) {
            $tempoutput = qq~<select name="privateforum"><option value="yes">是<option value="no" selected>否</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否作为私有论坛？</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput  对坛主和总斑竹无效
        </td>
        </tr>
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>私有论坛密码</b>(只对私有论坛有效)</font></td>
        <td bgcolor=#FFFFFF>
       <input type=text size=12 name="forumpass" value="$forumpass" maxlength=20> 对坛主和总斑竹无效</td>
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="hiddenforum"><option value="yes">是<option value="no">否</select>~;
        $tempoutput =~ s/value=\"$hiddenforum\"/value=\"$hiddenforum\" selected/g;
        if (!$hiddenforum) {
            $tempoutput = qq~<select name="hiddenforum"><option value="yes">是<option value="no" selected>否</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否隐藏论坛？</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="indexforum"><option value="yes">是<option value="no">否</select>~;
        $tempoutput =~ s/value=\"$indexforum\"/value=\"$indexforum\" selected/g;
        if (!$indexforum) {
            $tempoutput = qq~<select name="indexforum"><option value="yes" selected>是<option value="no" >否</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否显示导航栏？</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>

        ~;

        $tempoutput = qq~<select name="startnewthreads"><option value="yes" selected>正规论坛<option value="all">开放论坛<option value="follow">评论论坛<option value="no">精华区</select>~;
        $tempoutput =~ s/value=\"$startnewthreads\"/value=\"$startnewthreads\" selected/g;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛性质</b><br>1. 正规论坛-只允许注册会员发言<br>2. 开放论坛-允许所有人发言<br>3. 评论论坛-坛主和版主允许发言，其他注册用户只能回复<br>4. 精华区-只允许版主和坛主发言和操作<br>5. 认证论坛-除坛主和版主外，其他注册用户发言需要认证</font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="ratings"><option value="On">允许<option value="">不允许</select>~;
        $tempoutput =~ s/value=\"$ratings\"/value=\"$ratings\" selected/g;
        print qq~

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>允许对贴子投票评分？</b></font></td>
        <td bgcolor=#FFFFFF>
	  $tempoutput
	  </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛图片</b><br>请输入图片名称，此图片被用来放置在页面左边菜单下。<BR><b>不要包含 URL 地址或绝对路径！</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumgraphic" value="$forumgraphic"></td>
        </tr>

	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font face=宋体 color=#333333><b>队伍图片</b>(如果没有，请保持原样)<br>请输入图片名称，此图片被用来放置在主页面下。<BR><b>不要包含 URL 地址或绝对路径！</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamlogo" value="$teamlogo"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font face=宋体 color=#333333><b>队伍网址</b>(如果没有，请保持原样)</td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamurl" value="$teamurl"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
        ~;

} # end route

##################################################################################
######## Subroutes ( Processing the edit of a forum)


sub doedit {
	&errorout("保密论坛，密码不能空！！") if (($new_privateforum eq "yes")&&($new_forumpass eq ""));
	&errorout("对不起，论坛名字过长，请控制在 20 个汉字内！") if (length($new_forumname) >40);
	&errorout("论坛名字不能空！！") if ($new_forumname eq "");
	&errorout("论坛描述不能空！！") if ($new_forumdescription eq "");
	$new_privateforum = "yes" if ($new_forumpass ne "");

         $filetoopen = "$lbdir" . "data/allforums.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
	 open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         @forums = <FILE>;
         close(FILE);

         foreach $forum (@forums) {
         chomp $forum;
 	 next if ($forum eq "");
            ($forumid, $notneeded) = split(/\t/,$forum);
    	    next if ($forumid !~ /^[0-9]+$/);
                if ($forumid eq $inforum) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc, $forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    }
                }

                # Time to process the forms

                $editedline = "$inforum\t$category\t$categoryplace\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_miscadd1\t$new_miscadd2\t$new_miscadd3\t$new_miscadd4\t$new_miscad5\t";
                chomp $editedline;

                $dirtomake = "$lbdir" . "forum$inforum";
                $filetomake1 = "$dirtomake/foruminfo.cgi";
                open(FILE,">$filetomake1");
                print FILE $editedline;
                close(FILE);

                # Lets re-open the file

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE,"$filetoopen");
                flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                # Lets remake the file...

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                foreach $forum (@forums) {
                chomp $forum;
                ($tempforumid,$notneeded) = split(/\t/,$forum);
                    if ($tempforumid eq "$inforum") {
                        print FILE "$editedline\n";
                        }
                        else {
                            print FILE "$forum\n";
                            }
                    }
                close (FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");


                 print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 编辑论坛结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>所有信息已经保存</b><p>
                如果您设定了某人为版主，你或许会想从管理中心编辑他的资料，使他成为版主。<BR>
                其实这个是没必要的。这个仅仅影响发贴后名字边上的 'team' 图标，非版主不显示 'team' 图标！</font>
                </td></tr></table></td></tr></table>
                ~;

            } # end routine

##################################################################################
######## Subroutes ( Add category/forum Form )


sub catform {

# Present the form to be filled in


        print qq~
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="doaddcategory">
        <input type=hidden name="category" value="$incategory">
        <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 增加分类(同时增加一个论坛)</b>
        </td></tr>
        <tr>

        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>增加分类(同时增加一个论坛)</b>
        </td></tr>


        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>分类名称</b><br>请输入新分类名称</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="categoryname" value="$categoryname"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛名称</b><br>请输入论坛名称</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumname" value="$forumname"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛描述</b><br>请输入论坛描述</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛版主</b><br>请输入论坛版主，如果您希望有多个版主，请使用 "," (英文逗号，不是中文逗号)隔开。<BR><B>例如</B>：山鹰糊, 花无缺</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否使用 HTML 标签？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="htmlstate">
        <option value="on">使用<option value="off" selected>不使用</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否使用 LB5000 标签？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="idmbcodestate">
        <option value="on" selected>使用<option value="off">不使用</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否作为私有论坛？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="privateforum">
        <option value="yes">是<option value="no" selected>否</select> 对坛主和总斑竹无效
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>私有论坛密码</b>(必须配合上面参数使用)</font></td>
        <td bgcolor=#FFFFFF>
       <input type=text size=12 name="forumpass" value="$forumpass" maxlength=20> 对坛主和总斑竹无效</td>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否隐藏论坛？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="hiddenforum">
        <option value="yes">是<option value="no" selected>否</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>是否显示导航栏？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="indexforum">
        <option value="yes" selected>是<option value="no" >否</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛性质</b><br>1. 正规论坛-只允许注册会员发言<br>2. 开放论坛-允许所有人发言<br>3. 评论论坛-坛主和版主允许发言，其他注册用户只能回复<br>4. 精华区-只允许版主和坛主发言和操作<br>5. 认证论坛-除坛主和版主外，其他注册用户发言需要认证</font></td>
        <td bgcolor=#FFFFFF>
        <select name="startnewthreads">
        <option value="yes" selected>正规论坛<option value="all">开放论坛<option value="follow">评论论坛<option value="no">精华区</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>允许对贴子投票评分？</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="ratings">
        <option value="On">允许<option value="" selected>不允许</select>
	  </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>论坛图片</b><br>请输入图片名称，此图片被用来放置在页面左边菜单下。<BR><b>不要包含 URL 地址或绝对路径！</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumgraphic" value="logo.gif"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font face=宋体 color=#333333><b>队伍图片</b>(如果没有，请保持原样)<br>请输入图片名称，此图片被用来放置在主页面下。<BR><b>不要包含 URL 地址或绝对路径！</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamlogo" value=""></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font face=宋体 color=#333333><b>队伍网址</b>(如果没有，请保持原样)</td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamurl" value="http://"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
        ~;

} # end route


##################################################################################
######## Subroutes ( Create New cat/forum )


sub doaddcategory {
		&errorout("保密论坛，密码不能空！！") if (($new_privateforum eq "yes")&&($new_forumpass eq ""));
		&errorout("对不起，论坛名字过长，请控制在 20 个汉字内！") if (length($new_forumname) >40);
		&errorout("论坛名字不能空！！") if ($new_forumname eq "");
		&errorout("论坛描述不能空！！") if ($new_forumdescription eq "");
		&errorout("论坛类别不能空！！") if ($new_categoryname eq "");
		$new_privateforum = "yes" if ($new_forumpass ne "");

                $filetoopen = "$lbdir" . "data/allforums.cgi";
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                # Create a new number for the new forum folder, and files.

                foreach (@forums) {
                    ($forumid, $binit) = split(/\t/,$_);
                    if ($forumid > $high) { $high = $forumid; }
                    }

                $high++;

                $newforumid = $high;


                # Lets create the directory.

                $dirtomake = "$lbdir" . "forum$newforumid";

                mkdir ("$dirtomake", 0777);

                # Lets add a file to stop snoops, and to use to see if the forum was created

                $filetomake = "$dirtomake/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);

                $filetomake = "$lbdir" . "boarddata/list$newforumid.cgi";
                open(FILE,">$filetomake");
                close(FILE);

                $filetomake = "$dirtomake/.htaccess";
                open(FILE, ">$filetomake");
                print FILE "AuthUserFile /dev/null\n";
                print FILE "AuthGroupFile /dev/null\n";
                print FILE "AuthName DenyViaWeb\n";
                print FILE "AuthType Basic\n";
                print FILE "\n\n\n\n";
                print FILE "<Limit GET>\n";
                print FILE "order allow,deny\n";
                print FILE "deny from all\n";
                print FILE "</Limit>\n";
                close (FILE);

                $filetomake1 = "$dirtomake/foruminfo.cgi";
                open(FILE,">$filetomake1");
                print FILE "$newforumid\t$new_categoryname\t$incategory\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t\t\t0\t0\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_miscadd1\t$new_miscadd2\t$new_miscadd3\t$new_miscadd4\t$new_miscad5\t";
                close(FILE);

                $filetoopen = "$lbdir" . "data/allforums.cgi";
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
                flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                open(FILE, ">$filetoopen");
                flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $line (@forums) {
                    chomp $line;
                    print FILE "$line\n";
                    }
                print FILE "$newforumid\t$new_categoryname\t$incategory\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t\t\t0\t0\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_miscadd1\t$new_miscadd2\t$new_miscadd3\t$new_miscadd4\t$new_miscad5\t";
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 增加分类(同时增加一个论坛)结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>
                ~;

                print "<b>详细信息：</b><p>\n";
                print "<ul>\n";
                if (-e $dirtomake) {
                print "<li><b>新的分类和论坛已经建立</b><p>\n";
                    }
                    else {
                        print "<li><b>新的分类和论坛没有建立</b><p>请查看是否改变了目录属性？请改属性回 777 ！<p>\n";
                        }


                $filetoopen = "$dirtomake/index.html";
                if (-e $filetoopen) {
                    print "<li><b>新论坛 (index.html) 文件建立</b><p>\n";
                    }
                    else {
                        print "<li><b>新论坛 (index.html) 文件没有建立</b><p>请查看是否改变了目录属性？请改属性回 777 ！<p>\n";
                        }
                print "$filetoopen<p>\n";
                print "</ul></td></tr></table></td></tr></table>\n";

} # end routine


##################################################################################
######## Subroutes ( Edit Category Name )


sub editcatname {


        if ($checkaction ne "yes") {

            # Grab the line to edit.

            $filetoopen = "$lbdir" . "data/allforums.cgi";
    	    &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE,"$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @forums = <FILE>;
            close(FILE);
            &winunlock($filetoopen) if ($OS_USED eq "Nt");

            foreach $forum (@forums) {
            chomp $forum;
 	    next if ($forum eq "");
                ($tempno, $notneeded, $categoryplace) = split(/\t/,$forum);
    	    	next if ($tempno !~ /^[0-9]+$/);
                    if ($incategory eq "$categoryplace") {
                        ($trash, $categoryname, $notneeded) = split(/\t/,$forum);
                        }
                    }

            # Present the form to be filled in


            print qq~
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="editcatname">
            <input type=hidden name="category" value="$incategory">
            <input type=hidden name="checkaction" value="yes">
            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 编辑分类名称</b>
            </td></tr>
            <tr>

            <tr>
            <td bgcolor=#EEEEEE align=center colspan=2>
            <font color=#990000><b>编辑 '$categoryname' 分类的名称</b>
            </td></tr>


            <tr>
            <td bgcolor=#FFFFFF width=40%>
            <font color=#333333><b>分类名称</b><br>请输入分类名称</font></td>
            <td bgcolor=#FFFFFF>
            <input type=text size=40 name="categoryname" value="$categoryname"></td>
            </tr>


            <tr>
            <td bgcolor=#FFFFFF align=center colspan=2>
            <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
            ~;
            } # end if

            else {

                # Grab the lines to change.

                $filetoopen = "$lbdir" . "data/allforums.cgi";
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE,"$filetoopen");
	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                # Lets remake the file with the new info

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                foreach $forum (@forums) {
                    chomp $forum;
		    next if ($forum eq "");
                    ($tempno, $notneeded, $categorynumber) = split(/\t/,$forum);
    	    	    next if ($tempno !~ /^[0-9]+$/);
                    if ($incategory eq "$categorynumber") {
                        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                        $linetochange = "$forumid\t$new_categoryname\t$incategory\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t";
                        chomp $linetochange;
                        print FILE "$linetochange\n";
              	  	$dirtomake = "$lbdir" . "forum$forumid";
	                $filetomake1 = "$dirtomake/foruminfo.cgi";
          	        open(FILE1,">$filetomake1");
                        print FILE1 $linetochange;
                	close(FILE1);
                        $forumname = ""; $forumdescription = ""; $forummoderator = ""; $lastposter = ""; $lastposttime = ""; $threads = ""; $posts = ""; $forumgraphic = ""; $ratings = "";
                    }
                    else {
                        print FILE "$forum\n";
                    }
                }
                close (FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 编辑分类名称结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>所有信息已经成功保存</b>
                </td></tr></table></td></tr></table>
                ~;

                } # end else

            } # end routine


##################################################################################
######## Subroutes ( Edit Category Name )


sub reordercats {


        if ($checkaction ne "yes") {

            print qq~
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="reordercategories">
            <input type=hidden name="checkaction" value="yes">
            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 论坛分类重新排序</b>
            </td></tr>
            <tr><td bgcolor=#FFFFFF" colspan=3><font color=#333333>
            <b>注意事项：</b><br><br>
            在此您可以将论坛分类重新排序。分类将按照数字重新显示。<BR><BR><b>1 表示此为第一分类，将显示在最前面</b>。<br><br>
            <b>提交之前请仔细检查所有设置，并保证没有重复数字，有重复将会导致有的分类无法显示！</b><br><br>
            </td></tr>
            ~;

            $filetoopen = "$lbdir" . "data/allforums.cgi";
	    &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE, "$filetoopen");
	    flock(FILE, 1) if ($OS_USED eq "Unix");
            @forums = <FILE>;
            close(FILE);
	    &winunlock($filetoopen) if ($OS_USED eq "Nt");

            foreach $forum (@forums) { #start foreach @forums
                chomp $forum;
                ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
                push (@rearrangedforums, $rearrange);

                } # end foreach (@forums)

            @finalsortedforums = sort({$a<=>$b}@rearrangedforums);

            foreach $sortedforums (@finalsortedforums) { #start foreach @finalsortedforums

                ($categoryplace, $category, $forumgraphic, $ratings, $misc, $forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$sortedforums);

                if ($categoryplace ne $lastcategoryplace) { #start if $categoryplace
                    print qq~
                    <tr>
                    <td bgcolor=#FFFFFF width=40%><font color=#333333>
                    <b>-=> $category</b></font></td>
                    <td bgcolor=#FFFFFF><font color=#333333>现在位置 [ <B>$categoryplace</B> ]，请输入新的数字以便排序：<input type=text size=4 maxlength=2 name="$categoryplace" value="$categoryplace">
                    </td></tr>
                    ~;
                    } # end if

                    $lastcategoryplace = $categoryplace;

                 } # end foreach



                    print qq~
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <BR><input type=submit value="提 交"></td></form></tr></table></td></tr></table>
                    ~;

            } # end if


            else {

                # Grab the lines to change.

                $filetoopen = "$lbdir" . "data/allforums.cgi";
		&winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE,"$filetoopen");
	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                # Lets remake the file with the new info

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                foreach $forum (@forums) {
                    chomp $forum;
	 	    next if ($forum eq "");
                    ($tempno, $notneeded, $categorynumber) = split(/\t/,$forum);
    	    	    next if ($tempno !~ /^[0-9]+$/);
                    $newid = $PARAM{$categorynumber};
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                    print FILE "$forumid\t$category\t$newid\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t\n";
                }

                close (FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 编辑分类名称结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>所有信息已经成功保存</b>
                </td></tr></table></td></tr></table>
                ~;

                } # end else


} # end routine

sub reorder {


        if ($checkaction ne "yes") {

            print qq~
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="reorder">
            <input type=hidden name="checkaction" value="yes">
            <input type=hidden name="category" value="$inforum">

            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 论坛重新排序</b>
            </td></tr>
            <tr><td bgcolor=#FFFFFF" colspan=3><font color=#333333>
            <b>注意事项：</b><br><br>
            在此您可以将分论坛重新排序。<br>分论坛将自动根据顺序重新改变顺序和分区名称
            </td></tr>~;
            $filetoopen = "$lbdir" . "data/allforums.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         @forums = <FILE>;
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");


         foreach $forum (@forums) {
            chomp $forum;
	    next if ($forum eq "");
            ($forumid,$notneeded,$notneeded,$notneeded) = split(/\t/,$forum);
    	    next if ($forumid !~ /^[0-9]+$/);
                if ($forumid eq $inforum) {
                    ($forumid, $category, $categoryplace, $myforumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
                }
         }
            print qq~
            <tr><td>把论坛 <font color=red>$myforumname</font> 移到论坛
            <select name="forum">
            ~;



foreach my $forum (@forums) { #start foreach @forums
    chomp $forum;
    next if ($forum eq "");
    (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription) = split(/\t/,$forum);
    next if ($forumid !~ /^[0-9]+$/);
    next if ($categoryplace !~ /^[0-9]+$/);
    next if ($forumid eq $inforum);
    $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
    push (@rearrangedforums, $rearrange);
}

@finalsortedforums = sort {$a<=>$b} @rearrangedforums;

foreach my $sortedforums (@finalsortedforums) {
    (my $categoryplace, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $ratings, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $miscadd1,my $miscadd2,my $miscadd3,my $miscadd4,my $miscad5) = split(/\t/,$sortedforums);

    if ($categoryplace ne $lastcategoryplace) {
    $has=0;
          foreach (@hascat){
          $has=1 if ($_ eq $categoryplace);
          }
           if ($has ==0){
        $jumphtml .= "<option value=\"top$forumid\">>>&nbsp;$category <<\n";
     foreach my $myforums (@rearrangedforums) {
     (my $mycategoryplace, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $ratings, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $miscadd1,my $miscadd2,my $miscadd3,my $miscadd4,my $miscad5) = split(/\t/,$myforums);
      if (($forumname ne $myforumname)&&($categoryplace eq $mycategoryplace)){
        $jumphtml .= "<option value=\"$forumid\"> $forumname\n";
                                                                             }
                                                }
                             }

    }

    $lastcategoryplace = $categoryplace;
    push (@hascat, $categoryplace);
}
$jumphtml .= qq~</select>\n~;




                    print qq~
                    $jumphtml下，并且自动改变分区属性。
                   </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <BR><input type=submit value="提 交"></td></form></tr></table></td></tr></table>
                    ~;

            } # end if


            else {

                # Grab the lines to change.

                $filetoopen = "$lbdir" . "data/allforums.cgi";
		&winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE,"$filetoopen");
	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

            foreach $forum (@forums) {
            	chomp $forum;
	    	next if ($forum eq "");
            	($forumid,$notneeded,$categoryplace,$notneeded) = split(/\t/,$forum);
    	    	next if ($forumid !~ /^[0-9]+$/);
    	    	next if ($categoryplace !~ /^[0-9]+$/);
                if ($forumid eq "$incategory") {
                    ($oldforumid, $oldcategory, $oldcategoryplace, $oldmyforumname, $oldforumdescription, $oldforummoderator ,$oldhtmlstate ,$oldidmbcodestate ,$oldprivateforum, $oldstartnewthreads ,$oldlastposter ,$oldlastposttime, $oldthreads, $oldposts, $oldforumgraphic, $oldratings, $oldmisc,$oldforumpass,$oldhiddenforum,$oldindexforum,$oldteamlogo,$oldteamurl, $oldmiscadd1, $oldmiscadd2, $oldmiscadd3, $oldmiscadd4, $oldmiscad5) = split(/\t/,$forum);
                }
            }

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                foreach $forum (@forums) {
                    chomp $forum;
	 	    next if ($forum eq "");
                    ($forumid, $category, $categoryplace, $myforumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
    	    	    next if ($forumid !~ /^[0-9]+$/);
                    if ($forumid ne $incategory){
                	if ($forumid eq $inforum){
                  	  print FILE "$forum\n";
                  	  print FILE "$oldforumid\t$category\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldmiscadd1\t$oldmiscadd2\t$oldmiscadd3\t$oldmiscadd4\t$oldmiscad5\t\n";

                	  $dirtomake = "$lbdir" . "forum$inforum";
	                  $filetomake1 = "$dirtomake/foruminfo.cgi";
          	          open(FILE1,">$filetomake1");
                  	  print FILE1 "$oldforumid\t$category\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldmiscadd1\t$oldmiscadd2\t$oldmiscadd3\t$oldmiscadd4\t$oldmiscad5\t";
                	  close(FILE1);
         		}
              		elsif ("top$forumid" eq $inforum) {
                	  print FILE "$oldforumid\t$category\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldmiscadd1\t$oldmiscadd2\t$oldmiscadd3\t$oldmiscadd4\t$oldmiscad5\t\n";
                	  print FILE "$forum\n";
                	  $dirtomake = "$lbdir" . "forum$inforum";
	                  $filetomake1 = "$dirtomake/foruminfo.cgi";
          	          open(FILE1,">$filetomake1");
                	  print FILE1 "$oldforumid\t$category\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldmiscadd1\t$oldmiscadd2\t$oldmiscadd3\t$oldmiscadd4\t$oldmiscad5\t";
                	  close(FILE1);
              		}
             	    	else {
        			print FILE "$forum\n";
               	    	}
        	    }
        	}

                close (FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 分论坛排序名称结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>所有信息已经成功保存</b>
                </td></tr></table></td></tr></table>
                ~;

                } # end else


} # end routine

print qq~</td></tr></table></body></html>~;
exit;

sub errorout {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 发生错误</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>
                <font color=#333333><b>$_[0]</b>
                </td></tr></table></td></tr></table>
                ~;
exit;
}