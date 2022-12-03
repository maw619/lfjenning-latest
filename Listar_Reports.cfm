

<cfinclude template="headings.cfm"></cfinclude>	

  <cfif NOT (IsDefined("SESSION.Auth.IsLoggedIn") AND SESSION.Auth.IsLoggedIn)>
    <cflocation url="https://www.keybyme.com"> 
  </cfif>  

  <cfif isDefined("form.Criteria")>
    <cfset url.Criteria = trim(form.Criteria)>
 </cfif> 

<div class="container-fluid text-center">    


		
 
	<cfset GetRep.RecordCount=0>
	<cfquery name="GetRep" datasource="wolffdb_dsn">
	  Select *
		From LF_Reportes inner join LF_Projects on 
             rep_fk_pr_key = pr_key inner join LF_Employees on
             rep_fk_emp_key = emp_key
    where rep_user_name = '#SESSION.Auth.user_name#'         
           	<cfif isDefined('url.Criteria') AND TRIM(url.Criteria) NEQ ''>
             and  (rep_name LIKE '%#Trim(url.Criteria)#%' OR
                   rep_desc LIKE '%#Trim(url.Criteria)#%')
            </cfif>     
		order by rep_key desc
	</cfquery>
  
  <!--- <cfset GetEmp.RecordCount=0>
  <cfquery name="GetEmp" datasource="wolffdb_dsn">
      Select *
      From LF_Employees
          order by emp_name
  </cfquery>  --->

 <center>
				    	<h2> <cfoutput>Reports</cfoutput> </h2>
	                
<table border="2"  class="table table-striped">
   <tr></tr>
     <th colspan="10">
        <cfoutput> 
        <a href="add_report.cfm">Add Report</a> 
        </cfoutput>     
     </th>
     </tr>
    <tr>

    <cfform name="disp" method="post" action="Listar_Reports.cfm">

        <tr> 
        <td colspan="1" valign="bottom" align="center"><input type="submit" class="btn btn-secondary" name="editpho" value="Search"></td> 
        <td colspan="4"><input name="Criteria" size="30"></td>
        <td colspan="4">&nbsp;</td>
        </tr>          
     
    </cfform>  
 
</tr>
   <tr>
        <!--- <th style="color:#006" bgcolor="#CCCCCC"><span class="style9">Add Photo</th>  --->
	      <th style="color:#006" bgcolor="#CCCCCC"><span class="style9">Edit</th>
        <th style="color:#006" bgcolor="#CCCCCC">Report Date</th>  
        <th style="color:#006" bgcolor="#CCCCCC">Project</th>
	      <th style="color:#006" bgcolor="#CCCCCC">Report By</th>
        <th style="color:#006" bgcolor="#CCCCCC">Supervisor</th>
        <th style="color:#006" bgcolor="#CCCCCC">Description</th>
        <th style="color:#006" bgcolor="#CCCCCC">Send to:</th>
        <th style="color:#006" bgcolor="#CCCCCC"><span class="style9">Delete</th>        
    </tr> 
	
<cfset ws_I = 0>
<cfset WbgcolorYes = "##70dbdb">
<cfset WbgcolorNo = "##ebfafa">
	
 <cfloop query="GetRep"> 
   
  <cfquery name="GetEmp" datasource="wolffdb_dsn">
    Select *
      From LF_Employees
      where emp_key = #GetRep.rep_fk_emp_key_sup#
  </cfquery>
   
 <cfoutput> 
 <tr>
 
	 
	 	<cfif ws_I EQ 0>
                <cfset ws_color = WbgcolorNo>
                <cfset ws_I = 1>
        <cfelse>
                <cfset ws_color = WbgcolorYes>
                <cfset ws_I = 0>
        </cfif>  
        <!--- 
	<td align="center"><a href="Upload_Files.cfm?reporte=#TRIM(GetRep.rep_key)#"><img src="Images/add.png" width="16" height="16" alt=""/></a></td> 
        --->
  <td align="center"><a href="upd_report.cfm?claveU=#GetRep.rep_key#"><img src="Images/ico-edit.gif" width="16" height="16" alt=""/></a></td>					
  <td bgcolor="#(ws_color)#"><a href="Reporte_upd.cfm?claveU=#TRIM(GetRep.rep_key)#">#TRIM(GetRep.rep_yyyymmdd)#</a></td>
 <td bgcolor="#(ws_color)#">#TRIM(GetRep.pr_desc)#</td>
 <td bgcolor="#(ws_color)#">#TRIM(GetRep.emp_name)#</td>
  <td bgcolor="#(ws_color)#">#TRIM(GetEmp.emp_name)#</td>  
  <td bgcolor="#(ws_color)#">#TRIM(GetRep.rep_desc)#</td>
 <td bgcolor="#(ws_color)#">
   <a href="add_emails_tosend.cfm?claveU=#TRIM(GetRep.rep_key)#">Send to Emails</a>
   
     
</td>
  <td align="center"><a href="del_report.cfm?claveU=#GetRep.rep_key#"><img src="Images/ico-eliminar2.gif" width="20" height="20" alt=""/></a></td>               
 
 </tr>
 </cfoutput>
 </cfloop>
 
</table>
</center>

</div>
	


<cfinclude template="footer.cfm"></cfinclude>
