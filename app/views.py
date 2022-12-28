from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Person,Count
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# from django.contrib.sessions.models.Session
import random

# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name','none')
        password1 = request.POST.get('password1', 'none')
        password2 = request.POST.get('password2', 'none')
        email = request.POST.get('email','')
        retrive = Person.objects.filter(username = name)

        if len(retrive) == 0:
            if password1 == password2:
                if name != 'none':
                    obj = Person(username = name,password = password1,email = email)
                    obj.save()
                    amount = Count(user = obj, amount = 100000)
                    amount.save()
                    messages.info(request,'Sign successful')
                    return redirect('login')
                else:
                    messages.info(request,'Username can\'t be empty')
                    return redirect('index')
            else:
                messages.info(request,'password doesn\'t match')
                return redirect('/')

        else:
            messages.info(request,'Username already exists')
            return redirect('/')
    else:
        return render(request,'index.html')

def login(request):
    if request.method == 'POST':
        name = request.POST.get('uname',' ')
        password = request.POST.get('pass',' ')
        if name == ' ' or name == '':
            messages.info(request,'Username can\'t be empty')
            return redirect('login')
        if password == ' ' or password == '' :
            messages.info(request, 'Password can\'t be empty')
            return redirect('login')
        obj = Person.objects.filter(username = name,password = password)
        if obj:
            amount = Count.objects.filter(user_id = obj[0].id)
        else:
            messages.info(request,'login detials doesnot exists')
            return redirect('login')
        return render(request,'detials.html',{'data':obj[0],'amount':amount[0]})
    else:
        return render(request,'login.html')

def transactions(request,id):
    print(id)
    recive = request.POST.get('reciver','')
    money = float(request.POST.get('money',0))
    password = request.POST.get('p', '')
    obj = Person.objects.filter(id = id)
    if obj[0].username == recive:
        messages.info(request,"You can't send money to yourself")
        return redirect(f'{id}')
    # print(f"database:- {obj[0].password}")
    # print(f"input:- {password},money:-{money},recive is {recive}")
    if recive != '':
        reciver = Person.objects.filter(username = recive)
        user_id = reciver[0].id
        print(f"reciver id {reciver[0].id}")
        if len(reciver) != 0:
            # password of sender checked and amount is didected from sender
            if obj[0].password == password:
                amount = Count.objects.filter(user_id = id)
                if money > amount[0].amount:
                    messages.info(request,'insufficiant balance')
                    return redirect('login')
                else:
                    #only if no else for this if
                    if money < 0:
                        money = -(money)
                    total = amount[0].amount - money
                    update = Count.objects.filter(user_id = id).update(amount = total)
################################################# reciver end##############################################################################
                    add_money = Count.objects.filter(user_id = user_id)
                    print(add_money)
                    add = add_money[0].amount + money
                    update_data = Count.objects.filter(user_id = user_id).update(amount = add)
                    messages.success(request,f'Transaction successful.You have Successfully sent Rs.{money} to {recive}.')
                    return redirect('login')
            else:
                messages.info(request,'Incorrect password')
                return redirect('login')
        else:
            messages.info(request,'User doesn\'t exist')
            return redirect('login')
    else:
        messages.info(request,'Username can\'t be empty')
        return redirect('login')

def delete(request,id):
    remove = Person.objects.filter(id = id).delete()
    remove_account = Count.objects.filter(user = remove).delete()
    messages.info(request,'You have deleted you account successfully.We miss you')
    return redirect('index')

# def notifications(request):
def forgot(request):
    if request.method == "POST":
        name = request.POST.get('for_name','')
        retrive = Person.objects.filter(username = name)
        user_email = retrive[0].email
        otp = random.randint(1000,9999)
        request.session['email_otp'] = otp
        msg = f"Your otp is {otp}"


        send_mail('Email vrification OTP',msg,settings.EMAIL_HOST_USER,[user_email],fail_silently=False)
        return render(request,'email_verified.html',{'name':name})
    else:
        return render(request,'forgot.html')

def email_verified(request,name):
    if request.method == 'POST':
        u_otp = int(request.POST.get('mail_otp',''))
        otp = request.session['email_otp']

        if otp == '':
            messages.info(request,'OTP feild can\'t be empty')
            return redirect('login')
        else:
            if otp == u_otp:
                retrive = Person.objects.filter(username = name)
                return render(request,'email_verified.html',{'retrive':retrive[0],'password':retrive[0].password})
            else:
                messages.error(request,'Wrong OTP')
                return redirect('login')




