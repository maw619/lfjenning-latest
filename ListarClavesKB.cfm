<!DOCTYPE html>
<html lang="en">
<head>
  <title>Keybyme.com</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  
	 <link rel="stylesheet" type="text/css" href="my.css">

</head>
<body>

  <cfinclude template="menu.cfm"></cfinclude>
  
<div class="container-fluid text-center">    
  <div class="row content">

	  
    <div class="col-sm-8 text-left"> 
      
		
	
		
      <p>
		<div>
	      <cfif NOT (IsDefined("SESSION.Auth.IsLoggedIn") AND SESSION.Auth.IsLoggedIn)>
			    <cflocation url="https://www.keybyme.com/index.cfm">
          </cfif> 
		


 <cfif isDefined("form.Criteria")>
    <cfset url.Criteria = trim(form.Criteria)>
</cfif>
 <cfif isDefined("form.CriteriaCat")>
    <cfset url.CriteriaCat = trim(form.CriteriaCat)>
</cfif>	 
	 
	 		<cfset GetCat.RecordCount=0>
	<cfquery name="GetCat" datasource="wolffdb_dsn">
	  Select cat_key, cat_fk_user_key, cat_desc
		From Categorias_X
		Where cat_fk_user_key = #SESSION.Auth.user_key#
		order by cat_desc
	</cfquery>
	 
	 

<CFSET GetUser.RecordCount=0>
<CFQUERY NAME="GetUser" datasource="wolffdb_dsn">
  SELECT  *                  
  FROM  Claves left join Categorias_X on
        cl_cat = cat_key and
	    cl_fk_user_key = cat_fk_user_key
  Where #SESSION.Auth.user_key# = cl_fk_user_key
  	<cfif (isDefined('url.Criteria') AND TRIM(url.Criteria) NEQ '')>
             AND  (cl_url LIKE '%#Trim(url.Criteria)#%' OR
                   cl_username LIKE '%#Trim(url.Criteria)#%' OR
                   cl_pass2 LIKE '%#Trim(url.Criteria)#%' OR
                   cl_remarks LIKE '%#Trim(url.Criteria)#%')  
	</cfif>	
	<cfif (isDefined('url.CriteriaCat') AND TRIM(url.CriteriaCat) NEQ '')>
		      AND cl_cat = #Trim(url.CriteriaCat)#
			  <!---AND cl_cat LIKE '%#Trim(url.CriteriaCat)#%'--->
	</cfif>
	
</CFQUERY>
	

 
				    	<h2> <cfoutput>Links/Passwords</cfoutput> </h2>
	                
<table border="2" bordercolor="#blue">
   <tr>
     <th colspan="10">
        <cfoutput>
        <a href="add_claveKB.cfm">Add Link/Pass</a>&nbsp;&nbsp;&nbsp;&nbsp;
        <a href="ListarCategorias.cfm">Categories</a>&nbsp;&nbsp;&nbsp;&nbsp;
        
        </cfoutput>     
     </th>
     </tr>
     <tr>
<cfform name="disp" method="post" action="ListarClavesKB.cfm">

 
    <tr>
        <td colspan="2">Search:  <input name="Criteria" size="30"></td>
		<td>
		 
			
		<cfselect input name="CriteriaCat" size="1" onChange="this.options[this.selectedIndex].value && (window.location = this.options[this.selectedIndex].value);">		 
		<!---<cfselect input name="CriteriaCat" size="1">--->
		       <cfoutput>   
				     <option value="">Categories</option>
			     <cfloop query="GetCat">
					 
					 <option value="ListarClavesKB.cfm?CriteriaCat=#GetCat.cat_key#">#GetCat.cat_desc#</option>
	             </cfloop>
				</cfoutput>  	  
        </cfselect>
      	
			
<!---		<SELECT NAME="ws_cat_key" onChange="ListarClavesKB.cfm">
<OPTION>Categories</OPTION>
<CFOUTPUT QUERY="GetCat">
<OPTION VALUE="#cat_key#">#cat_desc#</OPTION>
</CFOUTPUT>
</SELECT>--->
		</td>
         <td><input type="submit" name="editpho" value="send"></td> 
		<td colspan="7">&nbsp;</td>
    </tr>          
 
</cfform>
</tr>
   <tr>
	    <th style="color:#006" bgcolor="#CCCCCC"><span class="style9">Edit</th>
        <th style="color:#006" bgcolor="#CCCCCC">URL</th>
        <th style="color:#006" bgcolor="#CCCCCC">username</th>
        <th style="color:#006" bgcolor="#CCCCCC">password</th>
        <th style="color:#006" bgcolor="#CCCCCC">pass2</th>
        <th style="color:#006" bgcolor="#CCCCCC">Category</th>
        <th style="color:#006" bgcolor="#CCCCCC">Remarks</th> 
        <th style="color:#006" bgcolor="#CCCCCC"><span class="style9">Delete</th>        
    </tr> 
	
<cfset ws_I = 0>
<cfset WbgcolorYes = "##70dbdb">
<cfset WbgcolorNo = "##ebfafa">
	
 <cfloop query="GetUser"> 
 <cfoutput> 
 <tr>
 <cfset decoded = decrypt(
    #TRIM(GetUser.cl_pass1)#,
    #TRIM(GetUser.cl_llave)#,
    "AES",
    "hex"
    ) />
	 
	 	<cfif ws_I EQ 0>
                <cfset ws_color = WbgcolorNo>
                <cfset ws_I = 1>
        <cfelse>
                <cfset ws_color = WbgcolorYes>
                <cfset ws_I = 0>
        </cfif>  
	 
  <td align="center"><a href="upd_clavesKB.cfm?claveU=#GetUser.cl_key#&action=1">
                                <img src="../image/ico-edit.gif" width="16" height="16" alt=""/></a></td>					
  <cfset ws_link = ws_parte1 & '#TRIM(GetUser.cl_url)#' & ws_parte2 & '#TRIM(GetUser.cl_url)#' & ws_parte3>
  <td bgcolor="#(ws_color)#">#TRIM(ws_link)#</td>
  <td bgcolor="#(ws_color)#">#TRIM(GetUser.cl_username)#</td>
  <td bgcolor="#(ws_color)#">#TRIM(decoded)#</td>
  <td bgcolor="#(ws_color)#">#TRIM(GetUser.cl_pass2)#</td>
  
  <td bgcolor="#(ws_color)#">#TRIM(GetUser.cat_desc)#</td>
  <td bgcolor="#(ws_color)#">#TRIM(GetUser.cl_remarks)#</td>   
  
  <td align="center"><a href="del_clavesKB.cfm?claveU=#GetUser.cl_key#&action=2">
                                 <img src="../image/ico-eliminar2.gif" width="20" height="20" alt=""/></a></td>               
 
 </tr>
 </cfoutput>
 </cfloop>
 
</table>
</div>
	  </p>
	  
     
     <!--- <h3>Test</h3>
      <p>Lorem ipsum...</p>--->
    </div>
   <!---<cfinclude template="propagandaKB.cfm"></cfinclude>--->
  </div>
</div>
	
 

</body>
</html>
