#!/usr/bin/perl

#############################################################
#  LeoBoard ver.5000 / LB5000 / �װ�������̳ ver.5000
#
#  ��Ȩ����: �װ�������(ԭ����ʯ���������)
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
require "lbadmin.lib.pl";
require "lbmail.lib.pl";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setmembers.cgi";

$query = new LBCGI;

&ipbanned; #��ɱһЩ ip

$action          = $query -> param('action');
$checkaction     = $query -> param('checkaction');
$inletter        = $query -> param('letter');
$inmember        = $query -> param('member');
$inmember        = &unHTML("$inmember");
$action          = &unHTML("$action");

$indellast       = $query -> param('dellast');
$indellast       = &unHTML("$indellast");
$indelposts      = $query -> param('delposts');
$indelposts      = &unHTML("$indelposts");
$indeltime       = $query -> param('deltime');
$indeltime       = &unHTML("$indeltime");
$noofone         = $query -> param('noofone');
$noofone         = &unHTML("$noofone");
$beginone        = $query -> param('beginone');
$beginone        = &unHTML("$beginone");

$noofone      = 2000 if ($noofone !~ /^[0-9]+$/);
$beginone     = 0 if ($beginone !~ /^[0-9]+$/);

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");


opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
my @backupdir = grep(/^backup/, @files2);
$backupdir=@backupdir;
if ($backupdir eq 0) {
	@backupdir = grep(/^BACKUP/, @files2);
	rename("${lbdir}BACKUP","${lbdir}backup");
}
if ($backupdir eq 0) {
	@backupdir = grep(/^Backup/, @files2);
	rename("${lbdir}Backup","${lbdir}backup");
}
$backupdir = $backupdir[0];


print header(-charset=>gb2312);       
&admintitle;
        
&getmember("$inmembername");
        
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / �û�����</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'updatecount'        =>    \&docount,
            'uptop'       	 =>    \&dotop,
            'uptopnext'       	 =>    \&dotopnext,
            'upemot'       	 =>    \&doemot,
            'upuser'       	 =>    \&doava,
            'shareforums'      	 =>    \&doshareforums,
            'dellock'      	 =>    \&dodellock,
            'uponlineuser'     	 =>    \&douponlineuser,
            'upconter'		 =>    \&doupconter,
            'init'        	 =>    \&doinit,
            'viewletter'         =>    \&viewletter,
            'edit'               =>    \&edit,        
            'deletemember'       =>    \&deletemember,
            'unban'              =>    \&unban,
            'delnopost'		 =>    \&delnopost,
            'canceldel'		 =>    \&canceldel,
            'deleteavatar'	 =>    \&deleteavatar,
            'delok'		 =>    \&delok
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &memberoptions; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        

############### delete member

sub deleteavatar {

    $oldmembercode = $membercode;
    &getmember("$inmember");
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ܰ�����Ȩɾ��̳���Ͱ������ϣ�</b></td></tr>";
            exit;
    }
    	unlink ("${imagesdir}usravatars/$inmember.gif");
    	unlink ("${imagesdir}usravatars/$inmember.png");
    	unlink ("${imagesdir}usravatars/$inmember.jpg");
    	unlink ("${imagesdir}usravatars/$inmember.swf");
    	unlink ("${imagesdir}usravatars/$inmember.bmp");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>�û�ͷ���Ѿ�ɾ����</b>
        </td></tr>
         ~;


} # end routine

##################################################################################
######## Subroutes (forum list)


sub memberoptions {

    $dirtoopen = "$lbdir" . "$memdir";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = sort(@filedata);
    @sortedfile = grep(/cgi$/i,@sortedfile);

    foreach (@sortedfile) {
    	if ($_ =~ /^\w/) {
        $fr = substr($_, 0, 1);
        $fr =~ tr/a-z/A-Z/;
        }
        else {
           $fr =substr($_, 0, 2);
        }
        push(@letters,$fr);
        }

    @sortedletters = sort(@letters);
     
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>��ѡ��һ��</b>
    </td>
    </tr>          
    ~;
  if ($membercode eq "ad") {
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=uptop">�����û�����</a></b><br>
    �û�������ʵ�����Զ����µģ����������������һ�¡�<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=updatecount">���¼����û�����</a></b><br>
    ��������ҳ��ʾ���û������������������ָ���ȷ���û�����<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>ɾ�������������û�</b>(ͬʱ���Զ������û�����)<BR>
    Ԥɾ������������ɾ���û���ֻ����һ��ͳ�ơ������̳���ǲ�����������ɾ���ġ�<BR>
    Ԥɾ��������ɾ���ڼ䣬����û���������̳����ô������ɾ����ʱ�򣬴��û����Ͻ���������<BR>
    ����ɾ�����û����������϶��ᶪʧ���������������ݣ��������޷��ָ��ġ�
	<form action="setmembers.cgi" method=get>
        <input type=hidden name="action" value="delnopost">
        <select name="deltime">
        <option value="90" >��������û���ʺͷ���
        <option value="121">�ĸ�����û���ʺͷ���
        <option value="151">�������û���ʺͷ���
        <option value="182">��������û���ʺͷ���
        <option value="212">�߸�����û���ʺͷ���
        <option value="243">�˸�����û���ʺͷ���
        <option value="273">�Ÿ�����û���ʺͷ���
        <option value="304">ʮ������û���ʺͷ���
        <option value="365">һ��֮��û���ʺͷ���
        <option value="730">����֮��û���ʺͷ���
        </select> �� 
        <select name="delposts">
        <option value="0"   >û�з�������
        <option value="10"  >�ܷ������� 10
        <option value="50"  >�ܷ������� 50
        <option value="100" >�ܷ������� 100
        <option value="200" >�ܷ������� 200
        <option value="300" >�ܷ������� 300
        <option value="500" >�ܷ������� 500
        <option value="800" >�ܷ������� 800
        <option value="1000">�ܷ������� 1000
        </select> �� 
        <select name="dellast">
        <option value="no"  >���ܷ��ʴ���
        <option value="5"   >�������� 5 ��
        <option value="10"  >�������� 10 ��
        <option value="20"  >�������� 20 ��
        <option value="50"  >�������� 50 ��
        <option value="80"  >�������� 80 ��
        <option value="100" >�������� 100 ��
        <option value="200" >�������� 200 ��
        <option value="500" >�������� 500 ��
        </select>
        <input type=submit value="Ԥ ɾ ��">
        </form>
        ~;
	if (-e "${lbdir}data/delmember.cgi") {
	    open (FILE, "${lbdir}data/delmember.cgi");
	    @delmembers = <FILE>;
	    close (FILE);
	    $delmembersize = @delmembers;
	    $delmembersize --;
	    $pretime=$delmembers[0];
	    chomp $pretime;
    	    $nowtime = time;
    	    $nowtime = $nowtime - 3*24*3600;
    	    if ($nowtime > $pretime) {
    	    	$oooput = qq~�����ϴ�Ԥɾ��ʱ���Ѿ����������� [<a href=$thisprog?action=delok>ȷ��ɾ��</a>]~;
    	    }
    	    else {
    	    	$oooput = qq~�����ϴ�Ԥɾ��ʱ�仹δ������ [<a href=$thisprog?action=delok>���ܣ�ǿ��ɾ��</a>]~;
    	    }
    	    $pretime=&dateformat($pretime);
    	    print qq~
        	�ϴ�Ԥɾ��ʱ�䣺$pretime (Ԥɾ���û������� $delmembersize ) [<a href=$thisprog?action=canceldel>ȡ��Ԥɾ��</a>]<BR>
        	$oooput
    	    ~;
	}
	else {
    	    print qq~
        	Ԥɾ���ļ������ڣ����ڿ��Խ���Ԥɾ����
    	    ~;
	}
    print qq~
    <BR><BR>
    </td>
    </tr>
    ~;
  }
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>�鿴���༭��ɾ������ֹ�û�</b><br>
    ����������ĸ����Բ鿴���û���ϸ���ϣ� ���ɱ༭���ı��û�����Ϣ��<br>
    ��ֹ�û���ֻҪ�򵥵ĵ�����༭�û�����Ȼ���ڡ��û����ԡ���ѡ�񡰽�ֹ�û����Ϳ��ԡ�<br>
    ɾ���û���ֻҪ�ҵ��û������ɾ���Ϳ��ԡ�<br>
	<form action="setmembers.cgi" method=get>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="���ٶ�λ">
        </form>
    
    ~;
    
    $nowcount =0;
    foreach (@sortedletters) {
        unless ($_ eq "$ltr") {
            $tempoutput .= qq~<br>~ if ($nowcount == int($nowcount/15)*15);
            $tempoutput .= qq~&nbsp;<a href="$thisprog?action=viewletter&letter=$_">$_</a>&nbsp;~;
            $ltr = "$_";
            $nowcount ++;
       }
    }
    
    print qq~
    ע���û������б�<br>$tempoutput
    </td>
    </tr>           
                
                
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><BR>
    <b>ע�����</b><p>
    �����ϣ���������û�һ���Զ����ͷ�Σ�ֻҪ�༭�������������ϡ�<br>
    �����̳���ô���ķ�������ȷ�����ǵĳ�Ա���.<br>
    ���������һ���û�Ϊ��������������ȴû���Զ����ͷ�Σ���ô�ͻ��Զ����һ������ͷ�Ρ�
    ����������Զ���ĵȼ�����ô����ԭͷ�ν���������<br>
    ����ֻ�ܹ������Լ�����̳����������Ҳ������������̳��ʹ�� #Moderation Mode �µĹ��ܡ�<br>
    ��ȷ�����������İ����ǿɿ��ġ�<br>
    ����Ҳ��̳��һ�������ܹ�ˮԤ���������ơ�<br>
    ֻ��̳�����ܹ�����������ġ�<br><br>
    ������ֹ��һ���û�����ôҲͬʱ��ֹ��������ԭ���ơ��ʼ�����ע��Ŀ��ܡ�
    </td>
    </tr>             
     ~;        
     
     } # end routne
     
     
