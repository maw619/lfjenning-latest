from django.db import models
from datetime import date  
from django.http import request
from django.contrib.auth.models import User
from django.conf import settings 


    
class Lf_Cargos(models.Model):
    ch_key = models.AutoField(primary_key=True)
    ch_desc = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lf_cargos'
    def __str__(self) -> str:
        return self.ch_desc

class Lf_Certificados(models.Model):
    cer_key = models.AutoField(primary_key=True)
    cer_desc = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lf_certificados'
    def __str__(self) -> str:
        return self.cer_desc

class Lf_EmpCer(models.Model):
    ec_key = models.AutoField(primary_key=True)
    ec_fk_emp_key = models.OneToOneField('Lf_Employees', on_delete=models.CASCADE)
    ec_fk_cer_key = models.OneToOneField('Lf_Certificados', on_delete=models.CASCADE)
    ec_exp_yyyymmdd =  models.CharField(max_length=45,default=date.today())
    
    class Meta:
        managed = True
        db_table = 'lf_emp_cer'
    def __str__(self) -> str:
        return f"{self.ec_key ,self.ec_fk_emp_key ,self.ec_fk_cer_key ,self.ec_exp_yyyymmdd}"


class Lf_Employees(models.Model):
    emp_key = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=70, blank=True, null=True)
    emp_fk_ch_key = models.ForeignKey('Lf_Cargos',on_delete=models.CASCADE)
    emp_email = models.CharField(max_length=80, blank=True, null=True)
    emp_phone = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lf_employees'
    def __str__(self) -> str:
        return self.emp_name


class Lf_Photos(models.Model):
    ph_key = models.AutoField(primary_key=True)
    ph_link = models.FileField(upload_to='img/',null=True, blank=True)
    ph_yyyymmdd = models.CharField(max_length=45,default=date.today())
    ph_desc = models.CharField(max_length=5000, blank=True, null=True)
    ph_user_name = models.CharField(max_length=50, blank=True, null=True)
    ph_obs = models.CharField(max_length=5000, blank=True, null=True)
    ph_fk_rep_key = models.ForeignKey('Lf_Reportes', on_delete=models.CASCADE, null=True)
    
    class Meta:
        managed = True
        db_table = 'lf_photos'
    def __str__(self) -> str:
        return f"{self.ph_link}"


class Lf_Photos2(models.Model):
    ph_key2 = models.AutoField(primary_key=True)
    ph_fk_rep_key2 = models.IntegerField(blank=True, null=True)
    ph_fk_ph_key = models.IntegerField(blank=True, null=True)
    ph_link2 = models.FileField(upload_to='img2/',null=True, blank=True)
    ph_yyyymmdd =  models.CharField(max_length=45,default=date.today())
    ph_desc2 = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lf_photos2'
    def __str__(self) -> str:
        return f"{self.ph_link2}"


class Lf_Reportes(models.Model):
    rep_key = models.AutoField(primary_key=True)
    rep_name = models.CharField(max_length=80, blank=True, null=True)
    rep_fk_emp_key = models.ForeignKey('Lf_Employees', related_name='rep_fk_emp_key', on_delete=models.CASCADE)
    rep_fk_pr_key = models.ForeignKey('Lf_Projects', related_name='rep_fk_emp_key' , on_delete=models.CASCADE)
    rep_fk_emp_key_sup = models.ForeignKey('Lf_Employees',related_name='rep_fk_emp_key_sup', verbose_name = 'emp_name', on_delete=models.CASCADE)
    rep_desc = models.CharField(max_length=255, blank=True, null=True)
    rep_user_name = models.CharField(max_length=50, blank=True, null=True)
    rep_send = models.IntegerField(blank=True, null=True)
    rep_send_email = models.CharField(max_length=80, blank=True, null=True)
    rep_notes = models.CharField(max_length=255, blank=True, null=True)
    rep_yyyymmdd = models.CharField(max_length=45,default=date.today())
    rep_ws_to = models.CharField(max_length=255, blank=True, null=True)
    rep_pages = models.IntegerField(blank=True, null=True)
 
    class Meta:
        managed = True
        db_table = 'lf_reportes'
        
    def __str__(self) -> str:
        return f"{self.rep_key}, {self.rep_user_name}, {self.rep_desc},  {self.rep_yyyymmdd}"
        
        
class Lf_Projects(models.Model):
    pr_key = models.AutoField(primary_key=True)
    pr_desc = models.CharField(max_length=150, blank=True, null=True)
    pr_address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lf_projects'
    def __str__(self) -> str:
        return self.pr_desc


class Lf_RepEmails(models.Model):
    repe_key = models.AutoField(primary_key=True)
    repe_fk_rep_key = models.OneToOneField('Lf_Reportes', on_delete=models.CASCADE)
    repe_fk_emp_key = models.OneToOneField('Lf_Employees', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'lf_rep_emails'
    def __str__(self) -> str:
        return self.repe_fk_rep_key,' ',self.repe_fk_emp_key


