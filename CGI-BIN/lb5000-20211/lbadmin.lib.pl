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
#            http://maildo.com/      ���һ����
#            
#############################################################

sub adminlogin {
    $inmembername =~ s/\_/ /g;
    print qq(
    <tr><td bgcolor="#333333" colspan=2><font face=$font color=#FFFFFF>
    <b>��ӭ���� LB5000 ��̳��������</b>
    </td></tr>
    <form action="$boardurl/$adminprog" method="post">
    <input type=hidden name="action" value="login">
    <tr>
    <td bgcolor=#EEEEEE valign=middle colspan=2 align=center><font face=$font color=#333333><b>�����������û����������½</b></font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle width=40% align=right><font face=$font color=#555555>�����������û���</font></td>
    <td bgcolor=#FFFFFF valign=middle><input type=text name="membername" value="$inmembername" maxlength=15></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle width=40% align=right><font face=$font color=#555555>��������������</font></td>
    <td bgcolor=#FFFFFF valign=middle><input type=password name="password" value="$inpassword" maxlength=20></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle colspan=2 align=center><input type=submit name="submit" value="�� ½"></form></td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2><font face=$font color=#555555>
    <blockquote><b>��ע��</b><p><b>ֻ����̳��̳�����ܵ�½��̳�������ġ�<br>δ������Ȩ�ĳ��Ե�½��Ϊ���ᱻ��¼�ڰ���</b><p>�ڽ�����̳��������ǰ����ȷ�������������� Cookie ѡ�<br> Cookie ֻ������ڵ�ǰ������������С�Ϊ�˰�ȫ���������ر����������Cookie ��ʧЧ�����Զ�ɾ����</blockquote>
    </td></tr>
    </table></td></tr></table>
    );
    
}
sub admintitle {
    print qq~
    <html>
    <head>
    <title>LB5000 - ��̳��������</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style>
A:visited{TEXT-DECORATION: none}
A:active{TEXT-DECORATION: none}
A:hover{TEXT-DECORATION: underline overline}
A:link{text-decoration: none;}
.t{LINE-HEIGHT: 1.4}
TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: ����; FONT-SIZE: 9pt} 
INPUT{BORDER-TOP-WIDTH: 1px; PADDING-RIGHT: 1px; PADDING-LEFT: 1px; BORDER-LEFT-WIDTH: 1px; FONT-SIZE: 9pt; BORDER-LEFT-COLOR: #cccccc; BORDER-BOTTOM-WIDTH: 1px; BORDER-BOTTOM-COLOR: #cccccc; PADDING-BOTTOM: 1px; BORDER-TOP-COLOR: #cccccc; PADDING-TOP: 1px; HEIGHT: 18px; BORDER-RIGHT-WIDTH: 1px; BORDER-RIGHT-COLOR: #cccccc}
textarea, select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: ����; font-size: 9pt; font-style: bold;}
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
    <b>����˵�</b>
    </td></tr>
    <tr>
    <td bgcolor="#FFFFFF"><font face=$font color=#333333>
    >> <a href="admincenter.cgi">����������ҳ(*)</a><br>
    >> <a href="admincenter.cgi?action=logout">�˳���������(*)</a><br>
    >> <a href="$boardurl/$forumsummaryprog">����������̳(*)</a>
    </td></tr>
    <tr>
    <td bgcolor="#EEEEEE"><font face=$font color=#333333><b>�û�����</b>
    </td></tr>
    <tr>
    <td bgcolor="#FFFFFF"><font face=$font color=#333333>
    >> <a href="$setmembersprog">�û�����/����(*)</a><BR>
    >> <a href="usermanager.cgi">�û�����/����(*)</a><BR>
    >> <a href="setmemberbak.cgi">�û��ⱸ��/��ԭ</a><BR>
    </td></tr>
    <tr>
    <td bgcolor="#EEEEEE"><font face=$font color=#333333><b>ע�����</b>
    </td></tr>
    <tr>
    <td bgcolor="#FFFFFF"><font face=$font color=#333333>
    >> <a href="noreg.cgi">���������û���(*)</a><BR>
    >> <a href="noregemail.cgi">�������� Email(*)</a><BR>
    >> <a href="noregip.cgi">��ֹ���� IP ע���û�(*)</a><BR>
    </td></tr>
    
    <tr>
    <td bgcolor="#EEEEEE"><font face=$font color=#333333><b>��̳����</b>
    </td></tr>
    <tr>
    <td bgcolor="#FFFFFF"><font face=$font color=#333333>
    >> <a href="$setforumsprog">��̳����</a><br>
    >> <a href="merge.cgi">�ϲ���̳</a><br>
    >> <a href="adbackup.cgi">��̳���ݵ�����/��ԭ</a><BR>
    >> <a href="$shareforumsprog">������̳����</a><BR>
    >> <a href="rebuildall.cgi">�ؽ�������̳</a><br>
    >> <a href="rebuildmain.cgi">���½�����̳������</a><br>
    </td></tr>

    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>���ù���</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="$setmembersprog?action=init">��ʼ������</a><br>
    >> <a href="$stylesprog">Ĭ�Ϸ������</a><br>
    >> <a href="$varsprog">������������</a><br>
    >> <a href="setmemdir.cgi">�û���ϢĿ¼����</a><br>
    >> <a href="setmpic.cgi">��̳ͼƬ����</a><br>
    >> <a href="setcity.cgi">������������</a><br>
    >> <a href="$membertitlesprog">�û��ȼ�����</a><br>
    >> <a href="setemotes.cgi">EMOTE ����</a><br>
    </td></tr>

    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>���ƹ���</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="setbadwords.cgi">�����������(*)</a><BR>
    >> <a href="setipbans.cgi">IP ��ֹ(*)</a><BR>
    >> <a href="setidbans.cgi">ID ��ֹ(*)</a><BR>
    </td></tr>

    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>���⹦��</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="massmsg.cgi">����Ϣ�㲥</a><BR>
    >> <a href="mailmembers.cgi">Email Ⱥ��</a><BR>
    >> <a href="setplugin.cgi">��̳����趨</a><br>      
    >> <a href="setskin.cgi">����������趨</a><br>      
    </td></tr>
    <tr>
    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>��̳�༭</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="setregrules.cgi">�޸�ע������</a><br>
    >> <a href="setregmsg.cgi">�޸Ķ���Ϣ��ӭ��Ϣ</a><br>
    >> <a href="settemplate.cgi">�༭��̳ģ��</a><br>
    </td></tr>
    
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>��������</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>
    >> <a href="baddellogs.cgi">��̳��ȫ��־</a><br>
    >> <a href="adminloginlogs.cgi">��������ȫ��־</a><br>
    >> <a href="userratinglog.cgi">�û�����������־</a><br>
    >> <a href="sizecount.cgi">ͳ����̳ռ�ÿռ�</a><br>
    >> <a href="vercheck.cgi">��̳�汾/����</a><br>
    </td></tr>
    ~;
    
    if (-e "${lbdir}data/leoskin.cgi"){
	require "${lbdir}data/leoskin.cgi";
	if ($skin1name ne ""){
	    print qq~    
    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>��̳���</b>
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
    >> <a href="admincenter.cgi">����������ҳ(*)</a><br>
    >> <a href="$boardurl/$forumsummaryprog">����������̳(*)</a><br>
    >> <a href="admincenter.cgi?action=logout">�˳���������(*)</a><br>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font face=$font color=#333333>&nbsp;
    </td></tr>
    
    <tr>
    <td bgcolor=#EEEEEE><font face=$font color=#333333><b>LB5000 ��Ϣ</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF align=left>
    <span class="large">�汾��</span><span class="body">$versionnumber</span><p>
    <font face=$font color="#333333">
    ���İ�Ȩ���У� <a href="http://www.cgier.com/" target=_blank>CGI �����֮��</a><br>
    ����֧����̳�� <a href="http://www.leobbs.com/">���ᳬ����̳</a>
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
