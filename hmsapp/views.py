from unicodedata import category
from django.shortcuts import render,redirect
import math
import random
from django.views.generic import ListView
import os
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User,auth
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from datetime import datetime,timedelta
from django.db import connection
cursor = connection.cursor()


# from django.db.models import Avg, Count, Min, Sum
# from django.db import connection
# cursor = connection.cursor()

# Create your views here.
login_required(login_url='log_in')
def home(request):
    cursor.execute( 'SELECT count(*) FROM hmsapp_appointment  ')
    total_pro = cursor.fetchone()
    
    for i in total_pro:
        total_appoint=i
    cursor.execute( 'SELECT count(*) FROM hmsapp_appointment where requested=2')
    confirm_appoint = cursor.fetchone()
    for i in confirm_appoint:
        con_appoint=i
    cursor.execute( 'SELECT count(*) FROM hmsapp_appointment where requested=1')
    req_appoint = cursor.fetchone()
    for i in req_appoint:
        r_appoint=i
    cursor.execute( 'SELECT count(*) FROM hmsapp_doctor ')
    total_doc = cursor.fetchone()
    
    for i in total_doc:
        total_doctor=i
    t_l_application = leave.objects.filter(approve=0).count()

    if not request.user.is_superuser:
        user_id = user_ext.objects.get(user_id=request.user.id)
        u_appointment = appointment.objects.filter(user_id=user_id).count()
   
        if request.user.user_ext.rol_id.id == 2:
            doc = doctor.objects.get(user_id=request.user.id)
            doc_appointment = appointment.objects.filter(doc_id=doc.id).count()
            doc_Approve_appoint = appointment.objects.filter(doc_id=doc.id,requested=2).count()
            today = datetime.now().date()
            today_appoint = appointment.objects.filter(doc_id=doc.id,date=today).count()
        else:
            doc_appointment=0
            doc_Approve_appoint=0
            today_appoint=0

    else:
        doc_appointment=0
        doc_Approve_appoint=0
        today_appoint=0
        u_appointment=0

    return render(request,'home.html',{'total_appoint':total_appoint,'total_doctor':total_doctor,'con_appoint':con_appoint,'r_appoint':r_appoint,'t_l_application':t_l_application,'u_appointment':u_appointment,'doc_appointment':doc_appointment,'doc_Approve_appoint':doc_Approve_appoint,'today_appoint':today_appoint})

def log_in(request):
    if request.method=="POST":
        uname = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=uname,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'User does not exist...')
            return redirect('sign_in')
    return render(request,'log_in.html')
def sendMail(email,password,username):       
    subject = 'Hospital '
    message = 'Dear sir/madam, your Username='+username+' and Password='+password+' thankyou, '
    html_content = '<p>Dear sir/Madam</p><br><p> you are successfully registered...</p><br><p> your <strong>username='+username+'</strong> and <strong>password='+password +'</strong></p><br><p> Thankyou</p>'
    
    recipient = email    #  recipient =request.POST["inputTagName"]
    send_mail(subject, 
        message, settings.EMAIL_HOST_USER, [recipient],html_message=html_content)

def generateOTP(request) :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = ""
 
   # length of password can be changed
   # by changing value in range
    for len in range(8):
        random_char = random.choice(digits)
        password += random_char
    
    return JsonResponse({'status':password})

def sign_in(request):
    if request.method=='POST':
        fname = request.POST['fname']
        username = request.POST['username']
        lname = request.POST['lname']
        address = request.POST['address']
        phone = request.POST.get('phone')
        print(phone)
        gender = request.POST['gender']
        dob = request.POST['dob']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']
        pro = request.FILES.get('image')
        if pro is not None:
            pro_pic = pro
        else:
            pro_pic ='static/image/user.jpg'
        try:    
            if password==c_password:
                if User.objects.filter(username = username).exists():
                   messages.info(request,'username already exist...')
                   return redirect('sign_in')
                else:
                    user = User.objects.create_user(
                        first_name=fname,
                        last_name = lname,
                        username = username,
                        password=password,
                        email=email,
                    )
                    rol_id = role.objects.get(id=3)
                    e_user = user_ext(
                        user_id= User.objects.get(id=user.id),
                        dob = dob,
                        image=pro_pic,
                        gender=gender,
                        phone=phone,
                        address=address,
                        rol_id = rol_id
                    )
                    
            else:
                messages.info(request,'password was incorrect...')
                return redirect('sign_in')
        except:
            messages.info(request,'network error...')
            return redirect('log_in')
        else:
            print(1)
            user.save()
            e_user.save()
            my_patient_group = Group.objects.get_or_create(name='USER')
            my_patient_group[0].user_set.add(user)
            sendMail(email,password,username)
            messages.info(request,'Registered successfully....')
            return redirect('log_in')
    return render(request,'sign_in.html')
   