##################################################################################
######## Subroutes (Do member count)  
sub canceldel {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {
	unlink ("${lbdir}data/delmember.cgi");
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>ȡ��Ԥɾ��</b><p>
        <font color=#333333>Ԥɾ���Ѿ���ȡ����</font>
        </td></tr>
         ~;
}
}

sub docount {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {

    $dirtoopen = "$lbdir" . "$memdir";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @countvar = grep(/\.cgi$/i,@filedata);
    
    $newtotalmembers = @countvar;
    
        require "$lbdir" . "data/boardstats.cgi";
        
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$newtotalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
    
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�����û�����</b><p>
                    
        <font color=#333333>��ǰ���� $newtotalmembers ��ע���û��������Ѿ����£�</font>
                    
        </td></tr>
         ~;
 }         
} # end routine

sub dotop {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {

    $dirtoopen = "$lbdir" . "$memdir";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @countvar = grep(/\.cgi$/i,@filedata);
    $totaluserdata = @countvar;

    mkdir("${lbdir}$backupdir",0777) if (!(-e "${lbdir}$backupdir"));
    open(FILE,">${lbdir}$backupdir/allname.cgi");
    foreach (@countvar) {
        print FILE "$_\n";
    }
    close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û�������ʼ��</b><br>
                    
        <font color=#333333><B>��ǰ���� $totaluserdata ��ע���û���׼�������Ѿ���ɡ�</b><BR><BR><BR>
	<form action="setmembers.cgi" method=get>
        <input type=hidden name="action" value="uptopnext">����ÿ�ν����������û��� 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="��ʼ����">
        </form>
	Ϊ�˼�����Դռ�ã�������ÿ�ν����������û�����Ĭ�� 2000��<BR>һ�㲻Ҫ���� 3000��������ֽ��������޷�������ɣ��뾡�����������Ŀ���ӳ�����ʱ�䡣
	<BR><BR>

        </td></tr>
         ~;
}
} # end routine

sub dotopnext {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {
    $dirtoopen = "$lbdir" . "$memdir";
    $filename = "alluser.pl";
    open(FILE,"${lbdir}$backupdir/allname.cgi");
    @allname = <FILE>;
    close(FILE);
    $allnamenum = @allname;
    if ($beginone < $allnamenum) {
        $lastone = $beginone + $noofone;
        $lastone = $allnamenum if ($lastone > $allnamenum);

        if ($beginone == 0) {
            unlink ("${lbdir}data/lbmember.cgi")  ;
            unlink ("${lbdir}data/lbmember0.cgi")  ;
            unlink ("${lbdir}data/lbmember1.cgi") ;
            unlink ("${lbdir}data/lbmember2.cgi") ;
            unlink ("${lbdir}data/lbmember3.cgi") ;
        }

	open  (MEMFILE, ">>${lbdir}data/lbmember.cgi");
	flock (MEMFILE, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE0, ">>${lbdir}data/lbmember0.cgi");
	flock (MEMFILE0, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE1, ">>${lbdir}data/lbmember1.cgi");
	flock (MEMFILE1, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE2, ">>${lbdir}data/lbmember2.cgi");
	flock (MEMFILE2, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE3, ">>${lbdir}data/lbmember3.cgi");
	flock (MEMFILE3, 2) if ($OS_USED eq "Unix");

	for ($i = $beginone; $i < $lastone; $i ++) {
	    $memberfile = $allname[$i];
	    open (FILE, "${lbdir}$memdir/$memberfile");
	    flock (FILE, 2) if ($OS_USED eq "Unix");
	    $line = <FILE>;
	    close (FILE);
	    chomp $line;
	    @memberdaten = split(/\t/,$line);
	    $username =$memberdaten[0];   
	    $userad=$memberdaten[3];
	    $anzahl = $memberdaten[4];
	    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
	    $anzahl1 = 0 if ($anzahl1 eq "");
	    $anzahl2 = 0 if ($anzahl2 eq "");
	    $anzahl   = $anzahl1 + $anzahl2;
	    $useremail=$memberdaten[5];
	    $date1    = $memberdaten[13];
	    $logtime = $memberdaten[27];
	    $addjy   = $memberdaten[28];
	    $meili   = $memberdaten[29];
	    $mymoney = $memberdaten[30];
	    $postdel = $memberdaten[31];

	    $logtime = 0 if ($logtime eq "");
	    $addjy   = 0 if ($addjy   eq "");
	    $meili   = 0 if ($meili   eq "");
	    $mymoney = 0 if ($mymoney eq "");
	    $postdel = 0 if ($postdel eq "");

	    $birthday = $memberdaten[36];

	    print MEMFILE "$username\t$userad\t$anzahl\t$date1\t$useremail\t\n";   
	    print MEMFILE0 "$username\t$anzahl\t\n";   
	    print MEMFILE1 "$username\t$useremail\t\n";   
	    print MEMFILE2 "$username\t$anzahl1\t$anzahl2\t$logtime\t$postdel\t$addjy\t$meili\t$mymoney\t\n";   
	    print MEMFILE3 "$username\t$birthday\t\n" if (($birthday ne "")&&($birthday ne "//"));  
	} 
	close(MEMFILE3);
	close(MEMFILE2);
	close(MEMFILE1);
	close(MEMFILE0);
	close(MEMFILE);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>�����û�����</b><p>
        <font color=#333333><B>��ǰ���� $allnamenum ��ע���û����Ѿ����������� $lastone ���û�������</b><BR><BR><BR>
        <font color=#333333>����޷��Զ���ʼ�� $noofone ���û���������������������Ӽ���<p>
        >> <a href="$thisprog?action=uptopnext&beginone=$lastone&noofone=$noofone">�������������û�</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=uptopnext&beginone=$lastone&noofone=$noofone">
	<BR><BR>

        </td></tr>
         ~;
     }
     else {


open (FILE, "$lbdir/data/lbmember0.cgi");
flock(FILE, 1) if ($OS_USED eq "Unix");
my @file = <FILE>;
close (FILE);
foreach my $line (@file) {
my @tmpuserdetail = split (/\t/, $line);
chomp @tmpuserdetail;
$postundmember {"$tmpuserdetail[0]"} = $tmpuserdetail[1];
}
my @sortiert = reverse sort { $postundmember{$a} <=> $postundmember{$b} } keys(%postundmember);

open  (MEMFILE0, ">${lbdir}data/lbmember0.cgi");
flock (MEMFILE0, 2) if ($OS_USED eq "Unix");
foreach my $member (@sortiert[0 ... 99]) {
    next if ($member eq "");
    print MEMFILE0 "$member\t$postundmember{\"$member\"}\t\n";
}
close(MEMFILE0);


        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�����û�����</b><p>
                    
        <font color=#333333>��ǰ���� $allnamenum ��ע���û��������û������Ѿ�������<BR><BR>
        </td></tr>
         ~;
     }

}
} # end routine

