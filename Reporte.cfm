<!DOCTYPE html>
<html lang="en">
<head>
  <title>L.F. Jennings</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  
	 <link rel="stylesheet" type="text/css" href="../Paginas/my.css">

</head>
<body>
 

  <cfif NOT (IsDefined("SESSION.Auth.IsLoggedIn") AND SESSION.Auth.IsLoggedIn)>
    <cflocation url="https://www.keybyme.com"> 
  </cfif>  

  <cfif isDefined("form.Criteria")>
    <cfset url.Criteria = trim(form.Criteria)>
 </cfif> 

<div class="container-fluid text-center">    
  <div class="row content">

	  
    <div class="col-sm-8 text-left"> 
       
      <p>
		<div>

		
 
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
      Where rep_key =  #GetRep.rep_key#  
       
  </cfquery>

 <center>
  <table>
    <tr>
      <td align="center">
        <a href="index.cfm">
        <img src="Images/jennings.png" width="90" height="90" alt=""/></a>
      </td>
      <td align="right">
        <strong>LF Jennings, Inc.</strong> <br>
407 N.Washington Street  <br>
Falls Church, VA 22046

      </td>
      <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
      <td>
        <CFSET ws_fechaW = DateFormat(Now(),"mm-dd-yyyy")>   
        <cfoutput><strong>#ws_fechaW#</strong></cfoutput><br>
      </td>
    </tr>
  </table>
				    	<h2> <cfoutput>#GetRep.rep_name#</cfoutput> </h2>
	                
<table border="2" bordercolor="#blue">
   <cfoutput>
     <tr> 
        <td>Project</td>  
        <td>#GetRep.pr_desc#</td>       
    </tr> 
	
    <tr> 
        <td>Report By:</td>  
        <td>#GetRep.emp_name#</td>       
    </tr> 

    <tr> 
        <td>On-site Supervisor:</td>  
        <td>#GetEmp.emp_name#</td>       
    </tr> 

    <tr>
        <td colspan="3">
            REPORT DETAILS:
        </td>
    </tr>

    <tr>
        <td>
            Description:
        </td>
        <td>
            #GetRep.rep_desc#
        </td>
    </tr>
    <cfset GetFoto.RecordCount=0>
	<cfquery name="GetFoto" datasource="wolffdb_dsn">
	  Select *
		From LF_Photos left join LF_Reportes on 
             ph_fk_rep_key = rep_key
        where ph_fk_rep_key = #GetRep.rep_key#    
          and rep_user_name = '#SESSION.Auth.user_name#'   
          and ph_user_name = '#SESSION.Auth.user_name#'
		order by ph_yyyymmdd
	</cfquery>

<cfloop query="GetFoto"> 
<tr>
    <td>
        #GetFoto.ph_desc#
    </td>
    <td><a href="#TRIM(GetFoto.ph_link)#"><img src="#TRIM(GetFoto.ph_link)#" width="250"/></a></td>
</tr>
</cfloop>   
</cfoutput>
</table>
</center>
</div>
	  </p>
	   
    </div> 
  </div>
</div>
	
  

</body>
</html>
