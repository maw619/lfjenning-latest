from django.shortcuts import render, redirect,HttpResponse
from .models import *
from .forms import *
from django.db import connection
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings 
from django_xhtml2pdf.utils import pdf_decorator
from django_xhtml2pdf.utils import pdf_decorator
import pdfkit
from django.contrib.auth import authenticate, login
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from .forms import FileFieldForm
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
# Import User Model From Django
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv
from django.contrib import messages

# Import PDF Stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Pagination Stuff
from django.core.paginator import Paginator


@login_required(login_url='login')
def home(request):
    return render(request, 'main/home.html' )

######################### projects ###########################
@login_required(login_url='login')
def add_project(request):
    form = AddProjectsForm()
    if request.method == 'POST':
        form = AddProjectsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form, 'tabletitle':'add project'.upper() }     
    return render(request, 'main/add_project.html', context )

@login_required(login_url='login')
def projects(request):
    data = Lf_Projects.objects.all()
    context = {'projects': data,'tabletitle':'projects'.upper()} 
    return render(request, 'main/projects.html', context)

def update_project(request,pk):
    projects = Lf_Projects.objects.get(pr_key=pk)
    form = AddProjectsForm(instance=projects)
    if request.method == 'POST':
        form = AddProjectsForm(request.POST, instance=projects)
        form.save()
        messages.success(request, 'Project Updated')
        return redirect('projects')
    return render(request, 'main/add_project.html', {'form':form})

def delete_project(request, pk):
    projects = Lf_Projects.objects.get(pr_key=pk)
    projects.delete()
    messages.success(request, 'Project Deleted')
    return redirect('projects')
     
######################### employees ###########################
@login_required(login_url='login')
def add_employees(request):
    fullname = request.user.first_name +" "+ request.user.last_name
    strFullname = fullname.strip('\"')
    # form = AddEmployeesForm(initial={"emp_name": strFullname, "emp_email":request.user.email})
    form = AddEmployeesForm()
    if request.method == 'POST':
        form = AddEmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    context = { 'form':form, 'tabletitle':'add employee'.upper()  }
    return render(request, 'main/add_employee.html', context)

@login_required(login_url='login')
def employees(request):
    employee = Lf_Employees.objects.all()
    context = { 'employees': employee,
                'tabletitle':'employees'.upper()
            }
    return render(request, 'main/employees.html', context)

def update_employee(request, pk):
    employee = Lf_Employees.objects.get(emp_key=pk)
    form = AddEmployeesForm(instance=employee)
    if request.method == 'POST':
        form = AddEmployeesForm(request.POST, instance=employee)
        form.save()
        return redirect('employees')

    return render(request, 'main/add_employee.html', {'form':form})

def delete_employee(request, pk):
    employee = Lf_Employees.objects.get(emp_key=pk)
    employee.delete()
    messages.success(request, "Employee deleted")
    return redirect('employees')
           
######################### reports ###########################

@login_required(login_url='login')
def reports(request):
 
    try:
        data = Lf_Reportes.objects.raw(f"""
        Select *
        From lf_reportes inner join lf_projects on 
        rep_fk_pr_key = pr_key inner join lf_employees on
        rep_fk_emp_key = emp_key
        where rep_user_name = '{request.user.username}';
        """)
 
        dataEmp = Lf_Employees.objects.raw(f"""
        Select *
        From lf_employees
        where emp_key = {data[0].rep_fk_emp_key_sup}
        """)
        
        dataEmp2 = Lf_Employees.objects.raw(f"""
        Select *
        From lf_employees
        where emp_key = {data[0].rep_fk_emp_key_sup}
        """)

        employee = Lf_Employees.objects.get(emp_key=data[0].rep_fk_emp_key_sup)
       #employee = Lf_Employees.objects.get(emp_key=data[0].rep_fk_emp_key)
       #supname = Lf_Employees.objects.get(emp_key=data[0].rep_fk_emp_key_sup)
         
    except:
        messages.success(request, 'You need to add at least one record')
        return render(request, 'main/reports.html')
    
    context = {'data': data,
               'data2':dataEmp,
               'data3':dataEmp2,
               'employee':employee,
               'tabletitle':'reports'.upper()}
    return render(request, 'main/reports.html', context)
 
