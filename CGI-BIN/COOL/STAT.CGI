#!/usr/bin/perl
#
########## ����ͼ������ͳ�� 1.0 Beta 0825 #############################################
#
#  ��Ȩ����: ɽӥ�� (Shining Hu) �� ����ʯ����������
#  E-mail��: webmaster@cgier.com  or  cgi@cgier.net
#  OICQ����: 1985858
#  ��ҳ��ַ: http://www.CGIer.com/ (CGI �����֮��)
#
#  ��������: 2000/08/08		����޸�����: 2000/08/25
#
########## -- Copyright 1997-20XX Sapphire Software Studio -- ########################
#
#  ����Ȩ������
#
#     ������Ϊ��������(shareware)�ṩ������վ���ʹ�ã�����Ƿ��޸ģ�
# ת�أ�ɢ��������������ͼ����Ϊ��������ɾ����Ȩ������
#     ���������վ��ʽ����������ű�������֪ͨ���ǣ��Ա������ܹ�֪����
# ������ܣ�����������վ�������ǵ����ӣ�ϣ���ܸ��������лл��
#
#  ��ʹ��Ҫ��
#
#     �����Ǹ�����վ������û���漰�κε���ҵ��Ϊ����ôֻ������ҳ����������վ��
# ���ӣ�������ʹ�á�
#     ��������ҵ��վ������������Ÿ�֪�����õ����ǵ������󷽿�ʹ�á�
#     �����ԶԽű��ڵ������������Ҫ���޸Ļ������������������޸Ľű����������֣�
#������������������������������������������������ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ���Ҫ�޸Ļ���Ҫ�������⹦���������������ȶ��лл������
#
######################################################################################
#    �����������ǵ��Ͷ��Ͱ�Ȩ����Ҫɾ�����ϵİ�Ȩ�������֣�лл��������
######################################################################################

$starttime = "2000/08/25";	# ��ʼͳ�Ƶ�����(�밴�� yyyy/mm/dd ��ʽ��д
$LOCK      = "YES";        	# Unix ��ϵͳ��д YES(��д)��Win ��ϵͳ��д�� YES ֵ
$totleview = 0;			# ������Ĭ�������������������ˬˬ :D

$mypath	   = "/user/l/la/laotong/cgi-bin/cool";	# �Զ���⵱ǰĿ¼����·�����������ɾ�����к�ֱ������!

$datapath  = "$mypath/data";    # �����ļ���ž���·��(���Ҫ�� / )��

$bg_gif    = "$mypath/bg.gif";  # ʹ�õı���ͼƬ�ļ����ľ���·��
$num_gif   = "$mypath/num.gif"; # ����ͼ�е�����ͼƬ�ļ����ľ���·��
$bar_gif   = "$mypath/bar.gif"; # ʹ�õ���״ͼƬ�ļ����ľ���·��
#ע����������ͼƬ�ļ��ɰ���Ĭ��ͼƬ�Ĵ�С���л���

######################################################################################
# ���²������Բ������ã�����Ϥ�����������£����԰���˵���Լ����ã�����ǰ�������ñ���
######################################################################################
$overtime         = 10*60;      # Ĭ��һ���û�������ʱ��(��λ����)
$reloadtime 	  = 12*60*60;	# Ĭ�ϴ�ʱ���ڵ�ͬһ�� IP ����(�������ˢ����д 0����λ����)
$fontc		  = "1";     	# ������ɫ    (0=��ɫ,1=��ɫ,2=��ɫ,3=��ɫ,4=��ɫ,5=��ɫ)
$fontb		  = "0";     	# ������Ӱ��ɫ(0=��ɫ,1=��ɫ,2=��ɫ,3=��ɫ,4=��ɫ,5=��ɫ)
$linec   	  = "5";     	# ������ɫ    (0=��ɫ,1=��ɫ,2=��ɫ,3=��ɫ,4=��ɫ,5=��ɫ)
$totlemany	  = 5; 		# Ĭ����������λ������ʵ��λ��������ʱ�����Զ���ʵ��λ�����
$onlinemany	  = 2; 		# Ĭ����������λ������ʵ��λ��������ʱ�����Զ���ʵ��λ�����
$yearmany	  = 6;		# Ĭ����������λ������ʵ��λ��������ʱ�����Զ���ʵ��λ�����
$daymany	  = 4; 		# Ĭ����������λ������ʵ��λ��������ʱ�����Զ���ʵ��λ�����

######################################################################################
# �������˽� PERL CGI ��̣������벻Ҫ���׸Ķ����沿�֣�
######################################################################################
use GD;

$people = 1;
$picx   = 468;                         #ͼƬ�Ŀ���
$picy   = 60;                          #ͼƬ�ĸ߶� 

# ȡʱ�� ###############################################################
($sec,$min,$hour,$mday,$mon,$year)=localtime(time); 
$mon=$mon+1;
$year=$year+1900;

#�ж����߼��Ƿ� RELOAD #################################################
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


#�ѵ�ǰ�����˵��������########################################################################
if ($check == 0) {
  open (FILE,">>$datapath/online.cgi")
  &lockfile(FILE);
  print FILE "$ENV{'REMOTE_ADDR'},$mday,$hour,$min,$sec\n";
  &unlockfile(FILE);
  close (FILE);
}

#�������������������ͳ��########################################################################
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

#��� 12 ���µ���ͳ��########################################################################
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

#���24Сʱͳ��########################################################################
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
#�ܷ�������1########################################################################
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


#��ʼ��ͼ########################################################################

print "Content-type: image/gif\n\n";

$im = new GD::Image($picx,$picy);

