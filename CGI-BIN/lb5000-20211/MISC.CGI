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
#            http://maildo.com/      ���һ����
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
$thisprog = "misc.cgi";
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip
	
$UIN                    = $query -> param('UIN');
$action                 = $query -> param('action');
$aimname                = $query -> param('aimname');
$aimname =~ s/ //g;
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;
if (!$inmembername) { $inmembername = "����"; }
if ($action eq "showsmilies") {
    $output = qq~
    <html><head><title>����ת��</title>
	<style>
		.t     {	LINE-HEIGHT: 1.4			}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
	</style>
    </head>
    <body topmargin=0 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1 border=0>
            <tr>
                <td bgcolor=$titlecolor align=center colspan=2>
                    <font color=$titlefontcolor><b>$boardname - ����ת��</b></font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo align=center>
                    <font color="$fontcolormisc">����</font>
                </td>
                    <td bgcolor=$miscbacktwo align=center>
                    <font color=$fontcolormisc>ת����</font>
                </td>
                </tr>
    ~;
    
        open (FILE, "$lbdir/data/lbemot.cgi");
	my @emoticondata = <FILE>;
	close (FILE);
	chomp @emoticondata;
        
    foreach $picture (@emoticondata) {
	$smileyname = $picture;
	$smileyname =~ s/\.gif//g;
	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone align=center>
	<font color=$fontcolormisc>:$smileyname:</font>
	</td>
	<td bgcolor=$miscbackone align=center>
	<img src=$imagesurl/emot/$picture>
	</td>
	</tr>
	~;
    }
    $output .= qq~
	</table>
	</td></tr>
	</table>
	</body>
	</html>
    ~;
}
elsif ($action eq "icq") {
    $output = qq~
    <html><head><title>$boardname �� ICQ Ѱ��</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}
		
	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}
	        
		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
	</style>
    </head>
    <body topmargin=10 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <form action="http://wwp.mirabilis.com/scripts/WWPMsg.dll" method="post">
        <input type="hidden" name="subject" value="���� - $boardname"><input type="hidden" name="to" value="$UIN">
        <table width=100% cellpadding=5 cellspacing=1 border=0>
            <tr>
                <td bgcolor=$titlecolor align=center colspan=2>
                    <font color=$titlefontcolor><b>$boardname - ICQ Ѱ��</b><br>����һ����Ϣ�� $UIN</font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo valign=top>
                    <font color=$fontcolormisc>��������������</font>
                </td>
                    <td bgcolor=$miscbacktwo>
                    <input type="text" name="from" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top>
                    <font color=$fontcolormisc>���������� Email</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <input type="text" name="fromemail" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top>
                    <font color=$fontcolormisc>Ҫ���͵���Ϣ</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <textarea name="body" rows="3" cols="30" wrap="Virtual"></textarea>
                </td>
                </tr>
                <tr>
                <td bgcolor=$miscbacktwo align=center colspan=2>
                <input type="submit" name="Send" value="������Ϣ"></form>
                </td>
                </tr>
            </table>
        </td></tr>
    </table>
    </body>
    </html>
    ~;
}
elsif ($action eq "lbcode") {
    $output = qq~
    <html><head><title>LB5000 ��ǩ</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}
		
	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}
	        
		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
	</style>
