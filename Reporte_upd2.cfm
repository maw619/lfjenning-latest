<!DOCTYPE html>
<html lang="en">
<head>
  <title>L.F. Jennings</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" type="text/css"  rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"  type="text/css"  rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js" integrity="sha512-GsLlZN/3F2ErC5ifS5QtgpiJtWd43JWSuIgh7mbzZ8zBps+dvLusV+eNQATqgA/HdeKFVgA5v3S/cIrLF7QnIg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>


<link rel="stylesheet" href="style.css">



<style>
@media print{
   #footer { 
    
  }
  
 img {
      image-orientation: from-image !important; /* Use EXIF data from the image */
}

body {
  /* Set "my-sec-counter" to 0 */
  counter-reset: my-sec-counter;
}

}
@page {
    margin:.5cm;
    
  }
    
* {
    -webkit-print-color-adjust: exact !important;   /* Chrome, Safari 6 – 15.3, Edge */
    color-adjust: exact !important;                 /* Firefox 48 – 96 */
    print-color-adjust: exact !important;           /* Firefox 97+, Safari 15.4+ */
}

body {
  /* Set "my-sec-counter" to 0 */
  counter-reset: my-sec-counter;
}

#footer::before {
  /* Increment "my-sec-counter" by 1 */
  counter-increment: my-sec-counter;
  content: counter(my-sec-counter) " / ";

}
  
#footer{
  height:6vh;
  border-top:3px solid black;
  text-align: right;
  font-size:medium;
  page-break-after: always !important; 
   
}

#box1{
  height:94vh;
    
}
img{
  max-height:400px;
}

#resize{
  max-height:350px;
  padding:2px;
  page-break-after: avoid !important; 
}




   </style>


</head>




  <CFSET GetUser.RecordCount=0>
  <CFQUERY NAME="GetUser" datasource="wolffdb_dsn">
    SELECT  *          
    FROM  Usuarios
    WHERE user_name = <cfqueryparam value="#URL.ws_id#" cfsqltype="cf_sql_nvarchar">

     
  </CFQUERY>
   

  <CFIF GetUser.RecordCount EQ 1>
    <CFSET SESSION.Auth = StructNew()>
    <CFSET SESSION.Auth.IsLoggedIn        = "Yes">
    <CFSET SESSION.Auth.user_key          = GetUser.user_key>
    <CFSET SESSION.Auth.user_name         = GetUser.user_name>
    <CFSET SESSION.Auth.user_password     = GetUser.user_password>
    <CFSET SESSION.Auth.user_nombre       = GetUser.user_nombre>
    <CFSET SESSION.Auth.user_apellido     = GetUser.user_apellido>       
    <CFSET SESSION.Auth.email             = GetUser.user_email>  
    <CFSET SESSION.Auth.user_role         = GetUser.user_role>
  </cfif>


  <cfif isDefined("form.Criteria")>
    <cfset url.Criteria = trim(form.Criteria)>
 </cfif> 
 
 
 <cfset GetRep.RecordCount=0>
 <cfquery name="GetRep" datasource="wolffdb_dsn">
   Select *
   From LF_Reportes inner join LF_Projects on 
            rep_fk_pr_key = pr_key inner join LF_Employees on
            rep_fk_emp_key = emp_key
       Where rep_key = <cfqueryparam value="#URL.claveU#" cfsqltype="cf_sql_numeric">     
    
 </cfquery>

<cfset GetEmp.RecordCount=0>
<cfquery name="GetEmp" datasource="wolffdb_dsn">
 Select *
   From LF_Reportes inner join  LF_Employees on
        rep_fk_emp_key_sup = emp_key
        inner join LF_Projects on 
        rep_fk_pr_key = pr_key
   Where rep_key =  #GetRep.rep_key#  
  order by emp_name  
</cfquery>


<!----------------------------------------------------- HTML starts here --------------------------------------------------------------------------------------->
<cfif #TRIM(GetRep.rep_notes)# neq "">
     <cfset pagesTotal = #GetRep.rep_pages# + 4>
<cfelse>
     <cfset pagesTotal = #GetRep.rep_pages# + 3>
</cfif>
<body id="body">



<div class="container text-center" id="container">   


