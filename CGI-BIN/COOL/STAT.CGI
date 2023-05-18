#!/usr/bin/perl
#
########## 网酷图形流量统计 1.0 Beta 0825 #############################################
#
#  版权所有: 山鹰糊 (Shining Hu) ／ 蓝宝石软件工作室
#  E-mail　: webmaster@cgier.com  or  cgi@cgier.net
#  OICQ　　: 1985858
#  主页地址: http://www.CGIer.com/ (CGI 编程者之家)
#
#  创建日期: 2000/08/08		最后修改日期: 2000/08/25
#
########## -- Copyright 1997-20XX Sapphire Software Studio -- ########################
#
#  【版权声明】
#
#     本软体为共享软体(shareware)提供个人网站免费使用，请勿非法修改，
# 转载，散播，或用于其他图利行为，并请勿删除版权声明。
#     如果您的网站正式起用了这个脚本，请您通知我们，以便我们能够知晓，
# 如果可能，请在您的网站做上我们的链接，希望能给予合作。谢谢！
#
#  【使用要求】
#
#     如你是个人网站，而且没有涉及任何的商业行为，那么只需在首页挂上我们网站的
# 连接，即可以使用。
#     如你是商业网站，则必须先来信告知，并得到我们的允许后方可使用。
#     您可以对脚本内的输出部分作必要的修改或美化，但不可任意修改脚本的其他部分，
#　　　　　　　　　　　　　　　　　　　　　　　　 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 如果要修改或需要增加特殊功能请务必先来信商榷，谢谢合作！
#
######################################################################################
#    请您尊重我们的劳动和版权，不要删除以上的版权声明部分，谢谢合作！！
######################################################################################

$starttime = "2000/08/25";	# 开始统计的日期(请按照 yyyy/mm/dd 格式填写
$LOCK      = "YES";        	# Unix 类系统请写 YES(大写)，Win 类系统请写非 YES 值
$totleview = 0;			# 总流量默认数，可以填个大数字爽爽 :D

$mypath	   = "/user/l/la/laotong/cgi-bin/cool";	# 自动检测当前目录绝对路径，如错误，请删除此行后直接设置!

$datapath  = "$mypath/data";    # 数据文件存放绝对路径(最后不要加 / )！

$bg_gif    = "$mypath/bg.gif";  # 使用的背景图片文件名的绝对路径
$num_gif   = "$mypath/num.gif"; # 计数图中的数字图片文件名的绝对路径
$bar_gif   = "$mypath/bar.gif"; # 使用的柱状图片文件名的绝对路径
#注：以上三张图片文件可按照默认图片的大小自行画制

######################################################################################
# 以下参数可以不用设置，在熟悉本程序的情况下，可以按照说明自己设置，设置前请先做好备份
######################################################################################
$overtime         = 10*60;      # 默认一个用户的在线时间(单位：秒)
$reloadtime 	  = 12*60*60;	# 默认此时间内的同一个 IP 不计(如果允许刷新则写 0，单位：秒)
$fontc		  = "1";     	# 字体颜色    (0=黑色,1=白色,2=黄色,3=绿色,4=红色,5=蓝色)
$fontb		  = "0";     	# 字体阴影颜色(0=黑色,1=白色,2=黄色,3=绿色,4=红色,5=蓝色)
$linec   	  = "5";     	# 折线颜色    (0=黑色,1=白色,2=黄色,3=绿色,4=红色,5=蓝色)
$totlemany	  = 5; 		# 默认总流量的位数，当实际位数大于它时，会自动按实际位数输出
$onlinemany	  = 2; 		# 默认在线量的位数，当实际位数大于它时，会自动按实际位数输出
$yearmany	  = 6;		# 默认年流量的位数，当实际位数大于它时，会自动按实际位数输出
$daymany	  = 4; 		# 默认日流量的位数，当实际位数大于它时，会自动按实际位数输出

######################################################################################
# 除非您了解 PERL CGI 编程，否则请不要轻易改动下面部分！
######################################################################################
use GD;

$people = 1;
$picx   = 468;                         #图片的宽度
$picy   = 60;                          #图片的高度 

