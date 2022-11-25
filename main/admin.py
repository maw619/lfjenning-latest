from django.contrib import admin
from .models import *

admin.site.register(Lf_Cargos)
admin.site.register(Lf_Certificados)
admin.site.register(Lf_EmpCer)
admin.site.register(Lf_Employees)

# class Lf_PhotosAdmin(admin.ModelAdmin):
#     readonly_fields = ('ph_key',)
#admin.site.register(Lf_Photos, Lf_PhotosAdmin)

    
 
admin.site.register(Lf_Photos)
admin.site.register(Lf_Photos2)
admin.site.register(Lf_Projects)
admin.site.register(Lf_RepEmails)
admin.site.register(Lf_Reportes)


