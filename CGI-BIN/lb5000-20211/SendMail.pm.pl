#############################################################
#  LeoBoard ver.5000 / LB5000 / 雷傲超级论坛 ver.5000
#  主页地址: http://www.CGIer.com/      CGI 编程者之家
#############################################################

package SendMail;

use Socket;

use MIME::Base64;
use MIME::QuotedPrint;

use Exporter;
use strict;
use vars qw($_LOCALHOST $VERSION $_MAILER @ISA @EXPORT @EXPORT_OK $_ERR);
use vars qw($_DEFAULT_SMTP_PORT);
@EXPORT = qw();
@EXPORT_OK = qw();

$VERSION = "2.03";
$_MAILER  = "Perl SendMail Module $VERSION";
$_DEFAULT_SMTP_PORT = 25;

eval {
  require Sys::Hostname;
  Sys::Hostname::import('hostname');
  $_LOCALHOST = hostname();
};
$_LOCALHOST = $_MAILER if $@;

sub new {
    my($pkg) 		= shift;
    my($smtpserver) 	= shift;
    my($smtpport) 	= shift;
    my($self) 		= {};

    bless $self, $pkg;

    $self->{'smtpserver'}  = ($smtpserver && $smtpserver =~ /^\s*$/)
		 ? "localhost" : $smtpserver;

    $self->{'smtpport'}    = ($smtpport && $smtpport =~ /^\d+$/) ? $smtpport : 
		$_DEFAULT_SMTP_PORT;

    $self->{'debugmode'}   = $self->OFF;
    $self->setMailHeader("X-MAILER", $_MAILER);

    $self->{'attachmentArr'} = [];

    return $self;

}
sub Attach ($;$) {
    my($self) = shift;
    my($filename) = shift;
    my($dataRef) = shift;
    my(%hash, $dump);

    return $self->setError("No attachment has been specified.")
	if $filename =~ /^\s*$/;
    if ($filename =~ /(\\|\/)/) {
      ($hash{'filename'}) = $filename =~ /^.*[\\\/]([^\\\/]+)$/;
    }
    else {
      $hash{'filename'} = $filename;
    }
    $hash{'filepath'} = $filename;
    $hash{'dataref'} = $dataRef if 
		(ref($dataRef) eq "SCALAR" || ref($dataRef) eq "GLOB");
    $hash{'attachtype'} = "attachment";
    return $self->attach(\%hash);

    return 0;
}

sub Bcc ($) {
    my($self)      = shift;
    my(@bcc)       = @_;
    my($currEmail) = undef;

    for $currEmail (@bcc) {
      push(@{$self->{'mailheaders'}->{'BCC'}}, $currEmail) if 
		($self->getEmailAddress($currEmail) !~ /^\s*$/);
    }

    return 0;
}

sub Cc ($) {
    my($self)      = shift;
    my(@cc)        = @_;
    my($currEmail) = undef;

    for $currEmail (@cc) {
      push(@{$self->{'mailheaders'}->{'CC'}}, $currEmail) if 
		($self->getEmailAddress($currEmail) !~ /^\s*$/);
    }

    return 0;
}

sub ErrorsTo ($) {
    my($self)      = shift;
    my(@errorsto)  = @_;
    my($currEmail) = undef;

    for $currEmail (@errorsto) {
      push(@{$self->{'mailheaders'}->{'ERRORS-TO'}}, $currEmail) if
		($self->getEmailAddress($currEmail) !~ /^\s*$/);
    }

    return 0;
}

sub From ($) {
    my($self) = shift;
    my($from) = shift;

    $self->{'mailheaders'}->{'FROM'} = $from;

    return 0;
}

sub Inline ($;$) {
    my($self) = shift;
    my($filename) = shift;
    my($dataRef) = shift;
    my(%hash, $dump);

    return $self->setError("No attachment has been specified.")
	if $filename =~ /^\s*$/;
    if ($filename =~ /(\\|\/)/) {
      ($hash{'filename'}) = $filename =~ /^.*[\\\/]([^\\\/]+)$/;
    }
    else {
      $hash{'filename'} = $filename;
    }
    $hash{'filepath'} = $filename;
    $hash{'dataref'} = $dataRef if 
	(ref($dataRef) eq "SCALAR" || ref($dataRef) eq "GLOB");
    $hash{'attachtype'} = "inline";
    return $self->attach(\%hash);

    return 0;
}

