from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django. contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Contact,MembershipPlan,Trainer,Enrollment,Feedback

# Create your views here.

def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('phoneNumber')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if len(username) != 10:
            messages.warning(request, 'Phone Number must be 10 digits!')
            return redirect('/signup')

        if pass1 != pass2:
            messages.warning(request,'Password is not maching!')
            return redirect('/signup')

        try:
            if User.objects.get(username = username):
                messages.warning(request,'Phone Number is already taken')
                return redirect('/signup')
        except User.DoesNotExist:
            pass
        try:
            if User.objects.get(email = email):
                messages.warning(request,'Email is already taken')
                return redirect('/signup')
        except User.DoesNotExist:
            pass

        thisuser = User.objects.create_user(username, email, pass1)
        thisuser.save()
        messages.success(request, 'SignUp Successfully!')
        return redirect('/login')

    return render(request, 'signup.html')


def handle_login(request):
    if request.method == 'POST':
        username = request.POST.get('phoneNumber')
        password = request.POST.get('pass')
        thisUser = authenticate(username = username, password = password)
        if thisUser is not None:
            login(request, thisUser)
            messages.success(request, 'Logged In Successfully') 
            if request.user.is_superuser:
                return redirect('/admin_home')
            return redirect("/")
        else:
            messages.warning(request, 'Invalid UserName or Password')
            return redirect('/signup')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request,'Logged Out Successfully!')
    return redirect('/')