sub delnopost {
opendir (DIR, "${lbdir}$memdir"); 
@files = readdir(DIR);
closedir (DIR);
@memberfiles = grep(/\.cgi$/i, @files);
$size=@memberfiles;
$size1=0;
$currenttime = time;

$from = "$homename <$adminemail_out>";
$subject = "����$boardname����Ҫ�ʼ�����";
$message = "";
$message .= "\n";
$message .= "$boardname\n";
$message .= "$boardurl/$forumsummaryprog\n";
$message .= "------------------------------------------\n\n";
$message .= "ϵͳ�������Ѿ���ʱ��δ���ʱ���̳�������ˣ�\n";
$message .= "Ϊ���ͷſռ䣬����û������ڣ��պ�ɾ����\n";
$message .= "������뱣������û��������½����̳һ�Ρ�\n";
$message .= "------------------------------------------\n";
$message .= "LeoBoard 5000 �� www.cgier.com ������Ʒ��\n";

if (-e "${lbdir}data/delmember.cgi") {
    print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>�����û�����</b><p>
        <font color=#333333>Ԥɾ���ļ����ڣ������ظ�Ԥɾ����</font>
        </td></tr>
    ~;
}
else {
  open (FILE, ">${lbdir}data/delmember.cgi");
  print FILE "$currenttime\t\n";
  close (FILE);

  open (MEMFILE, ">${lbdir}data/lbmember.cgi");
  flock (MEMFILE, 2) if ($OS_USED eq "Unix");
  foreach $memberfile (@memberfiles) { # start foreach
    open (FILE, "${lbdir}$memdir/$memberfile");
    flock (FILE, 2) if ($OS_USED eq "Unix");
    $line = <FILE>;
    close (FILE);
    undef $joineddate;
    undef $lastgone;
    undef $anzahl;
    undef $lastpostdate;
    undef $userad;
    undef $visitno;
    undef $anzahl1;
    undef $anzahl2;
    undef $emailaddr;
    undef $membername;
    
    ($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no ,$no ,$no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $addjy, $meili, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $useradd1, $useradd2, $jhmp) = split(/\t/,$line);

    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
    $anzahl = $anzahl1 + $anzahl2;
    ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);

    $lastgone = $lastpost   if ($lastpost > $lastgone);
    $lastgone = $joineddate if ($joineddate > $lastgone);

    $lastgone1 = $lastgone + $indeltime*3600*24;
    $to ="";
    
    if (($lastgone1 <= $currenttime)&&($anzahl <= $indelposts)&&($userad ne "ad")&&($userad ne "mo")&&($userad ne "smo")) {
  	if ($indellast ne "no") {
  	  if ($visitno <= $indellast) {
            open (FILE, ">>${lbdir}data/delmember.cgi");
            flock (FILE, 2) if ($OS_USED eq "Unix");
            print FILE "$memberfile\t$lastgone\t\n";
            close (FILE);
            $size1++;
	    if ($to eq "") { $to = $emailaddr; } else { $to .= ", $emailaddr"; }
	  }
        }
        else {
          open (FILE, ">>${lbdir}data/delmember.cgi");
          flock (FILE, 2) if ($OS_USED eq "Unix");
          print FILE "$memberfile\t$lastgone\t\n";
          close (FILE);
          $size1++;
	  if ($to eq "") { $to = $emailaddr; } else { $to .= ", $emailaddr"; }
        }
    }
    print MEMFILE "$membername\t$userad\t$anzahl\t$joineddate\t\n";
  } 
  close(MEMFILE);

  if (($emailfunctions eq "on")&&($to ne "")) {
      &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
      $delwarn = "";
  }
  else { $delwarn = "<BR><BR><font color=red><B>�ʼ�����û�д򿪣������û��޷�����Ԥɾ����Ϣ��<B></font>"; }
  unlink ("${lbdir}data/delmember.cgi") if ($size1 eq 0);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>�����û�����</b><p>
        <font color=#333333>��ǰ���� $size ��ע���û������������Ѿ����£�</font><BR>
        <font color=#333333>Ԥɾ�� $size1 ��ע���û������������Ѿ����£��������Խ����������������ɾ����</font>
        $delwarn
        </td></tr>
         ~;
  }
} # end routine

sub delok {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {

if ($checkaction eq "yes") {
        open (FILE, "${lbdir}data/delmember.cgi");
        @alldelname=<FILE>;
        close (FILE);
 	$delsize = @alldelname;
 	$delno = 0;

$from = "$homename <$adminemail_out>";
$subject = "����$boardname����Ҫ�ʼ�����";
$message = "";
$message .= "\n";
$message .= "$boardname\n";
$message .= "$boardurl/$forumsummaryprog\n";
$message .= "------------------------------------------\n\n";
$message .= "ϵͳ�������Ѿ���ʱ��δ���ʱ���̳�������ˣ�\n";
$message .= "Ϊ���ͷſռ䣬����û����Ѿ�����ȫɾ����\n";
$message .= "------------------------------------------\n";
$to = "";
 	for ($i=1;$i<$delsize;$i++) {
	    ($memberfile, $deltime)= split(/\t/,$alldelname[$i]);
	    open (FILE, "${lbdir}$memdir/$memberfile");
    	    flock (FILE, 2) if ($OS_USED eq "Unix");
    	    $line = <FILE>;
    	    close (FILE);
	    undef $joineddate;
	    undef $lastgone;
	    undef $anzahl;
	    undef $lastpostdate;
	    undef $userad;
	    undef $visitno;
	    undef $anzahl1;
	    undef $anzahl2;
	    undef $emailaddr;
	    undef $membername;

    	    ($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no ,$no ,$no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $addjy, $meili, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $useradd1, $useradd2, $jhmp) = split(/\t/,$line);

	    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
	    $anzahl = $anzahl1 + $anzahl2;
	    ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	    $lastgone = $lastpost   if ($lastpost > $lastgone);
	    $lastgone = $joineddate if ($joineddate > $lastgone);
	    
	    if ($lastgone <= $deltime) {
	        $membername =~ s/ /\_/isg;
		$membername =~ tr/A-Z/a-z/;

        	$filetounlink = "$lbdir" . "$memdir/$membername.cgi";
	        unlink $filetounlink;

	        $filetounlink = "$lbdir" . "$msgdir/in/$membername" . "_msg.cgi";
        	unlink $filetounlink;
	        $filetounlink = "$lbdir" . "$msgdir/out/$membername" . "_out.cgi";
        	unlink $filetounlink;
	        $filetounlink = "$lbdir" . "$msgdir/main/$membername" . "_mian.cgi";
        	unlink $filetounlink;
	    	unlink ("${imagesdir}usravatars/$membername.gif");
    		unlink ("${imagesdir}usravatars/$membername.png");
	    	unlink ("${imagesdir}usravatars/$membername.jpg");
    		unlink ("${imagesdir}usravatars/$membername.swf");
	    	unlink ("${imagesdir}usravatars/$membername.bmp");

	        $filetounlink = "$lbdir" . "memfav/$membername.cgi";
        	unlink $filetounlink;
	        $filetounlink = "$lbdir" . "memfriend/$membername.cgi";
	        unlink $filetounlink;
	        $delno ++;
	  	if ($to eq "") { $to = $emailaddr; } else { $to .= ", $emailaddr"; }
	    }
 	}
 	
  	if (($emailfunctions eq "on")&&($to ne "")) {
            &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
        }
 	
 	&dotop;
 	
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers=$totalmembers - $delno;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        # Delete the database for the member

	unlink ("${lbdir}data/delmember.cgi");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$delno ������ע���û��Ѿ�������ɾ��<BR>
        �û����Ѿ�ȫ������</b>
        </td></tr>
         ~;
}

else {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>��ȫɾ�����з���������Ԥɾ���û��������������Ӽ�����<BR>
        ��Ԥɾ���ڼ���ʹ���̳���û����ᱻɾ��<p>
        <p>
        >> <a href="$thisprog?action=delok&checkaction=yes">��ʼɾ��</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
        }
}
} # end routine