<div id="box1">

<cfoutput>
  <!---  Page 1 ---------------------------------------------------------------->
<img src="./jennings3.png" class="img-fluid" id="banner">
<div id="line" style="margin-bottom:15px;"></div>
    <cfset ws_phone = 0> 
    <cfif #GetRep.emp_phone# GT 0>		
          <cfset ws_phone = #GetRep.emp_phone#>
        <cfset areacode = left(ws_phone, 3)>
        <cfset firstthree = mid(ws_phone, 4, 3)>
        <cfset lastfour = right(ws_phone, 4)>
        <cfset ws_phone = "(#areacode#) " & "#firstthree#" & "-" & "#lastfour#"> 
    </cfif> 
<cfoutput>

<p class="fs-6">#GetRep.rep_yyyymmdd#</p>
<p class="fs-6">To: #GetRep.rep_ws_to#</p>
<p class="fs-6">From: #GetRep.emp_name#</p>
<br>

<p class="fs-6 text-wrap">This report is a follow up to the safety inspection completed on #GetRep.rep_yyyymmdd#. The
      purpose of the inspection was to identify potential safety hazards and/or OSHA violations.<br>
      Attached is a list of observations and recommendations based on the conditions present at the 
      time of my visit. Please review the report and verify that all potential hazards are corrected. <br>
      If you have any questions or require additional information after reviewing this report, please
      don't hesitate to contact me.</p>
<p class="fs-6" id="no-space">Sincerely, </p><br>
<p class="fs-6" id="no-space">#GetRep.emp_name#</p>
<p class="fs-6" id="no-space"> LF Jennings, Inc.</p>
<p class="fs-6" id="no-space"> Safety Department</p>
<p class="fs-6" id="no-space"><cfif ws_phone neq 0>#ws_phone#<br></cfif>#GetRep.emp_email#</p>
</cfoutput> 

</div>


<div id="footer" style="white-space: nowrap;"><cfoutput>#pagesTotal#</cfoutput></div>
<!---  Page 1 end ---------------------------------------------------------------->





<!---  Page 2 ---------------------------------------------------------------->

<div id="box1">
<img src="./jennings3.png" class="img-fluid" id="banner">
<div id="line" style="margin-bottom:15px;"></div>
 <CFSET ws_fechaW = DateFormat(Now(),"mm/dd/yyyy")><cfoutput>#ws_fechaW#</cfoutput></p>



<cfoutput> 
  <div class="card" style="width:100%; border-color:transparent;">
  <div class="card-body">
  <h3 class="card-title">Project Safety Inspection</h3>
  <h2 class="card-title"><strong>#GetRep.pr_desc#</strong></h2>
    <p class="card-text">Reported by: #GetRep.emp_name# </p>
   <p class="card-text">On-site Supervisor: #GetEmp.emp_name#</p>
   <p class="card-text">Scope of inspection: #GetRep.rep_desc#</p>
   <!--- <p class="card-text">Number Reported: #GetRep.rep_pages#</p> --->
  </div>
</div>
</cfoutput> 
</div>

<div id="footer" style="white-space: nowrap;"><cfoutput>#pagesTotal#</cfoutput></div>
<!---  Page 2 end ---------------------------------------------------------------->





<!----------------------------------- not html ----------------------------------->
  <cfset GetFoto.RecordCount=0>   
	<cfquery name="GetFoto" datasource="wolffdb_dsn">
	  Select *
		From LF_Photos left join LF_Reportes on 
             ph_fk_rep_key = rep_key
             left join LF_Photos2 on 
             ph_key = ph_fk_ph_key  
        where ph_fk_rep_key = #GetRep.rep_key#    
          and rep_user_name = '#SESSION.Auth.user_name#'   
          and ph_user_name = '#SESSION.Auth.user_name#'
		order by ph_yyyymmdd
	</cfquery>
<cfset ws_page = 0>
<cfloop query="GetFoto">
<!----------------------------------- not html ----------------------------------->









<!---  Page 3 ---------------------------------------------------------------->


<div id="box1">
  <table  class="table" width="100%">
    
    <cfset ws_page = ws_page + 1>
       <img src="./jennings3.png" class="img-fluid" id="banner">
        <div id="line" style="margin-bottom:15px;"></div>