sub OFF () {
    return 0;
}

sub ON () {
    return 1;
}

sub ReplyTo ($;@) {
    my($self)      = shift;
    my(@replyto)   = @_;

    push(@{$self->{'mailheaders'}->{'REPLY-TO'}}, @replyto);

    return 0;
}

sub Subject ($) {
    $_[0]->{'mailheaders'}->{'SUBJECT'} = $_[1];

    return 0;
}

sub To ($;@) {
    my($self)      = shift;
    my(@to)        = @_;
    
    for (@to) {
      my($currEmail) = $_;
      push(@{$self->{'mailheaders'}->{'TO'}}, $currEmail) if 
		($self->getEmailAddress($currEmail) !~ /^\s*$/);
    }

    return 0;
}

sub attach ($) {
    my($self) = shift;
    my($dataRef) = shift;

    return $self->setError("No attachment has been specified.")
	if $dataRef->{'filename'} =~ /^\s*$/;
    push(@{$self->{'attachmentArr'}}, $dataRef);

    return 0;
}

sub createMailData () {
    my($self) = shift;
    my($currHeader) = undef;

    return -1 if $self->isMailReady() != 0;

    $self->{'maildata'} = undef;

    $self->{'maildata'} = "To: ";
    $self->{'maildata'} .= join(",\r\n\t", @{$self->{'mailheaders'}->{'TO'}});
    $self->{'maildata'} .= "\r\nFrom: ".$self->{'mailheaders'}->{'FROM'}."\r\n";
    $self->{'maildata'} .= "Subject: ".$self->{'mailheaders'}->{'SUBJECT'}."\r\n";
    if (defined $self->{'mailheaders'}->{'CC'} && 
		@{$self->{'mailheaders'}->{'CC'}} > 0) {
      $self->{'maildata'} .= "Cc: ";
      $self->{'maildata'} .= join(",\r\n\t", @{$self->{'mailheaders'}->{'CC'}});
      $self->{'maildata'} .= "\r\n";
    }

    if (defined $self->{'mailheaders'}->{'REPLY-TO'} && 
		@{$self->{'mailheaders'}->{'REPLY-TO'}} > 0) {
      $self->{'maildata'} .= "Reply-To: ";
      $self->{'maildata'} .= join(",\r\n\t", 
		@{$self->{'mailheaders'}->{'REPLY-TO'}})."\r\n";
    }

    if (defined $self->{'mailheaders'}->{'ERRORS-TO'} && 
		@{$self->{'mailheaders'}->{'ERRORS-TO'}} > 0) {
      $self->{'maildata'} .= "Errors-To: ";
      $self->{'maildata'} .= join(",\r\n\t", 
		@{$self->{'mailheaders'}->{'ERRORS-TO'}})."\r\n";
    }

    for $currHeader (sort keys %{$self->{'mailheaders'}->{'OTHERS'}}) {
      my($currMailHeader) = undef;
      ($currMailHeader = $currHeader) =~ s/\b(\w)(\w+)\b/$1\L$2/g;
      $self->{'maildata'} .= "$currMailHeader: ";
      $self->{'maildata'} .= $self->{'mailheaders'}->{'OTHERS'}->{$currHeader};
      $self->{'maildata'} .= "\r\n";
    }

    if (scalar(@{$self->{'attachmentArr'}}) > 0) {
      my($currHash);
      srand(time ^ $$);
      my($boundary) = "==__SENDMAIL__".
		join("", ('a'..'z','A'..'Z', 0..9)[map rand $_, (62)x25]).
		"__==";
      $self->{'maildata'} .= "MIME-Version: 1.0\r\n";
      $self->{'maildata'} .= "Content-Type: multipart/mixed; ";
      $self->{'maildata'} .= "boundary=\"$boundary\"\r\n";
      $self->{'maildata'} .= "\r\n";

      if (defined $self->{'mailbody'}) {
        $self->{'maildata'} .= "\-\-$boundary\r\n";
        $self->{'maildata'} .= "Content-Type: text/html; charset=\"gb2312\"\r\n";
        $self->{'maildata'} .= "Content-Transfer-Encoding: quoted-printable\r\n\r\n";
        $self->{'maildata'} .= encode_qp($self->{'mailbody'})."\r\n\r\n";
      }

      for $currHash (@{$self->{'attachmentArr'}}) {
        $currHash->{'content-type'} = 
		$self->getMIMEType($currHash->{'filename'});
        $self->{'maildata'} .= "\-\-$boundary\r\n";
        $self->{'maildata'} .= "Content-Type: $currHash->{'content-type'}; name=\"$currHash->{'filename'}\"\r\n";
        $self->{'maildata'} .= "Content-Transfer-Encoding: base64\r\n";
        $self->{'maildata'} .= "Content-Disposition: $currHash->{'attachtype'}; filename=\"$currHash->{'filename'}\"\r\n";
        $self->{'maildata'} .= "\r\n";

	if (defined $currHash->{'dataref'}) {
	  if (ref($currHash->{'dataref'}) eq "SCALAR") {
	    $self->{'maildata'} .= encode_base64(${$currHash->{'dataref'}}, "\r\n");
	  }
	  else {
	    my($data) = undef;
	    my($buff) = "";
	    my($pos) = 0;
	    (defined ($pos = tell($currHash->{'dataref'}))) ||
    		return $self->setError("Error in tell(): $!");
	    while (read($currHash->{'dataref'}, $buff, 1024)) {
	      $data .= $buff;
            }
	    $self->{'maildata'} .= encode_base64($data, "\r\n");
	    seek($currHash->{'dataref'}, $pos, 0) ||
    		return $self->setError("Error in seek(): $!");
	  }
	}
	elsif (-f $currHash->{'filepath'}) {
          my($data) = undef;
	  my($buff) = "";
          open(FILE, $currHash->{'filepath'});
	  # In Windows platform, non-text file should use binmode() function.
	  if (! -T $currHash->{'filepath'}) {
	    binmode(FILE);
	  }
	  while (sysread(FILE, $buff, 1024)) {
	    $data .= $buff;
          }
          close(FILE);
          $self->{'maildata'} .= encode_base64($data, "\r\n");
	}
	else {
	  $self->{'maildata'} .= encode_base64("", "\r\n");
	}
        $self->{'maildata'} .= "\r\n";
      }
      $self->{'maildata'} .= "\-\-${boundary}\-\-\r\n";
    }
    else {
      $self->{'maildata'} .= "\r\n";
      $self->{'maildata'} .= "$self->{'mailbody'}\r\n";
    }

    return 0;
}

