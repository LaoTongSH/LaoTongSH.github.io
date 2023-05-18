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
#            http://maildo.com/      大家一起邮
#
#############################################################

sub signlbcode {
    my $signature = shift;
    $signature =~ s/javascript/\&\#106\;avascript/isg;
    $signature =~ s/FORM/\&\#70\;ORM/isg;
    $signature =~ s/value/\&\#118\;alue/isg;

   if (($arrawsignpic eq "on")||($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo')) {
	$signature =~ s/\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<img src=$1:\/\/$2 border=0>/isg;
    }
   if (($arrawsignflash eq "on")||($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo')) {
	$signature =~ s/(\[swf\])\s*(http|https|ftp):\/\/(\S+?\.swf)\s*(\[\/swf\])/<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$2:\/\/$3 quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>/isg;
	$signature =~ s/(\[FLASH=)(\S+?)(\,)(\S+?)(\])\s*(http|https|ftp):\/\/(\S+?\.swf)\s*(\[\/FLASH\])/<OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$2 HEIGHT=$4><PARAM NAME=MOVIE VALUE=$6:\/\/$7><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$6:\/\/$7 WIDTH=$2 HEIGHT=$4 PLAY=TRUE LOOP=TRUE QUALITY=HIGH><\/EMBED><\/OBJECT>/isg;
    }
    if (($arrawsignfontsize eq "on")||($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo')) {
    	$signature =~ s/\[size=\s*(.*?)\s*\]\s*(.*?)\s*\[\/size\]/<font size=$1>$2<\/font>/isg;
    }
    if ($arrawsignsound eq "on") {
	$signature =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.wav)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/mid.gif width=16 height=16 alt=MIDI音乐>/isg;
	$signature =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.mid)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/wave.gif width=16 height=16 alt=WAVE音乐>/isg;
	$signature =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.midi)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/wave.gif width=16 height=16 alt=WAVE音乐>/isg;
    }

    $signature =~ s/\<p>/<br><br>/isg;
    $signature =~ s|\[\[|\{\{|g;
    $signature =~ s|\]\]|\}\}|g;
    $signature =~ s|\n\[|\[|g;
    $signature =~ s|\]\n|\]|g;
    $signature =~ s|<br>| <br>|g;
    $signature =~ s|\[hr\]\n| |g;
    $signature =~ s|\[hr\]| |g;
    $signature =~ s/\[br\]/<br>/isg;
    $signature =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]/$1$2<br>$3<br>/isg;
    $signature =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]/$1/isg;
    $signature =~ s/\[url\](\[\S+\])(\S+?)(\[\S+\])\[\/url\]/<a href=$2 target=_blank>$1$2$3<\/a>/isg;
    $signature =~ s/\[url=(http|https|ftp):\/\/(\S+?)\]/<a href=$1:\/\/$2 target=_blank>/isg;
    $signature =~ s/\[url=(\S+?)\]/<a href=http:\/\/$1 target=_blank>/isg;
    $signature =~ s/\[url=\s*(.*?)\s*\]\s*(.*?)\s*\[\/url\]/<a href=$1 target=_blank>$2<\/a>/isg;
    $signature =~ s/\[url\]\s*(http|https|ftp):\/\/(.*?)\s*\[\/url\]/<a href=$1:\/\/$2 target=_blank>$1:\/\/$2<\/a>/isg;
    $signature =~ s/\[url\]\s*(.*?)\s*\[\/url\]/<a href=http:\/\/$1 target=_blank>$1<\/a>/isg;
    $signature =~ s/\[\/url\]/<\/a>/isg;
    $signature =~ s/(\[email\])(\S+\@\S+?)(\[\/email\])/<A HREF="mailto:$2">$2<\/A>/isg;
    $signature =~ s/\ (http|https|ftp):\/\/(\S+?)\ / <a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
    $signature =~ s/<br>(http|https|ftp):\/\/(\S+?)\ /<br><a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
    $signature =~ s/^(http|https|ftp|rtsp):\/\/(\S+?)\ /<a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
    $signature =~ s/\ www\.(\S+?)\ / <a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
    $signature =~ s/<br>www\.(\S+?)\ /<br><a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
    $signature =~ s/^www\.(\S+?)\ /<a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
    $signature =~ s/\[b\]/<b>/isg;
    $signature =~ s/\[\/b\]/<\/b>/isg;
    $signature =~ s/\[i\]/<i>/isg;
    $signature =~ s/\[\/i\]/<\/i>/isg;
    $signature =~ s/\[font=\s*(.*?)\s*\]\s*(.*?)\s*\[\/font\]/<font face=$1>$2<\/font>/isg;
    $signature =~ s/\[u\]/<u>/isg;
    $signature =~ s/\[\/u\]/<\/u>/isg;
    $signature =~ s/\[color=(\S+?)\]/<font color=$1>/isg;
    $signature =~ s/\[\/color\]/<\/font>/isg;
    $signature =~ s/\\(http|https|ftp):\/\/(\S+)/<a href=$1:\/\/$2 target=_blank>$1:\/\/$2<\/a>/isg;
    $signature =~ s/\[code\](.+?)\[\/code\]/$1/isg;
    $signature =~ s/\[email=(\S+?)\]/<a href=mailto:$1>/isg;
    $signature =~ s/\[\/email\]/<\/a>/isg;
    $signature=~ s/<br>(\w+\@\w+\.\w+)/<br><A HREF=mailto:$1>$1<\/A>/isg;
    $signature =~ s/^(\w+\@\w+\.\w+)/<A HREF=mailto:$1>$1<\/A>/isg;
    $signature =~ s/\\(\w+\@\w+\.\w+)/<A HREF=mailto:$1>$1<\/A>/isg;
    $signature =~ s/(\[fly\])(.+?)(\[\/fly\])/<marquee width=90% behavior=alternate scrollamount=3>$2<\/marquee>/isg;
    $signature =~ s/(\[s\])(.+?)(\[\/s\])/<s>$2<\/s>/isg;
    $signature =~ s/(\[sup\])(.+?)(\[\/sup\])/<sup>$2<\/sup>/isg;
    $signature =~ s/(\[sub\])(.+?)(\[\/sub\])/<sub>$2<\/sub>/isg;
    $signature =~ s/(\[align=)(left|center|right)(\])(.+?)(\[\/align\])/<DIV Align=$2>$4<\/DIV>/isg;
    $signature =~ s/(\[SHADOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/SHADOW\])/<table width=$2 style="filter:shadow\(color=$4\, direction=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
    $signature =~ s/(\[GLOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/GLOW\])/<table width=$2 style="filter:glow\(color=$4\, strength=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
    $signature =~ s/(\[BLUR=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/BLUR\])/<table width=$2 style="filter:blur\(Add=0, direction=$4\, strength=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
    $signature =~ s/(\[FLIPH\])(.+?)(\[\/FLIPH\])/<table style="filter:flipH"><tr><td>$2<\/td><\/tr><\/table>/isg;
    $signature =~ s/(\[FLIPV\])(.+?)(\[\/FLIPV\])/<table style="filter:flipV"><tr><td>$2<\/td><\/tr><\/table>/isg;
    $signature =~ s/(\[INVERT\])(.+?)(\[\/INVERT\])/<table style="filter:invert"><tr><td>$2<\/td><\/tr><\/table>/isg;
    $signature =~ s/(\[xray\])(.+?)(\[\/xray\])/<table style="filter:xray"><tr><td>$2<\/td><\/tr><\/table>/isg;
    $signature =~ s/(\[MOVE\])(.+?)(\[\/Move\])/<MARQUEE>$2<\/MARQUEE>/isg;

    $signature =~ s|\{\{|\[|g;
    $signature =~ s|\}\}|\]|g;
    $signature =~ s/\&amp;/\&/ig;
    $signature =~ s/&quot\;/\"/ig;
    $signature =~ s/ \&nbsp;/　/ig;
    $signature =~ s/apasswordcookie/a\&\#112\;asswordcookies/isg;
    $signature =~ s/adminpass/admin\&\#112\;assword/isg;
    $signature =~ s/document.cookie/documents\&\#46\;cookie/isg;
    $signature =~ s/file:/file\&\#58\;/isg;
    $signature =~ s/onmouse/\&\#111\;nmouse/isg;
    $signature =~ s/onexit/\&\#111\;nexit/isg;
    $signature =~ s/onerror/\&\#111\;nerror/isg;
    $signature =~ s/membercode/memberc\&\#111\;de/isg;
    $signature =~ s/setmembers.cgi/setmembers\&\#46\;cgi/isg;
    return $signature;
}
sub smilecode {
    my $post = shift;
    $post = $post."\n";
    $post =~ s/([\s|\>|\;])\:\)\s/$1<img src=$imagesurl\/emoticons\/smile.gif width=16 height=16>/isg;
    $post =~ s/^\:\)\s/<img src=$imagesurl\/emoticons\/smile.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:-\)\s/$1<img src=$imagesurl\/emoticons\/smile.gif width=16 height=16>/isg;
    $post =~ s/^\:-\)\s/<img src=$imagesurl\/emoticons\/smile.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])8\)\s/$1<img src=$imagesurl\/emoticons\/smile.gif width=16 height=16>/isg;
    $post =~ s/^8\)\s/<img src=$imagesurl\/emoticons\/smile.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])8-\)\s/$1<img src=$imagesurl\/emoticons\/smile.gif width=16 height=16>/isg;
    $post =~ s/^8-\)\s/<img src=$imagesurl\/emoticons\/smile.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\;\)\s/$1<img src=$imagesurl\/emoticons\/wink.gif width=16 height=16>/isg;
    $post =~ s/^\;\)\s/<img src=$imagesurl\/emoticons\/wink.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\;P\s/$1<img src=$imagesurl\/emoticons\/wink.gif width=16 height=16>/isg;
    $post =~ s/^\;P\s/<img src=$imagesurl\/emoticons\/wink.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\;-\)\s/$1<img src=$imagesurl\/emoticons\/wink.gif width=16 height=16>/isg;
    $post =~ s/^\;-\)\s/<img src=$imagesurl\/emoticons\/wink.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\;-P\s/$1<img src=$imagesurl\/emoticons\/wink.gif width=16 height=16>/isg;
    $post =~ s/^\;-P\s/<img src=$imagesurl\/emoticons\/wink.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\;\(\s/$1<img src=$imagesurl\/emoticons\/sad.gif width=16 height=16>/isg;
    $post =~ s/^\;\(\s/<img src=$imagesurl\/emoticons\/sad.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:\(\s/$1<img src=$imagesurl\/emoticons\/sad.gif width=16 height=16>/isg;
    $post =~ s/^\:\(\s/<img src=$imagesurl\/emoticons\/sad.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\;-\(\s/$1<img src=$imagesurl\/emoticons\/sad.gif width=16 height=16>/isg;
    $post =~ s/^\;-\(\s/<img src=$imagesurl\/emoticons\/sad.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:-\(\s/$1<img src=$imagesurl\/emoticons\/sad.gif width=16 height=16>/isg;
    $post =~ s/^\:-\(\s/<img src=$imagesurl\/emoticons\/sad.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:-\?\s/$1<img src=$imagesurl\/emoticons\/confused.gif width=15 height=22>/isg;
    $post =~ s/^\:-\?\s/<img src=$imagesurl\/emoticons\/confused.gif width=15 height=22>/isg;
    $post =~ s/([\s|\>|\;])\?\:\(\s/$1<img src=$imagesurl\/emoticons\/confused.gif width=15 height=22>/isg;
    $post =~ s/^\\?\:\(\s/<img src=$imagesurl\/emoticons\/confused.gif width=15 height=22>/isg;
    $post =~ s/([\s|\>|\;])\?\:-\(\s/$1<img src=$imagesurl\/emoticons\/confused.gif width=15 height=22>/isg;
    $post =~ s/^\\?\:-\(\s/<img src=$imagesurl\/emoticons\/confused.gif width=15 height=22>/isg;
    $post =~ s/([\s|\>|\;])\:D\s/$1<img src=$imagesurl\/emoticons\/biggrin.gif width=16 height=16>/isg;
    $post =~ s/^\:D\s/<img src=$imagesurl\/emoticons\/biggrin.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\;D\s/$1<img src=$imagesurl\/emoticons\/biggrin.gif width=16 height=16>/isg;
    $post =~ s/^\;D\s/<img src=$imagesurl\/emoticons\/biggrin.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:-D\s/$1<img src=$imagesurl\/emoticons\/biggrin.gif width=16 height=16>/isg;
    $post =~ s/^\:-D\s/<img src=$imagesurl\/emoticons\/biggrin.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\;-D\s/$1<img src=$imagesurl\/emoticons\/biggrin.gif width=16 height=16>/isg;
    $post =~ s/^\;-D\s/<img src=$imagesurl\/emoticons\/biggrin.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])8o\s/$1<img src=$imagesurl\/emoticons\/shocked.gif width=15 height=15>/isg;
    $post =~ s/^8o\s/<img src=$imagesurl\/emoticons\/shocked.gif width=15 height=15>/isg;
    $post =~ s/([\s|\>|\;])8p\s/$1<img src=$imagesurl\/emoticons\/shocked.gif width=15 height=15>/isg;
    $post =~ s/^8p\s/<img src=$imagesurl\/emoticons\/shocked.gif width=15 height=15>/isg;
    $post =~ s/([\s|\>|\;])8-o\s/$1<img src=$imagesurl\/emoticons\/shocked.gif width=15 height=15>/isg;
    $post =~ s/^8-o\s/<img src=$imagesurl\/emoticons\/shocked.gif width=15 height=15>/isg;
    $post =~ s/([\s|\>|\;])8-p\s/$1<img src=$imagesurl\/emoticons\/shocked.gif width=15 height=15>/isg;
    $post =~ s/^8-p\s/<img src=$imagesurl\/emoticons\/shocked.gif width=15 height=15>/isg;
    $post =~ s/([\s|\>|\;])\&gt;\:\(\s/$1<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/^\&gt;\:\(\s/<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\&gt;\:&lt;\s/$1<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/^\&gt;\:&lt;\s/<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\&gt;\:-\(\s/$1<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/^\&gt;\:-\(\s/<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\&gt;\:-&lt;\s/$1<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/^\&gt;\:-&lt;\s/<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:&lt;\s/$1<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/^\:&lt;\s/<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:-&lt;\s/$1<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/^\:-&lt;\s/<img src=$imagesurl\/emoticons\/angry.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])8D\s/$1<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/^8D\s/<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:o\s/$1<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/^\:o\s/<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:0\s/$1<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/^\:0\s/<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])8-D\s/$1<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/^8-D\s/<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\:-o\s/$1<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/^\:-o\s/<img src=$imagesurl\/emoticons\/cheesy.gif width=16 height=16>/isg;
    $post =~ s/([\s|\>|\;])\^-\^\s/$1<img src=$imagesurl\/emoticons\/cool.gif width=21 height=15>/isg;
    $post =~ s/^\^-\^\s/<img src=$imagesurl\/emoticons\/cool.gif width=21 height=15>/isg;
    $post =~ s/([\s|\>|\;])\^_\^\s/$1<img src=$imagesurl\/emoticons\/cool.gif width=21 height=15>/isg;
    $post =~ s/^\^_\^\s/<img src=$imagesurl\/emoticons\/cool.gif width=21 height=15>/isg;
    $post =~ s/([\s|\>|\;])\:p\s/$1<img src=$imagesurl\/emoticons\/cool.gif width=21 height=15>/isg;
    $post =~ s/^\:p\s/<img src=$imagesurl\/emoticons\/cool.gif width=21 height=15>/isg;
    $post =~ s/([\s|\>|\;])\:-p\s/$1<img src=$imagesurl\/emoticons\/cool.gif width=21 height=15>/isg;
    $post =~ s/^\:-p\s/<img src=$imagesurl\/emoticons\/cool.gif width=21 height=15>/isg;
    return $post;
}
sub lbcode {
    my $post = shift;

    $post =~ s/javascript/\&\#106\;avascript/isg;
    $post =~ s/value/\&\#118\;alue/isg;
    $post =~ s/onmouse/\&\#111\;nmouse/isg;
    $post =~ s/FORM/\&\#70\;ORM/isg;

    if ($post =~/\[HTML\]/isg){
	$post1=$post;

	$post1 =~ s/(\[HTML\])(.+?)(\[\/HTML\])/<SPAN><IMG src=$imagesurl\/images\/code.gif align=absBottom> HTML 代码片段如下:<BR><TEXTAREA style=\"WIDTH: 94%; BACKGROUND-COLOR: #f7f7f7\" name=textfield rows=10>$2<\/TEXTAREA><BR><INPUT onclick=runEx() type=button value=运行此代码 name=Button> [Ctrl+A 全部选择   提示:你可先修改部分代码，再按运行]<\/SPAN><BR>/is;
	$post1=$2;
	$post1 =~ s/\&\#106\;avascript/javascript/isg;
	$post1 =~ s/\&\#118\;alue/value/isg;
	$post1 =~ s/\&\#111\;nmouse/onmouse/isg;
	$post1=~s /<br>/\n/sg;
	$post1=~s /<p>/\n\n/sg;
	$post1=&HTML($post1);
    	$post1 =~ s/</\&lt;/g;
    	$post1 =~ s/>/\&gt;/g;
    	$post1 =~ s/"/\&quot;/g;
	$post =~ s/(\[HTML\])(.+?)(\[\/HTML\])/<br><SPAN><IMG src=$imagesurl\/images\/code.gif align=absBottom> HTML 代码片段如下:<BR><TEXTAREA style=\"WIDTH: 94%; BACKGROUND-COLOR: #f7f7f7\" name=textfield rows=10>$post1<\/TEXTAREA><BR><INPUT onclick=runEx() type=button value=运行此代码 name=Button> [Ctrl+A 全部选择   提示:你可先修改部分代码，再按运行]<\/SPAN><BR>/is;
	$post =~ s/(\[HTML\])//isg;
	$post =~ s/(\[\/HTML\])//isg;
    }else{
	$post =~ s/\<p>/<br><br>/isg;
	$post =~ s|<br>| <br>|g;
	$post =~ s|\[hr\]\n|\<hr width=40\% align=left>|g;
	$post =~ s|\[hr\]|\<hr width=40\% align=left>|g;

	if ($quotemode eq 1) {
	    $post =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]/<blockquote><hr noshade>$1<blockquote><hr noshade size=1>$2<hr noshade size=1><\/blockquote>$3<\/font><hr noshade><\/blockquote>/isg;
	    $post =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]/<font face=$font><blockquote><hr noshade size=1>$1<hr noshade size=1><\/blockquote><\/font>/isg;
	}
	else {
            if ($count eq 1) {  $quoteback = $postcolortwo; } else { $quoteback = $postcolorone; }
	    $post =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]/<BR><table cellpadding=0 cellspacing=0 border=0 WIDTH=94\% bgcolor=#000000 align=center><tr><td><table width=100% cellpadding=5 cellspacing=1 border=0><TR><TD BGCOLOR=$quoteback>$1<\/td><\/tr><\/table><\/td><\/tr><\/table><BR>/isg;
	}
	$post =~ s|\[\[|\{\{|g;
	$post =~ s|\]\]|\}\}|g;
	$post =~ s|\n\[|\[|g;
	$post =~ s|\]\n|\]|g;
	$post =~ s/\[br\]/<br>/isg;

	if (($arrawpostpic eq "on")||($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo')) {
	    $post =~ s/\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/^(http|https|ftp):\/\/(\S+?\.png)/<a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/^(http|https|ftp):\/\/(\S+?\.bmp)/<a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/^(http|https|ftp):\/\/(\S+?\.gif)/<a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/^(http|https|ftp):\/\/(\S+?\.jpg)/<a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/\ (http|https|ftp):\/\/(\S+?\.png)/\ <a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/\ (http|https|ftp):\/\/(\S+?\.bmp)/\ <a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/\ (http|https|ftp):\/\/(\S+?\.gif)/\ <a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/\ (http|https|ftp):\/\/(\S+?\.jpg)/\ <a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/<br>(http|https|ftp):\/\/(\S+?\.png)/<br><a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/<br>(http|https|ftp):\/\/(\S+?\.bmp)/<br><a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/<br>(http|https|ftp):\/\/(\S+?\.gif)/<br><a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	    $post =~ s/<br>(http|https|ftp):\/\/(\S+?\.jpg)/<br><a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>screen.width-333)this.width=screen.width-333\"><\/a>/isg;
	}
	if (($arrawpostflash eq "on")||($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo')) {
	    $post =~ s/(\[swf\])\s*(http|https|ftp):\/\/(\S+?\.swf)\s*(\[\/swf\])/<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$2:\/\/$3 quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>/isg;
	    $post =~ s/(\[FLASH=)(\S+?)(\,)(\S+?)(\])\s*(http|https|ftp):\/\/\s*(\S+?\.swf)\s*(\[\/FLASH\])/<OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$2 HEIGHT=$4><PARAM NAME=MOVIE VALUE=$6:\/\/$7><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$6:\/\/$7 WIDTH=$2 HEIGHT=$4 PLAY=TRUE LOOP=TRUE QUALITY=HIGH><\/EMBED><\/OBJECT>/isg;
	    $post =~ s/^(http|https|ftp):\/\/(\S+?\.swf)/<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$1:\/\/$2 quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>/isg;
	    $post =~ s/\ (http|https|ftp):\/\/(\S+?\.swf)/\ <PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$1:\/\/$2 quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>/isg;
	    $post =~ s/<br>(http|https|ftp):\/\/(\S+?\.swf)/<br><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$1:\/\/$2 quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>/isg;
	}
	if (($arrawpostfontsize eq "on")||($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo')) {
	    $post =~ s/\[size=\s*(.*?)\s*\]/<font size=$1>/isg;
	    $post =~ s/\[\/size\]/<\/font>/isg;
	    $post =~ s/\[\/font\]/<\/font>/isg;
	}

	if (($arrawpostsound eq "on")||($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo')) {
	    $post =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.wav)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/mid.gif width=16 height=16 alt=MIDI音乐>/isg;
	    $post =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.mid)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/wave.gif width=16 height=16 alt=WAVE音乐>/isg;
	    $post =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.midi)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/wave.gif width=16 height=16 alt=WAVE音乐>/isg;
	}

        if (($arrawpostreal eq "on")||($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo')) {
	    $post =~ s/(\[ra\])(\S+?)(\[\/ra\])/<center><object classid="clsid:CFCDAA03-8BE4-11CF-B84B-0020AFBBCCFA" id="RAOCX" width="320" height="70"><param name="_ExtentX" value="6694"><param name="_ExtentY" value="1588"><param name="AUTOSTART" value="0"><param name="SHUFFLE" value="0"><param name="PREFETCH" value="0"><param name="NOLABELS" value="0"><param name="SRC" value="$2"><param name="CONTROLS" value="StatusBar,ControlPanel"><param name="LOOP" value="0"><param name="NUMLOOP" value="0"><param name="CENTER" value="0"><param name="MAINTAINASPECT" value="0"><param name="BACKGROUNDCOLOR" value="#000000"><embed src="$2" width="320" autostart="true" height="70"><\/object>/isg;
	    $post =~ s/(\[rm\])(\S+?)(\[\/rm\])/<center><object CLASSID=clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA HEIGHT=300 ID=Player WIDTH=380 VIEWASTEXT><param NAME="_ExtentX" VALUE="12726"><param NAME="_ExtentY" VALUE="8520"><param NAME="AUTOSTART" VALUE="0"><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="ImageWindow"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="$2"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><\/object><br><object CLASSID=clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA HEIGHT=32 ID=Player WIDTH=380 VIEWASTEXT><param NAME="_ExtentX" VALUE="18256"><param NAME="_ExtentY" VALUE="794"><param NAME="AUTOSTART" VALUE="0"><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="controlpanel"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="0"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><param NAME="SRC" VALUE="$2"><\/object>/isg;
	}
	else{$post =~ s/(\[ra\])(\S+?)(\[\/ra\])/<b>这个分论坛不允许贴 RealPlayer 音乐/isg;
	     $post =~ s/(\[rm\])(\S+?)(\[\/rm\])/<b>这个分论坛不允许贴 RealPlayer 影片/isg;
	}
	if (($arrawpostmedia eq "on")||($membercode eq 'mo' || $membercode eq 'ad' || $inmembmod eq 'yes' || $membercode eq 'smo')) {
	    $post =~ s/(\[wma\])(\S+?)(\[\/wma\])/<b>这个是 Windows Media Player 音乐：<\/b><br><center><embed type="application\/x-mplayer2" pluginspage="http:\/\/www.microsoft.com\/Windows\/Downloads\/Contents\/Products\/MediaPlayer\/" src="$2" name="realradio" showcontrols=1 ShowDisplay=0 ShowStatusBar=1 width="320" height="70" autostart="0"><\/embed><\/center>/isg;
	    $post =~ s/(\[wmv\])(\S+?)(\[\/wmv\])/<b>这个是 Windows Media Player 影片：<\/b><br><center><EMBED id="videowindow1" name="videowindow1" src="$2" width="380" height="300" AutoStart=0 ><\/EMBED><\/center>/isg;
	}
	else{$post =~ s/(\[wma\])(\S+?)(\[\/wma\])/<b>这个分论坛不允许贴 Windows Media Player 音乐/isg;
	     $post =~ s/(\[wmv\])(\S+?)(\[\/wmv\])/<b>这个分论坛不允许贴 Windows Media Player 影片/isg;
	}

        $post =~ s/\[mms\](.*?)\[\/mms\]/<img src=$imagesurl\/images\/music.gif width=16 height=16 alt="WM 类数据流音乐" align=absmiddle> <a href="$1">$1<\/a>/isg;
	$post =~ s/\[mms=(.*?)\](.*?)\[\/mms\]/<img src=$imagesurl\/images\/music.gif width=16 height=16 alt="WM 类数据流音乐" align=absmiddle> <a href="$1">$2<\/a>/isg;
        $post =~ s/\[rtsp\](.*?)\[\/rtsp\]/<img src=$imagesurl\/images\/ra.gif width=16 height=16 alt="Real 类数据流" align=absmiddle> <a href="$1">$1<\/a>/isg;
	$post =~ s/\[rtsp=(.*?)\](.*?)\[\/rtsp\]/<img src=$imagesurl\/images\/ra.gif width=16 height=16 alt="Real 类数据流" align=absmiddle> <a href="$1">$2<\/a>/isg;

	$post =~ s/\[url\](\[\S+\])(\S+?)(\[\S+\])\[\/url\]/<a href=$2 target=_blank>$1$2$3<\/a>/isg;
	$post =~ s/\[url=(http|https|ftp):\/\/(\S+?)\]/<a href=$1:\/\/$2 target=_blank>/isg;
	$post =~ s/\[url=(\S+?)\]/<a href=http:\/\/$1\ target=_blank>/isg;
	$post =~ s/\[url=\s*(.*?)\s*\]\s*(.*?)\s*\[\/url\]/<a href=$1 target=_blank>$2<\/a>/isg;
	$post =~ s/\[url\]\s*(http|https|ftp):\/\/(.*?)\s*\[\/url\]/<a href=$1:\/\/$2 target=_blank>$1:\/\/$2<\/a>/isg;
	$post =~ s/\[url\]\s*(.*?)\s*\[\/url\]/<a href=http:\/\/$1 target=_blank>$1<\/a>/isg;
	$post =~ s/\[\/url\]/<\/a>/isg;
	$post =~ s/(\[email\])(\S+\@\S+?)(\[\/email\])/<A HREF="mailto:$2">$2<\/A>/isg;
	$post =~ s/\ (http|https|ftp):\/\/(\S+?)\ / <a href=$1:\/\/$2\ target=_blank>$1\:\/\/$2<\/a> /isg;
	$post =~ s/<br>(http|https|ftp):\/\/(\S+?)\ /<br><a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
	$post =~ s/^(http|https|ftp):\/\/(\S+?)\ /<a href=$1:\/\/$2 target=_blank>$1\:\/\/$2<\/a> /isg;
	$post =~ s/\ www\.(\S+?)\ / <a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
	$post =~ s/<br>www\.(\S+?)\ /<br><a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
	$post =~ s/^www\.(\S+?)\ /<a href=http:\/\/www.$1 target=_blank>www.$1<\/a> /isg;
	$post =~ s/\[b\]/<b>/isg;
	$post =~ s/\[\/b\]/<\/b>/isg;
	$post =~ s/\[i\]/<i>/isg;
	$post =~ s/\[\/i\]/<\/i>/isg;
	$post =~ s/\[font=\s*(.*?)\s*\]/<font face=$1>/isg;
	$post =~ s/\[u\]/<u>/isg;
	$post =~ s/\[\/u\]/<\/u>/isg;
	$post =~ s/\[color=(\S+?)\]/<font color=$1>/isg;
	$post =~ s/\[\/color\]/<\/font>/isg;
	$post =~ s/\[\/font\]/<\/font>/isg;
	$post =~ s/\\(http|https|ftp):\/\/(\S+)/<a href=$1:\/\/$2 target=_blank>$1:\/\/$2<\/a>/isg;
	$post =~ s/(\[list\])(.+?)(\[\/list\])/<ul>$2<\/ul>/isg;
	$post =~ s/(\[list=s\])(.+?)(\[\/list\])/<ol type="square">$2<\/ol>/isg;
	$post =~ s/(\[list=)(A|1|I)(\])(.+?)(\[\/list\])/<OL TYPE=$2>$4<\/OL>/isg;
	$post =~ s/(\[list=)(\S+?)(])(.+?)(\[\/list\])/ <ol start="$2">$4<\/ol>/isg;
	$post =~ s/\[\*\]/<li>/isg;
	$post =~ s/\[email=(\S+?)\]/<a href=mailto:$1>/isg;
	$post =~ s/\[\/email\]/<\/a>/isg;
	$post =~ s/<br>(\w+\@\w+\.\w+)/<br><A HREF=mailto:$1>$1<\/A>/isg;
	$post =~ s/^(\w+\@\w+\.\w+)/<A HREF=mailto:$1>$1<\/A>/isg;
	$post =~ s/\\(\w+\@\w+\.\w+)/<A HREF=mailto:$1>$1<\/A>/isg;
	$post =~ s/(\[fly\])(.+?)(\[\/fly\])/<marquee width=90% behavior=alternate scrollamount=3>$2<\/marquee>/isg;
	$post =~ s/(\[s\])(.+?)(\[\/s\])/<s>$2<\/s>/isg;
	$post =~ s/(\[sup\])(.+?)(\[\/sup\])/<sup>$2<\/sup>/isg;
	$post =~ s/(\[sub\])(.+?)(\[\/sub\])/<sub>$2<\/sub>/isg;
	$post =~ s/(\[align=)(left|center|right)(\])(.+?)(\[\/align\])/<DIV Align=$2>$4<\/DIV>/isg;
	$post =~ s/(\[SHADOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/SHADOW\])/<table width=$2 style="filter:shadow\(color=$4\, direction=$6)"><tr><td>$8<\/td><\/tr>s<\/table>/isg;
	$post =~ s/(\[GLOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/GLOW\])/<table width=$2 style="filter:glow\(color=$4\, strength=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
	$post =~ s/(\[BLUR=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/BLUR\])/<table width=$2 style="filter:blur\(Add=0, direction=$4\, strength=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
	$post =~ s/(\[FLIPH\])(.+?)(\[\/FLIPH\])/<table style="filter:flipH"><tr><td>$2<\/td><\/tr><\/table>/isg;
	$post =~ s/(\[FLIPV\])(.+?)(\[\/FLIPV\])/<table style="filter:flipV"><tr><td>$2<\/td><\/tr><\/table>/isg;
	$post =~ s/(\[INVERT\])(.+?)(\[\/INVERT\])/<table style="filter:invert"><tr><td>$2<\/td><\/tr><\/table>/isg;
	$post =~ s/(\[xray\])(.+?)(\[\/xray\])/<table style="filter:xray"><tr><td>$2<\/td><\/tr><\/table>/isg;
	$post =~ s/(\[MOVE\])(.+?)(\[\/Move\])/<MARQUEE scrollamount=3>$2<\/MARQUEE>/isg;

	if ($openiframe eq "yes") {
	    $post =~ s/(\[iframe\])(.+?)(\[\/iframe\])/<IFRAME SRC='$2' FRAMEBORDER=0 ALLOWTRANSPARENCY="true" SCROLLING="YES" WIDTH="100%" HEIGHT=340><\/IFRAME><br><br><a href="$2" target="_blank">Netscape 用户点这儿察看<\/a>/isg;
	}

	$post =~ s|\{\{|\[|g;
	$post =~ s|\}\}|\]|g;
	if ($post =~/\[code\]/isg){
	    $post1=$post;
	    $post1 =~ s/\[code\](.+?)\[\/code\]/<blockquote><font face=$font>代码：<\/font><hr><font face=$font><pre>$1<\/pre><\/font><hr><\/blockquote>/is;
	    $post1=$1;
	    $post1=&unHTML($1);
	    open(PERL,"<${lbdir}data/perl.dat");
	    @perlcodes = <PERL>;
	    close(PERL);
	    chomp(@perlcodes);
	    @bluecodes = split(/ /,$perlcodes[0]);
	    foreach(@bluecodes) {
		$post1 =~ s/(^|[\s\x7E\x21\x40\x24\x25\x5E\x26\x2A\x28\x29\x2B\x3D\x7C\x2F\x5C\x7B\x7D\x5B\x5D\x3A\x3B\x22\x27\x3C\x3E\x2C\x2E\x3F])($_)([\s\x7E\x21\x40\x24\x25\x5E\x26\x2A\x28\x29\x2B\x3D\x7C\x2F\x5C\x7B\x7D\x5B\x5D\x3A\x3B\x22\x27\x3C\x3E\x2C\x2E\x3F]|$)/$1<font color=0000FF>$2<\/font>$3/isg;
	    }
	    @bluecodes = ();
	    @redcodes = split(/ /,$perlcodes[1]);
	    foreach(@redcodes) {
		$post1 =~ s/(^|[\s\x7E\x21\x40\x24\x25\x5E\x26\x2A\x28\x29\x2B\x3D\x7C\x2F\x5C\x7B\x7D\x5B\x5D\x3A\x3B\x22\x27\x3C\x3E\x2C\x2E\x3F])($_)([\s\x7E\x21\x40\x24\x25\x5E\x26\x2A\x28\x29\x2B\x3D\x7C\x2F\x5C\x7B\x7D\x5B\x5D\x3A\x3B\x22\x27\x3C\x3E\x2C\x2E\x3F]|$)/$1<font color=FF0000>$2<\/font>$3/isg;
	     }
	    @redcodes = ();
	    @orangecodes = split(/ /,$perlcodes[2]);
	    @perlcodes = ();
	    foreach(@orangecodes) {
		$post1 =~ s/(^|[\s\x7E\x21\x40\x24\x25\x5E\x26\x2A\x28\x29\x2B\x3D\x7C\x2F\x5C\x7B\x7D\x5B\x5D\x3A\x3B\x22\x27\x3C\x3E\x2C\x2E\x3F])($_)([\s\x7E\x21\x40\x24\x25\x5E\x26\x2A\x28\x29\x2B\x3D\x7C\x2F\x5C\x7B\x7D\x5B\x5D\x3A\x3B\x22\x27\x3C\x3E\x2C\x2E\x3F]|$)/$1<font color=FF8000>$2<\/font>$3/isg;
	    }
	    $post1=~s /\&lt;br\&gt;/\n/sg;
	    $post1=~s /\&lt;p\&gt;/\n\n/sg;
	    $post1 =~ s/\&amp;/\&/g;
	    $post1 =~ s/&<font color=FF8000>gt<\/font>;/&gt;/isg;
	    $post1 =~ s/&<font color=FF8000>lt<\/font>;/&lt;/isg;
	    $post1=~s /\&lt;br\&gt;/<br>/sg;

	    $post =~ s/\[code\](.+?)\[\/code\]/<blockquote><font face=$font>代码：<\/font><hr><font face=$font><pre>$post1<\/pre><\/font><hr><\/blockquote>/is;
	    $post =~ s/\[code\](.+?)\[\/code\]//isg;
	}
    }
    $post =~ s/apasswordcookie/a\&\#112\;asswordcookies/isg;
    $post =~ s/adminpass/admin\&\#112\;assword/isg;
    $post =~ s/document.cookie/documents\&\#46\;cookie/isg;
    $post =~ s/file:/file\&\#58\;/isg;
    $post =~ s/onmouse/\&\#111\;nmouse/isg;
    $post =~ s/onexit/\&\#111\;nexit/isg;
    $post =~ s/onerror/\&\#111\;nerror/isg;
    $post =~ s/membercode/memberc\&\#111\;de/isg;
    $post =~ s/setmembers.cgi/setmembers\&\#46\;cgi/isg;
    return $post;
}
1;
