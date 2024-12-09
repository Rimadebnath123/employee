from django.shortcuts import render,redirect
from employees.models import Employee
from django.core.paginator import Paginator



def homePage(request):
    emp = Employee.objects.all().order_by('id')  # Explicitly order by a field
    paginator = Paginator(emp, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'emp': page_obj,  # Paginated employee list
        'page_obj': page_obj,
    }
    return render(request, "index.html", data)

def Add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        role = request.POST.get('role')
        
        # Create and save a new employee instance
        emp = Employee(name=name, email=email, department=department, role=role)
        emp.save()
        
        # Redirect to the home page after saving
        return redirect('home')
    
    return render(request, 'index.html')  # Render the form template if GET request

def Edit(request):
    emp=Employee.objects.all()
    data={
        'emp':emp,
    }
    return render(request,"index.html",data)

def Update(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        role = request.POST.get('role')
        
        # Retrieve the existing employee instance by id and update its fields
        emp = Employee.objects.get(id=id)
        emp.name = name
        emp.email = email
        emp.department = department
        emp.role = role
        emp.save()
        
        return redirect('home')
        
    return render(request, "index.html")

def Delete(request,id):
    emp=Employee.objects.filter(id=id)
    emp.delete()
    
    data={
        'emp':emp,
    }
    return redirect('home')


