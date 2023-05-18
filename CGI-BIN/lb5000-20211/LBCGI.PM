package LBCGI;
require 5.005;
# Writed by Leoboad Team
# Something is from Lincoln D. Stein's CGI.pm
use strict;
use vars qw(
$VERSION $DEFAULT_CLASS $OBJECT
$POST_MAX $DISABLE_UPLOADS $HEADERS_ONCE $CHAR_SET
$COOKIE_PATH $COOKIE_DOMAIN
$HAVE_LOAD_TIMES
@EXPORT
%SYSTEM
);
@EXPORT=qw(header param cookie redirect start_html end_html);
initialize_globals();
sub initialize_globals {
$DEFAULT_CLASS = 'LBCGI';
$VERSION='0.01 Build 0612';
$POST_MAX=-1;
$DISABLE_UPLOADS=0;
$HEADERS_ONCE=0;
$CHAR_SET='GB2312';
$COOKIE_PATH='/';
$COOKIE_DOMAIN=undef;
$HAVE_LOAD_TIMES++;
$SYSTEM{MOD_PERL}=(defined($ENV{'GATEWAY_INTERFACE'}) && $ENV{'GATEWAY_INTERFACE'} =~ /^CGI-Perl\//) ? 1: 0;
$SYSTEM{PERLEX}=(defined($ENV{'GATEWAY_INTERFACE'}) && $ENV{'GATEWAY_INTERFACE'} =~ /^CGI-PerlEx/) ? 1: 0;
if ($SYSTEM{MOD_PERL}){$|=1; require Apache unless $HAVE_LOAD_TIMES > 1}
undef $OBJECT if defined $OBJECT;
1;
}
sub import{
my $caller=caller;
for(@EXPORT){eval("*{$caller\::$_}=\\&{'$DEFAULT_CLASS\::$_'}");}
initialize_globals() if ($SYSTEM{MOD_PERL} || $SYSTEM{PERLEX});
}
sub new{
$OBJECT = bless {},$DEFAULT_CLASS
unless defined $OBJECT && UNIVERSAL::isa($OBJECT,$DEFAULT_CLASS);
if ($SYSTEM{MOD_PERL} && defined Apache->request) {Apache->request->register_cleanup(\&$DEFAULT_CLASS::initialize_globals);}
$OBJECT;
}
sub param{
my ($self,$name)= _self_or_default(@_);
$OBJECT->_initReadForm
unless defined $self->{'.formdata'} && ref($self->{'.formdata'}) eq 'HASH';
return wantarray ? sort(keys(%{$self->{'.filsdata'}})) : $name
if defined $name && defined $self->{'.filedata'}{$name};
return wantarray ? sort(keys(%{$self->{'.formdata'}})) : undef
unless defined $name && defined $self->{'.formdata'}{$name};
return wantarray ? @{$self->{'.formdata'}{$name}} : $self->{'.formdata'}{$name}->[0];
}
sub readUploadFile {
my $self=shift;
my ($name,$size)=@_;
return undef unless defined $name && defined $size && defined $self->{'.filedata'}{$name} && ($self->{'.filedata'}{$name}[0] ne '');
my $str=substr($self->{'.filedata'}{$name}[0],0,$size);
substr($self->{'.filedata'}{$name}[0],0,$size)='';
$str;
}
sub uploadInfo {
my $self=shift;
my $name=shift;
return undef unless defined $name && defined $self->{'.filedata'}{$name} && defined $self->{'.filedata'}{$name}[1] && defined $self->{'.filedata'}{$name}[2];
return wantarray ? ($self->{'.filedata'}{$name}[1],$self->{'.filedata'}{$name}[2]) : $self->{'.filedata'}{$name}[1];
}

sub header{
my($self,%arg)= _self_or_default(@_);
return undef if $self->{'.header_printed'}++ and $HEADERS_ONCE;
$arg{'-type'} ||= 'text/html';
$arg{'-charset'} ||= $CHAR_SET;
$arg{'-type'} .= '; charset='.$arg{'-charset'};
if (defined $self->{'.cgi_error'}){
my $errormsg='';
if ($self->{'.cgi_error'} =~ /^\s*(\d+)\s*(.*)/){
$arg{'-status'}=$1;
$errormsg=$2;
}else{$arg{'-status'}=500; $errormsg=$self->{'.cgi_error'};}
return "Status: $arg{'-status'}\015\012"."Content-Type: $arg{'-type'}\015\012\015\012".$errormsg
}
my @header;
push(@header,"Status: $arg{'-status'}")
if defined $arg{'-status'};
push(@header,"Location: $arg{'-location'}")
if defined $arg{'-location'};
push(@header,"Expires: ".toGMTstring($arg{'-expires'}))
if defined $arg{'-expires'};
push(@header,"Date: ".toGMTstring('now'));
push(@header,"Pragma: no-cache")
if defined $arg{'-cache'};
push(@header,"Content-Disposition: attachment; filename=\"$arg{'attachment'}\"")
if defined $arg{'-attachment'};
my $header;
$header .= join('',@{$arg{'-cookie'}})
if defined $arg{'-cookie'} && ref($arg{'-cookie'}) eq 'ARRAY';
$header .= join("\015\012",@header)."\015\012" if defined $header[0];
$header .= "Content-Type: $arg{'-type'}\015\012\015\012";
if ($SYSTEM{MOD_PERL}) {
my $r = Apache->request;
$r->send_cgi_header($header);
return '';
}
$header;
}
sub redirect {
my($self,%arg) = _self_or_default(@_);
return undef unless defined ($arg{'-location'});
my(@header);
unshift(@header,'-status'=>'302 Moved','-location'=>$arg{'-location'});
unshift(@header,'-cookie'=>$arg{'-cookie'})
if defined $arg{'-cookie'};
return $self->header(@header);
}
sub cookie{
my ($self,@arg) = _self_or_default(@_);
$self->getCookie if !defined $self->{'.cookies'};
return $self->getCookie unless defined $arg[0];
if (!defined $arg[1]){if (defined $self->{'.cookies'}{$arg[0]}){return $self->{'.cookies'}{$arg[0]};}else{ return undef;}}
return $self->setCookie(@arg);
}
sub getCookie{
my $self=shift;
return wantarray ? %{$self->{'.cookies'}} : $self->{'.cookies'}
if (defined $self->{'.cookies'} && ref ($self->{'.cookies'}) eq 'HASH');
my $cookie;
my %Cookie;
$self->{'.cookies'}=\%Cookie;
if (defined $ENV{HTTP_COOKIE} || defined $ENV{COOKIE}){
$cookie=$ENV{HTTP_COOKIE} || defined $ENV{COOKIE};
}else{return;}
my ($key, $value);
for (split(/;\s*/,$cookie)){
s/^\s+|\s+$//g;
($key, $value) = map(unescape($_),split(/=/, $_));
next unless defined $value;
$Cookie{$key} ||= $value;
}
return wantarray ? %Cookie : $self->{'.cookies'};
}
sub setCookie{
my ($self,%CookieArg)=@_;
my @cookie;
return '' unless defined $CookieArg{'-name'};
$CookieArg{value} ||='';
push(@cookie,escape($CookieArg{'-name'}).'='.escape($CookieArg{'-value'}));
push(@cookie,'path='.$CookieArg{'-path'})
if ($CookieArg{'-path'} ||= $COOKIE_PATH);
push(@cookie,'domain='.$CookieArg{'-domain'})
if ($CookieArg{'-domain'} ||= $COOKIE_DOMAIN);
push(@cookie,'expires='.toGMTstring($CookieArg{'-expires'},'cookie'))
if (defined $CookieArg{'-expires'} && $CookieArg{'-expires'} != -1);
push(@cookie,'secure='.$CookieArg{'-secure'})
if (defined $CookieArg{'-secure'});
return 'Set-Cookie: '.join('; ',@cookie)."\015\012";
}
sub escape {
my($self,$str)= _self_or_default(@_);
return if !defined $str;
$str=~ s/([^@\w\.\*\-\x20])/uc sprintf('%%%02x',ord($1))/eg;
$str=~ tr/ /+/;
$str;
}
sub unescape {
my($self,$str)= _self_or_default(@_);
return if !defined $str;
$str=~ tr/+/ /;
$str=~ s/%([0-9a-fA-F]{2})/chr hex($1)/eg;
$str;
}
sub toGMTstring {
my($self,$time,$format)= _self_or_default(@_);
$format ||= 'http';
my @MON=qw/Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec/;
my @WDAY=qw/Sun Mon Tue Wed Thu Fri Sat/;
my %mult=( 's'=>1,'m'=>60,'h'=>60*60,'d'=>60*60*24,'M'=>60*60*24*30,'y'=>60*60*24*365);
if (!$time || (lc($time) eq 'now') || $time =~/^\s*$/) {$time = time;}
elsif ($time=~ /^\s*\d+\s*$/){$time = scalar($time);}
elsif ($time=~/^([+-]?(?:\d+|\d*\.\d*))([mhdMy]?)/) {$time = time+($mult{$2} || 1)*$1;}
else{return $time;}
my($sc)=($format eq "cookie") ? '-' : ' ';
my($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime($time);
return sprintf("%s, %02d$sc%s$sc%04d %02d:%02d:%02d GMT",$WDAY[$wday],$mday,$MON[$mon],$year+1900,$hour,$min,$sec);
}
sub cgi_error {
my ($self,$err)=@_;
return undef unless defined $err;
$self->{'.cgi_error'} = $err;
}
sub _initReadForm {
my $self=shift;
my $method=(defined($ENV{'REQUEST_METHOD'})) ? $ENV{'REQUEST_METHOD'} : '';
my $content_length = (defined($ENV{'CONTENT_LENGTH'})) ? $ENV{'CONTENT_LENGTH'} : 0;
$self->{'.formdata'} = {}
unless defined $self->{'.formdata'} && ref($self->{'.formdata'}) eq 'HASH';
if (($POST_MAX > 0) && ($content_length > $POST_MAX)) {
return $self->cgi_error("413 Request entity too large");
}
if ($method eq 'POST' && defined($ENV{'CONTENT_TYPE'})
&& $ENV{'CONTENT_TYPE'}=~/^multipart\/form-data/){
my($boundary)=$ENV{'CONTENT_TYPE'} =~ /boundary=\"?([^\";,\s]+)/;
$self->_read_multipart($boundary,$content_length);
return 1;
}
my $query_string;
if ($method eq 'GET' || $method eq 'HEAD') {
if ($SYSTEM{MOD_PERL}) {$query_string = Apache->request->args;}else{$query_string = $ENV{'QUERY_STRING'}
if defined $ENV{'QUERY_STRING'};
$query_string ||= $ENV{'REDIRECT_QUERY_STRING'}
if defined $ENV{'REDIRECT_QUERY_STRING'};
}}elsif($method eq 'POST'){
read(STDIN,$query_string,$content_length);
}elsif(defined $ARGV[0]){$query_string = join('&',@ARGV)}
if (defined $query_string){$self->_parse_params($query_string);}
1;
}
sub _read_multipart {
my($self,$boundary,$Content_length) = @_;
$boundary='--'.quotemeta($boundary);
my $form=$self->{'.formdata'};
my $datarow_ref;
my $datacurrent_ref;
my $length=0;
binmode(STDIN);
while(<STDIN>){
$length += length;
if (m/^$boundary(\-\-)?\015\012$/o){
chop($$datacurrent_ref),
chop($$datacurrent_ref)
if (defined $$datacurrent_ref);
if (defined $1 && $1 eq '--'){
last;
}else{
my $info_head = "\015\012";
while(<STDIN>){
last if m/^\s*$/;
$info_head .= $_;
}
$info_head=~ s/((?:\"[^\"\n]*\"[^\";]*)*);\s*/$1\015\012/g;
my $name=($info_head=~/\015\012name\s*=\s*\"([^\"]+)/i || $info_head=~/\015\012name\s*=\s*([^\"][^\s]+)/i) ? $1 : undef;
my $filename=($info_head=~/\015\012filename\s*=\s*\"([^\"]+)/i || $info_head=~/\015\012filename\s*=\s*([^\"][^\s]+)/i) ? $1 : undef;
$filename=~ s/^.*[\/\\]// if defined $filename;
my $type=($info_head=~/\015\012Content-type:\s*([^\"][^\s]+)/i) ? $1 : undef;
if (defined $form->{$name} && ref($datarow_ref) eq 'ARRAY' && !(defined $filename && defined $type)){
$datarow_ref=$form->{$name};
$datacurrent_ref=\$$datarow_ref[@$datarow_ref];
}elsif(defined $name){
$datarow_ref=$form->{$name} = [];
$datacurrent_ref=\$$datarow_ref[0];
if (defined $filename && defined $type){
if ($DISABLE_UPLOADS){
undef $datacurrent_ref;
next;
}
$datarow_ref->[1]=$filename;
$datarow_ref->[2]=$type;
$self->{'.filedata'}{$name}=$datarow_ref;
}
}else{undef $datacurrent_ref;}
}}else{$$datacurrent_ref .= $_ if defined $datacurrent_ref;}
last if $length >= $Content_length;}
}
sub _parse_params {
my $self=shift;
my $str=shift;
my $form=$self->{'.formdata'};
my ($name,$value);
for(split(/[&;]/,$str)){
($name,$value)=map(unescape($_),split(/=/, $_));
$value='' unless defined $value;
$form->{$name}=[]
if !defined($form->{$name}) || ref($form->{$name}) ne 'ARRAY';
push (@{$form->{$name}},$value);}
}
sub _self_or_default {
return @_ if defined($_[0]) && UNIVERSAL::isa($_[0],$DEFAULT_CLASS);
$OBJECT=new() unless defined($OBJECT);
unshift(@_,$OBJECT);
return wantarray ? @_ : $OBJECT;
}
1;
