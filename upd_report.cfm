<cfinclude template="headings.cfm"></cfinclude>	
	
  
<div class="container-fluid text-center">    

       
  	 	  <cfif NOT (IsDefined("SESSION.Auth.IsLoggedIn") AND SESSION.Auth.IsLoggedIn)>
			    <cflocation url="https://www.keybyme.com/index.cfm">
          </cfif> 

  	<cfset GetRep.RecordCount=0>
	<cfquery name="GetRep" datasource="wolffdb_dsn">
	  Select *
		From LF_Reportes
		Where rep_key = <cfqueryparam value="#URL.claveU#" cfsqltype="cf_sql_numeric">  
	</cfquery>

   <cfquery name="GetEmp" datasource="wolffdb_dsn">
    Select *
    From LF_Employees
   </cfquery>	

  <cfquery name="GetPro" datasource="wolffdb_dsn">
    Select *
    From LF_Projects
   </cfquery>
 
 <cfform name="edit" method="post" action="act_upd_rep.cfm">
	<cfoutput>
        <input type="hidden" name="rep_key" value="#GetRep.rep_key#">	
    </cfoutput>
	<br>

	<table class="table table-striped">
	  <cfoutput>	
		<div class="form-group">
      <!--- <tr>
        <td>Report name: </td>
       <td><cfinput name="rep_name" value="#GetRep.rep_name#" size="80" class="form-control"></td>    
    </tr> --->

      <tr>
        <td>Report Description: </td>
       <td><cfinput name="rep_desc" value="#GetRep.rep_desc#" size="80" class="form-control"></td>    
    </tr>
     </cfoutput>

    <tr>
        <td>Report By: </td>
        <td> 
			
        <select name="rep_fk_emp_key" id="single" size="1">
		   <cfloop query="GetEmp"> 
			    <cfoutput>
					<cfif #Trim(GetRep.rep_fk_emp_key)# EQ #Trim(GetEmp.emp_key)#>
		               <option value="#GetEmp.emp_key#" selected> 
		                      #GetEmp.emp_name#
	                   </option>
			        <cfelse>
					   <option value="#GetEmp.emp_key#"> 
		                      #GetEmp.emp_name#
	                   </option>	
					</cfif>	
				 </cfoutput>	 
		   </cfloop> 
	
        </select>			
		</td>	
    </tr>

    <tr>
        <td>Supervisor: </td>
        <td> 
			
        <select name="rep_fk_emp_key_sup" id="single2" size="1">
		   <cfloop query="GetEmp"> 
			    <cfoutput>
					<cfif #Trim(GetRep.rep_fk_emp_key_sup)# EQ #Trim(GetEmp.emp_key)#>
		               <option value="#GetEmp.emp_key#" selected> 
		                      #GetEmp.emp_name#
	                   </option>
			        <cfelse>
					   <option value="#GetEmp.emp_key#"> 
		                      #GetEmp.emp_name#
	                   </option>	
					</cfif>	
				 </cfoutput>	 
		   </cfloop> 
	
        </select>			
		</td>	
    </tr>

    <tr>
        <td>Project: </td>
        <td> 
			
        <select name="rep_fk_pr_key" id="single3" size="1">
		   <cfloop query="GetPro"> 
			    <cfoutput>
					<cfif #Trim(GetRep.rep_fk_emp_key_sup)# EQ #Trim(GetPro.pr_key)#>
		               <option value="#GetPro.pr_key#" selected> 
		                      #GetPro.pr_desc#
	                   </option>
			        <cfelse>
					   <option value="#GetPro.pr_key#"> 
		                      #GetPro.pr_desc#
	                   </option>	
					</cfif>	
				 </cfoutput>	 
		   </cfloop> 
	
        </select>			
		</td>	
    </tr>

	<tr>
        <td>Notes: </td>
       <td><cfinput name="rep_notes" value="#GetRep.rep_notes#" size="120"  class="form-control"></td>    
    </tr>

    <tr>
        <td colspan="2">
		        <div class="d-grid gap-2">
				<input type="submit" class="btn btn-secondary" VALUE="Update"> 
				</div>
		</td>
     
 </tr> 	  
 </div>
	</table>		
   

</cfform>		

</div>
    <!-- jQuery -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <!-- Select2 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/js/select2.min.js"></script>
    <script>
      $("#single").select2({
          placeholder: "",
          allowClear: true
      });
            $("#single2").select2({
          placeholder: "",
          allowClear: true
      });
            $("#single3").select2({
          placeholder: "",
          allowClear: true
      });
    </script>
<cfinclude template="footer.cfm"></cfinclude>