sub doemot {
unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {

$dirtoopen = "$imagesdir" . "emot";
opendir (DIR, "$dirtoopen"); 
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/gif$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbemot.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);

$dirtoopen = "$imagesdir" . "posticons";
opendir (DIR, "$dirtoopen");
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/gif$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbpost.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ʼ��EMOT��POSTͼƬ</b><p>
                    
        <font color=#333333>����EMOT�ͱ���ͼƬ�Ѿ����£�</font>
                    
        </td></tr>
         ~;
}         
} # end routine
     
sub doava {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {
$dirtoopen = "$imagesdir" . "avatars";
opendir (DIR, "$dirtoopen");
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/gif$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbava.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ʼ���û�ͷ��ͼƬ</b><p>
                    
        <font color=#333333>�����û�ͷ��ͼƬ�Ѿ����£�</font>
                    
        </td></tr>
         ~;
}         
} # end routine

sub doupconter {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {
	my $onlinemaxtime = time;
	my $filetomake = "$lbdir" . "data/counter.cgi";
	open(FILE,">$filetomake");
        print FILE "1\t1\t1\t$onlinemaxtime\t";
	close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ʼ������ͳ�Ƽ����ʴ���</b><p>
                    
        <font color=#333333>���ʴ��������Ѿ���ʼ����</font>
                    
        </td></tr>
         ~;
}         
} # end routine
	
sub douponlineuser {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {
	$currenttime = time;
	my $filetoopen = "$lbdir" . "data/onlinedata.cgi";
        open(FILE9,">$filetoopen");
	print FILE9 "$inmembername\t$currenttime\t$currenttime\t������\t����\t����\t����\t������\t����\t$membercode\t" ;
	close (FILE9);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ʼ������ͳ�Ƽ����ʴ���</b><p>
                    
        <font color=#333333>��������ͳ�������Ѿ���ʼ����</font>
                    
        </td></tr>
         ~;
}         
} # end routine

sub doshareforums {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {
	my $filetoopen = "$lbdir" . "data/shareforums.cgi";
	unlink $filetoopen;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ʼ����̳��������Ϊ��</b><p>
                    
        <font color=#333333>�������������Ѿ���ʼ����</font>
                    
        </td></tr>
         ~;
}         
}

sub dodellock {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {
	my $dirtoopen = "$lbdir" . "lock";

opendir (DIRS, "$dirtoopen");
my @files = readdir(DIRS);
closedir (DIRS);
        foreach $file (@files) {
            $filetoremove = "$dirtoopen/$file";
            unlink $filetoremove;
            }

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ʼ�������ļ�</b><p>
                    
        <font color=#333333>���������ļ��Ѿ���ʼ����</font>
                    
        </td></tr>
         ~;
}         
} # end routine

sub doinit  {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {
print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ʼ����̳����</b><p>
                    
        <font color=#333333>�״�������̳�������У��Ժ������������̳����ͼƬ�ȣ�Ҳ��Ҫ���У�</font>
                    
        </td></tr>
        
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>����<b><a href="$thisprog?action=uptop">��ʼ���û�����</a></b><br>
    �û�������ʵ�����Զ����µģ����������������һ�¡�<BR><BR>
    </td>
    </tr>
    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>����<b><a href="$thisprog?action=upemot">��ʼ������ͼƬ��EMOTͼƬ</a></b><br>
    ����ͼƬ��EMOT��ʵ�����Զ����µģ����������������һ�¡�<BR><BR>
    </td>
    </tr>
    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>����<b><a href="$thisprog?action=upuser">��ʼ���û�ͷ��ͼƬ</a></b><br>
    �û�ͷ����ʵ�����Զ����µģ����������������һ�¡�<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>����<b><a href="$thisprog?action=uponlineuser">��ʼ������ͳ��</a></b><br>
    ��������������ͳ�����ݳ���Ļ��������������ʼ��һ�¡�<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>����<b><a href="$thisprog?action=upconter">��ʼ�����ʴ���</a></b><br>
    �����ķ��ʴ���ͳ�ƺ�����������������ݳ���Ļ��������������ʼ��һ�¡�<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>����<b><a href="$thisprog?action=shareforums">��ʼ����������</a></b><br>
    ��������������ɾ���������ǳ���Ļ��������������ʼ��һ�¡�<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>����<b><a href="$thisprog?action=dellock">��ʼ�������ļ�</a></b><br>
    �����������ļ�Ŀ¼���ж���Ļ���ɾ�������������ļ��Ļ��������������ʼ��һ�¡�<BR><BR>
    </td>
    </tr>

         ~;
}
}     
##################################################################################
######## Subroutes (Do member count) 


sub viewletter {

    $dirtoopen = "$lbdir" . "$memdir";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = sort(@filedata);
    @sortedfile = grep(/cgi$/i,@sortedfile);
    @sortedfile = sort alphabetically(@sortedfile);
    
    foreach (@sortedfile) {
    	if ($_ =~ /^\w/) {
        $fr = substr($_, 0, 1);
        $fr =~ tr/a-z/A-Z/;
        }
        else {
           $fr =substr($_, 0, 2);
        }
        push(@letters,$fr);
        }
    @sortedletters = sort(@letters);
    $nowcount =0;
    foreach (@sortedletters) {
        unless ($_ eq "$ltr") {
            $tempoutput .= qq~<br>~ if ($nowcount == int($nowcount/15)*15);
            $tempoutput .= qq~&nbsp;<a href="$thisprog?action=viewletter&letter=$_">$_</a>&nbsp;~;
            $ltr = "$_";
            $nowcount ++;
        }
    }

     
    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2><center>
    <font color=#990000><b>�鿴������ "$inletter" ��ͷ���û�</b><p>
	<form action="setmembers.cgi" method=get>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="���ٶ�λ">
        </form>
    ע���û������б�</center>
    $tempoutput
    </td>
    </tr>          
    <tr>
    <td bgcolor=#FFFFFF align=center colspan=2>
    &nbsp;
    </td>
    </tr>          
    ~;
               
               
    foreach (@sortedfile) {
    	if ($_ =~ /^\w/) {
        $frr = substr($_, 0, 1);
        $frr =~ tr/a-z/A-Z/;
        }
        else {
           $frr =substr($_, 0, 2);
        }
        if ($inletter eq $frr) {
            $_ =~ s/\.cgi$//;
            $member = $_;
            &getmember("$member");
            &showmember;
            }
        }
        
   } # end route



##################################################################################
######## Subroutes (Show member) 