login_required(login_url='log_in')
def profile(request):
    if request.user.is_superuser:
        usr = request.user.id
        user_e = User.objects.get(id=usr)
        return render(request,'profile/profile.html',{'user_ext':user_e})
    else:
        usr = request.user.id
        user_e = user_ext.objects.get(user_id=usr)
        return render(request,'profile/profile.html',{'user_ext':user_e})


def department_view(request):
    return render(request,'admin/category.html')
def listDpartment(request):
    dep_m = department.objects.all()
    deprt = Paginator(dep_m, 5)
    page_number = request.POST.get('page_no')
    print(page_number)
    dep = deprt.get_page(page_number)
    print(dep)
    return render(request,'admin/listcategory.html',{'dep':dep})
@csrf_exempt
def addDepartment(request):
    if request.method=="POST":
        name = request.POST.get('dpt_name')
        edit_id = int(request.POST.get('hidden_id'))
        if edit_id > 0:
            dep = department.objects.get(id=edit_id)
            dep.name = name
            dep.save()
            return JsonResponse({'status':1})
        else:
            dep = department(
                name=name
            )
            dep.save()
            return JsonResponse({'status':1})

def doctors(request):
    dep = department.objects.all()
    return render(request,'admin/doctor.html',{'dep':dep})
    
@csrf_exempt
def saveDoctor(request):
    if request.method=="POST":
        name = request.POST.get('doctor')
        dep_id = request.POST.get('depart')
        dep = department.objects.get(id=dep_id)
        hidden_id = int(request.POST.get('hidden_id'))
        if hidden_id>0:
            doc = doctor.objects.get(id=hidden_id)
            doc.name = name
            doc.dep_id = dep
            doc.save() 
            return JsonResponse({'status':1})
        else:
            doc = doctor(
                name=name,
                dep_id=dep
            )
            doc.save()
            return JsonResponse({'status':1})

def listDoctors(request):
    
    docs = doctor.objects.all()
    doct = Paginator(docs, 5)
    page_number = request.POST.get('page_no')
    print(page_number)
    doc = doct.get_page(page_number)
    print(doc)

    return render(request,'admin/listdoc.html',{'doc':doc})


def takeAppointment(request):
    doc = doctor.objects.all()
    dep = department.objects.all()
    return render(request,'user/appointment.html',{'doc':doc,'dep':dep})
@csrf_exempt
def addapointment(request,pk):
    if request.method=='POST':
        user = user_ext.objects.get(user_id=pk)
        doc_id = request.POST.get('doctor')
        doc = doctor.objects.get(user_id=doc_id)
        date = request.POST.get('date')
        depart=request.POST.get('depart')
        time = request.POST.get('time')
        dep = department.objects.get(id=depart)
        appoint = appointment(
            user_id=user,
            date=date,
            doc_id = doc,
            requested = 1,
            department=dep, 
            time = time
        )
        appoint.save()
        return JsonResponse({'status':1})
def viewPatients(request):
    pati = user_ext.objects.all()
    paginator = Paginator(pati, 5)
    page_number = request.POST.get('page_no')
    print(page_number)
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    rol = role.objects.all()
    dep = department.objects.all()

    return render(request,'admin/viewUsers.html',{'pati':pati,'role':rol,'dep':dep,'page_obj': page_obj})

def viewAppointment(request):
    user = request.user.id
    today = datetime.now()
    usr = user_ext.objects.get(user_id=user)
    appoin = appointment.objects.filter(user_id = usr.id) 

    appointmen = Paginator(appoin, 5)
    page_number = request.POST.get('page_no')
    print(page_number)
    appointments = appointmen.get_page(page_number)
    print(appointments)
    
    return render(request,'user/viewappointment.html',{'appointments':appointments,'today':today})

