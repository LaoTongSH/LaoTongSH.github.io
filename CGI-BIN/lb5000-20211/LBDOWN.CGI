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
require "lb.lib.pl";          # Require lbboard ()

$|++;      
$query = new LBCGI;
$requestver = $query->param('ver');
$requesturl = $query->param('url');

        $geturl="http://www.leoboard.com/cgi-bin/lbver.cgi?ver=$requestver&url=$requesturl";
        $out=&lbagent($geturl);
        
        (my $lastver, my $finish,my $downtime,my $nowver,my $hasfunc,my $gb,my $big5,my $download) = split(/��/,$out);
        (my $tmp,$lastver) = split(/\|/,$lastver);     
          print header(-charset=>gb2312);
          print qq~
          <html>
<head>
<title>Welcome To Leoboard!</title>
<STYLE type=text/css>
BODY {
	FONT-SIZE: 9pt; FONT-FAMILY: "MS Shell Dlg"
}
P {
	FONT-SIZE: 9pt; FONT-FAMILY: "MS Shell Dlg"
}
SELECT {
	FONT-SIZE: 9pt; FONT-FAMILY: "MS Shell Dlg"
}
TD {
	FONT-SIZE: 12px; FONT-FAMILY: "MS Shell Dlg"
}
INPUT {
	FONT-SIZE: 9pt; FONT-FAMILY: ����; verdana: 
}
TEXTAREA {
	FONT-SIZE: 9pt; FONT-FAMILY: ����; verdana: 
}
TEXTAREA {
	FONT-SIZE: 9pt; FONT-FAMILY: ����; verdana: 
}
.input1 {
	BORDER-RIGHT: #085d3f 1px solid; BORDER-TOP: #085d3f 1px solid; BORDER-LEFT: #085d3f 1px solid; BORDER-BOTTOM: #085d3f 1px solid; BACKGROUND-COLOR: white
}
A {
	FONT-SIZE: 9pt; TEXT-TRANSFORM: none; COLOR: #000000; TEXT-DECORATION: none
}
A.lefta {
	FONT-SIZE: 9pt; TEXT-TRANSFORM: none; COLOR: #c0c0c0; TEXT-DECORATION: none
}
A.flink {
	FONT-SIZE: 9pt; TEXT-TRANSFORM: none; COLOR: #000000; TEXT-DECORATION: none
}
A.lefta:hover {
	COLOR: #c0c0c0; TEXT-DECORATION: none
}
A:hover {
	COLOR: red; TEXT-DECORATION: none
}
A:visited {
	TEXT-DECORATION: none
}
.smallsize {
	FONT-SIZE: 9px; COLOR: #d9d9d9; FONT-FAMILY: "verdana"
}
LI {
	FONT-SIZE: 9pt; LINE-HEIGHT: 15pt
}
.tt2 {
	FONT-SIZE: 9pt; LINE-HEIGHT: 16pt
}
.tt1 {
	FONT-SIZE: 14px
}
.tt3 {
	FONT-SIZE: 9pt; LINE-HEIGHT: 13pt
}
A.hb {
	FONT-SIZE: 9pt; COLOR: #000000; LINE-HEIGHT: 10pt
}
A.tt1 {
	COLOR: #000000; TEXT-DECORATION: none
}


</STYLE>


