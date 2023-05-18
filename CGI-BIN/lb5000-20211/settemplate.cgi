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
require "data/boardstats.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                                      # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "settemplate.cgi";

$query = new LBCGI;
&ipbanned; #封杀一些 ip

$process = $query ->param("process");
$action  = $query ->param("action");


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

if ($process ne "preview template") {
   print header(-charset=>gb2312);
   &admintitle;
   }

&getmember("$inmembername");
        
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
   print qq(
   <tr><td bgcolor=#333333" ><font face=宋体 color=#FFFFFF>
   <b>欢迎来到论坛管理中心 / 编辑论坛模板</b>
   </td></tr>);

unless(defined($process)) {

   $templatefile = "$lbdir" . "data/template.cgi";

   if (-e $templatefile) {
      open (TEMPLATE, "$templatefile");
      local $/ = undef;
      $template_data = <TEMPLATE>;
      close (TEMPLATE);
      }
      else {
         print qq(<tr><td><font face="宋体" color="#FF0000">
                  <b>不能够找到模板文件</b><br>
                  请确定文件 'template.cgi' 在 *.cgi 程序目录下的 'data' 目录中！
                  </td></tr></table></td></tr></table></body></html>);
         exit;
         } # end is it there

   unless (-w $templatefile) {
         print qq(<tr><td><font face="宋体" color="#FF0000">
                  <b>不能够写入模板文件</b><br><br>
                  请确定 'data/template.cgi' 文件的属性设置成了 666 ！
                  </td></tr></table></td></tr></table></body></html>);
         exit;
         }
      

   # If we're here, lets print out the template....

   ($non_editable, $user_editable) = split(/\<!--end Java-->/, $template_data);

   $non_editable =~ s/</&lt;/g;
   $non_editable =~ s/>/&gt;/g;
   $non_editable =~ s/\"/&quot;/g;
   $non_editable =~ s/\n\n/\n/ig;
   $non_editable =~ s/[\f\n\r]+/\n/ig;
   $non_editable =~ s/[\r \n]+$/\n/ig;
   $non_editable =~ s/^[\r\n ]+/\n/ig;
   $non_editable =~ s/\s+$//ig;

   $user_editable =~ s/</&lt;/g;
   $user_editable =~ s/>/&gt;/g;
   $user_editable =~ s/\"/&quot;/g;
   $user_editable =~ s/\n\n/\n/ig;
   $user_editable =~ s/[\f\n\r]+/\n/ig;
   $user_editable =~ s/[\r \n]+$/\n/ig;
   $user_editable =~ s/^[\r\n ]+/\n/ig;
   $user_editable =~ s/\s+$//ig;

   print qq(
   <tr>
   <td colspan=2>
   <form action="$thisprog" method=POST name="the_form">
   <input type="hidden" name="non_editable" value="$non_editable">
   <input type="hidden" name=process value="true">
   <textarea name="template_info" wrap="soft" cols="85" rows="20">
   $user_editable
   </textarea>
   <br><br>
   <input type="submit" value="模板预览" onclick="preview_template();">
   <input type="submit" value="保存模板" onclick="save_changes();">
   </form>
   <br><hr color=#000000>
   <font face="宋体" color="#000000">
   <b>编辑模板文件帮助</b><br>
   您可以在这里编辑模板文件，如果您不懂CSS，请不要改动。   
   <br>
   单词 '\$lbboard_main' 是用来显示论坛内容， 从头部一直到页底版权信息链接。
   你可以把 '\$lbboard_main' 放在一个表格内，但请不要改变他的名字！
   <br><br>
   如果你想预览结果，请点击 '预览' 按钮。
   <br>
   <b>请保证您没有删除 &lt;/head&gt;,&lt;/body&gt; and &lt;/html&gt; 标签！</b><br>
    如果没有 &lt;html&gt; 标签，那么本程序会在头部自动给出。
   </td>
   </tr>
   );
   } # end if def(process)

   else {

      $template_info = $query -> param("template_info");
      $header_info   = $query -> param("non_editable");

      $header_info =~ s/&lt;/</g;
      $header_info =~ s/&gt;/>/g;
      $header_info =~ s/&quot;/\"/g;
      $header_info =~ s/\n\n/\n/ig;
      $header_info =~ s/[\f\n\r]+/\n/ig;
      $header_info =~ s/[\r\n ]+$/\n/ig;
      $header_info =~ s/^[\r\n ]+/\n/ig;
      $header_info =~ s/\s+$//ig;

      $template_info =~ s/&lt;/</g;
      $template_info =~ s/&gt;/>/g;
      $template_info =~ s/&quot;/\"/g;
      $template_info =~ s/\n\n/\n/ig;
      $template_info =~ s/[\f\n\r]+/\n/ig;
      $template_info =~ s/[\r \n]+$/\n/ig;
      $template_info =~ s/^[\r\n ]+/\n/ig;
      $template_info =~ s/\s+$//ig;

      if ($process eq "preview template") {

         print header(-charset=>gb2312);

	 &title;

         $temp_board = qq(
         <table width=$tablewidth border=1 align=center><tr><td>
         $output
         <br><br><br><br><br>
         <font face="宋体" color=#000000>
         <center><h1>LB5000 的预览结果</h1>
         请注意设置还没有存入！<br>
         要保存模板设置，请返回管理中心点击 '保存模板'。
         <br><br>
         如果您希望编辑论坛的宽度，请进入管理中心的 "风格结构" 中的 "表格颜色" 模块，<BR>
         修改 "所有表格宽度" 即可，你也可以将其设置成百分比(比如：90%)。<br>
         保存后，再回到 "编辑论坛模板"，重新预览！</center>
         <br><br><br><br><br><br><br>
         <table width=80% align=center cellpadding=3 cellspacing=0>
         <tr><td align=center valign=middle>
         <font face=宋体 color=#000000>
         <a href="http://www.cgier.com">CGI 编程者之家</a><br>&copy; 2000 CGIer.com
         </font></td></tr></table>
         <p></td></tr></table></body></html>);

         $template_info =~ s/\$lbboard_main/$temp_board\n/sg;

         print $header_info;
         print $template_info;

      }

      else {

         $templatefile = "$lbdir" . "data/template.cgi";

        &winlock($templatefile) if ($OS_USED eq "Nt");
         open (TEMPLATE, ">$templatefile");
         flock (TEMPLATE, 2) if ($OS_USED eq "Unix");
         print TEMPLATE "$header_info\n";
         print TEMPLATE "<!--end Java-->\n";
         print TEMPLATE $template_info;
         close (TEMPLATE);
        &winunlock($templatefile) if ($OS_USED eq "Nt");

         
         print "<tr><td><font face=宋体><b>所有模板信息已经写入</b></font></td></tr>";
         }

      }


   } # end if logged in

   else {
      &adminlogin;
      }
                
   print qq(</table></td></tr></table></td></tr></table></body></html>) if ($process ne "preview template");
   exit;
