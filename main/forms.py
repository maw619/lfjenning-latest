from urllib import request
from django import forms
from django.forms import ModelForm , ClearableFileInput
from .models import *


class AddProjectsForm(ModelForm):
    class Meta: 
        model = Lf_Projects
        fields = ('pr_desc', 'pr_address')
        labels = {
            "pr_desc" : "Project",
            "pr_address": "Address"
        }
        
        widgets = {
        'pr_desc': forms.TextInput(attrs={'class':'form-control'}),
        'pr_address': forms.TextInput(attrs={'class':'form-control'}),
       }  
 
 
class UpdateReportsForm(ModelForm):
    class Meta:
        model = Lf_Reportes
        fields = ['rep_name','rep_fk_emp_key','rep_fk_emp_key_sup',
                  'rep_notes','rep_user_name','rep_fk_pr_key','rep_desc',
                  'rep_yyyymmdd']
        labels = {
            "rep_fk_pr_key": 'Project',
            'rep_fk_emp_key': "Report By:",
            'rep_fk_emp_key_sup': "Supervisor", 
            'rep_notes': "Scope of Inspection", 
            
        }
 
        widgets = {
            'rep_name': forms.HiddenInput(),
            'rep_fk_emp_key': forms.Select(attrs={'class':'form-select'}),
            'rep_fk_emp_key_sup': forms.Select(attrs={'class':'form-select'}),
            'rep_notes': forms.TextInput(attrs={'class':'form-control'}),
            'rep_user_name': forms.TextInput(attrs={'class':'form-control'}),
            'rep_fk_pr_key': forms.HiddenInput(),
            'rep_desc': forms.TextInput(attrs={'class':'form-control'}),
            'rep_yyyymmdd': forms.TextInput(attrs={'class':'form-control'}),
           
        }
        
        
        
class AddReportsForm(ModelForm):
    class Meta:
        model = Lf_Reportes
        fields = ['rep_name','rep_fk_emp_key','rep_fk_emp_key_sup',
                  'rep_notes','rep_user_name','rep_fk_pr_key','rep_desc',
                  'rep_yyyymmdd']
        labels = {
            "rep_fk_pr_key": 'Project',
            'rep_fk_emp_key': "Report By:",
            'rep_fk_emp_key_sup': "Supervisor", 
            'rep_notes': "Scope of Inspection", 
            
        }
 
        widgets = {
            'rep_name': forms.HiddenInput(),
            'rep_fk_emp_key': forms.HiddenInput(),
            'rep_fk_emp_key_sup':forms.HiddenInput(),
            'rep_notes': forms.HiddenInput(),
            'rep_user_name': forms.HiddenInput(),
            'rep_fk_pr_key': forms.HiddenInput(),
            'rep_desc': forms.HiddenInput(),
            'rep_yyyymmdd': forms.HiddenInput(),
           
        }
        
            
class AddEmployeesForm(ModelForm):
    class Meta:
        model = Lf_Employees
        fields = {'emp_name','emp_email','emp_phone','emp_fk_ch_key'}
        labels = {
            "emp_name" : "Name",
            "emp_email": "Email",
            "emp_phone": "Phone",
            "emp_fk_ch_key": "Charges",
        }
        
        widgets = {
            'emp_name': forms.TextInput(attrs={'class':'form-control'}),
            'emp_email': forms.TextInput(attrs={'class':'form-control'}),
            'emp_phone': forms.TextInput(attrs={'class':'form-control'}),
            'emp_fk_ch_key': forms.Select(attrs={'class':'form-select'}),
        }
        
         
            
            
    
class AddPhotosForm(ModelForm):
     class Meta:
        model = Lf_Photos
        fields = {'ph_key','ph_link','ph_yyyymmdd','ph_user_name','ph_fk_rep_key','ph_desc','ph_obs'}
        labels = {
            "ph_link" : "Choose File",
            "ph_obs": "Observations",
            "ph_desc": "Description",
            'ph_fk_rep_key':'Report ID'
            
        }
        
        widgets = {
           
            'ph_link': ClearableFileInput(attrs={'class':'form-control','multiple': False, 'required':True}),
            'ph_obs': forms.TextInput(attrs={'class':'form-control'}),
            'ph_desc': forms.TextInput(attrs={'class':'form-control'}),
            'ph_fk_rep_key_id': forms.HiddenInput(),
            'ph_yyyymmdd': forms.HiddenInput(),
            'ph_user_name': forms.HiddenInput(),
            
        }
    
class AddPhotosFormById(ModelForm):
     class Meta:
        model = Lf_Photos
        fields = {'ph_key','ph_link','ph_yyyymmdd','ph_user_name','ph_fk_rep_key','ph_desc','ph_obs'}
        labels = {
            "ph_link" : "Choose File",
            "ph_obs": "Observations",
            "ph_desc": "Description",
            'ph_fk_rep_key':'Report ID'
            
        }
        
        widgets = {
           
            'ph_link': ClearableFileInput(attrs={'class':'form-control','multiple': False, 'required':True}),
            'ph_obs': forms.TextInput(attrs={'class':'form-control'}),
            'ph_desc': forms.TextInput(attrs={'class':'form-control'}),
            'ph_fk_rep_key_id': forms.TextInput(attrs={'class':'form-control'}),
            'ph_yyyymmdd': forms.HiddenInput(),
            'ph_user_name': forms.HiddenInput(),
            'ph_fk_rep_key': forms.HiddenInput(),
        }


    
class AddPhotosForm2(ModelForm):
     class Meta:
        model = Lf_Photos2
        fields = {'ph_key2','ph_fk_rep_key2','ph_fk_ph_key','ph_link2','ph_yyyymmdd', 'ph_desc2' }
        labels = {
            "ph_link2" : "Choose File",
          
        }
        
        widgets = {
            'ph_link2': ClearableFileInput(attrs={'class':'form-control','multiple': False}),
            'ph_desc2': forms.HiddenInput(),
            'ph_fk_rep_key2':  forms.HiddenInput(),
            'ph_yyyymmdd': forms.HiddenInput(),
            'ph_key2':  forms.HiddenInput(),
            'ph_fk_ph_key':   forms.HiddenInput(),
            
         }
    
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
class AddCertsForm(ModelForm):
     class Meta:
        model = Lf_Certificados
        fields = {'cer_key','cer_desc'}
        labels = {
            "cer_desc": "Certification",
        }
        
        widgets = {
            'cer_key': forms.HiddenInput(),
            'cer_desc':forms.TextInput(attrs={'class':'form-control'}),
         }
     
class AddChargsForm(ModelForm):
    class Meta:
        model = Lf_Cargos
        fields = {'ch_key', 'ch_desc'}
        labels = {
            'ch_desc': 'Description'
        }
        
        widgets = {
            'ch_key': forms.HiddenInput(),
            'ch_desc': forms.TextInput(attrs={'class':'form-control'})
        }
