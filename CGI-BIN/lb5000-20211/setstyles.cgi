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
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setstyles.cgi";

$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam =~ s/'//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
        	$_ =~ s/[\n\r]//isg;
        	$theparam =~ s/[\n\r]//isg;
            $printme .= "\$" . "$_ = \'$theparam\'\;\n" if ($_ ne "");
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

print header(-charset=>gb2312);
&admintitle;

&getmember("$inmembername");

if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

    if ($action eq "delstyle") {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>��ȫɾ���˷���̳�������Զ����񣬲��ɻָ�<p>
        <p>
        >> <a href="$thisprog?action=delstyleok&forum=$forum">��ʼɾ��</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
    }
    elsif ($action eq "delstyleok") {
        $filetomake = "$lbdir" . "data/style$forum.cgi";
    	unlink $filetomake;
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳�������� / ����̳���ɾ��</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>������Ϣ�Ѿ�����</b><br>�˷���̳�ķ���Ѿ���ȫɾ����
                    </td></tr></table></td></tr></table>
                    ~;

    }
    elsif ($action eq "process") {


        $printme .= "1\;\n";

        $filetomake = "$lbdir" . "data/styles.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE colspan=2>
                <font color=#333333><center><b>���µ���Ϣȫ���ɹ�����</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/1\;//g;
                print $printme;

                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }

                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳�������� / �������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>������Ϣû�б���</b><br>�ļ�����Ŀ¼����д������������Ϊ 777 ��
                    </td></tr></table></td></tr></table>
                    ~;
                    }

            }
            else {
                if ($action ne ""){
                $stylefile = "$lbdir" . "data/skin/$action.cgi";
                if (-e $stylefile) {
         	require $stylefile;
                }
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
        $myskin.=qq~<option value="$thd[$i]">��� [ $thd[$i] ]~;
        }
        $myskin =~ s/value=\"$action\"/value=\"$action\" selected/;
                $inmembername =~ s/\_/ /g;

                print qq~
                <tr><td bgcolor=#333333" colspan=3><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#333333><b>�趨���</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>ϵͳ�Դ��ķ��</b><br>��ѡ�����Ҫ��ʽȷ���ύ����Ч</font></td>
                <td bgcolor=#FFFFFF>
                <form action="$thisprog" method="post">
                <select name="action">
                <option value="">Ĭ�Ϸ��$myskin
                </select>
                <input type=submit value="�� ��">
                </form>
                </td></tr>

                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳BODY��ǩ</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����������̳���ı�����ɫ���߱���ͼƬ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>Ĭ�ϣ�bgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
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
		<font face=verdana color=#333333>һ���û������ϵĹ�����ɫ</font></td>
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
		<font face=verdana color=#333333>̳�������ϵĹ�����ɫ</font></td>
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
		<font face=verdana color=#333333>�ܰ��������ϵĹ�����ɫ</font></td>
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
		<font face=verdana color=#333333>���������ϵĹ�����ɫ</font></td>
		<td bgcolor=$teamglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="teamglow" value="$teamglow" size=7 maxlength=7>��Ĭ�ϣ�#9898BA</td>
		</tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>���˺ͽ����û������ϵĹ�����ɫ</font></td>
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
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ͶƱ���������ٺ��������ͶƱ����</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hotpollmark" value="$hotpollmark" size=3 maxlength=3>��һ��Ϊ 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>LB5000 ��ǩ����</center></b>(̳���Ͱ������ܴ���)<br>
                </td></tr>
                ~;

                $tempoutput = "<select name=\"arrawpostpic\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostpic\"/value=\"$arrawpostpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�������ͼ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostflash\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostflash\"/value=\"$arrawpostflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ����� Flash��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
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

                $tempoutput = "<select name=\"arrawpostsound\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostsound\"/value=\"$arrawpostsound\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�����������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostfontsize\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostfontsize\"/value=\"$arrawpostfontsize\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�����ı����ִ�С��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawsignpic\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignpic\"/value=\"$arrawsignpic\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�������ͼ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"arrawsignflash\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignflash\"/value=\"$arrawsignflash\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ����� Flash��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawsignsound\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignsound\"/value=\"$arrawsignsound\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�����������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawsignfontsize\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
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
                <font color=#990000><b><center>��̳ͼ������</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Զ���ͷ�������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxposticonwidth" value="$maxposticonwidth" size=3 maxlength=3>���벻Ҫ���� 110</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Զ���ͷ�����߶�</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxposticonheight" value="$maxposticonheight" size=3 maxlength=3>���벻Ҫ���� 130</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ͷ���Ĭ��ͼ����(Ϊ������)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultwidth" value="$defaultwidth" size=3 maxlength=3>��Ĭ�� 32 ���������Ϊ�գ�������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ͷ���Ĭ��ͼ��߶�(Ϊ������)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultheight" value="$defaultheight" size=3 maxlength=3>��Ĭ�� 32 ���������Ϊ�գ�������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����ͼ��Ĭ�Ͽ��(Ϊ������)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsmilewidth" value="$defaultsmilewidth" size=3 maxlength=3>��Ĭ�� 13 ���������Ϊ�գ�������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����ͼ��Ĭ�ϸ߶�(Ϊ������)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsmileheight" value="$defaultsmileheight" size=3 maxlength=3>��Ĭ�� 13 ���������Ϊ�գ�������</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��̳������ʽ����</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���Ӷ��������</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"paraspace\">\n<option value=\"130\">Ĭ�ϼ��<option value=\"100\">�����о�<option value=\"150\">1.5���о�<option value=\"200\">˫���о�";
                $tempoutput =~ s/value=\"$paraspace\"/value=\"$paraspace\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����ּ�����</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"wordspace\">\n<option value=\"0\">Ĭ�ϼ��<option value=\"-1\">����<option value=\"+2\">����<option value=\"+4\">�ӿ�";
                $wordspace =~ s/\+/\\+/;
                $tempoutput =~ s/value=\"$wordspace\"/value=\"$wordspace\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

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
                <input type=text name="maxsavepost" value="$maxsavepost" size=3 maxlength=2>����Ҫ���� 50����������Ӱ���ٶ�</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����������</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsignline" value="$maxsignline" size=5 maxlength=2>��һ�� 5 ��(������������ʹ��)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ��������ַ���</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsignlegth" value="$maxsignlegth" size=5 maxlength=4>��һ�� 200 ����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���˼�����������</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxinsline" value="$maxinsline" size=5 maxlength=2>��һ��  5 ��(������������ʹ��)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���˼�������ַ���</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxinslegth" value="$maxinslegth" size=5 maxlength=4>��һ�� 100 ����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ͷ���б�һ�м���ͼ��</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="interval" value="$interval" size=2 maxlength=2>��һ�� 10 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ͷ���б�һҳ����</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="linesperpage" value="$linesperpage" size=2 maxlength=2>��һ�� 10 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��̳ͶƱ����������������Ŀ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpollitem" value="$maxpollitem" size=2 maxlength=2>�������� 5 - 50 ֮��</td>
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
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ĭ���û�����ʱ���Ƕ��ٷ��ӣ�<BR>����û��������ʱ�仹û�ж�����Ĭ���û��Ѿ��뿪����̳��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="membergone" value="$membergone" size=5 maxlength=5>��һ��Ϊ 5 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��¼������̳����������⣿<br>��������ҳ����ʾ��� N �����⡣</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpostreport" value="$maxpostreport" size=3 maxlength=3>��һ�� 10 -- 20 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>һ��ɾ���������������پͱ���¼��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="logdelmax" value="$logdelmax" size=3 maxlength=3>��һ�� 5 - 10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÿ���������ɾ�����Ӵ�����(��̳����Ч)<br>�����������,������Ϊ 999.</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxdeloneday" value="$maxdeloneday" size=3 maxlength=3>��һ�� 5 - 10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����������·ͳ�Ƹ�����</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newrefers" value="$newrefers" size=3 maxlength=3>��һ�� 20 - 40 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����Сʱ�ڵ���������� new ��־��<BR>(�������Ҫ����������Ϊ 0)</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newmarktime" value="$newmarktime" size=3 maxlength=3>��һ�� 12 - 24 Сʱ</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"noself\">\n<option value=\"on\">��¼\n<option value=\"off\">����¼\n</select>\n";
                $tempoutput =~ s/value=\"$noself\"/value=\"$noself\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��¼��·���Լ���ҳ�ķ����ߣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ˢ����̳��ʱ����(��)<BR>������Ч��ֹ����ˢ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="banfreshtime" value="$banfreshtime" size=3 maxlength=3>��������裬������ 0</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"look\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$look\"/value=\"$look\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ񿪷���̳��ɫ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"showskin\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$showskin\"/value=\"$showskin\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ������û��Զ��������̳ʱ�ķ��</font></td>
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

                $tempoutput = "<select name=\"newmsgpop\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$newmsgpop\"/value=\"$newmsgpop\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���µĶ���Ϣ�Ƿ񵯳�������ʾ��</font></td>
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

                $tempoutput = "<select name=\"statsopen\"><option value=\"0\">�κ��˿��Բ鿴<option value=\"1\">ע���û����Բ鿴<option value=\"2\">̳���Ͱ������Բ鿴</select>\n";
                $tempoutput =~ s/value=\"$statsopen\"/value=\"$statsopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��̳ͳ�Ʋ쿴���ŷ�ʽ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"infosopen\"><option value=\"0\">�κ��˿��Բ鿴<option value=\"1\">ע���û����Բ鿴<option value=\"2\">̳���Ͱ������Բ鿴</select>\n";
                $tempoutput =~ s/value=\"$infosopen\"/value=\"$infosopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�б��������ϲ쿴���ŷ�ʽ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"searchopen\"><option value=\"0\">�κ��˿��Խ���<option value=\"1\">ע���û����Խ���</select>\n";
                $tempoutput =~ s/value=\"$searchopen\"/value=\"$searchopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��̳����������˭���У�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"regaccess\"><option value=\"off\">���������κ��˷���<option value=\"on\">�ǣ������½����ܷ���</select>\n";
                $tempoutput =~ s/value=\"$regaccess\"/value=\"$regaccess\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left  colspan=2>
                <font face=���� color=#333333>��ֻ̳��ע���û����Է��ʣ�</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pvtip\">\n<option value=\"on\">��ʾ IP �ͼ���\n<option value=\"off\">���� IP �ͼ���\n</select>\n";
                $tempoutput =~ s/value=\"$pvtip\"/value=\"$pvtip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><B>�Ƿ��� IP �ͼ�����</B><BR>��ʹѡ�������ʾ IP������ͨ�û�����<BR>ֻ�ܿ��� IP ��ǰ��λ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput���˹��ܶ�̳����Ч</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"smocanseeip\">\n<option value=\"yes\">��Ч\n<option value=\"no\">��Ч\n</select>\n";
                $tempoutput =~ s/value=\"$smocanseeip\"/value=\"$smocanseeip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>���� IP �ͼ������ܰ����Ƿ���Ч��</B><BR>��ѡ����Ч�����ܰ����ɲ鿴���е� IP<BR>���������� IP ���ܵ�����</font></td>
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
                <input type=text name="maxupload" value="$maxupload" size=5 maxlength=5>����Ҫ�� KB�����鲻Ҫ���� 500</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowavaupload\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$arrowavaupload\"/value=\"$arrowavaupload\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ������ϴ��Զ���ͷ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowuserdel\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$arrowuserdel\"/value=\"$arrowuserdel\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ�����ע���û��Լ�������ɾ���Լ������ӣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
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

                $tempoutput = "<select name=\"sendwelcomemessage\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$sendwelcomemessage\"/value=\"$sendwelcomemessage" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ񷢻�ӭ��Ϣ����ע���û���</font></td>
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

                $tempoutput = "<select name=\"sortposticonshow\">\n<option value=\"yes\">���ظ��˵������\n<option value=\"no\">�����˵������\n</select>\n";
                $tempoutput =~ s/value=\"$sortposticonshow\"/value=\"$sortposticonshow" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��̳���������������ʾΪ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"refreshforum\">\n<option value=\"off\">��Ҫ�Զ�ˢ��\n<option value=\"on\">Ҫ�Զ�ˢ��\n</select>\n";
                $tempoutput =~ s/value=\"$refreshforum\"/value=\"$refreshforum" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳�Ƿ��Զ�ˢ��(�����������ü��ʱ��)��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Զ�ˢ����̳��ʱ����(��)<BR>����������һ��ʹ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="autofreshtime" value="$autofreshtime" size= 5 maxlength=5>��һ������ 5 ���ӣ����� 300 �롣</td>
                </tr>
		~;

                $tempoutput = "<select name=\"movetopicname\">\n<option value=\"on\">��ʾ\n<option value=\"off\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$movetopicname\"/value=\"$movetopicname" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ת�ƹ��������Ƿ���ʾת��������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"editusertitleself\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$editusertitleself\"/value=\"$editusertitleself" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ������û������޸ĸ���ͷ�Σ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"editjhmpself\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$editjhmpself\"/value=\"$editjhmpself" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ������û������޸Ľ������ɣ�</font></td>
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

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳����ͼƬ<br>��ͼ������ images Ŀ¼�£�ֻ�������ƣ������Լ� URL ��ַ�����·��</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="boardlogo" value="$boardlogo"><BR></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <input type=submit value="�� ��"></td></form></tr></table></td></tr></table>
                ~;
                }
                }
                else {
                    &adminlogin;
                    }

print qq~</td></tr></table></body></html>~;
exit;
