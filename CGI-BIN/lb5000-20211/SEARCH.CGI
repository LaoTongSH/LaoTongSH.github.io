#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ����������)
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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "search.cgi";

$query = new LBCGI;

&ipbanned; #��ɱһЩ ip

for ('TYPE_OF_SEARCH','NAME_SEARCH','POST_SEARCH','FORUMS_TO_SEARCH','action', 'forum',
	'SEARCH_STRING','REFINE_SEARCH','CUR_TIME','nextforum', 'start') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
    }
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($forum) && ($forum !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($CUR_TIME) && ($CUR_TIME !~ /^[0-9]+$/));
$SEARCH_STRING =~ s/^system //g;

$ipaddress    = $ENV{'REMOTE_ADDR'};
$inmembername = $query->cookie("amembernamecookie");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
$filename = $inmembername;

if (!$filename) {
    $filename = "����$ipaddress";
    $filename =~ s/\.//g;
	$filename =~ s/\///g;
	$filename =~ s/\\//g;
}
else {
&getmember("$inmembername");
if ($userregistered eq "no") { &error("��̳����&�㻹ûע���أ�"); }
}

if ($inmembername eq "") {
   $inmembername = "����";
}

if ($searchopen == 1) {
    &error("��̳����&������Ȩ������̳������") if ($inmembername eq "����");
}

$filename =~ y/ /_/;
$filename =~ tr/A-Z/a-z/;
$filename = "$filename" . "_sch.cgi";

$searchfilename = "$lbdir" . "search/$filename";

$dirtoopen = "$lbdir" . "search";
opendir(DIR, "$dirtoopen");
while ($file = readdir(DIR)) {
	if ((stat("$dirtoopen/$file"))[9] < (time - 30*60)) {
    unlink("$dirtoopen/$file");
	}
}
closedir(DIR);

print header(-charset=>gb2312);
&badwordfile;

&title;

    $output .= qq~
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
        <tr>
            <td width=30% rowspan=2 valign=top>
            <img src="$imagesurl/images/$boardlogo" border=0>
            </td>
            <td valign=top align=left>
            <font face="$font" color=$fontcolormisc>
	           &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0>��<a href="$forumsummaryprog">$boardname</a>
	           <br>
            &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>����������
            </td>
            </tr>
       </table>
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=8 cellspacing=1 border=0 width=100%>
    ~;




# Do we have a search folder?

if (!-d "$dirtoopen") {
    mkdir("$dirtoopen", 0777) or die "�����ܽ�������Ŀ¼����ʹ�� FTP �� cgi-bin �е� LB5000 �½���һ�� search Ŀ¼��\n";
    chmod(0777, "$dirtoopen");
    }

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\t����\tnone\t��������Ҫ�������\t");
}

