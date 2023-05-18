document.write('<body onload="play()">')
var count=0
function play(){
msg=borba.innerText
comp=msg.length
type()
}
function type(){
if(count<=comp){
borba.innerText=msg.substring(0,count)
count++
setTimeout("type()",150)}
else{
count=0
play()
}}
document.write('<SPAN id="borba" style="HEIGHT: 210px; WIDTH: 220px; Z-INDEX: 1">')
document.write('我是人间的精灵<BR>')
document.write('穿越黑夜在你的心上飞行<br>')
document.write('不管你身在何处<br>')
document.write('你我都同行。<br><BR>')
document.write('</SPAN>')
