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
require "lb.lib.pl";          # Require lbboard ()

$|++;      
$query = new LBCGI;
$requestver = $query->param('ver');
$requesturl = $query->param('url');

        $geturl="http://www.leoboard.com/cgi-bin/lbver.cgi?ver=$requestver&url=$requesturl";
        $out=&lbagent($geturl);
        
        (my $lastver, my $finish,my $downtime,my $nowver,my $hasfunc,my $gb,my $big5,my $download) = split(/§/,$out);
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
	FONT-SIZE: 9pt; FONT-FAMILY: 宋体; verdana: 
}
TEXTAREA {
	FONT-SIZE: 9pt; FONT-FAMILY: 宋体; verdana: 
}
TEXTAREA {
	FONT-SIZE: 9pt; FONT-FAMILY: 宋体; verdana: 
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
                <br><br><font face=宋体 size=3 color=#333333 ><center><b>您现在使用的是最新版本，感谢你使用我们的论坛 ！</b><br><br>
                ~;
                }else{
               print qq~
                <br><br><font face=宋体 size=3 color=#333333 ><center><b>当前$nowver已经提供下载，如果你需要升级，请参看下面的连接 ！</b><br><br>
                ~;
               }
               print qq~
               <table><tr><td>当前最新版本:<font color=red><b>$lastver</b></font> <br><hr>
               <br>
               已完成功能:<br>
               $finish <br><br>
               <b>估计提供下载时间:$downtime</b> <br>
               <hr>
               </td></tr>
               <tr><td>当前可提供下载的最新版本:<font color=red><b>$nowver</b></font> <br><hr>
               <br>
               功能列表:<br>
               $hasfunc <br><br>
               <b>下载地址:<br>
                [GB版本]　<a href=$gb>$gb</a> <br>
                [BIG5版本]　<a href=$big5>$big5</a></b><br>
              <hr><br>
               <b>自2001年5月15日以来，至少<font color=blue><b>$download</b></font>人安装过本论坛！</b>
               <hr>本程序实时更新版本信息，判断正版用户，提供及时更新下载提醒等，如果您的产品需要类似功能，请联系<a href=mailto:info\@cgier.net>花无缺</a>，<a href=mailto:webmaster\@cgier.com>山鹰</a>!<br><br></td></tr></table>
               ~;
               }else{
               print qq~
                <br><br><center><font color=red size=4>版本信息错误</font><br><Br><font face=宋体 size=3 color=#333333 ><b>估计你输入的版本号不正确，请重新输入,<br>如果你是IB2000用户，请点第一次安装!</b><br><br><b>自2001年5月15日以来，至少<font color=blue><b>$download</b></font>人安装过本论坛！</b></font><br><br><br>
               <hr>本程序实时更新版本信息，判断正版用户，提供及时更新下载提醒等，如果您的产品需要类似功能，请联系<a href=mailto:info\@cgier.net>花无缺</a>，<a href=mailto:webmaster\@cgier.com>山鹰</a>!<br><br>
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
document.write("建议使用"+correctwidth+"×"+correctheight+"以上分辨率. 您当前的分辨率是:"+screen.width+"×"+screen.height+"。")
//-->
</script>
                    </font></div>
                </td>
              </tr>
              <tr > 
                <td colspan="2" width="100%" height="20"> 
                  <div align="center" class="text1">| <a href="http://www.joydown.com" target="_blank">欢乐软件下载</a> 
                    | <a href="http://www.leoboard.com" target="_blank">雷傲论坛</a> 
                    | <a href="http://www.cgier.com" target="_blank">CGI编程者之家</a> 
                    | <a href="http://www.realdown.com" target="_blank">电影即时载</a> 
                    | <a href="http://www.17do.com" target="_blank">大家一起 Do</a> 
                    | <a href="http://mail\@17do.com/" target="_blank">大家一起邮</a> 
                    | <a href="http://www.cnleo.com" target="_blank">雷傲工作室</a> 
                    | 
                    <script>
document.write("<a href=http://www.textclick.com/viewmain.asp?name=cnleo target=_blank><img src=http://ad.t2t2.com/stat.asp?user=cnleo&refer="+escape(document.referrer)+"&cur="+escape(document.URL)+" alt=太极统计 border=0 width=0 height=0></a>");
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