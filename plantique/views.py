from django.shortcuts import render,HttpResponse,redirect
from .import models
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        age=request.POST.get('age')
        email=request.POST.get('email')
        password=request.POST.get('password')
        image=request.FILES.get('image')
        if models.reg.objects.filter(email=email).exists():
            alert="<script>alert('email is already exist'); window.location.href='/register/';</script>;"
            return HttpResponse(alert)
        else:
            user=models.reg(name=name,age=age,email=email,password=password,image=image)
            user.save()
            return redirect('login')
    else:   
         return render(request, 'register.html')
     
def login(request):
    if request.method == "POST":
        # Step 1: Initial Login Phase
        if 'email' in request.POST and 'password' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = models.reg.objects.get(email=email, password=password)
                # Generate OTP
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                request.session['email'] = user.email

                # Send OTP via Email
                send_mail(
                    'Your Login OTP',
                    f'Your OTP is {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return render(request, 'otp.html', {'msg': 'OTP sent to your email.'})
            except models.reg.DoesNotExist:
                msg = "Invalid email or password"
                return render(request, 'login.html', {'msg': msg})

        # Step 2: OTP Verification Phase
        if 'otp' in request.POST:
            otp = request.POST.get('otp')
            if str(request.session.get('otp')) == otp:
                # OTP matches, log the user in
                return redirect('home')
            else:
                return render(request, 'otp.html', {'msg': 'Invalid OTP'})

    return render(request, 'login.html')

def otp(request):
    return render(request,'otp.html')
            
    
def home(request):
    return render(request,'home.html')

def profile(request):
    if "email" in request.session:
        user=request.session['email']
        try:
            client=models.reg.objects.get(email=user)
            return render(request,'profile.html',{'c':client})
        except models.reg.DoesNotExist:
            alert="<script> alert('user not found'); window.location.href='/profile/';</script>;"
            return HttpResponse(alert)
    else:
        alert="<script> alert('user not found'); window.location.href='/profile/';</script>;"
        return HttpResponse(alert)
    
def editprofile(request):
    if "email" in request.session:
        user=request.session['email']
        try:
            client=models.reg.objects.get(email=user)
            if request.method=='POST':
               client.name=request.POST.get('name')
               client.age=request.POST.get('age')
               client.email=request.POST.get('email')
               client.password=request.POST.get('password')
               client.image=request.FILES.get('image')
               client.save ()
               return redirect ('profile')
            else:
                return render(request,'editprofile.html',{'c':client})
            
        except models.reg.DoesNotExist:
            alert="<script>alert('user not found'); window.location.href='/profile/';</script>;"
            return HttpResponse(alert)    
    else:
        alert="<script> alert('user not found'); window.location.href='/profile/';</script>;"
        return HttpResponse(alert)    
    
def adminlogin(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        upassword=request.POST.get('upassword')
        auname='ADMIN'
        apassword='admin'
        if auname==uname:
            if apassword==upassword:
                return redirect('adminhome')
            return redirect('adminlogin')
        return redirect('adminlogin')
    return render(request,'adminlogin.html')

def adminhome(request):
    return render(request,'adminhome.html')    

def userlist(request):
    user=models.reg.objects.all()
    return render(request,'userlist.html',{'u':user})

def deleteuser(request,id):
    user=models.reg.objects.filter(id=id)
    user.delete()
    return redirect('userlist')

def sregister(request):
    if request.method=='POST':
        name=request.POST.get('name')
        age=request.POST.get('age')
        email=request.POST.get('email')
        password=request.POST.get('password')
        image=request.FILES.get('image')
        if models.sreg.objects.filter(email=email).exists():
            alert="<script>alert('email is already exist'); window.location.href='/sregister/';</script>;"
            return HttpResponse(alert)
        else:
            user=models.sreg(name=name,age=age,email=email,password=password,image=image)
            user.save()
            return redirect('slogin')
    else:   
         return render(request, 'sregister.html')  
     
def slogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=models.sreg.objects.get(email=email)
            if user.password==password:
                request.session['email']=email
                return redirect('shome')
            else:
                alert="<script>alert('invalid user'); window.location.href='/slogin/';</script>;"
                return HttpResponse(alert)
        except models.sreg.DoesNotExist:
               alert="<script>alert('user not found'); window.location.href='/slogin/';</script>;"
               return HttpResponse(alert)          
    else:
        return render(request,'slogin.html')     
    
def shome(request):
    return render(request,'shome.html')   

def sprofile(request):
    if "email" in request.session:
        user=request.session['email']
        try:
            client=models.sreg.objects.get(email=user)
            return render(request,'sprofile.html',{'c':client})
        except models.sreg.DoesNotExist:
            alert="<script> alert('user not found'); window.location.href='/sprofile/';</script>;"
            return HttpResponse(alert)
    else:
        alert="<script> alert('user not found'); window.location.href='/sprofile/';</script>;"
        return HttpResponse(alert)
    
def seditprofile(request):
    if "email" in request.session:
        user=request.session['email']
        try:
            client=models.sreg.objects.get(email=user)
            if request.method=='POST':
               client.name=request.POST.get('name')
               client.age=request.POST.get('age')
               client.email=request.POST.get('email')
               client.password=request.POST.get('password')
               client.image=request.FILES.get('image')
               client.save ()
               return redirect ('sprofile')
            else:
                return render(request,'seditprofile.html',{'c':client})
            
        except models.sreg.DoesNotExist:
            alert="<script>alert('user not found'); window.location.href='/sprofile/';</script>;"
            return HttpResponse(alert)    
    else:
        alert="<script> alert('user not found'); window.location.href='/sprofile/';</script>;"
        return HttpResponse(alert)

def saddproduct(request):
    if request.method=='POST':
        name=request.POST.get('name')
        image=request.FILES.get('image')
        quantity=request.POST.get('quantity')
        price=request.POST.get('price')

        user=models.sproduct(name=name,image=image,quantity=quantity,price=price)
        user.save()
        return redirect('sproductlist')   
    else:
        return render(request,'saddproduct.html') 
    
def sproductlist(request):
    product=models.sproduct.objects.all()
    return render(request,'sproductlist.html',{'p':product}) 
              
def sdeleteproduct(request,id):
    product=models.sproduct.objects.filter(id=id)
    product.delete()
    return redirect('sproductlist')

def seditproduct(request,id):
    p=models.sproduct.objects.get(id=id)
    if request.method=='POST':
        p.name=request.POST.get('name')
        p.image=request.FILES.get('image')
        p.quantity=request.POST.get('quantity')
        p.price=request.POST.get('price')
        p.save()
        return redirect('sproductlist')
    else:
        return render(request,'seditproduct.html',{'p':p})   
    
def logout(request):
    if 'email' in request.session:
        request.session.flush()
        return redirect('index')
    return redirect ('index')   

def sellerlist(request):
    user=models.sreg.objects.all()
    return render(request,'sellerlist.html',{'u':user})


def deleteseller(request,id):
    user=models.sreg.objects.filter(id=id)
    user.delete()
    return redirect('sellerlist')
 
def userproductlist(request):
    product=models.sproduct.objects.all()
    return render(request,'userproductlist.html',{'p':product})    
                  
def addtocart(request,id):
    if 'email' in request.session:
        user=request.session['email']
        client=models.reg.objects.get(email=user)
        product=models.sproduct.objects.get(id=id)
        if request.method=='POST':
            quantity=request.POST.get('quantity')
            quantity=int(quantity)
            total_price=product.price*quantity
            cart_item,created=models.cart.objects.get_or_create(user=client,product=product,defaults={'quantity':quantity,'total_price':total_price})
            if not created:
                cart_item.quantity=quantity
                cart_item.total_price=product.price*quantity
                cart_item.save()
                return redirect('cartlist')
            else:
                return redirect('cartlist')
        else:
             return render(request,'addtocart.html',{'p':product}) 
    else:
         return redirect('register')    
    
def cartlist(request):
    email=request.session.get('email')
    if 'email' in request.session:
        client=models.reg.objects.get(email=email)
        cartitems=models.cart.objects.filter(user=client)
        return render(request,'cartlist.html',{'cartitems':cartitems}) 
    else:  
        return render(request,'cartlist.html')            
                  
        

 
 
def buyitem(request, id):
    if 'email' in request.session:
        user = request.session['email']
        client = models.reg.objects.get(email=user)
        product = models.cart.objects.get(id=id)
        print(f"Product ID: {id}, Product: {product}")
        pr=models.sproduct.objects.get(id=product.product.id) 
        print(f"Product Details: {pr}")
        return render(request, 'buyitem.html', {'p': pr, 'user': client, 'c': product})
    else:
        return redirect('login')
    




from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest

def submit_buyitem(request, id):
    if 'email' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        user_email = request.session['email']
        client = models.reg.objects.get(email=user_email)

       
        cart_item = get_object_or_404(models.cart, id=id, user=client)
        product = cart_item.product
        quantity_requested = cart_item.quantity

        # Check stock
        # if product.quantity is None or product.quantity < quantity_requested:
        #     return HttpResponseBadRequest("Not enough stock available.")

        address = request.POST.get('address')
        phone_no = request.POST.get('phone_no')

        
        buy_item = models.buy(
            user=client,
            product=product,
            address=address,
            phone_no=phone_no
        )
        buy_item.save()

       
        product.quantity -= quantity_requested
        product.save()

       
        cart_item.delete()

        return redirect('paylist')

    else:
        return redirect('show_buyitem_form', id=id)

def paylist(request):
    if 'email' not in request.session:
        return redirect('login')

    user_email = request.session['email']
    client = models.reg.objects.get(email=user_email)

    # Get all buy entries for this user
    purchases = models.buy.objects.filter(user=client).select_related('product')

    return render(request, 'paylist.html', {'purchases': purchases, 'user': client})

def logout(request):
    if 'email' in request.session:
        request.session.flush()
        return redirect('index')
    return redirect ('index')  

def about(request):
    return render(request,'about.html')    


def orders(request):
    unassigned_orders = models.buy.objects.filter(assigned=False)
    return render(request, 'orders.html', {'orders': unassigned_orders})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import DeliveryPerson

def deliveryregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        zone = request.POST.get('zone')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        if models.DeliveryPerson.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email already exists'); window.location.href='/deliveryregister/';</script>")

        person = models.DeliveryPerson(
            name=name,
            age=age,
            email=email,
            phone=phone,
            password=password.strip(),  # avoid trailing spaces
            image=image,
            zone=zone,
            approved=False
        )
        person.save()
        return redirect('deliverylogin')

    return render(request, 'deliveryregister.html')


def deliverylogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            person = DeliveryPerson.objects.get(email=email)

            if person.password != password:
                return HttpResponse("<script>alert('Incorrect password'); window.location.href='/deliverylogin/';</script>")

            if not person.approved:
                return HttpResponse("<script>alert('You are not yet approved by admin. Please wait.'); window.location.href='/deliverylogin/';</script>")

            # Save session and redirect to deliveryhome
            request.session['delivery_email'] = person.email
            return redirect('deliveryhome')

        except DeliveryPerson.DoesNotExist:
            return HttpResponse("<script>alert('Email not registered'); window.location.href='/deliverylogin/';</script>")

    return render(request, 'deliverylogin.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . import models

def deliveryhome(request):
    if 'delivery_email' in request.session:
        email = request.session['delivery_email']
        person = models.DeliveryPerson.objects.get(email=email)

        # Exclude already delivered orders
        delivered_ids = models.DeliveredRecord.objects.values_list('assignment_id', flat=True)
        assigned_orders = models.AssignedDelivery.objects.filter(
            delivery_person=person
        ).exclude(id__in=delivered_ids)

        return render(request, 'deliveryhome.html', {
            'person': person,
            'orders': assigned_orders
        })
    else:
        return redirect('deliverylogin')


    
def deliverypersonlist(request):
    users = DeliveryPerson.objects.all()
    return render(request, 'deliverypersonlist.html', {'users': users})


def approvedeliveryperson(request, id):
    person = DeliveryPerson.objects.filter(id=id).first()
    if person:
        person.approved = True
        person.save()
    return redirect('deliverypersonlist')





def assigndelivery(request, id):
    order = models.buy.objects.get(id=id)
    delivery_people = models.DeliveryPerson.objects.filter(approved=True)

    if request.method == 'POST':
        delivery_person_id = request.POST.get('delivery_person_id')
        try:
            delivery_person = models.DeliveryPerson.objects.get(id=delivery_person_id)

            # Assign the order to the delivery person
            models.AssignedDelivery.objects.create(
                delivery_person=delivery_person,
                order=order
            )

            # ✅ Mark the order as assigned instead of deleting
            order.assigned = True
            order.save()

            return redirect('orders')

        except models.DeliveryPerson.DoesNotExist:
            return HttpResponse(
                f"<script>alert('Invalid delivery person'); window.location.href='/assigndelivery/{id}/';</script>"
            )

    return render(request, 'assigndelivery.html', {
        'order': order,
        'delivery_people': delivery_people
    })

 
# def deliverylogout(request):
#     if 'delivery_email' in request.session:
#         del request.session['delivery_email']
#     return redirect('deliverylogin')

def mark_delivered(request, assignment_id):
    if 'delivery_email' not in request.session:
        return redirect('deliverylogin')

    email = request.session['delivery_email']
    person = models.DeliveryPerson.objects.get(email=email)

    try:
        assignment = models.AssignedDelivery.objects.get(id=assignment_id, delivery_person=person)
        if request.method == 'POST':
            # prevent duplicate delivered records
            if not models.DeliveredRecord.objects.filter(assignment=assignment).exists():
                models.DeliveredRecord.objects.create(assignment=assignment)
        return redirect('deliveryhome')

    except models.AssignedDelivery.DoesNotExist:
        return HttpResponse(
            "<script>alert('Assignment not found'); window.location.href='/deliveryhome/';</script>"
        )


    
def delivered_orders(request):
    if 'delivery_email' not in request.session:
        return redirect('deliverylogin')

    email = request.session['delivery_email']
    person = models.DeliveryPerson.objects.get(email=email)

    delivered_records = models.DeliveredRecord.objects.filter(
        assignment__delivery_person=person
    ).select_related("assignment__order", "assignment__delivery_person")

    return render(request, 'delivered_orders.html', {
        'person': person,
        'delivered_orders': delivered_records
    })

# def delete_delivered_order(request, record_id):
#     if 'delivery_email' not in request.session:
#         return redirect('deliverylogin')

#     record = get_object_or_404(models.DeliveredRecord, id=record_id)

#     if request.method == 'POST':
#         record.delete()   # ✅ deletes permanently from DB
#         return redirect('delivered_orders')

#     return redirect('delivered_orders')

from .models import Feedbacks

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = int(request.POST.get('rating', 0))  # get rating from stars
        message = request.POST.get('message')

        Feedbacks.objects.create(
            name=name,
            email=email,
            message=message,
            rating=rating   # <-- save the star rating here
        )
        return redirect('home')  # redirect after submission
    return render(request, 'feedback.html')


from django.shortcuts import render, redirect
from .models import Feedbacks

def feedbacklist(request):
    feedbacks = Feedbacks.objects.all().order_by('-submitted_at')  # latest first
    return render(request, 'feedbacklist.html', {'feedbacks': feedbacks})


