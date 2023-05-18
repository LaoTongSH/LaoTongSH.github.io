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
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "lb.lib.pl";
$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################
$thisprog = "setmemberbak.cgi";

$query = new LBCGI;

$action          = $query -> param('action');
$action          = &unHTML("$action");
$checkaction     = $query -> param('checkaction');
$member          = $query -> param('member');
$member          = &unHTML("$member");
$noofone         = $query -> param('noofone');
$noofone         = &unHTML("$noofone");
$beginone        = $query -> param('beginone');
$beginone        = &unHTML("$beginone");
$totolerepire    = $query -> param('totolerepire');
$totolerepire    = &unHTML("$totolerepire");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");

$noofone      = 2000 if ($noofone !~ /^[0-9]+$/);
$beginone     = 0 if ($beginone !~ /^[0-9]+$/);
$totolerepire = 0 if ($totolerepire !~ /^[0-9]+$/);

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
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#333333" colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / �û��ⱸ�ݼ���ԭ</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'backup'             =>    \&backup,
            'backupnext'         =>    \&backupnext,
            'repire'             =>    \&repire,
            'repirenext'         =>    \&repirenext,
            'repireone'          =>    \&repireone,
            'restore'            =>    \&restore,
            'restorenext'        =>    \&restorenext
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
        

##################################################################################
######## Subroutes (forum list)


sub memberoptions {

    $backupfile = "$lbdir" . "$backupdir/alluser.pl";
    if (-e $backupfile) {
           $last_backup = (stat("$backupfile"))[9];
           $longdatebackup  = &longdate("$last_backup");
           $shorttimebackup = &shorttime("$last_backup");
           $last_backup = "$longdatebackup $shorttimebackup";
           $bakuptrue = 0;
    }
    else {
           $last_backup = "�û��ⱸ���ļ�û���ҵ�������û�б��ݹ�";
           $bakuptrue = 1;
    }   
     
    print qq~
     
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>��ѡ��һ��</b>
    </td>
    </tr>          
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2><UL>
    <font color=#333333><BR>�û��ⱸ���ļ�·���� <B>$backupfile</B><BR>�û�����󱸷����ڣ� <B>$last_backup</B><BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=backup">�����û����ݿ�</a></b><br>
    ���Է�ֹ�û������ƻ���Ҳ���Է���ת���û������ݡ�<BR>ע�⣺����ʱʱ���ݣ�һ��ÿ 3 - 5 �ձ���һ��Ϊ�ˡ�<BR><BR>
    </td>
    </tr>
    ~;
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=restore">��ԭ�û����ݿ�</a></b>��<font color=#990000>(Ϊ�˰�ȫ�����̳�� $inmembername ���ϲ��ỹԭ)</font><br>
    ת���û������ݺ󣬻����û����ݱ��ƻ����Ϳ���ʹ�ô˹��ܰѱ��ݵ��û�������ȫ����ԭ��<BR>
    ע�⣺�Ա���֮����û����и������ݽ�<font color=#990000><B>ȫ����ʧ</B></font>��������ʹ�á�<BR><BR>
    </td>
    </tr>
    ~ if ($bakuptrue == 0);

    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=repire">���ñ����û����޸���ʧ���û�</a></b><br>
    ���������⵼�²��ֵ��û������ƻ����Ϳ����ô˹��ָܻ���<BR>�������û����ϲ��ᱻ��ԭ��ֻ��ԭ���ƻ��˵��û�����<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>��ԭ����ָ���û�������</b><br>
    ���������⵼��ĳ���û������ݱ��ƻ���������Ҫ��ԭĳ���û������ϣ��Ϳ����ô˹��ܡ�<BR>
	<form action="setmemberbak.cgi" method=get>
        <input type=hidden name="action" value="repireone">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="�ָ����û�������">
        </form>
    <BR><BR>
    </td>
    </tr>
    ~;
}