sub showmember {

    $joineddate = &longdate("$joineddate");
    
    $cleanmember = $member;
    $cleanmember =~ s/\_/ /g;
    
    ## Sort last post, and where
    
    ($postdate, $posturl, $posttopic) = split(/\%%%/,$lastpostdate);
    
    if ($postdate ne "û�з����") {
        $postdate = &longdate("$postdate");
        $lastpostdetails = qq~��󷢱� <a href="$posturl">$posttopic</a> �� $postdate~;
        }
        else {
            $lastpostdetails = "û�з����";
            }

    if ($membercode eq "banned") {
        $unbanlink = qq~ | [<a href="$thisprog?action=unban&member=$member">ȡ����ֹ����</a>]~;
        }
    $totlepostandreply = $numberofposts+$numberofreplys;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2 align=center><font face=$font color=$fontcolormisc><b><font color=$fonthighlight>"$cleanmember"</b> ����ϸ���� �� [ <a href="$thisprog?action=edit&member=$member">�༭</a> ] | [ <a href="$thisprog?action=deletemember&member=$member">ɾ��</a> ]$unbanlink</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF width=30%><font color=#333333><b>ע��ʱ�䣺</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ�Σ�</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$membertitle</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��󷢱�</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastpostdetails</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����������</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$totlepostandreply</font> ƪ</td></tr>
    <tr>
    <td bgcolor=#FFFFFF>&nbsp;</td>
    <td bgcolor=#FFFFFF>&nbsp;</td></tr>
    
    ~;
    $unbanlink = "";
    } # end routine


##################################################################################
######## Subroutes (Edit member) 


sub edit {
    $oldmembercode = $membercode;
    
    if ($checkaction eq "yes") {
    
    
    $innewpassword      = $query -> param('password');
    $inrating           = $query -> param('rating');
    $inmembertitle      = $query -> param('membertitle');
    $inemailaddress     = $query -> param('emailaddress');
    $inhomepage         = $query -> param('homepage');
    $inaolname          = $query -> param('aolname');
    $inicqnumber        = $query -> param('icqnumber');
    $inlocation         = $query -> param('location');
    $innumberofposts    = $query -> param('numberofposts');
    $innumberofreplys   = $query -> param('numberofreplys');
    $intimedifference   = $query -> param('timedifference');
    $inmembercode       = $query -> param('membercode');
    $invisitno          = $query -> param('visitno');
    $injhmp             = $query -> param('jhmp');
    $inaddjy            = $query -> param('addjy');
    $inmeili            = $query -> param('meili');
    $inmymoney          = $query -> param('mymoney');
    $insex              = $query -> param('sex');
    $ineducation        = $query -> param('education');
    $inmarry            = $query -> param('marry');
    $inwork             = $query -> param('work');
    $inyear             = $query -> param('year');
    $inmonth            = $query -> param('month');
    $inday              = $query -> param('day');
    $inpostdel          = $query -> param('postdel');
    $inrating           = $query -> param('rating');
    $newsignature       = $query -> param('newsignature');
    $inuserflag         = $query -> param('userflag');
    $inusersx           = $query -> param('usersx');
    $inuserxz           = $query -> param('userxz');
    $injoineddate       = $query -> param('joineddate');

    $inlocation = &cleaninput("$inlocation");

    $inyear =~ s/\D//g;
    if (($inyear eq "")||($inmonth eq "")||($inday eq "")) {
    	$inyear  = "";
    	$inmonth = "";
    	$inday   = "";
    }
    $inborn = "$inyear/$inmonth/$inday";
    
    if ($inborn ne "//") { #��ʼ�Զ��ж�����
        if ($inyear-1900 < 0) {$inusersx = "";}	# ��Ч���
    	else {
    		$inusersx = "sx".(($inyear-1900) % 12 + 1);
    	}
    	if ($inmonth eq "01") {
    	    if (($inday >= 1)&&($inday <=19)) {
    	        $inuserxz = "z10";
    	    }
    	    else {
    	        $inuserxz = "z11";
    	    }
    	}
        elsif ($inmonth eq "02") {
    	    if (($inday >= 1)&&($inday <=18)) {
    	        $inuserxz = "z11";
    	    }
    	    else {
    	        $inuserxz = "z12";
    	    }
        }
        elsif ($inmonth eq "03") {
    	    if (($inday >= 1)&&($inday <=20)) {
    	        $inuserxz = "z12";
    	    }
    	    else {
    	        $inuserxz = "z1";
    	    }

        }
        elsif ($inmonth eq "04") {
    	    if (($inday >= 1)&&($inday <=19)) {
    	        $inuserxz = "z1";
    	    }
    	    else {
    	        $inuserxz = "z2";
    	    }
        }
        elsif ($inmonth eq "05") {
    	    if (($inday >= 1)&&($inday <=20)) {
    	        $inuserxz = "z2";
    	    }
    	    else {
    	        $inuserxz = "z3";
    	    }
        }
        elsif ($inmonth eq "06") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z3";
    	    }
    	    else {
    	        $inuserxz = "z4";
    	    }
        }
        elsif ($inmonth eq "07") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z4";
    	    }
    	    else {
    	        $inuserxz = "z5";
    	    }
        }
        elsif ($inmonth eq "08") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z5";
    	    }
    	    else {
    	        $inuserxz = "z6";
    	    }
        }
        elsif ($inmonth eq "09") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z6";
    	    }
    	    else {
    	        $inuserxz = "z7";
    	    }
        }
        elsif ($inmonth eq "10") {
    	    if (($inday >= 1)&&($inday <=23)) {
    	        $inuserxz = "z7";
    	    }
    	    else {
    	        $inuserxz = "z8";
    	    }
        }
        elsif ($inmonth eq "11") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z8";
    	    }
    	    else {
    	        $inuserxz = "z9";
    	    }
        }
        elsif ($inmonth eq "12") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z9";
    	    }
    	    else {
    	        $inuserxz = "z10";
    	    }
        }
        
    }

    if ($inpassword eq "")     { $blank = "yes"; }
    if ($inemailaddress eq "") { $blank = "yes"; }
    
    if ($blank eq "yes") {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>���������û����롢�ʼ���ַ</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    
    $inmembertitle = "Member" if ($inmembertitle eq "");

    if (length($injhmp) > 20) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>�������ɵ������������20���ַ���10�����֣��ڡ�</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if (length($inmembertitle) > 20) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>����ͷ�ε������������20���ַ���10�����֣��ڡ�</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if (length($inlocation) > 12) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>���Ե������������12���ַ���6�����֣��ڡ�</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if ((($inmembercode eq "ad")||($inmembercode eq "smo")||($inmembercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ܰ�����Ȩ�����κ���Ϊ̳���Ͱ���</b></td></tr>";
            exit;
    }

    if ($injhmp eq "") { $jhmp = "��������"; }
    else { $jhmp = ($jhmp); }
    if ($inrating eq "") { $inrating = 0; }
    elsif ($inrating > $maxweiwang) { $inrating = $maxweiwang; }
    elsif ($inrating < -5) { $inrating = -5; $inmembercode = "banned"; }
        
        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE,"$filetoopen");
        @forums = <FILE>;
        close(FILE);
        
        foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $trash) = split(/\t/,$forum);
            $namekey = "allow" . "$forumid";
            $tocheck = $query -> param("$namekey");
            if ($tocheck eq "yes") {
                $allowedforums2 .= "$forumid=$tocheck&";
                }
            }
            
        &getmember("$inmember");
    
        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;


        if ($inmembercode eq "banned") {
            $filetoopen = "$lbdir" . "data/banemaillist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$inemailaddress\t";
            close(FILE);
            $filetoopen = "$lbdir" . "data/baniplist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$ipaddress\t";
            close(FILE);
            $banresult = "��ֹ $membername ���Գɹ�";
       }


        $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$innewpassword\t$inmembertitle\t$inmembercode\t$innumberofposts|$innumberofreplys\t$inemailaddress\t$showemail\t$ipaddress\t$inhomepage\t$inaolname\t$inicqnumber\t$inlocation\t$interests\t$injoineddate\t$lastpostdate\t$newsignature\t$intimedifference\t$allowedforums2\t$useravatar\t$inuserflag\t$inuserxz\t$inusersx\t$personalavatar\t$personalwidth\t$personalheight\t$inrating\t$lastgone\t$invisitno\t$inaddjy\t$inmeili\t$inmymoney\t$inpostdel\t$insex\t$ineducation\t$inmarry\t$inwork\t$inborn\t$useradd1\t$useradd2\t$injhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

                print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ�����</b><br><br>$banresult<br>
                </td></tr>
                ~;
    
    }
    
    else {
    
    $filetoopen = "$lbdir" . "data/allforums.cgi";
         open(FILE,"$filetoopen");
         @forums = <FILE>;
         close(FILE);

         
         foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $ratings, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $miscadd1, $miscadd2, $miscadd3, $miscadd4, $miscad5) = split(/\t/,$forum);   
            if ($privateforum eq "yes") { 
                $grab = "$forumid\t$forumname";
                push(@newforums, $grab);
                }
            }
        $cleanmember = $inmember;
        $cleanmember =~ s/\_/ /g;
    
        &getmember("$inmember");
        if($privateforums) {
            @private = split(/&/,$privateforums);
            foreach $accessallowed (@private) {
                chomp $accessallowed;
                ($access, $value) = split(/=/,$accessallowed);
                $allowedentry2{$access} = $value;
                }
            }
    
        @allowedforums = sort alphabetically(@newforums);
        foreach $line (@allowedforums) {
            ($forumid, $forumname) = split(/\t/,$line);
            if ($allowedentry2{$forumid} eq "yes") { $checked = " checked"; }
            else { $checked = ""; }
            $privateoutput .= qq~<input type="checkbox" name="allow$forumid" value="yes" $checked>$forumname<br>\n~;
            }
            
    $memberstateoutput = qq~<select name="membercode"><option value="me">һ���û�<option value="rz">��֤�û�<option value="banned">��ֹ���û�����<option value="masked">���δ��û�����<option value="mo">����̳����<option value="smo">��̳�ܰ��� *<option value="ad">̳�� **</select>~;
    
    $memberstateoutput =~ s/value=\"$membercode\"/value=\"$membercode\" selected/g;
        if ($userregistered eq "no") {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�޴��û���</b></td></tr>";
            exit;
        }
    
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ܰ�����Ȩ�鿴̳���Ͱ������ϣ�</b></td></tr>";
            exit;
    }
