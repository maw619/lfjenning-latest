

<cfinclude template="headings.cfm"></cfinclude>	
	


  <cfif NOT (IsDefined("SESSION.Auth.IsLoggedIn") AND SESSION.Auth.IsLoggedIn)>
    <cflocation url="https://www.keybyme.com"> 
  </cfif>  

  <cfif isDefined("form.Criteria")>
    <cfset url.Criteria = trim(form.Criteria)>
 </cfif> 

<div class="container-fluid text-center">    

		<div>

		
 
	<cfset GetEmp.RecordCount=0>
	<cfquery name="GetEmp" datasource="wolffdb_dsn">
	  Select *
		From LF_Employees inner join LF_Cargos on
             emp_fk_ch_key = ch_key
           	<cfif isDefined('url.Criteria') AND TRIM(url.Criteria) NEQ ''>
             where  (emp_name LIKE '%#Trim(url.Criteria)#%' OR
                   emp_email LIKE '%#Trim(url.Criteria)#%' OR
                   ch_desc LIKE '%#Trim(url.Criteria)#%')
            </cfif>     
		order by emp_name
	</cfquery>
  
 <center>
				    	<h2> <cfoutput>Employees</cfoutput> </h2>
	                
<table border="2" class="table table-striped">
   <tr>
     <th colspan="10">
        <cfoutput> 
        <a href="add_emp.cfm">Add Employee</a> 
        </cfoutput>     
     </th>
     </tr>
    <tr>

    <cfform name="disp" method="post" action="Listar_Emp.cfm">

        <tr> 
        <td colspan="1" valign="bottom" align="center"><input type="submit" name="editpho" class="btn btn-secondary" value="Search"></td> 
        <td colspan="4"><input name="Criteria" size="30"></td>
        <td colspan="4">&nbsp;</td>
        </tr>
    </cfform>  
 
</tr>
   <tr>
	    <th style="color:#006" bgcolor="#CCCCCC"><span class="style9">Edit</th>
        <th style="color:#006" bgcolor="#CCCCCC">Name</th>  
	      <th style="color:#006" bgcolor="#CCCCCC">E-mail</th>
        <th style="color:#006" bgcolor="#CCCCCC">Phone</th>
        <th style="color:#006" bgcolor="#CCCCCC">Charge</th>
        <th style="color:#006" bgcolor="#CCCCCC"><span class="style9">Delete</th>        
    </tr> 
	
<cfset ws_I = 0>
<cfset WbgcolorYes = "##70dbdb">
<cfset WbgcolorNo = "##ebfafa">
	
 <cfloop query="GetEmp"> 
 <cfoutput> 
 <tr>
 
	 
	 	<cfif ws_I EQ 0>
                <cfset ws_color = WbgcolorNo>
                <cfset ws_I = 1>
        <cfelse>
                <cfset ws_color = WbgcolorYes>
                <cfset ws_I = 0>
        </cfif>  

        <cfset ws_phone = 0> 
        <cfif #GetEmp.emp_phone# GT 0>		
              <cfset ws_phone = #GetEmp.emp_phone#>
            <cfset areacode = left(ws_phone, 3)>
            <cfset firstthree = mid(ws_phone, 4, 3)>
            <cfset lastfour = right(ws_phone, 4)>
            <cfset ws_phone = "(#areacode#) " & "#firstthree#" & "-" & "#lastfour#"> 
        </cfif>      
	 
  <td align="center"><a href="upd_emp.cfm?claveU=#GetEmp.emp_key#"><img src="Images/ico-edit.gif" width="16" height="16" alt=""/></a></td>					
  <td bgcolor="#(ws_color)#">#TRIM(GetEmp.emp_name)#</td> 
  <td bgcolor="#(ws_color)#"><a href="mailto:#TRIM(GetEmp.emp_email)#" onclick="javascript:window.location='mailto:?subject=Interesting information&body=I thought you might find this information interesting:https://www.keybyme.com/LF/Reporte_upd.cfm?claveU=30">#TRIM(GetEmp.emp_email)#</a></td>
  <cfif ws_phone eq 0>
       <td bgcolor="#(ws_color)#"></a></td>
  <cfelse>
       <td bgcolor="#(ws_color)#"><a href="tel:#TRIM(ws_phone)#">#TRIM(ws_phone)#</a></td>
  </cfif>
  <td bgcolor="#(ws_color)#">#TRIM(GetEmp.ch_desc)#</td>
  <td align="center"><a href="del_emp.cfm?claveU=#GetEmp.emp_key#"><img src="Images/ico-eliminar2.gif" width="20" height="20" alt=""/></a></td>               
 
<!---
<a class="email" title="Email a friend" href="#" onclick="javascript:window.location='mailto:?subject=Interesting information&body=I thought you might find this information interesting:https://www.keybyme.com/LF/Reporte_upd.cfm?claveU=30">Email</a>

--->


 </tr>
 </cfoutput>
 </cfloop>
 
</table>
</center>

   <!---<cfinclude template="propagandaKB.cfm"></cfinclude>--->
  </div>
</div>


<cfinclude template="footer.cfm"></cfinclude>