sub getEmailAddress ($) {
    my($self)  = shift;
    my($value) = shift;
    my($retvalue) = undef;

    if ($value =~ /^\<([^\>\@]+\@[\w\-]+(\.[\w\-]+)+)\>/) {
      ($retvalue = $1) =~ tr/[A-Z]/[a-z]/;
      return $retvalue;
    }

    if ($value =~ /^[^\<]+\<([^\>\@]+\@[\w\-]+(\.[\w\-]+)+)\>/) {
      ($retvalue = $1) =~ tr/[A-Z]/[a-z]/;
      return $retvalue;
    }

    return "" if $value =~ /\s+/;

    $value =~ tr/[A-Z]/[a-z]/;
    return $value if $value =~ /^[^\@]+\@[\w\-]+(\.[\w\-]+)+$/;

    return "";
}

sub getMIMEType ($) {
    my($self) = shift;
    my($filename) = shift;
    my($ext, %MIMEHash);

    %MIMEHash = (
	'au'	=> 'audio/basic',
	'avi'	=> 'video/x-msvideo',
	'class'	=> 'application/octet-stream',
	'cpt'	=> 'application/mac-compactpro',
	'dcr'	=> 'application/x-director',
	'dir'	=> 'application/x-director',
	'doc'	=> 'application/msword',
	'exe'	=> 'application/octet-stream',
	'gif'	=> 'image/gif',
	'gtx'	=> 'application/x-gentrix',
	'jpeg'	=> 'image/jpeg',
	'jpg'	=> 'image/jpeg',
	'js'	=> 'application/x-javascript',
	'hqx'	=> 'application/mac-binhex40',
	'htm'	=> 'text/html',
	'html'	=> 'text/html',
	'mid'	=> 'audio/midi',
	'midi'	=> 'audio/midi',
	'mov'	=> 'video/quicktime',
	'mp2'	=> 'audio/mpeg',
	'mp3'	=> 'audio/mpeg',
	'mpeg'	=> 'video/mpeg',
	'mpg'	=> 'video/mpeg',
	'pdf'	=> 'application/pdf',
	'pm'	=> 'text/plain',
	'pl'	=> 'text/plain',
	'ppt'	=> 'application/powerpoint',
	'ps'	=> 'application/postscript',
	'qt'	=> 'video/quicktime',
	'ram'	=> 'audio/x-pn-realaudio',
	'rtf'	=> 'application/rtf',
	'tar'	=> 'application/x-tar',
	'tif'	=> 'image/tiff',
	'tiff'	=> 'image/tiff',
	'txt'	=> 'text/plain',
	'wav'	=> 'audio/x-wav',
	'xbm'	=> 'image/x-xbitmap',
	'zip'	=> 'application/zip',
    );
    ($ext) = $filename =~ /\.([^\.]+)$/;
    $ext =~ tr/[A-Z]/[a-z]/;
    
    return defined $MIMEHash{$ext} ? $MIMEHash{$ext} : "application/octet-stream";

}

