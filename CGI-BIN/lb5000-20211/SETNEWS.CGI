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
require "lbadmin.lib.pl";     # Require Admin func()
require "data/progs.cgi";    # Require prog names
require "data/boardinfo.cgi";# Require board info
require "data/styles.cgi";   # Require styles info
require "data/leonews.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";          # Require lbboard ()

$|++;                                      # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "setnews.cgi";


$query = new LBCGI;



	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \"$theparam\"\;\n";
            }
	}


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");

print header(-charset=>gb2312);
&admintitle;

&getmember("$inmembername");
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
             
    if ($action eq "process") {


        $printme .= "1\;\n";

        $filetomake = "$lbdir" . "data/leonews.cgi";

        open(FILE,">$filetomake");
        flock(FILE,2);
        print FILE "$printme";
        close(FILE);
        
         
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>Welcome your lb board Administration Center</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=verdana color=#333333 size=3><center><b>The following information has been saved</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/1\;//g;
                print $printme;

                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }

                else {
                    print qq~
                    <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                    <b>Welcome to your lb board Administration Center</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=verdana color=#333333 size=3><b>All information NOT saved</b><br>The file, or directory is not writable.
                    </td></tr></table></td></tr></table>
                    ~;
                    }
        
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                               print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>Welcome to your lb board Administration Center / News Setup</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>News Set up</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
            
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>News menu links and names</center></b><br>
                <font face=verdana color=#333333 size=1>Use these options to set your names and urls that showes in the menu
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#AD0000 size=1><b>Home Page name</a></b><br>Your home page</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink1name" value="$nlink1name"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Forums URL</b><br>the url to your forums</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink1url" value="$nlink1url"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#AD0000 size=1><b>MENU NAME</b><br>Name of url</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink2name" value="$nlink2name"></td>
                </tr>
                 
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Custom URL</a></b><br>anything you like</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink2url" value="$nlink2url"></td>
                </tr>
                 
                 
                 <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#AD0000 size=1><b>MENU NAME</b><br>Name of url</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink3name" value="$nlink3name"></td>
                </tr>
                 <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Custom URL</a></b><br>anything you like</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink3url" value="$nlink3url"></td>
                </tr>
                                                                   
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#AD0000 size=1><b>MENU NAME</b><br>Name of url</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink4name" value="$nlink4name"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Custom URL</a></b><br>anything you like</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink4url" value="$nlink4url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#AD0000 size=1><b>MENU NAME</b><br>Name of url</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink5name" value="$nlink5name"></td>
                </tr>
               <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Custom URL</b><br>anything you like</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink5url" value="$nlink5url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#AD0000 size=1><b>MENU NAME</b><br>Name of url</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink6name" value="$nlink6name"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Custom URL</b><br>anything you like</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink6url" value="$nlink6url"></td>
                </tr>
                 
                 
                 <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#AD0000 size=1><b>MENU NAME</b><br>Name of url</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink7name" value="$nlink7name"></td>
                </tr>
                 <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Custom URL</b><br>anything you like</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="nlink7url" value="$nlink7url"></td>
                </tr>
                 
                 
                  <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>Active topics colors & settings</center></b><br>
                <font face=verdana color=#333333 size=1>Use these options for the Active topics
                </td></tr>
                 
                                                                            
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Active topics</b><br>the number of active topics to be shown in the left bottom table</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=2 name="listcount" value="$listcount"></td>
                </tr>
                
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>active topics Set the table background colors alt 1</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="bgcolorone" value="$bgcolorone"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>active topics Set the table background colors alt 2</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="bgcolortwo" value="$bgcolortwo"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>News colors & settings</center></b><br>
                <font face=verdana color=#333333 size=1>Use these options for the news catagory settings
                </td></tr>
                
                 <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>News websites title</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="title" value="$title"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>News Background Color</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="boardbk" value="$boardbk"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>News tables title Color</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="newsbk" value="$newsbk"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>News body background Color</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="nebdc" value="$nebdc"></td>
                </tr>
                
                 <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>News border Color</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="nbdcolor" value="$nbdcolor"></td>
                </tr>
                
                 <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>News announcments title Color</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="annob" value="$annob"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>News font Color</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="newsfontcolor" value="$newsfontcolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>News comments font Color</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="cfontcolor" value="$cfontcolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>News title font Color</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="ntfontcolor" value="$ntfontcolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>Max number of posts to display.</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="maxp" value="$maxp"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>List all forums you want for in the news. "devide them like so 1;2;3;4;5 using ";".</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="forumn" value="$forumn"></td>
                </tr>
                 
                 <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Tables width</b><br>The width of the news table</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="ntbwidth" value="$ntbwidth"></td>
                </tr>
                
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>News annoucment gif</b><br>just put the pics name with extension "make sure the pics in the images folder</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="anoupic" value="$anoupic"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Do you want news table borders?</b><br>1=yes 0=no</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=1 name="boarderw" value="$boarderw"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>Link colors & settings</center></b><br>
                <font face=verdana color=#333333 size=1>Use these options for the links colors
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>select, option, textarea, input:</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="lin1" value="$lin1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>background-color::</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="lin2" value="$lin2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>a:visited,a:active:</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="lin3" value="$lin3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>a:hover</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="lin4" value="$lin4"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>Scrollbar colors settings</center></b><br>
                <font face=verdana color=#333333 size=1>Use these options for the scroll bar colors
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>scrollbar-3d-light-color:</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="sc1" value="$sc1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>scrollbar-arrow-color:</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="sc2" value="$sc2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>scrollbar-base-color:</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="sc3" value="$sc3"></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>scrollbar-dark-shadow-color:</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="sc4" value="$sc4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>scrollbar-face-color:</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="sc5" value="$sc5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>scrollbar-highlight-color:</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="sc6" value="$sc6"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>scrollbar-shadow-color:</b></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=10 name="sc7" value="$sc7"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>Tables on and off settings</center></b><br>
                <font face=verdana color=#333333 size=1>Use these options to turn off tables if you are diplaying news in your own table like via SSI
                </td></tr>
                
                ~;
                
                $tempoutput = "<select name=\"box1\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$box1\"/value=\"$box1\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Do you want news to have menu tables on the right and left?</b><br>
                <font face=verdana color=#333333 size=1>Leave this option to yes unless you are using the news in SSI option or your own tables</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
               
                
                $tempoutput = "<select name=\"announc\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$announc\"/value=\"$announc\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Do you want news announcments on top?</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                $tempoutput = "<select name=\"pass1\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$pass1\"/value=\"$pass1\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Turn password table on?</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                $tempoutput = "<select name=\"logo1\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$logo1\"/value=\"$logo1\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Do you want board logo enabled?</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                $tempoutput = "<select name=\"ava\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$ava\"/value=\"$ava\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Choose to turn avatars on or off in news. Warning on use if fou have avatars installed</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                $tempoutput = "<select name=\"clock\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$clock\"/value=\"$clock\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Choose to have a clock.</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                $tempoutput = "<select name=\"rtmenu\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$rtmenu\"/value=\"$rtmenu\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Choose to have menu buttons on right top of new page.</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                                                              
                $tempoutput = "<select name=\"memn\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$memn\"/value=\"$memn\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Inbox status at the top of news?</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                
                
                $tempoutput = "<select name=\"onlineb\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$onlineb\"/value=\"$onlineb\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Online status at the right of news?</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                $tempoutput = "<select name=\"mem1\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$mem1\"/value=\"$mem1\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Inbox status at the right of news?</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                $tempoutput = "<select name=\"fbar\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$fbar\"/value=\"$fbar\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Do you want a fancy colored scrollbar?</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>~;
                
                
                $tempoutput = "<select name=\"on\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
                $tempoutput =~ s/value=\"$on\"/value=\"$on\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Do you want news to have the whos online menu?</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
               
               <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value=submit></form></td></tr></table></td></tr></table>
               
               ~;

                            
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;

