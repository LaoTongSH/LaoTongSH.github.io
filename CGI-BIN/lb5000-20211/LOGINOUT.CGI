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
$|++;                        # Unbuffer the output
$thisprog = "loginout.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip
$boardurltemp =$boardurl;
$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
$cookiepath = $boardurltemp;
$cookiepath =~ s/\/$//;

$inforum        = $query -> param('forum');
$inforum        = &stripMETA("$inforum");
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));

for ('inmembername','inpassword','action','threadages','CookieDate','myinfo','mess','onlineview','advpost','viewMode','nodispavatar','nodispsign','nodispphoto','freshtime','hidden','selectstyle','tanchumsg') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
}
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if ($inmembername eq "") {
    $inmembername = "����";
}
&getmember("$inmembername");
$memberfilename = $inmembername;
$memberfilename =~ s/ /\_/g;
$memberfilename =~ tr/A-Z/a-z/;
$filetotrash = "$lbdir". "$msgdir/main/$memberfilename" . "_mian.cgi";
&title;
$output .= qq~
  <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
    <tr>
        <td width=30% rowspan=2 valign=top><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td valign=top align=left><font face="$font" color=$fontcolormisc>
        <font face="$font" color=$fontcolormisc>
	��<img src="$imagesurl/images/closedfold.gif" border=0>��<a href="$forumsummaryprog">$boardname</a><br>
        ��<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>����½/�˳�
        </td>
    </tr>
  </table>
  <p>
  <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
      <td>
      <table cellpadding=6 cellspacing=1 border=0 width=100%>
