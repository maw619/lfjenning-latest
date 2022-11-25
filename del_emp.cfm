<cfinclude template="headings.cfm"></cfinclude>	
	
<div class="main">
<div class="container-fluid text-center">    
  <div class="row content">

	  
    <div class="col-sm-8 text-left"> 
	      <cfif NOT (IsDefined("SESSION.Auth.IsLoggedIn") AND SESSION.Auth.IsLoggedIn)>
			    <cflocation url="https://www.keybyme.com/index.cfm">
          </cfif> 
		 
		
      <p>
		<div>
   
<CFSET Get_Emp.RecordCount=0>
<cfquery name = "Get_Emp" dataSource = "wolffdb_dsn">
    Select *   
    From LF_Employees
    Where emp_key = <cfqueryparam value="#URL.claveU#" cfsqltype="cf_sql_numeric"> 
</cfquery>


<cfparam name="url.action" default="">

<form name="edit" method="post" action="act_del_emp.cfm">
	  <h2 align="center">Delete Employee</h2><br>
<cfoutput>
<table align="center">
    <input type="hidden" name="emp_key" value="#Get_Emp.emp_key#">	
          <tr>
     	<td>Name: </td>
        <td>   
        <input 
         type="text" 
         name="pe_name" 
         value="#Get_Emp.emp_name#"
         size="80">
        </td>    
     </tr>
          
    <tr>
       	<td colspan="2"><input type="submit" name="editemp" value="Delete"></td>
    </tr>   				
</table>
</cfoutput>
</form>

</div>
	  </p>
	   
    </div>
 
  </div>
</div>
	
</div>

<cfinclude template="footer.cfm"></cfinclude>