def adViewAppointment(request):
    app = appointment.objects.all()
    deprt = department.objects.all()
    today = datetime.now()
    rol = role.objects.all()
    appoints = Paginator(app, 5)
    page_number = request.POST.get('page_no')
    print(page_number)
    appoint = appoints.get_page(page_number)
    print(appoint)
    return render(request,'admin/viewAppointment.html',{'appoint':appoint,'deprt':deprt,'today':today})

def log_out(request):
    auth.logout(request)
    return redirect('log_in')
@csrf_exempt
def approve(request):
    if request.method=='POST':
        id = request.POST.get('appoint_id')
        update = appointment.objects.get(id=id)
        update.requested=2
        update.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

@csrf_exempt
def cancelappointment(request):
    if request.method=='POST':
        id = request.POST.get('appoint_id')
        update = appointment.objects.get(id=id)
        update.requested = 3
        update.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})
@csrf_exempt
def updateDoctor(request):
    if request.method=='POST':
        appoint_id = request.POST.get('appionment_id')
        doc_id = request.POST.get('doc_id')
        print(doc_id)
        updDoc = appointment.objects.get(id=appoint_id)
        # doctor_id = User.objects.get(id=doc_id)
        docter = doctor.objects.get(user_id=doc_id)
        cat_id = request.POST.get('cat_id')
        cat = department.objects.get(id=cat_id)
        updDoc.doc_id = docter
        updDoc.department = cat
        updDoc.save()
        return JsonResponse({'status':1})

    else:
         return JsonResponse({'status':0})

@csrf_exempt
def get_doc(request):
    if request.method=='POST':
        dep_id = request.POST.get('departid')
        ap_date = request.POST.get('ap_date')
        dep = department.objects.get(id=dep_id)

        doc =list(User.objects.filter(doctor__dep_id=dep).exclude(leave__leave_date=ap_date,leave__approve=1).values())
        print(doc)
        responcedata={'doc':doc}
        return JsonResponse(responcedata)
        
def editProfile(request):
    user = request.user
    update = User.objects.get(id=user.id)
    user_e = user_ext.objects.get(user_id = update )
    if request.method=="POST":
        update.first_name = request.POST['fname']
        update.username = request.POST['username']
        update.last_name = request.POST['lname']
        user_e.address = request.POST['address']
        user_e.phone = request.POST['phone']
        user_e.gender = request.POST['gender']
        pro = request.FILES.get('edit_image')
       
        user_e.dob = request.POST['dob']
        update.email = request.POST['email']
        
        
        if pro is not None:
            user_e.image = pro
            if pro != request.POST.get('edit_pic'):
                if request.POST.get('edit_pic')!='/static/image/user.jpg':
                    # os.remove(update.user_ext.image.path)
                    pass
            update.save()
            user_e.save() 
            return redirect('home')
        else:
            user_e.image = request.POST.get('edit_pic') 
            img = request.POST.get('edit_pic') 
            print(img)
            update.save()
            user_e.save()
            return redirect('home')
@csrf_exempt        
def delete_patient(request,pk):
    if request.method=="POST":
        del_patient = user_ext.objects.get(id=pk)
        del_patient.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':2})
@csrf_exempt        
def delete_category(request,pk):
    if request.method=="POST":
        del_patient = department.objects.get(id=pk)
        del_patient.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':2})

@csrf_exempt        
def delete_doc(request,pk):
    if request.method=="POST":
        del_doc = doctor.objects.get(id=pk)
        user = User.objects.get(id=del_doc.user_id.id)
        my_patient_group = Group.objects.get_or_create(name='PATIENT')
        my_patient_group[0].user_set.add(user)
        usr = user_ext.objects.get(user_id=user.id)
        rol = role.objects.get(id =3)
        usr.rol_id = rol
        usr.save()
        del_doc.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':2})


def firts_page(request):
    return render(request,'first_page.html')

def roles(request):
    return render(request,'admin/roles.html')