$userflag = "blank" if ($userflag eq "");
$flaghtml = qq~
<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>���ڹ���:</b></td>
<td bgcolor=#ffffff>
<select name="userflag" size=1 onChange="showflag()">
<option value="blank">����</option>
<option value="China">�й�</option>
<option value="Angola">������</option>
<option value="Antigua">�����</option>
<option value="Argentina">����͢</option>
<option value="Armenia">��������</option>
<option value="Australia">�Ĵ�����</option>
<option value="Austria">�µ���</option>
<option value="Bahamas">�͹���</option>
<option value="Bahrain">����</option>
<option value="Bangladesh">�ϼ���</option>
<option value="Barbados">�ͰͶ�˹</option>
<option value="Belgium">����ʱ</option>
<option value="Bermuda">��Ľ��</option>
<option value="Bolivia">����ά��</option>
<option value="Brazil">����</option>
<option value="Brunei">����</option>
<option value="Canada">���ô�</option>
<option value="Chile">����</option>
<option value="Colombia">���ױ���</option>
<option value="Croatia">���޵���</option>
<option value="Cuba">�Ű�</option>
<option value="Cyprus">����·˹</option>
<option value="Czech_Republic">�ݿ�˹�工��</option>
<option value="Denmark">����</option>
<option value="Dominican_Republic">�������</option>
<option value="Ecuador">��϶��</option>
<option value="Egypt">����</option>
<option value="Estonia">��ɳ����</option>
<option value="Finland">����</option>
<option value="France">����</option>
<option value="Germany">�¹�</option>
<option value="Great_Britain">Ӣ��</option>
<option value="Greece">ϣ��</option>
<option value="Guatemala">Σ������</option>
<option value="Honduras">�鶼��˹</option>
<option value="Hungary">������</option>
<option value="Iceland">����</option>
<option value="India">ӡ��</option>
<option value="Indonesia">ӡ��������</option>
<option value="Iran">����</option>
<option value="Iraq">������</option>
<option value="Ireland">������</option>
<option value="Israel">��ɫ��</option>
<option value="Italy">�����</option>
<option value="Jamaica">�����</option>
<option value="Japan">�ձ�</option>
<option value="Jordan">Լ��</option>
<option value="Kazakstan">������</option>
<option value="Kenya">������</option>
<option value="Kuwait">������</option>
<option value="Latvia">����ά��</option>
<option value="Lebanon">�����</option>
<option value="Lithuania">������</option>
<option value="Malaysia">��������</option>
<option value="Malawi">����ά</option>
<option value="Malta">�����</option>
<option value="Mauritius">ë����˹</option>
<option value="Morocco">Ħ���</option>
<option value="Mozambique">Īɣ�ȿ�</option>
<option value="Netherlands">����</option>
<option value="New_Zealand">������</option>
<option value="Nicaragua">�������</option>
<option value="Nigeria">��������</option>
<option value="Norway">Ų��</option>
<option value="Pakistan">�ͻ�˹̹</option>
<option value="Panama">������</option>
<option value="Paraguay">������</option>
<option value="Peru">��³</option>
<option value="Poland">����</option>
<option value="Portugal">������</option>
<option value="Romania">��������</option>
<option value="Russia">���</option>
<option value="Saudi_Arabia">ɳ�ذ�����</option>
<option value="Singapore">�¼���</option>
<option value="Slovakia">˹�工��</option>
<option value="Slovenia">˹��������</option>
<option value="Solomon_Islands">������</option>
<option value="Somalia">������</option>
<option value="South_Africa">�Ϸ�</option>
<option value="South_Korea">����</option>
<option value="Spain">������</option>
<option value="Sri_Lanka">ӡ��</option>
<option value="Surinam">������</option>
<option value="Sweden">���</option>
<option value="Switzerland">��ʿ</option>
<option value="Thailand">̩��</option>
<option value="Trinidad_Tobago">��͸�</option>
<option value="Turkey">������</option>
<option value="Ukraine">�ڿ���</option>
<option value="United_Arab_Emirates">����������������</option>
<option value="United_States">����</option>
<option value="Uruguay">������</option>
<option value="Venezuela">ί������</option>
<option value="Yugoslavia">��˹����</option>
<option value="Zambia">�ޱ���</option>
<option value="Zimbabwe">��Ͳ�Τ</option>
</select>
<img src="$imagesurl/flags/$userflag.gif" name="userflags" border=0 height=14 width=21>
</td></tr>
~;
$flaghtml =~ s/value=\"$userflag\"/value=\"$userflag\" selected/;

        if ($userxz eq "") {$userxz = "blank"};
        $xzhtml =qq~
        <SCRIPT language=javascript>
        function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>����������</b>��ѡ����������������<br>������������յĻ�����ô������Ч��</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>����</OPTION> <OPTION value=\"z1\">������(3��21--4��19��)</OPTION> <OPTION value=\"z2\">��ţ��(4��20--5��20��)</OPTION> <OPTION value=\"z3\">˫����(5��21--6��21��)</OPTION> <OPTION value=\"z4\">��з��(6��22--7��22��)</OPTION> <OPTION value=\"z5\">ʨ����(7��23--8��22��)</OPTION> <OPTION value=\"z6\">��Ů��(8��23--9��22��)</OPTION> <OPTION value=\"z7\">�����(9��23--10��23��)</OPTION> <OPTION value=\"z8\">��Ы��(10��24--11��21��)</OPTION> <OPTION value=\"z9\">������(11��22--12��21��)</OPTION> <OPTION value=\"z10\">ħ����(12��22--1��19��)</OPTION> <OPTION value=\"z11\">ˮƿ��(1��20--2��18��)</OPTION> <OPTION value=\"z12\">˫����(2��19--3��20��)</OPTION></SELECT> <IMG border=0 height=15 name=userxzs src=$imagesurl/star/$userxz.gif width=15 align=absmiddle>
        </TD></TR>
	~;
        $xzhtml =~ s/value=\"$userxz\"/value=\"$userxz\" selected/;

        if ($usersx eq "") {$usersx = "blank"};
        $sxhtml =qq~
        <SCRIPT language=javascript>
        function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>������Ф��</b>��ѡ������������Ф��<br>������������յĻ�����ô������Ч��</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>����</OPTION> <OPTION value=\"sx1\">����</OPTION> <OPTION value=\"sx2\">��ţ</OPTION> <OPTION value=\"sx3\">����</OPTION> <OPTION value=\"sx4\">î��</OPTION> <OPTION value=\"sx5\">����</OPTION> <OPTION value=\"sx6\">����</OPTION> <OPTION value=\"sx7\">����</OPTION> <OPTION value=\"sx8\">δ��</OPTION> <OPTION value=\"sx9\">���</OPTION> <OPTION value=\"sx10\">����</OPTION> <OPTION value=\"sx11\">�繷</OPTION> <OPTION value=\"sx12\">����</OPTION></SELECT> <IMG border=0 name=usersxs src=$imagesurl/sx/$usersx.gif align=absmiddle>
        </TD></TR>
	~;
        $sxhtml =~ s/value=\"$usersx\"/value=\"$usersx\" selected/;
        if ($avatars eq "on") {
	    if (($personalavatar)&&($personalwidth)&&($personalheight)) { #�Զ���ͷ�����
	        if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	            $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>��[ <a href="$thisprog?action=deleteavatar&member=$inmember">ɾ �� ͷ ��</a> ]);
	        }
	        else {
	            $useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>��[ <a href="$thisprog?action=deleteavatar&member=$inmember">ɾ �� ͷ ��</a> ]);
	        }
	    }
            elsif (($useravatar ne "noavatar") && ($useravatar)) {
                $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$useravatar.gif" border=0 $defaultwidth $defaultheight>);
            }
            else {$useravatar="û��"; }
        }

  if ($oldmembercode eq "ad") {
    print qq~
    <form action="$thisprog" method=post name="creator">
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>Ҫ�༭���û����ƣ� </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ�Σ�</b><br>�������Զ���һ��ͷ�Σ�<br>Ĭ�� Member ��ʾ��ͷ��</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����������</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofposts" value="$numberofposts"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�ظ�������</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofreplys" value="$numberofreplys"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���ӱ�ɾ������</b></td>
    <td bgcolor=#FFFFFF><input type=text name="postdel" value="$postdel"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���룺</b></td>
    <td bgcolor=#FFFFFF><input type=password name="password" value="$password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�ʼ���ַ/MSN��ַ��</b></td>
    <td bgcolor=#FFFFFF><input type=text name="emailaddress" value="$emailaddress"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��ҳ��ַ��</b></td>
    <td bgcolor=#FFFFFF><input type=text name="homepage" value="$homepage"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>OICQ �ţ�</b></td>
    <td bgcolor=#FFFFFF><input type=text name="aolname" value="$aolname"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ICQ �ţ�</b></td>
    <td bgcolor=#FFFFFF><input type=text name="icqnumber" value="$icqnumber"></td>
    </tr>$flaghtml<tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���Ժη���</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="location" value="$location" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��������:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��������:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 �� $maxweiwang ֮��)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���⾭�飺</b></td>
    <td bgcolor=#FFFFFF><input type=text name="addjy" value="$addjy" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����������</b></td>
    <td bgcolor=#FFFFFF><input type=text name="meili" value="$meili" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����ǩ����</b></td>
    <td bgcolor=#FFFFFF><textarea name="newsignature" cols="60" rows="8">$signature</textarea></td>
    </tr><tr>
	~;

        $tempoutput = "<select name=\"sex\" size=\"1\"><option value=\"no\">���� </option><option value=\"m\">˧�� </option><option value=\"f\">��Ů </option></select>\n";
        $tempoutput =~ s/value=\"$sex\"/value=\"$sex\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>�Ա�</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"education\" size=\"1\"><option value=\"����\">���� </option><option value=\"Сѧ\">Сѧ </option><option value=\"����\">���� </option><option value=\"����\">����</option><option value=\"��ר\">��ר</option><option value=\"��ר\">��ר</option><option value=\"����\">����</option><option value=\"˶ʿ\">˶ʿ</option><option value=\"��ʿ\">��ʿ</option><option value=\"��ʿ��\">��ʿ��</option></select>\n";
        $tempoutput =~ s/value=\"$education\"/value=\"$education\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>���ѧ����</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"marry\" size=\"1\"><option value=\"����\">���� </option><option value=\"δ��\">δ�� </option><option value=\"�ѻ�\">�ѻ� </option><option value=\"���\">��� </option><option value=\"ɥż\">ɥż </option></select>\n";
        $tempoutput =~ s/value=\"$marry\"/value=\"$marry\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>����״����</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"work\" size=\"1\"><option value=\"����\">���� </option><option value=\"�����ҵ\">�����ҵ </option><option value=\"����ҵ\">����ҵ </option><option value=\"��ҵ\">��ҵ </option><option value=\"������ҵ\">������ҵ </option><option value=\"����ҵ\">����ҵ </option><option value=\"ѧ��\">ѧ�� </option><option value=\"����ʦ\">����ʦ </option><option value=\"���ܣ�����\">���ܣ����� </option><option value=\"��������\">�������� </option><option value=\"����ҵ\">����ҵ </option><option value=\"����/���/�г�\">����/���/�г� </option><option value=\"ʧҵ��\">ʧҵ�� </option></select>\n";
        $tempoutput =~ s/value=\"$work\"/value=\"$work\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>ְҵ״����</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;
	($year, $month, $day) = split(/\//, $born);
        $tempoutput1 = "<select name=\"month\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option></select>\n";
        $tempoutput1 =~ s/value=\"$month\"/value=\"$month\" selected/;

        $tempoutput2 = "<select name=\"day\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option><option value=\"13\">13</option><option value=\"14\">14</option><option value=\"15\">15</option><option value=\"16\">16</option><option value=\"17\">17</option><option value=\"18\">18</option><option value=\"19\">19</option><option value=\"20\">20</option><option value=\"21\">21</option><option value=\"22\">22</option><option value=\"23\">23</option><option value=\"24\">24</option><option value=\"25\">25</option><option value=\"26\">26</option><option value=\"27\">27</option><option value=\"28\">28</option><option value=\"29\">29</option><option value=\"30\">30</option><option value=\"31\">31</option></select>\n";
        $tempoutput2 =~ s/value=\"$day\"/value=\"$day\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>���գ�</b>�粻����д����ȫ�����ա�</td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><input type="text" name="year" size=4 maxlength=4 value="$year">��$tempoutput1��$tempoutput2��</font></td>
	</tr>$xzhtml
        </tr>$sxhtml
	~;
	
    print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>�����Ǯ��</b></td>
    <td bgcolor=#FFFFFF><input type=text name="mymoney" value="$mymoney" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���ʴ�����</b></td>
    <td bgcolor=#FFFFFF><input type=text name="visitno" value="$visitno" maxlength=7></td>
    </tr><tr>
    ~;
   $timedifference = 0 if ($timedifference eq '');
   $tempoutput = "<select name=\"timedifference\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
   $tempoutput =~ s/value=\"$timedifference\"/value=\"$timedifference\" selected/;
   $joineddate = $lastgone if ($joineddate eq "");
   $joineddate1 = $joineddate;
   $joineddate = &dateformat($joineddate);
   if ($lastgone ne "") {$lastgone   = &dateformat($lastgone); } else {$lastgone = $joineddate; }
   print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>ʱ�</b></td>
    <td bgcolor=#FFFFFF>$tempoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>˽����̳����Ȩ�ޣ�</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û����ͣ�</b><br>ע�⣺̳��Ϊ��̳����Ա���о��Ըߵ�Ȩ�ޡ�<br>�����������Ӵ����͵��û���<br>�ܰ������κ���̳�����а���Ȩ�ޣ�<br>�ڹ�������ֻ��һ��Ȩ�ޡ�</td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ע��ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ע��ʱ�� IP ��ַ��</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$ipaddress</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>������ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ��</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <input type=hidden name="joineddate" value="$joineddate1">
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmember">ɾ �� �� �� ��</a> ]</td>
    </tr>
    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="�� ��" name=submit></form></td>
    </tr>
    ~;
  }
  else {
    $memberstateoutput = qq~<select name="membercode"><option value="me">һ���û�<option value="rz">��֤�û�<option value="banned">��ֹ���û�����<option value="masked">���δ��û�����</select>~;
    $memberstateoutput =~ s/value=\"$membercode\"/value=\"$membercode\" selected/g;
    ($year, $month, $day) = split(/\//, $born);
    if ($lastgone ne "") {$lastgone   = &dateformat($lastgone); } else {$lastgone = $joineddate; }
    $joineddate = $lastgone if ($joineddate eq "");
    print qq~
    <form action="$thisprog" method=post>
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <input type=hidden name="numberofposts" value="$numberofposts">
    <input type=hidden name="numberofreplys" value="$numberofreplys">
    <input type=hidden name="postdel" value="$postdel">
    <input type=hidden name="emailaddress" value="$emailaddress">
    <input type=hidden name="homepage" value="$homepage">
    <input type=hidden name="aolname" value="$aolname">
    <input type=hidden name="icqnumber" value="$icqnumber">
    <input type=hidden name="location" value="$location">
    <input type=hidden name="newsignature" value="$signature">
    <input type=hidden name="sex" value="$sex">
    <input type=hidden name="education" value="$education">
    <input type=hidden name="marry" value="$marry">
    <input type=hidden name="work" value="$work">
    <input type=hidden name="month" value="$month">
    <input type=hidden name="day" value="$day">
    <input type=hidden name="year" value="$year">
    <input type=hidden name="visitno" value="$visitno">
    <input type=hidden name="joineddate" value="$joineddate">
    <input type=hidden name="userflag" value="$userflag">
    <input type=hidden name="usersx" value="$usersx">
    <input type=hidden name="userxz" value="$userxz">
    <input type=hidden name="timedifference" value="$timedifference">

    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>Ҫ�༭���û����ƣ� </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ�Σ�</b><br>�������Զ���һ��ͷ�Σ�<br>Ĭ�� Member ��ʾ��ͷ��</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���룺</b></td>
    <td bgcolor=#FFFFFF><input type=password name="password" value="$password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��������:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��������:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 �� $maxweiwang ֮��)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���⾭�飺</b></td>
    <td bgcolor=#FFFFFF><input type=text name="addjy" value="$addjy" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����������</b></td>
    <td bgcolor=#FFFFFF><input type=text name="meili" value="$meili" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�����Ǯ��</b></td>
    <td bgcolor=#FFFFFF><input type=text name="mymoney" value="$mymoney" maxlength=12></td>
    </tr><tr>
    ~;
   $joineddate = &dateformat($joineddate);
   print qq~
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>˽����̳����Ȩ�ޣ�</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û����ͣ�</b></td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ע��ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ע��ʱ�� IP ��ַ��</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$ipaddress</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>������ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ��</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmember">ɾ �� �� �� ��</a> ]</td>
    </tr>

    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="�� ��" name=submit></form></td>
    </tr>
    ~;
  	
  }  
 } # end else
    
} # endroute


