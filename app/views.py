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
 
from django.http import HttpResponse
import csv
from django.contrib import messages

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

from xhtml2pdf import pisa


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


def render_pdf_view(request):
			template_path = 'app/reporte_udp.html'
			
			request.session['first_name'] = request.user.first_name
			request.session['last_name'] = request.user.last_name
			data = Lf_Reportes.objects.raw(f"""
			Select * From lf_reportes inner join lf_projects on 
			rep_fk_pr_key = pr_key inner join lf_employees on
			rep_fk_emp_key = emp_key
			where rep_user_name = '{request.user.username}';
			""")

			dataEmp = Lf_Employees.objects.raw(f"""
			Select *
			From lf_employees
			where emp_key = {data[0].rep_fk_emp_key_sup}
			""")

			request.session['rep_key'] = data[0].rep_key
			request.session['rep_fk_emp_key'] = data[0].rep_fk_emp_key
			request.session['emp_key'] = dataEmp[0].emp_key
			request.session['date'] = date.today().strftime(f"%B %d,%Y")
			print(f"Rep Key is::::::::::: ",{request.session['rep_key']})
			print("rep_key:",request.session['rep_key'])
			print("rep_fk_emp_key:",request.session['rep_fk_emp_key'])
			print("emp_key:",request.session['emp_key'])
			print("date: ",request.session['date'])
			
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
		
			context = {'date': request.session['date'],
			'rep_ws_to':get_emp[0].rep_ws_to,
			'emp_name': get_rep[0].emp_name,
			'emp_email':get_rep[0].emp_email,
			'emp_phone':get_rep[0].emp_phone,
			'get_photo':get_photo,
					
			}
			
			destination = "\\Users\\marco\\PythonProjects\\New folder\\lfjennings\\app\\"
			file = open(destination + 'filename.pdf', "w+b")
			#context = {'myvar': 'this is your template context'}
			# Create a Django response object, and specify content_type as pdf
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="report.pdf"'
			# find the template and render it.
			template = get_template(template_path)
			html = template.render(context)

			# create a pdf
			pisa_status = pisa.CreatePDF(
			html, dest=file, link_callback=link_callback)
			# if error then show some funny view
			if pisa_status.err:
				return HttpResponse('We had some errors <pre>' + html + '</pre>')
			return response
	
 
 
# Generate a PDF File Venue List
def venue_pdf(request):
		# Create Bytestream buffer
		buf = io.BytesIO()
		# Create a canvas
		c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
		# Create a text object
		textob = c.beginText()
		textob.setTextOrigin(inch, inch)
		textob.setFont("Helvetica", 14)

			
		request.session['first_name'] = request.user.first_name
		request.session['last_name'] = request.user.last_name
		data = Lf_Reportes.objects.raw(f"""
		Select * From lf_reportes inner join lf_projects on 
		rep_fk_pr_key = pr_key inner join lf_employees on
		rep_fk_emp_key = emp_key
		where rep_user_name = '{request.user.username}';
		""")

		dataEmp = Lf_Employees.objects.raw(f"""
		Select *
		From lf_employees
		where emp_key = {data[0].rep_fk_emp_key_sup}
		""")

		request.session['rep_key'] = data[0].rep_key
		request.session['rep_fk_emp_key'] = data[0].rep_fk_emp_key
		request.session['emp_key'] = dataEmp[0].emp_key
		request.session['date'] = date.today().strftime(f"%B %d,%Y")
		print(f"Rep Key is::::::::::: ",{request.session['rep_key']})
		print("rep_key:",request.session['rep_key'])
		print("rep_fk_emp_key:",request.session['rep_fk_emp_key'])
		print("emp_key:",request.session['emp_key'])
		print("date: ",request.session['date'])
		
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
		venues = get_photo

	# Create blank list
		lines = []

		for venue in venues:
			lines.append(str(venue.ph_link))
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