sub getRcptLists () {
    my($self) = shift;
    my(@rcptLists) = ();
    my($currEmail) = undef;

    for $currEmail (@{$self->{'mailheaders'}->{'TO'}}) {
      my($currEmail) = $self->getEmailAddress($currEmail);
      push(@rcptLists, $currEmail) if 
		($currEmail !~ /^\s*$/ && (! grep(/^$currEmail$/, @rcptLists)));
    }

    if (defined $self->{'mailheaders'}->{'BCC'} && 
		@{$self->{'mailheaders'}->{'BCC'}} > 0) {
      for $currEmail (@{$self->{'mailheaders'}->{'BCC'}}) {
        my($currEmail) = $self->getEmailAddress($currEmail);
        push(@rcptLists, $currEmail) if 
		($currEmail !~ /^\s*$/ && (! grep(/^$currEmail$/, @rcptLists)));
      }
    }

    if (defined $self->{'mailheaders'}->{'CC'} && 
		@{$self->{'mailheaders'}->{'CC'}} > 0) {
      for $currEmail (@{$self->{'mailheaders'}->{'CC'}}) {
        my($currEmail) = $self->getEmailAddress($currEmail);
        push(@rcptLists, $currEmail) if 
		($currEmail !~ /^\s*$/ && (! grep(/^$currEmail$/, @rcptLists)));
      }
    }

    return \@rcptLists;
}

sub isMailReady () {
    my($self) = shift;

    return $self->setError("发信人没有填写.<br>No sender has been specified.") if
	! defined $self->{'mailheaders'}->{'FROM'};

    return $self->setError("收信人没有指定.<br>No recipient has been specified.") if 
	((! defined $self->{'mailheaders'}->{'TO'}) ||
		(defined @{$self->{'mailheaders'}->{'TO'}} &&
		 @{$self->{'mailheaders'}->{'TO'}} < 1));

    return $self->setError("邮件主题没有.<br>No subject has been specified.") if
	! defined $self->{'mailheaders'}->{'SUBJECT'};

    return $self->setError("邮件正文没有填写.<br>No mail body has been set.") if
	((! defined $self->{'mailbody'}) &&
		(scalar(@{$self->{'attachmentArr'}}) < 1));

    return 0;
}