############### delete member

sub deletemember {

    $oldmembercode = $membercode;
    &getmember("$inmember");
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ܰ�����Ȩɾ��̳���Ͱ������ϣ�</b></td></tr>";
            exit;
    }
    if ($inmembername eq $inmember) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�Լ�����ɾ���Լ�������Ӵ��</b></td></tr>";
            exit;
    }

if ($checkaction eq "yes") {
####################################################
    # Check to see if they were the last member to register

    require "$lbdir" . "data/boardstats.cgi";
        
    if($inmember eq "$lastregisteredmember") { #start

        $dirtoopen = "$lbdir" . "$memdir";
        opendir (DIR, "$dirtoopen"); 
        @filedata = readdir(DIR);
        closedir (DIR);
        @inmembers = grep(/cgi$/i,@filedata);

        local($highest) = 0;

        foreach (@inmembers) {
            $_ =~ s/\.cgi$//g;
            &getmember("$_");
            if (($joineddate > $highest) && ($inmember ne $membername)) {
                $highest = $joineddate;
                $memberkeep = $membername;
                }
        }
        
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers--;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$memberkeep\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        } # end if new/delete member

    else {
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers--;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        } # end if else

        # Delete the database for the member

        $filetounlink = "$lbdir" . "$memdir/$inmember.cgi";
        unlink $filetounlink;

        $filetounlink = "$lbdir" . "$msgdir/in/$inmember" . "_msg.cgi";
        unlink $filetounlink;
        $filetounlink = "$lbdir" . "$msgdir/out/$inmember" . "_out.cgi";
        unlink $filetounlink;
        $filetounlink = "$lbdir" . "$msgdir/main/$inmember" . "_mian.cgi";
       	unlink $filetounlink;

        $filetounlink = "$lbdir" . "memfav/$inmember.cgi";
        unlink $filetounlink;
        $filetounlink = "$lbdir" . "memfriend/$inmember.cgi";
        unlink $filetounlink;
    	unlink ("${imagesdir}usravatars/$inmember.gif");
    	unlink ("${imagesdir}usravatars/$inmember.png");
    	unlink ("${imagesdir}usravatars/$inmember.jpg");
    	unlink ("${imagesdir}usravatars/$inmember.swf");
    	unlink ("${imagesdir}usravatars/$inmember.bmp");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>�û��Ѿ������ݿ�����ȫɾ����</b>
        </td></tr>
         ~;


} # end checkaction else