# 取时间 ###############################################################
($sec,$min,$hour,$mday,$mon,$year)=localtime(time); 
$mon=$mon+1;
$year=$year+1900;

#判断在线及是否 RELOAD #################################################
open (FILE,"$datapath/online.cgi");
&lockfile(FILE);
@LINES=<FILE>;
&unlockfile(FILE);
close(FILE);

open (FILE,">$datapath/online.cgi") || die "Can't Open $filename: $!\n";
&lockfile(FILE);
$check=0;
foreach(@LINES) {
   ($addr,$come_day,$come_hour,$come_min,$come_sec,$come_time)=split(/,/,$_);
   $flag=($mday-$come_day)*24*3600+($hour-$come_hour)*3600+($min-$come_min)*60+($sec-$come_sec);
   if ( $addr eq "$ENV{'REMOTE_ADDR'}" ) {
      print FILE "$ENV{'REMOTE_ADDR'},$mday,$hour,$min,$sec\n";
      $check=1;
      $reloads=1 if ($flag < $reloadtime && $flag > 0);
   }
   elsif (($flag < $reloadtime && $flag > 0)||($flag < $overtime && $flag > 0)) {
      print FILE $_;
      $people++ if($flag < $overtime && $flag > 0);
   }
}
&unlockfile(FILE);
close(FILE);


#把当前在线人的情况存盘########################################################################
if ($check == 0) {
  open (FILE,">>$datapath/online.cgi")
  &lockfile(FILE);
  print FILE "$ENV{'REMOTE_ADDR'},$mday,$hour,$min,$sec\n";
  &unlockfile(FILE);
  close (FILE);
}

#今日流量和最大日流量统计########################################################################
open (FILE,"$datapath/day.cgi");
&lockfile(FILE);
$str=<FILE>;
($taday,$maxday)=split(/,/,$str);
&unlockfile(FILE);
close(FILE);
($datetime,$totalhours)=split(/\|/,$taday);

if ($reloads == 0) {
  $datetime1 = sprintf("%04d%02d%02d",$year,$mon,$mday);
  if ($datetime eq $datetime1) {
     $totalhours++;
  }
  else {
     $totalhours=1;
  }
  $taday="$datetime1|$totalhours";
  $maxday = $totalhours if($totalhours>$maxday);

  open (FILE,">$datapath/day.cgi");
  &lockfile(FILE);
  print FILE "$taday,$maxday\n";
  &unlockfile(FILE);
  close(FILE);
}

#最近 12 个月的月统计########################################################################
open (FILE,"$datapath/month.cgi");
&lockfile(FILE);
$str=<FILE>;
($month[1],$month[2],$month[3],$month[4],$month[5],$month[6],$month[7],$month[8],$month[9],$month[10],$month[11],$month[12],$maxmonth)=split(/,/,$str);
&unlockfile(FILE);
close(FILE);
($datetime,$data)=split(/\|/,$month[$mon]);

if ($reloads == 0) {
  $datetime1 = sprintf("%04d%02d",$year,$mon);
  if ($datetime eq $datetime1) {
     $data++;
  }
  else {
     $data=1;
  }
  $month[$mon]="$datetime1|$data";
  $maxmonth = $data if($data>$maxmonth);
  open (FILE,">$datapath/month.cgi");
  &lockfile(FILE);
  print FILE "$month[1],$month[2],$month[3],$month[4],$month[5],$month[6],$month[7],$month[8],$month[9],$month[10],$month[11],$month[12],$maxmonth\n";
  &unlockfile(FILE);
  close(FILE);
}

#最近24小时统计########################################################################
open (FILE,"$datapath/hour.cgi");
&lockfile(FILE);
$str=<FILE>;
($hourm[0],$hourm[1],$hourm[2],$hourm[3],$hourm[4],$hourm[5],$hourm[6],$hourm[7],$hourm[8],$hourm[9],$hourm[10],$hourm[11],$hourm[12],$hourm[13],$hourm[14],$hourm[15],$hourm[16],$hourm[17],$hourm[18],$hourm[19],$hourm[20],$hourm[21],$hourm[22],$hourm[23],$maxhour)=split(/,/,$str);
&unlockfile(FILE);
close(FILE);
($datetime,$data)=split(/\|/,$hourm[$hour]);