@csrf_exempt
def saveRole(request):
    if request.method=="POST":
        name = request.POST.get('role_name')
        edit_id = int(request.POST.get('hidden_id'))
        if edit_id > 0:
            rol = role.objects.get(id=edit_id)
            rol.name = name
            rol.save()
            return JsonResponse({'status':1})
        else:
            rol = role(
                name=name
            )
            rol.save()
            return JsonResponse({'status':1})

def listRole(request):
    rols = role.objects.all()
    rol_s = Paginator(rols, 5)
    page_number = request.POST.get('page_no')
    print(page_number)
    rol = rol_s.get_page(page_number)
    print(rol)

    return render(request,'admin/rolelist.html',{'rol':rol})

@csrf_exempt 
def updaterole(request):
    if request.method=='POST':
        user_id = request.POST.get('user_id')
        rol_id = request.POST.get('rol_id')
        usr = user_ext.objects.get(id=user_id)
        ussr = User.objects.get(id = usr.user_id.id)
        if rol_id == '2':
            dep_id = request.POST.get('dep_id')
            dep = department.objects.get(id=dep_id)
            doc = doctor(
                user_id = ussr,
                dep_id = dep
            )
            doc.save()
        rol = role.objects.get(id =rol_id )
        usr.rol_id = rol
        usr.save()

        print(type(rol_id))
        if rol_id == '1':
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(ussr)
            print(my_admin_group)
            return JsonResponse({'status':1})
        elif rol_id == '2':
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(ussr)
            return JsonResponse({'status':1})
        elif rol_id == '3':
            
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(ussr)
            print(my_patient_group)
            return JsonResponse({'status':1})
        else:
            return JsonResponse({'status':2})
    else:
        return JsonResponse({'status':1})



def view_Patients(request):
    patien_ = user_ext.objects.filter(rol_id=3)
    pa_s = Paginator(patien_, 5)
    page_number = request.POST.get('page_no')
    print(page_number)
    patien_ts = pa_s.get_page(page_number)
    print(patien_ts)

    return render(request,'admin/patients.html',{'pati':patien_ts})
@csrf_exempt        
def view_doc_wise_patient(request,pk):
    doc = doctor.objects.get(user_id=pk)
    dec_appo = appointment.objects.filter(doc_id=doc.id)
    dec_appoin = Paginator(dec_appo, 5)
    page_number = request.POST.get('page_no')
    print(page_number)
    dec_appointments = dec_appoin.get_page(page_number)
    print(dec_appointments)

   
    return render(request,'doctor/doc_patients.html',{'appointments':dec_appointments})


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()    

def applyLeave(request):
    return render(request,'doctor/apply_lave.html')

@csrf_exempt
def leave_apply(request):
    if request.method=='POST':
        reason = request.POST.get('reason')
        user_id = request.user.id
        user = User.objects.get(id = user_id)
        doc_id = doctor.objects.get(user_id = user_id)
        date = request.POST.get('l_date')
        leave_data=leave(
            user_id=user,
            reason=reason,
            leave_date=date,
            approve = 0,
        )
        leave_data.save()
        leave_data.doc_id.add(doc_id)
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':2})
        

def leaveApplications(request):
    l = leave.objects.all() 
    lea = Paginator(l, 5)
    page_number = request.POST.get('page_no')
    print(page_number)
    leaves = lea.get_page(page_number)
    print(leaves)
    return render(request,'admin/leaveapplications.html',{'leaves':leaves})
@csrf_exempt
def leave_approve(request):
    if request.method=='POST':
        id = request.POST.get('leave_id')
        update = leave.objects.get(id=id)
        update.approve=1
        update.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':1})


def list_leave(request,pk):
    if pk>0:
        user_id = User.objects.get(id=pk)
        leave_Detail = leave.objects.filter(user_id = user_id.id)
        return render(request,'doctor/leave_list.html',{'leave_Detail':leave_Detail})


@csrf_exempt
def cancel_leave(request):
    if request.method=='POST':
        id = request.POST.get('leave_id')
        deleteLeave = leave.objects.get(id=id)
        deleteLeave.approve = 3
        deleteLeave.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':2})

def about(request):
    return render(request,'about.html')



    



   



        