#������ɫ
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

#������
open(GIF,"$bg_gif");
$bggif = newFromGif GD::Image(GIF);
close(GIF);
$im->copy($bggif,0,0,0,0,468,60);


#��ʾ�ܷ�����
$totleman+=$totleview;
$totlemany = length($totleman)  if (length($totleman) > $totlemany);  #�������λ���������
$totleman = sprintf ("%0".$totlemany."d",$totleman);
$im->string(gdMediumBoldFont,8+(9-$totlemany)*3,44,"$totleman",$fontbgcolor);
$im->string(gdMediumBoldFont,8+(9-$totlemany)*3,45,"$totleman",$fontbgcolor);
$im->string(gdMediumBoldFont,9+(9-$totlemany)*3,44,"$totleman",$fontbgcolor);
$im->string(gdMediumBoldFont,9+(9-$totlemany)*3,45,"$totleman",$fontbgcolor);
$im->string(gdMediumBoldFont,7+(9-$totlemany)*3,43,"$totleman",$fontcolor);

#�������ͳ��
$daymany = length($totalhours)  if (length($totalhours) > $daymany);  #�������λ���������
$totalhours = sprintf ("%0".$daymany."d",$totalhours);
$im->string(gdMediumBoldFont,136+(9-$daymany)*3,46,"$totalhours",$fontbgcolor);
$im->string(gdMediumBoldFont,136+(9-$daymany)*3,45,"$totalhours",$fontbgcolor);
$im->string(gdMediumBoldFont,135+(9-$daymany)*3,44,"$totalhours",$fontcolor);

#���ڼ���ͳ��
$totalmonths=0;  
for ($inti=1;$inti<=12;$inti++)
{
   ($datetime,$data1)=split(/\|/,$month[$inti]);
   $datetime2 = substr($datetime,0,4);
   $totalmonths=$data1+$totalmonths if ($datetime2 eq $year);
}
$yearmany= length($totalmonths)  if (length($totalmonths) > $yearmany);  #�������λ���������
$totalmonths = sprintf ("%0".$yearmany."d",$totalmonths); 
$im->string(gdMediumBoldFont,262+(9-$yearmany)*3,46,"$totalmonths",$fontbgcolor);
$im->string(gdMediumBoldFont,262+(9-$yearmany)*3,45,"$totalmonths",$fontbgcolor);
$im->string(gdMediumBoldFont,261+(9-$yearmany)*3,44,"$totalmonths",$fontcolor);


#��ʾ��������
$onlinemany = length($people)  if (length($people) > $onlinemany);  #�������λ���������
$people = sprintf ("%0".$onlinemany."d",$people); #��λ
$im->string(gdMediumBoldFont,432+(3-$onlinemany)*3,2,"$people",$fontbgcolor);
$im->string(gdMediumBoldFont,432+(3-$onlinemany)*3,1,"$people",$fontbgcolor);
$im->string(gdMediumBoldFont,431+(3-$onlinemany)*3,0,"$people",$fontcolor);

#��ʾ IP
$ipip=$ENV{'REMOTE_ADDR'};
$im->string(gdSmallFont,376+(15-length($ipip))*3,46,"$ipip",$fontbgcolor);
$im->string(gdSmallFont,376+(15-length($ipip))*3,45,"$ipip",$fontbgcolor);
$im->string(gdSmallFont,377+(15-length($ipip))*3,46,"$ipip",$fontbgcolor);
$im->string(gdSmallFont,377+(15-length($ipip))*3,45,"$ipip",$fontbgcolor);
$im->string(gdSmallFont,375+(15-length($ipip))*3,44,"$ipip",$fontcolor);

# �� num ͼ
open(GIF,"$num_gif");
  $numgif = newFromGif GD::Image(GIF);
close(GIF);

$cntstr  = sprintf("%5d", $maxmonth);	# ���������
for ($i=0; $i<length($cntstr); $i++) {
   $n = substr($cntstr, $i, 1);
   $im->copy($numgif,346+$i*5,4,$n*5,0,5,7);
}

$cntstr  = sprintf("%5d", $maxday);	# ���������
for ($i=0; $i<length($cntstr); $i++) {
   $n = substr($cntstr, $i, 1);
   $im->copy($numgif,346+$i*5,18,$n*5,0,5,7);
}

$cntstr  = sprintf("%5d", $maxhour);	# ���Сʱ����
for ($i=0; $i<length($cntstr); $i++) {
   $n = substr($cntstr, $i, 1);
   $im->copy($numgif,346+$i*5,32,$n*5,0,5,7);
}

($rsec,$rmin,$rhour,$rmday,$rmon,$ryear)=localtime(time);
$endtime  = sprintf("%04d/%02d/%02d",$ryear+1900,$rmon+1,$rmday);

$im->string(gdTinyFont,407,19,"$starttime",$fontcolor); # ��ʼ����
$im->string(gdTinyFont,415,33,"$endtime",$fontcolor);   # ��������
	
# �� bar ͼ
open(GIF,"$bar_gif");
$bargif = newFromGif GD::Image(GIF);
close(GIF);

# ��ʾ������ͼ
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
	
# ��ʾ24Сʱ����ͼ	
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

#���
binmode STDOUT;
if ($GDversion <= 1.19) {
   print $im->gif ;
}
else {
   print $im->png ;
}

exit;

#���������ӳ���########################################################################
sub lockfile
{
  flock($_[0],2) if ($LOCK eq "YES");
}
sub unlockfile
{
  flock($_[0],8) if ($LOCK eq "YES");
}

#����·�������ӳ���########################################################################
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