if ($reloads == 0) {
  $datetime1 = sprintf("%04d%02d%02d%02d",$year,$mon,$mday,$hour);
  if ($datetime eq $datetime1) {
     $data++;
  }
  else {
     $data=1;
  }
  $hourm[$hour]="$datetime1|$data";
  $maxhour = $data if($data>$maxhour);
  open (FILE,">$datapath/hour.cgi");
  &lockfile(FILE);
  print FILE "$hourm[0],$hourm[1],$hourm[2],$hourm[3],$hourm[4],$hourm[5],$hourm[6],$hourm[7],$hourm[8],$hourm[9],$hourm[10],$hourm[11],$hourm[12],$hourm[13],$hourm[14],$hourm[15],$hourm[16],$hourm[17],$hourm[18],$hourm[19],$hourm[20],$hourm[21],$hourm[22],$hourm[23],$maxhour\n";
  &unlockfile(FILE);
  close(FILE);
}  
#总访问量加1########################################################################
open (FILE,"$datapath/totles.cgi");
&lockfile(FILE);
$totleman = <FILE>;
&unlockfile(FILE);
close(FILE);
  
if ($reloads == 0) {
  $totleman++;
  open (FILE,">$datapath/totles.cgi");
  &lockfile(FILE);
  print FILE $totleman;
  &unlockfile(FILE);
  close(FILE);
}


#开始绘图########################################################################

print "Content-type: image/gif\n\n";

$im = new GD::Image($picx,$picy);

#定义颜色
$bg     = $im->colorAllocate(199,190,171);
$white  = $im->colorAllocate(255,255,255);
$black  = $im->colorAllocate(0, 0, 0);
$red    = $im->colorAllocate(255, 150, 150);
$green  = $im->colorAllocate(32,255,32);
$yellow = $im->colorAllocate(255,204,0);
$blue   = $im->colorAllocate(203,251,252);
$im->interlaced('true');
$fontcolor   = ($black,$white,$yellow,$green,$red,$blue)[$fontc];
$fontbgcolor = ($black,$white,$yellow,$green,$red,$blue)[$fontb];
$linecolor   = ($black,$white,$yellow,$green,$red,$blue)[$linec];

#贴背景
open(GIF,"$bg_gif");
$bggif = newFromGif GD::Image(GIF);
close(GIF);
$im->copy($bggif,0,0,0,0,468,60);


#显示总访问量
$totleman+=$totleview;
$totlemany = length($totleman)  if (length($totleman) > $totlemany);  #如果超过位数，则调整
$totleman = sprintf ("%0".$totlemany."d",$totleman);
$im->string(gdMediumBoldFont,8+(9-$totlemany)*3,44,"$totleman",$fontbgcolor);
$im->string(gdMediumBoldFont,8+(9-$totlemany)*3,45,"$totleman",$fontbgcolor);
$im->string(gdMediumBoldFont,9+(9-$totlemany)*3,44,"$totleman",$fontbgcolor);
$im->string(gdMediumBoldFont,9+(9-$totlemany)*3,45,"$totleman",$fontbgcolor);
$im->string(gdMediumBoldFont,7+(9-$totlemany)*3,43,"$totleman",$fontcolor);

#今天计数统计
$daymany = length($totalhours)  if (length($totalhours) > $daymany);  #如果超过位数，则调整
$totalhours = sprintf ("%0".$daymany."d",$totalhours);
$im->string(gdMediumBoldFont,136+(9-$daymany)*3,46,"$totalhours",$fontbgcolor);
$im->string(gdMediumBoldFont,136+(9-$daymany)*3,45,"$totalhours",$fontbgcolor);
$im->string(gdMediumBoldFont,135+(9-$daymany)*3,44,"$totalhours",$fontcolor);