def delete_report(request, pk):
    report = Lf_Reportes.objects.get(rep_key=pk)
    report.delete()
    messages.success(request, 'report deleted')
    return redirect('reports')

@login_required(login_url='login')
def load_update_form(request, pk):
    reports = Lf_Reportes.objects.get(rep_key=pk)
    employee = Lf_Employees.objects.get(emp_key=reports.rep_fk_emp_key)
    supname = Lf_Employees.objects.get(emp_key=reports.rep_fk_emp_key_sup)
    project = Lf_Projects.objects.get(pr_key=reports.rep_fk_pr_key)
    context = { 'reports':reports,
                'getPro': Lf_Projects.objects.all(),
                'empList': Lf_Employees.objects.all(),
                'supList': Lf_Employees.objects.all(),
                'emp':employee,
                'project': project,
                'supname': supname,
                'rep_user_name': request.user.username,
                'tabletitle':'update reports'.upper()}
    
    return render(request, 'main/update_reports.html', context)

@login_required(login_url='login')
def update_report(request, pk):
    reports = Lf_Reportes.objects.get(rep_key=pk)
    if request.method == 'POST':
       # rep_name = request.POST['rep_name']
        rep_fk_emp_key =  request.POST['rep_fk_emp_key']
        rep_fk_pr_key = request.POST['rep_fk_pr_key']
        rep_fk_emp_key_sup =  request.POST['rep_fk_emp_key_sup']
        rep_desc =  request.POST['rep_desc']
        rep_notes = request.POST['rep_notes']
        #reports.rep_name = rep_name
        reports.rep_fk_emp_key = rep_fk_emp_key
        reports.rep_fk_pr_key = rep_fk_pr_key
        reports.rep_fk_emp_key_sup = rep_fk_emp_key_sup
        reports.rep_desc = rep_desc
        #reports.rep_yyyymmdd = request.POST['rep_yyyymmdd']
        reports.rep_notes = rep_notes
        reports.save()       
        messages.success(request, "record updated") 
        return redirect('reports')
    return render(request, 'main/update_reports.html')



@login_required(login_url='login')
def add_reports(request):
    form = AddReportsForm()
 
    if request.method == 'POST':
        form = AddReportsForm(request.POST)
        if form.is_valid(): 
            form.save()
            data = Lf_Reportes.objects.raw(f"""
            Select *
            From lf_reportes inner join lf_projects on 
            rep_fk_pr_key = pr_key inner join lf_employees on
            rep_fk_emp_key = emp_key
            where rep_user_name = '{request.user.username}';
            """)
            
            last = ''
            for x in data:
                last = x.rep_key
                print("iterated:::::",x.rep_key)
            request.session['rep_key'] = last
            return redirect('add_photo_single')             
    context = {'form':form, 
    'getPro': Lf_Projects.objects.all(),
    'empList': Lf_Employees.objects.all(),
    'supList': Lf_Employees.objects.all(),
    'rep_user_name': request.user.username,
    'tabletitle':'add reports'.upper(),

    }  
    return render(request, 'main/add_report.html', context)