else {

        $cleanedmember = $inmember;
        $cleanedmember =~ s/\_/ /g;

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>ֻ�е����������Ӳſ���ɾ���û�<b>"$cleanedmember"</b><p>
        >> <a href="$thisprog?action=deletemember&checkaction=yes&member=$inmember">ɾ���û�</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
        }

} # end routine

sub unban {

        &getmember("$inmember");
    
        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;

        # Remove from ban lists
            
        $filetoopen = "$lbdir" . "data/banlist.cgi";
        open(FILE,"$filetoopen");
        @bandata = <FILE>;
        close(FILE);

        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE,">$filetoopen");
        flock (FILE, 2) if ($OS_USED eq "Unix");
        foreach (@bandata) {
            chomp $_;
            ($bannedname, $bannedemail) = split(/\t/,$_);
            $bannedname =~ s/\_/ /g;
            unless ($bannedname eq $membername) { print FILE "$_\n"; }
            }
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
            

        $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$password\t$membertitle\tme\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$aolname\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$allowedforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$addjy\t$meili\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$useradd1\t$useradd2\t$jhmp\t$useradd3\t$useradd4\t$useradd5\t$useradd6\t$useradd7\t$useradd8\t";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$membername �Ѿ�ȡ����ֹ����</b>
        </td></tr>
        ~;

} # end route


print qq~</td></tr></table></body></html>~;
exit;