sub backup {

    $dirtoopen = "$lbdir" . "$memdir";

    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @countvar = grep(/\.cgi$/,@filedata);
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
                    
        <b>�û��ⱸ��</b><br>
                    
        <font color=#333333><B>��ǰ���� $totaluserdata ��ע���û���׼�������Ѿ���ɡ�</b><BR><BR><BR>
	<form action="setmemberbak.cgi" method=get>
        <input type=hidden name="action" value="backupnext">����ÿ�α��ݵ��û��� 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="��ʼ����">
        </form>
	Ϊ�˼�����Դռ�ã�������ÿ�α��ݵ��û�����Ĭ�� 2000��<BR>һ�㲻Ҫ���� 3000��������ֱ����޷�������ɣ��뾡�����������Ŀ���ӳ�����ʱ�䡣
	<BR><BR>

        </td></tr>
         ~;
         
     } # end routine

sub backupnext {
    $dirtoopen = "$lbdir" . "$memdir";
    $filename = "alluser.pl";
    open(FILE,"${lbdir}$backupdir/allname.cgi");
    @allname = <FILE>;
    close(FILE);
    $allnamenum = @allname;
    if ($beginone < $allnamenum) {
        $lastone = $beginone + $noofone;
        $lastone = $allnamenum if ($lastone > $allnamenum);
    
        unlink ("${lbdir}$backupdir/$filename") if ($beginone == 0);
        open(FILE,">>${lbdir}$backupdir/$filename");
            print FILE "nodisplay.cgi\t11111\tnodisplay\t11111\tnodisplay\t11111\tnodisplay\t11111\tnodisplay\t11111\tnodisplay\t11111\tnodisplay\t11111\t\n" if ($beginone == 0);
	    for ($i = $beginone; $i < $lastone; $i ++) {
		chomp $allname[$i];
		$filesname="$dirtoopen/$allname[$i]";
		open(FILE1,"$filesname"); 
		$userinfo=<FILE1>;
		close(FILE1);
		chomp $userinfo;
		$allname[$i] =~ tr/A-Z/a-z/;
		print FILE "$allname[$i]\t$userinfo\n";
	    }
        close(FILE); 

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��ⱸ��</b><br>
                    
        <font color=#333333><B>��ǰ���� $allnamenum ��ע���û����Ѿ������� $lastone ���û�������</b><BR><BR><BR>
        <font color=#333333>����޷��Զ���ʼ�� $noofone ���û��ı��ݣ�������������Ӽ���<p>
        >> <a href="$thisprog?action=backupnext&beginone=$lastone&noofone=$noofone">���������û���</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=backupnext&beginone=$lastone&noofone=$noofone">
	<BR><BR>

        </td></tr>
         ~;
     }
     else {

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��ⱸ��</b><p>
                    
        <font color=#333333>��ǰ���� $allnamenum ��ע���û��������Ѿ����ݽ�����<BR><BR>
        ���ݵ��û������� LB5000 �ı���ר��Ŀ¼�£�cgi-bin �µ� backup Ŀ¼����<BR>����·��Ϊ</font> ${lbdir}$backupdir/$filename<font color=#333333> ��<BR>Ϊ�˰�ȫ��������������� ftp ���ر��档</font>                    
        </td></tr>
         ~;
     }
}

sub restore {
    if (-e "${lbdir}$backupdir/alluser.pl") {
        if (-e "${lbdir}$backupdir/allname.cgi") {
          open(FILE,"${lbdir}$backupdir/allname.cgi");
          @allname = <FILE>;
          close(FILE);
          $allname = @allname;
        }
        else {
          open(FILE,"${lbdir}$backupdir/alluser.pl");
          @allname = <FILE>;
          close(FILE);
          $allname = @allname;
          $allname --;
        }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��⻹ԭ</b><br>
                    
        <font color=#333333><B>��ǰ���� $allname ��ע���û���׼�������Ѿ���ɡ�</b><BR><BR><BR>
	<form action="setmemberbak.cgi" method=get>
        <input type=hidden name="action" value="restorenext">����ÿ�λ�ԭ���û��� 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="��ʼ��ԭ">
        </form>
	Ϊ�˼�����Դռ�ã�������ÿ�λ�ԭ���û�����Ĭ�� 2000��<BR>һ�㲻Ҫ���� 3000��������ֻ�ԭ�޷�������ɣ��뾡�����������Ŀ���ӳ���ԭʱ�䡣
	<BR><BR>

        </td></tr>
         ~;
     }
     else {
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��ⱸ���ļ�û���ҵ�</b><p>
     	~;
     }
}

