package MIME::QuotedPrint;

use strict;
use vars qw(@ISA @EXPORT $VERSION);

require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(encode_qp decode_qp);

$VERSION = sprintf("%d.%02d", q$Revision: 2.3 $ =~ /(\d+)\.(\d+)/);


sub encode_qp ($)
{
    my $res = shift;
    $res =~ s/([^ \t\n!-<>-~])/sprintf("=%02X", ord($1))/eg;  # rule #2,#3
    $res =~ s/([ \t]+)$/
      join('', map { sprintf("=%02X", ord($_)) }
		   split('', $1)
      )/egm;                        # rule #3 (encode whitespace at eol)

    # rule #5 (lines must be shorter than 76 chars, but we are not allowed
    # to break =XX escapes.  This makes things complicated :-( )
    my $brokenlines = "";
    $brokenlines .= "$1=\n"
	while $res =~ s/(.*?^[^\n]{73} (?:
		 [^=\n]{2} (?! [^=\n]{0,1} $) # 75 not followed by .?\n
		|[^=\n]    (?! [^=\n]{0,2} $) # 74 not followed by .?.?\n
		|          (?! [^=\n]{0,3} $) # 73 not followed by .?.?.?\n
	    ))//xsm;

    "$brokenlines$res";
}


sub decode_qp ($)
{
    my $res = shift;
    $res =~ s/[ \t]+?(\r?\n)/$1/g;  # rule #3 (trailing space must be deleted)
    $res =~ s/=\r?\n//g;            # rule #5 (soft line breaks)
    $res =~ s/=([\da-fA-F]{2})/pack("C", hex($1))/ge;
    $res;
}

# Set up aliases so that these functions also can be called as
#
# MIME::QuotedPrint::encode();
# MIME::QuotedPrint::decode();

*encode = \&encode_qp;
*decode = \&decode_qp;

1;