</head>
<body background=http://www.leoboard.com/lb5000/images/schedulebg.gif text="#333333" link="#0066CC" alink="#663366" vlink="#663366">
<div align=center>
<center>
    <table width="776" height="40" border="0" cellspacing="0" cellpadding="0" align="center" bgcolor="#ffffff">
      <tr> 
        <td height="40" width="176"> 
          
        <div align="center"><img src="http://www.leoboard.com/images/mainlogo.gif" width="170" height="60" border="0" align="middle"></div>
        </td>
        
      <td height="40" colspan="2"> 
        <div align="right">
          <script src="http://www.leoboard.com/cgi-bin/leoad.cgi"></script>
        </div>
      </div>
         
        
      
      <tr align="right"> 
        <td colspan="3"> 
          <table border="1" cellspacing="1" bordercolorlight="#666666" bordercolordark="#FFFFFF" cellpadding="1" width="100%">
            <tr bgcolor="#CCCCCC"> 
              <td colspan="7">&nbsp;</td>
            </tr>
          </table>
        </td>
      </tr>
    </table> 

    <table width="776" border="1" cellspacing="0" cellpadding="0" align="center">
      <tr> 
        <td colspan="2" valign="top"> 
        ~;
           if ($requestver =~/LB5000/g){
                $myver=$requestver;
                $myver=~s /LB5000II v//isg;
                $newver=$nowver;
                $newver=~s /LB5000II v//isg;
                if ($myver >= $newver){
                print qq~
                <br><br><font face=���� size=3 color=#333333 ><center><b>������ʹ�õ������°汾����л��ʹ�����ǵ���̳ ��</b><br><br>
                ~;
                }else{
               print qq~
                <br><br><font face=���� size=3 color=#333333 ><center><b>��ǰ$nowver�Ѿ��ṩ���أ��������Ҫ��������ο���������� ��</b><br><br>
                ~;
               }
               print qq~
               <table><tr><td>��ǰ���°汾:<font color=red><b>$lastver</b></font> <br><hr>
               <br>
               ����ɹ���:<br>
               $finish <br><br>
               <b>�����ṩ����ʱ��:$downtime</b> <br>
               <hr>
               </td></tr>
               <tr><td>��ǰ���ṩ���ص����°汾:<font color=red><b>$nowver</b></font> <br><hr>
               <br>
               �����б�:<br>
               $hasfunc <br><br>
               <b>���ص�ַ:<br>
                [GB�汾]��<a href=$gb>$gb</a> <br>
                [BIG5�汾]��<a href=$big5>$big5</a></b><br>
              <hr><br>
               <b>��2001��5��15������������<font color=blue><b>$download</b></font>�˰�װ������̳��</b>
               <hr>������ʵʱ���°汾��Ϣ���ж������û����ṩ��ʱ�����������ѵȣ�������Ĳ�Ʒ��Ҫ���ƹ��ܣ�����ϵ<a href=mailto:info\@cgier.net>����ȱ</a>��<a href=mailto:webmaster\@cgier.com>ɽӥ</a>!<br><br></td></tr></table>
               ~;
               }else{
               print qq~
                <br><br><center><font color=red size=4>�汾��Ϣ����</font><br><Br><font face=���� size=3 color=#333333 ><b>����������İ汾�Ų���ȷ������������,<br>�������IB2000�û�������һ�ΰ�װ!</b><br><br><b>��2001��5��15������������<font color=blue><b>$download</b></font>�˰�װ������̳��</b></font><br><br><br>
               <hr>������ʵʱ���°汾��Ϣ���ж������û����ṩ��ʱ�����������ѵȣ�������Ĳ�Ʒ��Ҫ���ƹ��ܣ�����ϵ<a href=mailto:info\@cgier.net>����ȱ</a>��<a href=mailto:webmaster\@cgier.com>ɽӥ</a>!<br><br>
                ~;
               }
               

                print qq~
                </center>
                </td></tr></table></td></tr></table>
                </td>
      </tr>
    </table>
    <table width="776" border="1" cellspacing="0" cellpadding="0" align="center">
      <tr> 
        <td height="38" colspan="3" valign="top"> 
          <div align="center"> </div>
          <div align="center"> </div>
          <div align="center">
            <table height=22 cellspacing=0 cellpadding=0 width="100%" 
                  border=0>
              <tbody> 
              <tr > 
                <td colspan="2" width="100%" height="20"> 
                  <div align="center"><font class="chinese_text13" color="#000000"> 
                    <script language=JavaScript1.2>
<!--
var correctwidth=800
var correctheight=600
if (screen.width!=correctwidth||screen.height!=correctheight)
document.write("����ʹ��"+correctwidth+"��"+correctheight+"���Ϸֱ���. ����ǰ�ķֱ�����:"+screen.width+"��"+screen.height+"��")
//-->
</script>
                    </font></div>
                </td>
              </tr>
              <tr > 
                <td colspan="2" width="100%" height="20"> 
                  <div align="center" class="text1">| <a href="http://www.joydown.com" target="_blank">������������</a> 
                    | <a href="http://www.leoboard.com" target="_blank">�װ���̳</a> 
                    | <a href="http://www.cgier.com" target="_blank">CGI�����֮��</a> 
                    | <a href="http://www.realdown.com" target="_blank">��Ӱ��ʱ��</a> 
                    | <a href="http://www.17do.com" target="_blank">���һ�� Do</a> 
                    | <a href="http://mail\@17do.com/" target="_blank">���һ����</a> 
                    | <a href="http://www.cnleo.com" target="_blank">�װ�������</a> 
                    | 
                    <script>
document.write("<a href=http://www.textclick.com/viewmain.asp?name=cnleo target=_blank><img src=http://ad.t2t2.com/stat.asp?user=cnleo&refer="+escape(document.referrer)+"&cur="+escape(document.URL)+" alt=̫��ͳ�� border=0 width=0 height=0></a>");
</script>
                  </div>
                </td>
              </tr>
              </tbody> 
            </table>
          </div>
        </td>
      </tr>
    </table>
    <br>
  </center></div>
</body>
</html>
                ~;
              
              
              exit;