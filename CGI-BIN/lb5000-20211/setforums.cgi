#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ���������)
#
#  ������  : ɽӥ�� (Shining Hu)
#            ����ȱ (Ifairy Han)
#
#  ��ҳ��ַ: http://www.CGIer.com/      CGI �����֮��
#	     http://www.LeoBoard.com/   �װ���̳֧����ҳ
#	     http://www.leoBBS.com/     ����ֱ̳ͨ��
#            http://mail@17do.com/      ���һ����
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

&ipbanned; #��ɱһЩ ip

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
    <b>��ӭ������̳�������� / ��̳����</b>
    </td></tr>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>���з����Ѿ�����</b><br>
    ��ǰ��̳$size���Ѿ����ݣ�
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
    <b>��ӭ������̳�������� / ��̳����</b>
    </td></tr>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>���з����Ѿ���ԭ</b><br>
    ��ǰ��̳$size���Ѿ���ԭ��
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
    <b>��ӭ������̳�������� / ��̳����</b>
    </td></tr>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>������Ϣ�Ѿ�����</b><br>
    ����������$totle1 ƪ<BR>
    �ظ�������$totle2 ƪ
    </td></tr>
    ~;

}
sub forumlist {
    $highest = 0;
    print qq~
    <tr><td bgcolor=#333333 colspan=3><font color=#FFFFFF>
    <b>��ӭ������̳�������� / ��̳����</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font color=#333333>
    <b>����<a href="$thisprog?action=updatecount">����ͳ��</a>��</b><br>
    ��������̳����������ͳ�����������������޸���ҳ��������ʾ�Ĵ���<br><br>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font color=#333333>
    <b>����<a href="$thisprog?action=bakcat">������̳����</a>/<a href="$thisprog?action=upcat">��ԭ��̳����</a></b><br>
    ��������̳�ķ�����б��ݣ����������޸�������̳��ʧ�������(��̳Ҳ���Զ����б��ݺͻָ�)<br><br>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font color=#333333>
    <b>����ע�����</b><br>
    �����棬��������Ŀǰ���е���̳���ࡣ�����Ա༭��̳��������������һ���µ���̳����������С�
    Ҳ���Ա༭��ɾ��Ŀǰ���ڵ���̳�������Զ�Ŀǰ�ķ������½������С�<br>
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
            �������� <b>$category</b><td bgcolor=#EEEEEE width=15% align=center nowrap><font color=#333333><a href="$thisprog?action=editcatname&category=$categoryplace">�༭��������</a></td><td bgcolor=#EEEEEE width=25%><font color=#333333><a href="$thisprog?action=addforum&category=$categoryplace">������̳���˷�����</a></font></td>
            </td></tr>
            ~;
            foreach my $myforums (@rearrangedforums) {
            (my $mycategoryplace, my $category,my $forumname, my $forumdescription, my $forumid, my $threads, my $posts, my $forumgraphic, my $ratings, my $misc,my $forumpass,my $hiddenforum,my $indexforum,my $teamlogo,my $teamurl,my $miscadd1,my $miscadd2,my $miscadd3,my $miscadd4,my $miscad5) = split(/\t/,$myforums);
            if ($categoryplace eq $mycategoryplace){
            print qq~
            <tr>
            <td bgcolor=#FFFFFF colspan=3 nowrap><font color=#333333>
            ��̳���� <b>$forumname</b><br>�������� <b>$threads</b>��<-->��<font color=#333333>�ظ����� <b>$posts</b><br><br><a href="$thisprog?action=edit&forum=$forumid">�༭</a> | <font color=#333333><a href="$thisprog?action=delete&forum=$forumid">ɾ��</a> | <a href="$thisprog?action=recount&forum=$forumid">���¼�������ͻظ��� / �޸�</a>| <font color=#333333><a href="$thisprog?action=style&forum=$forumid">�Զ�����</a></font>| <font color=#333333><a href="setstyles.cgi?action=delstyle&forum=$forumid">ɾ���Զ�����</a></font>| <font color=#333333><a href="$thisprog?action=reorder&forum=$forumid">����������</a></font></td>
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
        <a href="$thisprog?action=reordercategories">��̳������������</a>
        ����--����
        <a href="$thisprog?action=addcategory&category=$highest">���ӷ���(ͬʱ����һ����̳)</a>
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
         <b>��ӭ������̳�������� / �ؼ�������ͻظ���</b>
         </td></tr>
         <tr>
         <td bgcolor=#FFFFFF colspan=2>
         <font color=#990000>
         <center><b>��̳���³ɹ�</b></center><p>
         �������� $topiccount<p>
         �ظ����� $threadcount
         </td></tr></table></td></tr></table>
         ~;


} # routine ends

##################################################################################
######## Subroutes ( Add forum Form )


sub addforum {

        print qq~
        <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
        <b>��ӭ������̳�������� / ������̳</b>
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
        <font color=#990000><b>�� '$category' ��������������̳</b>
        </td></tr>

        <form action="$thisprog" method="post">
        <input type=hidden name="categorynumber" value="$incategory">
        <input type=hidden name="categoryname" value="$category">
        <input type=hidden name="action" value="processnew">
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>����������̳������<BR>(������� 20 ��������)</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumname" value="$forumname" maxlength=40></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>����������̳������</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳�����������ϣ���ж����������ʹ�� "," (Ӣ�Ķ��ţ��������Ķ���)������<BR><B>����</B>��ɽӥ��, ����ȱ</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� HTML ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="htmlstate">
        <option value="on">ʹ��<option value="off" selected>��ʹ��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� LB5000 ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="idmbcodestate">
        <option value="on" selected>ʹ��<option value="off">��ʹ��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���Ϊ˽����̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="privateforum">
        <option value="yes">��<option value="no" selected>��</select> ��̳�����ܰ�����Ч
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>˽����̳����</b>(ֻ��˽����̳��Ч)</font></td>
        <td bgcolor=#FFFFFF>
       <input type=text size=12 name="forumpass" value="$forumpass" maxlength=20> ��̳�����ܰ�����Ч</td>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�������̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="hiddenforum">
        <option value="yes">��<option value="no" selected>��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���ʾ��������</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="indexforum">
        <option value="yes" selected>��<option value="no" >��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>1. ������̳-ֻ����ע���Ա����<br>2. ������̳-���������˷���<br>3. ������̳-̳���Ͱ��������ԣ�����ע���û�ֻ�ܻظ�<br>4. ������-ֻ���������̳�����ԺͲ���<br>5. ��֤��̳-��̳���Ͱ����⣬����ע���û�������Ҫ��֤</font></td>
        <td bgcolor=#FFFFFF>
        <select name="startnewthreads">
        <option value="yes" selected>������̳<option value="all">������̳<option value="follow">������̳<option value="no">������</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>���������ͶƱ���֣�</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="ratings">
        <option value="On">����<option value="" selected>������</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳ͼƬ</b><br>������ͼƬ���ƣ���ͼƬ��������������̳ҳ����߲˵��¡�<BR><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumgraphic" value="logo.gif"></td>
        </tr>

	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>����ͼƬ</b>(���û�У��뱣��ԭ��)<br>������ͼƬ���ƣ���ͼƬ��������������ҳ���¡�<BR><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamlogo" value=""></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>������ַ</b>(���û�У��뱣��ԭ��)<br>������������̳ͼƬ�ĵ�ַ����</td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamurl" value="http://"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
        ~;

} # end route


##################################################################################
######## Subroutes ( Create Forum )


sub createforum {
		&errorout("������̳�����벻�ܿգ���") if (($new_privateforum eq "yes")&&($new_forumpass eq ""));
		&errorout("�Բ�����̳���ֹ������������ 20 �������ڣ�") if (length($new_forumname) >40);
		&errorout("��̳���ֲ��ܿգ���") if ($new_forumname eq "");
		&errorout("��̳�������ܿգ���") if ($new_forumdescription eq "");
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
                <b>��ӭ������̳�������� / ������̳���</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>
                ~;

                print "<b>��ϸ����</b><p>\n";
                print "<ul>\n";
                if (-e $dirtomake) {
                print "<li><b>����̳Ŀ¼�Ѿ�����</b><p>\n";
                    }
                    else {
                        print "<li><b>����̳Ŀ¼û�н���</b><p>��鿴�Ƿ�ı���Ŀ¼���ԣ�������Ի� 777 ��<p>\n";
                        }


                $filetoopen = "$dirtomake/index.html";
                if (-e $filetoopen) {
                    print "<li><b>����̳ (index.html) �ļ�����</b><p>\n";
                    }
                    else {
                        print "<li><b>����̳ (index.html) �ļ�û�н���</b><p>��鿴�Ƿ�ı���Ŀ¼���ԣ�������Ի� 777 ��\n";
                        }
                print "$filetoopen<p>\n";
                print "</ul></td></tr></table></td></tr></table>\n";

} ######## end routine

##################################################################################
######## Subroutes ( Warning of Delete Forum )

sub warning { #start

        print qq~
        <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
        <b>��ӭ������̳�������� / ɾ����̳</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���棡��</b>
        </td></tr>

        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>�����ȷ��Ҫɾ����̳����ô������������<p>
        >> <a href="$thisprog?action=delete&checkaction=yes&forum=$inforum">ɾ����̳�Լ���̳�µ������ļ�</a> <<
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
        print FILE "$inmembername\t���벻��ʾ\t$ENV{'REMOTE_ADDR'}\t$ENV{'HTTP_X_FORWARDED_FOR'}\tɾ����̳$forumname\t$thistime\t\n";
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
                    <b>��ӭ������̳�������� / ɾ����̳���</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF colspan=2>
                    <font color=#990000>

                    <center><b>��̳�ѱ�ɾ��</b></center><p>

                    ���� $thdcount ���ⱻɾ��<p>

                    ���� $threadcount �ظ���ɾ��

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
        $myskin.=qq~<option value="$thd[$i]">��� [ $thd[$i] ]~;
        }
        $myskin =~ s/value=\"$incategory\"/value=\"$incategory\" selected/;
       &getforum("$inforum");

print qq~
        <tr><td bgcolor=#333333" colspan=3><font color=#FFFFFF>
        <b>��ӭ������̳�������� / �༭��̳���</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=3>
        <font color=#000000><b>�༭ $forumname �ķ���̳���,<Br>����㲻����ģ�������ѡ�����д������</b>
        </td></tr>
        <tr><td bgcolor=#FFFFFF align=center colspan=3><font color=#ffffff>LEOBOARD 5000 VII</font></td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳���ѡ��</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>ϵͳ�Դ��ķ��</b><br>��ѡ�����Ҫ��ʽȷ���ύ����Ч</font></td>
                <td bgcolor=#FFFFFF>
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="style">
                <input type=hidden name="forum" value="$inforum">
                <select name="category"><option value="main">Ĭ�Ϸ��
                $myskin
                </select>
                <input type=submit value="�� ��">
                </form>
                </td></tr>

        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="dostyle">
        <input type=hidden name="forum" value="$inforum">

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳BODY��ǩ</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>����������̳���ı�����ɫ���߱���ͼƬ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>Ĭ�ϣ�bgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>��ҳ��ַ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳ҳ�ײ˵�</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵���������ɫ</font></td>
                <td bgcolor=$menufontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menufontcolor" value="$menufontcolor" size=7 maxlength=7>��Ĭ�ϣ�#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵���������ɫ</font></td>
                <td bgcolor=$menubackground  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackground" value="$menubackground" size=7 maxlength=7>��Ĭ�ϣ�#DDDDDD</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵�������ͼƬ</font></td>
                <td background=$imagesurl/images/$menubackpic  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackpic" value="$menubackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>�˵����߽���ɫ</font></td>
                <td bgcolor=$titleborder  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titleborder" value="$titleborder" size=7 maxlength=7>��Ĭ�ϣ�#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>������ۺ���ɫ</b>
                </font></td>
                </tr>


                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���������</font></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"font\">\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"��Բ\">��Բ\n</select><p>\n";
                $tempoutput =~ s/value=\"$font\"/value=\"$font\" selected/;
                print qq~
                $tempoutput</td>
                </tr>


                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"�������"������ɫ</font></td>
                <td bgcolor=$lastpostfontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lastpostfontcolor" value="$lastpostfontcolor" size=7 maxlength=7>��Ĭ�ϣ�#000000</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"������"������ɫ</font></td>
                <td bgcolor=$fonthighlight  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fonthighlight" value="$fonthighlight" size=7 maxlength=7>��Ĭ�ϣ�#990000</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�鿴ʱ��������������</font></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"posternamefont\">\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"��Բ\">��Բ\n</select><p>\n";
                $tempoutput =~ s/value=\"$posternamefont\"/value=\"$posternamefont\" selected/;
                print qq~
                $tempoutput</td>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>һ���û�����������ɫ</font></td>
                <td bgcolor=$posternamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="posternamecolor" value="$posternamecolor" size=7 maxlength=7>��Ĭ�ϣ�#000066</td>
                </tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font color=#333333>һ���û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$memglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="memglow" value="$memglow" size=7 maxlength=7>��Ĭ�ϣ�#9898BA</td>
		</tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>̳������������ɫ</font></td>
                <td bgcolor=$adminnamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="adminnamecolor" value="$adminnamecolor" size=7 maxlength=7>��Ĭ�ϣ�#990000</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>̳�������ϵĹ�����ɫ</font></td>
		<td bgcolor=$adminglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="adminglow" value="$adminglow" size=7 maxlength=7>��Ĭ�ϣ�#9898BA</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ܰ�������������ɫ</font></td>
                <td bgcolor=$smonamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="smonamecolor" value="$smonamecolor" size=7 maxlength=7>��Ĭ�ϣ�#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>�ܰ��������ϵĹ�����ɫ</font></td>
		<td bgcolor=$smoglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="smoglow" value="$smoglow" size=7 maxlength=7>��Ĭ�ϣ�#9898BA</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��������������ɫ</font></td>
                <td bgcolor=$teamnamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="teamnamecolor" value="$teamnamecolor" size=7 maxlength=7>��Ĭ�ϣ�#0000ff</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>���������ϵĹ�����ɫ</font></td>
		<td bgcolor=$teamglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="teamglow" value="$teamglow" size=7 maxlength=7>��Ĭ�ϣ�#9898BA</td>
		</tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>���˺ͽ����û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$banglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="banglow" value="$banglow" size=7 maxlength=7>��Ĭ�ϣ�none</td>
		</tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>����ҳ����ɫ</center></b><br>
                <font color=#333333>��Щ��ɫ���ý�����ÿ��ҳ�档����ע�ᡢ��½�������Լ�����ҳ�档
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>��������ɫ</font></td>
                <td bgcolor=$fontcolormisc  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fontcolormisc" value="$fontcolormisc" size=7 maxlength=7>��Ĭ�ϣ�#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫһ</font></td>
                <td bgcolor=$miscbackone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbackone" value="$miscbackone" size=7 maxlength=7>��Ĭ�ϣ�#FFFFFF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫ��</font></td>
                <td bgcolor=$miscbacktwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbacktwo" value="$miscbacktwo" size=7 maxlength=7>��Ĭ�ϣ�#EEEEEE</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��������ͼƬ(��������)</font></td>
                <td background=$imagesurl/images/$otherbackpic width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="otherbackpic" value="$otherbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��������ͼƬ(��̳ͼ��)</font></td>
                <td background=$imagesurl/images/$otherbackpic1 width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="otherbackpic1" value="$otherbackpic1"></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>�����ɫ</center></b><br>
                <font color=#333333>��Щ��ɫ�󲿷�����lbboard.cgi��forums.cgi��topic.cgi
                </td></tr>


                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�����������ɫ</font></td>
                <td bgcolor=$catback  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catback" value="$catback" size=7 maxlength=7>��Ĭ�ϣ�#ebebFF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>���������ͼƬ</font></td>
                <td background=$imagesurl/images/$catbackpic  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catbackpic" value="$catbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�����������ɫ</font></td>
                <td bgcolor=$catfontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catfontcolor" value="$catfontcolor" size=7 maxlength=7>��Ĭ�ϣ�#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>���б��߽���ɫ</font></td>
                <td bgcolor=$tablebordercolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablebordercolor" value="$tablebordercolor" size=7 maxlength=7>��Ĭ�ϣ�#000000</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���б����</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablewidth" value="$tablewidth" size=5 maxlength=5>��Ĭ�ϣ�750</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>������ɫ</center></b><br>
                <font color=#333333>������ɫ�������ڷ����һ������ı���
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��̳/����ı�����������ɫ</font></td>
                <td bgcolor=$titlecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titlecolor" value="$titlecolor" size=7 maxlength=7>��Ĭ�ϣ�#acbded</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��̳/����ı�����������ɫ</font></td>
                <td bgcolor=$titlefontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titlefontcolor" value="$titlefontcolor" size=7 maxlength=7>��Ĭ�ϣ�#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��̳������ɫ</center></b><br>
                <font color=#333333>�鿴��̳����ʱ��ɫ (forums.cgi)
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������ɫһ</font></td>
                <td bgcolor=$forumcolorone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumcolorone" value="$forumcolorone" size=7 maxlength=7>��Ĭ�ϣ�#f0F3Fa</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������ɫ��</font></td>
                <td bgcolor=$forumcolortwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumcolortwo" value="$forumcolortwo" size=7 maxlength=7>��Ĭ�ϣ�#F2F8FF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫ</font></td>
                <td bgcolor=$forumfontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumfontcolor" value="$forumfontcolor" size=7 maxlength=7>��Ĭ�ϣ�#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>�ظ���ɫ</center></b><br>
                <font color=#333333>�ظ�������ɫ(topic.cgi)
                </td></tr>


                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ���ɫһ</font></td>
                <td bgcolor=$postcolorone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcolorone" value="$postcolorone" size=7 maxlength=7>��Ĭ�ϣ�#EFF3F9</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ���ɫ��</font></td>
                <td bgcolor=$postcolortwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcolortwo" value="$postcolortwo" size=7 maxlength=7>��Ĭ�ϣ�#F2F4EF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ�������ɫһ</font></td>
                <td bgcolor=$postfontcolorone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolorone" value="$postfontcolorone" size=7 maxlength=7>��Ĭ�ϣ�#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ�������ɫ��</font></td>
                <td bgcolor=$postfontcolortwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolortwo" value="$postfontcolortwo" size=7 maxlength=7>��Ĭ�ϣ�#555555</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>ҳ����</center></b><br>
                <font color=#333333>ÿҳ��ʾ����Ļظ�������һƪ����ظ�����һ������ʱ��ҳ��ʾ (topic.cgi)
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÿҳ������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxthreads" value="$maxthreads" size=3 maxlength=3>��һ��Ϊ 20 -- 30</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÿ����ÿҳ�Ļظ���</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtopics" value="$maxtopics" size=3 maxlength=3>��һ��Ϊ 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�ظ����������ٺ������������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hottopicmark" value="$hottopicmark" size=3 maxlength=3>��һ��Ϊ 10 -- 15</td>
                </tr>
                <tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ͶƱ���������ٺ��������ͶƱ����</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hotpollmark" value="$hotpollmark" size=3 maxlength=3>��һ��Ϊ 10 -- 15</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostpic\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostpic\"/value=\"$arrawpostpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>LB5000 ��ǩ����</center></b>(̳���Ͱ������ܴ���)<br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�������ͼ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostflash\"><option value=\"off\">������<option value=\"on\" >����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostflash\"/value=\"$arrawpostflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ����� Flash��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostreal\"><option value=\"off\">������<option value=\"on\" >����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostreal\"/value=\"$arrawpostreal\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ������� Real �ļ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostmedia\"><option value=\"off\">������<option value=\"on\" >����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostmedia\"/value=\"$arrawpostmedia\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ������� Media �ļ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostsound\"><option value=\"off\">������<option value=\"on\" >����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostsound\"/value=\"$arrawpostsound\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�����������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostfontsize\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostfontsize\"/value=\"$arrawpostfontsize\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�����ı����ִ�С��</font></td>
                <td bgcolor=#FFFFFF>
                 $tempoutput
		</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"arrawsignpic\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawsignpic\"/value=\"$arrawsignpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�������ͼ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;
		$tempoutput = "<select name=\"arrawsignflash\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawsignflash\"/value=\"$arrawsignflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ����� Flash��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;


		$tempoutput = "<select name=\"arrawsignsound\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawsignsound\"/value=\"$arrawsignsound\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�����������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"arrawsignfontsize\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawsignfontsize\"/value=\"$arrawsignfontsize\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�����ı����ִ�С��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

		<tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳��ť����</b> (��ͼ������ images Ŀ¼�£�ֻ�������ƣ������Լ� URL ��ַ�����·��)<br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��������ťͼ��</font>��(��С��99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newthreadlogo" value="$newthreadlogo" onblur="document.images.i_newthreadlogo.src='$imagesurl/images/'+this.value;">��
                <img src=$imagesurl/images/$newthreadlogo name="i_newthreadlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ͶƱ��ťͼ��</font>��(��С��99*25)</td>
                <td bgcolor=#FFFFFF>
		<input type=text name="newpolllogo" value="$newpolllogo" onblur="document.images.i_newpolllogo.src='$imagesurl/images/'+this.value;">��
                <img src=$imagesurl/images/$newpolllogo name="i_newpolllogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>С�ֱ���ťͼ��</font>��(��С��99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newxzblogo" value="$newxzblogo" onblur="document.images.i_newxzblogo.src='$imagesurl/images/'+this.value;">��
                <img src=$imagesurl/images/$newxzblogo name="i_newxzblogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�ظ����Ӱ�ťͼ��</font>��(��С��99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newreplylogo" value="$newreplylogo" onblur="document.images.i_newreplylogo.src='$imagesurl/images/'+this.value;">��
                <img src=$imagesurl/images/$newreplylogo name="i_newreplylogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ԭ���ڰ�ťͼ��</font>��(��С��74*21)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="wlogo" value="$wlogo" onblur="document.images.i_wlogo.src='$imagesurl/images/'+this.value;">��
                <img src=$imagesurl/images/$wlogo name="i_wlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�´��ڰ�ťͼ��</font>��(��С��74*21)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="nwlogo" value="$nwlogo" onblur="document.images.i_nwlogo.src='$imagesurl/images/'+this.value;">��
                <img src=$imagesurl/images/$nwlogo name="i_nwlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������ťͼ��</font>��(��С������)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="help_blogo" value="$help_blogo" onblur="document.images.i_help_blogo.src='$imagesurl/images/'+this.value;">��
                <img src=$imagesurl/images/$help_blogo name="i_help_blogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������� new ͼ��</font>��(��С������)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="new_blogo" value="$new_blogo" onblur="document.images.i_new_blogo.src='$imagesurl/images/'+this.value;">��
                <img src=$imagesurl/images/$new_blogo name="i_new_blogo"></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��̳������ʽ����</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������ÿ������������ʾ�Ĵ���</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsmail" value="$maxsmail" size=2 maxlength=2>��һ�� 2 -- 5 ��������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�ظ�ʱ��Ĭ���г������ظ�����</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxlistpost" value="$maxlistpost" size=2 maxlength=2>��һ�� 5 -- 8 ��������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̶��ڶ��˵���������<br>���Թ̶�������Ҫ��������̳�������档</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtoptopic" value="$maxtoptopic" size=2 maxlength=2>��һ�� 1 -- 5 ��������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ԥ�����ַ���</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsavepost" value="$maxsavepost" size=3 maxlength=3>����Ҫ���� 50����������Ӱ���ٶ�</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��̳ͶƱ����������������Ŀ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpollitem" value="$maxpollitem" size=2 maxlength=2>�������� 5 - 50 ֮��</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>�������</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����β��������</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adfoot" rows="5" cols="40">$adfoot</textarea><BR><BR>
                </td>
                </tr>
		~;

               $tempoutput = "<select name=\"forumimagead\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
               $tempoutput =~ s/value=\"$forumimagead\"/value=\"$forumimagead\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>�Ƿ�ʹ�÷���̳�������</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�������ͼƬ URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�����������Ŀ����ַ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink" value="$adimagelink"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�������ͼƬ���</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth" value="$adimagewidth" maxlength=3>&nbsp;����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�������ͼƬ�߶�</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight" value="$adimageheight" maxlength=3>&nbsp;����</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"useimageadtopic\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
               $tempoutput =~ s/value=\"$useimageadtopic\"/value=\"$useimageadtopic\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>�鿴�˷���̳������ʱ�Ƿ�<BR>ʹ�ô˸������</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput�������������<BR>����̳��ʹ�ø������Ļ�����ѡ����Ч<BR><BR></td>
               </tr>
		~;

               $tempoutput = "<select name=\"forumimagead1\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
               $tempoutput =~ s/value=\"$forumimagead1\"/value=\"$forumimagead1\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>�Ƿ�ʹ�÷���̳���¹̶����</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳���¹̶����ͼƬ URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage1" value="$adimage1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳���¹̶��������Ŀ����ַ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink1" value="$adimagelink1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳���¹̶����ͼƬ���</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth1" value="$adimagewidth1" maxlength=3>&nbsp;����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳���¹̶����ͼƬ�߶�</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight1" value="$adimageheight1" maxlength=3>&nbsp;����</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"useimageadtopic1\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
               $tempoutput =~ s/value=\"$useimageadtopic1\"/value=\"$useimageadtopic1\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>�鿴�˷���̳������ʱ�Ƿ�<BR>ʹ�ô����¹̶����</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput�������������<BR>����̳��ʹ�����¹̶����Ļ�����ѡ����Ч</td>
               </tr>
<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><center><b>��ʼ����Ч����</b> (Leoboard.cgi & Forums.cgi)</center><br>
</font></td>
</tr>
~;


$tempoutput = "<select name=\"pagechange\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
$tempoutput =~ s/value=\"$pagechange\"/value=\"$pagechange\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>����ҳ��ʱ�Ƿ�ʹ����Ч?</b><br>IE 4.0 ���ϰ汾�������Ч</font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

$tempoutput = "<select name=\"cinoption\">\n
<option value=\"0\">��״����\n
<option value=\"1\">��״����\n
<option value=\"2\">Բ������\n
<option value=\"3\">Բ�η���\n
<option value=\"4\">���ϲ���\n
<option value=\"5\">���²���\n
<option value=\"6\">���Ҳ���\n
<option value=\"7\">�������\n
<option value=\"8\">��ֱ�ڱ�\n
<option value=\"9\">ˮƽ�ڱ�\n
<option value=\"10\">��������ʽ\n
<option value=\"11\">��������ʽ\n
<option value=\"12\">����ֽ�\n
<option value=\"13\">��������������\n
<option value=\"14\">������������չ\n
<option value=\"15\">��������������\n
<option value=\"16\">������������չ\n
<option value=\"17\">�����³��\n
<option value=\"18\">�����ϳ��\n
<option value=\"29\">�����³��\n
<option value=\"20\">�����ϳ��\n
<option value=\"21\">���ˮƽ����\n
<option value=\"22\">�����ֱ����\n
<option value=\"23\">���(�����κ�һ��)\n
</select>\n";
$tempoutput =~ s/value=\"$cinoption\"/value=\"$cinoption\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>��Ч����?</b></font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>��Чά��ʱ��?</b><br>���� 1.0 = 1 ��, 0.5 = 1/2 ��.</font></td>
<td bgcolor=#FFFFFF>
<input type=text size=10 name="timetoshow" value="$timetoshow"> Ĭ�ϣ�1</td>
</tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��������</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>��Ȩ��Ϣ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>
                 ~;

                $tempoutput = "<select name=\"floodcontrol\"><option value=\"off\">��<option value=\"on\">��</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>�Ƿ��ˮԤ�����ƣ�</b><br>ǿ���Ƽ�ʹ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>�û����������ʱ��</b><br>��ˮԤ�����Ʋ���Ӱ�쵽̳�������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="floodcontrollimit" value="$floodcontrollimit" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>����Сʱ�ڵ���������� new ��־��<BR>(�������Ҫ����������Ϊ 0)</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newmarktime" value="$newmarktime" size=3 maxlength=3>��һ�� 12 - 24 Сʱ</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"look\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$look\"/value=\"$look\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ񿪷ű�����ɫ���ܣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"announcemove\">\n<option value=\"on\">�ƶ�\n<option value=\"off\">���ƶ�\n</select>\n";
               	$tempoutput =~ s/value=\"$announcemove\"/value=\"$announcemove\" selected/;
               	print qq~

               	<tr>
               	<td bgcolor=#FFFFFF colspan=2>
               	<font color=#333333>��̳�����Ƿ�����ƶ����</font></td>
               	<td bgcolor=#FFFFFF>
               	$tempoutput</td>
               	</tr>
               	~;

                $tempoutput = "<select name=\"announcements\"><option value=\"no\">��ʹ��<option value=\"yes\">ʹ��</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>�Ƿ�ʹ�ù�����̳</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;

                $tempoutput = "<select name=\"sticky\"><option value=\"off\">����˳���µķ������<option value=\"on\">�������⣬�µķ���������</select>\n";
                $tempoutput =~ s/value=\"$sticky\"/value=\"$sticky\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>�鿴���ӻظ���ʱ�����µĻظ��ǽ��������أ����Ƿ������</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"refreshurl\"><option value=\"0\">�Զ����ص�ǰ��̳<option value=\"1\">�Զ����ص�ǰ����</select>\n";
                $tempoutput =~ s/value=\"$refreshurl\"/value=\"$refreshurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>�����ظ����Ӻ��Զ�ת�Ƶ���</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"postopen\"><option value=\"yes\">���Է����ظ�����<option value=\"no\">���������ظ�����</select>\n";
                $tempoutput =~ s/value=\"$postopen\"/value=\"$postopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳�����ظ����⹦�ܣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pollopen\"><option value=\"yes\">��ͶƱ<option value=\"no\">�ر�ͶƱ</select>\n";
                $tempoutput =~ s/value=\"$pollopen\"/value=\"$pollopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳ͶƱ���ܣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"xzbopen\"><option value=\"yes\">��С�ֱ�<option value=\"no\">�ر�С�ֱ�</select>\n";
                $tempoutput =~ s/value=\"$xzbopen\"/value=\"$xzbopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳С�ֱ����ܣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"useemote\"><option value=\"yes\">ʹ��<option value=\"no\">��ʹ��</select>\n";
                $tempoutput =~ s/value=\"$useemote\"/value=\"$useemote\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ�ʹ�� EMOTE ��ǩ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"regaccess\"><option value=\"off\">���������κ��˷���<option value=\"on\">�ǣ������½����ܷ���</select>\n";
                $tempoutput =~ s/value=\"$regaccess\"/value=\"$regaccess\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��ֻ̳��ע���û����Է��ʣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowuserdel\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$arrowuserdel\"/value=\"$arrowuserdel\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ�����ע���û��Լ�ɾ���Լ������ӣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"newmsgpop\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$newmsgpop\"/value=\"$newmsgpop\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���µĶ���Ϣ�Ƿ񵯳�������ʾ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pvtip\">\n<option value=\"on\">��ʾ IP �ͼ���\n<option value=\"off\">���� IP �ͼ���\n</select>\n";
                $tempoutput =~ s/value=\"$pvtip\"/value=\"$pvtip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>�Ƿ��� IP �ͼ�����</b><BR>��ʹѡ�������ʾ IP������ͨ�û�����<BR>ֻ�ܿ��� IP ��ǰ��λ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput���˹��ܶ�̳����Ч</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"smocanseeip\">\n<option value=\"yes\">��Ч\n<option value=\"no\">��Ч\n</select>\n";
                $tempoutput =~ s/value=\"$smocanseeip\"/value=\"$smocanseeip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>���� IP �ͼ������ܰ����Ƿ���Ч��</b><BR>��ѡ����Ч�����ܰ����ɲ鿴���е� IP<BR>���������� IP ���ܵ�����</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"arrowupload\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$arrowupload\"/value=\"$arrowupload\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����Ƿ������ϴ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput���˹��ܶ԰�����̳����Ч</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"allowattachment\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$allowattachment\"/value=\"$allowattachment\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�ظ��Ƿ������ϴ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput���˹��ܶ԰�����̳����Ч</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��̳�ϴ��ļ���������ֵ(��λ��KB)<br>��������˲������ϴ����������Ч��</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxupload" value="$maxupload" size=5 maxlength=5>����Ҫ�� KB ���������鲻Ҫ���� 500 ��</td>
                </tr>

                ~;

                $tempoutput = "<select name=\"quotemode\">\n<option value=\"0\">���\n<option value=\"1\">����\n</select>\n";
                $tempoutput =~ s/value=\"$quotemode\"/value=\"$quotemode\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���ñ�ǩ����ʽ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"defaulttopicshow\"><option value=>�鿴���е�����<option value=\"1\">�鿴һ���ڵ�����<option value=\"2\">�鿴�����ڵ�����<option value=\"7\">�鿴һ�����ڵ�����<option value=\"15\">�鿴������ڵ�����<option value=\"30\">�鿴һ�����ڵ�����<option value=\"60\">�鿴�������ڵ�����<option value=\"180\">�鿴�����ڵ�����</select>\n";
                $tempoutput =~ s/value=\"$defaulttopicshow\"/value=\"$defaulttopicshow\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ĭ����ʾ������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"defaulforumcshow\"><option value=\"orderlastpostd\">�����ظ�ʱ�併��<option value=\"orderlastposta\">�����ظ�ʱ������<option value=\"orderthreadd\">�����ⷢ��ʱ�併��<option value=\"orderthreada\">�����ⷢ��ʱ������<option value=\"orderstartbyd\">�����ⷢ���˽���<option value=\"orderstartbya\">�����ⷢ��������<option value=\"orderclickd\">��������������<option value=\"orderclicka\">��������������<option value=\"orderreplyd\">������ظ�������<option value=\"orderreplya\">������ظ�������<option value=\"ordertitled\">��������⽵��<option value=\"ordertitlea\">�������������</select>\n";
                $tempoutput =~ s/value=\"$defaulforumcshow\"/value=\"$defaulforumcshow\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ĭ����������ʽ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"onlineview\">\n<option value=\"1\">��ʾ\n<option value=\"0\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$onlineview\"/value=\"$onlineview\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ĭ���Ƿ���ʾ�����û���ϸ�б�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"advpost\">\n<option value=\"1\">�߼�ģʽ\n<option value=\"0\">���ģʽ\n</select>\n";
                $tempoutput =~ s/value=\"$advpost\"/value=\"$advpost\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ĭ�Ϸ���ģʽ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"sortalltopic\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$sortalltopic\"/value=\"$sortalltopic" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ񿪷���̳��������쿴���ܣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"dispquickreply\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$dispquickreply\"/value=\"$dispquickreply" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ����ÿ��ٻظ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispview\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispview\"/value=\"$dispview\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>�Ƿ���ʾ��̳ͼ��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"refreshforum\">\n<option value=\"off\">��Ҫ�Զ�ˢ��\n<option value=\"on\">Ҫ�Զ�ˢ��\n</select>\n";
                $tempoutput =~ s/value=\"$refreshforum\"/value=\"$refreshforum" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������̳�Ƿ��Զ�ˢ��(�����������ü��ʱ��)��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Զ�ˢ����̳��ʱ����(��)<BR>����������һ��ʹ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="autofreshtime" value="$autofreshtime" size= 5 maxlength=4>��һ������ 5 ���ӣ����� 300 �롣</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>����̳������������</b>(���û��������)<br>�����뱳���������ƣ���������<BR>Ӧ�ϴ��� non-cgi/midi Ŀ¼�¡�<br><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="midiaddr" value="$midiaddr">~;
                $midiabsaddr = "$imagesdir" . "midi/$midiaddr";
                print qq~��<EMBED src="$imagesurl/midi/$midiaddr" autostart="false" width=70 height=25 loop="true" align=absmiddle>~ if ((-e "$midiabsaddr")&&($midiaddr ne ""));
                print qq~
                </td>
                </tr>
                <td bgcolor=#FFFFFF align=center colspan=3>
                <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
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
                <b>��ӭ������̳�������� / ����̳����趨</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE colspan=2>
                <font color=#333333><center><b>������Ϣ�Ѿ��ɹ�����</b><br><br>
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
                    <b>��ӭ������̳�������� / ����̳����趨</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>������Ϣû�б���</b><br>�ļ�����Ŀ¼����д<br>������� data Ŀ¼�� styles*.cgi �ļ������ԣ�
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
        <b>��ӭ������̳�������� / �༭��̳</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>�༭ '$category' �����е� '$forumname' ��̳</b>
        </td></tr>

        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="doedit">
        <input type=hidden name="forum" value="$inforum">
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳����</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumname" value="$forumname"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳����</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳�����������ϣ���ж����������ʹ�� "," (Ӣ�Ķ��ţ��������Ķ���)������<BR><B>����</B>��ɽӥ��, ����ȱ</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>
        ~;

        $tempoutput = qq~<select name="htmlstate"><option value="on">ʹ��<option value="off">��ʹ��</select>~;
        $tempoutput =~ s/value=\"$htmlstate\"/value=\"$htmlstate\" selected/g;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� HTML ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="idmbcodestate"><option value="on">ʹ��<option value="off">��ʹ��</select>~;
        $tempoutput =~ s/value=\"$idmbcodestate\"/value=\"$idmbcodestate\" selected/g;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� LB5000 ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="privateforum"><option value="yes">��<option value="no">��</select>~;
        $tempoutput =~ s/value=\"$privateforum\"/value=\"$privateforum\" selected/g;
        if (!$privateforum) {
            $tempoutput = qq~<select name="privateforum"><option value="yes">��<option value="no" selected>��</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���Ϊ˽����̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput  ��̳�����ܰ�����Ч
        </td>
        </tr>
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>˽����̳����</b>(ֻ��˽����̳��Ч)</font></td>
        <td bgcolor=#FFFFFF>
       <input type=text size=12 name="forumpass" value="$forumpass" maxlength=20> ��̳�����ܰ�����Ч</td>
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="hiddenforum"><option value="yes">��<option value="no">��</select>~;
        $tempoutput =~ s/value=\"$hiddenforum\"/value=\"$hiddenforum\" selected/g;
        if (!$hiddenforum) {
            $tempoutput = qq~<select name="hiddenforum"><option value="yes">��<option value="no" selected>��</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�������̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="indexforum"><option value="yes">��<option value="no">��</select>~;
        $tempoutput =~ s/value=\"$indexforum\"/value=\"$indexforum\" selected/g;
        if (!$indexforum) {
            $tempoutput = qq~<select name="indexforum"><option value="yes" selected>��<option value="no" >��</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���ʾ��������</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>

        ~;

        $tempoutput = qq~<select name="startnewthreads"><option value="yes" selected>������̳<option value="all">������̳<option value="follow">������̳<option value="no">������</select>~;
        $tempoutput =~ s/value=\"$startnewthreads\"/value=\"$startnewthreads\" selected/g;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>1. ������̳-ֻ����ע���Ա����<br>2. ������̳-���������˷���<br>3. ������̳-̳���Ͱ��������ԣ�����ע���û�ֻ�ܻظ�<br>4. ������-ֻ���������̳�����ԺͲ���<br>5. ��֤��̳-��̳���Ͱ����⣬����ע���û�������Ҫ��֤</font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;

        $tempoutput = qq~<select name="ratings"><option value="On">����<option value="">������</select>~;
        $tempoutput =~ s/value=\"$ratings\"/value=\"$ratings\" selected/g;
        print qq~

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>���������ͶƱ���֣�</b></font></td>
        <td bgcolor=#FFFFFF>
	  $tempoutput
	  </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳ͼƬ</b><br>������ͼƬ���ƣ���ͼƬ������������ҳ����߲˵��¡�<BR><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumgraphic" value="$forumgraphic"></td>
        </tr>

	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font face=���� color=#333333><b>����ͼƬ</b>(���û�У��뱣��ԭ��)<br>������ͼƬ���ƣ���ͼƬ��������������ҳ���¡�<BR><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamlogo" value="$teamlogo"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font face=���� color=#333333><b>������ַ</b>(���û�У��뱣��ԭ��)</td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamurl" value="$teamurl"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
        ~;

} # end route

##################################################################################
######## Subroutes ( Processing the edit of a forum)


sub doedit {
	&errorout("������̳�����벻�ܿգ���") if (($new_privateforum eq "yes")&&($new_forumpass eq ""));
	&errorout("�Բ�����̳���ֹ������������ 20 �������ڣ�") if (length($new_forumname) >40);
	&errorout("��̳���ֲ��ܿգ���") if ($new_forumname eq "");
	&errorout("��̳�������ܿգ���") if ($new_forumdescription eq "");
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
                <b>��ӭ������̳�������� / �༭��̳���</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ�����</b><p>
                ������趨��ĳ��Ϊ��������������ӹ������ı༭�������ϣ�ʹ����Ϊ������<BR>
                ��ʵ�����û��Ҫ�ġ��������Ӱ�췢�������ֱ��ϵ� 'team' ͼ�꣬�ǰ�������ʾ 'team' ͼ�꣡</font>
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
        <b>��ӭ������̳�������� / ���ӷ���(ͬʱ����һ����̳)</b>
        </td></tr>
        <tr>

        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���ӷ���(ͬʱ����һ����̳)</b>
        </td></tr>


        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��������</b><br>�������·�������</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="categoryname" value="$categoryname"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳����</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumname" value="$forumname"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳����</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳�����������ϣ���ж����������ʹ�� "," (Ӣ�Ķ��ţ��������Ķ���)������<BR><B>����</B>��ɽӥ��, ����ȱ</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� HTML ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="htmlstate">
        <option value="on">ʹ��<option value="off" selected>��ʹ��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� LB5000 ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="idmbcodestate">
        <option value="on" selected>ʹ��<option value="off">��ʹ��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���Ϊ˽����̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="privateforum">
        <option value="yes">��<option value="no" selected>��</select> ��̳�����ܰ�����Ч
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>˽����̳����</b>(��������������ʹ��)</font></td>
        <td bgcolor=#FFFFFF>
       <input type=text size=12 name="forumpass" value="$forumpass" maxlength=20> ��̳�����ܰ�����Ч</td>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�������̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="hiddenforum">
        <option value="yes">��<option value="no" selected>��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���ʾ��������</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="indexforum">
        <option value="yes" selected>��<option value="no" >��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>1. ������̳-ֻ����ע���Ա����<br>2. ������̳-���������˷���<br>3. ������̳-̳���Ͱ��������ԣ�����ע���û�ֻ�ܻظ�<br>4. ������-ֻ���������̳�����ԺͲ���<br>5. ��֤��̳-��̳���Ͱ����⣬����ע���û�������Ҫ��֤</font></td>
        <td bgcolor=#FFFFFF>
        <select name="startnewthreads">
        <option value="yes" selected>������̳<option value="all">������̳<option value="follow">������̳<option value="no">������</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>���������ͶƱ���֣�</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="ratings">
        <option value="On">����<option value="" selected>������</select>
	  </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳ͼƬ</b><br>������ͼƬ���ƣ���ͼƬ������������ҳ����߲˵��¡�<BR><b>��Ҫ���� URL ��ַ�����·����</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumgraphic" value="logo.gif"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font face=���� color=#333333><b>����ͼƬ</b>(���û�У��뱣��ԭ��)<br>������ͼƬ���ƣ���ͼƬ��������������ҳ���¡�<BR><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamlogo" value=""></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font face=���� color=#333333><b>������ַ</b>(���û�У��뱣��ԭ��)</td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamurl" value="http://"></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
        ~;

} # end route


##################################################################################
######## Subroutes ( Create New cat/forum )


sub doaddcategory {
		&errorout("������̳�����벻�ܿգ���") if (($new_privateforum eq "yes")&&($new_forumpass eq ""));
		&errorout("�Բ�����̳���ֹ������������ 20 �������ڣ�") if (length($new_forumname) >40);
		&errorout("��̳���ֲ��ܿգ���") if ($new_forumname eq "");
		&errorout("��̳�������ܿգ���") if ($new_forumdescription eq "");
		&errorout("��̳����ܿգ���") if ($new_categoryname eq "");
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
                <b>��ӭ������̳�������� / ���ӷ���(ͬʱ����һ����̳)���</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>
                ~;

                print "<b>��ϸ��Ϣ��</b><p>\n";
                print "<ul>\n";
                if (-e $dirtomake) {
                print "<li><b>�µķ������̳�Ѿ�����</b><p>\n";
                    }
                    else {
                        print "<li><b>�µķ������̳û�н���</b><p>��鿴�Ƿ�ı���Ŀ¼���ԣ�������Ի� 777 ��<p>\n";
                        }


                $filetoopen = "$dirtomake/index.html";
                if (-e $filetoopen) {
                    print "<li><b>����̳ (index.html) �ļ�����</b><p>\n";
                    }
                    else {
                        print "<li><b>����̳ (index.html) �ļ�û�н���</b><p>��鿴�Ƿ�ı���Ŀ¼���ԣ�������Ի� 777 ��<p>\n";
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
            <b>��ӭ������̳�������� / �༭��������</b>
            </td></tr>
            <tr>

            <tr>
            <td bgcolor=#EEEEEE align=center colspan=2>
            <font color=#990000><b>�༭ '$categoryname' ���������</b>
            </td></tr>


            <tr>
            <td bgcolor=#FFFFFF width=40%>
            <font color=#333333><b>��������</b><br>�������������</font></td>
            <td bgcolor=#FFFFFF>
            <input type=text size=40 name="categoryname" value="$categoryname"></td>
            </tr>


            <tr>
            <td bgcolor=#FFFFFF align=center colspan=2>
            <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
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
                <b>��ӭ������̳�������� / �༭�������ƽ��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ��ɹ�����</b>
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
            <b>��ӭ������̳�������� / ��̳������������</b>
            </td></tr>
            <tr><td bgcolor=#FFFFFF" colspan=3><font color=#333333>
            <b>ע�����</b><br><br>
            �ڴ������Խ���̳�����������򡣷��ཫ��������������ʾ��<BR><BR><b>1 ��ʾ��Ϊ��һ���࣬����ʾ����ǰ��</b>��<br><br>
            <b>�ύ֮ǰ����ϸ����������ã�����֤û���ظ����֣����ظ����ᵼ���еķ����޷���ʾ��</b><br><br>
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
                    <td bgcolor=#FFFFFF><font color=#333333>����λ�� [ <B>$categoryplace</B> ]���������µ������Ա�����<input type=text size=4 maxlength=2 name="$categoryplace" value="$categoryplace">
                    </td></tr>
                    ~;
                    } # end if

                    $lastcategoryplace = $categoryplace;

                 } # end foreach



                    print qq~
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <BR><input type=submit value="�� ��"></td></form></tr></table></td></tr></table>
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
                <b>��ӭ������̳�������� / �༭�������ƽ��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ��ɹ�����</b>
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
            <b>��ӭ������̳�������� / ��̳��������</b>
            </td></tr>
            <tr><td bgcolor=#FFFFFF" colspan=3><font color=#333333>
            <b>ע�����</b><br><br>
            �ڴ������Խ�����̳��������<br>����̳���Զ�����˳�����¸ı�˳��ͷ�������
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
            <tr><td>����̳ <font color=red>$myforumname</font> �Ƶ���̳
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
                    $jumphtml�£������Զ��ı�������ԡ�
                   </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <BR><input type=submit value="�� ��"></td></form></tr></table></td></tr></table>
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
                <b>��ӭ������̳�������� / ����̳�������ƽ��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ��ɹ�����</b>
                </td></tr></table></td></tr></table>
                ~;

                } # end else


} # end routine

print qq~</td></tr></table></body></html>~;
exit;

sub errorout {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / ��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>
                <font color=#333333><b>$_[0]</b>
                </td></tr></table></td></tr></table>
                ~;
exit;
}