#年内计数统计
$totalmonths=0;  
for ($inti=1;$inti<=12;$inti++)
{
   ($datetime,$data1)=split(/\|/,$month[$inti]);
   $datetime2 = substr($datetime,0,4);
   $totalmonths=$data1+$totalmonths if ($datetime2 eq $year);
}
$yearmany= length($totalmonths)  if (length($totalmonths) > $yearmany);  #如果超过位数，则调整
$totalmonths = sprintf ("%0".$yearmany."d",$totalmonths); 
$im->string(gdMediumBoldFont,262+(9-$yearmany)*3,46,"$totalmonths",$fontbgcolor);
$im->string(gdMediumBoldFont,262+(9-$yearmany)*3,45,"$totalmonths",$fontbgcolor);
$im->string(gdMediumBoldFont,261+(9-$yearmany)*3,44,"$totalmonths",$fontcolor);


#显示在线人数
$onlinemany = length($people)  if (length($people) > $onlinemany);  #如果超过位数，则调整
$people = sprintf ("%0".$onlinemany."d",$people); #８位
$im->string(gdMediumBoldFont,432+(3-$onlinemany)*3,2,"$people",$fontbgcolor);
$im->string(gdMediumBoldFont,432+(3-$onlinemany)*3,1,"$people",$fontbgcolor);
$im->string(gdMediumBoldFont,431+(3-$onlinemany)*3,0,"$people",$fontcolor);

#显示 IP
$ipip=$ENV{'REMOTE_ADDR'};
$im->string(gdSmallFont,376+(15-length($ipip))*3,46,"$ipip",$fontbgcolor);
$im->string(gdSmallFont,376+(15-length($ipip))*3,45,"$ipip",$fontbgcolor);
$im->string(gdSmallFont,377+(15-length($ipip))*3,46,"$ipip",$fontbgcolor);
$im->string(gdSmallFont,377+(15-length($ipip))*3,45,"$ipip",$fontbgcolor);
$im->string(gdSmallFont,375+(15-length($ipip))*3,44,"$ipip",$fontcolor);

# 打开 num 图
open(GIF,"$num_gif");
  $numgif = newFromGif GD::Image(GIF);
close(GIF);

$cntstr  = sprintf("%5d", $maxmonth);	# 最大月流量
for ($i=0; $i<length($cntstr); $i++) {
   $n = substr($cntstr, $i, 1);
   $im->copy($numgif,346+$i*5,4,$n*5,0,5,7);
}

$cntstr  = sprintf("%5d", $maxday);	# 最大日流量
for ($i=0; $i<length($cntstr); $i++) {
   $n = substr($cntstr, $i, 1);
   $im->copy($numgif,346+$i*5,18,$n*5,0,5,7);
}

$cntstr  = sprintf("%5d", $maxhour);	# 最大小时流量
for ($i=0; $i<length($cntstr); $i++) {
   $n = substr($cntstr, $i, 1);
   $im->copy($numgif,346+$i*5,32,$n*5,0,5,7);
}

($rsec,$rmin,$rhour,$rmday,$rmon,$ryear)=localtime(time);
$endtime  = sprintf("%04d/%02d/%02d",$ryear+1900,$rmon+1,$rmday);

$im->string(gdTinyFont,407,19,"$starttime",$fontcolor); # 开始日期
$im->string(gdTinyFont,415,33,"$endtime",$fontcolor);   # 结束日期
	
# 打开 bar 图
open(GIF,"$bar_gif");
$bargif = newFromGif GD::Image(GIF);
close(GIF);