def reporte_udp(request, pk):
        user = authenticate(request, username=request.user.username,password=request.user.password)        
        login(request,user)
        request.session['first_name'] = request.user.first_name
        request.session['last_name'] = request.user.last_name
        
        data = Lf_Reportes.objects.raw(f"""
        Select * From lf_reportes inner join lf_projects on 
        rep_fk_pr_key = pr_key inner join lf_employees on
        rep_fk_emp_key = emp_key
        where rep_key = '{pk}';
        """)
        

        
        try:
            
            dataEmp = Lf_Employees.objects.raw(f"""
            Select *
            From lf_employees
            where emp_key = {data[0].rep_fk_emp_key_sup}
            """)
            
            for x in data:
                print(x)
            request.session['rep_key'] = data[0].rep_key
            request.session['rep_fk_emp_key'] = data[0].rep_fk_emp_key
            request.session['emp_key'] = dataEmp[0].emp_key
            request.session['date'] = date.today().strftime(f"%B %d,%Y")
            print("inside reporte_udp ============")
            print(f"Rep Key is::::::::::: ",{request.session['rep_key']})
            print("rep_fk_emp_key:",request.session['rep_fk_emp_key'])
            print("emp_key:",request.session['emp_key'])
            print("date: ",request.session['date'])
            print("inside reporte_udp ============")
            get_rep = Lf_Reportes.objects.raw(f"""
            Select * From lf_reportes inner join lf_projects on 
            rep_fk_pr_key = pr_key inner join lf_employees on
            rep_fk_emp_key = emp_key
            Where rep_key = '{request.session['rep_key']}'
        """)
        
            get_emp = Lf_Reportes.objects.raw(f"""
            Select * From lf_reportes inner join lf_employees on
            rep_fk_emp_key_sup = emp_key
            inner join lf_projects on 
            rep_fk_pr_key = pr_key
            Where rep_key = '{request.session['rep_key']}'  
            order by emp_name;
        """)
        
            get_photo = Lf_Photos.objects.raw(f"""
            Select *
            From lf_photos left join lf_reportes on 
            ph_fk_rep_key = rep_key
            left join lf_photos2 on 
            ph_key = ph_fk_ph_key  
            where ph_fk_rep_key = '{request.session['rep_key']}'
            and rep_user_name = '{request.user.username}'   
            and ph_user_name = '{request.user.username}'
        """)

            rep_fk_emp_key_sup = request.POST.getlist('rep_fk_emp_key_sup')
            print("ooooooooooooooooo",get_rep[0].pr_desc)
            context = {'date': request.session['date'],
                    'rep_ws_to':get_emp[0].rep_ws_to,
                    'emp_name': get_emp[0].emp_name,
                    'emp_email':get_rep[0].emp_email,
                    'emp_phone':get_rep[0].emp_phone,
                    'get_photo':get_photo,
                    'get_rep': get_rep[0],
                    'pr_desc': get_rep[0].pr_desc
                }
        #filename = f"{request.user.username}-{datetime.now()}.pdf"

            mail = EmailMultiAlternatives('subject', 'message', settings.EMAIL_HOST_USER, rep_fk_emp_key_sup)
            mail.attach_file('fname.pdf')
           # mail.send()
        except:
            messages.success(request, 'something went wrong')
            return render(request, 'main/reports.html')
        return render(request, 'main/reporte_udp.html', context)