def contact(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login first! And try Again!')
        return redirect('/login')

    if request.method == "POST":
        name = request.POST.get('fullname')
        phone_no= request.POST.get('PhoneNumber')
        email = request.POST.get('email')
        description = request.POST.get('desc')
        query = Contact(name = name, phone_no = phone_no, email = email, description = description)
        query.save()
        messages.success(request, 'Thanks! you will get a response soon.')
        return redirect('/contact')
    return render(request,'contact.html')



def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login first and try Again!')
        return redirect('/login')

    membership = MembershipPlan.objects.all()
    trainer = Trainer.objects.all()
    context = {'membership': membership, 'trainer': trainer}

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone_no = request.POST.get('phone_no')
        dob = request.POST.get('dob')
        membership_plan = request.POST.get('membership_plan')
        trainer = request.POST.get('trainer')
        address = request.POST.get('address')
        query = Enrollment(fullname=fullname, email=email, gender=gender, phone_no=phone_no, dob=dob, membership_plan=membership_plan, trainer=trainer, address=address)
        query.save()
        messages.success(request, 'Enrollment Successful!')

    return render(request,'enroll.html',context)

def explore_plans(rerquest):
    plans = MembershipPlan.objects.all()
    context ={'plans':plans}
    return render(rerquest,"explore_plan.html",context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login first and try Again!')
        return redirect('/login')

    user_phone = request.user
    details = Enrollment.objects.filter(phone_no=user_phone)
    if len(details)<1:
        messages.warning(request, 'You are not enrolled yet! Please Enroll...')
        return redirect('/enroll')
    context = {'details': details}
    return render(request, 'profile.html', context)


def about(request):
    return render(request, 'about.html')

def feedback(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact_no = request.POST.get("contact_no")
        feedback = request.POST.get("feedback")
        query = Feedback(name=name, email=email, contact=contact_no, feedback=feedback)
        query.save()
        messages.success(request,"Feedback sent")
        return redirect("/")
    return render(request,"index.html")

# admin views

def dashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login as admin to access administration')
        return redirect('/admin_home')
    if not request.user.is_superuser:
              messages.warning(request, 'Login as admin to access administration')
              return redirect('/login')
    
        
    members = Enrollment.objects.all()
    membership_plans = MembershipPlan.objects.all()
    Trainers = Trainer.objects.all()
    Contacts = Contact.objects.all()
    feedbacks = Feedback.objects.all()
    context = {'members': members,'membership_plans':membership_plans,'Trainers':Trainers,'Contacts':Contacts,"feedbacks":feedbacks }
    return render(request,"admin_home.html", context)
 
# delete admin_contact route
def delete_contact(request,id):
    if  request.method == 'POST' :
        data =Contact.objects.get(id=id)
        data.delete()
        return redirect("/admin_home")
    data =Contact.objects.get(id=id)
    context={'data':data}
    return render(request,"admin_delete_contact.html",context)

#    add admin_member route
def add_member(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone_no = request.POST.get('phone_no')
        dob = request.POST.get('dob')
        membership_plan = request.POST.get('membership-plan')
        trainer = request.POST.get('trainer')
        address = request.POST.get('address')
        end_date = request.POST.get('end_date')
        payment_status = request.POST.get('payment_status')
        payment_amount = request.POST.get('payment_amount')
        query = Enrollment(fullname=fullname, email=email, gender=gender, phone_no=phone_no, dob=dob, membership_plan=membership_plan, trainer=trainer, address=address,end_date=end_date,payment_status=payment_status, payment_amount=payment_amount)
        query.save()
        return redirect("/admin_home")
    return render(request,"admin_home.html")
    

# Edit admin_member route
def edit_member(request,id):
    if request.method=="POST":
        fullname =request.POST["fullname"]
        email =request.POST["email"]
        gender =request.POST["gender"]
        phone_no =request.POST["phone_no"]
        dob =request.POST["dob"]
        membership_plan =request.POST["membership_plan"]
        trainer =request.POST["trainer"]
        address =request.POST["address"]
        end_date =request.POST["end_date"]
        payment_status =request.POST["payment_status"]
        payment_amount =request.POST["payment_amount"]
        edit = Enrollment.objects.get(id=id)
        edit.fullname = fullname
        edit.email = email
        edit.gender = gender
        edit.phone_no = phone_no
        edit.dob = dob
        edit.membership_plan = membership_plan
        edit.trainer = trainer
        edit.address = address
        edit.end_date = end_date
        edit.payment_status = payment_status
        edit.payment_amount = payment_amount
        edit.save()
        # print(fullname,email,gender,phone_no,dob,membership_plan,trainer,address,end_date,payment_status,payment_amount) 
        return redirect("/admin_home")
    data = Enrollment.objects.get(id=id)
    context ={"data":data}
    return render(request,"admin_edit_member.html",context)
       
# delete admin_member route
def delete_member(request,id):
    if  request.method == 'POST' :
        data =Enrollment.objects.get(id=id)
        data.delete()
        return redirect("/admin_home")
    data =Enrollment.objects.get(id=id)
    context={'data':data}
    return render(request,"admin_delete_member.html",context)



# add admin membership route
def add_membership(request):
    if request.method == 'POST':
        plan = request.POST.get('plan')
        duration = request.POST.get('duration')
        offer = request.POST.get('offer')
        price = request.POST.get('price')
        query = MembershipPlan(plan=plan, duration=duration, offer=offer, price=price)
        query.save()

    return redirect("/admin_home")

# Edit admin_membership route
def edit_membership(request,id):
    if request.method=="POST":
        plan =request.POST["plan"]
        duration =request.POST["duration"]
        offer =request.POST["offer"]
        price =request.POST["price"]
        edit = MembershipPlan.objects.get(id=id)
        edit.plan = plan
        edit.duration = duration
        edit.offer = offer
        edit.price = price
        edit.save()
        # print(plan,price)
        return redirect("/admin_home")
    data = MembershipPlan.objects.get(id=id)
    context = {"data":data}
    return render(request,"admin_edit_membership.html",context)

# delete admin_membership route
def delete_membership(request,id):
    if  request.method == 'POST' :
        data =MembershipPlan.objects.get(id=id)
        data.delete()
        return redirect("/admin_home")
    data =MembershipPlan.objects.get(id=id)
    context={'data':data}
    return render(request,"admin_delete_membership.html",context)

# add admin trainer route
def add_trainer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        gender = request.POST.get('gender')
        salary = request.POST.get('salary')
        query = Trainer(name=name, phone_no=phone_no, gender=gender, salary=salary)
        query.save()

    return redirect("/admin_home")

# Edit admin trainer  route
def edit_trainer(request,id):
    if request.method=="POST":
        name =request.POST["name"]
        phone_no =request.POST["phone_no"]
        gender =request.POST["gender"]
        salary =request.POST["salary"]
        
        edit = Trainer.objects.get(id=id)
        edit.name = name
        edit.phone_no = phone_no
        edit.gender = gender
        edit.salary = salary
        edit.save()
        # print(name,phone_no,gender,salary,join_date)
        return redirect("/admin_home")
    data = Trainer.objects.get(id=id)
    context = {"data":data}
    return render(request,"admin_edit_trainer.html",context)


# delete admin_trainer route
def delete_trainer(request,id):
    if  request.method == 'POST' :
        data =Trainer.objects.get(id=id)
        data.delete()
        return redirect("/admin_home")
    data =Trainer.objects.get(id=id)
    context={'data':data}
    return render(request,"admin_delete_trainer.html",context)


# delete feedback route
def delete_feedback(request,id):
    if  request.method == 'POST' :
        data =Feedback.objects.get(id=id)
        data.delete()
        return redirect("/admin_home")
    data =Feedback.objects.get(id=id)
    context={'data':data}
    return render(request,"admin_delete_feedback.html",context)



 


