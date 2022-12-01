from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from main.models import *
from datetime import date  

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            #store login sessions
            request.session['username'] = request.user.username
            request.session['password'] = request.user.password
            
            request.session['first_name'] = request.user.first_name
            request.session['last_name'] = request.user.last_name
            
            
            
           
       
            if(Lf_Reportes.objects.filter(rep_name=request.user.username).first()):
            
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
                return redirect('home')
            else:
                #messages.success(request, 'You need to add an employee')
                return redirect('home')
        else:
            messages.success(request, 'There was a problem logging in, try again')
            return render(request, 'authenticate/login.html')

    else:
        return render(request, 'authenticate/login.html')
    
    
def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out')
    return redirect('login')
#['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
def register_user(request):
    employees = Lf_Employees.objects.all()
    form = CustomUserCreationForm()
    if request.method == "POST":
        
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('login')
        else:
             messages.success(request, 'You have errors. Try again')
             return redirect('register')
    return render(request, 'authenticate/register.html', {'form':form})

