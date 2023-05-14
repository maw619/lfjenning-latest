from django.contrib import admin
from .models import *

@admin.register(Lf_Cargos)
class Lf_CargosAdmin(admin.ModelAdmin):
    list_display = "ch_key","ch_desc"
    
@admin.register(Lf_EmpCer)
class Lf_EmpCerAdmin(admin.ModelAdmin):
    list_display = "ec_key","ec_exp_yyyymmdd","ec_fk_cer_key_id","ec_fk_emp_key_id"

@admin.register(Lf_Employees)
class Lf_EmployeesAdmin(admin.ModelAdmin):
    list_display = "emp_name","emp_email","emp_phone", "emp_fk_ch_key_id"

@admin.register(Lf_Photos)
class Lf_PhotosAdmin(admin.ModelAdmin):
    list_display = "ph_key","ph_fk_rep_key_id","ph_link", "ph_yyyymmdd","ph_desc","ph_user_name","ph_obs"
 
@admin.register(Lf_Photos2)
class Lf_Photos2Admin(admin.ModelAdmin):
    list_display = "ph_key2","ph_fk_rep_key2","ph_link2", "ph_yyyymmdd","ph_desc2"

@admin.register(Lf_Projects)
class Lf_ProjectsAdmin(admin.ModelAdmin):
    list_display = "pr_key","pr_desc","pr_address"

@admin.register(Lf_Reportes)
class Lf_ReportesAdmin(admin.ModelAdmin):
    list_display = "rep_key","rep_name","rep_desc","rep_user_name","rep_send","rep_send_email","rep_notes","rep_yyyymmdd","rep_ws_to","rep_pages","rep_fk_emp_key_id","rep_fk_emp_key_sup_id","rep_fk_pr_key_id"

admin.site.register(EmailGroup)