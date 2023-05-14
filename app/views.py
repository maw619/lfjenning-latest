from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.core.mail import EmailMessage, EmailMultiAlternatives
from main.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from io import StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
# Import User Model From Django
from django.contrib.auth.models import User
import time
from django.http import HttpResponse
import csv
from django.contrib import messages
import datetime 
# Import PDF Stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django_xhtml2pdf.utils import pdf_decorator
# Import Pagination Stuff
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.generic import View
from .render import render_to_pdf
from xhtml2pdf import pisa
import PyPDF2
from PyPDF2 import PdfReader
import PyPDF2, io, requests


def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path


def render_pdf_view(request,pk):
	template_path = 'main/reporte_udp2.html'
			
	user = authenticate(request, username=request.user.username,password=request.user.password)        
	login(request,user)
	first_name = request.user.first_name
	last_name = request.user.last_name
	
	data = Lf_Reportes.objects.raw(f"""
	Select * From lf_reportes inner join lf_projects on 
	rep_fk_pr_key_id = pr_key inner join lf_employees on
	rep_fk_emp_key_id = emp_key
	where rep_key = '{pk}';
	""")

	get_rep = Lf_Reportes.objects.raw(f"""
	Select * From lf_reportes inner join lf_projects on 
	rep_fk_pr_key_id = pr_key inner join lf_employees on
	rep_fk_emp_key_id = emp_key
	Where rep_key = '{pk}'
""")

	get_emp = Lf_Reportes.objects.raw(f"""
	Select * From lf_reportes inner join lf_employees on
	rep_fk_emp_key_id = emp_key
	inner join lf_projects on 
	rep_fk_pr_key_id = pr_key
	Where rep_key = '{pk}'  
	order by emp_name;
""")

	get_photo = Lf_Photos.objects.raw(f"""
	Select *
	From lf_photos left join lf_reportes on 
	ph_fk_rep_key_id = rep_key
	left join lf_photos2 on 
	ph_key = ph_fk_ph_key  
	where ph_fk_rep_key_id = '{pk}'

""")
	
	now = datetime.datetime.now()
	date_string = now.strftime('%Y-%m-%d')

		
	destination = "/Users/marco/pythonProjects/lf_jennings/lfjenning-latest/app"
	#destination = "/root/lfjenning-latest/app/"

	
	#file = open(destination+f'{date_string}.pdf', 'rb')
	# readpdf = PyPDF2.PdfFileReader(file)
	# totalpages = readpdf.numPages

	# reader = PdfReader(destination+f'{date_string}.pdf')
	# pdf_page_count = len(reader.pages)
	
	current_number = 1

	pages = len(get_photo) + 3
	rep_fk_emp_key_sup = request.POST.getlist('rep_fk_emp_key_sup') 
	sup_name = Lf_Employees.objects.filter(emp_key = get_emp[0].rep_fk_emp_key_sup_id)
	context = {
			'mydate': date.today().strftime(f"%B %d,%Y"),
			'rep_ws_to':get_emp[0].rep_ws_to,
			'emp_name': get_emp[0].emp_name,
			'emp_email':get_rep[0].emp_email,
			'emp_phone':get_rep[0].emp_phone,
			'get_photo':get_photo,
			'sup_name':sup_name[0].emp_name,
			'get_rep': get_rep[0],
			'pr_desc': get_rep[0].pr_desc,
			'emails':Lf_Employees.objects.all(),
			'rep_key':pk,
			'totalpages':pages,
			'observation':'observation',
		}
	
	
	# print("SUPERVISOR NAME IS", sup_name[0].emp_name)
	# print('rep_ws_to',get_emp[0].rep_ws_to)	
	# print('emp_name',get_emp[0].emp_name)
	# print('emp_email',get_rep[0].emp_email)
	# print('emp_phone',get_rep[0].emp_phone) 
	# print('get_rep',get_rep[0])
	# print('get_rep',get_rep[0].rep_fk_emp_key_sup_id)
	# print('pr_desc',get_rep[0].pr_desc)
 

	file = open(f"{get_rep[0].pr_desc}-{date_string}.pdf", "w+b")
	#context = {'myvar': 'this is your template context'}
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

	email_groups = EmailGroup.objects.all()
	rep_fk_emp_key_sup = request.POST.getlist('rep_fk_emp_key_sup')
				
	
	 
		# if error then show some funny view
	html_content = f'''
	<p>Project: <bold>{get_rep[0].pr_desc}</bold></p>
	<p>From: L.F. Jennings Safety Department</p>
	<p><a href="https://google.com">Click here to open {get_rep[0].pr_desc}</a></p>
	<br>
	Please find attached the safety report for {get_rep[0].pr_desc}
	<br>
	<br>
	<br>
	{get_emp[0].emp_name} <br><br>
	from Project Safety <br>
	<img src="https://mybucketholly.s3.amazonaws.com/jennings2.png" alt="LF Jennings Logo" width="75" height="75"><br>
	<bold>L.F. Jennings, INC</bold><br>
	407 N. Washington Street <br>
	Falls Church, VA 22046
	
	'''

					
	# create a pdf
	pisa_status = pisa.CreatePDF(
	html, 
	dest=file, 
	link_callback=link_callback)
	#time.sleep(1)
	groups_field = request.POST.getlist('groups_field')
	
	if groups_field:
		print("GROUPS FIELD1", groups_field)
		for group in email_groups:
			if group.name in groups_field:
				print("Group:", group.name)
				members = group.members.all()
				for member in members:
					print("Email:", member.emp_email)
					
				# Send email to the group members
				subject = 'Safety Report Email'
				message = ''  # Add your message content here
				from_email = settings.EMAIL_HOST_USER

				# Build recipient list
				recipient_list = [member.emp_email for member in members]

				mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
				mail.attach_alternative(html_content, "text/html")
				mail.attach_file(f"{get_rep[0].pr_desc}-{date_string}.pdf")
				mail.send()
	else:
		mail = EmailMultiAlternatives('Safety Report Email', '', settings.EMAIL_HOST_USER, rep_fk_emp_key_sup)
		mail.attach_alternative(html_content, "text/html")
		mail.attach_file(f"{get_rep[0].pr_desc}-{date_string}.pdf")
		mail.send()

	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	messages.success(request, 'Email sent')
	return redirect('reports')
 
 
 







 
 
