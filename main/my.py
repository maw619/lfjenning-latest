import weasyprint

url = 'http://127.0.0.1:8000/auth/pdf/ad/Charlie23@/'
weasyprint.HTML(url).write_pdf('2.pdf')
