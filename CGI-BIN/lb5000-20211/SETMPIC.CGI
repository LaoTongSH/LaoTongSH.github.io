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
require "lbmail.lib.pl";
require "data/progs.cgi";
require "data/mpic.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setmpic.cgi";

$query = new LBCGI;

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam =~ s/'//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \'$theparam\'\;\n";
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");


print header(-charset=>gb2312);       
&admintitle;
        
&getmember("$inmembername");
        
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 论坛图例设置</b>
            </td></tr>
            ~;
            

            if($action eq 'submit') { 
               &submit;
            }
            else { &options; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        

##################################################################################
sub submit {
	
	
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/mpic.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>以下信息已经成功保存</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=宋体 color=#333333><b>所有信息没有保存</b><br>文件或者目录不可写<br>请检测你的 data 目录和 mpic.cgi 文件的属性！
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                }
                
sub options {

   
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>论坛图例</b>
    </td>
    </tr>          
    ~;
    print qq~
    <tr>
    <td bgcolor=#FFFFFF>
    <form action="$thisprog" method="post">
    <input type="hidden" name="action" value="submit">
    <table cellspacing=0 cellpadding=0 border=0 width=95% align=center>
    <tr><td colspan=3 height=50>注意：以下所有图片必须放在${imagesdir}images目录下，不要加url路径！</td></tr>
    
    <tr>
    <td colspan=3 bgcolor=#EEEEEE>在线名单图例　　(大小：12*11)</td></tr>
    <tr>
    <td><b>论坛坛主</b></td><td><input type="text" name="onlineadmin" value="$onlineadmin"
     onblur="document.images.i_onlineadmin.src='$imagesurl/images/'+this.value;">
    </td><td><img src="$imagesurl/images/$onlineadmin" name="i_onlineadmin"></td></tr>
    
    <tr>
    <td><b>论坛总版主</b></td><td><input type="text" name="onlinesmod" value="$onlinesmod"
     onblur="document.images.i_onlinesmod.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlinesmod" name="i_onlinesmod"></td></tr>
     
     <tr>
    <td><b>论坛版主</b></td><td><input type="text" name="onlinemod" value="$onlinemod"
     onblur="document.images.i_onlinemod.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlinemod" name="i_onlinemod"></td></tr>
     
     <tr>
    <td><b>普通会员</b></td><td><input type="text" name="onlinemember" value="$onlinemember"
     onblur="document.images.i_onlinemember.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlinemember" name="i_onlinemember"></td></tr>
     
     <tr>
     <td><b>突出显示自己的颜色</b></td><td><input type="text" name="onlineselfcolor" value="$onlineselfcolor">
     </td><td><font color=$onlineselfcolor name="i_onlineself">自己</td></tr>
     
     <tr>
    <td><b>客人或隐身会员</b></td><td><input type="text" name="onlineguest" value="$onlineguest"
     onblur="document.images.i_onlineguest.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$onlineguest" name="i_onlineguest"></td></tr>
     <tr><td><BR></td><td></td></tr>
     
     <tr><td colspan=3 bgcolor=#EEEEEE>论坛图例　　(大小：13*16)</td></tr>
     
      <tr>
    <td><b>正规论坛 - 有新的帖子</b></td><td><input type="text" name="zg_havenew" value="$zg_havenew"
     onblur="document.images.i_zg_havenew.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$zg_havenew" name="i_zg_havenew"></td></tr>
     
      <tr>
    <td><b>正规论坛 - 没有新的帖子</b></td><td><input type="text" name="zg_nonew" value="$zg_nonew"
     onblur="document.images.i_zg_nonew.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$zg_nonew" name="i_zg_nonew"></td></tr>
     
          <tr>
    <td><b>开放论坛 - 有新的帖子</b></td><td><input type="text" name="kf_havenew" value="$kf_havenew"
     onblur="document.images.i_kf_havenew.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$kf_havenew" name="i_kf_havenew"></td></tr>
     
      <tr>
    <td><b>开放论坛 - 没有新的帖子</b></td><td><input type="text" name="kf_nonew" value="$kf_nonew"
     onblur="document.images.i_kf_nonew.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$kf_nonew" name="i_kf_nonew"></td></tr>
     
          <tr>
    <td><b>评论论坛 - 有新的帖子</b></td><td><input type="text" name="pl_havenew" value="$pl_havenew"
     onblur="document.images.i_pl_havenew.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$pl_havenew" name="i_pl_havenew"></td></tr>
     
      <tr>
    <td><b>评论论坛 - 没有新的帖子</b></td><td><input type="text" name="pl_nonew" value="$pl_nonew"
     onblur="document.images.i_pl_nonew.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$pl_nonew" name="i_pl_nonew"></td></tr>
     
          <tr>
    <td><b>保密论坛 - 有新的帖子</b></td><td><input type="text" name="bm_havenew" value="$bm_havenew"
     onblur="document.images.i_bm_havenew.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$bm_havenew" name="i_bm_havenew"></td></tr>
     
      <tr>
    <td><b>保密论坛 - 没有新的帖子</b></td><td><input type="text" name="bm_nonew" value="$bm_nonew"
     onblur="document.images.i_bm_nonew.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$bm_nonew" name="i_bm_nonew"></td></tr>
     
          <tr>
    <td><b>精华区</b></td><td><input type="text" name="jh_pic" value="$jh_pic"
     onblur="document.images.i_jh_pic.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$jh_pic" name="i_jh_pic"></td></tr>
     
      <tr>
    <td><b>联盟论坛区</b></td><td><input type="text" name="lm_pic" value="$lm_pic"
     onblur="document.images.i_lm_pic.src='$imagesurl/images/'+this.value;">
     </td><td><img src="$imagesurl/images/$lm_pic" name="i_lm_pic"></td></tr>
     <tr><td><BR></td><td></td></tr>
                
     <tr><td colspan=3 bgcolor=#EEEEEE>论坛按钮</td></tr>

                <tr>
                <td>
                <b>发新帖按钮图标</b>　(大小：99*25)</td>
                <td><input type=text name="newthreadlogo" value="$newthreadlogo" onblur="document.images.i_newthreadlogo.src='$imagesurl/images/'+this.value;">
                </td><td><img src=$imagesurl/images/$newthreadlogo name="i_newthreadlogo"></td>
                </tr>

                <tr>
                <td><b>发起投票按钮图标</b>　(大小：99*25)</td>
                <td>
                <input type=text name="newpolllogo" value="$newpolllogo" onblur="document.images.i_newpolllogo.src='$imagesurl/images/'+this.value;">
                </td><td><img src=$imagesurl/images/$newpolllogo name="i_newpolllogo"></td>
                </tr>

                <tr>
                <td><b>小字报按钮图标</b>　(大小：99*25)</td>
                <td>
                <input type=text name="newxzblogo" value="$newxzblogo" onblur="document.images.i_newxzblogo.src='$imagesurl/images/'+this.value;">
                </td><td><img src=$imagesurl/images/$newxzblogo name="i_newxzblogo"></td>
                </tr>

                <tr>
                <td><b>回复帖子按钮图标</b>　(大小：99*25)</td>
                <td>
                <input type=text name="newreplylogo" value="$newreplylogo" onblur="document.images.i_newreplylogo.src='$imagesurl/images/'+this.value;">
                </td><td><img src=$imagesurl/images/$newreplylogo name="i_newreplylogo"></td>
                </tr>

                <tr>
                <td><b>原窗口按钮图标</b>　(大小：74*21)</td>
                <td>
                <input type=text name="wlogo" value="$wlogo" onblur="document.images.i_wlogo.src='$imagesurl/images/'+this.value;">
                </td><td><img src=$imagesurl/images/$wlogo name="i_wlogo"></td>
                </tr>

                <tr>
                <td><b>新窗口按钮图标</b>　(大小：74*21)</td>
                <td>
                <input type=text name="nwlogo" value="$nwlogo" onblur="document.images.i_nwlogo.src='$imagesurl/images/'+this.value;">
                </td><td><img src=$imagesurl/images/$nwlogo name="i_nwlogo"></td>
                </tr>

                <tr>
                <td><b>帮助按钮图标</b>　(大小：不限)</td>
                <td>
                <input type=text name="help_blogo" value="$help_blogo" onblur="document.images.i_help_blogo.src='$imagesurl/images/'+this.value;">
                </td><td><img src=$imagesurl/images/$help_blogo name="i_help_blogo"></td>
                </tr>

                <tr>
                <td><b>新贴最后的 new 图标</b>　(大小：不限)</td>
                <td>
                <input type=text name="new_blogo" value="$new_blogo" onblur="document.images.i_new_blogo.src='$imagesurl/images/'+this.value;">
                </td><td><img src=$imagesurl/images/$new_blogo name="i_new_blogo"></td>
                </tr>
     
   <tr><td colspan=3 height=50 align=center><input type="submit" value="提 交"> <input type="reset" value="复 位"></td></tr>
     
    </form>
    
    </td>
    </tr>             
     ~;        
     
     } 
     
     
print qq~</td></tr></table></body></html>~;
exit;