<script type="text/javascript" language="JavaScript">
<cfoutput>
var #toScript(ws_page, "jsvar")#;


</cfoutput>

console.log(jsvar)
</script>
      <br><br>  



<script>


</script>
    <strong><p id="shaded" style="background:rgba(0,0,0,.2)">Observation <cfoutput>#ws_page#</cfoutput></p></strong> 
     
  <tr>
    <td colspan="3">
        #GetFoto.ph_obs#
    </td>
  </tr>
  <tr>
    <td colspan="3">
        #GetFoto.ph_desc#
    </td>
  </tr>

  <cfif #TRIM(GetFoto.ph_key)# eq #TRIM(GetFoto.ph_fk_ph_key)#>
    <tr>
    <td>
           
  
            




<div class="container text-center">
  <div class="row">
    <div class="col">
      <a href="#TRIM(GetFoto.ph_link)#"><img class="img-fluid" src="#TRIM(GetFoto.ph_link)#" id="resize"></a>
    </div>
    <div class="col">
   <a href="#TRIM(GetFoto.ph_link2)#"><img class="img-fluid" src="#TRIM(GetFoto.ph_link2)#" id="resize"></a>
    </div>
  </div>
</div>


    </td>  
    <td>
     
    </td>
   </tr> 
  <cfelse> 
  <tr>  
    <td colspan="3">
      <a href="#TRIM(GetFoto.ph_link)#"><img class="img-fluid" src="#TRIM(GetFoto.ph_link)#" id="resize" ></a>
    </td>
</tr>
</cfif>
</table>

</div>

<div id="footer" style="white-space: nowrap;"><cfoutput>#pagesTotal#</cfoutput></div>
<!---  Page 3 end ---------------------------------------------------------------->


<button onclick="topFunction()" id="myBtn" title="Go to top">Top</button> 

</cfloop>  



<!---  Page 4 ---------------------------------------------------------------->
<cfif #TRIM(GetRep.rep_notes)# neq "">
  
<div id="box1">
<img src="./jennings3.png" class="img-fluid">
        <div id="line" style="margin-bottom:15px;"></div>
<table class="table" width="100%"> 
<tr>
  <td>
    #TRIM(GetRep.rep_notes)#
  </td>
</tr>
</table>
</div>

<div id="footer" style="white-space: nowrap;"><cfoutput>#pagesTotal#</cfoutput></div>
</cfif>
 <!---  Page 4 end ---------------------------------------------------------------->



  <!---  Page 5 ---------------------------------------------------------------->

<div id="box1">
<img src="./jennings3.png" class="img-fluid" id="banner">
        <div id="line" style="margin-bottom:15px;"></div>
<table class="table">
  <tr><td>
    <br><br>
  Submitted by: <br>

  #GetRep.emp_name# <br><br>
  L.F. Jennings.<br>
  Safety Department<br>
  <cfif ws_phone neq 0>
  #ws_phone#<br>
  </cfif>    
  #GetRep.emp_email#
</td></tr>
</table>
</div>
</cfoutput>
</div>
<div class="container">
<div id="footer" class="footer" ><cfoutput>#pagesTotal#</cfoutput></div>
</div>
 <!---  Page 5 end ---------------------------------------------------------------->

</div>  <!---  container --->

</body>


<script>
// Get the button
let mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
</script>

<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/0.5.0-beta4/html2canvas.min.js"></script>

<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js" integrity="sha384-oBqDVmMz9ATKxIep9tiCxS/Z9fNfEXiDAYTujMAeBAsjFuCZSmKbSSUnQlmh/jp3" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.min.js" integrity="sha384-IDwe1+LCz02ROU9k972gdyvl+AESN10+x7tBKgc9I5HFtuNz0wWnPclzo6p9vxnk" crossorigin="anonymous"></script>

<script>
function printIt() {
  source = document.getElementsByClassName("footer");
  show = document.getElementsByClassName("footer");

  for(var i = 0; i < source.length; i++)
	show[0].innerHTML =  source[i].innerHTML;
     
    var wnd = window.top;
    wnd.print();
    
}
printIt()
  </script>
  
<script>

</script>
<script>

</script>

</html>