sub receiveFromServer ($) {
    my($self) = shift;
    my($socket) = shift;
    my($reply);

    while ($socket && ($reply = <$socket>)) {
      return $self->setError($reply) if $reply =~ /^5/;
      print $reply if $self->{'debugmode'};
      last if $reply =~ /^\d+ /;
    }

    return 0;
}
sub reset () {
    my($self) = shift;

    $self->{'debugmode'} = $self->OFF;
    $self->{'mailbody'} = undef;
    $self->{'maildata'} = undef;
    $self->{'mailheaders'} = undef;
    $self->{'sender'} = undef;
    $self->{'attachmentArr'} = [];

    return 0;
}
sub sendMail () {
    my($self) = shift;
    my($iaddr, $paddr, $proto, $rcptlistRef, $currEmail) = undef;

    $self->{'sender'} = $self->getEmailAddress($self->{'mailheaders'}->{'FROM'});

    return $self->setError("Please check the sender's email address setting.")
	if $self->{'sender'} =~ /^\s*$/; 

    return -1 if $self->createMailData() != 0;

    $rcptlistRef = $self->getRcptLists();

    return $self->setError("No recipient has been specified.") if 
		@{$rcptlistRef} == 0;

    $iaddr = inet_aton($self->{'smtpserver'}) || 
		return $self->setError("no host: $self->{'smtpserver'}");
    $paddr = sockaddr_in($self->{'smtpport'}, $iaddr);
    $proto = getprotobyname('tcp');
    socket(SOCK, PF_INET, SOCK_STREAM, $proto) || 
		return $self->setError("Socket error: $!");
    connect(SOCK, $paddr) || 
	return $self->setError("Error in connecting to $self->{'smtpserver'} at port $self->{'smtpport'}: $!");

    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    return -1 if $self->sendToServer(\*SOCK, "HELO $_LOCALHOST") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    return -1 if $self->sendToServer(\*SOCK, "MAIL FROM: <$self->{'sender'}>") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    for $currEmail (@{$rcptlistRef}) {
      return -1 if $self->sendToServer(\*SOCK, "RCPT TO: <$currEmail>") != 0;
      return -1 if $self->receiveFromServer(\*SOCK) != 0;
    }
    return -1 if $self->sendToServer(\*SOCK, "DATA") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    return -1 if $self->sendToServer(\*SOCK, "$self->{'maildata'}\r\n.") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    return -1 if $self->sendToServer(\*SOCK, "QUIT") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    eof(SOCK) || close(SOCK) || 
	return $self->setError("Fail close connectiong socket: $!");
    print "The mail has been sent to ".scalar(@{$rcptlistRef}) if 
		$self->{'debugmode'};
    print " person/s successfully.\n" if $self->{'debugmode'};

    return 0;
}

sub sendToServer ($$) {
    my($self) = shift;
    my($socket) = shift;
    my($message) = shift;

    print "$message\n" if $self->{'debugmode'};

    #
    # Sending data to the server.
    #
    send($socket, "$message\r\n", 0) || 
		return $self->setError("Fail to send $message: $!");

    return 0;
}

sub setDebug ($) {
    my($self) = shift;

    $self->{'debugmode'} = shift;

    return 0;
}

sub setError ($) {
    my($self)     = shift;
    my($errorMsg) = shift;

    $self->{'error'} = $errorMsg if $errorMsg !~ /^\s*$/;

    return -1;
}
sub setMailBody ($) {
    my($self)	  = shift;
    my($mailbody) = shift;

    $self->{'mailbody'} = $mailbody;

    return 0;
}

sub setMailHeader ($$) {
    my($self)	  	 = shift;
    my($mailheader)	 = shift;
    my($mailheadervalue) = shift;

    $mailheader =~ tr/[a-z]/[A-Z]/;

    $self->{'mailheaders'}->{'OTHERS'}->{$mailheader} = $mailheadervalue;

    return 0;
}

sub setSMTPPort ($) {
    my($self)     = shift;
    my($smtpport) = shift;

    $self->{'smtpport'} = $smtpport if $smtpport =~ /^\d+$/;

    return 0;
}

sub setSMTPServer ($) {
    my($self)       = shift;
    my($smtpserver) = shift;

    $smtpserver =~ s/\s*//g;

    $self->{'smtpserver'} = $smtpserver if $smtpserver !~ /^\s*$/;

    return 0;
}

sub version () {
    my($self) = shift;

    return $VERSION;
}

1;
__END__

=head1 NAME

SendMail -- This is a perl module which is using Socket to connect the SMTP port to send mails.