def render_pdf_view_standalone(request,pk):



	template_path = 'main/reporte_udp2.html'
			
	user = authenticate(request, username=request.user.username,password=request.user.password)        
	login(request,user)
	first_name = request.user.first_name
	last_name = request.user.last_name
	
	data = Lf_Reportes.objects.raw(f"""
	Select * From lf_reportes inner join lf_projects on 
	rep_fk_pr_key_id = pr_key inner join lf_employees on
	rep_fk_emp_key_id = emp_key
	where rep_key = '{pk}';
	""")

	get_rep = Lf_Reportes.objects.raw(f"""
	Select * From lf_reportes inner join lf_projects on 
	rep_fk_pr_key_id = pr_key inner join lf_employees on
	rep_fk_emp_key_id = emp_key
	Where rep_key = '{pk}'
""")

	get_emp = Lf_Reportes.objects.raw(f"""
	Select * From lf_reportes inner join lf_employees on
	rep_fk_emp_key_id = emp_key
	inner join lf_projects on 
	rep_fk_pr_key_id = pr_key
	Where rep_key = '{pk}'  
	order by emp_name;
""")

	get_photo = Lf_Photos.objects.raw(f"""
	Select *
	From lf_photos left join lf_reportes on 
	ph_fk_rep_key_id = rep_key
	left join lf_photos2 on 
	ph_key = ph_fk_ph_key  
	where ph_fk_rep_key_id = '{pk}'

""")
	
	now = datetime.datetime.now()
	date_string = now.strftime('%Y-%m-%d')

		
	destination = "/Users/marco/pythonProjects/lf_jennings/lfjenning-latest/app"
	#destination = "/root/lfjenning-latest/app/"

	
	#file = open(destination+f'{date_string}.pdf', 'rb')
	# readpdf = PyPDF2.PdfFileReader(file)
	# totalpages = readpdf.numPages

	# reader = PdfReader(destination+f'{date_string}.pdf')
	# pdf_page_count = len(reader.pages)
	
	member_name = request.GET.getlist('rep_fk_emp_key_sup') 
	group_selected = request.GET.getlist('groups_field')  
	show_group = None
	show_emails = None
	if group_selected is not None:
		show_group = ""
		for group_name in group_selected:
			
			show_group = []
			group = EmailGroup.objects.filter(name=group_name).first()
			if group:
				show_group.append(group)

			members = group.members.all()
			show_emails = []
			for member in members:
				show_emails.append(member.emp_email)

	show_single_name = ""
	if member_name is not None:
		show_single_name = member_name



	show_group_names = ""
	if show_group:
		for group in show_group:
			show_group_names = group.name
	else:
		print("No group found")
 
	pages = len(get_photo) + 3
	rep_fk_emp_key_sup = request.POST.getlist('rep_fk_emp_key_sup') 
	sup_name = Lf_Employees.objects.filter(emp_key = get_emp[0].rep_fk_emp_key_sup_id)
	context = {
			'mydate': date.today().strftime(f"%B %d,%Y"),
			'rep_ws_to':get_emp[0].rep_ws_to,
			'emp_name': get_emp[0].emp_name,
			'emp_email':get_rep[0].emp_email,
			'emp_phone':get_rep[0].emp_phone,
			'get_photo':get_photo,
			'sup_name':sup_name[0].emp_name,
			'get_rep': get_rep[0],
			'pr_desc': get_rep[0].pr_desc,
			'emails':Lf_Employees.objects.all(),
			'rep_key':pk,
			'totalpages':pages,
			'observation':'observation',
			'groups': EmailGroup.objects.all(),
			'show_group_names': show_group_names,
			'show_names': show_emails,
			'group_selected': group_selected,
			'show_single_name': show_single_name,
		}
	
	
	# print("SUPERVISOR NAME IS", sup_name[0].emp_name)
	# print('rep_ws_to',get_emp[0].rep_ws_to)	
	# print('emp_name',get_emp[0].emp_name)
	# print('emp_email',get_rep[0].emp_email)
	# print('emp_phone',get_rep[0].emp_phone) 
	# print('get_rep',get_rep[0])
	# print('get_rep',get_rep[0].rep_fk_emp_key_sup_id)
	# print('pr_desc',get_rep[0].pr_desc)
 

	file = open(f"{get_rep[0].pr_desc}-{date_string}.pdf", "w+b")
	#context = {'myvar': 'this is your template context'}
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

	email_groups = EmailGroup.objects.all()
	rep_fk_emp_key_sup = request.POST.getlist('rep_fk_emp_key_sup')
				
	
	 
		# if error then show some funny view
	html_content = f'''
	<p>Project: <bold>{get_rep[0].pr_desc}</bold></p>
	<p>From: L.F. Jennings Safety Department</p>
	<p><a href="https://google.com">Click here to open {get_rep[0].pr_desc}</a></p>
	<br>
	Please find attached the safety report for {get_rep[0].pr_desc}
	<br>
	<br>
	<br>
	{get_emp[0].emp_name} <br><br>
	from Project Safety <br>
	<img src="https://mybucketholly.s3.amazonaws.com/jennings2.png" alt="LF Jennings Logo" width="75" height="75"><br>
	<bold>L.F. Jennings, INC</bold><br>
	407 N. Washington Street <br>
	Falls Church, VA 22046
	
	'''

					
	# create a pdf
	pisa_status = pisa.CreatePDF(
	html, 
	dest=file, 
	link_callback=link_callback)
	#time.sleep(1)
	
	
	if request.method == 'POST':
		if group_selected:
			for group in email_groups:
				if group.name in group_selected:
					members = group.members.all()
					recipient_list = [member.emp_email for member in members]

					mail = EmailMultiAlternatives('Safety Report Email', '', settings.EMAIL_HOST_USER, recipient_list)
					mail.attach_alternative(html_content, "text/html")
					mail.attach_file(f"{get_rep[0].pr_desc}-{date_string}.pdf")
					mail.send()
		else:
			mail = EmailMultiAlternatives('Safety Report Email', '', settings.EMAIL_HOST_USER, show_single_name)
			mail.attach_alternative(html_content, "text/html")
			mail.attach_file(f"{get_rep[0].pr_desc}-{date_string}.pdf")
			mail.send()

		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		messages.success(request, 'Email sent')
		return redirect('reports')
	return render(request, 'app/reporte_udp_standalone.html', context)
 