<script language="javaScript" type="text/javascript" SRC="$imagesurl/images/board.js"></SCRIPT>
    </head>
    <body topmargin=10 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1 border=0>
            <tr>
                <td bgcolor=$titlecolor align=center colspan=2>
                    <font color=$titlefontcolor><b>LB5000 ��ǩ</b>
                    <br>LB5000 ��ǩ���� HTML ��ǩ������ HTML ��ǩ��ȫ������Բ��������ֲ��еĸ�ʽ��ʹ������
                    </font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone><ul>
                    <font color=$fontcolormisc>
                    <font color=$fonthighlight>[quote]</font>�����ǩ��������Ϊ���������õģ��������ʲô�����������Ա�ĵط�������������ǩ��<font color=$fonthighlight>[/quote]</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><hr noshade color=$fonthighlight><blockquote>�����ǩ��������Ϊ���������õģ��������ʲô�����������Ա�ĵط�������������ǩ��</blockquote><hr noshade color=$fonthighlight></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone><UL>
                    <font color=$fontcolormisc>
                    <font color=$fonthighlight>[code]</font>
                    	<BR>unless ( eq "$authenticateme") {
			<BR>print "����Ĺ�������";
			<BR>&unlock;
			<BR>exit;
			<BR>}<BR>
			<font color=$fonthighlight>[/code]</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc>
			<BLOCKQUOTE>���룺<hr noshade color=$fonthighlight>
			unless ( eq "$authenticateme") { <BR>
			print "����Ĺ�������"; <BR>
			&unlock; <BR>
			exit; <BR>
			}<hr noshade color=$fonthighlight></FONT></BLOCKQUOTE>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[html]</font>&lt;font size=5&gt;HTML �� JS ����֧��&lt;/font&gt;<font color=$fonthighlight>[/html]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><SPAN><IMG src=$imagesurl/images/code.gif align=absBottom> HTML ����Ƭ������:<BR><TEXTAREA style="WIDTH: 94%; BACKGROUND-COLOR: #f7f7f7" name=textfield rows=4>&lt;font size=5&gt;HTML �� JS ����֧��&lt;/font&gt;<\/TEXTAREA><BR><INPUT onclick=runEx() type=button value=���д˴��� name=Button> [Ctrl+A ȫ��ѡ��   ��ʾ:������޸Ĳ��ִ��룬�ٰ�����]</SPAN><BR></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[url]</font>http://www.CGIer.com<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="http://www.CGIer.com">http://www.CGIer.com</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[url=http://www.CGIer.com]</font>CGI �����֮��<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="http://www.CGIer.com">CGI �����֮��</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[email=webmaster\@cgier.com]</font>д�Ÿ���<font color=$fonthighlight>[/email]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="mailto:webmaster\@cgier.com">д�Ÿ���</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[email]</font>webmaster\@cgier.com<font color=$fonthighlight>[/email]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="mailto:webmaster\@cgier.com">webmaster\@cgier.com</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[b]</font>���ּӴ���Ч��<font color=$fonthighlight>[/b]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><b>���ּӴ���Ч��</b></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[i]</font>���ּ���бЧ��<font color=$fonthighlight>[/i]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><i>���ּ���бЧ��</i></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[u]</font>���ּ��»���Ч��<font color=$fonthighlight>[/u]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><u>���ּ��»���Ч��</u></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[size=4]</font>�ı����ִ�С<font color=$fonthighlight>[/size]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font size=4>�ı����ִ�С</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[font=impact]</font>�ı�����<font color=$fonthighlight>[/font]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font face=impact>�ı�����</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[color=red]</font>�ı�������ɫ<font color=$fonthighlight>[/color]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=red>�ı�������ɫ</font>
                </td>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[s]</font>�����ϼ�ɾ����<font color=$fonthighlight>[/s]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><s>�����ϼ�ɾ����</s></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sup]</font>�ϱ�����<font color=$fonthighlight>[/sup]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><sup>�ϱ�����</sup></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sub]</font>�±�����<font color=$fonthighlight>[/sub]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><sub>�±�����</sub></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[FLIPH]</font>���ҵߵ�����<font color=$fonthighlight>[/FLIPH]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:flipH">���ҵߵ�����</table></FLIPH>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[FLIPV]</font>���µߵ�����<font color=$fonthighlight>[/FLIPV]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:flipV">���µߵ�����</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[INVERT]</font>��ƬЧ��<font color=$fonthighlight>[/INVERT]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:invert"><img src="$imagesurl/images/ad8831.gif" border=0></table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[XRAY]</font>�ع�Ч��<font color=$fonthighlight>[/XRAY]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:xray"><img src="$imagesurl/images/logo.gif" border=0></table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[shadow=���ֿ���,��ɫ,�߽��С]</font>��Ӱ����<font color=$fonthighlight>[/shadow]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:shadow\(color=#f000ff\, direction=1)">��Ӱ����</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[GLOW=���ֿ���,��ɫ,�߽��С]</font>��������<font color=$fonthighlight>[/GLOW]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:glow\(color=#00f0ff\, strength=1)">��������</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[BLUR=���ֿ���,����,Ũ��]</font>ģ������<font color=$fonthighlight>[/BLUR]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:blur\(Add=0, direction=6\, strength=2)">ģ������</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[list]</font>��ʼ�б�<br><font color=$fonthighlight>[*]</font>�б���Ŀ<br><font color=$fonthighlight>[/list]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><ul>��ʼ�б�<br><li>�б���Ŀ</ul></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[img]</font>http://www.17do.com/ib2000/images/mainlogo.gif<font color=$fonthighlight>[/img]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><img src="$imagesurl/images/mainlogo.gif" border=0></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[fly]</font>����������Ч<font color=$fonthighlight>[/fly]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><marquee width=90% behavior=alternate scrollamount=3>����������Ч<\/marquee></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[move]</font>����������Ч<font color=$fonthighlight>[/move]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><marquee width=90% scrollamount=3>����������Ч<\/marquee></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[swf]</font>http://www.micromedia.com/demo.swf<font color=$fonthighlight>[/swf]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�� FLASH �ļ�(�Զ����ƴ�С)</font>
                </td> 
                </tr> 
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[flash=����,�߶�]</font>http://www.micromedia.com/demo.swf<font color=$fonthighlight>[/flash]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�� FLASH �ļ�(�ֶ����ô�С)</font>
                </td> 
                </tr> 
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sound]</font>http://www.cgier.com/demo.wav<font color=$fonthighlight>[/sound]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�����������ļ�(*.mid,*.wav)</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[mms]</font>mms://www.microsoft.com/demo.asf<font color=$fonthighlight>[/mms]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�� WM ��ʽ������</font>
                </td> 
                </tr> 
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[rtsp]</font>rtsp://www.real.com/demo.ram<font color=$fonthighlight>[/rtsp]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�� Real ��ʽ������</font>
                </td> 
                </tr> 
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[ra]</font>http://www.cgier.com/demo.ra<font color=$fonthighlight>[/ra]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Real Player������Ƶ�ļ�(*.mp3,*.ra)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[rm]</font>http://www.cgier.com/demo.rm<font color=$fonthighlight>[/rm]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Real Player������Ƶ�ļ�(*.rm)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wmv]</font>http://www.cgier.com/demo.wmv<font color=$fonthighlight>[/wmv]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Windows Media Player������Ƶ�ļ�(*.wmv)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wma]</font>http://www.cgier.com/demo.wma<font color=$fonthighlight>[/wma]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Windows Media Player������Ƶ�ļ�(*.wma)</font>
                </td>
                </tr>
            </table>
        </td></tr>
    </table>
    </body>
    </html>
    ~;
}
elsif ($action eq "newmsg") {
    $output = qq~
    <html><head><title>���µĶ���Ϣ</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}
		
	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}
	        
		.t     {	LINE-HEIGHT: 1.4			}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
</style>
</head>
    
<body topmargin=8 leftmargin=13 bgcolor=#FFFFFF>
<br>
<table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center height=280>
  <tr> 
    <td> 
      <table cellpadding=6 cellspacing=1 border=0 width=100% height=279>
        <tr> 
          <td  bgcolor=$titlecolor colspan=2 height=27> 
            <div align=center>����Ϣ֪ͨ</div>
          </td>
        </tr>
        <tr> 
          <td colspan=2 bgcolor=$forumcolorone>
            <div align=center><br>
              
              <center>
                <font color=$titlefontcolor><a href=$messangerprog><img src=$imagesurl/images/newmail.gif border=0></a>���µĶ���Ϣ<br>
                <br>
                <a href=$messangerprog>���˲鿴</a><br>
                </font>
              </center>
              <br></div>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
    </html>
~;
}
print header(-charset=>gb2312);
print $output;
exit;