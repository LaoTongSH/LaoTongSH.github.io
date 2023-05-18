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

sub getlastvisit {
    $lv = $query->cookie("templastvisit");
    if (! $lv) {
        $lv = $query->cookie("lastvisit");
        if (! $lv) { $ctime = time; $lv = "$inforum-$ctime--"; }
        $tempvisitcookie = cookie(-name    =>   "templastvisit",
                                  -path    =>   "$cookiepath/",  
                                  -expires =>   "+30d",
                                  -value   =>   "$lv");
    }
    @pairs = split(/\--/,$lv);
    foreach (@pairs) {
        ($n, $val) = split(/\-/,$_);
        $lastvisitinfo{$n} = "$val";
    }
}

sub setlastvisit {
    local($tinfo) = @_;
    ($tid, $tv) = split(/\,/,$tinfo);
    $lastvisit = $query->cookie("lastvisit");
    @newv= ""; $u = "0";
    @pairs = split(/\--/,$lastvisit);
    foreach (@pairs) {
        ($n, $val) = split(/\-/,$_);
        if ("$tid" eq "$n") {
            $u = "1"; $val = $tv;
        }
        push(@newv, "$n-$val--");
    }

    if ($u eq "0" && $tinfo ne "") { push(@newv,"$tid-$tv--"); }
    $nfo = ""; $nfo = join("",@newv);
    $permvisitcookie = cookie(-name    =>   "lastvisit",
                              -value   =>   "$nfo",
                              -path    =>   "$cookiepath/",
                              -expires =>   "+30d");
    if ($mv eq "1") {
        $tempvisitcookie = cookie(-name    =>   "templastvisit",
                                  -value   =>   "$nfo",
                                  -expires =>   "+30d",
                                  -path    =>   "$cookiepath/");
    }
}

###########################
# Forum Jump
sub forumjump {

$jumphtml .= qq~
<SCRIPT LANGUAGE="JavaScript">
<!-- 
function menu(){
var URL = document.jump.jumpto.options[document.jump.jumpto.selectedIndex].value;
top.location.href = URL; target = '_self';
}
// -->
</SCRIPT>
<form action="$boardurl/$forumsprog" method="post" name="jump">
<select name="jumpto" onchange="menu()">
<option value="$boardurl/$forumsummaryprog">跳转论坛至...</option>
~;        

if ($#forums < 1) {
  my $filetoopen = "$lbdir" . "data/allforums.cgi";
  flock(FILE, 1) if ($OS_USED eq "Unix");
  open(FILE, "$filetoopen");
  @forums = <FILE>;
  close(FILE);
}
foreach my $forum (@forums) { #start foreach @forums
    chomp $forum;
    next if ($forum eq "");
    (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription, my $tmp , $tmp , $tmp , $tmp,  $tmp , $tmp , $tmp,  $tmp,  $tmp,  $tmp, $tmp, $tmp, $tmp,my $hiddenforum,$tmp,$tmp,$tmp, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);
    next if ($forumid !~ /^[0-9]+$/);
    next if ($categoryplace !~ /^[0-9]+$/);
    $rearrange = ("$categoryplace\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$ratings\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$miscadd1\t$miscadd2\t$miscadd3\t$miscadd4\t$miscad5\t");
    push (@rearrangedforums, $rearrange);
}

@finalsortedforums = sort {$a<=>$b} @rearrangedforums;

foreach my $sortedforums (@finalsortedforums) {
  (my $categoryplace, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $ratings, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $miscadd1,my $miscadd2,my $miscadd3,my $miscadd4,my $miscad5) = split(/\t/,$sortedforums);
  if ($categoryplace ne $lastcategoryplace) {
      $has=0;
      foreach (@hascat){ $has=1 if ($_ eq $categoryplace); }
      if ($has ==0){
        $jumphtml .= "<option value=\"$forumsprog?forum=$forumid\" style=background-color:$titlecolor>╋$category\n</option>";
        foreach my $myforums (@rearrangedforums) { 
           (my $mycategoryplace, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $ratings, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $miscadd1,my $miscadd2,my $miscadd3,my $miscadd4,my $miscad5) = split(/\t/,$myforums); 	    
           if ($categoryplace eq $mycategoryplace){
             if ($hiddenforum eq "yes"){ $forumname .="(隐含)" ; }
             $jumphtml .= "<option value=\"$forumsprog?forum=$forumid\">　├$forumname\n</option>" if (($disphideboard eq "yes")||($hidden eq "")||($membercode eq "ad"));
           }
        }
      }
  }
  $lastcategoryplace = $categoryplace;
  push (@hascat, $categoryplace);
}
$jumphtml .= qq~</select>\n~;
}
 
sub printmessanger {
   my %args = (
   -Title        => "", 
   -ToPrint      => "",
   -Version      => "", 
   @_, 
   ); 

   my $title         = $args{-Title}; 
   my $output        = $args{-ToPrint}; 
   my $versionnumber = $args{-Version};

    
   print qq~
    <html>
    <head>
    <title>$title</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
      
    <style type="text/css">
    <!--
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}
		
	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}
	        
		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
-->
</style>
<script>    
function openwin(url, width, height) {
	var Win = window.open(url,"openScript",'width=' + width + ',height=' + height + ',resizable=1,scrollbars=yes,menubar=yes,status=yes' );
}
ie = (document.all)? true:false
if (ie){
function ctlent(eventobject){if(event.ctrlKey && window.event.keyCode==13){this.document.FORM.submit();}}
}
</script>
</head>
<body bgcolor=#ffffff topmargin=10 leftmargin=10>
~;


print qq~$output\n~;
exit;
}


sub messangererror {
    local($errorinfo) = @_;
    (my $where, my $errormsg) = split(/\&/, $errorinfo);

    $output = qq~
	<table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
	<tr>	
	    <td>
		<table cellpadding=6 cellspacing=1 border=0 width=100%>
		<tr>
   			<td bgcolor=$miscbacktwo valign=middle align=center><font face=$font color=$fontcolormisc><b>错误： $where</b></font></td></tr>
   			<tr>
   				<td bgcolor=$miscbackone valign=middle><font face=$font color=$fontcolormisc>
   				<b>关于 $where 的详细错误原因</b>
   				<ul>
   				<li><b>$errormsg</b>
   				<li>你是否仔细阅读了<a href="$helpprog">帮助文件</a>？
   				</ul>
		                <b>产生 $where 错误可能的原因：</b>
                		<ul>
		                <li>密码错误
                		<li>用户名错误
		                <li>用户没有<a href="$registerprog">注册</a>
   				</ul>
   				</tr>
   				</td></tr>
   				<tr>
   				<td bgcolor=$miscbacktwo valign=middle align=center><font face=$font color=$fontcolormisc> <a href="javascript:history.go(-1)"> << 返回上一页</a>
   				</td></tr>
   				</table></td></tr></table>
				~;
   
	&printmessanger(
            -Title   => "$boardname - 短消息", 
            -ToPrint => $output, 
            -Version => $versionnumber 
        );
}

1;