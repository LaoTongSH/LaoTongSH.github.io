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
#            http://maildo.com/      大家一起邮
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
require "data/boardinfo.cgi";
require "data/progs.cgi";
require "data/styles.cgi";
require "lb.lib.pl";
$|++;

$bgcolor = "white"; # 背景颜色

########### No need to edit below this line ###################
$thisprog = "viewavatars.cgi";

if ((!$interval) || ($interval < 1)) { $interval = 10; }
if ((!$linesperpage) || ($linesperpage < 1)) { $linesperpage = 10; }
$perpage = $interval * $linesperpage;
$query = new LBCGI;

$startimage  = $query -> param ("startimage");
$endimage    = $query -> param ("endimage");
$inpage      = $query -> param ("page");

if (($startimage < 0) || ($startimage eq "") || ($endimage <= 0) || ($endimage < $startimage)) {
 $startimage = 0;
 $endimage = $perpage - 1;
}
if ($inpage eq "") { $inpage = 1; }

$inmembername   = cookie("amembernamecookie");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
$inmembername =~ s/\///g;
$inmembername =~ s/\.\.//g;
$inmembername =~ s/\\//g;

if (!$inmembername) {
  $inmembername = "客人";
} else {
  &getmember("$inmembername");
  &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");


$count = 0;

$dirtoopen = "$imagesdir" . "avatars";
opendir (DIR, "$dirtoopen");
@dirdata = readdir(DIR);
closedir (DIR);

@images = grep(/\.gif$/i,@dirdata);

foreach $image (@images) {
  if ($membercode ne 'ad') {
    if ($image =~ /admin\_/ig) {
      next;
    }
  }
  if ($image =~ /noavatar/ig) {
    next;
  } else {
    push (@cleanimages, $image);
  }
}

$totalimages = @cleanimages - 1;

if ($endimage > $totalimages) { $endimage = $totalimages; }

@imagestoshow = @cleanimages[$startimage..$endimage];

$numimages = $endimage - $startimage;
$shownimages = 0;

foreach (@imagestoshow) {
  $avatar =  $_;
  $avatar =~ s/.gif//i;
  $avatarout .= qq~<td align="center" valign="center"><img src="$imagesurl/avatars/$avatar.gif" alt="$avatar" $defaultwidth $defaultheight><br>$avatar</td>\n~;
  $count++;
  $shownimages++;

  if (($count eq $interval) && ($shownimages <= $numimages)) {
    $count = 0;
    $countdown++;
    $avatarout .= qq~</tr><tr bgcolor="$bgcolor">\n~;
  }
}


print header(-charset=>gb2312);

&title;

$output .= qq~
<p>
 <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
  <tr>
   <td width=30% rowspan=2> 
   <img src=$imagesurl/images/$boardlogo>
  </td>
  <td valign=top align=left>
   <font color=$fontcolormisc>
   　<img src=$imagesurl/images/closedfold.gif width=15 height=11>　<a href=$forumsummaryprog>$boardname</a><br>
   　<img src=$imagesurl/images/bar.gif width=15 height=15><img src=$imagesurl/images/openfold.gif width=15 height=11>　用户头像列表
  </td>
 </tr>
</table>
<p>
~;

$output .= qq~
<table align="center" border="0" bgcolor="000000" cellspacing="1" cellpadding="2">
<tr bgcolor="$bgcolor">
$avatarout~;

for($count; $count < $interval; $count++) {
     $output .= qq~<td>&nbsp;</td>~;
}

&splitpages;

$output .= qq~
</tr><br><tr><td colspan=$interval bgcolor="$bgcolor" align=center>
<center><font color=$fontcolormisc>$pagelinks</font></td></tr></table>
~;

&output( -Title   => "$boardname - 用户头像列表",
         -ToPrint => $output, 
         -Version => $versionnumber );

sub splitpages {
 $totalpages = @cleanimages / $perpage;
 ($pagenumbers, $decimal) = split (/\./, $totalpages);
 if ($decimal > 0) { $pagenumbers++; }

 $page = 1;
 $start = 0;
 $end = $perpage - 1;
 $pagedigit = 0;

 while ($pagenumbers > $pagedigit) {
   $pagedigit++;
   if ($inpage ne $page) {
     $pagelinks .= qq~[<a href="$boardurl/$thisprog?startimage=$start&endimage=$end&page=$page">第$pagedigit页</a>] ~;
   }
   else { $pagelinks .= qq~[<B>第$pagedigit页</B>] ~; }
   $start += $perpage;
   $end += $perpage;
   $page++;
 }
 $page--;
 $pagelinks = qq~本列表共有$page页　$pagelinks~;

 if ($totalpages <= 1) { 
  $pagelinks = qq~用户头像列表只有一页.~; 
 }
}
