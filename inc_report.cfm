 
 <cfoutput>
	<CFSET ws_fecha = DateFormat(Now(),"mmmm d, yyyy")> 
  <cfset ws_fecha_x = #ws_fecha#>
  
 
	<CFQUERY name="test" datasource="wolffdb_dsn">
	INSERT INTO LF_Reportes(rep_fk_emp_key, rep_fk_emp_key_sup, rep_fk_pr_key, rep_desc, rep_pages, rep_user_name, rep_yyyymmdd)
	 VALUES( '#Trim(FORM.rep_fk_emp_key)#'
          , '#Trim(FORM.rep_fk_emp_key_sup)#'
          , '#Trim(FORM.pr_key)#'
          , '#Trim(FORM.rep_desc)#' 
          , '0'
          , '#SESSION.Auth.user_name#'
          , '#ws_fecha#')
	</CFQUERY> 
   </cfoutput>
	   
 <cfset GetRep.RecordCount=0>
 <cfquery name="GetRep" datasource="wolffdb_dsn">
   Select Top 1 *
     From LF_Reportes
     order by rep_key desc
 </cfquery>

<cfoutput>
<cflocation url="Upload_Files.cfm?reporte=#GetRep.rep_key#" addtoken="false">
</cfoutput>