@pdf_decorator  
def reporte_udp2(request, rep_key):
        user = authenticate(request, username=request.user.username,password=request.user.password)        
        login(request,user)
        
        if request.method == 'POST':
            request.session['first_name'] = request.user.first_name
            request.session['last_name'] = request.user.last_name
            data = Lf_Reportes.objects.raw(f"""
            Select * From lf_reportes inner join lf_projects on 
            rep_fk_pr_key = pr_key inner join lf_employees on
            rep_fk_emp_key = emp_key
            where rep_key = '{rep_key}';
            """)
            
            counter = 0
            for x in data:
                counter = counter + 1
            print("count:",counter)
            if(counter > 0):
                dataEmp = Lf_Employees.objects.raw(f"""
                Select *
                From lf_employees
                where emp_key = {data[0].rep_fk_emp_key_sup}
                """)
                
                for x in data:
                    print(x)
                request.session['rep_key'] = data[0].rep_key
                request.session['rep_fk_emp_key'] = data[0].rep_fk_emp_key
                request.session['emp_key'] = dataEmp[0].emp_key
                request.session['date'] = date.today().strftime(f"%B %d,%Y")

            get_rep = Lf_Reportes.objects.raw(f"""
                Select * From lf_reportes inner join lf_projects on 
                rep_fk_pr_key = pr_key inner join lf_employees on
                rep_fk_emp_key = emp_key
                Where rep_key = '{request.session['rep_key']}'
            """)
            
            get_emp = Lf_Reportes.objects.raw(f"""
                Select * From lf_reportes inner join lf_employees on
                rep_fk_emp_key_sup = emp_key
                inner join lf_projects on 
                rep_fk_pr_key = pr_key
                Where rep_key = '{request.session['rep_key']}'  
                order by emp_name;
            """)
            
            get_photo = Lf_Photos.objects.raw(f"""
                Select *
                From lf_photos left join lf_reportes on 
                ph_fk_rep_key = rep_key
                left join lf_photos2 on 
                ph_key = ph_fk_ph_key  
                where ph_fk_rep_key = '{request.session['rep_key']}'
                and rep_user_name = '{request.user.username}'   
                and ph_user_name = '{request.user.username}'
            """)

            emails = Lf_Employees.objects.all()
            rep_fk_emp_key_sup = request.POST.getlist('rep_fk_emp_key_sup')
            
        
            context = {'date': request.session['date'],
                    'rep_ws_to':get_emp[0].rep_ws_to,
                    'emp_name': get_emp[0].emp_name,
                    'emp_email':emails[0],
                    'emp_phone':get_rep[0].emp_phone,
                    'get_photo':get_photo,
                    'get_rep': get_rep[0],
                    'pr_desc': get_rep[0].pr_desc
                }
            
            #filename = f"{request.user.username}-{datetime.now()}.pdf"
            print("inside the reporte_udp2 view")
            mail = EmailMultiAlternatives('subject', 'message', settings.EMAIL_HOST_USER, rep_fk_emp_key_sup)
            mail.attach_file('fname.pdf')
            mail.send()
        
        return render(request, 'main/reporte_udp2.html', context)
                
                
