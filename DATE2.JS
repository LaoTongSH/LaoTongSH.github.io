<!--
//---------
   var enabled = 0;   today = new Date();
   var day;   var date;
   if(today.getDay()==0)     day = "日"
   if(today.getDay()==1)     day = "一"
   if(today.getDay()==2)     day = "二"
   if(today.getDay()==3)     day = "三"
   if(today.getDay()==4)     day = "四"
   if(today.getDay()==5)     day = "五"
   if(today.getDay()==6)     day = "六"
   document.fgColor = " FF0072";
   date2 = "<font  color=red>" +  day + "</font>";
   document.write("<center>" +date2.fontsize(1) +  "</center>");
 
// -->
