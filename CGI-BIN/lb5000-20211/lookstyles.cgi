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
$thisprog = "lookstyles.cgi";

    $query = new LBCGI;
&ipbanned; #��ɱһЩ ip

	@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }



$action      =  $PARAM{'action'};
$inforum     =  $PARAM{'forum'};
$inmembername        = $query -> param("membername");
$inpassword          = $query -> param("password");
$action              = &cleaninput("$action");
$inmembername        = &cleaninput("$inmembername");
$inpassword          = &cleaninput("$inpassword");
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

    if ($inmembername eq "") { $inmembername = "����"; }
    else {
    &getmember("$inmembername");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
        }   

&mischeader("������ɫ�б�");

print header(-charset=>gb2312);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
&styleform;                
##################################################################################
sub styleform {
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
&error("������ɫ&�Բ��𣬱���鲻����鿴��ɫ��") if ($look eq "off");
&title;
if ($privateforum ne "yes") {
    	&whosonline("$inmembername\t$forumname\tnone\t�鿴��̳$forumname����ɫ\t");
    }
    else {
	&whosonline("$inmembername\t$forumname(��)\tnone\t�鿴������̳$forumname����ɫ\t");
    }

$output .= qq~

         <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
             <tr>
               <td width=30% rowspan=2 valign=top>$forumgraphic
               </td>
               <td valign=top>
        <img src=$imagesurl/images/closedfold.gif width=15 height=11>��<a href=$forumsummaryprog>$boardname</a><br>
       <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/closedfold.gif width=15 height=11>��<a href=forums.cgi?forum=$inforum>$forumname</a><br>
          �� <img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>���鿴$forumname����ɫ
      </td></tr></table>
        <table width=97% align=center><br>
        
                
              
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳BODY��ǩ</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>����������̳���ı�����ɫ���߱���ͼƬ��</font></td>
                <td bgcolor=#FFFFFF>
                $lbbody</td>
                </tr>
                              
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳ҳ�ײ˵�</b>
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>ҳ�ױ�����ɫ (�˵����Ϸ�)</font></td>
                <td bgcolor=$titleback  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $titleback</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>ҳ��������ɫ (�˵����Ϸ�)</font></td>
                <td bgcolor=$titlefont  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $titlefont</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>ҳ�ױ߽���ɫ (�˵����Ϸ�)</font></td>
                <td bgcolor=$titleborder  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $titleborder</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵���������ɫ</font></td>
                <td bgcolor=$menufontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $menufontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵���������ɫ</font></td>
                <td bgcolor=$menubackground  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $menubackground</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>������ۺ���ɫ</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"�������"������ɫ</font></td>
                <td bgcolor=$lastpostfontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $lastpostfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"������"������ɫ</font></td>
                <td bgcolor=$fonthighlight  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $fonthighlight</td>
                </tr>
                
                                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>һ���û�����������ɫ</font></td>
                <td bgcolor=$posternamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $posternamecolor</td>
                </tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>һ���û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$memglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$memglow</td>
		</tr>
               
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>̳������������ɫ</font></td>
                <td bgcolor=$adminnamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $adminnamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>̳�������ϵĹ�����ɫ</font></td>
		<td bgcolor=$adminglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$adminglow</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ܰ�������������ɫ</font></td>
                <td bgcolor=$smonamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $smonamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>�ܰ��������ϵĹ�����ɫ</font></td>
		<td bgcolor=$smoglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$smoglow</td>
		</tr>                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��������������ɫ</font></td>
                <td bgcolor=$teamnamecolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $teamnamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>���������ϵĹ�����ɫ</font></td>
		<td bgcolor=$teamglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$teamglow</td>
		</tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>���˺ͽ����û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$banglow  width=12>��</td>
		<td bgcolor=#FFFFFF>
		$banglow</td>
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
                $fontcolormisc</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫһ</font></td>
                <td bgcolor=$miscbackone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $miscbackone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫ��</font></td>
                <td bgcolor=$miscbacktwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $miscbacktwo</td>
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
                $catback</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�����������ɫ</font></td>
                <td bgcolor=$catfontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $catfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>���б��߽���ɫ</font></td>
                <td bgcolor=$tablebordercolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $tablebordercolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���б����</font></td>
                <td bgcolor=#FFFFFF>
                $tablewidth</td>
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
                $titlecolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��̳/����ı�����������ɫ</font></td>
                <td bgcolor=$titlefontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $titlefontcolor</td>
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
                $forumcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������ɫ��</font></td>
                <td bgcolor=$forumcolortwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $forumcolortwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫ</font></td>
                <td bgcolor=$forumfontcolor  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $forumfontcolor</td>
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
                $postcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ���ɫ��</font></td>
                <td bgcolor=$postcolortwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $postcolortwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ�������ɫһ</font></td>
                <td bgcolor=$postfontcolorone  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $postfontcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ�������ɫ��</font></td>
                <td bgcolor=$postfontcolortwo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                $postfontcolortwo</td>
                </tr>
               
              
                ~;             

}






$output .= qq~</td></tr></table><br><br></body></html>~;
&output(
     -Title   => "�鿴$forumname����ɫ", 
     -ToPrint => $output, 
     -Version => $versionnumber 
    );
exit;