def reporte_udp3(request,pk):
        user = authenticate(request, username=request.user.username,password=request.user.password)        
        login(request,user)
        request.session['first_name'] = request.user.first_name
        request.session['last_name'] = request.user.last_name
        
        data = Lf_Reportes.objects.raw(f"""
        Select * From lf_reportes inner join lf_projects on 
        rep_fk_pr_key = pr_key inner join lf_employees on
        rep_fk_emp_key = emp_key
        where rep_key = '{pk}';
        """)
        
        counter = 0
        for x in data:
            counter = counter + 1
        print("count:",counter)
        
        try:
            
            dataEmp = Lf_Employees.objects.raw(f"""
            Select *
            From lf_employees
            where emp_key = {data[0].rep_fk_emp_key_sup}
            """)
            
            for x in data:
                print(x)
            request.session['rep_key'] = data[0].rep_key
            request.session['rep_fk_emp_key'] = data[0].rep_fk_emp_key
            request.session['emp_key'] = dataEmp[0].emp_key
            request.session['date'] = date.today().strftime(f"%B %d,%Y")
            print("inside reporte_udp ============")
            print(f"Rep Key is::::::::::: ",{request.session['rep_key']})
            print("rep_fk_emp_key:",request.session['rep_fk_emp_key'])
            print("emp_key:",request.session['emp_key'])
            print("date: ",request.session['date'])
            print("inside reporte_udp ============")
            
            
            get_rep = Lf_Reportes.objects.raw(f"""
            Select * From lf_reportes inner join lf_projects on 
            rep_fk_pr_key = pr_key inner join lf_employees on
            rep_fk_emp_key = emp_key
            Where rep_key = '{request.session['rep_key']}'
        """)
        
            get_emp = Lf_Reportes.objects.raw(f"""
            Select * From lf_reportes inner join lf_employees on
            rep_fk_emp_key_sup = emp_key
            inner join lf_projects on 
            rep_fk_pr_key = pr_key
            Where rep_key = '{request.session['rep_key']}'  
            order by emp_name;
        """)
        
            get_photo = Lf_Photos.objects.raw(f"""
            Select *
            From lf_photos left join lf_reportes on 
            ph_fk_rep_key = rep_key
            left join lf_photos2 on 
            ph_key = ph_fk_ph_key  
            where ph_fk_rep_key = '{request.session['rep_key']}'
            and rep_user_name = '{request.user.username}'   
            and ph_user_name = '{request.user.username}'
        """)

            rep_fk_emp_key_sup = request.POST.getlist('rep_fk_emp_key_sup')
            print("ooooooooooooooooo",get_rep[0].pr_desc)
            context = {'date': request.session['date'],
                    'rep_ws_to':get_emp[0].rep_ws_to,
                    'emp_name': get_emp[0].emp_name,
                    'emp_email':get_rep[0].emp_email,
                    'emp_phone':get_rep[0].emp_phone,
                    'get_photo':get_photo,
                    'get_rep': get_rep[0],
                    'pr_desc': get_rep[0].pr_desc
                }
            
            buf = io.BytesIO()
            # Create a canvas
            c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
            # Create a text object
            textob = c.beginText()
            textob.setTextOrigin(inch, inch)
            textob.setFont("Helvetica", 14)

            # Add some lines of text
            #lines = [
            #	"This is line 1",
            #	"This is line 2",
            #	"This is line 3",
            #]

            # Designate The Model
            venues = Venue.objects.all()

            # Create blank list
            lines = []

            for x in get_rep:
                lines.append(x.rep_key)
                         
                lines.append(" ")

            # Loop
            for line in lines:
                textob.textLine(line)

            # Finish Up
            c.drawText(textob)
            c.showPage()
            c.save()
            buf.seek(0)
    
     
        except:
            messages.success(request, 'something went wrong')
            return render(request, 'main/reports.html')

        
       
        # Return something
        return FileResponse(buf, as_attachment=True, filename='venue.pdf')


################### charges #############################################
@login_required(login_url='login')
def add_charge(request):    
    if request.method == 'POST':
        form = AddChargsForm(request.POST)
        form.save()
        return redirect('charges')
    form = AddChargsForm()
    return render(request, 'main/add_charge.html', {'form':form})

@login_required(login_url='login')
def charges(request):
    cargos = Lf_Cargos.objects.raw(
        """
         Select *
		From lf_cargos
		order by ch_desc
        """
    )
    context = {'charges': cargos, 'tabletitle':'charges'.upper() }
    return render(request, 'main/charges.html', context)

def update_charge(request, pk):
    charge = Lf_Cargos.objects.get(ch_key=pk)
    form = AddChargsForm(instance=charge)
    if request.method == 'POST':
        form = AddChargsForm(request.POST, instance=charge)
        form.save()
        messages.success(request, 'Charge Updated')
        return redirect('charges')
    return render(request, 'main/add_charge.html', {'form': form})

def delete_charge(request,pk):
    charge = Lf_Cargos.objects.get(ch_key=pk)
    charge.delete()
    messages.success(request, 'Charge deleted')
    return redirect('charges')

################### photos #############################################
@login_required(login_url='login')
def photos(request):
    photoList = Lf_Photos.objects.raw(
    f"""Select *
		From lf_photos where ph_user_name = '{request.user.username}'         
		order by ph_yyyymmdd
    """)
    context = {'photo': photoList, 'tabletitle':'photos'.upper() }
    return render(request, 'main/photos.html', context)