=head1 SYNOPSIS

  use SendMail;

  $smtpserver 		= "mail.server.com";
  $smtpport   		= 25;
  $sender     		= "Sender <sender@domain.com>";
  $subject    		= "Subject of the mail.";
  $recipient  		= "Recipient <recipient@domain.com>";
  $recipient2 		= "Recipient 2 <recipient2@domain.com>";
  @recipients 		= ($recipient, $recipient2);
  $administrator 	= "Administrator <admin@domain.com>";
  $administrator2 	= "Administrator 2 <admin2@domain.com>";
  $replyto		= $sender;
  $replyto2		= $recipient;
  @replytos		= ($replyto, $replyto2);
  $header		= "X-Mailer";
  $headervalue		= "Perl SendMail Module 2.03";
  $mailbodydata		= "This is a testing mail.";

  $obj = new SendMail();
  $obj = new SendMail($smtpserver);
  $obj = new SendMail($smtpserver, $smtpport);

  $obj->setDebug($obj->ON);
  $obj->setDebug($obj->OFF);

  $obj->From($sender);

  $obj->Subject($subject);

  $obj->To($recipient);
  $obj->To($recipient, $recipient2);
  $obj->To(@recipients);

  $obj->Cc($recipient);
  $obj->Cc($recipient, $recipient2);
  $obj->Cc(@recipients);

  $obj->Bcc($recipient);
  $obj->Bcc($recipient, $recipient2);
  $obj->Bcc(@recipients);

  $obj->ErrorsTo($administrator);
  $obj->ErrorsTo($administrator, $administrator2);
  $obj->ErrorsTo(@administrators);

  $obj->ReplyTo($replyto);
  $obj->ReplyTo($replyto, $replyto2);
  $obj->ReplyTo(@replytos);

  $obj->setMailHeader($header, $headervalue);

  $obj->setMailBody($mailbodydata);

  $obj->Attach($file);
  $obj->Attach($file, \$filedata);
  $obj->Attach($file, \*FILEHANDLE);

  $obj->Inline($file);
  $obj->Inline($file, \$filedata);
  $obj->Inline($file, \*FILEHANDLE);

  if ($obj->sendMail() != 0) {
    print $obj->{'error'}."\n";
  }

  $obj->reset();

=head1 EXAMPLE


http://www.tneoh.zoneit.com/perl/SendMail/testSendMail.pl

=head1 DESCRIPTION


This module is written so that user can easily use it to send mailing list. 
Please do not abuse it.

And it can be used in any perl script to send a mail similar to sending mail
by using /usr/lib/sendmail program.

I have tested this module on Unix and Windows platforms, it works fine. 
Of course you need perl version 5. With the example script, 
testSendMail.pl, you can simply a testing on it.

Errors, comments or questions are welcome.

=head1 CHANGES


1.00->1.01 Recipients with email address contains a "-" in the hostname,
will be able to receive the email now.

1.01->1.02 Module now not only expecting one line reply from the server, it
can receive multiple lines until the server waiting for next command.

1.02->1.03 Repeat declaration of "$currEmail" will give an error in NT
system.

1.03->1.04 Email addresses are enclosed in < and > after "MAIL FROM" and
"RCPT TO" commands.(RFC821) For Microsoft Exchange 4, email addresses
not enclosed in < and > will get an error from the system.

1.04->1.05 getEmailAddress() subroutine should accept email address
in just "<user@domain.com>" format.

1.05->2.00b Simple MIME supported. attach(), Attach() and Inline() 
subroutines added.

2.00b->2.00 Attach() and Inline() supports for filehandle which is
easier for users who are using CGI.pm. Prototypes are added. And we
send "\r\n" to the SMTP server instead of only "\n".

2.00->2.01 After sending the maildata, supposed to be "\r\n" instead
of just "\n".

2.01->2.02 Calling eof() to check the opened socket, else it will
cause an error in ActivePerl5.6.

2.02->2.03 Change all EOL to "\r\n", instead of just "\n".

=head1 CREDITS


laurens van alphen

Dag 豬en

Juliano, Sylvia, CON, OASD(HA)/TMA

Tony Simopoulos

Jeff Graves

Pisciotta, Steve

=head1 SOURCE


http://www.tneoh.zoneit.com/perl/SendMail/SendMail.pm


=head1 AUTHOR


Simon Tneoh Chee-Boon	tneohcb@pc.jaring.my

Copyright (c) 1998,1999,2000 Simon Tneoh Chee-Boon. All rights reserved.
This program is free software; you can redistribute it and/or
modify it under the same terms as Perl itself.

=head1 VERSION

Version 2.03 	16 August 2000

=head1 SEE ALSO

Socket.pm, MIME::Base64.pm, MIME::QuotedPrint.pm

=cut