if ($action eq "startsearch") {

    $SEARCH_STRING =~ s/\, /\,/g;

    if ($TYPE_OF_SEARCH eq "username_search") {
        $REFINE_SEARCH = "$NAME_SEARCH";
        }
        else {
            $REFINE_SEARCH = "$POST_SEARCH";
            }


    open (SEARCH, ">$searchfilename") or die "���ܹ����浽 search Ŀ¼�������ô�Ŀ¼Ϊ 777 ��\n";
    print SEARCH "$CUR_TIME\n";
    print SEARCH "$SEARCH_STRING\n";
    print SEARCH "$TYPE_OF_SEARCH\n";
    print SEARCH "$REFINE_SEARCH\n";
    print SEARCH "$FORUMS_TO_SEARCH\n";
    close (SEARCH);

    $relocurl = "$boardurl/$thisprog?action=continue";

        $output .= qq~
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>������....</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
            ��ȴ��������������<br>
            <b>��ǰ���������</b>
            <ul>
            <li>�������....
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="1; url=$relocurl">
            ~;

    }

    elsif ($action eq "display") {
         &displayresults;
         }

    elsif ($action eq "continue") {

        &getmember($inmembername);

        # Grab the params

        open (INSEARCH, "$searchfilename");
        @searchparam = <INSEARCH>;
        close (INSEARCH);

        my $SEARCH_STRING    = $searchparam[1];
        chomp $SEARCH_STRING;
        my $TYPE_OF_SEARCH   = $searchparam[2];
        chomp $TYPE_OF_SEARCH;
        my $REFINE_SEARCH    = $searchparam[3];
        chomp $REFINE_SEARCH;
        my $FORUMS_TO_SEARCH = $searchparam[4];
        chomp $FORUMS_TO_SEARCH;


        @KEYWORDS = split(/\,/,$SEARCH_STRING);

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
        @forums = <FILE>;
        close(FILE);

        @checkforums = @forums;
        @checkforums = reverse(@checkforums);

        $search_in_forum = $FORUMS_TO_SEARCH;

        if ($FORUMS_TO_SEARCH eq "all") {
            $nextforum++;
            $search_in_forum = $nextforum;
            ($forumno, $trash) = split(/\t/,$checkforums[0]);

            if ("$search_in_forum" > "$forumno") { $nofile="true"; $FORUMS_TO_SEARCH = "done"; }
            }


        foreach $forum (@forums) { #start foreach @forums
            chomp $forum;
            ($tempforumno, $trash) = split(/\t/,$forum);
            if ($tempforumno eq $search_in_forum) { #1
                ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum) = split(/\t/,$forum);
                $nofile = "true" if (($privateforum eq "yes") && ($allowedentry{$forumid} ne "yes") &&($membercode ne "ad")&&($membercode ne 'smo'));
                } #e1
               else { next; }
            } # end foreach @allforums


            $filetoopen = "$lbdir" . "boarddata/list$forumid.cgi";
            open(FILE, "$filetoopen") or $nofile = "true";
            @topics = <FILE>;
            close(FILE);

            if ($nofile ne "true") { #start nofile
            foreach $topic (@topics) { # start topic foreach
                chomp $topic;
                ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\t/,$topic);
	        $topictitle =~ s/^����������//;

                if ($TYPE_OF_SEARCH eq "keyword_search") {

                    if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "topictitle_search") { #1
                        foreach (@KEYWORDS) { #new1
                            if (($topictitle =~ m|$_|gi)  and ("$lida" ne "$topicid")) { #2
                                $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$startedpostdate\t�ҵ��ؼ��֣� <B>$_</B>");
                                push (@founditems, $founditem);
                                $lida = $topicid;
                                } #e2
                             }
                        } #e1

                            if (($REFINE_SEARCH eq "both_search") or ($REFINE_SEARCH eq "post_search")) { # 1
                                $filetoopen = "$lbdir" . "forum$forumid/$topicid.thd.cgi";
                                open (THREAD, "$filetoopen") or next;
                                @thddata = <THREAD>;
                                close (THREAD);

                                foreach (@thddata) { # start foreach 'thd'
                                    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$_);
                                    foreach (@KEYWORDS) { #new1
                                    if (($post =~ m|$_|gi) and ("$lida" ne "$topicid")) { # s 'if' n1
                                        $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$postdate\t�ҵ� <B>$_</B> ��");
                                        push (@founditems, $founditem);
                                        $lida = $topicid;
                                        } # e 'if' n1
                                      }
                                    } # end foreach 'thd'
                            } # e1
                    } # END MAIN IF 'keyword_search'

                    elsif ($TYPE_OF_SEARCH eq "username_search") {

                        if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "topictitle_search") { #1
                            foreach (@KEYWORDS) { #new1
                            if (($startedby =~ m|$_|gi) and ("$lidc" ne "$topicid")) { #2
                                $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$startedpostdate\t�������ߣ� <B>$_</B>");
                                push (@founditems, $founditem);
                                $lidc = $topicid;
                                } #e2
                               }
                            } #e1

                                if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "post_search") { # 1
                                    $filetoopen = "$lbdir" . "forum$forumid/$topicid.thd.cgi";
                                    open (THREAD, "$filetoopen") or next;
                                    @thddata = <THREAD>;
                                    close (THREAD);
				    $toptttt = 0;
                                    foreach (@thddata) { # start foreach 'thd'
				        $toptttt++;
				        next if ($toptttt == 1);
                                        ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$_);
                                        foreach (@KEYWORDS) { #new1
                                        if (($membername =~ m|$_|gi) and ($lidc != $topicid)) { # s 'if' n1
                                            $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$postdate\t�ظ��ˣ� <B>$membername</B>");
                                            push (@founditems, $founditem);
                                            $lidc = $topicid;
                                            } # e 'if' n1
                                          }
				        $toptttt++;
                                        } # end foreach 'thd'
                                } # e1
                        } # END MAIN ELSIF 'username_search'

                     } # end main foreach list loop

                    # What do we do next? First push all the data to the text file

                        $matches_in_forum = @founditems;
                        $matches_so_far   = @searchparam - 5;

                        open (OUT, ">>$searchfilename") or die "���ܹ����浽 search Ŀ¼�������ô�Ŀ¼Ϊ 777 ��\n";
                        foreach (@founditems) {
                            chomp $_;
                            print OUT "$_\n";
                            }
                        close (OUT);

                    undef @founditems;
                    undef @KEYWORDS;
                    } # end if no file

                    # Then work out where to go

                    if ($FORUMS_TO_SEARCH eq "all") {
                        $relocurl = "$boardurl/$thisprog?action=continue&nextforum=$search_in_forum";
                        }
                        else {
                            $relocurl = "$boardurl/$thisprog?action=display";
                            }

                  if (!$matches_in_forum) {
                  	$matches_in_forum = "������...";
                  }
                  else {
                  	$matches_in_forums = " ��" if ($matches_in_forum);
                  }

                  $matches_so_far   = "������..." if (!$matches_so_far);
                  $forumname        = "������..." if (!$forumname);

                  $output .= qq~
			            <tr>
			            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>������....</b></font></td></tr>
			            <tr>
			            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
			            ��ȴ����������������С�<br>
			            <b>��ǰ���������</b>
			            <ul>
			            <li>��ϸ���....<BR>
                        <li>������̳�� <b>$forumname</b>
                        <li>��������� <b>$matches_so_far</b>
                        <li>ƥ����ϣ� <b>$matches_in_forum</b>$matches_in_forums
			            </ul>
			            </tr>
			            </td>
			            </table></td></tr></table>
			            <meta http-equiv="refresh" content="1; url=$relocurl">
			            ~;

                  } # end if action eq continue


                    else {

                        # Print form

						&getmember("$inmembername");


						$jumphtml .= qq~
						<select name="FORUMS_TO_SEARCH">
						<option value="all">������̳
						~;

						$filetoopen = "$lbdir" . "data/allforums.cgi";
						open(FILE, "$filetoopen");
						@forums = <FILE>;
						close(FILE);

						foreach $forum (@forums) { #start foreach @forums
						    chomp $forum;
						    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
						    next if ($forumid !~ /^[0-9]+$/);
						    next if ($categoryplace !~ /^[0-9]+$/);
						    if ((($privateforum eq "yes") && ($userregistered ne "no") && ($allowedentry{$forumid} eq "yes"))||($membercode eq "ad")||($membercode eq 'smo')) {
						        $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
						        }
						        elsif ($privateforum ne "yes") {
						            $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
						            }
						        push (@rearrangedforums, $rearrange);

						} # end foreach (@forums)

						@finalsortedforums = sort(@rearrangedforums);
foreach my $sortedforums (@finalsortedforums) {
    (my $categoryplace, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $ratings, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $miscadd1,my $miscadd2,my $miscadd3,my $miscadd4,my $miscad5) = split(/\t/,$sortedforums);

    if ($categoryplace ne $lastcategoryplace) {
    $has=0;
          foreach (@hascat){
          $has=1 if ($_ eq $categoryplace);
          }
           if ($has ==0){
        $jumphtml .= "<option value=\"$forumid\">>>&nbsp;$category <<\n";
     foreach my $myforums (@rearrangedforums) {
     (my $mycategoryplace, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $ratings, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $miscadd1,my $miscadd2,my $miscadd3,my $miscadd4,my $miscad5) = split(/\t/,$myforums);
      if (($forumname ne $myforumname)&&($categoryplace eq $mycategoryplace)){
        $jumphtml .= "<option value=\"$forumid\"> $forumname\n";
                                                                             }
                                                }
                             }

    }

    $lastcategoryplace = $categoryplace;
}

$jumphtml .= qq~</select>\n~;
if ($forum) { $jumphtml =~ s/\<option value=\"$forum\"\>/\<option value=\"$forum\" selected\>/isg; }

						$refineposts = qq~<select name="POST_SEARCH">
						                  <option value="topictitle_search">�������������ؼ���
						                  <option value="post_search">�����������������ؼ���
						                  <option value="both_search">���߶�����
						                  </select>
						                  ~;

                        $refinename  = qq~<select name="NAME_SEARCH">
						                  <option value="topictitle_search">������������
						                  <option value="post_search">�����ظ�����
						                  <option value="both_search">���߶�����
						                  </select>
						                  ~;

                     $currenttime = time;

						$output .= qq~
						<tr>
						<td bgcolor="$miscbacktwo" valign=middle colspan=2 align="center">
						<p><form action="$boardurl/$thisprog" method="post">
						<input type=hidden name="action" value="startsearch">
				                <input type=hidden name="CUR_TIME" value="$currenttime">
						<font face="$font" color=$fontcolormisc><b>������Ҫ�����Ĺؼ���</b></font></td></tr>
						<tr>
						<td bgcolor=$miscbackone width colspan=2 align="center" valign="middle"><font face="$font" color=$fontcolormisc><b>������Ҫ�����Ĺؼ���</b>
						(����ؼ���֮��ʹ�ö��� ',' �ָ�)</font><br><br><input type=text size=40 name="SEARCH_STRING"></td></tr>
                        <tr>
						<td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc><b>����ѡ��</b></font></td></tr>

                        <tr>
						<td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
                        <b>��������</b></font>&nbsp;<input name="TYPE_OF_SEARCH" type="radio" value="username_search">
                        </td>
                        <td bgcolor="$miscbackone" align="left" valign="middle">
                        $refinename
                        </td>
                        </tr>
                        <tr>
                        <td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
                        <b>�ؼ�������</b></font>&nbsp;<input name="TYPE_OF_SEARCH" type="radio" value="keyword_search" checked>
                        </td>
                        <td bgcolor="$miscbackone" align="left" valign="middle">
                        $refineposts
                        </td>
                        </tr>
                        <tr>
						<td bgcolor="$miscbacktwo" valign="middle" colspan=2 align=center><font face="$font" color=$fontcolormisc><b>��ѡ��Ҫ��������̳ (��Ҫѡ��Щ�� >> �� << �������ģ���ֻ���������������̳)</b></font></td></tr>
						<tr>
						<td bgcolor="$miscbackone" colspan="2" valign="middle" align="center"><font face="$font" color=$fontcolormisc>
                        <b>������̳�� &nbsp; $jumphtml</b></td>
						</tr>
						<tr>
						<td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center><BR>
						<input type=submit value="��ʼ����">
						</td></form></tr></table></td></tr></table>
						~;
						}
                        &output(
	                    -Title   => "$boardname - ��������",
	                    -ToPrint => "$output",
	                    -Version => $versionnumber
	                    );

sub displayresults {



   open (READ, "$searchfilename") or &error("�������&�Բ����������ֻ�ܱ��� 30 ���ӣ�������������");
   @completed_search = <READ>;
   close (READ);

   foreach (@completed_search) {
      push (@TRUE_RESULTS, $_) if ($_ =~ /\t/)
      }

   $total_results = @TRUE_RESULTS;

   $SEARCH_STRING    = $completed_search[1];
   chomp $SEARCH_STRING;
   $TYPE_OF_SEARCH   = $completed_search[2];
   chomp $TYPE_OF_SEARCH;
   $REFINE_SEARCH    = $completed_search[3];
   chomp $REFINE_SEARCH;
   $FORUMS_TO_SEARCH = $completed_search[4];
   chomp $FORUMS_TO_SEARCH;

   $TYPE_OF_SEARCH = "�ؼ���"      if ($TYPE_OF_SEARCH eq "keyword_search");
   $TYPE_OF_SEARCH = "����"        if ($TYPE_OF_SEARCH eq "username_search");

   $REFINE_SEARCH = "����"         if ($REFINE_SEARCH eq "topictitle_search");
   $REFINE_SEARCH = "��������"     if ($REFINE_SEARCH eq "post_search");
   $REFINE_SEARCH = "����ͻظ�"   if ($REFINE_SEARCH eq "both_search");

   if ($total_results > 0) {
      $result_line = qq(ʹ��<b>$TYPE_OF_SEARCH</b>������ʽ����<b>$REFINE_SEARCH</b>�������� <b>$total_results</b> ����ƥ�������);
      }
      else {
      		$result_line = qq(�Բ���ʹ��<b>$TYPE_OF_SEARCH</b>������ʽ����<b>$REFINE_SEARCH</b>��<b>û��</b>�������κ���ƥ�������);
          }



   $output .= qq~
   <tr>
      <td bgcolor="$miscbacktwo" valign=middle colspan=3 align=center>
         <font face="$font" color=$fontcolormisc>
         $result_line
         </font>
      </td>
   </tr>
   <tr>
      <td bgcolor=$miscbackone valign=middle align=center>
         <font face="$font" color=$fontcolormisc>
         <b>����</b></font>
      </td>
      <td bgcolor=$miscbackone valign=middle align=center>
         <font face="$font" color=$fontcolormisc>
         <b>����ʱ�䡢λ��</b></font>
      </td>
      <td bgcolor=$miscbackone valign=middle align=center>
         <font face="$font" color=$fontcolormisc>
         <b>�ؼ���ƥ��˵��</b></font>
         </font>
      </td>
   </tr>
   ~;
   ### Work out if there is a span, and if so how many pages.

    $maxthreads = 25;
    $numberofitems = $total_results;
    $numberofpages = $numberofitems / $maxthreads;
    $instart = $start;

    if ($numberofitems > $maxthreads) { #if
        $showmore = "yes";
        if ($instart eq "" || $instart < 0) { $instart = 0; }
        if ($instart > 0) { $startarray = $instart; }
            else { $startarray = 0; }
            $endarray = $instart + $maxthreads - 1;
            if ($endarray < ($numberofitems - 1)) { $more = "yes"; }
            if (($endarray > ($maxthreads - 1)) && ($more ne "yes")) { $endarray = $numberofitems - 1; }
            } #
            else {
                $showmore = "no";
                $startarray = 0;
                $pages = qq~<font face="$font" color=$menufontcolor>�������ֻ��һҳ</font>~;
                $endarray = $numberofitems - 1;
                }

    ### if we have multiple pages, print them

        if ($showmore eq "yes") { #1
            if ($maxthreads < $numberofitems) { #2
                ($integer,$decimal) = split(/\./,$numberofpages);
                    if ($decimal > 0) { $numberofpages = $integer + 1; }
                        $pagestart = 0;
                        $counter = 0;
                            while ($numberofpages > $counter) { #3
                                $counter++;
                                if ($instart ne $pagestart) { $pages .= qq~<a href="$thisprog?action=display&start=$pagestart"><font face="$font" color=$fonthighlight><b>$counter</b></font></a> ~; }
                                 else { $pages .= qq~<a href="$thisprog?action=display&start=$pagestart"><font face="$font" color=$menufontcolor>$counter</font></a> ~; }
                                $pagestart = $pagestart + $maxthreads;
                                } #e3
                            } #e2
                $pages = qq~<font face="$font" color=$menufontcolor><b>����������ж�ҳ</b> [ $pages ]~;
                } #1

   foreach (@TRUE_RESULTS[$startarray .. $endarray]) { # start foreach loop

   ($forumid, $topicid, $topictitle, $topicdescription, $forumname, $postdate, $string_returned) = split(/\t/,$_);
    $topictitle =~ s/^����������//;

   $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
   $longdate = &longdate("$postdate");

   $topicdescription = qq(&nbsp;-=> $topicdescription) if $topicdescription;

        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                chomp $good;
                $topictitle=~ s/$bad/$good/isg;
                }
            }
	    if (($membercode eq "ad") || ($inmembmod eq "yes") || ($membercode eq 'smo')) {
		$admini = qq~<br><DIV ALIGN=Right><font color=$titlecolor>|<a href=jinghua.cgi?action=add&forum=$forumid&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=$postingsprog?action=locktop&forum=$forumid&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=$postingsprog?action=puttop&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=$postingsprog?action=lock&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=$postingsprog?action=unlock&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=$postingsprog?action=delete&forum=$forumid&topic=$topicid><font color=$titlecolor>ɾ</font></a>|<a href=$postingsprog?action=movetopic&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|</font>&nbsp;</DIV>~;
		};

   $output .= qq(
   <tr>
      <td bgcolor=$miscbackone valign=middle>
         <font face="$font" color=$fontcolormisc>
         <B><a href="$boardurl/$threadprog?forum=$forumid&topic=$topicid">$topictitle</a></B><br>
         $topicdescription$admini
      </td>
      <td bgcolor=$miscbackone valign=middle>
         <font face="$font" color=$fontcolormisc>
         ������̳�� <a href="$boardurl/$forumsprog?forum=$forumid">$forumname</a><BR>����ʱ�䣺 $longdate</font>
      </td>
         <td bgcolor=$miscbackone valign=middle align=center>
         <font face="$font" color=$fontcolormisc>
         $string_returned
         </font>
      </td>
   </tr>
   );

   undef $topicdescription;

   } # end foreach

   $output .= qq(
      <tr>
      <td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center>
         <font face="$font" color=$fontcolormisc>
         $pages
         </font>
      </td>
      <td bgcolor="$miscbacktwo" valign=middle colspan=1 align=center>
         <font face="$font" color=$fontcolormisc>
         <a href="$boardurl/$thisprog"><b>>> �� �� �� �� <<</b></a>
         </font>
      </td>
   </tr>
   </table></td></tr></table>);


   &output( -Title   => "$boardname - �������",
             -ToPrint => "$output",
             -Version => $versionnumber);


} # end routine







