#------------------------------------------------------#
#                                                      #
#              本程序为 中国CGI之家 提供	           #
#              Ajie的留言板多用户版V4.0                #
#------------------------------------------------------#

$insidejs = qq~
<INPUT title="加粗" onclick=YBBCbold() type=button value=" B " name=bold class=input2>
<INPUT title="倾斜" onclick=YBBCitalic() type=button value=" I " name=italic class=input2>
<INPUT title="下划线" onclick=YBBCunder() type=button value=" U " name=under class=input2>
<INPUT title="超链接" onclick=YBBCurl() type=button value=" 链接 " class=input2>
<INPUT title="EMAIL" onclick=YBBCemail() type=button value=" 邮箱 " class=input2>
<INPUT title="图片" onclick=YBBCimage() type=button value=" 图片 " class=input2>
<INPUT title="使文字飞行" onclick=fly() type=button value=" 飞 " class=input2>
<INPUT title="使文字产生移动效果" onclick=move() type=button value=" 移 " class=input2>
<INPUT title="产生光晕效果的文字" onclick=glow() type=button value=" 光 " class=input2>
~;