<!DOCTYPE html>
<html lang="en">
<head>
  <title>L.F. Jennings</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js" integrity="sha512-GsLlZN/3F2ErC5ifS5QtgpiJtWd43JWSuIgh7mbzZ8zBps+dvLusV+eNQATqgA/HdeKFVgA5v3S/cIrLF7QnIg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    
  
	 <link rel="stylesheet" type="text/css" href="../Paginas/my.css">

</head>
<body id="body">



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

<cfset GetEmp2.RecordCount=0>
<cfquery name="GetEmp2" datasource="wolffdb_dsn">
    Select *
    From LF_Employees
        order by emp_name
</cfquery> 
<div class="container">   

 <center>
  <table width="100%" class="table">
    <tr>

      <td align="left">
        <strong>LF Jennings, Inc.</strong> <br>
407 N.Washington Street  <br>
Falls Church, VA 22046

      </td>
      <td align="right">
        <a href="index.cfm">
        <img src="Images/jennings.png" width="90" height="90" alt=""/></a>
        <strong>LF Jennings, Inc.</strong>
      </td>
    </tr>
    <tr>  
     
      <td colspan="2" align="right">
        <strong>Date:</strong>&nbsp;&nbsp;
        <CFSET ws_fechaW = DateFormat(Now(),"mm-dd-yyyy")>   
        <cfoutput><strong>#ws_fechaW#</strong></cfoutput><br>
      </td>
    </tr> 
  </table>
  <cfoutput>
    <h3> Project Safety Inspection</h3>
    <h2> <strong>#GetRep.pr_desc#</strong></h2>
</cfoutput>  
	                
<table width="100%" border="2" bordercolor="#blue">
   <cfoutput> 
    <tr> 
        <td>Report By:</td>  
        <td colspan="2">#GetRep.emp_name#</td>       
    </tr> 

    <tr> 
        <td>On-site Supervisor:</td>  
        <td colspan="2">#GetEmp.emp_name#</td>       
    </tr> 

    <tr>
       
        <td colspan="2">
 
        </td>
        <td align="right">
 
          <a href="add_emails_tosend.cfm?claveU=#TRIM(GetRep.rep_key)#">Send to Emails</a>
        </td>
    </tr>

    <tr>
        <td>
            Scope of inspection:
        </td>
        <td colspan="2">
            #GetRep.rep_desc#
        </td>
    </tr>
  </cfoutput>
</table>
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
<br><br>
<cfloop query="GetFoto"> 

  <table width="100%" border="2" bordercolor="#blue">
    <cfoutput>
   
  <tr>
    <td colspan="2">
        #GetFoto.ph_obs#
    </td>
</tr>

<tr>
    <td>
        #GetFoto.ph_desc#
    </td>
    <td align="right">
      <a href="Upload_Files2.cfm?reporte=#GetFoto.ph_fk_rep_key#&llave=#GetFoto.ph_key#"><strong>Add second photo</strong></a> 
  </td>
</tr>
  
  <cfif #TRIM(GetFoto.ph_key)# eq #TRIM(GetFoto.ph_fk_ph_key)#>
      <td>
        <a href="#TRIM(GetFoto.ph_link)#"><img src="#TRIM(GetFoto.ph_link)#" width="300"></a>
      </td>  
      <td>
        <a href="#TRIM(GetFoto.ph_link2)#"><img src="#TRIM(GetFoto.ph_link2)#" width="300"></a>
      </td>
     </tr>   
    <cfelse>
   <tr>
    <td colspan="2">
      <a href="#TRIM(GetFoto.ph_link)#"><img src="#TRIM(GetFoto.ph_link)#" width="300"/></a>
    </td>
    </tr> 
  </cfif> 

<br><br>
</cfoutput>
</table>
</cfloop>   
<table width="100%" border="2" bordercolor="#blue">
  <cfoutput>
<tr><td colspan="3"><br><br></td></tr> 
<!--- <tr>
  <td colspan="3">
    #TRIM(GetEmp.rep_notes)#
  </td>
</tr> --->
</cfoutput>
</table>
<table width="100%">
  <tr><td colspan="3"><br></td></tr> 
        
        <tr>
            <td align="right">
                <cfoutput>
                    
                 <a href="Upload_Files.cfm?reporte=#GetFoto.ph_fk_rep_key#"><strong>Add Photo</strong></a> 
               <!--- <a href="Upload_Files.cfm?reporte=#GetRep.rep_keyy#"><strong>Add Photo</strong></a> ---> 
                
                </cfoutput>
            <td>    
        </tr>
        <tr><td><br></td></tr>
        <TR>
          <TD><p class="text-end">
               <strong>Notes:</strong>
          </p></TD>
          <TD>
        <CFFORM ACTION="upd_notes.cfm" METHOD="post">
          <cfoutput>
            <input type="hidden" name="rep_key" value="#GetRep.rep_key#">	
        </cfoutput>
        <CFINPUT TYPE="Text"     
                 NAME="rep_notes" 
                 value="#GetRep.rep_notes#"
                 size="120"
                 MAXLENGTH="120"
                 class="form-control"
                 autocomplete="off"> 
        <input type="submit" class="btn btn-secondary" VALUE="Update Notes"> 
      </TD> 
      </TR>
      </CFFORM>
</table    
</center>
</div>
</div>
	  </p>
	   
    </div> 
  </div>
</div>

  

</body>
</html>