# 显示年流量图
for ($inti=1;$inti<=12;$inti++) {
   ($datetime,$data)=split(/\|/,$month[$inti]);
   $datetime2 = substr($datetime,0,4);
   if ($datetime2 eq $year) {
      $month[$inti]=sprintf("%02d",$data);
   }
   else {
      $month[$inti]="00";
   }
}
$month[13]="00";
$month[0]="00";
@findmax=sort @month;
$maxhc=$findmax[$#findmax]+2000 if ($findmax[$#findmax] > 49000 );
if ($findmax[$#findmax] < 49000 ) { $maxhc=50000;}
if ($findmax[$#findmax] < 14900 ) { $maxhc=15000;}
if ($findmax[$#findmax] < 9900  ) { $maxhc=10000;}
if ($findmax[$#findmax] < 4900  ) { $maxhc=5000; }
if ($findmax[$#findmax] < 2000  ) { $maxhc=2000; }
if ($findmax[$#findmax] < 950   ) { $maxhc=1000; }
if ($findmax[$#findmax] < 480   ) { $maxhc=500;  }
if ($findmax[$#findmax] < 190   ) { $maxhc=200;  }
if ($findmax[$#findmax] < 95    ) { $maxhc=100;  }
if ($findmax[$#findmax] < 46    ) { $maxhc=50;   }
if ($findmax[$#findmax] < 19    ) { $maxhc=20;   }
if ($findmax[$#findmax] < 10    ) { $maxhc=10;   }

for ($i=1;$i<=11;$i++) {
   $count1=$month[$i];
   $count2=$month[$i+1];
   $im->line(210+$i*9,30-28*($count1/$maxhc),219+$i*9,30-28*($count2/$maxhc),$linecolor);
   $im->line(211+$i*9,30-28*($count1/$maxhc),220+$i*9,30-28*($count2/$maxhc),$linecolor);
}
	
# 显示24小时流量图	
for ($inti=0;$inti<=23;$inti++) {
   ($datetime,$data)=split(/\|/,$hourm[$inti]);
   $datetime2 = substr($datetime,0,8);
   $datetime3 = sprintf("%04d%02d%02d",$year,$mon,$mday);
   if ($datetime2 eq $datetime3) {
      $hourm[$inti]=sprintf("%02d",$data);
   }
   else {
      $hourm[$inti]="00";
   }
}
$hourm[24]="00";
@findmax=sort @hourm;
$maxhc=$findmax[$#findmax]+2000 if ($findmax[$#findmax] > 49000 );
if ($findmax[$#findmax] < 49000 ) { $maxhc=50000;}
if ($findmax[$#findmax] < 14900 ) { $maxhc=15000;}
if ($findmax[$#findmax] < 9900  ) { $maxhc=10000;}
if ($findmax[$#findmax] < 4900  ) { $maxhc=5000; }
if ($findmax[$#findmax] < 2000  ) { $maxhc=2000; }
if ($findmax[$#findmax] < 950   ) { $maxhc=1000; }
if ($findmax[$#findmax] < 480   ) { $maxhc=500;  }
if ($findmax[$#findmax] < 190   ) { $maxhc=200;  }
if ($findmax[$#findmax] < 95    ) { $maxhc=100;  }
if ($findmax[$#findmax] < 46    ) { $maxhc=50;   }
if ($findmax[$#findmax] < 19    ) { $maxhc=20;   }
if ($findmax[$#findmax] < 10    ) { $maxhc=10;   }
if ($findmax[$#findmax] < 6     ) { $maxhc=6;    }
if ($findmax[$#findmax] < 3     ) { $maxhc=3;    }

for ($i=0;$i<=23;$i++) {
   $count1=$hourm[$i];
   $count2=$hourm[$i+1];
   $im->copy($bargif,93+$i*4.2,32-30*($count1/$maxhc),0,30-30*($count1/$maxhc),3,30*($count1/$maxhc));
}

#输出
binmode STDOUT;
if ($GDversion <= 1.19) {
   print $im->gif ;
}
else {
   print $im->png ;
}

exit;

#加锁解锁子程序########################################################################
sub lockfile
{
  flock($_[0],2) if ($LOCK eq "YES");
}
sub unlockfile
{
  flock($_[0],8) if ($LOCK eq "YES");
}

#绝对路径测试子程序########################################################################
sub mypath
{
    local $temp;
    $temp=__FILE__;
    $temp=~ s/\\/\//g if ($temp=~/\\/);
    if ($temp) {
      $mypath=substr($temp,0,rindex($temp,"/"));
    }
    else {
      $mypath=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
      $mypath=~ s/\\/\//g;
    }
    return $mypath;
}
###########################################################################################