sub restorenext {
    $memberfiletitle = $inmembername;
    $memberfiletitle =~ y/ /_/;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitle .= ".cgi";
    $dirtoopen = "$lbdir" . "$memdir";
    $filename = "alluser.pl";
    open(FILE,"${lbdir}$backupdir/$filename");
    @alluser = <FILE>;
    close(FILE);
    $allusernum = @alluser;
    if ($beginone < $allusernum) {
        $lastone = $beginone + $noofone;
        $lastone = $allusernum if ($lastone > $allusernum);

        for ($i = $beginone; $i < $lastone; $i ++) {
	    chomp $alluser[$i];
    	    next if ($alluser[$i] =~ /^nodisplay\.cgi/);
    	    ($userfilename,@userinfo) = split(/\t/,$alluser[$i]);
    	    next if ($userfilename eq "");
    	    $userinfo = join("\t",@userinfo);
    	    next if ($userinfo eq "");
    	    if ($memberfiletitle ne $userfilename) {
    	        if (open (FILE, ">$dirtoopen/$userfilename")) {
        	  flock(FILE, 2) if ($OS_USED eq "Unix");
    	          print FILE "$userinfo\n";
    	          close(FILE);
    	        }
    	    }
	}

        $allusernum --;
        $lastone --;
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��ⱸ��</b><br>
                    
        <font color=#333333><B>��ǰ���� $allusernum ��ע���û����Ѿ���ԭ�� $lastone ���û�������</b><BR><BR><BR>
        <font color=#333333>����޷��Զ���ʼ�� $noofone ���û��Ļ�ԭ��������������Ӽ���<p>
        >> <a href="$thisprog?action=restorenext&beginone=$lastone&noofone=$noofone">������ԭ�û���</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=restorenext&beginone=$lastone&noofone=$noofone">
	<BR><BR>

        </td></tr>
         ~;
     }
     else {
	$allusernum --;
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��⻹ԭ</b><p>
                    
        <font color=#333333>�û������Ѿ���ԭ(̳�� $inmembername ����δ����)���û����ݿ��й��� $allusernum ��ע���û���<BR><BR>
        </td></tr>
         ~;
     }
}

sub repire {
    if (-e "${lbdir}$backupdir/alluser.pl") {
        if (-e "${lbdir}$backupdir/allname.cgi") {
          open(FILE,"${lbdir}$backupdir/allname.cgi");
          @allname = <FILE>;
          close(FILE);
          $allname = @allname;
        }
        else {
          open(FILE,"${lbdir}$backupdir/alluser.pl");
          @allname = <FILE>;
          close(FILE);
          $allname = @allname;
          $allname --;
        }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��⻹ԭ</b><br>
                    
        <font color=#333333><B>��ǰ���� $allname ��ע���û���׼�������Ѿ���ɡ�</b><BR><BR><BR>
	<form action="setmemberbak.cgi" method=get>
        <input type=hidden name="action" value="repirenext">����ÿ�μ���޸����û��� 
        <input type=hidden name="beginone" value=0>
        <input type=hidden name="totolerepire" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="��ʼ����޸�">
        </form>
	Ϊ�˼�����Դռ�ã�������ÿ�μ���޸����û�����Ĭ�� 2000��<BR>һ�㲻Ҫ���� 3000��������ּ���޸��޷�������ɣ��뾡�����������Ŀ���ӳ�����޸�ʱ�䡣
	<BR><BR>

        </td></tr>
         ~;
     }
     else {
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��ⱸ���ļ�û���ҵ�</b><p>
     	~;
     }
}

