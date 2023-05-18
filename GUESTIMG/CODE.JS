var Quote = 0;
var Bold  = 0;
var Italic = 0;
var Underline = 0;
var Code = 0;
var text_enter_url      = "请输入主页地址";
var text_enter_fly      = "请输入文字";
var text_enter_move      = "请输入文字";
var text_enter_col      = "使文字产生光晕效果.用法: [GLOW=宽度, 颜色, 边界]要产生光晕效果的文字[/GLOW]";
var text_enter_image    = "请输入图片地址";
var text_enter_email    = "请输入邮件地址";
var error_no_url        = "您必须输入地址";
var error_no_fly        = "您必须输入文字";
var error_no_move        = "您必须输入文字";
var error_no_col        = "您必须输入各项参数!";
var error_no_title      = "您必须输入主页标题";
var error_no_email      = "您必须输入邮件地址";
function textiWrite(NewCode) {
document.form.texti.value+=NewCode;
document.form.texti.focus();
return;
}
function fly() {
var FoundErrors = '';
var enterTXT   = prompt(text_enter_fly, "文字");
if (!enterTXT)    {
FoundErrors += "\n" + error_no_fly;
}
if (FoundErrors)  {
alert("错误!"+FoundErrors);
return;
}
var ToAdd = "[fly]"+enterTXT+"[/fly]";
document.form.texti.value+=ToAdd;
document.form.texti.focus();
}
function move() {
var FoundErrors = '';
var enterTXT   = prompt(text_enter_move, "文字");
if (!enterTXT)    {
FoundErrors += "\n" + error_no_move;
}
if (FoundErrors)  {
alert("错误!"+FoundErrors);
return;
}
var ToAdd = "[move]"+enterTXT+"[/move]";
document.form.texti.value+=ToAdd;
document.form.texti.focus();
}
function glow() {
var FoundErrors = '';
var enterURL   = prompt(text_enter_col, "文字");
var enterCOL   = prompt(text_enter_col, "255,red,2");
if (!enterURL||!enterCOL)    {
FoundErrors += "\n" + error_no_col;
}
if (FoundErrors)  {
alert("错误!"+FoundErrors);
return;
}
var ToAdd = "[glow="+enterCOL+"]"+enterURL+"[/glow]";
document.form.texti.value+=ToAdd;
document.form.texti.focus();
}
function YBBCurl() {
var FoundErrors = '';
var enterURL   = prompt(text_enter_url, "http://");
if (!enterURL)    {
FoundErrors += "\n" + error_no_url;
}
if (FoundErrors)  {
alert("错误!"+FoundErrors);
return;
}
var ToAdd = "[URL="+enterURL+"]"+enterURL+"[/URL]";
document.form.texti.value+=ToAdd;
document.form.texti.focus();
}
function YBBCimage() {
var FoundErrors = '';
var enterURL   = prompt(text_enter_image, "http://");
if (!enterURL) {
FoundErrors += "\n" + error_no_url;
}
if (FoundErrors) {
alert("错误!"+FoundErrors);
return;
}
var ToAdd = "[IMG]"+enterURL+"[/IMG]";
document.form.texti.value+=ToAdd;
document.form.texti.focus();
}
function YBBCemail() {
var emailAddress = prompt(text_enter_email,"");
if (!emailAddress) { alert(error_no_email); return; }
var ToAdd = "[EMAIL]"+emailAddress+"[/EMAIL]";
textiWrite(ToAdd);
}
function YBBCbold() {
if (Bold == 0) {
ToAdd = "[B]";
document.form.bold.value = " B*";
Bold = 1;
} else {
ToAdd = "[/B]";
document.form.bold.value = " B ";
Bold = 0;
}
textiWrite(ToAdd);
}
function YBBCitalic() {
if (Italic == 0) {
ToAdd = "[I]";
document.form.italic.value = " I*";
Italic = 1;
} else {
ToAdd = "[/I]";
document.form.italic.value = " I ";
Italic = 0;
}
textiWrite(ToAdd);
}
function YBBCunder() {
if (Underline == 0) {
ToAdd = "[U]";
document.form.under.value = " U*";
Underline = 1;
} else {
ToAdd = "[/U]";
document.form.under.value = " U ";
Underline = 0;
}
textiWrite(ToAdd);
}