@login_required(login_url='login')
def add_photos(request):
    data = Lf_Reportes.objects.raw(f"""
            Select *
            From lf_reportes inner join lf_projects on 
            rep_fk_pr_key = pr_key inner join lf_employees on
            rep_fk_emp_key = emp_key
            where rep_user_name = '{request.user.username}';
            """)
            
    last = ''
    for x in data:
        last = x.rep_key
    
    #print("last iterated:::::",last)
    request.session['rep_key'] = last
    form = AddPhotosForm(initial={'ph_user_name': request.user.username,'ph_fk_rep_key': last}) 
    print(" request.session['ph_fk_rep_key'] = ", request.session['rep_key'])
    if(request.method == "POST"):
        form = AddPhotosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('reporte_udp', pk = request.session['rep_key'])
        
    context = {'form':form,
               'ph_user_name': request.user.username,
               'tabletitle':'add photo'.upper()
            }
    return render(request, 'main/add_photo.html', context)

@login_required(login_url='login')
def add_photo(request):
    form = AddPhotosForm(initial={'ph_fk_rep_key':request.session['rep_key'], 'ph_user_name':request.user.username}) 
    if(request.method == "POST"):
        form = AddPhotosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('reporte_udp', pk = request.session['rep_key'])
        
    context = {'form':form,
               'ph_user_name': request.user.username,
               'tabletitle':'add photo'.upper() }
    return render(request, 'main/add_photo.html', context)

@login_required(login_url='login')
def add_photo2(request, ph_fk_ph_key):
    form = AddPhotosForm2(initial={'ph_fk_ph_key2': request.session['rep_key'],'ph_fk_ph_key':ph_fk_ph_key}) 
    if(request.method == "POST"):
        form = AddPhotosForm2(request.POST, request.FILES)
     
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('reporte_udp', pk = request.session['rep_key'])
        
    context = {'form':form,
               'ph_user_name': request.user.username,
               'tabletitle':'add photo'.upper() }
    return render(request, 'main/add_photo2.html', context)


def delete_photo(request, pk):
    pic = Lf_Photos.objects.get(ph_key=pk)
    pic.delete()
    messages.success(request, "Image deleted")
    return redirect('photos')

def update_photo(request, pk):
    photo = Lf_Photos.objects.get(ph_key=pk)
    form = AddPhotosForm(instance=photo)
    if request.method == 'POST':
        form = AddPhotosForm(request.POST, request.FILES, instance=photo)
        form.save()
        return redirect('photos')
    return render(request, 'main/add_photo.html', {'form':form})

################### certificates #############################################
@login_required(login_url='login')
def certification(request):
    certs = Lf_Certificados.objects.all()
    context = {'certs': certs,'tabletitle':'certifications'.upper()}
    return render(request, 'main/certifications.html', context)

@login_required(login_url='login')
def add_cert(request):
    form = AddCertsForm()
    if(request.method == 'POST'):
        form = AddCertsForm(request.POST)
        form.save()
        return redirect('certification')
    context = {'form': form,'tabletitle':'add certification'.upper()}
    return render(request, 'main/add_certs.html', context)

def update_cert(request, pk):
    certs = Lf_Certificados.objects.get(cer_key=pk)
    form = AddCertsForm(instance=certs)
    if request.method == 'POST':
        form = AddCertsForm(request.POST, instance=certs)
        form.save()
        messages.success(request, 'Certification Updated')
        return redirect('certification')
    
    return render(request, 'main/add_certs.html', {'form':form})

def delete_cert(request, pk):
    cert = Lf_Certificados.objects.get(cer_key=pk)
    cert.delete()
    messages.success(request, 'Certification Deleted')
    return redirect('certification')

def emailMessage(request,pk):
    messages.success(request, 'email sent successfully')
    return redirect('reporte_udp', pk = pk)
 
def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Add some lines of text
    #lines = [
    #	"This is line 1",
    #	"This is line 2",
    #	"This is line 3",
    #]

    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
 
    # Return something
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')