sub repirenext {
    $memberfiletitle = $inmembername;
    $memberfiletitle =~ y/ /_/;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitle .= ".cgi";
    $dirtoopen = "$lbdir" . "$memdir";
    $filename = "alluser.pl";
    open(FILE,"${lbdir}$backupdir/$filename");
    @alluser = <FILE>;
    close(FILE);
    $allusernum = @alluser;
    if ($beginone < $allusernum) {
        $lastone = $beginone + $noofone;
        $lastone = $allusernum if ($lastone > $allusernum);

        for ($i = $beginone; $i < $lastone; $i ++) {
	    chomp $alluser[$i];
    	    next if ($alluser[$i] =~ /^nodisplay\.cgi/);
    	    ($userfilename,@userinfo) = split(/\t/,$alluser[$i]);
    	    next if ($userfilename eq "");
    	    $userinfo = join("\t",@userinfo);
    	    next if ($userinfo eq "");
    	    if ($memberfiletitle ne $userfilename) {
    	        open (FILE, "$dirtoopen/$userfilename");
    	        $userdatanow = <FILE>;
    	        close(FILE);
		chomp $userdatanow;

		($membername1, $password1, $no) = split(/\t/,$userdatanow);
		if (($membername1 eq "")||($password1 eq "")) {
    	            if (open (FILE, ">$dirtoopen/$userfilename")) {
    	              print FILE "$userinfo\n";
    	              close(FILE);
    	            }
    	            $totolerepire ++;
    	        }
    	    }
	}

        $allusernum --;
        if ($lastone > $allusernum) {
        	$lastone1 = $allusernum;
        }
        else {
        	$lastone1 = $lastone;
        }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��ⱸ��</b><br>
                    
        <font color=#333333><B>��ǰ���� $allusernum ��ע���û����Ѿ������ $lastone1 ���û����޸��� $totolerepire ���û� ������</b><BR><BR><BR>
        <font color=#333333>����޷��Զ���ʼ�� $noofone ���û��ļ�飬������������Ӽ���<p>
        >> <a href="$thisprog?action=repirenext&beginone=$lastone&noofone=$noofone&totolerepire=$totolerepire">�����޸��û���</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=repirenext&beginone=$lastone&noofone=$noofone&totolerepire=$totolerepire">
	<BR><BR>

        </td></tr>
         ~;
     }
     else {
	$allusernum --;
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ԭ���ݱ��ƻ����û�</b><p>
                    
        <font color=#333333>$totolerepire �����ݱ��ƻ����û��Ѿ���ԭ��Ŀǰ�û����ݿ��й��� $allusernum ��ע���û���<BR><BR>
        </td></tr>
         ~;
     }
}

sub repireone {
    if ($checkaction eq "yes") {

        $memberfilename = $member;
        $memberfilename =~ y/ /_/;
        $memberfilename =~ tr/A-Z/a-z/;
	$memberfilename .= ".cgi";

    if (-e "${lbdir}$backupdir/alluser.pl") {
    	$dirtoopen = "$lbdir" . "$memdir";
    	
	$filename = "alluser.pl";
	open(FILE,"${lbdir}$backupdir/$filename");
	@totlename = <FILE>;
	close(FILE); 
    	$totaluserdata = @totlename;
	$repireuser = 0;
	
    	foreach $data (@totlename) {
    	    chomp $data;
    	    next if ($data eq "");
    	    next if ($data =~ /^nodisplay.cgi/);
    	    ($userfilename,@userinfo) = split(/\t/,$data);
    	    next if ($userfilename eq "");
    	    $userinfo = join("\t",@userinfo);
    	    next if ($userinfo eq "");
    	    if ($memberfilename eq $userfilename) {
    	        open (FILE, ">$dirtoopen/$userfilename");
    	        print FILE "$userinfo\n";
    	        close(FILE);
    	        $repireuser = 1;
    	    }
	}
      $totaluserdata --;
      if ($repireuser eq 1) {
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ԭ���ݱ��ƻ����û�</b><p>
                    
        <font color=#333333>�û� $member �������Ѿ���ԭ��Ŀǰ�û����ݿ��й��� $totaluserdata ��ע���û���<BR><BR>
        </td></tr>
         ~;
      }
      else {
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>��ԭ���ݱ��ƻ����û�</b><p>
                    
        <font color=#333333>�û����ݿ���û���û� $member �����ϣ�Ŀǰ�û����ݿ��й��� $totaluserdata ��ע���û���<BR><BR>
        </td></tr>
         ~;
      }
     }
     else {
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>�û��ⱸ���ļ�û���ҵ�</b><p>
     	~;
     }
  }
  else {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>ֻ�е����������Ӳſ��Ի�ԭ $member �û�������<p>
        >> <a href="$thisprog?action=repireone&member=$member&checkaction=yes">ȷ����ԭ���û�������</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
  }

}

print qq~</td></tr></table></body></html>~;
exit;
