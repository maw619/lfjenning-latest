
<cfinclude template="headings.cfm"></cfinclude>	
	


<style>
span{
   
}

</style>


  
<div class="container-fluid text-center">    

    
		<br>
		 
			<cfif NOT (IsDefined("SESSION.Auth.IsLoggedIn") AND SESSION.Auth.IsLoggedIn)>
	            <cflocation url="https://www.keybyme.com"> 
          </cfif> 

<!---======================================================--->  					
<cfset GetPro.RecordCount=0>
<cfquery name="GetPro" datasource="wolffdb_dsn">
	  Select *
		From LF_Projects
        order by pr_desc
</cfquery>   
         
<!---======================================================---> 
<cfset GetEmp.RecordCount=0>
<cfquery name="GetEmp" datasource="wolffdb_dsn">
	  Select *
		From LF_Employees
        order by emp_name
</cfquery>   
         
<!---======================================================---> 

 <CFFORM ACTION="inc_report.cfm" METHOD="post">
        <table align="center" class="table table-striped" >		
<TR>
   <TH colspan="2">
      <span class="style1"><font size="+1">Add Report</font></span>
   </TH>
</TR>
<div class="form-group">
<!--- <TR>
   
   <TD>
        <p class="text-end">Report name:</p>
   </TD>
   <TD>
        <CFINPUT TYPE="Text"     
                 NAME="rep_name" 
	             MESSAGE="Name is required!"
	             MAXLENGTH="80"
                 REQUIRED="Yes"
                 class="form-control"
                 autocomplete="off">   
   </TD>
</TR> --->

<tr>
    <td><p class="text-end">Project:</p></td>

 
    <td>
   
       <select id="single" class="form-select"  name="pr_key" size="1" >
           <option value="0" selected>Projects</option>
              <cfloop query="GetPro"> 
               <cfoutput>  
                   <option value="#GetPro.pr_key#"> 
                       #GetPro.pr_desc#
                   </option> 	 
               </cfoutput>	 
           </cfloop> 
      </select>        
    </td>     
</tr> 

<tr>
    <td><p class="text-end">Report By:</p></td>
    <td>
 
       <select id="single2" class="form-select"  name="rep_fk_emp_key" size="1" >
           <option value="0" selected>Report By</option>
              <cfloop query="GetEmp"> 
               <cfoutput>  
                   <option value="#GetEmp.emp_key#"> 
                       #GetEmp.emp_name#
                   </option> 	 
               </cfoutput>	 
           </cfloop> 
      </select>        
    </td>     
</tr> 

<tr>
    <td><p class="text-end">Supervisor:</p></td>
    <td>

       <select id="single3" class="form-select"  name="rep_fk_emp_key_sup" size="1">
           <option value="0" selected>Supervisor</option>
              <cfloop query="GetEmp"> 
               <cfoutput>  
                   <option value="#GetEmp.emp_key#"> 
                       #GetEmp.emp_name#
                   </option> 	 
               </cfoutput>	 
           </cfloop> 
      </select>        
    </td>     
</tr> 

<TR>
    <TD><p class="text-end">
         Scope of Inspection:
    </p></TD>
    <TD>
         <CFINPUT TYPE="Text"     
                  NAME="rep_desc" 
                  size="120"
                  MAXLENGTH="120"
                  class="form-control"
                  autocomplete="off">   
    </TD>
 </TR>

 <!--- <TR>
    <TD><p class="text-end">
         Notes:
    </p></TD>
    <TD>
         <CFINPUT TYPE="Text"     
                  NAME="rep_notes" 
                  size="120"
                  MAXLENGTH="120"
                  class="form-control"
                  autocomplete="off">   
    </TD>


 </TR> --->

 <TR>
 <TD colspan="2" align="center">
<div class="d-grid gap-2">
 <input type="submit" class="btn btn-secondary" VALUE="Add"> 
</div>
 </TD> 
</TR>    
</table>
<br>
<br>
<br>
</CFFORM>
			
</div>




    <!-- jQuery -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <!-- Select2 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/js/select2.min.js"></script>
    <script>
      $("#single").select2({
          placeholder: "Select an Employee",
          allowClear: true
      });
            $("#single2").select2({
          placeholder: "Select an Employee",
          allowClear: true
      });
            $("#single3").select2({
          placeholder: "Select an Employee",
          allowClear: true
      });
    </script>
<cfinclude template="footer.cfm"></cfinclude>