~;
if ($action eq "login") {

    if (($userregistered ne "no") && ($inpassword eq $password)) {

     &whosonline("$inmembername\t��̳��½\tnone\t��½��̳\t");

     my $filetoopen2 = "$lbdir" . "data/onlinedata.cgi";
     my $filetoopens = &lockfilename($filetoopen2);
     if (!(-e "$filetoopens.lck")) {
	my $ipaddresstemp1  = $ENV{'REMOTE_ADDR'};
	$ipaddresstemp = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ipaddresstemp = $ipaddresstemp1 if (($ipaddresstemp eq "")||($ipaddresstemp eq "unknown"));
	my $ipaddresstemp2 = $ENV{'HTTP_CLIENT_IP'};
	$ipaddresstemp = $ipaddresstemp2 if (($ipaddresstemp2 ne "")&&($ipaddresstemp2 ne "unknown"));
        &winlock($filetoopen2);
        open(FILE,">$filetoopen2");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $line (@onlinedata) {
                chomp $line;
                (my $savedusername, my $no) = split(/\t/, $line);
		print FILE "$line\n" if ($savedusername ne "����($ipaddresstemp)");
        }
        close(FILE);
        &winunlock($filetoopen2);
     }

	if ($inforum eq "") {
            $refrashurl = $forumsummaryprog;
	}
    	else {
	    $refrashurl = $forumsprog."?forum=$inforum";
	}
	$output .= qq~
	<tr>
	<td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>��л���½ $inmembername</b></font></td></tr>
	<tr>
	<td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
	���������
	<ul>
	<li><a href="$refrashurl">������̳</a>
	<meta http-equiv="refresh" content="3; url=$refrashurl">
	</ul>
	</tr></td>
	</table></td></tr></table>~;

       if ($myinfo==1) {
           if (length($mess) == 0) {$mess = "�Բ��������ں�æ�������Ժ�����ϵ�ҡ�";}
           else { $mess =~ s/[\a\f\n\e\0\r\t\`\~\!\@\$\%\^\&\*\=\+\\\'\:\"\/\<\>\?]//isg; }
       	   if (open(FILE,">$filetotrash")) {
       	     print FILE "$mess";
       	     close(FILE);
       	   }
       }
       else {
           unlink "$filetotrash" if (-e "$filetotrash");
       }

	$namecookie = cookie(-name    =>"amembernamecookie",
                         -value   =>   "$inmembername",
			 -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
    	$passcookie = cookie(-name    =>"apasswordcookie",
                         -value   =>   "$inpassword",
			 -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
       $onlineviewcookie = cookie(-name    =>   "onlineview",
                         -value   =>   "$onlineview",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
	   $advpostcookie = cookie(-name    =>   "advpost",
                        -values   =>   "$advpost",
                        -path    =>   "$cookiepath/",
                        -expires =>   "$CookieDate");
       $threadcookie = cookie(-name    =>   "threadages",
                        -value   =>   "$threadages",
                        -path    =>   "$cookiepath/",
                        -expires =>   "$CookieDate");
       $viewcookie = cookie(-name    =>   "viewMode",
                         -value   =>   "$viewMode",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
       $nodisp     = cookie(-name    =>   "nodisp",
                         -value   =>   "$nodispavatar|$nodispsign|$nodispphoto",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
       $freshtimecookie = cookie(-name    =>   "freshtime",
		    	 -value   =>   "$freshtime",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
       $selectstylecookie = cookie(-name    =>   "selectstyle",
		    	 -value   =>   "$selectstyle",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");
	$tanchumsgcookie = cookie(-name    =>   "tanchumsg",
		    	 -value   =>   "$tanchumsg",
                         -path    =>   "$cookiepath/",
                         -expires =>   "$CookieDate");

    	print header(-cookie=>[$onlineviewcookie,$advpostcookie,$threadcookie,$viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie, $namecookie,$passcookie], -charset=>gb2312);
    }
    else {
	print header(-charset=>gb2312);
	$output .= qq~
	<tr><td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>��½����</b></font></td></tr>
	<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
	��½����Ŀ���ԭ��
	<ul>
	<li>�������<li>�û�������<li>������<a href=$registerprog>ע��</a>�û�
	</ul>
	</tr></td>
	</table></td></tr></table>
	~;
    }
}
elsif ($action eq "logout") {
   $filetoopen = "$lbdir" . "data/onlinedata.cgi";
   my $filetoopens = &lockfilename($filetoopen);
   if (!(-e "$filetoopens.lck")) {
      &winlock($filetoopen);
      open(FILE,"$filetoopen");
      flock(FILE, 1) if ($OS_USED eq "Unix");
      @onlinedata = <FILE>;
      close(FILE);
      $onlinedata = @onlinedata;
      if ($onlinedata > 0) {
        open(ONLINEFILE,">$filetoopen");
        flock(ONLINEFILE, 2) if ($OS_USED eq "Unix");
        foreach $line (@onlinedata) {
            chomp $line;
            ($savedusername, my $no) = split(/\t/, $line);
			if (lc($savedusername) ne lc($inmembername)) {
		    	print ONLINEFILE "$line\n";
			}
			else {
        	    &uplogintime("$savedusername","")
			}
        }
        close(ONLINEFILE);
      }
      else { unlink("$filetoopen") if ($onlinedata eq 0); }
      &winunlock($filetoopen);
   }
   unlink "$filetotrash" if (-e "$filetotrash");
	$output .= qq~
	<tr><td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc><b>�������Ѿ��˳���̳</b></font></td></tr>
	<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
	����ѡ�
	<ul>
	<li><a href="$forumsummaryprog">������̳</a>
	<li><a href=javascript:close();>�ر����������</a>
	</ul>
	</tr>
	</td>
	</table></td></tr></table>
	~;

        $namecookie = cookie(-name    =>   "amembernamecookie",
			     -path    =>   "$cookiepath/",
                             -value   =>   "");
	$passcookie = cookie(-name    =>   "apasswordcookie",
                             -value   =>   "",
			     -path    =>   "$cookiepath/",
                             -expires =>   "");
        $trashcookie = cookie(-name    =>   "templastvisit",
			      -path    =>   "$cookiepath/",
                              -value   =>   "");

        $threadages = cookie(-name    =>   "threadages",
			      -path    =>   "$cookiepath/",
                              -value   =>   "");
        $onlineviewcookie= cookie(-name    =>   "onlineview",
                      	      -value   =>   "",
                              -path    =>   "$cookiepath/");
	    $advpostcookie= cookie(-name    =>   "advpost",
                           -values   =>   "",
                             -path    =>   "$cookiepath/");
        $viewcookie = cookie(-name    =>   "viewMode",
                       -value   =>   "",
                       -path    =>   "$cookiepath/");
        $nodisp = cookie(-name    =>   "nodisp",
                       -value   =>   "",
                       -path    =>   "$cookiepath/");
       $freshtimecookie = cookie(-name    =>   "freshtime",
		    	 -value   =>   "",
                         -path    =>   "$cookiepath/");
       $selectstylecookie = cookie(-name    =>   "$selectstyle",
		    	 -value   =>   "",
                         -path    =>   "$cookiepath/");
       $tanchumsgcookie = cookie(-name    =>   "$tanchumsg",
		    	 -value   =>   "",
                         -path    =>   "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie, $trashcookie,$threadages,$onlineviewcookie,$advpostcookie,$viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie], -charset=>gb2312);
}
else {
if ($defaulttopicshow ne "") { $inthreadages = $defaulttopicshow; }
if ($query->cookie("threadages")) { $inthreadages = $query->cookie("threadages"); }
if ($query->cookie("selectstyle")) { $inselectstyle = $query->cookie("selectstyle"); }
if ($query->cookie("viewMode") ne ""){
$checked ="checked";
$checked1 ="";
}else{
$checked1 ="checked" ;
$checked ="" ;
}
if ($query->cookie("tanchumsg") eq ""){
$tcchecked ="checked";
$tcchecked1 ="";
}else{
$tcchecked1 ="checked" ;
$tcchecked ="" ;
}
if (($query->cookie("onlineview") == 1)||($query->cookie("onlineview") eq "")){
$online ="checked";
$online1 ="";
}else{
$online1 ="checked";
$online ="";
}
if (($query->cookie("advpost") == 1)||($query->cookie("advpost") eq "")){
$aadvpost ="checked";
$aadvpost1 ="";
}else{
$aadvpost1 ="checked";
$aadvpost ="";
}

$nodisp = $query->cookie("nodisp");
($nodispavatar, $nodispsign, $nodispphoto)  = split(/\|/,$nodisp);

if ($nodispavatar eq "yes"){
$checked2 ="checked" ;
}
if ($nodispsign eq "yes"){
$checked3 ="checked" ;
}
if ($nodispphoto eq "yes"){
$checked4 ="checked" ;
}

    print header(-charset=>gb2312);
    $inmembername =~ s/\_/ /g;

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t��̳��½\tnone\t��½��̳\t");
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
        $myskin.=qq~<option value="$thd[$i]">[ $thd[$i] ]</option>~;
        }

    $output .= qq~
    <tr>
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="login">
    <input type=hidden name="forum" value="$inforum">
    <font face="$font" color=$fontcolormisc><b>�����������û����������½</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>�����������û���</font></td>
    <td bgcolor=$miscbackone valign=middle><input type=text name="inmembername" value="$inmembername"> &nbsp; <a href="$registerprog"><font face="$font" color=$fontcolormisc>��û��ע�᣿</font></a></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>��������������</font></td>
    <td bgcolor=$miscbackone valign=middle><input type=password name="inpassword" value="$inpassword"> &nbsp; <font face="$font" color=$fontcolormisc><a href="$profileprog?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
    <tr>
    <td bgcolor=$miscbacktwo colspan=2 valign=middle><font face="$font" color=$fontcolormisc><b>��̳��½ѡ��</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>��̳����</b> ��ѡ����ĵ�½��ʾ��ʽ�������ʵ����������˽��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="hidden" value="0" checked id=1> <label for=1>������½����ʾ�����߻�Ա�б���</label><br>
                <input type="radio" name="hidden" value="1" id=2> <label for=2>������½����Ҫ������ʾ�������б���</label><br>
                </font>
                </td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>Cookie ѡ��</b><BR> ��ѡ����� Cookie ����ʱ�䣬�´η��ʿ��Է������롣</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="CookieDate" value="-1d" checked id=3> <label for=3>�����棬�ر��������ʧЧ</label><br>
                <input type="radio" name="CookieDate" value="+1d" id=4> <label for=4>����һ��</label><br>
                <input type="radio" name="CookieDate" value="+30d" id=5> <label for=5>����һ��</label><br>
                <input type="radio" name="CookieDate" value="+20y" id=6> <label for=6>���ñ���</label><br>
                </font>
                </td></tr>
<tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>����Ϣѡ��</b><br> ��ѡ�����½���Ƿ���ն���Ϣ�����ⱻ���š�<BR>�����ģʽ�򿪺�ֻ���˳����ص�½���ܽ��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="myinfo" value="0" checked onclick=h_display(mess),mess.value="" id=7> <label for=7>�������ն���Ϣ</label><br>
                <input type="radio" name="myinfo" value="1" onclick=n_display(mess),mess.value="�Բ��������ں�æ�������Ժ�����ϵ�ҡ�" id=8> <label for=8>�����ģʽ</label>��<input type="text" name="mess" size=40 maxlength=40 id=mess style="DISPLAY: none">
                </font>
                </td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>�����б�</b> ��ѡ���������������ʾ��ʽ�����Լӿ���̳��ʾ��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="onlineview" value="1" $online id=9> <label for=9>��ʾ��ϸ����</label><br>
                <input type="radio" name="onlineview" value="0" $online1 id=10> <label for=10>�ر���ϸ����</label><br>
                </font>
                </td></tr>
<tr>
   <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>Ĭ�Ϸ�����ʽ</b> ��ѡ���㷢��ʱ��ʾ�ķ�ʽ��</font></td>
   <td bgcolor=$miscbackone valign=middle><font class='misc'>
               <input type="radio" name="advpost" values="1" $aadvpost id=18> <label for=18>�߼�ģʽ</label><br>
               <input type="radio" name="advpost" values="0" $aadvpost1 id=19> <label for=19>��ģʽ</label><br>
               </font>
               </td></tr>      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>�鿴����</b> ��ѡ����ϲ�ò鿴����Ķ��٣����Լӿ���̳��ʾ��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
        <select name="threadages">
        <option value="all">�鿴���е�����</option>
        <option value="1">�鿴һ���ڵ�����</option>
        <option value="2">�鿴�����ڵ�����</option>
        <option value="7">�鿴һ�����ڵ�����</option>
        <option value="15">�鿴������ڵ�����</option>
        <option value="30">�鿴һ�����ڵ�����</option>
        <option value="61">�鿴�������ڵ�����</option>
        <option value="182">�鿴�����ڵ�����</option>
        <option value="365">�鿴һ���ڵ�����</option>
        </select>
                </font>
                </td></tr>
      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>�鿴����</b> ��ѡ����ϲ�õĲ鿴���ӷ�ʽ�����Է����Ķ���</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="viewMode" value="" $checked1 id=11> <label for=11>��ԭ���������</label><br>
                <input type="radio" name="viewMode" value="_blank" $checked id=12> <label for=12>���´��������</label><br>
                </font>
                </td></tr>

      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>�鿴��������</b> ��ѡ��鿴��������ʱ���Ƿ���ʾ�û�ͷ��ǩ������ͼ��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="checkbox" name="nodispavatar" value="yes" $checked2 id=13> <label for=13>����ʾ�û�ͷ��</label><br>
                <input type="checkbox" name="nodispsign"   value="yes" $checked3 id=14> <label for=14>����ʾ�û�ǩ��</label><br>
                <input type="checkbox" name="nodispphoto"  value="yes" $checked4 id=15> <label for=15>����ʾ�û���ͼ</label><br>
                </font>
                </td></tr>
		   <tr>
~;
if ($showskin ne "off") {$output.=qq~
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>����趨</b> ��ѡ�������̳���</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
		  <select name="selectstyle">
        <option value="">Ĭ�Ϸ��</option>
	$myskin
        </select>
        </font>
        </td></tr>
~;}
$output.=qq~
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>�ж���Ϣ�Ƿ񵯳���</b> <BR>���������Ա�����˲��������ѡ����Ч��</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" class=1 name="tanchumsg" value="" $tcchecked id=16> <label for=16>��������Ϣ����</label><br>
                <input type="radio" class=1 name="tanchumsg" value="no" $tcchecked1 id=17> <label for=17>����������Ϣ����</label><br>
                </font></td></tr>

<tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>ҳ���Զ�ˢ��ʱ��</b> <BR>���������̳��ҳ�Զ�ˢ�µ�ʱ�䣨���������շ���̳��Ĭ�����ý���ˢ�»��߲�ˢ�£�</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
ÿ�� <input type=text name="freshtime" value="$freshtime" maxlength="2" size="2"> �����Զ�ˢ��һ��
<tr>
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="�� ½"></td></form></tr></table></td></tr></table>
    ~;
}

$output =~ s/option value=\"$inthreadages\"/option value=\"$inthreadages\" selected/;
$inselectstyle =~ s/\(/\\(/isg;
$inselectstyle =~ s/\)/\\)/isg;
$output =~ s/option value=\"$inselectstyle\"/option value=\"$inselectstyle\" selected/;
&output(
-Title   => "$boardname - ��½/�˳�",
-ToPrint => $output,
-Version => $versionnumber
);