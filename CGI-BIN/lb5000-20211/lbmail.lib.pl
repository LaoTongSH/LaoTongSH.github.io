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
#            http://maildo.com/      ���һ����
#            
#############################################################

sub sendmail {
#   if ($emailtype eq "send_mail") { $SMTP_SERVER = ""; }
#   if (($emailtype eq "smtp_mail")||($emailtype eq "esmtp_mail")) { $SEND_MAIL = ""; }
 my ($fromaddr, $replyaddr, $to, $smtp, $subject, $message) = @_;
 $to =~ s/\\//g;
 $to =~ s/\,/\, /g;
 $to =~ s/[ \t]+/ /g;
 $to =~ s/ \,/\,/g;
 $to =~ s/\, $//g;
 $to =~ s/ $//g;
 if ($to ne "") {
   $fromaddr =~ s/.*<([^\s]*?)>/$1/;
   $replyaddr =~ s/.*<([^\s]*?)>/$1/;
   $replyaddr =~ s/^([^\s]+).*/$1/;
   $message.= "\nLB5000 ��̳������֧�֣�http://www.leoBBS.com/\n";
   $message.= "���İ�Ȩ��CGI �����֮��  http://www.CGIer.com/\n";
   if ($emailtype eq "blat_mail") {
        $tempfile = "$lbdir" . "tempfile.txt";
        open(FILE,">$tempfile");
        print FILE "$message";
        close(FILE);
        my @to1 = split (/\, /,$to);
	foreach $to (@to1) {
            open(MAIL,"|blat $tempfile -t \'$to\' -b \'$bccinfo\' -i \'$fromaddr\' -f \'$fromaddr\' -s \"$subject\"");
            close(MAIL);
        }
        unlink ("$tempfile");
   }
   elsif ($emailtype eq "sendmail") {
        my @to1 = split (/\, /,$to);
	foreach $to (@to1) {
	    open (MAIL,"| $SEND_MAIL -t");
	    print MAIL qq~To: $to\n~;
	    print MAIL qq~From: $fromaddr\n~;
	    print MAIL qq~Reply-to: $replyaddr\n~ if $replyaddr;
	    print MAIL "X-Mailer: LeoBoard Sendmail Mail Sender!\n";
	    print MAIL "Subject: $subject\n\n";
	    print MAIL "$message";
	    print MAIL "\n.";
	    close(MAIL);
	}
   }
   else {
	$smtp =~ s/^\s+//g;
	$smtp =~ s/\s+$//g;
	$SMTP_PORT = 25 if (($SMTP_PORT !~ /^\d+$/)||($SMTP_PORT eq ""));

     if ($emailtype eq "smtp_mail") {
	if ($smtp ne "") {
	  eval {
	    ($0 =~ m,(.*)/[^/]+,)   and unshift (@INC, "$1");
	    ($0 =~ m,(.*)\\[^\\]+,) and unshift (@INC, "$1");
    	     require "SendMail.pm.pl";
	  };
	  eval("use MIME::Base64;");
	  eval("use MIME::QuotedPrint;");

	  my($sender)   = $fromaddr;
	  my($subject)  = $subject;
	  my(@recipient) = split (/\, /,$to);
	  my $last = pop(@recipient);
	  my $renum = @recipient;
	  
	  my($sm) = new SendMail($smtp, $SMTP_PORT);
	  $sm->From($sender);
	  $sm->To($last);
  	  $sm->Bcc(@recipients) if ($renum > 0);
	  $sm->ReplyTo($replyaddr) if $replyaddr;
	  $sm->Subject($subject);
	  $sm->setMailHeader("URL", "http://www.CGIer.com");
	  $sm->setMailBody($message);
	  if ($sm->sendMail() != 0) {
	     return(1);
	  }
	}
     }
     if ($emailtype eq "esmtp_mail") {
	if ($smtp ne "") {
	   $message =~ s/\n/\r/isg;
	   &smtpmail($to, $fromaddr, $subject, $message, $smtp);
	}
     }
   }
 }
}

sub smtpmail    #�����ʼ��ĺ���
{
use Socket;
    my ($address, $from, $subject, $body,$smtp) = @_;

	$smtp =~ s/^\s+//g;
	$smtp =~ s/\s+$//g;
	$SMTP_PORT = 25 if (($SMTP_PORT !~ /^\d+$/)||($SMTP_PORT eq ""));

    my ($a, $i, $name, $aliases, $proto, $type, $len, $thataddr);
    my @to = split(/, /, $address);

    #�Ե�ַ���н���
    my $AF_INET = 2;
    my $SOCK_STREAM = 1;
    my $SOCKADDR = 'S n a4 x8';

    ($name, $aliases, $proto) = getprotobyname('tcp');
    ($name, $aliases, $SMTP_PORT) = getservbyname($SMTP_PORT, 'tcp') unless ($SMTP_PORT =~ /^\d+$/);
    ($name, $aliases, $type, $len, $thataddr) = gethostbyname($smtp);
    my $this = pack($SOCKADDR, $AF_INET, 0, $thisaddr);
    my $that = pack($SOCKADDR, $AF_INET, $SMTP_PORT, $thataddr);

    #��ESMTP��socket�˿�
    socket(S, $AF_INET, $SOCK_STREAM, $proto);
    bind(S, $this);
    connect(S, $that);

    select(S);
    $| = 1;
    select(STDOUT);
    $a = <S>;
    if ($a !~ /^2/)
    {
        close(S);
        undef $|;
        return 0;
    }

    #����ESMTP�����֤
    print S "EHLO localhost\n";
    $a = <S>;
    print S "AUTH LOGIN\n";
    $a = <S>;
    my $encode_smtpuser = Base64encode($SMTPUSER);    #������֤���û������뾭��Base64�������������
    print S "$encode_smtpuser\n";
    $a = <S>;
    my $encode_smtppass = Base64encode($SMTPPASS);    #������֤��������뾭��Base64�������������
    print S "$encode_smtppass\n";
    $a = <S>;

    #�����ʼ�ͷ����Ϣ
    print S qq~MAIL FROM: $from\n~;
    $a = <S>;
    foreach $i(@to)
    {
        print S qq~RCPT TO: <$i>\n~;
    }
    $a = <S>;

    #�����ʼ�����
    print S "DATA\n";
    print S "Subject: $subject\n";
    print S $body;
    print S "\n";
    print S "\n\n";
    print S ".\n";
    $a = <S>;

    print S "QUIT\n";
    $a = <S>;
    close(S);
    undef $|;
    return 1;
}

sub Base64encode    #Base64���뺯��
{
    my $res = "";
    while ($_[0] =~ /(.{1,45})/gs)
    {
        $res .= substr(pack('u', $1), 1);
        chop($res);
    }
    $res =~ tr| -_|A-Za-z0-9+/|;
    my $padding = (3 - length($_[0]) % 3) % 3;
    $res =~ s/.{$padding}$/'=' x $padding/e if ($padding);
    return $res;
}

1;
