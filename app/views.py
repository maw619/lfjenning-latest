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
   
			 
			destination = "/Users/marco/PythonProjects/lf-jennings-latest/lfjenning-latest/app/"
			#destination = "/root/lfjenning-latest/app/"
   
			
			# file = open(destination+f'{date_string}.pdf', 'rb')
			# readpdf = PyPDF2.PdfFileReader(file)
			# totalpages = readpdf.numPages

			# reader = PdfReader(destination+f'{date_string}.pdf')
			# pdf_page_count = len(reader.pages)

			page = []	
			for x in range(100):
				page.append(x)
		 
   

			rep_fk_emp_key_sup = request.POST.getlist('rep_fk_emp_key_sup') 
			context = {'mydate': date.today().strftime(f"%B %d,%Y"),
					'rep_ws_to':get_emp[0].rep_ws_to,
					'emp_name': get_emp[0].emp_name,
					'emp_email':get_rep[0].emp_email,
					'emp_phone':get_rep[0].emp_phone,
					'get_photo':get_photo,
					'get_rep': get_rep[0],
					'pr_desc': get_rep[0].pr_desc,
					'emails':Lf_Employees.objects.all(),
					'rep_key':pk,
					'page':page,
					'totalpages':0,
				}
   
			

		
				
	
			
			 
			#/Users/marco/PythonProjects/lf-jennings-latest/lfjenning-latest/app/
			file = open(destination + f'{date_string}.pdf', "w+b")
			#context = {'myvar': 'this is your template context'}
			# Create a Django response object, and specify content_type as pdf
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="report.pdf"'
			# find the template and render it.
			template = get_template(template_path)
			html = template.render(context)

			rep_fk_emp_key_sup = request.POST.getlist('rep_fk_emp_key_sup')
				# if error then show some funny view
			
			# create a pdf
			pisa_status = pisa.CreatePDF(
			html, 
			dest=file, 
			link_callback=link_callback)
			time.sleep(2)
			print("inside the reporte_udp2 from app view")
			mail = EmailMultiAlternatives('Safety Report Email', 'message', settings.EMAIL_HOST_USER, rep_fk_emp_key_sup)
			mail.attach_file(destination+f'{date_string}.pdf')
			#mail.send()
			if pisa_status.err:
				return HttpResponse('We had some errors <pre>' + html + '</pre>')
			messages.success(request,'email sent')
			return redirect('reports')
 